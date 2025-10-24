import React, { useState, useEffect } from 'react';
import { Phone, Mail, MapPin, ChevronRight, Star, CheckCircle, Menu, X, MessageCircle } from 'lucide-react';
import Header from './components/Header';
import ProductCatalog from './components/ProductCatalog';
import AboutUs from './components/AboutUs';
import Clients from './components/Clients';
import ContactForm from './components/ContactForm';
import WhatsAppButton from './components/WhatsAppButton';

function App() {
  const [activeSection, setActiveSection] = useState('inicio');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const sections = ['inicio', 'electrodomesticos', 'nosotros', 'clientes', 'contacto'];
      const scrollPosition = window.scrollY + 100;

      sections.forEach(section => {
        const element = document.getElementById(section);
        if (element) {
          const offsetTop = element.offsetTop;
          const height = element.offsetHeight;
          
          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + height) {
            setActiveSection(section);
          }
        }
      });
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-[#F7F7F7]">
      <Header 
        activeSection={activeSection}
        onSectionClick={scrollToSection}
        isMenuOpen={isMenuOpen}
        setIsMenuOpen={setIsMenuOpen}
      />

      {/* Hero Section */}
      <section id="inicio" className="pt-20 pb-16 bg-gradient-to-br from-[#FF9F1C] to-[#FBD38D]">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
            <div className="text-center lg:text-left">
              <h1 className="text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                Potencia e <span className="text-[#000000]">Innovación</span>
              </h1>
              <p className="text-xl text-white/90 mb-8 leading-relaxed">
                Líder en distribución mayorista de electrodomésticos innovadores en Panamá. 
                Soluciones confiables y tecnológicamente avanzadas para tu hogar.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <button 
                  onClick={() => scrollToSection('contacto')}
                  className="bg-[#000000] text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-800 transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  Solicitar Cotización
                </button>
                <button 
                  onClick={() => scrollToSection('electrodomesticos')}
                  className="bg-white text-[#FF9F1C] px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-50 transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
                >
                  Ver Catálogo <ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">500+</div>
                    <div className="text-white/80">Productos</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">100+</div>
                    <div className="text-white/80">Clientes</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">24/7</div>
                    <div className="text-white/80">Soporte</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">5★</div>
                    <div className="text-white/80">Calificación</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6 rounded-xl bg-[#F7F7F7] hover:shadow-lg transition-all duration-300">
                <div className="w-16 h-16 bg-[#4CAF50] rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-[#000000] mb-3">Garantía Completa</h3>
                <p className="text-[#718096]">Todos nuestros productos incluyen garantía completa y soporte técnico especializado.</p>
              </div>
              <div className="text-center p-6 rounded-xl bg-[#F7F7F7] hover:shadow-lg transition-all duration-300">
                <div className="w-16 h-16 bg-[#FF9F1C] rounded-full flex items-center justify-center mx-auto mb-4">
                  <Star className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-[#000000] mb-3">Calidad Premium</h3>
                <p className="text-[#718096]">Seleccionamos solo las mejores marcas y productos con tecnología avanzada.</p>
              </div>
              <div className="text-center p-6 rounded-xl bg-[#F7F7F7] hover:shadow-lg transition-all duration-300">
                <div className="w-16 h-16 bg-[#ff4b4b] rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-[#000000] mb-3">Atención Personalizada</h3>
                <p className="text-[#718096]">Servicio dedicado y personalizado para cada cliente corporativo.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <ProductCatalog />
      <AboutUs />
      <Clients />
      <ContactForm />
      <WhatsAppButton />

      {/* Footer */}
      <footer className="bg-[#000000] text-white py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-[#FF9F1C] mb-4">HomePower</h3>
              <p className="text-gray-300 mb-4">Distribución mayorista de electrodomésticos innovadores en Panamá.</p>
              <div className="flex space-x-4">
                <a href="#" className="text-gray-300 hover:text-[#FF9F1C] transition-colors">Facebook</a>
                <a href="#" className="text-gray-300 hover:text-[#FF9F1C] transition-colors">Instagram</a>
                <a href="#" className="text-gray-300 hover:text-[#FF9F1C] transition-colors">TikTok</a>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Productos</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Planchas</a></li>
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Licuadoras</a></li>
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Air Fryers</a></li>
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Cafeteras</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Nosotros</a></li>
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Clientes</a></li>
                <li><a href="#" className="hover:text-[#FF9F1C] transition-colors">Contacto</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contacto</h4>
              <div className="space-y-2 text-gray-300">
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>+507 6123-4567</span>
                </div>
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>info@homepowerpty.com</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>Panamá, Panamá</span>
                </div>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 HomePowerPTY. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;