"""Extract form fields from a Playwright page."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from playwright.async_api import Page


@dataclass
class FormField:
    selector: str
    tag: str  # input / select / textarea / custom-select
    input_type: str  # text, email, tel, radio, checkbox, file, custom-select, ...
    name: str
    field_id: str
    label: str
    placeholder: str
    value: str  # current value, if any
    options: list[dict[str, str]] = field(default_factory=list)  # for select/radio/custom
    required: bool = False
    default_value: str = ""  # first option value for selects
    listbox_id: str = ""  # for custom dropdowns: the listbox element id
    hidden_id: str = ""  # for search-select fields: the hidden input id that stores the value

    # Values that indicate a custom dropdown is still at its placeholder
    _PLACEHOLDER_VALUES = {"select", "please select", "-- select --", "choose", ""}

    @property
    def is_meaningfully_filled(self) -> bool:
        """True if the field has a real value (not just a select/dropdown default)."""
        if not self.value:
            return False
        if self.tag == "select" and self.value == self.default_value:
            return False
        if self.value.strip().lower() in self._PLACEHOLDER_VALUES:
            return False
        return True

    @property
    def effective_label(self) -> str:
        """Best-effort label: explicit label, or inferred from selector/id/name."""
        if self.label:
            return self.label
        raw = self.field_id or self.name or self.selector
        raw = re.sub(r'^[#.]', '', raw)
        raw = re.sub(r'-(edit|dropdown-edit|dropdown)$', '', raw)
        raw = re.sub(r'^(form_)?', '', raw)
        raw = re.sub(r'^(s|lLKP_|lKP_|l)', '', raw)
        raw = re.sub(r'ID$', '', raw)
        raw = re.sub(r'([a-z])([A-Z])', r'\1 \2', raw)
        raw = re.sub(r'[_-]+', ' ', raw)
        return raw.strip() or self.selector

    def describe(self) -> dict:
        """Compact dict sent to the LLM / local matcher."""
        d: dict = {
            "selector": self.selector,
            "tag": self.tag,
            "type": self.input_type,
            "label": self.effective_label,
        }
        if self.placeholder:
            d["placeholder"] = self.placeholder
        if self.options:
            d["options"] = self.options
        if self.required:
            d["required"] = True
        if self.is_meaningfully_filled:
            d["current_value"] = self.value
        if self.listbox_id:
            d["listbox_id"] = self.listbox_id
        if self.hidden_id:
            d["hidden_id"] = self.hidden_id
        return d


_JS_EXTRACT = """
() => {
    function labelFor(el) {
        if (el.id) {
            const lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
            if (lab) return lab.innerText.trim();
        }
        const parent = el.closest('label');
        if (parent) return parent.innerText.trim();
        if (el.getAttribute('aria-label')) return el.getAttribute('aria-label').trim();
        const prev = el.previousElementSibling;
        if (prev && ['LABEL', 'SPAN', 'TD', 'TH', 'DIV'].includes(prev.tagName)) {
            const t = prev.innerText.trim();
            if (t.length > 0 && t.length < 200) return t;
        }
        // Try the closest form-group or field wrapper
        const wrapper = el.closest('.form-group, .field-wrapper, .pu-field');
        if (wrapper) {
            const lab2 = wrapper.querySelector('label');
            if (lab2) return lab2.innerText.trim();
        }
        return '';
    }

    function selectorFor(el) {
        if (el.id) return '#' + CSS.escape(el.id);
        if (el.name) return el.tagName.toLowerCase() + '[name="' + CSS.escape(el.name) + '"]';
        const path = [];
        let cur = el;
        while (cur && cur !== document.body) {
            let seg = cur.tagName.toLowerCase();
            if (cur.id) { path.unshift('#' + CSS.escape(cur.id)); break; }
            const siblings = Array.from(cur.parentElement?.children || []).filter(c => c.tagName === cur.tagName);
            if (siblings.length > 1) seg += ':nth-of-type(' + (siblings.indexOf(cur) + 1) + ')';
            path.unshift(seg);
            cur = cur.parentElement;
        }
        return path.join(' > ');
    }

    const results = [];
    const seen = new Set();

    // ── Standard form elements ──
    for (const el of document.querySelectorAll('input, select, textarea')) {
        const t = (el.type || '').toLowerCase();
        if (['hidden', 'submit', 'button', 'image', 'reset'].includes(t)) continue;
        if (el.offsetParent === null && t !== 'radio' && t !== 'checkbox') continue;

        // Skip inputs that are part of custom pu-select dropdowns (handled below)
        const puParent = el.closest('.pu-select');
        if (puParent && el.id && el.id.endsWith('-edit')) continue;

        // Skip PUSearchTextFieldBox (readonly search fields, handled below)
        if (el.classList.contains('PUSearchTextFieldBox')) continue;

        const sel = selectorFor(el);
        if (seen.has(sel)) continue;
        seen.add(sel);

        const tag = el.tagName.toLowerCase();
        const options = [];
        let defaultSelectValue = '';
        if (tag === 'select') {
            for (const opt of el.options) {
                if (opt.value) options.push({value: opt.value, text: opt.innerText.trim()});
            }
            if (el.options.length > 0) defaultSelectValue = el.options[0].value;
        }
        if (t === 'radio') {
            const radios = document.querySelectorAll('input[type="radio"][name="' + CSS.escape(el.name) + '"]');
            for (const r of radios) {
                const rl = labelFor(r) || r.value;
                options.push({value: r.value, text: rl});
            }
        }

        results.push({
            selector: sel,
            tag: tag,
            input_type: t || tag,
            name: el.name || '',
            field_id: el.id || '',
            label: labelFor(el),
            placeholder: el.placeholder || '',
            value: el.value || '',
            options: options,
            required: el.required || el.getAttribute('aria-required') === 'true',
            default_value: defaultSelectValue,
            listbox_id: '',
        });
    }

    // ── Custom pu-select dropdowns ──
    for (const container of document.querySelectorAll('.pu-select')) {
        // Skip hidden containers (conditionally shown fields)
        if (container.offsetParent === null) continue;

        const editInput = container.querySelector('[id$="-edit"]');
        if (!editInput) continue;

        const editId = editInput.id;
        const baseId = editId.replace('-dropdown-edit', '').replace('-edit', '');
        const listboxId = editId.replace('-edit', '-list');
        const listbox = document.getElementById(listboxId);

        const sel = '#' + CSS.escape(editId);
        if (seen.has(sel)) continue;
        seen.add(sel);

        const options = [];
        if (listbox) {
            for (const li of listbox.children) {
                const text = li.innerText?.trim() || '';
                const val = li.getAttribute('data-value') || li.getAttribute('value') || text;
                if (text && text.toLowerCase() !== 'select') {
                    options.push({value: val, text: text});
                }
            }
        }

        // Try to find label - check for label associated with the container or nearby
        let label = '';
        const wrapper = container.closest('.form-group, .field-wrapper, .pu-field, td');
        if (wrapper) {
            const lab = wrapper.querySelector('label');
            if (lab) label = lab.innerText.trim();
        }
        if (!label) label = labelFor(editInput);

        const isRequired = editInput.required ||
                           editInput.getAttribute('aria-required') === 'true' ||
                           (wrapper && wrapper.querySelector('.required')) !== null;

        results.push({
            selector: sel,
            tag: 'custom-select',
            input_type: 'custom-select',
            name: baseId,
            field_id: editId,
            label: label,
            placeholder: '',
            value: editInput.value || '',
            options: options,
            required: isRequired,
            default_value: '',
            listbox_id: listboxId,
        });
    }

    // ── Search text fields (PUSearchTextFieldBox) ──
    for (const el of document.querySelectorAll('input.PUSearchTextFieldBox')) {
        if (el.offsetParent === null) continue;
        const sel = selectorFor(el);
        if (seen.has(sel)) continue;
        seen.add(sel);

        // Hidden input stores the actual value (e.g. #major_1Text → #major_1)
        const hiddenId = el.id.replace(/Text$/, '');

        // Find the label
        let label = labelFor(el);
        if (!label) {
            const wrapper = el.closest('.form-group');
            if (wrapper) {
                const lab = wrapper.querySelector('label');
                if (lab) label = lab.innerText.trim();
            }
        }
        if (!label) {
            const searchImg = el.parentElement?.querySelector('a img[title]');
            if (searchImg) label = searchImg.title.replace('Search for ', '') + ':';
        }

        const isRequired = el.required || el.getAttribute('aria-required') === 'true';

        results.push({
            selector: sel,
            tag: 'search-select',
            input_type: 'search-select',
            name: el.name || '',
            field_id: el.id || '',
            label: label,
            placeholder: '',
            value: el.value || '',
            options: [],
            required: isRequired,
            default_value: '',
            listbox_id: '',
            hidden_id: hiddenId,
        });
    }

    return results;
}
"""


async def extract_fields(page: Page) -> list[FormField]:
    raw = await page.evaluate(_JS_EXTRACT)
    fields: list[FormField] = []
    seen_radio_names: set[str] = set()
    for r in raw:
        if r["input_type"] == "radio":
            if r["name"] in seen_radio_names:
                continue
            seen_radio_names.add(r["name"])
        fields.append(FormField(**r))
    return fields


# JS to read back current values of all visible form fields
_JS_READ_BACK = """
() => {
    function labelFor(el) {
        if (el.id) {
            const lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
            if (lab) return lab.innerText.trim();
        }
        const parent = el.closest('label');
        if (parent) return parent.innerText.trim();
        if (el.getAttribute('aria-label')) return el.getAttribute('aria-label').trim();
        const prev = el.previousElementSibling;
        if (prev && ['LABEL', 'SPAN', 'TD', 'TH', 'DIV'].includes(prev.tagName)) {
            const t = prev.innerText.trim();
            if (t.length > 0 && t.length < 200) return t;
        }
        const wrapper = el.closest('.form-group, .field-wrapper, .pu-field');
        if (wrapper) {
            const lab2 = wrapper.querySelector('label');
            if (lab2) return lab2.innerText.trim();
        }
        return '';
    }

    function inferLabel(el) {
        // For custom dropdowns, infer from ID
        const id = el.id || '';
        let raw = id.replace(/-dropdown-edit$/, '').replace(/-edit$/, '');
        raw = raw.replace(/^(form_)?/, '');
        raw = raw.replace(/^(s|lLKP_|lKP_|l)/, '');
        raw = raw.replace(/ID$/, '');
        raw = raw.replace(/([a-z])([A-Z])/g, '$1 $2');
        raw = raw.replace(/[_-]+/g, ' ');
        return raw.trim();
    }

    const results = [];

    // Standard form elements
    for (const el of document.querySelectorAll('input, select, textarea')) {
        const t = (el.type || '').toLowerCase();
        if (['hidden', 'submit', 'button', 'image', 'reset'].includes(t)) continue;
        if (el.offsetParent === null && t !== 'radio' && t !== 'checkbox') continue;
        if (el.closest('.pu-select') && el.id && el.id.endsWith('-edit')) continue;

        const tag = el.tagName.toLowerCase();
        let displayValue = el.value || '';
        if (tag === 'select' && el.selectedIndex >= 0) {
            displayValue = el.options[el.selectedIndex].text.trim();
        }
        if (t === 'radio' || t === 'checkbox') {
            if (!el.checked) continue;
            displayValue = labelFor(el) || el.value;
        }
        if (!displayValue) continue;

        results.push({
            label: labelFor(el) || inferLabel(el),
            field_id: el.id || '',
            value: el.value,
            display_value: displayValue,
            tag: tag,
            type: t || tag,
        });
    }

    // Custom pu-select dropdowns
    for (const container of document.querySelectorAll('.pu-select')) {
        if (container.offsetParent === null) continue;
        const editInput = container.querySelector('[id$="-edit"]');
        if (!editInput) continue;
        const val = editInput.value || '';
        if (!val || val.toLowerCase() === 'select') continue;

        results.push({
            label: labelFor(editInput) || inferLabel(editInput),
            field_id: editInput.id || '',
            value: val,
            display_value: val,
            tag: 'custom-select',
            type: 'custom-select',
        });
    }

    return results;
}
"""


async def read_current_values(page: Page) -> list[dict]:
    """Read back all current form field values from the page."""
    return await page.evaluate(_JS_READ_BACK)
