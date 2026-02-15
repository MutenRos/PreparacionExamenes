// Loader dinámico de contenido de lecciones para optimizar performance
import { lessonCache } from './performance';

// Mapa de imports dinámicos
const contentLoaders: Record<string, () => Promise<any>> = {
  // Cursos de fundamentos (markdown puro)
  'fundamentals': () => import('@/data/courses/fundamentals').then(m => {
    const lessons: any = {};
    m.fundamentals.lessons.forEach((lesson: any) => {
      lessons[lesson.id] = {
        title: lesson.title,
        duration: '30 min',
        xp: 50,
        content: lesson.content,
      };
    });
    return lessons;
  }),
  'intro-programacion': () => import('@/data/courses/intro-programacion').then(m => {
    const lessons: any = {};
    m.introProgramacion.lessons.forEach((lesson: any) => {
      lessons[lesson.id] = {
        title: lesson.title,
        duration: '20 min',
        xp: 30,
        content: lesson.content,
      };
    });
    return lessons;
  }),
  
  // Python - Cursos básicos y avanzados
  'py-intro': () => import('@/data/lessons-content-py-intro').then(m => m.default),
  'py-variables': () => import('@/data/lessons-content-py-variables').then(m => m.default),
  'py-control': () => import('@/data/lessons-content-py-control').then(m => m.default),
  'py-functions': () => import('@/data/lessons-content-functions').then(m => m.default),
  'py-classes': () => import('@/data/lessons-content-classes').then(m => m.default),
  'py-files': () => import('@/data/lessons-content-files').then(m => m.default),
  'py-lists': () => import('@/data/lessons-content-lists').then(m => m.default),
  'py-dicts': () => import('@/data/lessons-content-dicts').then(m => m.default),
  'py-modules': () => import('@/data/lessons-content-modules').then(m => m.default),
  'py-web': () => import('@/data/lessons-content-web').then(m => m.default),
  'py-django': () => import('@/data/lessons-content-python-django').then(m => m.default),
  'py-flask': () => import('@/data/lessons-content-python-flask').then(m => m.default),

  // JavaScript & TypeScript
  'typescript': () => import('@/data/lessons-content-typescript').then(m => m.default),
  'js-intro': () => import('@/data/lessons-content-js-intro').then(m => m.default),
  'js-dom': () => import('@/data/lessons-content-js-dom').then(m => m.default),
  'js-async': () => import('@/data/lessons-content-js-async').then(m => m.default),
  'js-es6': () => import('@/data/lessons-content-js-es6').then(m => m.js_es6Content),
  'js-advanced': () => import('@/data/lessons-content-javascript').then(m => m.default), // Alias
  'javascript': () => import('@/data/lessons-content-javascript').then(m => m.default),
  'js-testing': () => import('@/data/lessons-content-testing-js').then(m => m.default),

  // Web
  'web-html': () => import('@/data/lessons-content-html').then(m => m.default),
  'web-css': () => import('@/data/lessons-content-css').then(m => m.default),
  'web-flexbox': () => import('@/data/lessons-content-web-flexbox').then(m => m.default),
  'web-responsive': () => import('@/data/lessons-content-web-responsive').then(m => m.default),

  // React & Frontend Frameworks
  'react': () => import('@/data/lessons-content-react').then(m => m.default),
  'nextjs-intro': () => import('@/data/lessons-content-nextjs-intro').then(m => m.default),
  'nextjs': () => import('@/data/lessons-content-nextjs-intro').then(m => m.default), // Alias

  // Backend & Databases
  'nodejs': () => import('@/data/lessons-content-nodejs').then(m => m.default),
  'sql-intro': () => import('@/data/lessons-content-sql-intro').then(m => m.default),
  'sql-queries': () => import('@/data/lessons-content-sql-intro').then(m => m.default), // Alias - TODO: crear curso avanzado
  'mongodb': () => import('@/data/lessons-content-mongodb').then(m => m.default),
  'rest-api': () => import('@/data/lessons-content-rest-api').then(m => m.default),
  'graphql': () => import('@/data/lessons-content-graphql').then(m => m.default),

  // DevOps & Tools
  'git-intro': () => import('@/data/lessons-content-git-intro').then(m => m.default),
  'git': () => import('@/data/lessons-content-git-intro').then(m => m.default), // Alias
  'docker-intro': () => import('@/data/lessons-content-docker-intro').then(m => m.default),
  'docker': () => import('@/data/lessons-content-docker-intro').then(m => m.default), // Alias
  'linux': () => import('@/data/lessons-content-linux').then(m => m.default),
  
  // Arduino & Hardware
  'arduino-intro': () => import('@/data/lessons-content-arduino-intro').then(m => m.default),

  // C++
  'cpp-intro': () => import('@/data/lessons-content-cpp-intro').then(m => m.default),
  'cpp-oop': () => import('@/data/lessons-content-cpp-oop').then(m => m.default),
  'cpp-stl': () => import('@/data/lessons-content-cpp-stl').then(m => m.default),
  'cpp-memory': () => import('@/data/lessons-content-cpp-memory').then(m => m.default),
  'cpp-advanced': () => import('@/data/lessons-content-cpp-advanced').then(m => m.default),
  'cpp-fileio': () => import('@/data/lessons-content-cpp-fileio').then(m => m.default),
  'cpp-concurrency': () => import('@/data/lessons-content-cpp-concurrency').then(m => m.default),
  'cpp-networking': () => import('@/data/lessons-content-cpp-networking').then(m => m.default),
  'cpp-databases': () => import('@/data/lessons-content-cpp-databases').then(m => m.default),
  'cpp-game-engine': () => import('@/data/lessons-content-cpp-game-engine').then(m => m.default),

  // Java
  'java-intro': () => import('@/data/lessons-content-java-intro').then(m => m.default),
  'java-oop': () => import('@/data/lessons-content-java-oop').then(m => m.default),
  'java-collections': () => import('@/data/lessons-content-java-collections').then(m => m.default),
  'java-exceptions': () => import('@/data/lessons-content-java-exceptions').then(m => m.default),
  'java-fileio': () => import('@/data/lessons-content-java-fileio').then(m => m.default),
  'java-threads': () => import('@/data/lessons-content-java-threads').then(m => m.default),
  'java-jdbc': () => import('@/data/lessons-content-java-jdbc').then(m => m.default),
  'java-spring': () => import('@/data/lessons-content-java-spring').then(m => m.default),

  // DAM (Desarrollo de Aplicaciones Multiplataforma) - 1º
  'dam-sistemas': () => import('@/data/lessons-content-dam-sistemas').then(m => m.default),
  'dam-bbdd': () => import('@/data/lessons-content-dam-bbdd').then(m => m.default),
  'dam-programacion': () => import('@/data/lessons-content-dam-programacion').then(m => m.default),
  'dam-lenguajes-marcas': () => import('@/data/lessons-content-dam-lenguajes-marcas').then(m => m.default),
  'dam-entornos': () => import('@/data/lessons-content-dam-entornos').then(m => m.default),

  // DAM - 2º
  'dam-acceso-datos': () => import('@/data/lessons-content-dam-acceso-datos').then(m => m.default),
  'dam-interfaces': () => import('@/data/lessons-content-dam-interfaces').then(m => m.default),
  'dam-multimedia': () => import('@/data/lessons-content-dam-multimedia').then(m => m.default),
  'dam-servicios': () => import('@/data/lessons-content-dam-servicios').then(m => m.default),
  'dam-sge': () => import('@/data/lessons-content-dam-sge').then(m => m.default),

  // SMR (Sistemas Microinformáticos y Redes) - 1º
  'smr-montaje': () => import('@/data/lessons-content-smr-montaje').then(m => m.default),
  'smr-ofimatica': () => import('@/data/lessons-content-smr-ofimatica').then(m => m.default),
  'smr-redes': () => import('@/data/lessons-content-smr-redes').then(m => m.default),
  'smr-so-mono': () => import('@/data/lessons-content-smr-so-mono').then(m => m.default),
  'smr-so-red': () => import('@/data/lessons-content-smr-so-red').then(m => m.default),

  // SMR - 2º
  'smr-seguridad': () => import('@/data/lessons-content-smr-seguridad').then(m => m.default),
  'smr-servicios-red': () => import('@/data/lessons-content-smr-servicios-red').then(m => m.default),
  'smr-web': () => import('@/data/lessons-content-smr-web').then(m => m.default),
  'smr-bbdd-gestion': () => import('@/data/lessons-content-smr-bbdd-gestion').then(m => m.default),

  // Web Development (Avanzado)
  'web-cliente': () => import('@/data/lessons-content-web-cliente').then(m => m.default),
  'web-servidor': () => import('@/data/lessons-content-web-servidor').then(m => m.default),
  'web-despliegue': () => import('@/data/lessons-content-web-despliegue').then(m => m.default),
  'web-diseno': () => import('@/data/lessons-content-web-diseno').then(m => m.default),
  'web-avanzado': () => import('@/data/lessons-content-web-avanzado').then(m => m.default),

  // Arduino/Hardware (adicionales)
  'arduino-sensors': () => import('@/data/lessons-content-arduino-sensors').then(m => m.default),
  'arduino-actuators': () => import('@/data/lessons-content-arduino-actuators').then(m => m.default),

  // DevOps (adicionales)
  'kubernetes': () => import('@/data/lessons-content-kubernetes').then(m => m.default),
  'cicd': () => import('@/data/lessons-content-cicd').then(m => m.default),

  // Backend/Mobile
  'express': () => import('@/data/lessons-content-express').then(m => m.default),
  'react-native': () => import('@/data/lessons-content-react-native').then(m => m.default),
  'flutter': () => import('@/data/lessons-content-flutter').then(m => m.default),

  // Databases (adicionales)
  'postgresql': () => import('@/data/lessons-content-postgresql').then(m => m.default),

  // Data Science
  'numpy': () => import('@/data/lessons-content-numpy').then(m => m.default),
  'pandas': () => import('@/data/lessons-content-pandas').then(m => m.default),
  'matplotlib': () => import('@/data/lessons-content-matplotlib').then(m => m.default),
  'scikit-learn': () => import('@/data/lessons-content-scikit-learn').then(m => m.default),

  // Cloud
  'aws': () => import('@/data/lessons-content-aws').then(m => m.default),
  'azure': () => import('@/data/lessons-content-azure').then(m => m.default),
  'gcp': () => import('@/data/lessons-content-gcp').then(m => m.default),

  // Security
  'security': () => import('@/data/lessons-content-security').then(m => m.default),
  'pentesting': () => import('@/data/lessons-content-pentesting').then(m => m.default),

  // IoT/Robotics
  'iot': () => import('@/data/lessons-content-iot').then(m => m.default),
  'esp32': () => import('@/data/lessons-content-esp32').then(m => m.default),
  'robotics': () => import('@/data/lessons-content-robotics').then(m => m.default),
  'ros': () => import('@/data/lessons-content-ros').then(m => m.default),

  // Game Development
  'unity': () => import('@/data/lessons-content-unity').then(m => m.default),
  'godot': () => import('@/data/lessons-content-godot').then(m => m.default),

  // Blockchain
  'blockchain': () => import('@/data/lessons-content-blockchain').then(m => m.default),
  'web3': () => import('@/data/lessons-content-web3').then(m => m.default),

  // AI/ML
  'tensorflow': () => import('@/data/lessons-content-tensorflow').then(m => m.default),
  'pytorch': () => import('@/data/lessons-content-pytorch').then(m => m.default),
  'computer-vision': () => import('@/data/lessons-content-computer-vision').then(m => m.default),
  'nlp': () => import('@/data/lessons-content-nlp').then(m => m.default),
  'llm': () => import('@/data/lessons-content-llm').then(m => m.default),
  'ai-robotics': () => import('@/data/lessons-content-ai-robotics').then(m => m.default),

  // Otros
  'ofimatica-intro': () => import('@/data/lessons-content-ofimatica-intro').then(m => m.default),
  'modelado3d-intro': () => import('@/data/lessons-content-modelado3d-intro').then(m => m.default),
  'impresion3d-intro': () => import('@/data/lessons-content-impresion3d-intro').then(m => m.default),
  'redes-seguras-intro': () => import('@/data/lessons-content-redes-seguras-intro').then(m => m.default),
  'domotica-intro': () => import('@/data/lessons-content-domotica-intro').then(m => m.default),
  'minecraft-intro': () => import('@/data/lessons-content-minecraft-intro').then(m => m.default),

  // Masters
  'master-ai': () => import('@/data/lessons-content-master-ai').then(m => m.default),
  'master-fullstack': () => import('@/data/lessons-content-master-fullstack').then(m => m.default),
  'master-mobile': () => import('@/data/lessons-content-master-mobile').then(m => m.default),
  'master-gamedev': () => import('@/data/lessons-content-master-gamedev').then(m => m.default),
  'master-robotics': () => import('@/data/lessons-content-master-robotics').then(m => m.default),
  'master-security': () => import('@/data/lessons-content-master-security').then(m => m.default),
  'master-cloud': () => import('@/data/lessons-content-master-cloud').then(m => m.default),

  // Bridges
  'bridge-oop': () => import('@/data/lessons-content-bridge-oop').then(m => m.default),
  'bridge-algorithms': () => import('@/data/lessons-content-bridge-algorithms').then(m => m.default),
};

export async function loadLessonContent(courseId: string) {
  // Verificar si está en caché
  const cached = lessonCache.get(courseId);
  if (cached) {
    return cached;
  }

  try {
    const loader = contentLoaders[courseId];
    
    if (!loader) {
      console.warn(`No content loader found for courseId: ${courseId}`);
      return null;
    }

    const content = await loader();
    
    // Guardar en caché
    if (content) {
      lessonCache.set(courseId, content);
    }
    
    return content;
  } catch (error) {
    console.error(`Error loading content for ${courseId}:`, error);
    return null;
  }
}

// Precargar contenido para la siguiente lección
export function preloadNextLesson(courseId: string) {
  const loader = contentLoaders[courseId];
  if (loader) {
    loader().then(content => {
      if (content) {
        lessonCache.set(courseId, content);
      }
    }).catch(() => {
      // Silently fail preload
    });
  }
}
