---
applyTo: "**/*.{html,css,js,php}"
---

# Home Power PTY - Stack & Implementation Instructions

## Purpose
These instructions apply to all coding, UX, UI, frontend, and implementation-related work in this repository.

Home Power PTY is a **Spanish-language B2B wholesale appliance website in Panama**, built as a **mobile-first product catalog and lead-generation site**, where the main conversion goal is **qualified WhatsApp inquiries from wholesale buyers**.

This is **not** a traditional DTC checkout-first e-commerce site.  
All decisions must support:
- product discovery
- trust building
- wholesale buyer clarity
- mobile usability
- WhatsApp conversion flow

---

## Business Context
- **Brand**: Home Power PTY
- **Market**: Panama / LatAm
- **Audience**: Store owners, resellers, commercial buyers, wholesale clients
- **Primary CTA**: WhatsApp
- **Language**: Spanish
- **Traffic Priority**: Mobile-first
- **Site Type**: Single-page catalog + contact/recruitment forms

---

## Stack Constraints
Treat these as fixed unless the user explicitly approves a strategic change.

- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Backend**: PHP 8+
- **Hosting**: Hostinger
- **Deployment**: GitHub Actions + FTP
- **Assets**: WebP images, MP4 promo videos

---

## Non-Negotiable Rules

### 1) No framework recommendations by default
Do not recommend or introduce:
- React
- Next.js
- Vue
- Nuxt
- Angular
- Tailwind
- Bootstrap
- jQuery
- heavy animation libraries
- unnecessary third-party dependencies

Only mention strategic migrations if the user explicitly asks for alternatives.

### 2) Mobile-first is mandatory
Assume the primary browsing experience is mobile.

Prioritize:
- small-screen readability
- touch usability
- thumb-friendly spacing
- performance on mobile networks
- reduced layout shift
- clear CTA visibility without overlap

Desktop improvements must never harm mobile behavior.

### 3) Spanish-first copy
All user-facing copy proposals must default to **Spanish**, unless the user explicitly requests another language.

This includes:
- headings
- buttons
- helper text
- form labels
- validation messages
- trust copy
- product UX microcopy
- modal text
- CTA text

Keep copy commercially clear, direct, and appropriate for wholesale buyers in Panama/LatAm.

### 4) WhatsApp is the primary conversion path
Treat WhatsApp as the main CTA and lead-generation endpoint.

Prioritize:
- WhatsApp button visibility
- WhatsApp CTA clarity
- prefilled message relevance
- low-friction contact paths
- trust reinforcement before click
- mobile-safe fixed CTA behavior

Do not prioritize cart, checkout, or account-style UX patterns unless explicitly requested.

### 5) B2B wholesale logic first
This website serves wholesale buyers, not casual retail impulse shoppers.

Recommendations must prioritize:
- credibility
- clear product browsing
- catalog confidence
- business legitimacy
- fast buyer understanding
- low-friction inquiry flow
- trust signals from clients and company information

Avoid DTC-style recommendations that do not fit a wholesale lead funnel.

### 6) Lightweight performance discipline
Prefer lightweight native solutions.

Prioritize:
- semantic HTML
- modular CSS
- minimal JS
- deferred or lazy-loaded non-critical assets
- optimized images
- stable layouts
- low bundle overhead

Avoid adding code that creates unnecessary complexity for a simple stack.

### 7) Accessibility is required
Assume WCAG 2.1 AA compliance is expected.

Always consider:
- semantic structure
- keyboard navigation
- visible focus states
- accessible labels
- contrast
- screen-reader clarity
- modal and form accessibility

Accessibility fixes are not optional.

### 8) Preserve structure unless approved
Do not change:
- core file structure
- naming conventions
- deployment flow
- backend flow
- PHP endpoints
- content architecture

unless the user explicitly approves it.

You may suggest improvements, but do not assume permission to restructure.

### 9) Brand consistency matters
Keep the interface aligned with the existing Home Power commercial identity:
- bold
- trustworthy
- clear
- practical
- conversion-oriented

Do not propose aesthetics that feel overly editorial, luxury-only, or disconnected from appliance wholesale retail reality.

### 10) Do not implement unapproved changes
By default:
- analyze
- recommend
- explain
- outline
- draft
- propose

Do not assume permission to:
- rewrite files
- refactor architecture
- rename files
- delete files
- replace flows
- introduce dependencies

Implementation requires explicit approval from the user.

---

## Default Decision Priorities
When making recommendations, optimize in this order:

1. broken functionality
2. mobile usability
3. WhatsApp conversion clarity
4. accessibility
5. trust and credibility
6. performance
7. maintainability
8. visual polish

---

## Preferred UX Direction
Favor:
- clear hierarchy
- fast scanning
- simple navigation
- strong CTA visibility
- clear contact paths
- business trust signals
- concise product presentation
- low-friction forms

Avoid:
- overdesigned interfaces
- excessive animation
- clutter
- generic SaaS patterns
- checkout-first assumptions
- desktop-first layouts

---

## Coding Style Guidance
When proposing or writing code:
- keep solutions simple
- prefer native browser capabilities
- avoid overengineering
- preserve readability
- respect existing patterns unless clearly broken
- isolate changes to the smallest safe scope
- avoid introducing hidden dependencies

---

## Output Expectations for Code Assistance
When asked to review or improve code:
- identify the issue clearly
- explain impact briefly
- propose the smallest effective fix
- mention affected files
- note risks if any
- ask for approval before implementation if the change is not already authorized

---

## Audit vs Implementation Behavior
If the request is analytical, prioritize diagnosis and recommendations.  
If the request is implementation-oriented, still respect all repository constraints and approval rules.

Do not blur analysis and execution.

---

## Repository Identity Reminder
This repository supports a **Spanish-speaking, mobile-first, WhatsApp-driven B2B wholesale appliance catalog in Panama**.

Every suggestion should fit that reality.