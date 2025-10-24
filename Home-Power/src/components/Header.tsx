import React from 'react';
import { Menu, X, Phone, Mail } from 'lucide-react';

interface HeaderProps {
  activeSection: string;
  onSectionClick: (section: string) => void;
  isMenuOpen: boolean;
  setIsMenuOpen: (open: boolean) => void;
}

const Header: React.FC<HeaderProps> = ({ activeSection, onSectionClick, isMenuOpen, setIsMenuOpen }) => {
  const navItems = [
    { id: 'inicio', label: 'Inicio' },
    { id: 'electrodomesticos', label: 'Electrodomésticos' },
    { id: 'nosotros', label: 'Nosotros' },
    { id: 'clientes', label: 'Clientes' },
    { id: 'contacto', label: 'Contacto' }
  ];

  return (
    <header className="fixed top-0 w-full bg-white/95 backdrop-blur-sm shadow-lg z-50">
      {/* Top Contact Bar */}
      <div className="bg-[#000000] text-white py-2">
        <div className="container mx-auto px-4">
          <div className="flex flex-col sm:flex-row justify-between items-center text-sm">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4" />
                <span>+507 6123-4567</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                <span>info@homepowerpty.com</span>
              </div>
            </div>
            <div className="flex items-center gap-4 mt-1 sm:mt-0">
              <a href="#" className="hover:text-[#FF9F1C] transition-colors">Facebook</a>
              <a href="#" className="hover:text-[#FF9F1C] transition-colors">Instagram</a>
              <a href="#" className="hover:text-[#FF9F1C] transition-colors">TikTok</a>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="py-4">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-[#FF9F1C]">HomePower</h1>
              <span className="text-sm text-[#718096] ml-2">PTY</span>
            </div>

            {/* Desktop Navigation */}
            <ul className="hidden lg:flex space-x-8">
              {navItems.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => onSectionClick(item.id)}
                    className={`font-medium transition-colors duration-300 hover:text-[#FF9F1C] ${
                      activeSection === item.id ? 'text-[#FF9F1C]' : 'text-[#000000]'
                    }`}
                  >
                    {item.label}
                  </button>
                </li>
              ))}
            </ul>

            {/* CTA Button */}
            <button
              onClick={() => onSectionClick('contacto')}
              className="hidden lg:block bg-[#FF9F1C] text-white px-6 py-2 rounded-lg font-semibold hover:bg-[#FF9F1C]/90 transition-all duration-300 transform hover:scale-105"
            >
              Cotizar Ahora
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="lg:hidden text-[#000000] hover:text-[#FF9F1C] transition-colors"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden bg-white border-t border-gray-200">
            <div className="container mx-auto px-4 py-4">
              <ul className="space-y-4">
                {navItems.map((item) => (
                  <li key={item.id}>
                    <button
                      onClick={() => onSectionClick(item.id)}
                      className={`block w-full text-left font-medium transition-colors duration-300 hover:text-[#FF9F1C] ${
                        activeSection === item.id ? 'text-[#FF9F1C]' : 'text-[#000000]'
                      }`}
                    >
                      {item.label}
                    </button>
                  </li>
                ))}
                <li className="pt-4 border-t border-gray-200">
                  <button
                    onClick={() => onSectionClick('contacto')}
                    className="w-full bg-[#FF9F1C] text-white px-6 py-2 rounded-lg font-semibold hover:bg-[#FF9F1C]/90 transition-colors"
                  >
                    Cotizar Ahora
                  </button>
                </li>
              </ul>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;