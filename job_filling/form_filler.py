"""CLI entry point: fill academic job application forms automatically."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys

from playwright.async_api import Page

import browser as br
import field_extractor as fe
import llm_matcher_local as lml
import profile_store as ps

# ── Colours for terminal output ──────────────────────────────────────────────

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def _sanitize_key(label: str) -> str:
    """Turn a form label into a short snake_case key.

    Strips verbose descriptions — keeps only the meaningful part before
    any long explanation (e.g. "Title:*" stays "title", not the full paragraph).
    """
    # Take only the part before " - " or first sentence if very long
    s = label.split(" - ")[0].strip()
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s[:40]


def _check_label_mismatch(key: str, current_label: str, learned: dict) -> str | None:
    """Return a warning string if the current label differs significantly from stored."""
    if key not in learned:
        return None
    stored = learned[key]
    stored_label = stored.get("label", "")
    if not stored_label:
        return None
    # Normalise for comparison
    cur_norm = re.sub(r"[^a-z0-9]", "", current_label.lower())
    sto_norm = re.sub(r"[^a-z0-9]", "", stored_label.lower())
    if cur_norm == sto_norm:
        return None
    # Check if one contains the other (minor difference is OK)
    if cur_norm in sto_norm or sto_norm in cur_norm:
        return None
    return (
        f"Field '{key}' label differs from stored:\n"
        f"      Stored:  \"{stored_label}\"\n"
        f"      Current: \"{current_label}\""
    )


# ── Core logic ───────────────────────────────────────────────────────────────

async def fill_field(page: Page, instruction: dict) -> None:
    """Execute a single auto-fill instruction on the page."""
    sel = instruction["selector"]
    val = instruction["value"]
    action = instruction.get("action", "fill")
    listbox_id = instruction.get("listbox_id", "")

    if action == "custom-select" and listbox_id:
        await page.click(sel)
        await page.wait_for_timeout(300)
        clicked = await page.evaluate(f"""
        (val) => {{
            const listbox = document.getElementById({repr(listbox_id)});
            if (!listbox) return false;
            for (const li of listbox.children) {{
                const text = li.innerText?.trim() || '';
                const dataVal = li.getAttribute('data-value') || li.getAttribute('value') || text;
                if (dataVal === val || text === val) {{
                    li.click();
                    return true;
                }}
            }}
            return false;
        }}
        """, val)
        if not clicked:
            await page.fill(sel, val)
            await page.wait_for_timeout(300)
            await page.keyboard.press("Enter")
    elif action == "search-select":
        hidden_id = instruction.get("hidden_id", "")
        field_id = sel.lstrip("#")  # e.g. "major_1Text"

        # Find the search link via aria-controls (works for both SearchDialog and SelectUniDialog)
        search_link = page.locator(f'a[aria-controls="{field_id}"]')
        if await search_link.count() == 0:
            raise Exception(f"Could not find search link for {sel}")

        # Click the search link and capture the popup
        context = page.context
        pages_before = {pg.url for pg in context.pages}

        await search_link.click()
        await page.wait_for_timeout(2000)

        # Find the new popup page
        popup = None
        for pg in context.pages:
            if pg.url not in pages_before:
                popup = pg
                break

        if not popup:
            raise Exception("Search popup did not open")

        await popup.wait_for_load_state("domcontentloaded")

        # Find search input (works for both SearchDialog and SelectUniDialog)
        search_input = popup.locator('input[type="text"]').first
        await search_input.fill(val)

        # Click Search button
        search_btn = popup.locator(
            'input[type="submit"][value="Search"], '
            'input[type="button"][value="Search"]'
        )
        if await search_btn.count() > 0:
            await search_btn.first.click()
        else:
            await search_input.press("Enter")

        await popup.wait_for_timeout(2000)
        await popup.wait_for_load_state("domcontentloaded")

        # Get results from select box (try multiple known IDs)
        result = await popup.evaluate("""() => {
            const selectors = [
                '#ctl00_MainContentPlaceHolder_SearchSelectBox',
                '#ctl00_MainContentPlaceHolder__objUniListbox',
                'select[size]',
            ];
            for (const s of selectors) {
                const sel = document.querySelector(s);
                if (sel && sel.options.length > 0) {
                    return {
                        selector: s,
                        options: Array.from(sel.options).map(o => ({value: o.value, text: o.text})),
                    };
                }
            }
            return null;
        }""")

        if not result or not result["options"]:
            # Fallback: try manual entry via "didn't find" checkbox + text box
            manual_ok = await popup.evaluate("""(val) => {
                // Find and click the "didn't find" checkbox
                const cbs = document.querySelectorAll('input[type="checkbox"]');
                let checked = false;
                for (const cb of cbs) {
                    cb.click();
                    checked = true;
                    break;
                }
                if (!checked) return false;
                // Find the manual entry text box (OtherValue / EntryText)
                const inp = document.querySelector(
                    '#ctl00_MainContentPlaceHolder_OtherValue, ' +
                    'input[id*="OtherValue"], input[id*="EntryText"], input[id*="entryText"]'
                );
                if (!inp) return false;
                inp.value = val;
                return true;
            }""", val)
            if not manual_ok:
                await popup.close()
                raise Exception(f"No search results for '{val}' and no manual entry option")
            await popup.wait_for_timeout(300)
            select_btn = popup.locator('input[type="button"][value="Select"]')
            await select_btn.click()
            await page.wait_for_timeout(500)
            return

        options = result["options"]
        select_sel = result["selector"]

        # Find best match: exact > shortest containing match > first
        best_value = None
        val_lower = val.lower()
        # 1. Exact match
        for o in options:
            if o["text"].lower() == val_lower:
                best_value = o["value"]
                break
        # 2. Contains match - prefer shortest text (most specific)
        if not best_value:
            candidates = [
                o for o in options if val_lower in o["text"].lower()
            ]
            if candidates:
                candidates.sort(key=lambda o: len(o["text"]))
                best_value = candidates[0]["value"]
        # 3. Fallback: first option
        if not best_value:
            best_value = options[0]["value"]

        await popup.locator(select_sel).select_option(best_value)

        # Click Select button
        select_btn = popup.locator('input[type="button"][value="Select"]')
        await select_btn.click()
        await page.wait_for_timeout(500)
    elif action == "select":
        await page.select_option(sel, val)
    elif action == "check":
        if val:
            locator = page.locator(f'{sel}[value="{val}"]')
            if await locator.count() > 0:
                await locator.click()
            else:
                await page.click(sel)
        else:
            await page.click(sel)
    elif action == "date-fill":
        # Element UI date picker: click → clear → type → Enter
        await page.click(sel)
        await page.wait_for_timeout(300)
        await page.keyboard.press("Meta+a")
        await page.wait_for_timeout(100)
        await page.keyboard.press("Backspace")
        await page.wait_for_timeout(200)
        await page.keyboard.type(val, delay=50)
        await page.wait_for_timeout(300)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(300)
    else:
        # Auto-detect Element UI date picker and use keyboard input
        is_date = await page.evaluate(
            """(sel) => {
                var el = document.querySelector(sel);
                return el ? !!el.closest(".el-date-editor") : false;
            }""", sel)
        if is_date:
            await page.click(sel)
            await page.wait_for_timeout(300)
            await page.keyboard.press("Meta+a")
            await page.wait_for_timeout(100)
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(200)
            await page.keyboard.type(val, delay=50)
            await page.wait_for_timeout(300)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(300)
        else:
            await page.fill(sel, val)


async def fill_page(page: Page, profile_path=None) -> None:
    """Extract fields, match via local rules only, fill what we can."""
    path = profile_path or ps.DEFAULT_PATH
    profile = ps.load_profile(path)
    learned = profile.get("learned_fields", {})

    print(f"{CYAN}Extracting form fields...{RESET}")
    fields = await fe.extract_fields(page)
    if not fields:
        print(f"{YELLOW}No form fields found on this page.{RESET}")
        return

    print(f"  Found {len(fields)} fields.")

    fields_json = [f.describe() for f in fields]

    print(f"{CYAN}Matching fields to your profile (local rules)...{RESET}")
    result = lml.match_fields_local(fields_json, profile)

    auto_fill = result.get("auto_fill", [])
    need_input = result.get("need_input", [])

    # ── Auto-fill with mismatch warnings ─────────────────────────────────
    if auto_fill:
        print(f"\n{GREEN}Auto-filling {len(auto_fill)} fields:{RESET}")
        for inst in auto_fill:
            label = inst.get("label", inst["selector"])
            key = _sanitize_key(label)

            # Check for label mismatch warning
            warning = _check_label_mismatch(key, label, learned)
            if warning:
                print(f"  {RED}⚠ WARNING:{RESET} {warning}")
                print(f"      Still filling with value: {inst['value'][:60]}")

            print(f"  {GREEN}✓{RESET} {label} → {inst['value'][:60]}")
            try:
                await fill_field(page, inst)
            except Exception as e:
                print(f"  {YELLOW}⚠ Failed to fill {inst['selector']}: {e}{RESET}")

    if need_input:
        print(f"\n{YELLOW}Could not match {len(need_input)} fields:{RESET}")
        for item in need_input:
            label = item.get("label", item["selector"])
            print(f"  {YELLOW}○{RESET} {label}")

    print(f"\n{GREEN}Page fill complete.{RESET}")


def _save_learned_field(key: str, label: str, value: str, path=None) -> None:
    """Save a field with its label and value to learned_fields."""
    path = path or ps.DEFAULT_PATH
    profile = ps.load_profile(path)
    learned = profile.get("learned_fields", {})

    learned[key] = {
        "value": value,
        "label": label,
    }
    profile["learned_fields"] = learned
    ps.save_profile(profile, path)
    print(f"  {CYAN}Saved: learned_fields.{key} = {value}{RESET}")


async def read_back_and_learn(page: Page, profile_path=None) -> None:
    """Read ALL form fields from page (including empty ones), save to learned_fields.

    - Fields with values: record the value
    - Fields intentionally left blank: record as "" (so we don't ask again)
    - Fields cleared (previously had value, now empty): record as "" and warn
    """
    path = profile_path or ps.DEFAULT_PATH
    profile = ps.load_profile(path)
    learned = profile.get("learned_fields", {})

    print(f"{CYAN}读取页面所有字段当前值...{RESET}")
    fields = await fe.extract_fields(page)

    new_count = 0
    for f in fields:
        label = f.effective_label
        key = _sanitize_key(label)
        if not key:
            continue

        # Determine the current value
        raw_value = f.value.strip()
        # Treat placeholder values as intentionally blank
        is_placeholder = raw_value.lower() in ("select", "please select", "-- select --", "choose")
        save_value = "" if (not raw_value or is_placeholder) else raw_value

        # For custom-select / select, save the display text (more readable)
        if save_value and f.tag in ("select", "custom-select"):
            # raw_value is already the display text for custom-selects
            pass

        # Check existing
        key_exists = key in learned
        existing = learned.get(key, {})
        if isinstance(existing, dict):
            old_value = existing.get("value", "")
        else:
            old_value = str(existing) if existing else ""

        if key_exists and old_value == save_value:
            continue  # No change

        learned[key] = {
            "value": save_value,
            "label": label,
        }

        if save_value == "" and old_value:
            print(f"  {YELLOW}○ 已清空:{RESET} {label} (之前: {old_value})")
        elif save_value == "":
            print(f"  {CYAN}○ 留空:{RESET} {label} (已记录，下次不再询问)")
        elif not old_value:
            print(f"  {GREEN}+ 新增:{RESET} {label} = {save_value}")
        else:
            print(f"  {CYAN}~ 更新:{RESET} {label}: {old_value} → {save_value}")
        new_count += 1

    if new_count == 0:
        print(f"  没有新的变更。")
    else:
        profile["learned_fields"] = learned
        ps.save_profile(profile, path)
        print(f"  {GREEN}已保存 {new_count} 个字段到 profile.yaml{RESET}")


# ── CLI commands ─────────────────────────────────────────────────────────────

async def cmd_extract(args: argparse.Namespace) -> int:
    """Extract form fields and output raw JSON to stdout."""
    browser_inst, page = await br.connect(args.cdp_url)
    try:
        fields = await fe.extract_fields(page)
        fields_json = [f.describe() for f in fields]
        output = {"url": page.url, "fields": fields_json}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    finally:
        await browser_inst.close()
    return 0


async def cmd_apply(args: argparse.Namespace) -> int:
    """Apply fill instructions from a JSON file."""
    with open(args.instructions, encoding="utf-8") as f:
        instructions = json.load(f)

    browser_inst, page = await br.connect(args.cdp_url)
    try:
        for inst in instructions.get("auto_fill", []):
            label = inst.get("label", inst["selector"])
            print(f"  {GREEN}✓{RESET} {label} → {str(inst['value'])[:60]}")
            try:
                await fill_field(page, inst)
            except Exception as e:
                print(f"  {YELLOW}⚠ Failed: {e}{RESET}")
        print(f"\n{GREEN}Apply complete.{RESET}")
    finally:
        await browser_inst.close()
    return 0


async def cmd_wait_and_learn(args: argparse.Namespace) -> int:
    """Wait for page navigation, then auto-learn field values.

    Learns current page fields FIRST (before waiting), so that even if the
    page navigates away, we have the correct field values saved.
    """
    browser_inst, page = await br.connect(args.cdp_url)
    try:
        old_url = page.url

        # Learn current page fields NOW (captures apply results + any user edits so far)
        print(f"{CYAN}正在学习当前页面字段值...{RESET}")
        try:
            await read_back_and_learn(page, args.profile)
        except Exception:
            print(f"{YELLOW}无法读回值。{RESET}")

        print(f"{CYAN}等待页面导航... (当前: {old_url}){RESET}")
        print(f"{CYAN}请在 Chrome 中检查并点击下一页。{RESET}")
        await br.wait_for_navigation(page, timeout=1_800_000)

        await asyncio.sleep(1.5)
        context = browser_inst.contexts[0]
        new_page = context.pages[-1]
        print(json.dumps({"new_url": new_page.url}))
    finally:
        await browser_inst.close()
    return 0


async def cmd_fill(args: argparse.Namespace) -> int:
    browser_inst, page = await br.connect(args.cdp_url)
    try:
        print(f"{CYAN}Connected to: {page.url}{RESET}")
        await fill_page(page, args.profile)
        print(f"\n{CYAN}Please review and manually edit any fields in Chrome.{RESET}")
        print(f"{CYAN}When done, run 'python form_filler.py learn' to save your edits.{RESET}")
    finally:
        await browser_inst.close()
    return 0


async def cmd_learn(args: argparse.Namespace) -> int:
    """Read back current page values and save to profile."""
    browser_inst, page = await br.connect(args.cdp_url)
    try:
        print(f"{CYAN}Connected to: {page.url}{RESET}")
        await read_back_and_learn(page, args.profile)
    finally:
        await browser_inst.close()
    return 0


async def cmd_watch(args: argparse.Namespace) -> int:
    browser_inst, page = await br.connect(args.cdp_url)
    try:
        print(f"{CYAN}Connected to: {page.url}{RESET}")
        print(f"{CYAN}Watch mode: auto-fill → you review → learn → wait for next page{RESET}")
        print(f"{CYAN}Press Ctrl+C to stop.{RESET}\n")

        while True:
            await fill_page(page, args.profile)
            print(f"\n{CYAN}Review the page in Chrome, fill in any missing fields manually.{RESET}")
            print(f"{CYAN}Then click 'Next' / 'Save & Continue' in the browser.{RESET}")
            print(f"{CYAN}I'll learn from your edits and auto-fill the next page.{RESET}\n")
            try:
                old_url = page.url

                # Learn current page before waiting for navigation
                print(f"{CYAN}正在学习当前页面字段值...{RESET}")
                try:
                    await read_back_and_learn(page, args.profile)
                except Exception:
                    print(f"{YELLOW}无法读回值。{RESET}")

                await br.wait_for_navigation(page, timeout=1_800_000)

                await asyncio.sleep(1.5)
                context = browser_inst.contexts[0]
                pages = context.pages
                page = pages[-1]
                print(f"\n{CYAN}New page detected: {page.url}{RESET}\n")
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass
    finally:
        try:
            await read_back_and_learn(page, args.profile)
        except Exception:
            pass
        print(f"\n{CYAN}Stopped. Disconnecting (Chrome stays open).{RESET}")
        await browser_inst.close()
    return 0


# ── Entry point ──────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Auto-fill academic job application forms."
    )
    parser.add_argument(
        "--cdp-url",
        default=br.CDP_URL,
        help="Chrome DevTools Protocol URL (default: %(default)s)",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Path to profile.yaml (default: ./profile.yaml)",
    )

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("extract", help="Extract form fields as JSON (for Claude Code)")
    apply_parser = sub.add_parser("apply", help="Apply fill instructions from JSON file")
    apply_parser.add_argument("instructions", help="Path to JSON instructions file")
    sub.add_parser("wait-and-learn", help="Wait for navigation then auto-learn")
    sub.add_parser("fill", help="Fill the current page (local rules only)")
    sub.add_parser("watch", help="Continuously fill pages as you navigate")
    sub.add_parser("learn", help="Read back current page values and save to profile")

    args = parser.parse_args(argv)

    if args.command is None:
        args.command = "fill"

    if args.command == "extract":
        return asyncio.run(cmd_extract(args))
    elif args.command == "apply":
        return asyncio.run(cmd_apply(args))
    elif args.command == "wait-and-learn":
        return asyncio.run(cmd_wait_and_learn(args))
    elif args.command == "fill":
        return asyncio.run(cmd_fill(args))
    elif args.command == "watch":
        return asyncio.run(cmd_watch(args))
    elif args.command == "learn":
        return asyncio.run(cmd_learn(args))
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
