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
