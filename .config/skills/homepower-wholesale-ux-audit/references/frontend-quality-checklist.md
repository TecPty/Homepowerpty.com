# Frontend Quality and Performance Checklist — Home Power PTY

## Core Web Vitals Targets (Mobile)

| Metric | Target | Fail Threshold |
|--------|--------|----------------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | > 4.0s |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | > 0.25 |
| INP (Interaction to Next Paint) | ≤ 200ms | > 500ms |
| FCP (First Contentful Paint) | ≤ 1.8s | > 3.0s |

## Images and Media

- [ ] All images served as WebP with appropriate fallback
- [ ] Hero image and above-the-fold images are NOT lazy-loaded (`loading="eager"` or no attribute)
- [ ] All below-fold images use `loading="lazy"`
- [ ] Images have explicit `width` and `height` attributes to prevent CLS
- [ ] Product thumbnails are pre-sized at display dimensions (no oversized images scaled down via CSS)
- [ ] Promotional video (`/media/videos/`) uses `preload="none"` until modal is triggered
- [ ] No autoplay video loads on mobile (bandwidth concern)

## CSS

- [ ] CSS custom properties (config_new.css) are used consistently; no hardcoded hex values that duplicate tokens
- [ ] No duplicate selector blocks across styles.css and templates/*.css for the same component
- [ ] Media queries follow mobile-first pattern (`min-width`), not desktop-first (`max-width`)
- [ ] No `!important` used to override layout rules (indicates specificity debt)
- [ ] Animations use `transform` and `opacity` only (GPU-composited); no `top/left/width` animations
- [ ] Transitions have `prefers-reduced-motion` override: `@media (prefers-reduced-motion: reduce)`

## JavaScript

- [ ] No render-blocking `<script>` tags in `<head>` without `defer` or `async`
- [ ] Scripts that only apply to a section are not initialized globally
- [ ] Modal JS (carnival_modal.js, promo_video_modal.js) does not execute on pages where the modal doesn't exist
- [ ] Event listeners are removed when components are destroyed or modals are closed
- [ ] filter_products.js does not recalculate DOM on every keystroke (debounce or throttle in place)
- [ ] No console.log statements in production code
- [ ] No inline `onclick` handlers in HTML; event binding is in JS files

## Forms and PHP

- [ ] CSRF token is fetched fresh per form session (get_csrf_token.php)
- [ ] send_form.php validates all inputs server-side (not just client-side)
- [ ] File uploads (upload_cv.php) validate: file type (allowlist), file size limit, no direct execution path
- [ ] Form submission uses `fetch` with error handling; network failure is surfaced to the user
- [ ] Success state disables the submit button to prevent duplicate submissions

## HTML Hygiene

- [ ] `<title>` and `<meta name="description">` are present and product/page-specific
- [ ] Open Graph tags (`og:title`, `og:image`, `og:description`) are present on index.html and product pages
- [ ] No duplicate `id` attributes in the document
- [ ] `<link rel="canonical">` present on product detail pages
- [ ] Favicon is served in modern format (SVG or 32×32 PNG); no 404 on `/favicon.ico`
- [ ] sitemap.xml includes all product detail page URLs

## Render Stability (CLS)

- [ ] Client logo images have explicit dimensions or aspect-ratio CSS set
- [ ] Font faces are declared with `font-display: swap`
- [ ] No elements injected above existing content after page load
- [ ] Sticky header height is factored into scroll-margin / scroll-padding-top for anchor links

## Asset Delivery

- [ ] All CSS and JS files are served with long-term cache headers (handled at Hostinger level)
- [ ] No unused CSS template files are loaded on pages that don't need them
- [ ] Video files are not in the HTML critical path (only loaded on modal trigger)
