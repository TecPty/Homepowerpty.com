# WCAG 2.1 AA Accessibility Checklist — Home Power PTY

## Structure and Semantics

- [ ] Single `<h1>` per page that describes the page purpose
- [ ] Heading hierarchy is logical: h1 → h2 → h3, no skipped levels
- [ ] Landmark regions present: `<header>`, `<nav>`, `<main>`, `<footer>`
- [ ] Interactive elements use semantic HTML (`<button>`, `<a href>`, `<input>`) not `<div onClick>`
- [ ] Lists use `<ul>` / `<ol>` / `<li>`, not styled `<div>` sequences
- [ ] Language attribute set: `<html lang="es">`

## Images and Media

- [ ] All `<img>` tags have meaningful `alt` text in Spanish
- [ ] Purely decorative images use `alt=""` or `role="presentation"`
- [ ] Product images have descriptive alt text (product name + key feature)
- [ ] Client logos have alt text identifying the brand
- [ ] Video has captions or a text transcript if audio content is informational
- [ ] Autoplay video is muted and has visible pause control

## Color and Contrast

- [ ] Normal text (< 18px or < 14px bold) contrast ratio ≥ 4.5:1
- [ ] Large text (≥ 18px or ≥ 14px bold) contrast ratio ≥ 3:1
- [ ] UI components (buttons, inputs, icons) contrast ≥ 3:1 against background
- [ ] Status is not communicated by color alone (error, success, selected state)
- [ ] Focus indicator is visible and has ≥ 3:1 contrast against adjacent colors

## Keyboard and Focus

- [ ] All interactive elements are reachable by Tab key
- [ ] Tab order follows visual reading order (top-to-bottom, left-to-right)
- [ ] Focus is never trapped (except inside open modals, where it is intentionally contained)
- [ ] Modals: focus moves into modal on open; returns to trigger on close
- [ ] Custom dropdowns and filters are operable with arrow keys and Enter/Space
- [ ] Skip navigation link present and functional (or first focusable element reaches main content quickly)

## Forms

- [ ] Every input has an associated `<label>` (via `for`/`id` or `aria-label`)
- [ ] Required fields are marked with `aria-required="true"` and a visual indicator
- [ ] Error messages are associated with the specific field via `aria-describedby`
- [ ] Error messages describe the problem and the fix, not just "campo requerido"
- [ ] Autocomplete attributes set for standard fields (name, email, tel)
- [ ] File upload control has an accessible label and explains accepted formats

## Interactive Components

- [ ] Mobile navigation toggle has `aria-expanded` that reflects open/closed state
- [ ] Navigation menu hidden from screen readers when collapsed (`aria-hidden` or `display:none`)
- [ ] Modal has `role="dialog"`, `aria-modal="true"`, and `aria-labelledby` pointing to modal title
- [ ] Close buttons have discernible text or `aria-label`
- [ ] Icon-only buttons have `aria-label` (WhatsApp FAB, social icons, close X)
- [ ] Filter buttons communicate selected state via `aria-pressed` or `aria-selected`
- [ ] Product cards: entire card is not one giant link; action elements have individual labels

## Mobile and Touch

- [ ] Touch targets ≥ 44×44 CSS pixels (WCAG 2.5.5)
- [ ] No content relies on hover-only states that are inaccessible on touch
- [ ] Pinch-zoom is not disabled (`user-scalable=no` is absent or overridden)
- [ ] Content is not obscured by fixed/sticky elements at any viewport width
