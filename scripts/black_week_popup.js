// ===== BLACK WEEK POPUP FUNCTIONALITY =====
(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        popupDelay: 3000, // Show popup after 3 seconds
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
        const remindLater = getLocalStorageItem(CONFIG.storageKeys.remindLater);
        const now = Date.now();
        
        // Don't show if permanently dismissed
        if (dismissed && dismissed.value === true) {
            return false;
        }
        
        // Don't show if "remind later" is still active
        if (remindLater && (now - remindLater.timestamp) < CONFIG.remindDelay) {
            return false;
        }
        
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
        
        // Start countdown
        updateCountdown();
        const countdownInterval = setInterval(updateCountdown, 60000); // Update every minute
        
        // Show popup if conditions are met
        if (shouldShowPopup()) {
            setTimeout(showPopup, CONFIG.popupDelay);
        }
        
        // Clean up interval when page unloads
        window.addEventListener('beforeunload', () => {
            clearInterval(countdownInterval);
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
        resetStorage: () => {
            localStorage.removeItem(CONFIG.storageKeys.dismissed);
            localStorage.removeItem(CONFIG.storageKeys.remindLater);
        }
    };
})();