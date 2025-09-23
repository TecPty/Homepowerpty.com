import React from 'react';
import { Star, Quote } from 'lucide-react';

const Clients: React.FC = () => {
  const testimonials = [
    {
      id: 1,
      name: 'María González',
      company: 'Electrodomésticos del Istmo',
      rating: 5,
      comment: 'HomePower ha sido nuestro proveedor principal durante más de 3 años. Su calidad de productos y servicio al cliente es excepcional.',
      avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=150'
    },
    {
      id: 2,
      name: 'Carlos Mendoza',
      company: 'Distribuciones Panamá',
      rating: 5,
      comment: 'Los precios competitivos y la garantía extendida que ofrece HomePower nos han permitido expandir nuestro negocio significativamente.',
      avatar: 'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=150'
    },
    {
      id: 3,
      name: 'Ana Rodríguez',
      company: 'Hogar Moderno',
      rating: 5,
      comment: 'El soporte técnico de HomePower es incomparable. Siempre están disponibles para resolver cualquier duda o problema.',
      avatar: 'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=150'
    }
  ];

  const clientLogos = [
    { name: 'ElectroMax', logo: 'EM' },
    { name: 'Hogar Plus', logo: 'HP' },
    { name: 'TecnoVida', logo: 'TV' },
    { name: 'Casa Moderna', logo: 'CM' },
    { name: 'ElectroStore', logo: 'ES' },
    { name: 'Innovación Hogar', logo: 'IH' }
  ];

  const benefits = [
    {
      title: 'Precios Mayoristas',
      description: 'Ofrecemos los mejores precios del mercado para compras al por mayor',
      icon: '💰'
    },
    {
      title: 'Soporte Dedicado',
      description: 'Cada cliente tiene un representante dedicado para atención personalizada',
      icon: '🤝'
    },
    {
      title: 'Entrega Garantizada',
      description: 'Cumplimos con los tiempos de entrega acordados sin excepción',
      icon: '🚚'
    },
    {
      title: 'Garantía Extendida',
      description: 'Todos nuestros productos incluyen garantía extendida sin costo adicional',
      icon: '🛡️'
    }
  ];

  return (
    <section id="clientes" className="py-16 bg-[#F7F7F7]">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-[#000000] mb-4">Nuestros Clientes</h2>
            <p className="text-xl text-[#718096] max-w-3xl mx-auto">
              Empresas líderes confían en HomePower para sus necesidades de electrodomésticos. 
              Conoce las experiencias de nuestros socios comerciales.
            </p>
          </div>

          {/* Client Logos */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-[#000000] text-center mb-8">Empresas que Confían en Nosotros</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
              {clientLogos.map((client, index) => (
                <div
                  key={index}
                  className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center"
                >
                  <div className="text-center">
                    <div className="w-12 h-12 bg-[#FF9F1C] text-white rounded-full flex items-center justify-center mx-auto mb-2 font-bold">
                      {client.logo}
                    </div>
                    <span className="text-sm font-medium text-[#718096]">{client.name}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Testimonials */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-[#000000] text-center mb-12">Lo que Dicen Nuestros Clientes</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {testimonials.map((testimonial) => (
                <div
                  key={testimonial.id}
                  className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 relative"
                >
                  <div className="absolute -top-4 left-8">
                    <div className="w-8 h-8 bg-[#FF9F1C] rounded-full flex items-center justify-center">
                      <Quote className="w-4 h-4 text-white" />
                    </div>
                  </div>
                  
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-5 h-5 text-[#FBD38D] fill-current" />
                    ))}
                  </div>
                  
                  <p className="text-[#718096] mb-6 leading-relaxed italic">"{testimonial.comment}"</p>
                  
                  <div className="flex items-center">
                    <img
                      src={testimonial.avatar}
                      alt={testimonial.name}
                      className="w-12 h-12 rounded-full mr-4 object-cover"
                    />
                    <div>
                      <h4 className="font-semibold text-[#000000]">{testimonial.name}</h4>
                      <p className="text-sm text-[#718096]">{testimonial.company}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Benefits for Clients */}
          <div className="bg-white rounded-2xl p-12">
            <h3 className="text-3xl font-bold text-[#000000] text-center mb-12">¿Por qué Elegir HomePower?</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {benefits.map((benefit, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl mb-4">{benefit.icon}</div>
                  <h4 className="text-lg font-semibold text-[#000000] mb-3">{benefit.title}</h4>
                  <p className="text-[#718096] text-sm leading-relaxed">{benefit.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* CTA Section */}
          <div className="mt-16 bg-gradient-to-r from-[#FF9F1C] to-[#FBD38D] rounded-2xl p-12 text-center text-white">
            <h3 className="text-3xl font-bold mb-4">¿Listo para Ser Nuestro Próximo Cliente?</h3>
            <p className="text-xl mb-8 opacity-90">
              Únete a las empresas líderes que ya confían en HomePower para sus necesidades de electrodomésticos.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-[#000000] text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-all duration-300 transform hover:scale-105">
                Solicitar Propuesta
              </button>
              <button className="bg-white text-[#FF9F1C] px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-300 transform hover:scale-105">
                Agendar Reunión
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Clients;