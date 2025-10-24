import React, { useState, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';

const WhatsAppButton: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility);
    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  useEffect(() => {
    // Show tooltip after 3 seconds if user hasn't interacted
    const timer = setTimeout(() => {
      setShowTooltip(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const handleWhatsAppClick = () => {
    const message = encodeURIComponent(
      'Hola! Me interesa conocer más información sobre los productos de HomePower. ¿Podrían ayudarme?'
    );
    const whatsappUrl = `https://wa.me/50761234567?text=${message}`;
    window.open(whatsappUrl, '_blank');
    setShowTooltip(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Tooltip */}
      {showTooltip && (
        <div className="absolute bottom-full right-0 mb-4 animate-pulse">
          <div className="bg-white rounded-lg shadow-xl p-4 max-w-xs relative">
            <button
              onClick={() => setShowTooltip(false)}
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
            >
              <X className="w-4 h-4" />
            </button>
            <p className="text-sm text-gray-800 pr-6">
              ¡Hola! ¿Necesitas ayuda con algún producto? Escríbenos por WhatsApp 👋
            </p>
            <div className="absolute -bottom-2 right-4 w-4 h-4 bg-white transform rotate-45 shadow-lg"></div>
          </div>
        </div>
      )}

      {/* WhatsApp Button */}
      <button
        onClick={handleWhatsAppClick}
        className="bg-[#4CAF50] hover:bg-[#4CAF50]/90 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110 animate-bounce"
        aria-label="Contactar por WhatsApp"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Pulse Animation */}
      <div className="absolute inset-0 bg-[#4CAF50] rounded-full animate-ping opacity-20"></div>
    </div>
  );
};

export default WhatsAppButton;