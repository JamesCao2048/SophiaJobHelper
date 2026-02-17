"""Match form fields using local logic without external API calls."""

from __future__ import annotations

import re
from typing import Any


def _sanitize_key(label: str) -> str:
    s = label.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")[:60]


def _find_best_option(options: list[dict], target: str) -> str | None:
    """Find the option value whose text best matches target (case-insensitive)."""
    if not options or not target:
        return None
    target_lower = target.lower().strip()
    # Exact match on text
    for opt in options:
        if opt["text"].lower().strip() == target_lower:
            return opt["value"]
    # Exact match on value
    for opt in options:
        if opt["value"].lower().strip() == target_lower:
            return opt["value"]
    # Substring match (target in text)
    for opt in options:
        if target_lower in opt["text"].lower():
            return opt["value"]
    # Substring match (text in target)
    for opt in options:
        if opt["text"].lower().strip() in target_lower and len(opt["text"].strip()) > 2:
            return opt["value"]
    return None


# Mapping: (keywords_in_label) -> (profile_category, profile_key) or callable
# Each rule is (list_of_keywords, category, key, is_all_required)
_RULES: list[tuple[list[str], str, str | None, bool]] = [
    # Personal
    (["first name"], "personal", "first_name", False),
    (["firstname"], "personal", "first_name", False),
    (["given name"], "personal", "first_name", False),
    (["last name"], "personal", "last_name", False),
    (["lastname"], "personal", "last_name", False),
    (["surname"], "personal", "last_name", False),
    (["family name"], "personal", "last_name", False),
    (["email"], "personal", "email", False),
    (["e-mail"], "personal", "email", False),
    (["phone"], "personal", "phone", False),
    (["telephone"], "personal", "phone", False),
    (["mobile"], "personal", "phone", False),
    (["website"], "personal", "website", False),
    (["web site"], "personal", "website", False),
    (["homepage"], "personal", "website", False),
    # Address
    (["street"], "address", "street", False),
    (["address line"], "address", "street", False),
    (["home address"], "address", "street", False),
    (["city"], "address", "city", False),
    (["suburb"], "address", "city", False),
    (["town"], "address", "city", False),
    (["state"], "address", "state", False),
    (["province"], "address", "state", False),
    (["zip"], "address", "zip", False),
    (["postal"], "address", "zip", False),
    (["postcode"], "address", "zip", False),
    (["country"], "address", "country", False),
    (["nationality"], "personal", "nationality", False),
    # Current position
    (["current", "position"], "current_position", "title", True),
    (["current", "title"], "current_position", "title", True),
    (["current", "job"], "current_position", "title", True),
    (["current", "institution"], "current_position", "institution", True),
    (["current", "employer"], "current_position", "institution", True),
    (["current", "organization"], "current_position", "institution", True),
    (["department"], "current_position", "department", False),
]


def match_fields_local(
    fields_json: list[dict],
    profile: dict[str, Any],
) -> dict[str, list[dict]]:
    """Rule-based matching + learned_fields reuse."""
    auto_fill: list[dict] = []
    need_input: list[dict] = []

    learned = profile.get("learned_fields", {})

    for field in fields_json:
        selector = field["selector"]
        label = field.get("label", "")
        label_lower = label.lower()
        field_type = field.get("type", "text")
        tag = field.get("tag", "input")
        options = field.get("options", [])
        current_val = field.get("current_value", "")

        # Skip if already meaningfully filled
        if current_val:
            continue

        matched = False
        matched_value = None
        intentionally_blank = False

        # 1. PRIORITY: Try learned_fields first (highest priority)
        san_key = _sanitize_key(label)
        if san_key and san_key in learned:
            entry = learned[san_key]
            val = entry.get("value") if isinstance(entry, dict) else str(entry)
            if val == "":
                # User intentionally left this blank — skip entirely
                intentionally_blank = True
            else:
                matched_value = val

        # 2. If not in learned_fields, try rule-based matching against profile
        if matched_value is None:
            for keywords, category, key, all_required in _RULES:
                if all_required:
                    if all(kw in label_lower for kw in keywords):
                        matched_value = profile.get(category, {}).get(key)
                        break
                else:
                    if any(kw in label_lower for kw in keywords):
                        matched_value = profile.get(category, {}).get(key)
                        break

        # Skip fields the user intentionally left blank
        if intentionally_blank:
            matched = True  # Don't add to need_input

        # 4. Build instruction if we have a value
        if not intentionally_blank and matched_value is not None and str(matched_value).strip():
            val_str = str(matched_value).strip()

            if tag == "custom-select" and options:
                opt_val = _find_best_option(options, val_str)
                if opt_val:
                    auto_fill.append({
                        "selector": selector,
                        "value": opt_val,
                        "action": "custom-select",
                        "label": label,
                        "listbox_id": field.get("listbox_id", ""),
                    })
                    matched = True
            elif tag == "select" and options:
                opt_val = _find_best_option(options, val_str)
                if opt_val:
                    auto_fill.append({
                        "selector": selector,
                        "value": opt_val,
                        "action": "select",
                        "label": label,
                    })
                    matched = True
            elif field_type in ("radio", "checkbox") and options:
                opt_val = _find_best_option(options, val_str)
                if opt_val:
                    auto_fill.append({
                        "selector": selector,
                        "value": opt_val,
                        "action": "check",
                        "label": label,
                    })
                    matched = True
            else:
                auto_fill.append({
                    "selector": selector,
                    "value": val_str,
                    "action": "fill",
                    "label": label,
                })
                matched = True

        if not matched:
            hint = f"Type: {field_type}"
            if options:
                option_texts = [o["text"] for o in options[:8]]
                hint += f" | Options: {', '.join(option_texts)}"
                if len(options) > 8:
                    hint += f" ... (+{len(options) - 8} more)"
            need_input.append({
                "selector": selector,
                "label": label or selector,
                "hint": hint,
            })

    return {
        "auto_fill": auto_fill,
        "need_input": need_input,
    }
