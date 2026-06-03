(function () {
  const SLIDES = [
    {
      category: "CAFETERAS",
      title: "Disfruta tu café, todos los días",
      desc: "Prácticas, elegantes y perfectas para tu rutina.",
      img: "media/images/products/CAFETERA_12_TAZAS.webp",
      href: "#productos",
    },
    {
      category: "AIR FRYER",
      title: "Cocina sin aceite, vive mejor",
      desc: "Digital 4.5L con 8 programas automáticos.",
      img: "media/images/products/AIR_FRYER.webp",
      href: "#productos",
    },
    {
      category: "SANDWICHERAS",
      title: "El desayuno perfecto cada día",
      desc: "Placas antiadherentes, diseño compacto.",
      img: "media/images/products/PANINI_2.webp",
      href: "#productos",
    },
    {
      category: "PLANCHAS",
      title: "Potencia y precisión para tu ropa",
      desc: "Base cerámica, control de temperatura.",
      img: "media/images/products/PLANCHA_VAPOR_2.webp",
      href: "#productos",
    },
    {
      category: "LICUADORAS",
      title: "Potencia en cada preparación",
      desc: "Motor 500W, jarra de vidrio 1.5L.",
      img: "media/images/products/LICUADORA_NEGRA_3.webp",
      href: "#productos",
    },
  ];

  const track = document.querySelector(".hero-slider__track");
  if (!track) return;

  const slider = document.querySelector(".hero-slider");
  const prevBtn = document.querySelector("#hero-prev");
  const nextBtn = document.querySelector("#hero-next");

  const categoryEl = track.querySelector(".hero-slider__category");
  const titleEl = track.querySelector(".hero-slider__title");
  const descEl = track.querySelector(".hero-slider__description");
  const imgEl = track.querySelector(".hero-slider__image");
  const ctaEl = track.querySelector(".hero-slider__cta");
  const dots = document.querySelectorAll(".hero-slider__dot");

  if (!categoryEl || !titleEl || !descEl || !imgEl || !ctaEl) return;

  let currentIndex = 0;
  let autoPlayTimer = null;
  const autoPlayDelay = 5000;
  const transitionDuration = 400;

  function setTransitionState(isAnimating) {
    const opacity = isAnimating ? "0" : "1";
    const transform = isAnimating ? "translateY(10px)" : "translateY(0)";
    [imgEl, categoryEl, titleEl, descEl, ctaEl].forEach((el) => {
      el.style.opacity = opacity;
      el.style.transform = transform;
    });
  }

  function applyTransitionStyles() {
    const transition = `opacity ${transitionDuration}ms ease, transform ${transitionDuration}ms ease`;
    [imgEl, categoryEl, titleEl, descEl, ctaEl].forEach((el) => {
      el.style.transition = transition;
      el.style.willChange = "opacity, transform";
    });
  }

  function updateDots() {
    dots.forEach((dot, index) => {
      const isActive = index === currentIndex;
      dot.classList.toggle("active", isActive);
      dot.classList.toggle("hero-slider__dot--active", isActive);
      dot.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function renderSlide(index) {
    const slide = SLIDES[index];
    categoryEl.textContent = slide.category;
    titleEl.textContent = slide.title;
    descEl.textContent = slide.desc;
    imgEl.src = slide.img;
    imgEl.alt = slide.title;
    ctaEl.href = slide.href;
    updateDots();
  }

  function goToSlide(index) {
    currentIndex = (index + SLIDES.length) % SLIDES.length;
    setTransitionState(true);

    window.setTimeout(() => {
      renderSlide(currentIndex);
      requestAnimationFrame(() => setTransitionState(false));
    }, transitionDuration / 2);
  }

  function goToNextSlide() {
    goToSlide(currentIndex + 1);
  }

  function goToPrevSlide() {
    goToSlide(currentIndex - 1);
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoPlayTimer = window.setInterval(goToNextSlide, autoPlayDelay);
  }

  function stopAutoPlay() {
    if (autoPlayTimer) {
      window.clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
  }

  applyTransitionStyles();
  renderSlide(currentIndex);
  setTransitionState(false);
  startAutoPlay();

  if (nextBtn) nextBtn.addEventListener("click", () => { goToNextSlide(); startAutoPlay(); });
  if (prevBtn) prevBtn.addEventListener("click", () => { goToPrevSlide(); startAutoPlay(); });

  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      goToSlide(index);
      startAutoPlay();
    });
  });

  if (slider) {
    slider.addEventListener("mouseenter", stopAutoPlay);
    slider.addEventListener("mouseleave", startAutoPlay);
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopAutoPlay();
    else startAutoPlay();
  });
})();
