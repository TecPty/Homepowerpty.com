import Header     from './modules/header.js';
import GoldBreeze from './effects/gold-breeze.js';

document.addEventListener('DOMContentLoaded', () => {
  Header.init();
  GoldBreeze.init(); // guard interno: no-op si #particle-canvas no existe
});
