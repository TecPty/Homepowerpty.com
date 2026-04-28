// @ts-check
const { test, expect } = require('@playwright/test');

// ─── 1. SMOKE — La página carga correctamente ────────────────────────────────
test('página carga con título correcto', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/Home Power/i);
  await expect(page.locator('header.luxury-header')).toBeVisible();
  await expect(page.locator('h1.hero-title')).toBeVisible();
  await expect(page.locator('#catalogo')).toBeVisible();
});

// ─── 2. WHATSAPP — Botón flotante visible y funcional en mobile ──────────────
test('botón flotante de WhatsApp visible en mobile', async ({ page }) => {
  await page.goto('/');

  const btn = page.locator('.floating-whatsapp-btn');
  await expect(btn).toBeVisible();

  const href = await btn.getAttribute('href');
  expect(href).toMatch(/^https:\/\/wa\.me\//);

  // Verificamos que abre en nueva pestaña (target=_blank) — requisito de seguridad
  const rel = await btn.getAttribute('rel');
  expect(rel).toContain('noopener');
});

// ─── 3. FILTRO — Filtrar por categoría muestra solo esos productos ───────────
test('filtro de catálogo muestra solo productos de la categoría seleccionada', async ({ page }) => {
  await page.goto('/');

  // Scroll al catálogo para activar el JS del filtro
  await page.locator('#catalogo').scrollIntoViewIfNeeded();

  // Click en "Batidoras"
  const filterBatidoras = page.locator('.filter-item[data-category="mixer"]');
  await filterBatidoras.click();
  await expect(filterBatidoras).toHaveClass(/active/);

  // Al menos un producto de "mixer" debe ser visible
  const mixerProduct = page.locator('.product[data-category="mixer"]').first();
  await expect(mixerProduct).toBeVisible({ timeout: 2000 });

  // Un producto de otra categoría debe estar oculto (display: none)
  const airFryerProduct = page.locator('.product[data-category="air_fryer"]').first();
  await expect(airFryerProduct).toBeHidden();

  // Volver a "Todos" restaura la vista completa
  await page.locator('.filter-item[data-category="all"]').click();
  await expect(airFryerProduct).toBeVisible({ timeout: 2000 });
});

// ─── 4. FORMULARIO DE CONTACTO — Validación de campos requeridos ─────────────
test('formulario de contacto tiene campos requeridos y botón de envío', async ({ page }) => {
  await page.goto('/');

  await page.locator('#contacto').scrollIntoViewIfNeeded();

  const form = page.locator('#form');
  await expect(form).toBeVisible();

  // Campos requeridos existen
  await expect(form.locator('input[name="name"][required]')).toBeVisible();
  await expect(form.locator('input[name="email"][required]')).toBeVisible();

  // Botón de envío visible
  const submitBtn = form.locator('button[type="submit"].btn-whatsapp-submit');
  await expect(submitBtn).toBeVisible();
  await expect(submitBtn).toContainText(/enviar/i);

  // Al hacer submit con campos vacíos, el browser bloquea (validación nativa HTML5)
  await submitBtn.click();
  // Si la página no navega ni recarga, la validación HTML5 detuvo el envío
  await expect(page).toHaveURL('/');
});

// ─── 5. LINKS WHATSAPP DE PRODUCTO — Formato correcto en CTAs del catálogo ───
test('CTAs de productos tienen href de WhatsApp con texto prefillado', async ({ page }) => {
  await page.goto('/');

  const productCtas = page.locator('.product_cta');
  const count = await productCtas.count();
  expect(count).toBeGreaterThan(0);

  // Verificamos el primer CTA visible
  const firstCta = productCtas.first();
  const href = await firstCta.getAttribute('href');
  expect(href).toMatch(/^https:\/\/wa\.me\/507/);
  expect(href).toContain('text=');
});

// ─── 6. ANCHOR #testimonios — scroll al carrusel de clientes ─────────────────
test('nav link #testimonios hace scroll al carrusel de clientes', async ({ page }) => {
  await page.goto('/#testimonios');
  await page.waitForLoadState('domcontentloaded');

  // El anchor target y la sección destino deben existir en el DOM
  await expect(page.locator('#testimonios')).toBeAttached();
  await expect(page.locator('#clientes')).toBeVisible();
});

// ─── 7. ANCHOR #oportunidades — scroll al formulario de empleos ──────────────
test('nav link #oportunidades hace scroll al formulario de empleos', async ({ page }) => {
  await page.goto('/#oportunidades');
  await page.waitForLoadState('domcontentloaded');

  // La sección y el form deben existir y ser visibles
  await expect(page.locator('#oportunidades')).toBeAttached();
  await expect(page.locator('#careers_form')).toBeVisible();
});

// ─── 8. FORMULARIO EMPLEOS — todos los campos requeridos por el JS ───────────
test('sección #oportunidades tiene todos los campos requeridos', async ({ page }) => {
  await page.goto('/');

  await page.locator('#oportunidades').scrollIntoViewIfNeeded();

  // Verificar form container y mensaje de estado
  await expect(page.locator('#careers_form')).toBeVisible();
  await expect(page.locator('#careers_form_msg')).toBeAttached();

  // Campos de texto
  await expect(page.locator('#careers_form input[name="full_name"]')).toBeVisible();
  await expect(page.locator('#careers_form input[name="email"]')).toBeVisible();
  await expect(page.locator('#careers_form input[name="phone"]')).toBeVisible();
  await expect(page.locator('#careers_form input[name="position"]')).toBeVisible();

  // File upload
  await expect(page.locator('#cv_trigger')).toBeVisible();
  await expect(page.locator('#cv_file')).toBeAttached();
  await expect(page.locator('#file_name')).toBeAttached();

  // Submit button con clase correcta para el JS
  await expect(page.locator('#careers_form .careers_submit')).toBeVisible();
});

// ─── 9. CSS tokens — config_new.css NO está linkeado en <head> ───────────────
test('config_new.css no está linkeado en el head de la página', async ({ page }) => {
  await page.goto('/');

  const linkCount = await page.locator('link[href*="config_new"]').count();
  expect(linkCount).toBe(0);
});
