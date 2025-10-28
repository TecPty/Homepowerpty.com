# Copilot Instructions for Homepowerpty.com

## Project Overview
Static website for Home Power Pty built with vanilla HTML, CSS, and JavaScript. No modern frameworks or build systems. Backend limited to simple PHP forms for data submission. Site focuses on product catalog display, contact forms, and career applications.

## Core Architecture

### Key Components
- `index.html`: Main entry point with base structure and asset references
- `unified_forms.js`: Central form handling for both contact and careers forms
- `styles/styles.css`: Global styles using CSS variables
- `php/send_form.php`: Form processing with CSRF protection and email sending

### File Structure
```
public_html/
├── .htaccess          # Performance and security rules
├── sitemap.xml        # SEO optimization
├── index.html         # Main entry
├── media/            # Images and icons
│   ├── icons/        # UI elements
│   └── images/       # Products and content
├── scripts/          # JavaScript modules
├── styles/          # CSS files
│   └── templates/    # Component styles
└── php/             # Form handlers
```

## Design Patterns

### Form System
1. **Unified Handler**: `unified_forms.js` manages both contact and career forms
2. **Real-time Validation**: Client-side validation with visual feedback
3. **Floating Labels**: Using CSS transforms and transitions:
```css
.form_label.active {
    transform: translateY(-100%) scale(0.9);
}
```
4. **Visual States**: `.valid`/`.invalid` classes with color transitions
5. **File Upload**: Specialized handling for CV uploads in careers form

### UI/UX Patterns
- Mobile-first design (breakpoints: 768px, 480px)
- Glassmorphism effects for forms and cards
- Product image hover effects (product/box swap)
- WhatsApp integration for pricing queries
- Lazy loading for performance

### Brand Variables
```css
:root {
    --color_orange: #FF9F1C;
    --color_green: #4CAF50;
    --font_title: "Montserrat", sans-serif;
    --font_text: "Lato", sans-serif;
}
```

## Development Workflow

### Local Development
1. Direct file editing - no build process
2. Use browser DevTools for debugging
3. Test forms with `test_form.php`
4. Debug logging in `debug_careers_form.js`

### Deployment Process
1. Upload to public_html/ via File Manager
2. Verify critical files:
   - `.htaccess` in root
   - `sitemap.xml` accessible
   - PHP enabled for forms
3. Run test suite:
   - Form submissions
   - Mobile responsiveness
   - Load time (target: <4s)
   - WhatsApp links

### Common Tasks

#### Adding Products
1. Add markup in `index.html` product section
2. Place images in `media/images/products/`
3. Set proper `data-category` for filtering
4. Format WhatsApp link with product code

#### Modifying Forms
1. Update HTML with semantic input names
2. Add validation rules in `unified_forms.js`
3. Update PHP handler if needed
4. Test with debug mode enabled

## Dependencies
- Google Fonts (Montserrat, Lato)
- Basic PHP environment
- No external JavaScript libraries

## AI Agent Guidelines
- Use existing CSS variables for visual consistency
- Implement both client and server validation
- Follow floating label pattern for forms
- Ensure mobile-first responsiveness
- Document changes inline
- Test critical paths:
  - Form submission flow
  - Image lazy loading
  - Mobile navigation
  - WhatsApp integration

## Support Contact
- Developer: Luis R.
- Team: Net Web
- 24/7 support for 48h post-launch

## Key Files Reference
- `index.html`: Core structure and content
- `styles/styles.css`: Global styles
- `scripts/unified_forms.js`: Form handling
- `php/send_form.php`: Backend processing