import { defineConfig } from 'vite';
import legacy from '@vitejs/plugin-legacy';
import { resolve } from 'path';
import fs from 'fs';
import path from 'path';

// ── Exclusiones del build ────────────────────────────────────────────────────
const EXCLUDED_DIRS  = new Set([
  'node_modules', '.git', 'dist',
  'playwright-report', 'test-results', 'web'
]);
const EXCLUDED_FILES = /-backup\.html$/;

// ── Scan recursivo de HTML entries ───────────────────────────────────────────
function getHtmlEntries(dir, fileList = {}) {
  for (const file of fs.readdirSync(dir)) {
    const fullPath = resolve(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      if (!EXCLUDED_DIRS.has(file)) getHtmlEntries(fullPath, fileList);
    } else if (file.endsWith('.html') && !EXCLUDED_FILES.test(file)) {
      const name = fullPath
        .replace(resolve(__dirname), '')
        .replace(/\\/g, '/')
        .replace(/^\//, '')
        .replace(/\.html$/, '')
        .replace(/\//g, '_') || 'main';
      fileList[name] = fullPath;
    }
  }
  return fileList;
}

// ── Plugin: copia assets estáticos al dist/ post-build ──────────────────────
function copyStaticAssets() {
  const STATIC_DIRS  = ['styles', 'media', 'scripts'];
  const STATIC_FILES = ['robots.txt', 'sitemap.xml'];

  function copyDir(src, dest) {
    if (!fs.existsSync(src)) return;
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      const s = path.join(src, entry);
      const d = path.join(dest, entry);
      fs.statSync(s).isDirectory() ? copyDir(s, d) : fs.copyFileSync(s, d);
    }
  }

  return {
    name: 'copy-static-assets',
    closeBundle() {
      for (const dir of STATIC_DIRS) {
        copyDir(path.resolve(__dirname, dir), path.join('dist', dir));
        console.log(`  ✅ Copiado: ${dir}/ → dist/${dir}/`);
      }
      for (const file of STATIC_FILES) {
        const src = path.resolve(__dirname, file);
        if (fs.existsSync(src)) {
          fs.copyFileSync(src, path.join('dist', file));
          console.log(`  ✅ Copiado: ${file} → dist/${file}`);
        }
      }
    }
  };
}

// ── Config principal ─────────────────────────────────────────────────────────
export default defineConfig({
  plugins: [
    legacy({
      targets: ['defaults', 'not IE 11'],
      polyfills: ['es.promise.finally', 'es/map', 'es/set'],
      modernPolyfills: true
    }),
    copyStaticAssets()
  ],
  build: {
    target: 'es2015',
    rollupOptions: {
      input: getHtmlEntries(__dirname)
    }
  }
});
