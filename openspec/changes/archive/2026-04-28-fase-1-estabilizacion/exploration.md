# Exploration: fase-1-estabilizacion

**Explored**: 2026-04-28  
**Scope revision**: 6 fixes diagnosed → 2 real fixes remain (4 already resolved)

---

## Current State

The site is largely functional. 4 of the 6 originally diagnosed fixes were already applied at some point before this exploration. The 2 genuine open issues are:

1. **Broken nav anchors** — `#testimonios` and `#oportunidades` have no target element in `index.html`
2. **Inverted CSS variables** in `styles/config_new.css` — dormant trap waiting to be triggered

---

## Fix-by-Fix Analysis

### Fix 1 — Anchor navigation

| | |
|---|---|
| **Issue confirmed** | Partially — but the described cause is wrong, and two worse breaks exist |
| **`#nosotros`** | ✅ Works — `id="nosotros"` exists on line 3089 |
| **`#testimonios`** | ❌ Broken — nav links at lines 128 & 166, **no target element exists** |
| **`#oportunidades`** | ❌ Broken — nav links at lines 130 & 168, **no target element exists** |
| **Required change** | Add `id="testimonios"` and `id="oportunidades"` to their respective sections |
| **Risk** | Low — additive IDs, non-breaking |

### Fix 2 — Contact form → ✅ ALREADY FIXED

- Form at line 3102: `<form id="form" action="php/send_form.php" method="post" class="luxury-form">` ✓
- `send_contact_form.js`: uses `getElementById('form')` + `fetch('./php/send_form.php')` ✓
- PHP fields (name, number, message, email, company) match HTML inputs exactly ✓

### Fix 3 — Product filter selector → ✅ ALREADY FIXED

- `filter_products.js` selectors: `.catalog-group-tab`, `.filter-item[data-category]`, `.product[data-category]` — all match HTML
- No `.product_category` or `.category-card` found in `filter_products.js`

### Fix 4 — CSS variable conflict (DORMANT RISK)

| | |
|---|---|
| **Issue confirmed** | Conflict exists in the files, but is DORMANT — neither file is linked |
| **`config_new.css`** | `--color_black: #bec2c4` (INVERTED gray), `--color_white: #000000` (INVERTED black) |
| **`styles.css`** | `--color_black: #2c3e50` ✓, `--color_white: #ffffff` ✓ |
| **`index.html` loads** | Only `luxury.css` + `gold-breeze.css` — neither conflict file is active |
| **Required change** | Fix inverted values in `config_new.css` before it's ever linked |
| **Risk** | If `config_new.css` is linked anywhere, text becomes invisible site-wide |

### Fix 5 — Missing script tags → ✅ ALREADY FIXED

Script block before `</body>` (lines 3215–3219):
```html
<script src="scripts/gold-breeze.js"></script>
<script defer src="scripts/header.js"></script>
<script defer src="scripts/filter_products.js"></script>
<script defer src="scripts/scroll-reveal.js"></script>
<script defer src="scripts/send_contact_form.js"></script>
```
Both `filter_products.js` and `send_contact_form.js` loaded with `defer` ✓

### Fix 6 — WhatsApp FAB → ✅ ALREADY FIXED

- HTML at line 3204: `<a href="https://wa.me/50769838322" class="floating-whatsapp-btn" target="_blank" rel="noopener">` ✓
- `luxury.css` line 1141: `position: fixed; bottom: 30px; right: 30px; z-index: 9999;` — fully styled ✓

---

## Affected Files

| File | Change needed |
|------|--------------|
| `index.html` | Add `id="testimonios"` and `id="oportunidades"` to their sections |
| `styles/config_new.css` | Fix `--color_black` (#bec2c4 → #2c3e50) and `--color_white` (#000000 → #ffffff) |

---

## Recommendation

Re-scope the change to 2 surgical fixes. The other 4 were already resolved.

---

## Risks

- `#testimonios`/`#oportunidades` — sections may need to be located in the HTML before IDs can be added
- `config_new.css` — if linked before fix, text/background contrast inverts site-wide

---

## Ready for Proposal

**Yes** — narrower scope than the original diagnosis. Proposal must document the scope delta.
