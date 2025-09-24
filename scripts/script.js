st.contains('active')) {
                        activeCategories.push(categoryName);
                    } else {
                        activeCategories = activeCategories.filter(cat => cat !== categoryName);
                    }
                    
                    // Filter products
                    products.forEach(product => {
                        const productCategory = product.dataset.category;
                        
                        if (activeCategories.length === 0 || activeCategories.includes(productCategory)) {
                            product.style.display = 'block';
                        } else {
                            product.style.display = 'none';
                        }
                    });
                });
            });
        })();

        // CLIENTS SLIDER FUNCTIONALITY
(function() {
    const slider = document.getElementById('clients_slider');
    const leftArrow = document.getElementById('slider_clients_arrow_left');
    const rightArrow = document.getElementById('slider_clients_arrow_right');
    let isAnimating = false;

    // Verificar que todos los elementos existan
    if (!slider || !leftArrow || !rightArrow) {
        console.log('Elementos del slider no encontrados');
        return;
    }

    console.log('Slider de clientes inicializado con 10 logos');

    function getSliderValues() {
        const windowWidth = window.innerWidth;
        if (windowWidth > 864) {
            // Desktop: 4 clientes visibles
            return { moveDistance: 25, resetMargin: -100 }; // 25% = 1 cliente
        } else if (windowWidth > 768) {
            // Tablet: 2 clientes visibles
            return { moveDistance: 50, resetMargin: -50 };
        } else {
            // Móvil: 1 cliente visible
            return { moveDistance: 100, resetMargin: 0 };
        }
    }

    async function moveSlide(direction) {
        if (isAnimating) return;
        isAnimating = true;

        const { moveDistance, resetMargin } = getSliderValues();
        const margin = direction === 'right' ? `-${moveDistance}` : '0';

        try {
            await animateSlide(margin);
            updateSlideOrder(direction);
            resetSlidePosition(resetMargin);
        } catch (error) {
            console.error('Error en la animación del slider:', error);
        } finally {
            setTimeout(() => {
                isAnimating = false;
            }, 100);
        }
    }

    function animateSlide(margin) {
        return new Promise(resolve => {
            slider.style.transition = 'transform 400ms cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            slider.style.transform = `translateX(${margin}%)`;
            setTimeout(resolve, 400);
        });
    }

    function updateSlideOrder(direction) {
        if (direction === 'right') {
            // Mover el primer elemento al final
            const first = slider.firstElementChild;
            if (first) {
                slider.appendChild(first);
            }
        } else {
            // Mover el último elemento al principio
            const last = slider.lastElementChild;
            if (last) {
                slider.prepend(last);
            }
        }
    }

    function resetSlidePosition(resetMargin) {
        slider.style.transition = 'none';
        slider.style.transform = `translateX(${resetMargin}%)`;
    }

    // Event listeners para las flechas
    rightArrow.addEventListener('click', (e) => {
        e.preventDefault();
        moveSlide('right');
    });

    leftArrow.addEventListener('click', (e) => {
        e.preventDefault();
        moveSlide('left');
    });

    // Touch support para móviles
    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartTime = 0;

    slider.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
        touchStartTime = Date.now();
    }, { passive: true });

    slider.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].clientX;
        const touchTime = Date.now() - touchStartTime;
        
        // Solo procesar si es un swipe rápido
        if (touchTime < 500) {
            handleSwipe(touchStartX, touchEndX);
        }
    }, { passive: true });

    function handleSwipe(startX, endX) {
        const swipeThreshold = 50;
        const diff = startX - endX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                moveSlide('right');
            } else {
                moveSlide('left');
            }
        }
    }

    // Auto-slide cada 5 segundos
    let autoSlideInterval;
    
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            if (!isAnimating) {
                moveSlide('right');
            }
        }, 5000);
    }

    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
        }
    }

    // Pausar auto-slide cuando el usuario interactúa
    slider.addEventListener('mouseenter', stopAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);
    
    leftArrow.addEventListener('click', () => {
        stopAutoSlide();
        setTimeout(startAutoSlide, 3000); // Reanudar después de 3 segundos
    });
    
    rightArrow.addEventListener('click', () => {
        stopAutoSlide();
        setTimeout(startAutoSlide, 3000);
    });

    // Inicializar
    const { resetMargin } = getSliderValues();
    resetSlidePosition(resetMargin);
    startAutoSlide();

    // Reajustar en cambio de ventana
    window.addEventListener('resize', () => {
        const { resetMargin } = getSliderValues();
        resetSlidePosition(resetMargin);
    });

})();

        // FORM FUNCTIONALITY
        (function() {
            const form = document.getElementById('contact_form');
            const formMsg = document.getElementById('form_msg');
            const inputs = document.querySelectorAll('.form_input');
            const labels = document.querySelectorAll('.form_label');
            
            // Handle input labels
            inputs.forEach((input, index) => {
                const label = labels[index];
                if (!label) return;
                
                function updateLabel() {
                    if (input.value.length > 0 || input === document.activeElement) {
                        label.classList.add('active');
                    } else {
                        label.classList.remove('active');
                    }
                }
                
                input.addEventListener('input', updateLabel);
                input.addEventListener('focus', updateLabel);
                input.addEventListener('blur', updateLabel);
                
                // Initial check
                updateLabel();
            });
            
            // Form validation
            function validateField(field, value) {
                switch(field) {
                    case 'name':
                        return value.trim().length >= 2;
                    case 'number':
                        return /^[\d\s\+\-\(\)]{7,}$/.test(value.trim());
                    case 'message':
                        return value.trim().length >= 10;
                    default:
                        return false;
                }
            }
            
            function showMessage(message, type) {
                formMsg.textContent = message;
                formMsg.className = `form_msg active ${type}`;
                
                if (type === 'success') {
                    setTimeout(() => {
                        formMsg.classList.remove('active');
                        form.reset();
                        labels.forEach(label => label.classList.remove('active'));
                    }, 3000);
                }
            }
            
            // Real-time validation
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    if (input.name) {
                        const isValid = validateField(input.name, input.value);
                        input.style.borderColor = isValid ? 'var(--color_green)' : 'var(--color_orange)';
                    }
                });
            });
            
            // Form submission
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const submitBtn = form.querySelector('.form_submit');
                const formData = new FormData(form);
                
                // Get form values
                const name = formData.get('name')?.trim();
                const number = formData.get('number')?.trim();
                const message = formData.get('message')?.trim();
                
                // Validate fields
                if (!validateField('name', name) || !validateField('number', number) || !validateField('message', message)) {
                    showMessage('Por favor, complete todos los campos correctamente', 'error');
                    return;
                }
                
                // Disable button
                submitBtn.disabled = true;
                submitBtn.textContent = 'Enviando...';
                
                try {
                    // Simulate form submission (replace with actual endpoint)
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    // Success message
                    showMessage('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success');
                    
                } catch (error) {
                    console.error('Error:', error);
                    showMessage('Error de conexión. Verifique su internet o contáctenos por WhatsApp.', 'error');
                } finally {
                    // Re-enable button
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Contactar';
                }
            });
        })();

        // SMOOTH SCROLL FOR ANCHOR LINKS
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const headerHeight = 125; // Account for fixed header
                    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // INTERSECTION OBSERVER FOR ANIMATIONS
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.product, .article_about_us, .testimonial').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });

        // LOADING ANIMATION
        window.addEventListener('load', () => {
            document.body.style.opacity = '1';
            document.body.style.transition = 'opacity 0.3s ease';
        });

        // Initialize page
        document.body.style.opacity = '0';
