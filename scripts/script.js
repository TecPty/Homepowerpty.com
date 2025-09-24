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
            
            if (!slider || !leftArrow || !rightArrow) return;
            
            let isAnimating = false;
            
            function getSliderValues() {
                const windowWidth = window.innerWidth;
                return windowWidth > 768 
                    ? { moveDistance: 50, resetMargin: -25 }
                    : { moveDistance: 100, resetMargin: -50 };
            }
            
            async function moveSlide(direction) {
                if (isAnimating) return;
                isAnimating = true;
                
                const { moveDistance, resetMargin } = getSliderValues();
                const margin = direction === 'right' ? `-${moveDistance}` : '0';
                
                try {
                    // Animate slide
                    slider.style.transition = 'transform 300ms ease';
                    slider.style.transform = `translateX(${margin}%)`;
                    
                    // Wait for animation
                    await new Promise(resolve => setTimeout(resolve, 300));
                    
                    // Update slide order
                    if (direction === 'right') {
                        const first = slider.firstElementChild;
                        slider.appendChild(first);
                    } else {
                        const last = slider.lastElementChild;
                        slider.prepend(last);
                    }
                    
                    // Reset position
                    slider.style.transition = 'none';
                    slider.style.transform = `translateX(${resetMargin}%)`;
                    
                } catch (error) {
                    console.error('Error in slider animation:', error);
                } finally {
                    isAnimating = false;
                }
            }
            
            leftArrow.addEventListener('click', () => moveSlide('left'));
            rightArrow.addEventListener('click', () => moveSlide('right'));
            
            // Touch support for mobile
            let touchStartX = 0;
            let touchEndX = 0;
            
            slider.addEventListener('touchstart', e => {
                touchStartX = e.touches[0].clientX;
            }, { passive: true });
            
            slider.addEventListener('touchend', e => {
                touchEndX = e.changedTouches[0].clientX;
                const diff = touchStartX - touchEndX;
                const threshold = 50;
                
                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        moveSlide('right');
                    } else {
                        moveSlide('left');
                    }
                }
            }, { passive: true });
            
            // Initialize slider position
            const { resetMargin } = getSliderValues();
            slider.style.transform = `translateX(${resetMargin}%)`;
            
            // Handle resize
            window.addEventListener('resize', () => {
                const { resetMargin } = getSliderValues();
                slider.style.transition = 'none';
                slider.style.transform = `translateX(${resetMargin}%)`;
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
