import React from 'react';
import { Target, Eye, Award, Users, Clock, Shield } from 'lucide-react';

const AboutUs: React.FC = () => {
  const values = [
    {
      icon: <Award className="w-8 h-8 text-[#FF9F1C]" />,
      title: 'Calidad Premium',
      description: 'Seleccionamos solo las mejores marcas y productos con los más altos estándares de calidad.'
    },
    {
      icon: <Users className="w-8 h-8 text-[#4CAF50]" />,
      title: 'Atención Personalizada',
      description: 'Cada cliente recibe un servicio dedicado y soluciones adaptadas a sus necesidades específicas.'
    },
    {
      icon: <Clock className="w-8 h-8 text-[#ff4b4b]" />,
      title: 'Entrega Rápida',
      description: 'Procesos ágiles y eficientes para garantizar la entrega oportuna de todos nuestros productos.'
    },
    {
      icon: <Shield className="w-8 h-8 text-[#718096]" />,
      title: 'Garantía Extendida',
      description: 'Respaldamos nuestros productos con garantías completas y soporte técnico especializado.'
    }
  ];

  const stats = [
    { number: '15+', label: 'Años de Experiencia' },
    { number: '500+', label: 'Productos en Catálogo' },
    { number: '100+', label: 'Clientes Satisfechos' },
    { number: '24/7', label: 'Soporte Técnico' }
  ];

  return (
    <section id="nosotros" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-[#000000] mb-4">Conoce HomePower</h2>
            <p className="text-xl text-[#718096] max-w-3xl mx-auto">
              Somos líderes en la distribución mayorista de electrodomésticos innovadores, 
              comprometidos con la excelencia y la satisfacción de nuestros clientes.
            </p>
          </div>

          {/* Mission and Vision */}
          <div className="grid lg:grid-cols-2 gap-12 mb-16">
            {/* Mission */}
            <div className="bg-[#F7F7F7] rounded-2xl p-8">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-[#FF9F1C] rounded-lg flex items-center justify-center mr-4">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-[#000000]">Nuestra Misión</h3>
              </div>
              <p className="text-[#718096] leading-relaxed text-lg">
                Brindar soluciones innovadoras y confiables en electrodomésticos para el hogar, 
                ofreciendo productos de alta calidad con precios competitivos y un servicio 
                excepcional que supere las expectativas de nuestros clientes corporativos en 
                Panamá y Latinoamérica.
              </p>
            </div>

            {/* Vision */}
            <div className="bg-[#F7F7F7] rounded-2xl p-8">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-[#4CAF50] rounded-lg flex items-center justify-center mr-4">
                  <Eye className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-[#000000]">Nuestra Visión</h3>
              </div>
              <p className="text-[#718096] leading-relaxed text-lg">
                Convertirnos en la empresa líder de distribución mayorista de electrodomésticos 
                en Latinoamérica, reconocida por nuestra innovación, calidad excepcional y 
                compromiso inquebrantable con el éxito de nuestros socios comerciales.
              </p>
            </div>
          </div>

          {/* Values */}
          <div className="mb-16">
            <h3 className="text-3xl font-bold text-[#000000] text-center mb-12">Nuestros Valores</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {values.map((value, index) => (
                <div
                  key={index}
                  className="text-center p-6 rounded-xl bg-[#F7F7F7] hover:shadow-lg transition-all duration-300 transform hover:-translate-y-2"
                >
                  <div className="flex justify-center mb-4">
                    {value.icon}
                  </div>
                  <h4 className="text-lg font-semibold text-[#000000] mb-3">{value.title}</h4>
                  <p className="text-[#718096] text-sm leading-relaxed">{value.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="bg-gradient-to-r from-[#FF9F1C] to-[#FBD38D] rounded-2xl p-12 text-white text-center">
            <h3 className="text-3xl font-bold mb-8">HomePower en Números</h3>
            <div className="grid md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl font-bold mb-2">{stat.number}</div>
                  <div className="text-white/90">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Team Section */}
          <div className="mt-16 text-center">
            <h3 className="text-3xl font-bold text-[#000000] mb-6">Nuestro Compromiso</h3>
            <p className="text-lg text-[#718096] max-w-4xl mx-auto mb-8">
              En HomePower, cada miembro de nuestro equipo está comprometido con brindar 
              la mejor experiencia de compra, desde la selección de productos hasta el 
              soporte post-venta. Trabajamos incansablemente para ser tu socio confiable 
              en el crecimiento de tu negocio.
            </p>
            <div className="inline-flex items-center gap-2 bg-[#FF9F1C] text-white px-8 py-4 rounded-lg font-semibold">
              <Shield className="w-5 h-5" />
              Garantía de Satisfacción 100%
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutUs;