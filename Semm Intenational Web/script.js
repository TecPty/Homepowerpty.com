// Services Data
const servicesData = [
    {
        id: 'construccion-general',
        title: 'Construcción General',
        description: 'Servicios completos de construcción para proyectos residenciales, comerciales e industriales con los más altos estándares de calidad.',
        icon: 'fas fa-hard-hat',
        category: 'construccion',
        features: [
            'Construcción de edificios residenciales',
            'Proyectos comerciales e industriales',
            'Remodelaciones y ampliaciones',
            'Supervisión técnica especializada',
            'Certificaciones de calidad'
        ]
    },
    {
        id: 'instalaciones-electricas',
        title: 'Instalaciones Eléctricas',
        description: 'Instalaciones eléctricas completas, mantenimiento y reparaciones con los más altos estándares de seguridad.',
        icon: 'fas fa-bolt',
        category: 'electricidad',
        features: [
            'Instalaciones eléctricas residenciales y comerciales',
            'Tableros eléctricos y automatización',
            'Iluminación LED eficiente',
            'Sistemas de respaldo eléctrico',
            'Certificaciones de seguridad'
        ]
    },
    {
        id: 'refrigeracion',
        title: 'Refrigeración y Aire Acondicionado',
        description: 'Instalación, mantenimiento y reparación de sistemas de refrigeración y climatización para espacios residenciales, comerciales e industriales.',
        icon: 'fas fa-snowflake',
        category: 'electricidad',
        features: [
            'Instalación de equipos centrales y splits',
            'Mantenimiento preventivo y correctivo',
            'Carga de gases refrigerantes',
            'Limpieza de ductos y filtros',
            'Sistemas de refrigeración industrial'
        ]
    },
    {
        id: 'paneles-solares',
        title: 'Paneles Solares',
        description: 'Soluciones de energía renovable con instalación de sistemas fotovoltaicos para reducir costos energéticos.',
        icon: 'fas fa-solar-panel',
        category: 'energia',
        features: [
            'Diseño y cálculo de sistemas solares',
            'Instalación de paneles fotovoltaicos',
            'Conexión a red eléctrica',
            'Monitoreo de producción energética',
            'Mantenimiento de sistemas solares'
        ]
    },
    {
        id: 'limpieza',
        title: 'Limpieza Profesional',
        description: 'Servicios de limpieza especializada para mantener espacios impecables con productos y técnicas profesionales.',
        icon: 'fas fa-broom',
        category: 'limpieza',
        features: [
            'Limpieza profunda de oficinas y comercios',
            'Limpieza de cristales y fachadas',
            'Limpieza de alfombras y tapicería',
            'Servicios post-construcción',
            'Mantenimiento regular programado'
        ]
    },
    {
        id: 'desinfeccion',
        title: 'Desinfección Sanitaria',
        description: 'Procesos de desinfección especializada para garantizar ambientes seguros y libres de patógenos.',
        icon: 'fas fa-shield-virus',
        category: 'limpieza',
        features: [
            'Desinfección con productos certificados',
            'Nebulización y atomización',
            'Protocolos sanitarios especializados',
            'Desinfección de aires acondicionados',
            'Certificaciones de salubridad'
        ]
    },
    {
        id: 'control-plagas',
        title: 'Control de Plagas',
        description: 'Eliminación y prevención de plagas con métodos seguros y efectivos para proteger su salud y propiedad.',
        icon: 'fas fa-bug',
        category: 'limpieza',
        features: [
            'Fumigación residencial y comercial',
            'Control de roedores',
            'Eliminación de insectos',
            'Tratamientos preventivos',
            'Seguimiento y garantía'
        ]
    }
];

// Gallery Data
const galleryData = [
    {
        id: '1',
        title: 'Edificio Residencial - Torre Azul',
        category: 'construccion',
        image: 'https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=800',
        description: 'Construcción completa de edificio residencial de 15 pisos con acabados de lujo.',
        location: 'Ciudad de Panamá'
    },
    {
        id: '2',
        title: 'Sistema Eléctrico Industrial',
        category: 'electricidad',
        image: 'https://images.pexels.com/photos/257736/pexels-photo-257736.jpeg?auto=compress&cs=tinysrgb&w=800',
        description: 'Instalación eléctrica completa para planta industrial con sistemas automatizados.',
        location: 'David, Chiriquí'
    },
    {
        id: '3',
        title: 'Sistema Central de A/C - Hotel',
        category: 'refrigeracion',
        image: 'https://images.pexels.com/photos/2724748/pexels-photo-2724748.jpeg?auto=compress&cs=tinysrgb&w=800',
        description: 'Instalación completa de sistema de aire acondicionado central para hotel de 150 habitaciones.',
        location: 'Ciudad de Panamá'
    },
    {
        id: '4',
        title: 'Instalación Solar Comercial',
        category: 'solar',
        image: 'https://images.pexels.com/photos/9875441/pexels-photo-9875441.jpeg?auto=compress&cs=tinysrgb&w=800',
        description: 'Sistema fotovoltaico de 100kW para centro comercial, reducción del 70% en costos eléctricos.',
        location: 'San José, Costa Rica'
    },
    {
        id: '5',
        title: 'Centro Comercial Plaza Norte',
        category: 'construccion',
        image: 'https://images.pexels.com/photos/2467558/pexels-photo-2467558.jpeg?auto=compress&cs=tinysrgb&w=800',
        description: 'Construcción de centro comercial con 50 locales comerciales y estacionamiento subterráneo.',
        location: 'David, Chiriquí'
    },
    {
        id: '6',
        title: 'Instalación Eléctrica Residencial',
        category: 'electricidad',
        image: 'https://images.pexels.com/photos/8092/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=800',
        description: 'Cableado eléctrico completo y sistemas domóticos para residencia de lujo.',
        location: 'San José, Costa Rica'
    }
];

