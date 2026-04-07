---
name: homepower-wholesale-ux-audit
description: Expert UX/UI, CRO, accessibility, and frontend audit skill for Home Power PTY, a Spanish-language B2B wholesale appliance website in Panama. Use for conversion flow, WhatsApp lead generation, mobile-first usability, product catalog UX, trust signals, performance, WCAG 2.1 AA checks, and frontend quality in LatAm wholesale funnels.
argument-hint: Audit type: full | quick-wins | section | performance | accessibility | fix-only
user-invocable: true
---

# Home Power PTY - UX/UI Audit Skill

Senior-level audit workflow combining UX/UI, CRO, accessibility, frontend QA, and mobile-first ecommerce analysis for a B2B wholesale appliance catalog in LatAm.

## Primary Objective

Audit the site to detect and prioritize:
- conversion blockers
- UX friction
- accessibility failures (WCAG 2.1 AA)
- frontend quality defects
- mobile usability issues
- trust gaps
- performance bottlenecks
- WhatsApp lead-generation weaknesses

The goal is to improve qualified wholesale lead generation without breaking the current stack, structure, or brand consistency.

## Business Context

### Company Snapshot
- Brand: Home Power PTY
- Website: homepowerpty.com
- Market: Panama
- Business model: B2B wholesale appliance distribution
- Primary conversion goal: qualified WhatsApp inquiries from wholesale buyers
- Secondary goals: product discovery, trust building, contact form submissions, recruitment inquiries
- Site language: Spanish
- Audience: store owners, resellers, commercial buyers, wholesale clients
- Traffic profile: mobile-first
- Site type: single-page commercial catalog with dual lead forms

### UX Reality
Treat the site as:
- a trust-building wholesale catalog
- a lead-generation funnel
- a product browsing experience
- a WhatsApp conversion bridge

Do not evaluate it as a DTC checkout flow.

## Technical Constraints

- Frontend: HTML5 + modular CSS3 + Vanilla JS
- Backend: PHP 8+
- Hosting: Hostinger
- Deploy: GitHub Actions + FTP
- Assets: WebP + MP4

### Non-Goals
- Do not recommend framework migration or architecture rewrite unless explicitly requested.
- Prefer incremental, low-risk, high-impact changes.

## Site Sections In Scope

1. Social header bar
2. Main header and navigation
3. Hero banner
4. Product catalog and filters
5. Client logo grid
6. About section
7. Testimonials
8. Dual contact forms
9. Footer
10. Floating WhatsApp CTA
11. Promo video modal
12. Seasonal/legacy modal logic

## Input Modes

Use the argument hint value to pick depth and output style.

### `full`
Complete audit across all sections and technical layers.

### `quick-wins`
Top high-impact issues that can be fixed quickly, with emphasis on broken functionality, trust, accessibility, and performance.

### `section`
Audit one specified section only, such as hero, catalog, forms, footer, testimonials, or navigation.

### `performance`
Focus on Core Web Vitals, media loading, script loading, render stability, and unnecessary payload.

### `accessibility`
Focus on WCAG 2.1 AA issues, keyboard flow, semantics, labels, accessible names, and contrast.

### `fix-only`
User has already identified a likely issue.
In this mode:
1. Minimize diagnosis, but still validate the cause within the smallest necessary scope.
2. Read only the directly affected file(s) plus immediate dependencies.
3. Propose the smallest safe fix.
4. Provide a copy-pasteable patch only if the user has already approved implementation.
5. State the acceptance criterion to verify the fix.
6. Note regression risk and adjacent files to re-test.

## Context Loading Rule

Load only the minimum relevant context needed for the selected mode.

### Default loading priority
1. `index.html`
2. Relevant CSS file(s) for the affected section
3. Relevant JS file(s) for the affected interaction
4. Related PHP endpoint(s) only if forms/submission are involved
5. Product detail pages only if the request involves a specific product page

### Full audit default
For a full audit, start with:
1. `index.html`
2. `styles/styles.css`
3. `styles/config_new.css`

Then expand only into the section-specific scripts and templates needed to support findings.

Do not read unnecessary files just to appear thorough.

## Audit Workflow

1. Confirm audit mode and scope.
2. Map primary and secondary conversion paths.
3. Evaluate UX and CRO.
4. Evaluate mobile-first usability.
5. Evaluate accessibility (WCAG 2.1 AA).
6. Evaluate frontend quality.
7. Evaluate performance.
8. Prioritize findings by severity, business impact, and effort.
9. Produce a developer-ready handoff.

## Severity Rules

- **Critical**: blocks conversion, lead capture, primary navigation, core interaction, or creates severe trust failure
- **High**: major friction, broken secondary flow, strong credibility damage, serious accessibility barrier, or meaningful performance regression
- **Medium**: noticeable quality problem with workaround
- **Low**: polish issue or minor inconsistency

## Classification Rules

Every finding must be labeled as one of these:

- **Confirmed**: directly supported by repository evidence
- **Likely**: strongly suggested by repository evidence but not fully verified
- **Needs Validation**: plausible issue that requires browser/runtime/manual confirmation

