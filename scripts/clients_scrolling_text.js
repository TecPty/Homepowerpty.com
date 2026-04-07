(function () {
  'use strict';

  const ticker = document.getElementById('clients_ticker');
  const list = document.getElementById('clients_slider');
  const clone = document.getElementById('clients_slider_clone');

  if (!ticker || !list || !clone) return;

  // Duplicate the client track to create a seamless loop.
  clone.innerHTML = list.innerHTML;

  // Prevent deferred placeholders in the visible track.
  const primaryLogos = list.querySelectorAll('.client_logo');
  primaryLogos.forEach((img) => {
    img.loading = 'eager';
    img.decoding = 'async';
    img.removeAttribute('data-animation');
    img.removeAttribute('data-duration');
    img.removeAttribute('data-delay');
  });

  // Keep clone lightweight while avoiding conflicting animation attributes.
  const cloneLogos = clone.querySelectorAll('.client_logo');
  cloneLogos.forEach((img) => {
    img.loading = 'lazy';
    img.decoding = 'async';
    img.removeAttribute('data-animation');
    img.removeAttribute('data-duration');
    img.removeAttribute('data-delay');
  });

  const activate = () => {
    ticker.classList.add('enable-animation');
  };

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      if (entries[0].isIntersecting) {
        activate();
        obs.disconnect();
      }
    }, { threshold: 0.2 });

    observer.observe(ticker);
  } else {
    activate();
  }
})();