// Testimonials Data
const testimonialsData = [
    {
        id: '1',
        name: 'Carlos Mendoza',
        company: 'Hotel Real Panamá',
        message: 'SEMM International transformó nuestro sistema de climatización. Su profesionalismo y calidad técnica son excepcionales. El ahorro energético ha sido del 40%.',
        location: 'Ciudad de Panamá',
        rating: 5
    },
    {
        id: '2',
        name: 'María González',
        company: 'Centro Médico San Rafael',
        message: 'Los protocolos de desinfección implementados por SEMM han sido fundamentales para mantener nuestras instalaciones seguras. Trabajo impecable y puntual.',
        location: 'David, Chiriquí',
        rating: 5
    },
    {
        id: '3',
        name: 'Roberto Silva',
        company: 'Industrias Alimentarias CR',
        message: 'El sistema de paneles solares instalado por SEMM ha reducido nuestros costos eléctricos significativamente. La inversión se ha recuperado en tiempo récord.',
        location: 'San José, Costa Rica',
        rating: 5
    },
    {
        id: '4',
        name: 'Ana Patricia López',
        company: 'Complejo Residencial Vista Hermosa',
        message: 'Servicios de construcción y mantenimiento excepcionales. El equipo es muy profesional y los resultados superaron nuestras expectativas.',
        location: 'Chiriquí, Panamá',
        rating: 5
    }
];

// DOM Elements
const menuToggle = document.getElementById('menuToggle');
const nav = document.getElementById('nav');
const header = document.getElementById('header');
const servicesGrid = document.getElementById('servicesGrid');
const galleryGrid = document.getElementById('galleryGrid');
const testimonialsGrid = document.getElementById('testimonialsGrid');
const contactForm = document.getElementById('contactForm');

// Mobile Menu Toggle
menuToggle.addEventListener('click', () => {
    nav.classList.toggle('active');
});

// Header Scroll Effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    }
});

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            // Close mobile menu if open
            nav.classList.remove('active');
        }
    });
});

// Services Filter Functionality
function renderServices(filter = 'todos') {
    const filteredServices = filter === 'todos' 
        ? servicesData 
        : servicesData.filter(service => service.category === filter);

    servicesGrid.innerHTML = filteredServices.map(service => `
        <div class="service-card" data-category="${service.category}">
            <div class="service-header">
                <div class="service-icon">
                    <i class="${service.icon}"></i>
                </div>
                <span class="service-category">${getCategoryLabel(service.category)}</span>
            </div>
            <h3>${service.title}</h3>
            <p>${service.description}</p>
            <ul class="service-features">
                ${service.features.slice(0, 3).map(feature => `
                    <li><i class="fas fa-arrow-right"></i> ${feature}</li>
                `).join('')}
                ${service.features.length > 3 ? `<li style="color: var(--primary-blue); font-weight: 600;">+${service.features.length - 3} servicios más...</li>` : ''}
            </ul>
            <a href="#contacto" class="btn btn-primary">Solicitar Información</a>
        </div>
    `).join('');
}

function getCategoryLabel(category) {
    const labels = {
        'construccion': 'Construcción',
        'electricidad': 'Electricidad',
        'limpieza': 'Limpieza',
        'energia': 'Energía'
    };
    return labels[category] || category;
}

// Services Filter Event Listeners
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Filter services
        const filter = btn.getAttribute('data-filter');
        renderServices(filter);
    });
});

// Gallery Filter Functionality
function renderGallery(filter = 'todos') {
    const filteredGallery = filter === 'todos' 
        ? galleryData 
        : galleryData.filter(item => item.category === filter);

    galleryGrid.innerHTML = filteredGallery.map(item => `
        <div class="gallery-item" data-category="${item.category}">
            <img src="${item.image}" alt="${item.title}">
            <div class="gallery-overlay">
                <span class="gallery-category">${getCategoryLabel(item.category)}</span>
                <h3>${item.title}</h3>
                <p><i class="fas fa-map-marker-alt"></i> ${item.location}</p>
                <p>${item.description}</p>
            </div>
        </div>
    `).join('');
}

