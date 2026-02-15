/**
 * SEO Configuration
 * Metadata y configuración SEO para Code Dungeon
 */

import { Metadata } from 'next';

const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://codedungeon.es';

export const siteConfig = {
  name: 'Code Dungeon',
  title: 'Code Dungeon - Aprende Programación para Todos',
  description:
    'Academia online de programación con gamificación real. Cursos para todas las edades, todos los niveles y todos los lenguajes. Python, JavaScript, C#, Unity y más.',
  url: baseUrl,
  ogImage: `${baseUrl}/og-image.png`,
  links: {
    twitter: 'https://twitter.com/CodeDungeonDev',
    github: 'https://github.com/codedungeon',
    discord: 'https://discord.gg/codedungeon',
  },
  keywords: [
    'programación',
    'aprender a programar',
    'cursos de programación',
    'Python',
    'JavaScript',
    'C#',
    'Unity',
    'gamificación',
    'educación online',
    'coding para niños',
    'academia de programación',
    'desarrollo web',
    'desarrollo de videojuegos',
  ],
};

export const defaultMetadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: siteConfig.title,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  keywords: siteConfig.keywords,
  authors: [
    {
      name: 'CodeAcademy Team',
      url: siteConfig.url,
    },
  ],
  creator: 'CodeAcademy',
  publisher: 'CodeAcademy',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'es_ES',
    url: siteConfig.url,
    title: siteConfig.title,
    description: siteConfig.description,
    siteName: siteConfig.name,
    images: [
      {
        url: siteConfig.ogImage,
        width: 1200,
        height: 630,
        alt: siteConfig.name,
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.title,
    description: siteConfig.description,
    images: [siteConfig.ogImage],
    creator: '@CodeAcademyDev',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
};

/**
 * Generar metadata para páginas dinámicas
 */
export function generatePageMetadata({
  title,
  description,
  image,
  noIndex = false,
}: {
  title: string;
  description?: string;
  image?: string;
  noIndex?: boolean;
}): Metadata {
  return {
    title,
    description: description || siteConfig.description,
    openGraph: {
      title,
      description: description || siteConfig.description,
      images: image ? [image] : [siteConfig.ogImage],
    },
    twitter: {
      title,
      description: description || siteConfig.description,
      images: image ? [image] : [siteConfig.ogImage],
    },
    robots: noIndex
      ? {
          index: false,
          follow: false,
        }
      : undefined,
  };
}

/**
 * JSON-LD para SEO estructurado
 */
export const jsonLdWebsite = {
  '@context': 'https://schema.org',
  '@type': 'EducationalOrganization',
  name: siteConfig.name,
  description: siteConfig.description,
  url: siteConfig.url,
  logo: `${siteConfig.url}/logo.png`,
  sameAs: [
    siteConfig.links.twitter,
    siteConfig.links.github,
    siteConfig.links.discord,
  ],
  contactPoint: {
    '@type': 'ContactPoint',
    email: 'hola@codedungeon.es',
    contactType: 'Customer Service',
    availableLanguage: ['Spanish', 'English'],
  },
};

export const jsonLdCourse = (course: {
  name: string;
  description: string;
  provider: string;
  duration: string;
  price?: number;
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Course',
  name: course.name,
  description: course.description,
  provider: {
    '@type': 'Organization',
    name: course.provider,
    sameAs: siteConfig.url,
  },
  timeRequired: course.duration,
  offers: course.price
    ? {
        '@type': 'Offer',
        price: course.price,
        priceCurrency: 'EUR',
      }
    : undefined,
});
