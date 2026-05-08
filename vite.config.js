import { defineConfig } from 'vite';
import legacy from '@vitejs/plugin-legacy';
import { resolve } from 'path';
import fs from 'fs';

// Find all HTML files in the directory recursively
function getHtmlEntries(dir, fileList = {}) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = resolve(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      if (file !== 'node_modules' && file !== '.git' && file !== 'dist') {
        getHtmlEntries(fullPath, fileList);
      }
    } else if (file.endsWith('.html')) {
      const name = fullPath.replace(resolve(__dirname), '').replace(/\\/g, '/').replace(/^\//, '').replace(/\.html$/, '').replace(/\//g, '_') || 'main';
      fileList[name] = fullPath;
    }
  }
  return fileList;
}

export default defineConfig({
  plugins: [
    legacy({
      targets: ['defaults', 'not IE 11'],
      polyfills: ['es.promise.finally', 'es/map', 'es/set'],
      modernPolyfills: true
    })
  ],
  build: {
    target: 'es2015',
    rollupOptions: {
      input: getHtmlEntries(__dirname)
    }
  }
});
