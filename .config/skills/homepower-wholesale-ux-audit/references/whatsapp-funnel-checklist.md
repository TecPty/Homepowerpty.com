# WhatsApp Funnel and CTA Checklist — Home Power PTY

## Link Construction

- [ ] All WhatsApp CTAs use `https://wa.me/<number>` format (not `api.whatsapp.com` or shortlinks)
- [ ] Phone number uses full international format with country code (e.g., `50769XXXXXX` for Panama)
- [ ] Pre-filled message (`?text=`) is URL-encoded correctly (no raw spaces or special characters)
- [ ] Pre-filled message is written in Spanish and includes business context
- [ ] Product-level CTAs pass the product name in the pre-filled message

## CTA Copy and Placement

- [ ] WhatsApp CTA copy is action-oriented and wholesale-specific:
  - ✅ "Consultar precios al por mayor"
  - ✅ "Pedir cotización por WhatsApp"
  - ❌ "Contáctanos" (too generic)
  - ❌ "Más información" (low intent)
- [ ] Floating WhatsApp button is present and visible on all scroll depths
- [ ] At least one WhatsApp CTA is above the fold on mobile without any scrolling
- [ ] Hero section includes a WhatsApp CTA or a direct scroll-to-catalog action
- [ ] Product detail pages (productos/) each have a standalone WhatsApp inquiry link
- [ ] Contact section includes WhatsApp as the preferred contact method with clear copy

## Visual Identity

- [ ] WhatsApp button uses official brand green (#25D366 or close variant) for instant recognition
- [ ] Button icon is the WhatsApp logo or a phone/chat icon that reads as messaging
- [ ] Floating button does not overlap form submit buttons, navigation, or product cards
- [ ] On desktop, floating button has a label text alongside the icon

## Interrupt Patterns

- [ ] No modal or overlay appears between landing and first WhatsApp click
- [ ] Seasonal/promotional modals (carnival_modal.js, seasonal_popup.js) do not fire on first scroll before user orientation completes
- [ ] If a modal promotes a product, it includes its own WhatsApp link
- [ ] Promo video modal does not autoplay with sound on mobile

## Funnel Exit Points to Audit

These are moments where a user could lose intent:

1. Hero → no clear next step → user scrolls aimlessly
2. Filter → zero results state → no fallback CTA
3. Product card → taps for detail → no WhatsApp link on detail page
4. Testimonials → builds trust but no CTA nearby → trust moment wasted
5. Contact form → too many fields or confusing labels → abandons to competitor
6. Footer → user reaches bottom → no final WhatsApp recovery CTA

## Measurement Hooks

When recommending tracking, prefer solutions that require no external scripts (no Google Analytics JS bundles), using:
- UTM parameters appended to WhatsApp `wa.me` links per section
- Custom `data-event` attributes that can be consumed by a lightweight inline analytics snippet