Never present an assumption as confirmed fact.

## Defect Separation Rule

Do not merge distinct issues into one line item when they affect different systems.

Examples:
- missing script loading vs broken script logic
- corrupted copy vs weak commercial messaging
- dead legacy code vs active broken code
- accessibility defects vs performance defects
- invalid markup vs visual layout defects

## Evidence Rule

Every Critical and High severity finding must include:
- exact affected file(s)
- exact broken feature, behavior, or user flow
- repository evidence that supports the finding
- classification: Confirmed, Likely, or Needs Validation
- minimal safe fix direction
- recommended implementation order

If a finding references script loading, enumerate:
- the missing or misloaded script
- where it should be loaded
- which feature it powers
- what breaks when it is absent

If a finding references broken copy, distinguish between:
- corrupted text
- placeholder text
- mixed-language inconsistency
- weak commercial messaging

## Output Strictness Rule

Do not return only an executive summary or broad conclusions.

Do not use vague phrases such as:
- needs improvement
- is not ideal
- could be better
- appears problematic

Prefer precise language:
- what is broken
- where it is broken
- why it breaks
- what it affects
- what should be fixed first

Do not collapse multiple broken systems into one generic statement unless you also enumerate each impacted feature separately.

## Required Output Structure

Return the audit in this exact order:

### 1. Executive Summary
Include:
- overall conversion health
- most serious blockers
- top 3 priorities
- expected upside from fixing them

### 2. Critical Issues
For each item, use this exact structure:

#### [Issue Title]
- **Severity:** Critical
- **Classification:** Confirmed | Likely | Needs Validation
- **Type:** Bug | UX | Accessibility | Performance | Content | SEO | Maintainability
- **Affected file(s):** ...
- **Broken feature / flow:** ...

**Problem**
- exact defect
- why it happens
- where it happens

**Evidence**
- repository evidence
- file references
- script includes, selectors, markup, or code behavior as relevant

**User Impact**
- what the visitor experiences

**Business Impact**
- effect on leads, trust, usability, or conversion

**Minimal Safe Fix**
- smallest correct stack-compatible fix direction

**Risks / Dependencies**
- what must be checked before changing it
- possible regressions

**Priority Order**
- implementation order number

### 3. High Issues
Use the same structure as Critical issues.

### 4. Medium Issues
For each item, include:
- title
- type
- affected area
- evidence
- why it matters
- recommended fix
- effort

### 5. Low Issues
Brief list format is acceptable.

### 6. Quick Wins Under 30 Minutes
List concrete, low-risk fixes ordered by impact.

### 7. Safe Implementation Order
Always prioritize:
1. functional restoration
2. lead-generation flow recovery
3. trust and credibility issues
4. accessibility failures
5. HTML/CSS structural defects
6. performance optimizations
7. secondary UX polish

### 8. Validation Checklist
Include:
- mobile checks
- desktop checks
- form checks
- WhatsApp flow checks
- accessibility checks
- regression checks

### 9. Approval-Gated Changes
List changes that should not be implemented without explicit approval.

## Developer Handoff Requirement

The audit must be actionable enough that a developer can begin fixing issues without re-discovering the problem from scratch.

For every Critical and High issue, include:
1. issue title
2. severity
3. classification
4. type
5. affected file(s)
6. evidence
7. broken feature or user flow
8. user-facing impact
9. business impact
10. minimal safe fix
11. risks or dependencies
12. implementation priority

## Quality Bar

A completed audit must:
- align with the wholesale lead-generation goal
- include mobile-first findings
- include WhatsApp funnel analysis
- include WCAG 2.1 AA findings
- include performance and frontend quality findings
- provide prioritized and implementable actions
- avoid framework migration recommendations unless requested

## Repo-Aware File Targets

Use these paths when preparing findings or implementation notes:
- `index.html`
- `styles/config_new.css`
- `styles/styles.css`
- `styles/templates/*.css`
- `scripts/header.js`
- `scripts/filter_products.js`
- `scripts/send_contact_form.js`
- `scripts/send_careers_form.js`
- `scripts/product-interactions.js`
- `scripts/promo_video_modal.js`
- `scripts/carnival_modal.js`
- `scripts/file_upload.js`
- `php/send_form.php`
- `php/upload_cv.php`
- `php/get_csrf_token.php`
- `productos/<slug>/index.html`
- `productos/<slug>/img/`

## Deep-Dive References

Load on demand when needed:
- [CRO and conversion checklist](./references/cro-checklist.md)
- [WCAG 2.1 AA accessibility checklist](./references/wcag-checklist.md)
- [WhatsApp funnel and CTA checklist](./references/whatsapp-funnel-checklist.md)
- [Frontend quality and performance checklist](./references/frontend-quality-checklist.md)

## Prompt Starters
- `/homepower-wholesale-ux-audit full`
- `/homepower-wholesale-ux-audit quick-wins`
- `/homepower-wholesale-ux-audit section hero`
- `/homepower-wholesale-ux-audit performance`
- `/homepower-wholesale-ux-audit accessibility`
- `/homepower-wholesale-ux-audit fix-only`