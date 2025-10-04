(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        popupDelay: 3000, // Mostrar después de 3 segundos (era 500ms)
        scrollThreshold: 30, // Mostrar después de 30% de scroll
        countdownEndDate: new Date('2024-12-06T23:59:59').getTime(),
        storageKeys: {
            dismissed: 'blackWeek2024Dismissed',
            lastShown: 'blackWeek2024LastShown'
        }
    };
    
    // DOM Elements
    const popup = document.getElementById('blackWeekPopup');
    const closeBtn = document.getElementById('closePopup');
    
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
    
    // No mostrar si se cerró permanentemente
    if (dismissed && dismissed.value === true) {
        return false;
    }
    
    // No mostrar si el countdown ha terminado
    if (now > CONFIG.countdownEndDate) {
        return false;
    }
    
    // Respetar "remind later" - no mostrar si fue cerrado recientemente
    if (dismissed && dismissed.timestamp) {
        const hoursSinceDismissed = (now - dismissed.timestamp) / (1000 * 60 * 60);
        if (hoursSinceDismissed < 24) { // No mostrar por 24 horas si se cerró
            return false;
        }
    }
    
    return true;
}
    
    function showPopup() {
        if (popup) {
            popup.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Registrar que se mostró
            setLocalStorageItem(CONFIG.storageKeys.lastShown, Date.now());
            
            // Analytics
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
        
        // Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'popup_dismissed', {
                event_category: 'promotion',
                event_label: 'black_week_2024',
                value: permanent ? 'permanent' : 'temporary'
            });
        }
    }
    
    // Detectar scroll para mostrar popup
    let hasScrolled = false;
    function checkScroll() {
        if (hasScrolled) return;
        
        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        
        if (scrollPercent > CONFIG.scrollThreshold) {
            hasScrolled = true;
            if (shouldShowPopup()) {
                showPopup();
            }
        }
    }
    
    // Event Listeners
    function setupEventListeners() {
        // Close button
        if (closeBtn) {
            closeBtn.addEventListener('click', () => dismissPopup(false));
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
        
        // Listener de scroll
        window.addEventListener('scroll', checkScroll, { passive: true });
        
        // Mostrar al hacer clic en "Inicio" (después de scroll)
        const inicioLinks = document.querySelectorAll('a[href="#inicio"]');
        inicioLinks.forEach(link => {
            link.addEventListener('click', () => {
                setTimeout(() => {
                    if (shouldShowPopup()) {
                        showPopup();
                    }
                }, 500);
            });
        });
    }
    
    // Initialize
    function init() {
        if (!popup) {
            console.warn('Black Week popup element not found');
            return;
        }
        
        setupEventListeners();
        
        // Mostrar después del delay SOLO si debe mostrarse
        if (shouldShowPopup()) {
            setTimeout(() => {
                // Verificar nuevamente por si el usuario scrolleó rápido
                if (!hasScrolled) {
                    showPopup();
                }
            }, CONFIG.popupDelay);
        }
        
        // Clean up
        window.addEventListener('beforeunload', () => {
            window.removeEventListener('scroll', checkScroll);
        });
    }
    
    // Wait for DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose API for debugging
    window.BlackWeekPopup = {
        show: showPopup,
        hide: hidePopup,
        dismiss: dismissPopup,
        forceShow: () => {
            console.log('Forcing Black Week popup to show');
            showPopup();
        },
        resetStorage: () => {
            localStorage.removeItem(CONFIG.storageKeys.dismissed);
            localStorage.removeItem(CONFIG.storageKeys.lastShown);
            console.log('Black Week popup storage cleared');
        }
    };
})();