"""Use Claude API to match form fields against the user's profile and materials."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anthropic
import yaml

MATERIALS_DIR = Path(__file__).parent / "materials"

SYSTEM_PROMPT = """\
You are a form-filling assistant. The user is applying for academic faculty positions.

You will receive:
1. A list of form fields extracted from a web page (JSON).
2. The user's structured profile (YAML).
3. Summaries of the user's application materials (CV, research statement, etc.).

Your job: for each form field, decide whether it can be filled automatically from the profile/materials, or whether the user needs to provide the answer.

Return ONLY valid JSON with this structure:
{
  "auto_fill": [
    {"selector": "...", "value": "...", "action": "fill"},
    {"selector": "...", "value": "...", "action": "select"},
    {"selector": "...", "value": "...", "action": "check"}
  ],
  "need_input": [
    {"selector": "...", "label": "...", "hint": "..."}
  ]
}

Rules:
- "action" is "fill" for text inputs/textareas, "select" for dropdowns (value must match an option value), "check" for checkboxes/radios (value is the option value to select).
- For <select> fields, pick the option whose text or value best matches the profile data. Use the option's "value" attribute, not the display text.
- For radio buttons, "value" should be the value attribute of the correct radio option.
- If a field already has a correct value filled in (current_value matches what you'd fill), skip it entirely — do not include it in either list.
- Only include a field in "need_input" if you truly cannot determine the answer.
- Be precise with selectors — use them exactly as provided.
- For text areas asking for statements/descriptions, you may compose a brief answer from the materials, but keep it concise and relevant to what the field asks.
"""


def _load_materials_summary() -> str:
    parts: list[str] = []
    for md in sorted(MATERIALS_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        # Truncate very long files to first ~2000 chars to fit context
        if len(text) > 2000:
            text = text[:2000] + "\n... (truncated)"
        parts.append(f"### {md.stem}\n{text}")
    return "\n\n".join(parts)


def _build_user_message(
    fields_json: list[dict],
    profile: dict[str, Any],
) -> str:
    profile_yaml = yaml.dump(profile, default_flow_style=False, allow_unicode=True, sort_keys=False)
    materials = _load_materials_summary()
    return (
        "## Form Fields\n"
        f"```json\n{json.dumps(fields_json, indent=2, ensure_ascii=False)}\n```\n\n"
        "## User Profile\n"
        f"```yaml\n{profile_yaml}```\n\n"
        "## Application Materials\n"
        f"{materials}\n"
    )


async def match_fields(
    fields_json: list[dict],
    profile: dict[str, Any],
    model: str = "claude-sonnet-4-5-20250929",
) -> dict[str, list[dict]]:
    """Call Claude API and return {auto_fill: [...], need_input: [...]}."""
    client = anthropic.AsyncAnthropic()  # uses ANTHROPIC_API_KEY env var
    user_msg = _build_user_message(fields_json, profile)

    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    # Extract JSON from the response
    text = response.content[0].text.strip()
    # Handle possible markdown code fence
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    result = json.loads(text)
    return result
