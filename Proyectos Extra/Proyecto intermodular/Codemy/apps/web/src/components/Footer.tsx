import Link from 'next/link'
import { Code2, Github, Twitter, Linkedin, Mail, Heart } from 'lucide-react'

export function Footer() {
  const currentYear = new Date().getFullYear()

  const links = {
    product: [
      { name: 'Cursos', href: '/cursos' },
      { name: 'Retos', href: '/retos' },
      { name: 'Ranking', href: '/ranking' },
      { name: 'Precios', href: '/precios' },
      { name: 'API', href: '/api' }
    ],
    company: [
      { name: 'Sobre nosotros', href: '/about' },
      { name: 'Blog', href: '/blog' },
      { name: 'Careers', href: '/careers' },
      { name: 'Prensa', href: '/press' },
      { name: 'Contacto', href: '/contacto' }
    ],
    resources: [
      { name: 'Documentación', href: '/docs' },
      { name: 'Guías', href: '/guides' },
      { name: 'FAQ', href: '/faq' },
      { name: 'Comunidad', href: '/community' },
      { name: 'Estado', href: '/status' }
    ],
    legal: [
      { name: 'Privacidad', href: '/privacy' },
      { name: 'Términos', href: '/terms' },
      { name: 'Cookies', href: '/cookies' },
      { name: 'Legal', href: '/legal' },
      { name: 'GDPR', href: '/gdpr' }
    ]
  }

  const socialLinks = [
    { name: 'GitHub', icon: Github, href: 'https://github.com/codedungeon' },
    { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/codedungeondev' },
    { name: 'LinkedIn', icon: Linkedin, href: 'https://linkedin.com/company/codedungeon' },
    { name: 'Email', icon: Mail, href: 'mailto:hola@codedungeon.es' }
  ]

  return (
    <footer className="bg-stone-950 text-stone-100 border-t-2 border-stone-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-6 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-6">
              <div className="w-8 h-8 bg-amber-700 border-2 border-amber-800 flex items-center justify-center">
                <Code2 className="w-5 h-5 text-stone-100" />
              </div>
              <span className="text-xl font-bold text-stone-100">
                Code Dungeon
              </span>
            </Link>
            <p className="text-stone-400 text-sm leading-relaxed mb-6 max-w-sm">
              Academia web completa para aprender programación con gamificación, 
              autocorrección y soporte multi-lenguaje. El futuro de la educación tecnológica.
            </p>
            <div className="flex items-center space-x-4">
              {socialLinks.map((social) => {
                const IconComponent = social.icon
                return (
                  <a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center hover:bg-amber-600 transition-colors border border-stone-500/30"
                  >
                    <IconComponent className="w-5 h-5" />
                  </a>
                )
              })}
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-bold text-white mb-4">Producto</h3>
            <ul className="space-y-2">
              {links.product.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-bold text-white mb-4">Empresa</h3>
            <ul className="space-y-2">
              {links.company.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-bold text-white mb-4">Recursos</h3>
            <ul className="space-y-2">
              {links.resources.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-bold text-white mb-4">Legal</h3>
            <ul className="space-y-2">
              {links.legal.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-gray-400 hover:text-white transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="max-w-xl">
            <h3 className="font-bold text-white mb-2">Newsletter</h3>
            <p className="text-gray-400 text-sm mb-4">
              Recibe las últimas actualizaciones, nuevos cursos y contenido exclusivo.
            </p>
            <form className="flex space-x-2">
              <input
                type="email"
                placeholder="tu@email.com"
                className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:border-stone-500 focus:ring-1 focus:ring-blue-500 outline-none text-white placeholder-gray-400"
              />
              <button
                type="submit"
                className="bg-gradient-to-r from-stone-600 to-stone-600 px-6 py-2 rounded-lg hover:from-stone-700 hover:to-stone-700 transition-colors font-medium"
              >
                Suscribirse
              </button>
            </form>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          {/* Professor Attribution */}
          <div className="mb-6 p-4 bg-gradient-to-r from-stone-900/30 to-stone-900/30 rounded-lg border border-stone-800/30">
            <div className="flex items-center gap-3 text-sm">
              <div className="flex items-center gap-2 text-stone-400">
                <Code2 className="w-5 h-5" />
                <span className="font-semibold">Contenido Educativo:</span>
              </div>
              <span className="text-gray-300">
                Basado en el curso de programación de{' '}
                <a
                  href="https://github.com/jocarsa/dam2526"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-stone-400 hover:text-stone-300 font-semibold underline decoration-dotted underline-offset-2"
                >
                  José Vicente Carratalá
                </a>
                {' '}(jocarsa/dam2526)
              </span>
            </div>
          </div>
          
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              <p className="flex items-center space-x-1">
                <span>© {currentYear} CodeAcademy. Hecho con</span>
                <Heart className="w-4 h-4 text-red-500 fill-current" />
                <span>en España.</span>
              </p>
            </div>
            
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span>Todos los sistemas operativos</span>
              </div>
              <div className="text-xs">
                v1.0.0-beta
              </div>
            </div>
          </div>
        </div>

        {/* Extra Info */}
        <div className="mt-8 p-4 bg-gray-800/50 rounded-lg border border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center text-xs text-gray-400">
            <div>
              <p className="mb-2 md:mb-0">
                🚀 <strong>MVP AAA</strong> - Arquitectura escalable desde 100 a 100,000 usuarios
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <span>Next.js 14</span>
              <span>•</span>
              <span>Supabase</span>
              <span>•</span>
              <span>Stripe</span>
              <span>•</span>
              <span>Docker</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}