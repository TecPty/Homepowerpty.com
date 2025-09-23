import React, { useState } from 'react';
import { Search, Filter, ShoppingCart, Eye } from 'lucide-react';

const ProductCatalog: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('todos');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { id: 'todos', label: 'Todos los Productos' },
    { id: 'cocina', label: 'Cocina' },
    { id: 'cuidado', label: 'Cuidado Personal' },
    { id: 'limpieza', label: 'Limpieza' }
  ];

  const products = [
    {
      id: 1,
      name: 'Plancha de Vapor Pro',
      category: 'cuidado',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/6963098/pexels-photo-6963098.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['2400W', 'Base cerámica', 'Vapor vertical'],
      inStock: true
    },
    {
      id: 2,
      name: 'Licuadora Ultra Power',
      category: 'cocina',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/8034895/pexels-photo-8034895.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['1200W', '2L capacidad', '5 velocidades'],
      inStock: true
    },
    {
      id: 3,
      name: 'Air Fryer Digital',
      category: 'cocina',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/7251718/pexels-photo-7251718.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['1400W', '4L capacidad', 'Pantalla digital'],
      inStock: true
    },
    {
      id: 4,
      name: 'Cafetera Espresso',
      category: 'cocina',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['19 bar', 'Molinillo integrado', 'Espumador'],
      inStock: true
    },
    {
      id: 5,
      name: 'Tostadora 4 Rebanadas',
      category: 'cocina',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/6578916/pexels-photo-6578916.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['1600W', '6 niveles', 'Función descongelar'],
      inStock: false
    },
    {
      id: 6,
      name: 'Sandwichera Multifunción',
      category: 'cocina',
      price: 'Consultar',
      image: 'https://images.pexels.com/photos/4349775/pexels-photo-4349775.jpeg?auto=compress&cs=tinysrgb&w=800',
      specs: ['800W', 'Placas intercambiables', 'Antiadherente'],
      inStock: true
    }
  ];

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'todos' || product.category === selectedCategory;
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleStockInquiry = (productName: string) => {
    const message = `Hola, me interesa consultar el stock del producto: ${productName}`;
    const whatsappUrl = `https://wa.me/50761234567?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <section id="electrodomesticos" className="py-16 bg-[#F7F7F7]">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-[#000000] mb-4">Nuestro Catálogo</h2>
            <p className="text-xl text-[#718096] max-w-3xl mx-auto">
              Descubre nuestra amplia selección de electrodomésticos innovadores con la mejor calidad y garantía
            </p>
          </div>

          {/* Search and Filter */}
          <div className="mb-8">
            <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#718096] w-5 h-5" />
                <input
                  type="text"
                  placeholder="Buscar productos..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent"
                />
              </div>
              
              <div className="flex gap-2 flex-wrap">
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={`px-6 py-2 rounded-full font-medium transition-all duration-300 ${
                      selectedCategory === category.id
                        ? 'bg-[#FF9F1C] text-white shadow-lg'
                        : 'bg-white text-[#718096] hover:bg-[#FF9F1C]/10 hover:text-[#FF9F1C]'
                    }`}
                  >
                    {category.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Products Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredProducts.map((product) => (
              <div
                key={product.id}
                className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2"
              >
                <div className="relative overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-64 object-cover transition-transform duration-300 hover:scale-110"
                  />
                  <div className="absolute top-4 right-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      product.inStock 
                        ? 'bg-[#4CAF50] text-white' 
                        : 'bg-[#ff4b4b] text-white'
                    }`}>
                      {product.inStock ? 'En Stock' : 'Consultar'}
                    </span>
                  </div>
                </div>
                
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-[#000000] mb-3">{product.name}</h3>
                  
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-[#718096] mb-2">Especificaciones:</h4>
                    <ul className="space-y-1">
                      {product.specs.map((spec, index) => (
                        <li key={index} className="text-sm text-[#718096] flex items-center gap-2">
                          <div className="w-1.5 h-1.5 bg-[#FF9F1C] rounded-full"></div>
                          {spec}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-lg font-bold text-[#FF9F1C]">{product.price}</span>
                    <button
                      onClick={() => handleStockInquiry(product.name)}
                      className="bg-[#FF9F1C] text-white px-4 py-2 rounded-lg font-medium hover:bg-[#FF9F1C]/90 transition-all duration-300 flex items-center gap-2"
                    >
                      <Eye className="w-4 h-4" />
                      Consultar Stock
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredProducts.length === 0 && (
            <div className="text-center py-12">
              <p className="text-xl text-[#718096]">No se encontraron productos que coincidan con tu búsqueda.</p>
            </div>
          )}

          {/* CTA Section */}
          <div className="mt-16 bg-gradient-to-r from-[#FF9F1C] to-[#FBD38D] rounded-2xl p-8 text-center text-white">
            <h3 className="text-2xl font-bold mb-4">¿No encuentras lo que buscas?</h3>
            <p className="text-lg mb-6 opacity-90">
              Contáctanos y te ayudaremos a encontrar el electrodoméstico perfecto para tus necesidades
            </p>
            <button
              onClick={() => handleStockInquiry('producto personalizado')}
              className="bg-[#000000] text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-all duration-300 transform hover:scale-105"
            >
              Contactar Especialista
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProductCatalog;