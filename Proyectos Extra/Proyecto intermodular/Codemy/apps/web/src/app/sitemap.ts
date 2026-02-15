/**
 * Sitemap Generator
 * Genera sitemap.xml dinámico para SEO
 */

import { MetadataRoute } from 'next';
import { FREE_COURSE } from '@/data/free-course';

const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://codedungeon.es';

export default function sitemap(): MetadataRoute.Sitemap {
  const routes = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 1,
    },
    {
      url: `${baseUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    },
    {
      url: `${baseUrl}/auth/signup`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.8,
    },
    {
      url: `${baseUrl}/auth/login`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    },
  ];

  // Añadir lecciones del curso gratuito
  const lessonRoutes = FREE_COURSE.lessons.map((lesson) => ({
    url: `${baseUrl}/course/free/${lesson.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [...routes, ...lessonRoutes];
}
