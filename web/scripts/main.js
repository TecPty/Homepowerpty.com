import GoldBreeze  from './effects/gold-breeze.js';
import Header      from './modules/header.js';
import Catalog     from './modules/catalog.js';
import ContactForm from './modules/contact-form.js';
import CareersForm from './modules/careers-form.js';
import ScrollReveal from './modules/scroll-reveal.js';

document.addEventListener('DOMContentLoaded', () => {
  GoldBreeze.init();
  Header.init();
  Catalog.init();
  ContactForm.init();
  CareersForm.init();
  ScrollReveal.init();
});