// Gallery Filter Event Listeners
document.querySelectorAll('.gallery-filter').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.gallery-filter').forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Filter gallery
        const filter = btn.getAttribute('data-filter');
        renderGallery(filter);
    });
});

// Testimonials Rendering
function renderTestimonials() {
    testimonialsGrid.innerHTML = testimonialsData.map(testimonial => `
        <div class="testimonial-card">
            <div class="testimonial-rating">
                ${Array(testimonial.rating).fill('<i class="fas fa-star"></i>').join('')}
            </div>
            <p class="testimonial-message">${testimonial.message}</p>
            <div class="testimonial-author">
                <div class="testimonial-name">${testimonial.name}</div>
                <div class="testimonial-company">${testimonial.company}</div>
                <div class="testimonial-location"><i class="fas fa-map-marker-alt"></i> ${testimonial.location}</div>
            </div>
        </div>
    `).join('');
}

// Contact Form Handling
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    // Here you would typically send the data to your server
    console.log('Form submitted:', data);
    
    // Show success message
    alert('¡Gracias por contactarnos! Nos comunicaremos con usted pronto.');
    
    // Reset form
    this.reset();
});

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Add animation classes and observe elements
function initAnimations() {
    const animatedElements = document.querySelectorAll('.service-card, .gallery-item, .testimonial-card, .contact-card');
    animatedElements.forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    renderServices();
    renderGallery();
    renderTestimonials();
    initAnimations();
    
    // Añadir control de reproducción del video
    const video = document.getElementById('myVideo');
    
    // Asegurar que el video se reproduzca
    video.play().catch(function(error) {
        console.log("Video autoplay failed:", error);
    });
    
    // Optimizar rendimiento pausando el video cuando no es visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.play();
            } else {
                video.pause();
            }
        });
    }, { threshold: 0.5 });
    
    observer.observe(video);
});

// Agregar lazy loading para el video
const video = document.createElement('video');
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');
video.setAttribute('loop', '');
video.setAttribute('playsinline', '');
video.setAttribute('loading', 'lazy');

// Cargar el video cuando sea necesario
const loadVideo = () => {
    const source = document.createElement('source');
    source.src = './assets/media/service-1.mp4';
    source.type = 'video/mp4';
    video.appendChild(source);
};

// Usar Intersection Observer para cargar el video
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            loadVideo();
            observer.unobserve(entry.target);
        }
    });
});

observer.observe(document.querySelector('.video-banner'));

// Add scroll-to-top functionality
window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Show/hide scroll to top button (if you want to add one)
    if (scrollTop > 300) {
        // Show button
    } else {
        // Hide button
    }
});

// WhatsApp Integration
function openWhatsApp(message = '') {
    const phone = '50764732642';
    const defaultMessage = 'Hola, me interesa conocer más sobre los servicios de SEMM International.';
    const finalMessage = message || defaultMessage;
    const url = `https://wa.me/${phone}?text=${encodeURIComponent(finalMessage)}`;
    window.open(url, '_blank');
}

// Add WhatsApp click handlers
document.querySelectorAll('a[href*="wa.me"]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        openWhatsApp();
    });
});

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#dee2e6';
        }
    });
    
    return isValid;
}

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Phone validation
function validatePhone(phone) {
    const re = /^[\+]?[0-9\s\-\(\)]{8,}$/;
    return re.test(phone);
}

// Enhanced form submission
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!validateForm(this)) {
        alert('Por favor, complete todos los campos requeridos.');
        return;
    }
    
    const email = this.querySelector('#email').value;
    const phone = this.querySelector('#phone').value;
    
    if (!validateEmail(email)) {
        alert('Por favor, ingrese un correo electrónico válido.');
        return;
    }
    
    if (!validatePhone(phone)) {
        alert('Por favor, ingrese un número de teléfono válido.');
        return;
    }
    
    // Simulate form submission
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('¡Gracias por contactarnos! Nos comunicaremos con usted pronto.');
        this.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 2000);
});

// Lazy loading for images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Schema Markup
const schemaMarkup = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "SEMM International",
    "description": "Servicios profesionales de construcción y electricidad",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Ciudad de Panamá",
        "addressCountry": "PA"
    },
    "telephone": "(507) 6473-2642",
    "email": "infosemminternational@gmail.com",
    "url": "https://semminternational.com"
};

// Inject Schema Markup into the document
document.addEventListener('DOMContentLoaded', () => {
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(schemaMarkup);
    document.head.appendChild(script);
});