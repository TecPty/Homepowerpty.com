import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Users, Award, Star, ArrowRight, Menu, ChefHat, Coffee, Utensils } from "lucide-react"

export default function ElArteDeServir() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <BookOpen className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold text-foreground">El Arte de Servir</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <a
              href="#sobre-el-libro"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Sobre el Libro
            </a>
            <a
              href="#contenido"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Contenido
            </a>
            <a
              href="#testimonios"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Testimonios
            </a>
            <a
              href="#autor"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Autor
            </a>
          </nav>

          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="hidden md:inline-flex">
              Vista Previa
            </Button>
            <Button>Obtener Libro</Button>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 bg-gradient-to-br from-background via-muted/30 to-background">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge variant="secondary" className="mb-6 bg-accent text-accent-foreground">
                📚 Guía Profesional de Hospitalidad
              </Badge>
              <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl text-balance">
                El Arte de Servir
              </h1>
              <p className="mt-4 text-xl text-muted-foreground text-balance">
                La guía para transformar el servicio en momentos memorables
              </p>
              <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-xl text-pretty">
                Más que servicio, una guía para transformar cada visita en una experiencia única estrellada. Descubre
                las técnicas profesionales que elevan la hospitalidad a un arte.
              </p>
              <div className="mt-10 flex items-center gap-x-6">
                <Button size="lg" className="h-12 px-8">
                  Obtener el Libro
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg" className="h-12 px-8 bg-transparent">
                  Leer Muestra
                </Button>
              </div>
              <p className="mt-4 text-sm text-muted-foreground">
                Disponible en formato digital • Acceso inmediato • Garantía de satisfacción
              </p>
            </div>
            <div className="flex justify-center lg:justify-end">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-accent/20 rounded-2xl blur-3xl"></div>
                <img
                  src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-mxjgvOknSOMn5Hucc4pQvsBHjaK76q.png"
                  alt="Portada del libro El Arte de Servir"
                  className="relative w-80 h-auto rounded-2xl shadow-2xl"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About the Book Section */}
      <section id="sobre-el-libro" className="py-20 lg:py-32 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl text-balance">
              Sobre el Libro
            </h2>
            <p className="mt-4 text-lg text-muted-foreground text-pretty">
              Una guía completa para profesionales de la hospitalidad
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <Card className="p-8">
                <CardContent className="p-0">
                  <h3 className="text-2xl font-bold mb-4 text-foreground">¿Para Quién es Este Libro?</h3>
                  <p className="text-muted-foreground leading-relaxed mb-6">
                    Dirigido a todos aquellos profesionales que comprenden que el servicio es mucho más que una
                    transacción. Desde meseros experimentados hasta gerentes de restaurante, este libro ofrece las
                    herramientas necesarias para elevar cada interacción a un nivel excepcional.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-start">
                      <ChefHat className="h-5 w-5 text-primary mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">Profesionales de restaurantes y hoteles</span>
                    </li>
                    <li className="flex items-start">
                      <Users className="h-5 w-5 text-primary mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">Gerentes y supervisores de servicio</span>
                    </li>
                    <li className="flex items-start">
                      <Coffee className="h-5 w-5 text-primary mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">Emprendedores del sector gastronómico</span>
                    </li>
                    <li className="flex items-start">
                      <Award className="h-5 w-5 text-primary mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">Estudiantes de hospitalidad y turismo</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-6 text-foreground">Lo Que Aprenderás</h3>
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center mr-4 mt-1 flex-shrink-0">
                    <span className="text-sm font-semibold text-primary">1</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground">Fundamentos del Servicio Excepcional</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Los principios básicos que transforman un servicio ordinario en una experiencia memorable.
                    </p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center mr-4 mt-1 flex-shrink-0">
                    <span className="text-sm font-semibold text-primary">2</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground">Técnicas de Comunicación Efectiva</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Cómo conectar genuinamente con cada cliente y crear momentos únicos.
                    </p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center mr-4 mt-1 flex-shrink-0">
                    <span className="text-sm font-semibold text-primary">3</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-foreground">Gestión de Situaciones Difíciles</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Estrategias probadas para convertir problemas en oportunidades de fidelización.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Content/Chapters Section */}
      <section id="contenido" className="py-20 lg:py-32">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl text-balance">
              Contenido del Libro
            </h2>
            <p className="mt-4 text-lg text-muted-foreground text-pretty">
              Capítulos diseñados para una transformación completa del servicio
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <Utensils className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Introducción al Servicio</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Los fundamentos que todo profesional debe dominar para crear experiencias excepcionales desde el
                  primer contacto.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <Users className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Psicología del Cliente</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Comprende las motivaciones y expectativas de tus clientes para anticipar sus necesidades y superarlas.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <Award className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Excelencia Operativa</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Sistemas y procesos que garantizan consistencia en la calidad del servicio, día tras día.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <Coffee className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Momentos de Verdad</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Identifica y aprovecha esos momentos críticos que definen la percepción del cliente sobre tu servicio.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <ChefHat className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Liderazgo en Servicio</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Cómo liderar equipos de servicio y crear una cultura organizacional centrada en la excelencia.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50">
              <CardHeader>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <Star className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Casos de Éxito</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Ejemplos reales de transformaciones exitosas y las lecciones aprendidas en el camino.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonios" className="py-20 lg:py-32 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl text-balance">
              Lo Que Dicen los Profesionales
            </h2>
            <p className="mt-4 text-lg text-muted-foreground text-pretty">
              Testimonios de líderes en la industria de la hospitalidad
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                  ))}
                </div>
                <blockquote className="text-base leading-relaxed mb-4">
                  "Este libro ha revolucionado la forma en que nuestro equipo entiende el servicio. Los resultados han
                  sido extraordinarios, con un aumento del 40% en la satisfacción del cliente."
                </blockquote>
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                    <span className="text-sm font-semibold text-primary">MR</span>
                  </div>
                  <div>
                    <div className="font-semibold text-sm">María Rodríguez</div>
                    <div className="text-xs text-muted-foreground">Gerente General, Restaurante Estrella</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                  ))}
                </div>
                <blockquote className="text-base leading-relaxed mb-4">
                  "Una guía indispensable para cualquier profesional serio sobre la hospitalidad. Las técnicas son
                  prácticas y los resultados, inmediatos."
                </blockquote>
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                    <span className="text-sm font-semibold text-primary">CL</span>
                  </div>
                  <div>
                    <div className="font-semibold text-sm">Carlos López</div>
                    <div className="text-xs text-muted-foreground">Director de Operaciones, Hotel Boutique</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                  ))}
                </div>
                <blockquote className="text-base leading-relaxed mb-4">
                  "Transformó completamente nuestra cultura de servicio. Ahora nuestros clientes no solo regresan, sino
                  que se convierten en embajadores de nuestra marca."
                </blockquote>
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                    <span className="text-sm font-semibold text-primary">AS</span>
                  </div>
                  <div>
                    <div className="font-semibold text-sm">Ana Sánchez</div>
                    <div className="text-xs text-muted-foreground">Propietaria, Cadena de Cafeterías</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Author Section */}
      <section id="autor" className="py-20 lg:py-32">
        <div className="container">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl text-balance mb-6">
                Sobre el Autor
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                Con más de 15 años de experiencia en la industria de la hospitalidad, el autor ha trabajado en algunos
                de los restaurantes y hoteles más prestigiosos del mundo. Su pasión por la excelencia en el servicio lo
                ha llevado a desarrollar metodologías únicas que han transformado cientos de establecimientos.
              </p>
              <p className="text-lg text-muted-foreground leading-relaxed mb-8">
                Consultor internacional y conferencista reconocido, ha capacitado a miles de profesionales en el arte de
                crear experiencias memorables para los clientes.
              </p>
              <div className="flex items-center space-x-4">
                <Badge variant="outline" className="bg-transparent">
                  15+ años de experiencia
                </Badge>
                <Badge variant="outline" className="bg-transparent">
                  Consultor internacional
                </Badge>
              </div>
            </div>
            <div className="flex justify-center lg:justify-end">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-accent/20 rounded-2xl blur-2xl"></div>
                <div className="relative w-80 h-80 rounded-2xl bg-gradient-to-br from-muted to-card flex items-center justify-center shadow-xl">
                  <div className="text-center">
                    <div className="h-24 w-24 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="h-12 w-12 text-primary" />
                    </div>
                    <p className="text-muted-foreground text-sm">Foto del autor</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 lg:py-32 bg-primary text-primary-foreground">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl text-balance">
              ¿Listo para Transformar tu Servicio?
            </h2>
            <p className="mt-4 text-lg text-primary-foreground/80 text-pretty">
              Únete a miles de profesionales que ya han elevado su servicio al siguiente nivel con "El Arte de Servir".
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button size="lg" variant="secondary" className="h-12 px-8">
                Obtener el Libro Ahora
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-12 px-8 border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/10 bg-transparent"
              >
                Leer Muestra Gratis
              </Button>
            </div>
            <p className="mt-4 text-sm text-primary-foreground/60">
              Acceso inmediato • Formato digital • Garantía de satisfacción
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30">
        <div className="container py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                  <BookOpen className="h-5 w-5 text-primary-foreground" />
                </div>
                <span className="text-xl font-bold">El Arte de Servir</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Transformando el servicio en experiencias memorables, una interacción a la vez.
              </p>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Libro</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Contenido
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Muestra Gratuita
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Testimonios
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Recursos Adicionales
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Servicios</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Consultoría
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Capacitaciones
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Conferencias
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Contacto
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Política de Privacidad
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Términos de Uso
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Devoluciones
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Soporte
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">© 2024 El Arte de Servir. Todos los derechos reservados.</p>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                <span className="sr-only">LinkedIn</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z"
                    clipRule="evenodd"
                  />
                </svg>
              </a>
              <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                <span className="sr-only">Instagram</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"
                    clipRule="evenodd"
                  />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
