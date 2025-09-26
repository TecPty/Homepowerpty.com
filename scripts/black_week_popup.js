// ===== BLACK WEEK POPUP FUNCTIONALITY =====
(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        popupDelay: 500, // Show popup after 0.5 seconds (much faster)
        remindDelay: 24 * 60 * 60 * 1000, // Remind after 24 hours
        countdownEndDate: new Date('2024-12-06T23:59:59').getTime(), // Black Week end date
        storageKeys: {
            dismissed: 'blackWeek2024Dismissed',
            remindLater: 'blackWeek2024RemindLater'
        }
    };
    
    // DOM Elements
    const popup = document.getElementById('blackWeekPopup');
    const closeBtn = document.getElementById('closePopup');
    const remindBtn = document.getElementById('remindLater');
    const primaryCTA = document.querySelector('.popup-cta-primary');
    
    // Countdown elements
    const daysEl = document.getElementById('days');
    const hoursEl = document.getElementById('hours');
    const minutesEl = document.getElementById('minutes');
    
    // Carousel elements
    const bannersContainer = document.getElementById('bannersContainer');
    const prevBtn = document.getElementById('prevBanner');
    const nextBtn = document.getElementById('nextBanner');
    const indicatorsContainer = document.getElementById('carouselIndicators');
    
    // Carousel state
    let currentSlide = 0;
    let autoSlideInterval = null;
    const bannerSlides = [];
    
    // Utility Functions
    function setLocalStorageItem(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify({
                value: value,
                timestamp: Date.now()
            }));
        } catch (error) {
            console.warn('LocalStorage not available:', error);
        }
    }
    
    function getLocalStorageItem(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.warn('Error reading from localStorage:', error);
            return null;
        }
    }
    
    function shouldShowPopup() {
        const dismissed = getLocalStorageItem(CONFIG.storageKeys.dismissed);
        const now = Date.now();
        
        // Only don't show if permanently dismissed (but still show for "remind later")
        if (dismissed && dismissed.value === true) {
            return false;
        }
        
        // ALWAYS SHOW for Black Week promotion - ignore "remind later"
        // This ensures maximum visibility for the promotional campaign
        
        // Don't show if countdown has ended
        if (now > CONFIG.countdownEndDate) {
            return false;
        }
        
        return true;
    }
    
    function showPopup() {
        if (popup) {
            popup.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Analytics event (if you have analytics)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'popup_shown', {
                    event_category: 'promotion',
                    event_label: 'black_week_2024'
                });
            }
        }
    }
    
    function hidePopup() {
        if (popup) {
            popup.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    function dismissPopup(permanent = false) {
        hidePopup();
        
        if (permanent) {
            setLocalStorageItem(CONFIG.storageKeys.dismissed, true);
        }
        
        // Analytics event
        if (typeof gtag !== 'undefined') {
            gtag('event', 'popup_dismissed', {
                event_category: 'promotion',
                event_label: 'black_week_2024',
                value: permanent ? 'permanent' : 'temporary'
            });
        }
    }
    
    function remindLater() {
        setLocalStorageItem(CONFIG.storageKeys.remindLater, true);
        dismissPopup(false);
        
        // Show confirmation message
        showMessage('Te recordaremos mañana sobre esta increíble oferta! 🔔', 'success');
    }
    
    // Carousel Functions
    function initCarousel() {
        console.log('Initializing carousel...');
        const slides = bannersContainer ? bannersContainer.querySelectorAll('.banner-slide') : [];
        console.log('Found slides:', slides.length);
        
        if (slides.length === 0) {
            console.warn('No banner slides found');
            return;
        }
        
        // Store slides for reference
        slides.forEach((slide, index) => {
            bannerSlides.push(slide);
            console.log(`Added slide ${index}:`, slide);
        });
        
        // Create indicators
        createIndicators();
        
        // Start auto-slide
        startAutoSlide();
        
        console.log('Carousel initialized successfully');
    }
    
    function createIndicators() {
        console.log('Creating indicators...');
        if (!indicatorsContainer || bannerSlides.length === 0) {
            console.warn('No indicators container found or no slides available');
            return;
        }
        
        // Clear existing indicators
        indicatorsContainer.innerHTML = '';
        
        bannerSlides.forEach((_, index) => {
            const indicator = document.createElement('div');
            indicator.className = index === 0 ? 'indicator active' : 'indicator';
            indicator.addEventListener('click', () => goToSlide(index));
            indicatorsContainer.appendChild(indicator);
            console.log(`Created indicator ${index}`);
        });
        
        console.log(`Created ${bannerSlides.length} indicators`);
    }
    
    function goToSlide(slideIndex) {
        if (!bannersContainer || bannerSlides.length === 0) return;
        
        // Remove active class from current slide
        bannerSlides[currentSlide].classList.remove('active');
        
        // Add prev class for animation
        if (slideIndex > currentSlide) {
            bannerSlides[currentSlide].classList.add('prev');
        }
        
        // Update current slide
        currentSlide = slideIndex;
        
        // Add active class to new slide
        bannerSlides[currentSlide].classList.add('active');
        
        // Update indicators
        updateIndicators();
        
        // Clean up classes after animation
        setTimeout(() => {
            bannerSlides.forEach(slide => {
                slide.classList.remove('prev');
            });
        }, 500);
        
        // Reset auto-slide
        resetAutoSlide();
    }
    
    function nextSlide() {
        const nextIndex = (currentSlide + 1) % bannerSlides.length;
        goToSlide(nextIndex);
    }
    
    function prevSlide() {
        const prevIndex = currentSlide === 0 ? bannerSlides.length - 1 : currentSlide - 1;
        goToSlide(prevIndex);
    }
    
    function updateIndicators() {
        if (!indicatorsContainer) return;
        
        const indicators = indicatorsContainer.querySelectorAll('.indicator');
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentSlide);
        });
    }
    
    function startAutoSlide() {
        if (bannerSlides.length <= 1) return;
        
        autoSlideInterval = setInterval(() => {
            nextSlide();
        }, 4000); // Change slide every 4 seconds
    }
    
    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
            autoSlideInterval = null;
        }
    }
    
    function resetAutoSlide() {
        stopAutoSlide();
        startAutoSlide();
    }
    
    function updateCountdown() {
        const now = new Date().getTime();
        const distance = CONFIG.countdownEndDate - now;
        
        if (distance < 0) {
            // Countdown finished
            if (daysEl) daysEl.textContent = '00';
            if (hoursEl) hoursEl.textContent = '00';
            if (minutesEl) minutesEl.textContent = '00';
            
            // Hide popup if countdown is over
            setTimeout(() => {
                dismissPopup(true);
            }, 5000);
            return;
        }
        
        // Calculate time units
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        
        // Update DOM
        if (daysEl) daysEl.textContent = days.toString().padStart(2, '0');
        if (hoursEl) hoursEl.textContent = hours.toString().padStart(2, '0');
        if (minutesEl) minutesEl.textContent = minutes.toString().padStart(2, '0');
    }
    
    function showMessage(message, type = 'info') {
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.className = `popup-message popup-message-${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4CAF50' : '#2196F3'};
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            z-index: 10000;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(messageEl);
        
        // Animate in
        setTimeout(() => {
            messageEl.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            messageEl.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(messageEl);
            }, 300);
        }, 3000);
    }
    
    function trackCTAClick() {
        // Analytics event
        if (typeof gtag !== 'undefined') {
            gtag('event', 'cta_clicked', {
                event_category: 'promotion',
                event_label: 'black_week_2024_whatsapp'
            });
        }
        
        // Dismiss popup after CTA click
        setTimeout(() => {
            dismissPopup(true);
        }, 1000);
    }
    
    // Event Listeners
    function setupEventListeners() {
        // Close button
        if (closeBtn) {
            closeBtn.addEventListener('click', () => dismissPopup(false));
        }
        
        // Remind later button
        if (remindBtn) {
            remindBtn.addEventListener('click', remindLater);
        }
        
        // Primary CTA tracking
        if (primaryCTA) {
            primaryCTA.addEventListener('click', trackCTAClick);
        }
        
        // Carousel controls
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                prevSlide();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                nextSlide();
            });
        }
        
        // Pause auto-slide on hover
        if (bannersContainer) {
            bannersContainer.addEventListener('mouseenter', stopAutoSlide);
            bannersContainer.addEventListener('mouseleave', startAutoSlide);
        }
        
        // Show popup on "Inicio" button clicks
        const inicioLinks = document.querySelectorAll('a[href="#inicio"]');
        inicioLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                // Small delay to let the scroll animation finish
                setTimeout(() => {
                    if (shouldShowPopup()) {
                        showPopup();
                    } else {
                        // Even if dismissed permanently, show once when clicking Inicio during Black Week
                        console.log('Showing Black Week popup on Inicio click');
                        showPopup();
                    }
                }, 500);
            });
        });
        
        // Also trigger on logo click (goes to inicio)
        const logoLinks = document.querySelectorAll('.logo_icon, .footer_logo');
        logoLinks.forEach(logo => {
            logo.addEventListener('click', (e) => {
                setTimeout(() => {
                    console.log('Showing Black Week popup on logo click');
                    showPopup();
                }, 500);
            });
        });
        
        // Close on overlay click
        if (popup) {
            popup.addEventListener('click', (e) => {
                if (e.target.classList.contains('popup-overlay')) {
                    dismissPopup(false);
                }
            });
        }
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && popup && popup.classList.contains('active')) {
                dismissPopup(false);
            }
        });
    }
    
    // Initialize
    function init() {
        if (!popup) {
            console.warn('Black Week popup element not found');
            return;
        }
        
        setupEventListeners();
        
        // Initialize carousel
        initCarousel();
        
        // Start countdown
        updateCountdown();
        const countdownInterval = setInterval(updateCountdown, 60000); // Update every minute
        
        // ALWAYS show popup immediately on page load during Black Week campaign
        console.log('Black Week campaign active - showing popup immediately');
        setTimeout(showPopup, CONFIG.popupDelay);
        
        // Also show if normal conditions are met (backup)
        if (shouldShowPopup()) {
            setTimeout(showPopup, CONFIG.popupDelay + 1000);
        }
        
        // Clean up interval when page unloads
        window.addEventListener('beforeunload', () => {
            clearInterval(countdownInterval);
            stopAutoSlide();
        });
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose some functions globally for debugging (optional)
    window.BlackWeekPopup = {
        show: showPopup,
        hide: hidePopup,
        dismiss: dismissPopup,
        nextSlide: nextSlide,
        prevSlide: prevSlide,
        goToSlide: goToSlide,
        currentSlide: () => currentSlide,
        slideCount: () => bannerSlides.length,
        forceShow: () => {
            console.log('Forcing Black Week popup to show');
            showPopup();
        },
        resetStorage: () => {
            localStorage.removeItem(CONFIG.storageKeys.dismissed);
            localStorage.removeItem(CONFIG.storageKeys.remindLater);
            console.log('Black Week popup storage cleared');
        }
    };
})();