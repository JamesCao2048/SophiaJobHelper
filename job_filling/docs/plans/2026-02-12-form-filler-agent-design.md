# Form Filler Agent Design

## Problem

Filling academic job application forms is repetitive. Each school has its own system, but the information asked is largely the same: personal details, education, work experience, etc.

## Solution

A Python CLI agent that uses Playwright to connect to the user's already-logged-in Chrome browser, extracts form fields from the current page, uses Claude API to match fields against the user's profile and materials, and automatically fills what it can. Fields it can't fill are prompted in the terminal; answers are saved to `profile.yaml` for future reuse.

## Architecture

```
Chrome (logged in, --remote-debugging-port=9222)
    ↑ Playwright CDP connection
    |
Agent (Python CLI)
    ├── field_extractor.py   — extract form fields from DOM
    ├── llm_matcher.py       — Claude API: match fields → profile/materials
    ├── browser.py           — Playwright CDP connection management
    ├── profile_store.py     — profile.yaml read/write/append
    └── form_filler.py       — CLI entry point (fill / watch commands)
```

## Workflow

### `fill` — Single page fill

1. Connect to Chrome via CDP (`localhost:9222`)
2. Extract all form fields: label, name/id, input type, placeholder, options
3. Send to Claude API: fields + profile.yaml + materials summary
4. LLM returns JSON: `auto_fill` (field + value) + `need_input` (field + hint)
5. Playwright fills `auto_fill` fields
6. Terminal prompts user for `need_input` fields
7. User answers saved to `profile.yaml`

### `watch` — Continuous mode

- After filling a page, enter wait state
- Detect URL/DOM changes (user clicks "next page")
- Trigger new `fill` cycle
- Loop until user presses Ctrl+C or types `stop`

## Data

### `profile.yaml`

Structured personal info organized by category: personal, address, current_position, education, application_specific. New answers from terminal prompts are appended under the relevant category.

### `materials/*.md`

Existing CV, research/teaching statements. Used as LLM context for matching and for filling text areas.

## Form Field Handling

| Field type | Strategy |
|------------|----------|
| text input | Direct fill |
| select | LLM picks closest option from list |
| radio | LLM selects based on semantics |
| checkbox | LLM determines check/uncheck |
| textarea | Extract from materials or profile |
| file upload | Prompt user or auto-upload matching PDF |
| date picker | Detect format, convert, fill |

## Implementation Order

1. profile_store.py — YAML read/write/append
2. Generate initial profile.yaml from cv_latest.md via LLM
3. browser.py — Playwright CDP connection
4. field_extractor.py — DOM form field extraction
5. llm_matcher.py — Claude API prompt + response parsing
6. form_filler.py — CLI orchestration (fill + watch)

## Dependencies

- playwright
- anthropic
- pyyaml
- pymupdf (existing)
- pytest (existing)
