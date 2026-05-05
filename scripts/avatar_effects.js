// Avatar Effects Script
(function() {
    'use strict';

    // Esperar que el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        
        // Seleccionar todos los avatares
        const avatars = document.querySelectorAll('.testimonial_avatar');
        
        // Agregar efectos de interacción
        avatars.forEach((avatar, index) => {
            
            // Efecto de entrada escalonado
            setTimeout(() => {
                avatar.style.opacity = '0';
                avatar.style.transform = 'scale(0.8) translateY(20px)';
                avatar.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                
                requestAnimationFrame(() => {
                    avatar.style.opacity = '1';
                    avatar.style.transform = 'scale(1) translateY(0)';
                });
            }, index * 150);
            
            // Efecto hover mejorado
            avatar.addEventListener('mouseenter', function() {
                this.classList.add('pulse');
                
                // Agregar efecto de rotación suave al hover
                const img = this.querySelector('.avatar_img');
                if (img) {
                    img.style.transform = 'scale(1.05) rotate(2deg)';
                }
            });
            
            avatar.addEventListener('mouseleave', function() {
                this.classList.remove('pulse');
                
                // Restaurar transformación
                const img = this.querySelector('.avatar_img');
                if (img) {
                    img.style.transform = 'scale(1) rotate(0deg)';
                }
            });
            
            // Efecto de click/toque
            avatar.addEventListener('click', function() {
                // Crear efecto de ripple
                createRippleEffect(this);
                
                // Agregar clase temporal para efecto visual
                this.classList.add('clicked');
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 300);
            });
        });
        
        // Función para crear efecto ripple
        function createRippleEffect(element) {
            const ripple = document.createElement('div');
            ripple.className = 'ripple-effect';
            
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = (rect.width / 2 - size / 2) + 'px';
            ripple.style.top = (rect.height / 2 - size / 2) + 'px';
            
            element.style.position = 'relative';
            element.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
        
        // Observador de intersección para animaciones de scroll
        const observerOptions = {
            threshold: 0.3,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const avatar = entry.target;
                    avatar.classList.add('animate-in');
                    
                    // Agregar efecto de pulso aleatorio ocasional
                    setInterval(() => {
                        if (Math.random() < 0.1) { // 10% de probabilidad
                            avatar.classList.add('pulse');
                            setTimeout(() => {
                                avatar.classList.remove('pulse');
                            }, 2000);
                        }
                    }, 5000);
                }
            });
        }, observerOptions);
        
        // Observar todos los avatares
        avatars.forEach(avatar => {
            observer.observe(avatar);
        });
    });
})();