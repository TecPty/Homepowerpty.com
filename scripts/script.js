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
        // Eliminado aquí para evitar conflictos con scripts/clients_slider.js
        // Mantener una sola implementación del carrusel (la clase ClientsSlider)

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
        // Eliminado aquí para evitar duplicar el comportamiento.
        // La lógica de scroll suave vive en scripts/header.js y calcula correctamente el offset del header.

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

        // CLIENT LOGO ENTRANCE ANIMATIONS
        const clientLogos = document.querySelectorAll('.client_logo');
        if (clientLogos.length) {
            const logoObserver = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;

                    const logo = entry.target;
                    const duration = parseFloat(logo.dataset.duration) || 1;
                    const delay = parseFloat(logo.dataset.delay) || 0;

                    logo.style.setProperty('--client-animation-duration', `${duration}s`);
                    logo.style.setProperty('--client-animation-delay', `${delay}s`);
                    logo.classList.add('is-visible');
                    obs.unobserve(logo);
                });
            }, { threshold: 0.35 });

            clientLogos.forEach(logo => {
                logo.style.setProperty('--client-animation-duration', `${logo.dataset.duration || 1}s`);
                logo.style.setProperty('--client-animation-delay', `${logo.dataset.delay || 0}s`);
                logoObserver.observe(logo);
            });
        }

        // LOADING ANIMATION
        window.addEventListener('load', () => {
            document.body.style.opacity = '1';
            document.body.style.transition = 'opacity 0.3s ease';
        });

        // Initialize page
        document.body.style.opacity = '0';
document.addEventListener('DOMContentLoaded', function() {
    const menuBurger = document.getElementById('menuBurger');
    const menuClose = document.getElementById('menuClose');
    const fullscreenMenu = document.getElementById('fullscreenMenu');
    const menuLinks = document.querySelectorAll('.fullscreen-menu-link');
    const body = document.body;
    
    // Abrir menú
    if (menuBurger) {
        menuBurger.addEventListener('click', function() {
            fullscreenMenu.classList.add('active');
            body.classList.add('menu-open');
        });
    }
    
    // Cerrar menú con el botón X
    if (menuClose) {
        menuClose.addEventListener('click', function() {
            closeMenu();
        });
    }
    
    // Cerrar menú al hacer click en un enlace
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMenu();
        });
    });
    
    // Cerrar menú con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && fullscreenMenu.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Función para cerrar el menú
    function closeMenu() {
        fullscreenMenu.classList.remove('active');
        body.classList.remove('menu-open');
    }
});
