import React, { useState } from 'react';
import { Phone, Mail, MapPin, Clock, Send, CheckCircle } from 'lucide-react';

const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    company: '',
    category: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const categories = [
    'Seleccionar categoría',
    'Planchas',
    'Licuadoras',
    'Air Fryers',
    'Cafeteras',
    'Tostadoras',
    'Sandwicheras',
    'Teteras',
    'Estufas',
    'Otros'
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    console.log('Formulario enviado:', formData);
    setIsSubmitted(true);
    setIsSubmitting(false);

    // Reset form after 3 seconds
    setTimeout(() => {
      setIsSubmitted(false);
      setFormData({
        name: '',
        phone: '',
        email: '',
        company: '',
        category: '',
        message: ''
      });
    }, 3000);
  };

  const contactInfo = [
    {
      icon: <Phone className="w-6 h-6" />,
      title: 'Teléfono Principal',
      info: '+507 6123-4567',
      color: 'text-[#4CAF50]'
    },
    {
      icon: <Mail className="w-6 h-6" />,
      title: 'Correo Corporativo',
      info: 'info@homepowerpty.com',
      color: 'text-[#FF9F1C]'
    },
    {
      icon: <MapPin className="w-6 h-6" />,
      title: 'Oficina Principal',
      info: 'Ciudad de Panamá, Panamá',
      color: 'text-[#ff4b4b]'
    },
    {
      icon: <Clock className="w-6 h-6" />,
      title: 'Horario de Atención',
      info: 'Lun-Vie: 8:00 AM - 6:00 PM',
      color: 'text-[#718096]'
    }
  ];

  if (isSubmitted) {
    return (
      <section id="contacto" className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <div className="bg-[#4CAF50] w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-[#000000] mb-4">¡Mensaje Enviado!</h2>
            <p className="text-lg text-[#718096] mb-6">
              Gracias por contactarnos. Nuestro equipo se pondrá en contacto contigo dentro de las próximas 24 horas.
            </p>
            <div className="bg-[#F7F7F7] rounded-lg p-6">
              <p className="text-[#718096]">
                Para consultas urgentes, puedes llamarnos directamente al 
                <a href="tel:+50761234567" className="text-[#FF9F1C] font-semibold ml-1">
                  +507 6123-4567
                </a>
              </p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="contacto" className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-[#000000] mb-4">Contáctanos</h2>
            <p className="text-xl text-[#718096] max-w-3xl mx-auto">
              Estamos aquí para ayudarte. Envíanos tu consulta y nos pondremos en contacto contigo 
              lo antes posible para brindarte la mejor atención.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div className="bg-[#F7F7F7] rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-[#000000] mb-6">Envíanos tu Consulta</h3>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-[#000000] mb-2">
                      Nombre Completo *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300"
                      placeholder="Tu nombre completo"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-[#000000] mb-2">
                      Teléfono *
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300"
                      placeholder="+507 1234-5678"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-[#000000] mb-2">
                      Correo Electrónico *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300"
                      placeholder="tu@email.com"
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="company" className="block text-sm font-medium text-[#000000] mb-2">
                      Empresa
                    </label>
                    <input
                      type="text"
                      id="company"
                      name="company"
                      value={formData.company}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300"
                      placeholder="Nombre de tu empresa"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-[#000000] mb-2">
                    Categoría de Interés
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300"
                  >
                    {categories.map((category, index) => (
                      <option key={index} value={index === 0 ? '' : category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-[#000000] mb-2">
                    Mensaje *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                    rows={5}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FF9F1C] focus:border-transparent transition-all duration-300 resize-none"
                    placeholder="Cuéntanos sobre tus necesidades, cantidades requeridas, presupuesto estimado, etc."
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-[#FF9F1C] text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-[#FF9F1C]/90 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Enviando...
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      Enviar Consulta
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Contact Information */}
            <div>
              <h3 className="text-2xl font-bold text-[#000000] mb-8">Información de Contacto</h3>
              
              <div className="space-y-6 mb-8">
                {contactInfo.map((item, index) => (
                  <div key={index} className="flex items-start gap-4">
                    <div className={`${item.color} mt-1`}>
                      {item.icon}
                    </div>
                    <div>
                      <h4 className="font-semibold text-[#000000] mb-1">{item.title}</h4>
                      <p className="text-[#718096]">{item.info}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Map Placeholder */}
              <div className="bg-[#F7F7F7] rounded-xl p-8 text-center mb-8">
                <MapPin className="w-16 h-16 text-[#FF9F1C] mx-auto mb-4" />
                <h4 className="text-lg font-semibold text-[#000000] mb-2">Visítanos</h4>
                <p className="text-[#718096]">
                  Oficina ubicada en el corazón comercial de Ciudad de Panamá. 
                  Agenda una cita para conocer nuestros productos en persona.
                </p>
              </div>

              {/* Quick Actions */}
              <div className="space-y-4">
                <a
                  href="https://wa.me/50761234567?text=Hola,%20me%20interesa%20conocer%20más%20sobre%20sus%20productos"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full bg-[#4CAF50] text-white px-6 py-3 rounded-lg font-semibold text-center hover:bg-[#4CAF50]/90 transition-all duration-300 transform hover:scale-105"
                >
                  Chatear por WhatsApp
                </a>
                <a
                  href="tel:+50761234567"
                  className="block w-full bg-[#000000] text-white px-6 py-3 rounded-lg font-semibold text-center hover:bg-gray-800 transition-all duration-300 transform hover:scale-105"
                >
                  Llamar Ahora
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactForm;