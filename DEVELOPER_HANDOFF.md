# HomePower PTY — Developer Handoff: Execution-Ready Issue Registry

**Prepared from**: Static source-code analysis and grep/PowerShell verification  
**Date**: 2025  
**Scope**: `index.html`, `scripts/`, `styles/`, `php/`  
**Constraint**: No framework migrations. Vanilla HTML/CSS/JS only.

---

## Status Overview

| Category | Count |
|----------|-------|
| Critical issues | 6 |
| High issues | 12 |
| Medium issues | 10 |
| Dead code scripts | 8 |
| Scripts needing validation | 5 |
| Quick wins (< 30 min each) | 12 |

**Current state**: The entire interactive layer of the page is non-functional. Zero JavaScript is loaded except the particle canvas animation (`gold-breeze.js`). The contact form cannot submit. The category filter does nothing. The mobile navigation has no HTML. Every feature that requires script execution is completely dead.

---

## Classification Legend

### Severity
- **CRITICAL** — Breaks a core user flow or business-critical feature entirely
- **HIGH** — Major UX failure, significant trust damage, or business conversion impact
- **MEDIUM** — Quality issue with workaround or indirect impact
- **LOW** — Cosmetic or minor quality issue

### Confidence
- **CONFIRMED** — Verified by reading source file and/or grep/PowerShell evidence
- **LIKELY** — Logically follows from confirmed evidence; not runtime-tested
- **NEEDS VALIDATION** — Requires runtime testing or additional file reads

### Issue Type
- `Bug:MissingWiring` — Script exists or element exists but the two are not connected
- `Bug:BrokenLogic` — Code is loaded/present but internally incorrect
- `Bug:WrongEndpoint` — AJAX or form target file does not exist on disk
- `Bug:StructuralHTML` — Invalid or broken HTML markup
- `Bug:DeadCode` — Loaded or wired, but DOM anchor is absent; execution is always a no-op
- `Content:Corrupted` — Text garbled by encoding failure or AI generation artifact
- `Content:Placeholder` — Developer placeholder text never replaced
- `Content:WeakCopy` — Text is coherent but ineffective for business goal
- `CSS:UnresolvedVariable` — CSS custom property referenced but never defined anywhere
- `CSS:ConflictingTokens` — CSS custom property has inconsistent definitions across files
- `SEO` — Open Graph, structured data, or search metadata defect
- `UX:MissingFeature` — Expected interactive element is absent from the page
- `UX:Accessibility` — Fails WCAG 2.1 Level AA
- `Maintainability` — Production debug artifacts, dead code, merged incompatible systems

---

## Section 1: Critical Issues

---

### CRIT-01 — 17 of 18 scripts not loaded; entire interactive layer is dead

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:MissingWiring` |
| **Affected files** | `index.html` (script tag section), all 17 unloaded scripts |
| **Evidence** | `Select-String '<script' index.html` returns exactly one match: line 1030 `<script src="scripts/gold-breeze.js"></script>`. No other `<script>` tags exist in the 983-line file. `Get-ChildItem scripts\*.js` returns 18 JS files on disk. |
| **Broken feature** | Every interactive feature on the page |
| **User-facing impact** | Category filter shows all 28 products simultaneously with no filtering. Contact form submits to wrong endpoint (separate issue). No input focus animations. No header scroll effects. No modals. |
| **Business impact** | Zero JS-handled lead capture. Site is functionally a static brochure. |
| **Minimal safe fix** | Add `<script defer src="scripts/...">` tags before `</body>` for the 4–7 confirmed-functional scripts listed below. Do NOT add script tags for dead-code scripts (DOM anchors absent). |
| **Risks / Dependencies** | Fix CRIT-04, CRIT-05 first (broken logic inside scripts). Loading a script before its DOM anchor issues are fixed produces misleading behavior. |
| **Implementation priority** | 1 (after all Bug:BrokenLogic fixes) |

**Script-to-Feature map — what each unloaded script controls:**

| Script | Feature broken by not loading | Safe to load now? |
|--------|-------------------------------|-------------------|
| `scripts/filter_products.js` | Category filter (all 12 category cards are non-interactive) | YES — after CRIT-05 selector fix |
| `scripts/send_contact_form.js` | Contact form validation + CSRF + AJAX submission | YES — after CRIT-02, CRIT-03, CRIT-04 fixes |
| `scripts/header.js` | Header scroll state + sticky shadow + mobile menu | YES (scroll) — NO (mobile menu until HIGH-12 HTML added) |
| `scripts/inputs.js` | Form input floating-label animation | NO — form uses `placeholder` only, no `.form_input`/`.form_label` classes; would be a no-op |
| `scripts/promo_video_modal.js` | Hero video promotional popup | NO — `id="seasonalPopup"` absent from HTML (see Dead Code) |
| `scripts/carnival_modal.js` | Seasonal carnival modal | NO — `id="carnivalModal"` absent from HTML (see Dead Code) |
| `scripts/send_careers_form.js` | Careers / CV form submission | NO — `id="careers_form"` absent from HTML (see Dead Code) |
| `scripts/clients_scrolling_text.js` | Scrolling clients ticker | NO — ticker DOM anchors absent; HTML uses static grid (see Dead Code) |
| `scripts/cv_button_handler.js` | CV email-CTA button state feedback | NO — `.cv_upload_link` absent from HTML (see Dead Code) |
| `scripts/avatar_effects.js` | Testimonial avatar animations | NO — `.testimonial_avatar` absent from HTML (see Dead Code) |
| `scripts/seasonal_popup.js` | Seasonal popup (predecessor of promo_video_modal.js) | NO — likely same dead DOM anchor (see Dead Code) |
| `scripts/gold-effects.js` | Gold particle effects | NOT APPLICABLE — loaded only by `productos/*/index.html`, not index.html |
| `scripts/image-optimization.js` | Unknown | NEEDS VALIDATION |
| `scripts/fix_text.js` | Unknown | NEEDS VALIDATION |
| `scripts/cleanup_text_encoding.js` | Unknown (possibly one-time utility) | NEEDS VALIDATION |
| `scripts/product-interactions.js` | Unknown | NEEDS VALIDATION |
| `scripts/file_upload.js` | Unknown (possibly tied to careers form) | NEEDS VALIDATION |

---

### CRIT-02 — Contact form has no `id="form"`; JS handler never attaches

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:MissingWiring` |
| **Affected files** | `index.html` line 978, `scripts/send_contact_form.js` lines 1–2 |
| **Evidence** | `index.html` line 978: `<form action="php/submit_form.php" method="post" class="luxury-form">` — no `id` attribute present. `send_contact_form.js` line 1: `const form = document.getElementById('form');` / line 2: `if (!form) return;`. `getElementById('form')` returns `null`. Guard fires immediately. |
| **Broken feature** | All contact form interactivity (field validation, AJAX submission, success/error feedback) |
| **User-facing impact** | Form has no client-side validation. Submit button triggers a synchronous browser POST to a non-existent endpoint (see CRIT-03). User sees a server 404 error page. |
| **Business impact** | Zero leads captured via the contact form. |
| **Minimal safe fix** | Add `id="form"` to the form tag: `<form id="form" action="php/send_form.php" method="post" class="luxury-form">` |
| **Risks / Dependencies** | Fix is not sufficient alone — CRIT-03 (wrong action), CRIT-04 (field name mismatch), and CRIT-01 (script not loaded) must also be resolved for the form to work end-to-end. |
| **Implementation priority** | 2 |

---

### CRIT-03 — Contact form `action` attribute points to `php/submit_form.php` which does not exist

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:WrongEndpoint` |
| **Affected files** | `index.html` line 978, `php/` directory |
| **Evidence** | `index.html` line 978: `action="php/submit_form.php"`. `php/` directory contains: `get_csrf_token.php`, `send_form.php`, `send_form_simple.php`, `test_email.php`, `test_form.php`, `upload_cv.php`. The file `php/submit_form.php` is NOT present. `send_contact_form.js` line 89 (the AJAX fetch): `'./php/send_form.php'` — the correct endpoint is already in the JS. |
| **Broken feature** | Contact form submission (HTML fallback path and user expectation) |
| **User-facing impact** | When the JS handler fails (CRIT-02 not yet fixed), the browser falls through to a native POST. The server returns HTTP 404. |
| **Business impact** | Any submission attempt by a user who has JS disabled or before CRIT-01/CRIT-02 are fixed results in a 404 page. |
| **Minimal safe fix** | Change `action="php/submit_form.php"` to `action="php/send_form.php"` in `index.html` line 978. |
| **Risks / Dependencies** | Independent fix. Apply with CRIT-02. |
| **Implementation priority** | 2 |

---

### CRIT-04 — Contact form HTML field names don't match JS validation; submit throws TypeError

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:BrokenLogic` |
| **Affected files** | `index.html` lines 980–988, `scripts/send_contact_form.js` lines 1–30 and 55–70 |
| **Evidence** | HTML field names (index.html lines 980–987): `name="nombre"`, `name="telefono"`, `name="correo"`, `name="empresa"`, `name="mensaje"`. JS submit handler (`send_contact_form.js`): `const name = formData.get('name')?.trim()` → returns `undefined` (no field named `name`). Then `validateField('name', undefined)` is called. Inside `validateField`: `return value.trim().length >= 2` → `undefined.trim()` → **TypeError: Cannot read properties of undefined (reading 'trim')**. The catch block shows a generic error to the user. |
| **Broken feature** | Contact form validation and AJAX submission |
| **User-facing impact** | After CRIT-01 and CRIT-02 are fixed, every submit attempt crashes with a TypeError. Generic error shown. No leads captured. |
| **Business impact** | Contact form remains non-functional even after other fixes until this is resolved. |
| **Minimal safe fix (Option A — rename HTML to match JS)** | In `index.html`: change `name="nombre"→name="name"`, `name="telefono"→name="number"`, `name="correo"→name="email"` (keep or drop `empresa`), `name="mensaje"→name="message"`. In `send_contact_form.js`: add `case 'email': return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());` to `validateField`. |
| **Minimal safe fix (Option B — update JS to match HTML)** | In `send_contact_form.js`: change `formData.get('name')` → `formData.get('nombre')`, `formData.get('number')` → `formData.get('telefono')`, `formData.get('message')` → `formData.get('mensaje')`. Update switch cases in `validateField` to match. |
| **Risks / Dependencies** | Before choosing Option A or B, verify which field names `php/send_form.php` reads from `$_POST`. The PHP side must receive the field names that the HTML sends. |
| **Additional finding** | `send_contact_form.js` defines a `validatePhone()` function that is never called from the submit handler. Dead code within the script. |
| **Implementation priority** | 2 |

---

### CRIT-05 — `filter_products.js` queries `.product_category`; HTML uses `.category-card`

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:BrokenLogic` |
| **Affected files** | `scripts/filter_products.js` line 2, `index.html` lines 165–200 |
| **Evidence** | `filter_products.js` line 2: `const categories = document.querySelectorAll('.product_category');`. Grep for `.product_category` in index.html: **zero matches**. Grep for `.category-card` in index.html: **12 matches** (all category filter cards). `categories` is an empty NodeList. The `forEach` on line 4 iterates zero times. Zero click listeners are added. |
| **Broken feature** | Product category filter — all 28 products are always visible simultaneously |
| **User-facing impact** | Clicking any category card does nothing. The entire filtering UX is absent. |
| **Business impact** | Users cannot narrow products by category. The product section requires scrolling through all 28 items even when only interested in one type. |
| **Minimal safe fix** | In `filter_products.js` line 2: change `.product_category` to `.category-card`. |
| **Risks / Dependencies** | Only effective after CRIT-01 (script is loaded). Fix both in the same commit. |
| **Additional finding** | `filter_products.js` also binds `.quick_view_btn` (lines 34–46). Grep shows zero `.quick_view_btn` elements in index.html. The current product card HTML uses `.product_cta` links. This second half of `filter_products.js` is dead code, but gracefully handles it (iterates empty NodeList with no side effects). |
| **Implementation priority** | 3 (fix selector, then add script tag) |

---

### CRIT-06 — `#nosotros` navigation anchor missing from DOM

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:StructuralHTML` |
| **Affected file** | `index.html` lines 82 (nav link) |
| **Evidence** | Line 82 in nav: `<li><a href="#nosotros">Nosotros</a></li>`. PowerShell grep for `id="nosotros"` across entire index.html: **zero matches**. The About section content lives at lines 969–979 inside `<section class="contact-section" id="contacto">` — no `id="nosotros"` on any element. |
| **Broken feature** | "Nosotros" nav link — clicking it does nothing; browser cannot scroll to a non-existent anchor |
| **User-facing impact** | One of five primary navigation items is non-functional on every page load. |
| **Business impact** | Users cannot navigate to the company's "About" section via the nav. Trust signals (who the company is) are hidden. |
| **Minimal safe fix** | Add `id="nosotros"` to the `<div class="contact-info">` element at line 969: `<div class="contact-info" id="nosotros">`. |
| **Risks / Dependencies** | None. Zero-risk HTML attribute addition. |
| **Implementation priority** | 1 (quickest fix, zero risk) |

---

## Section 2: High Issues

---

### HIGH-01 — Hero `<h1>` uses consumer/DTC language on a B2B wholesale catalog

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:WeakCopy` |
| **Affected file** | `index.html` line 100 |
| **Evidence** | `<h1 class="hero-title">Potencia e Innovación para<br>tu hogar</h1>` — "tu hogar" = "your home". Meta description line 13: `"Stock exclusivo para negocios que buscan lo mejor"` — "para negocios" = "for businesses". The page targets wholesale buyers (tiendas, distribuidores) but the first H1 addresses retail consumers. |
| **User-facing impact** | B2B buyers arrive and read consumer messaging. Immediate trust mismatch. |
| **Business impact** | Increased bounce from primary customer segment. |
| **Minimal safe fix** | Replace with B2B-appropriate messaging. Requires stakeholder input. |
| **Classification** | **Approval-gated** — see Section 6. |
| **Implementation priority** | After approval |

---

### HIGH-02 — No floating WhatsApp FAB; primary conversion CTA absent below the fold

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `UX:MissingFeature` |
| **Affected file** | `index.html` (missing element) |
| **Evidence** | PowerShell grep for `wa-fab\|floating\|fab\|fixed` (position) in index.html: **zero matches**. WhatsApp links exist only in: header `.btn-outline-gold` (above fold), hero `.btn-text-icon` (above fold), and per-product `.product_cta` inline links. No persistent CTA exists at any scroll depth. |
| **User-facing impact** | Users scrolling past the hero (categories, 28 products, client logos) have no persistent WhatsApp CTA. The only path to WhatsApp requires scrolling back to the top or clicking a per-product link. |
| **Business impact** | Panama B2B wholesale buyer intent is to contact via WhatsApp. Missed conversions from all mid-page and footer-zone users. |
| **Minimal safe fix** | Add fixed-position HTML + ~15 lines CSS. No JS dependency. See Quick Wins section (item 7). |
| **Implementation priority** | 4 |

---

### HIGH-03 — Two product cards use `<div>` instead of `<a>` image wrapper; cards not clickable

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:StructuralHTML` |
| **Affected file** | `index.html` lines 657 and 864 |
| **Evidence** | All other 26 product cards use `<a href="productos/..." class="product_image_wrapper">`. Lines 657 and 864 use `<div class="product_image_wrapper">` with no `href`. Confirmed by: `Select-String "product_image_wrapper" index.html` returning only 2 `<div>` entries vs 26 `<a>` entries. |
| **User-facing impact** | Clicking the image or title of these two products navigates nowhere. User cannot reach the product detail page from the catalog. |

**Card 1 — "Freidora de Aire Negra" (line 657):**

| Sub-issue | Detail |
|-----------|--------|
| Missing `<a>` wrapper | `<div class="product_image_wrapper">` — card not clickable |
| Wrong image | `src="productos/air-fryer-4-5l/img/AIR_FRYER.webp"` — this is the silver Air Fryer 4.5L Digital's image |
| Missing product directory | `productos/freidora-aire-negra/` does NOT exist on disk (`Test-Path` returned `False`) |
| Minimal fix | Requires: create `productos/freidora-aire-negra/` directory + product page, source correct product image, then wrap with `<a>` |

**Card 2 — "Sandwichera Metal Profesional" (line 864):**

| Sub-issue | Detail |
|-----------|--------|
| Missing `<a>` wrapper | `<div class="product_image_wrapper">` — card not clickable |
| Image src | `src="productos/sandwichera-metal/img/SANDWCHERA_METAL.webp"` — directory EXISTS |
| Filename typo | `SANDWCHERA_METAL.webp` is missing the letter `I` (correct: `SANDWICHERA_METAL.webp`). File must be confirmed to exist under the misspelled name before renaming. |
| Minimal fix | Replace `<div class="product_image_wrapper">` with `<a href="productos/sandwichera-metal/" class="product_image_wrapper">` and close with `</a>` |

| **Implementation priority** | Card 2: immediate (5 min). Card 1: requires product directory creation first. |

---

### HIGH-04 — `var(--color-accent)` (hyphen) used 14 times in inline styles; never defined in any CSS file

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `CSS:UnresolvedVariable` |
| **Affected files** | `index.html` (14 occurrences), `styles/config_new.css`, `styles/styles.css` |
| **Evidence** | PowerShell occurrence count: `--color-accent` (hyphen) → **14** occurrences in index.html. `config_new.css` `:root`: defines `--color_accent: #FBD38D` (underscore). `styles.css` `:root`: also defines `--color_accent` (underscore). Neither file defines `--color-accent` with a hyphen anywhere. All 12 category card SVG icons use `stroke="var(--color-accent)"`. |
| **Visual result** | All 12 category icon SVGs render with no stroke color (empty string resolves to `transparent`). Gold accent color is absent from all 14 affected elements (category icons, contact section heading). |
| **Minimal safe fix (Option A — add alias)** | Add to `styles/styles.css` `:root`: `--color-accent: var(--color_accent);` This fixes all 14 occurrences at once and future-proofs against the naming inconsistency. |
| **Minimal safe fix (Option B — bulk replace)** | Global find-replace in `index.html`: `--color-accent` → `--color_accent`. Touches only inline styles; does not address the underlying naming convention conflict between the two CSS files. |
| **Risks** | Option A is safer. If more inline styles or new templates are added using the hyphen convention, Option B would require repeated fixing. |
| **Implementation priority** | 2 |

---

### HIGH-05 — Google Fonts loads `Inter` and `Playfair Display`; CSS tokens reference `Montserrat` and `Lato`

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `CSS:ConflictingTokens` |
| **Affected files** | `index.html` lines 8–9 (Google Fonts link), `styles/styles.css` (`:root` block) |
| **Evidence** | Google Fonts URL in index.html: `family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600;700`. CSS in `styles.css` `:root`: `--font_title: "Montserrat", sans-serif;` and `--font_text: "Lato", sans-serif;`. PowerShell counts: `Montserrat` → 0 in index.html; `Lato` → 0 in index.html; `Inter` → 31; `Playfair Display` → 1. |
| **Visual result** | All elements using `--font_title` or `--font_text` render in the OS system fallback sans-serif. Designed typography is absent from the entire site. |
| **Two valid resolutions** | (A) Change Google Fonts URL to load `Montserrat` + `Lato` if those are the intended design fonts. (B) Update `styles.css` `:root` to `--font_title: "Playfair Display", serif; --font_text: "Inter", sans-serif;` if Inter+Playfair is the intended design direction. |
| **Classification** | **Approval-gated** — requires design decision. See Section 6. |
| **Implementation priority** | After design decision |

---

### HIGH-06 — `var(--font-heading)` used in contact section; never defined in any CSS file

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `CSS:UnresolvedVariable` |
| **Affected file** | `index.html` line 968 |
| **Evidence** | Line 968: `<h2 style="color:var(--color-accent); font-family:var(--font-heading); ...">Conoce Home Power</h2>`. PowerShell: `--font-heading` → 1 occurrence in index.html. Zero occurrences in `config_new.css`, `styles.css`, or `gold-breeze.css`. |
| **Visual result** | "Conoce Home Power" heading renders in browser default font. |
| **Minimal safe fix** | Add `--font-heading: var(--font_title);` to `styles.css` `:root` block. Or remove the inline `font-family:var(--font-heading)` and use a CSS class that applies the correct font token. |
| **Implementation priority** | 2 |

---

### HIGH-07 — About section body text is corrupted AI-generated copy (2 paragraphs)

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:Corrupted` |
| **Affected file** | `index.html` lines 971 and 973 |
| **Evidence — Line 971 (verbatim)** | `"es a una luxury B2B appliance distributor la potenia de Manios in Panama con las que las comproméstica de nuestor-alentoomésticos en Panama."` |
| **Evidence — Line 973 (verbatim)** | `"Un compromism o sté comprone éiramo imposoando en la enartunbrrnento peren mogas a para etroo de los tornacloros que qustian eevrncañas y acesozas procienes que tu metosionamiente ismaticos."` |
| **User-facing impact** | Any user reading the About section encounters incoherent text that reads as corrupted data. Destroys brand credibility. |
| **Business impact** | Wholesale buyers performing due diligence on a supplier will question the company's legitimacy. |
| **Minimal safe fix** | Replace with real company description. Requires stakeholder input. |
| **Classification** | **Approval-gated** — see Section 6. |

---

### HIGH-08 — Client wall subtitle is garbled placeholder text

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:Placeholder` |
| **Affected file** | `index.html` line 950 |
| **Evidence (verbatim)** | `<p style="color:#666; margin-bottom:40px;">Real alte clientes distribuidor en Panama</p>` — "Real alte clientes" is not valid Spanish. |
| **Minimal safe fix** | Replace with real subtitle, e.g., `"Nuestros clientes distribuidores en Panamá"`. Requires approval. |

---

### HIGH-09 — Footer address is placeholder lorem-ipsum text

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:Placeholder` |
| **Affected file** | `index.html` line 1006 |
| **Evidence (verbatim)** | `📍 Adresse cuor 51, Elbonstile, 18 Panama, Gore lantes` — "Adresse" is French for "address". "Elbonstile" and "Gore lantes" are not real place names. |
| **User-facing impact** | Wholesale buyers looking to verify the company's location see obviously fake data. Trust destroyed. |
| **Minimal safe fix** | Replace with real address or remove the address line entirely. **Approval-gated**. |

---

### HIGH-10 — Footer social icons are developer placeholder spans with no icons or links

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:Placeholder` |
| **Affected file** | `index.html` lines 1019–1022 |
| **Evidence (verbatim)** | `<span>[IG]</span>`, `<span>[FB]</span>`, `<span>[IN]</span>`, `<span>[YT]</span>`. No SVG icons, no `<a href>` links, no `aria-label`. |
| **User-facing impact** | Footer shows "[IG] [FB] [IN] [YT]" as plain text. No social links work. |
| **Minimal safe fix** | Replace each `<span>` with `<a href="[URL]" aria-label="[Platform]" target="_blank" rel="noopener">` wrapping an SVG icon. Note: `media/icons/socials_networks/` contains existing icon assets. |
| **Classification** | Requires social media profile URLs — approval-gated for URL values. The HTML swap itself is quick. |

---

### HIGH-11 — Product feature bullet text has character-encoding corruption

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Content:Corrupted` |
| **Affected file** | `index.html` lines 643, 644, 695 |
| **Evidence (direct grep output)** | Line 643: `<li> eimer 30 min</li>` (should be "Timer 30 min"). Line 644: `<li> eemperatura ajustable</li>` (should be "Temperatura ajustable"). Line 695: `<li> eimer 60 minutos</li>` (should be "Timer 60 minutos"). |
| **Additional corruption in section comments** | Line 503: `<!-- ESeUFAS -->` (should be ESTUFAS). Line 681: `<!-- HORNIeO -->` (should be HORNITO). Line 759: `<!-- eOSeADORAS -->` (should be TOSTADORAS). These are internal code comments; not visible to users but indicate the scope of the encoding event. |
| **User-facing impact** | "Freidora de Aire Negra" card and "Hornito 23L" card show corrupted product feature text. Reduces product page trust. |
| **Minimal safe fix** | Correct the three `<li>` text values: "Timer 30 min", "Temperatura ajustable", "Timer 60 minutos". Correct section comments for developer hygiene. |
| **Implementation priority** | 3 |

---

### HIGH-12 — Mobile navigation HTML is completely absent; no hamburger button exists in index.html

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Confidence** | CONFIRMED |
| **Type** | `Bug:StructuralHTML` + `Bug:MissingWiring` |
| **Affected files** | `index.html` lines 67–90, `scripts/header.js`, `styles/styles.css` |
| **Evidence** | PowerShell grep for `menuBurger\|fullscreenMenu\|menu-burger\|btn_menu\|hamburger\|mobile-menu` in index.html: **zero matches**. Header HTML (lines 67–90) contains only: `<header class="luxury-header">`, `<nav class="luxury-nav">`, `<ul class="nav-links">`, one CTA `<a>` button. No `<button>` for hamburger. No overlay div. `header.js` requires: `getElementById('menuBurger')`, `getElementById('fullscreenMenu')`, `getElementById('menuClose')` — all return `null`. `styles.css` contains full mobile menu CSS (`.menu-burger`, `.fullscreen-menu`, `.fullscreen-menu.open`) that targets elements not in the HTML. |
| **User-facing impact** | On mobile viewport widths, the nav collapses (CSS hides list items) but there is no button to open it. All nav items are inaccessible via normal interaction. Users cannot navigate between sections without knowing the anchor link pattern directly. |
| **Additional finding** | `header.js` contains two separate mobile menu implementations in the same file: a `DOMContentLoaded` block (targets `menuBurger`, `fullscreenMenu`, `menuClose`) and an IIFE legacy block (targets `btn_menu`, `menuBurger`, `btn_menu_close`, `.menu_item`, `overlay`). Both target IDs that do not exist in the current HTML. The file should be consolidated to one implementation before the HTML is added. |
| **Minimal safe fix** | Add the missing HTML elements to the header: a `<button id="menuBurger">` (hamburger icon) and a `<nav id="fullscreenMenu">` mobile overlay. Match the IDs that `header.js` expects. Clean up the duplicate IIFE implementation in `header.js` first. |
| **Implementation priority** | 5 (complex — consolidate header.js first, then add HTML) |

---

## Section 3: Medium Issues

| ID | Type | File | Line | Description |
|----|------|------|------|-------------|
| MED-01 | `SEO` | `index.html` | 26 | `og:locale` is `es_ES` (Spain Spanish) not `es_PA` (Panama Spanish). |
| MED-02 | `SEO` | `index.html` | 19, 33 | `og:title` and `twitter:title` are `"Homepowerpty"` (one word). Should match brand: "Home Power PTY". |
| MED-03 | `SEO` / `UX:Accessibility` | `index.html` | 21 | `og:image` points to `media/icons/logo/logo.png` (a small logo). Spec requires 1200×630 min. A wrong-sized OG image will be cropped or refused by social platforms. |
| MED-04 | `UX:Accessibility` | `index.html` | 165–200 | All 12 category card SVGs use identical markup: `<rect x="4" y="4" width="16" height="16" rx="2" ry="2"><circle cx="12" cy="12" r="3">`. No visual differentiation between "Planchas", "Licuadoras", "Air Fryer", etc. Every icon looks the same. |
| MED-05 | `Content:Placeholder` | `index.html` | 1024 | Copyright year is `© 2024`. Should be `© 2025`. |
| MED-06 | `UX` | `index.html` | 988 | `<textarea name="mensaje" placeholder="Mensaje" rows="1">` — a single-row textarea. Users cannot see their message as they type. Standard minimum is `rows="4"`. |
| MED-07 | `Bug:StructuralHTML` | `index.html` | ~213–940 | All 28 `<li class="product">` elements are direct children of `<div class="products-grid">`. Per HTML specification, `<li>` must be a direct child of `<ul>`, `<ol>`, or `<menu>`. This is invalid HTML and may cause accessibility tree and screen reader failures. Change `<div class="products-grid">` to `<ul class="products-grid">`. |
| MED-08 | `UX:Accessibility` | `index.html` | 62 | Announcement bar: `WhatsApp: (507) 6983-8322` is plain prose text. Not a link. On desktop, not tappable. Mobile OS auto-detection of phone numbers is unreliable. Wrap with `<a href="https://wa.me/50769838322">`. |
| MED-09 | `UX` | `index.html` | 103 | Hero WhatsApp CTA uses `<img src="media/icons/socials_networks/whatsapp_icon.ico">`. `.ico` files used in `<img>` tags are not reliably rendered cross-browser (Chrome supports it; Safari has inconsistencies). Replace with `.png` or `.svg`. |
| MED-10 | `Content:Corrupted` / `UX:Accessibility` | `index.html` | 328, 353 | `alt="Licadora Chocolate"` and `alt="Licadora Azul"` — missing letter 'u'. Correct: "Licuadora". Same typo appears in product `<h3>` titles on those cards. Screen readers will mispronounce. |

---

## Section 4: Dead Code Scripts

The following scripts exist on disk and are **not loaded** in `index.html`. Even if loaded, they would immediately exit because their DOM anchor elements don't exist in the current HTML. They should not be loaded until the corresponding HTML sections are built.

| Script | Guard condition | DOM element queried | Status | Note |
|--------|----------------|---------------------|--------|------|
| `scripts/carnival_modal.js` | `if (!modal) return` | `getElementById('carnivalModal')` | **Dead** | Also contains 9 `console.log` calls at lines 15, 32, 36, 201, 209, 247, 250, 252, 256. A standalone test page exists at `test_carnival.html`. Remove console.logs before reactivating. |
| `scripts/promo_video_modal.js` | `if (!popup) return` | `getElementById('seasonalPopup')` | **Dead** | `seasonalPopup` absent from index.html |
| `scripts/send_careers_form.js` | `if (!form) return` | `getElementById('careers_form')` | **Dead** | No careers form section in index.html |
| `scripts/clients_scrolling_text.js` | Early return on missing element | `getElementById('clients_ticker')`, `'clients_slider'`, `'clients_slider_clone'` | **Dead** | HTML uses static `.client-grid` grid, not a ticker |
| `scripts/cv_button_handler.js` | None (binds directly) | `document.querySelector('.cv_upload_link')` | **Dead** | `.cv_upload_link` absent from index.html; tied to the missing careers form |
| `scripts/avatar_effects.js` | None (iterates empty array) | `querySelectorAll('.testimonial_avatar')` | **Dead** | No testimonials section in index.html |
| `scripts/seasonal_popup.js` | Likely same as promo_video_modal.js | Likely `seasonalPopup` | **LIKELY Dead** | Probable predecessor of `promo_video_modal.js` — NEEDS VALIDATION |
| `scripts/inputs.js` | None (binds directly) | `.form_input`, `.form_label` | **Dead** | Contact form uses `placeholder`-only inputs; no `.form_input` or `.form_label` class exists on any form element in index.html |

---

## Section 5: Scripts Needing Validation

The following scripts have unknown or unclear runtime behaviour. Do not add `<script>` tags for them until each is validated.

| Script | Reason to validate |
|--------|-------------------|
| `scripts/image-optimization.js` | Unknown — may be a build-time utility, not a runtime script. Read the file and check for `DOMContentLoaded` or IIFE pattern to determine. |
| `scripts/fix_text.js` | Unknown purpose. May be a one-time encoding fix utility. Check for `DOMContentLoaded` wrapper. |
| `scripts/cleanup_text_encoding.js` | Likely a one-time utility (name suggests encoding cleanup). If so, it should not be in production script loading. |
| `scripts/product-interactions.js` | Unknown DOM dependencies. Read the file to determine what DOM elements it targets before loading. |
| `scripts/file_upload.js` | May be tied to the missing careers form (CV upload). If so, dead code until careers form HTML is implemented. |

---

## Section 6: Quick Wins (under 30 minutes each)

Each item below is an independent fix. Apply in any order. Total combined time if done consecutively: ~55 min.

| # | Fix | File | Estimated time |
|---|-----|------|----------------|
| 1 | Add `id="nosotros"` to `<div class="contact-info">` (line 969) | `index.html` | 1 min |
| 2 | Change form `action` to `php/send_form.php` + add `id="form"` (line 978) | `index.html` | 2 min |
| 3 | Change `filter_products.js` line 2 selector: `.product_category` → `.category-card` | `scripts/filter_products.js` | 1 min |
| 4 | Add `--color-accent: var(--color_accent);` alias to `styles.css` `:root` block | `styles/styles.css` | 2 min |
| 5 | Add `--font-heading: var(--font_title);` to `styles.css` `:root` block | `styles/styles.css` | 1 min |
| 6 | Add `<script defer src="scripts/filter_products.js">` and `<script defer src="scripts/send_contact_form.js">` before `</body>` | `index.html` | 3 min |
| 7 | Add floating WhatsApp FAB (HTML + inline or class CSS, no JS needed) | `index.html` | 10 min |
| 8 | Wrap announcement bar number in WhatsApp link: `<a href="https://wa.me/50769838322" style="color:inherit; text-decoration:underline;">+507 6983-8322</a>` | `index.html` line 62 | 2 min |
| 9 | Fix footer social spans `[IG]` etc. — replace with SVGs from `media/icons/socials_networks/` and `<a>` link wrappers (URLs approval-gated, but HTML structure can be scaffolded) | `index.html` lines 1019–1022 | 8 min |
| 10 | Fix copyright year `© 2024` → `© 2025` | `index.html` line 1024 | 1 min |
| 11 | Fix `textarea` rows: `rows="1"` → `rows="4"` | `index.html` line 988 | 1 min |
| 12 | Correct product feature corruption: "eimer" → "Timer", "eemperatura" → "Temperatura" (3 `<li>` elements) | `index.html` lines 643, 644, 695 | 3 min |

---

## Section 7: Safe Implementation Order

Sequence that minimizes regressions. Items in the same group can be done in parallel.

**Group A — Zero-risk HTML attribute additions:**
1. Add `id="nosotros"` to `.contact-info` div ← CRIT-06
2. Add `id="form"` to form element ← CRIT-02
3. Fix `action="php/send_form.php"` ← CRIT-03
4. Fix `og:locale` → `es_PA`, `og:title` → `"Home Power PTY"` ← MED-01, MED-02
5. Fix copyright year ← MED-05
6. Fix textarea `rows="1"` → `rows="4"` ← MED-06
7. Correct 3 corrupted `<li>` product feature texts ← HIGH-11

**Group B — CSS token fixes (no JS dependency):**
8. Add `--color-accent` and `--font-heading` aliases to `styles.css` `:root` ← HIGH-04, HIGH-06
9. *Font decision pending* — resolve HIGH-05 (Google Fonts vs CSS token mismatch) once design decision is made

**Group C — Script logic fixes (before loading scripts):**
10. Fix `filter_products.js` selector ← CRIT-05
11. Resolve contact form field names (CRIT-04) — confirm `send_form.php` expected field names first

**Group D — Load the two confirmed-functional scripts:**
12. Add `<script defer src="scripts/filter_products.js">` ← CRIT-01 partial
13. Add `<script defer src="scripts/send_contact_form.js">` ← CRIT-01 partial

**Group E — Header script (dependent on mobile nav HTML decision):**
14. Consolidate `header.js` (remove duplicate IIFE) ← HIGH-12 prerequisite
15. Add mobile hamburger button HTML to header ← HIGH-12
16. Add `<script defer src="scripts/header.js">` ← CRIT-01 partial

**Group F — Structural corrections:**
17. Replace `<div class="products-grid">` with `<ul>`, and `</div>` with `</ul>` ← MED-07
18. Fix "Sandwichera Metal" card: replace `<div>` image wrapper with `<a>` ← HIGH-03 Card 2
19. Create `productos/freidora-aire-negra/` directory + page + image (or resolve product intent) ← HIGH-03 Card 1

**Group G — Content (approval-gated):**

See Section 8.

---

## Section 8: Approval-Gated Changes

These items require stakeholder input before a developer can implement them. Each is blocked on a decision, not on technical complexity.

| Change needed | Blocked on | Where used |
|---------------|------------|------------|
| Hero `<h1>` replacement copy (B2B language) | Brand/marketing team | `index.html` line 100 |
| About section body copy (lines 971, 973) | Company description from stakeholder | `index.html` lines 971, 973 |
| Client wall subtitle line 950 | Approved marketing copy | `index.html` line 950 |
| Footer real address or removal | Stakeholder decision + real address | `index.html` line 1006 |
| Footer social media URLs | Actual profiles for IG, FB, LinkedIn, YouTube | `index.html` lines 1019–1022 |
| Font system decision | Design: Montserrat+Lato vs Inter+Playfair Display | `styles/styles.css` `:root` + Google Fonts URL |
| `og:image` — proper 1200×630 image | Design team creates/exports a share image | `index.html` line 21 |
| "Freidora de Aire Negra" product page | Confirm if this is a distinct product SKU or maps to `air-fryer-4-5l/` | `index.html` line 657 + new directory |

---

## Appendix A: Complete Confirmed DOM ID Inventory

**IDs that exist in index.html (confirmed):**

| ID | Element | Line |
|----|---------|------|
| `particle-canvas` | `<canvas>` | ~96 |
| `vignette-effect` | `<div>` | ~97 |
| `inicio` | `<section>` | ~95 |
| `categorias` | `<section>` | ~163 |
| `productos` | `<section>` | ~210 |
| `clientes` | `<section>` | ~942 |
| `contacto` | `<section>` | ~966 |

**IDs referenced by scripts or nav links but ABSENT from index.html:**

| ID | Referenced by | Required for |
|----|--------------|-------------|
| `form` | `send_contact_form.js` line 1 | Contact form JS handler |
| `nosotros` | Nav `<a href="#nosotros">` line 82 | Nav anchor scroll |
| `menuBurger` | `header.js` line 4 | Mobile menu open button |
| `fullscreenMenu` | `header.js` line 5 | Mobile menu overlay |
| `menuClose` | `header.js` line 6 | Mobile menu close button |
| `carnivalModal` | `carnival_modal.js` | Carnival promo modal |
| `carnivalCanvas` | `carnival_modal.js` | Carnival canvas animation |
| `seasonalPopup` | `promo_video_modal.js` | Promotional video popup |
| `careers_form` | `send_careers_form.js` | Careers/CV form |
| `clients_ticker` | `clients_scrolling_text.js` | Scrolling clients ticker |
| `clients_slider` | `clients_scrolling_text.js` | Scrolling clients ticker |

---

## Appendix B: CSS Custom Property Audit

| Token | Defined as | Defined in | Used (hyphen) | Used (underscore) | Status |
|-------|-----------|------------|---------------|-------------------|--------|
| `--color_accent` / `--color-accent` | `--color_accent: #FBD38D` | `config_new.css`, `styles.css` | 14× in index.html inline styles | in CSS files | **BROKEN** — hyphen ≠ underscore |
| `--font_title` | `"Montserrat", sans-serif` | `styles.css` | — | in CSS rules | **BROKEN** — Montserrat not loaded |
| `--font_text` | `"Lato", sans-serif` | `styles.css` | — | in CSS rules | **BROKEN** — Lato not loaded |
| `--font-heading` | not defined anywhere | nowhere | 1× in index.html inline style | — | **BROKEN** — undefined |
| `--color_black` | `#2c3e50` (dark) in `styles.css` / `#bec2c4` (light!) in `config_new.css` | conflict | — | in CSS rules | **CONFLICT** — two contradictory definitions |
| `--color_white` | `#ffffff` in `styles.css` / `#000000` (black!) in `config_new.css` | conflict | — | in CSS rules | **CONFLICT** — `config_new.css` inverts semantics; `styles.css` wins if loaded last |

**Note on `config_new.css` token conflict**: `config_new.css` defines `--color_black: #bec2c4` (a light gray) and `--color_white: #000000` (black). These are semantically inverted. If `config_new.css` ever loads *after* `styles.css`, all elements using `--color_black` would show light gray text and `--color_white` elements would appear black. Verify cascade order. Recommend aliasing via `styles.css` and deprecating `config_new.css`.

---

*End of handoff document.*
