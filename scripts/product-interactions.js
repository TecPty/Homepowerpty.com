document.addEventListener('DOMContentLoaded', function () {
  // Interacciones de productos (robusto con o sin <picture>)
  const productImages = document.querySelectorAll('.product_image_wrapper');
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImage');
  const modalCaption = document.getElementById('modalCaption');

  productImages.forEach((wrapper) => {
    const picture = wrapper.querySelector('picture');
    const img = wrapper.querySelector('.product_img');
    if (!img) return;

    let isMainImage = true;
    const mainSrc = img.getAttribute('src');
    const boxSrc = img.dataset.box || '';

    // Alternar fuentes si existe <picture> y/o hay data-box
    const toggleImageSources = (showHover) => {
      if (!boxSrc) return;

      if (picture) {
        const mainSources = Array.from(
          picture.querySelectorAll('source:not([data-hover])')
        );
        const hoverSources = Array.from(
          picture.querySelectorAll('source[data-hover]')
        );

        if (showHover) {
          mainSources.forEach((source) => {
            source.dataset.originalSrcset = source.srcset;
            source.srcset = '';
          });
          hoverSources.forEach((source) => {
            source.srcset = source.dataset.originalSrcset || source.srcset;
          });
        } else {
          mainSources.forEach((source) => {
            source.srcset = source.dataset.originalSrcset || source.srcset;
          });
          hoverSources.forEach((source) => {
            source.srcset = '';
          });
        }
      }

      // Fallback para alternar imagen base
      if (showHover) {
        img.src = boxSrc;
        isMainImage = false;
      } else {
        img.src = mainSrc;
        isMainImage = true;
      }
    };

    // Hover (si hay data-box)
    if (boxSrc) {
      wrapper.addEventListener('mouseenter', () => toggleImageSources(true));
      wrapper.addEventListener('mouseleave', () => toggleImageSources(false));
    }

    // Abrir modal al hacer click
    img.addEventListener('click', () => {
      if (!modal || !modalImg) return;
      modal.style.display = 'block';
      modalImg.src = isMainImage
        ? img.getAttribute('src') || mainSrc
        : boxSrc || mainSrc;
      if (modalCaption) modalCaption.textContent = img.alt || '';
    });
  });

  // Cerrar modal
  const closeModal = document.querySelector('.close-modal');
  if (closeModal && modal) {
    closeModal.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  // Cerrar modal al hacer click fuera de la imagen
  window.addEventListener('click', (e) => {
    if (modal && e.target === modal) {
      modal.style.display = 'none';
    }
  });

  // Cerrar modal con ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.style.display === 'block') {
      modal.style.display = 'none';
    }
  });
});



