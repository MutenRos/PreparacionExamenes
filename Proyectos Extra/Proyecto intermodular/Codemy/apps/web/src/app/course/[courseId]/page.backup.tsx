'use client';

import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, BookOpen, Clock, Trophy, Target, CheckCircle, Circle, Lock, Play, Star, MessageSquare } from 'lucide-react';
import Forum from '@/components/Forum';

// Mock data - en producción vendría de Supabase
const coursesData = {
  'py-intro': {
    id: 'py-intro',
    title: 'Introducción a Python',
    description: 'Aprende los fundamentos de Python desde cero. Este curso te enseñará los conceptos básicos de programación y la sintaxis de Python.',
    icon: '🐍',
    xp: 200,
    level: 'Principiante',
    duration: '30 min',
    category: 'Python',
    objectives: [
      'Entender qué es Python y para qué se usa',
      'Instalar Python en tu computadora',
      'Escribir y ejecutar tu primer programa',
      'Usar la función print() para mostrar información',
    ],
    lessons: [
      { id: '1', title: '¿Qué es Python?', duration: '5 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Instalación', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Primer programa', duration: '8 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'print() básico', duration: '7 min', status: 'locked' as const, xp: 50 },
    ],
    progress: 0,
    studentsEnrolled: 1234,
  },
  'py-variables': {
    id: 'py-variables',
    title: 'Variables y Tipos de Datos',
    description: 'Domina el uso de variables y tipos de datos en Python. Aprenderás a almacenar y manipular diferentes tipos de información.',
    icon: '📦',
    xp: 250,
    level: 'Principiante',
    duration: '39 min',
    category: 'Python',
    objectives: [
      'Comprender qué son las variables y cómo usarlas',
      'Trabajar con números enteros y decimales',
      'Manipular cadenas de texto',
      'Usar valores booleanos en condiciones',
    ],
    lessons: [
      { id: '1', title: 'Qué es una variable', duration: '6 min', status: 'locked' as const, xp: 50 },
      { id: '2', title: 'Números enteros', duration: '8 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Números decimales', duration: '8 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Cadenas de texto', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Booleanos', duration: '7 min', status: 'locked' as const, xp: 50 },
    ],
    progress: 0,
    studentsEnrolled: 987,
  },
  'py-control': {
    id: 'py-control',
    title: 'Control de Flujo',
    description: 'Aprende a controlar el flujo de ejecución de tus programas con condicionales y bucles.',
    icon: '🔀',
    xp: 300,
    level: 'Principiante',
    duration: '58 min',
    category: 'Python',
    objectives: [
      'Usar condicionales if para tomar decisiones',
      'Implementar bucles while para repetir acciones',
      'Trabajar con bucles for para iterar',
      'Controlar bucles con break y continue',
    ],
    lessons: [
      { id: '1', title: 'Condicionales if', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '2', title: 'if-else', duration: '8 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'elif múltiple', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Bucle while', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Bucle for', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'break y continue', duration: '8 min', status: 'locked' as const, xp: 50 },
    ],
    progress: 0,
    studentsEnrolled: 856,
  },
  'py-functions': {
    id: 'py-functions',
    title: 'Funciones en Python',
    description: 'Aprende a crear funciones reutilizables. Basado en el contenido de Jose Vicente Carratalá (jocarsa/dam2526).',
    icon: '⚙️',
    xp: 350,
    level: 'Principiante',
    duration: '60 min',
    category: 'Python',
    objectives: [
      'Definir funciones con def',
      'Usar parámetros y argumentos',
      'Retornar valores con return',
      'Aplicar funciones en programas reales',
    ],
    lessons: [
      { id: '1', title: 'Qué es una función', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '2', title: 'Parámetros', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'return', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Parámetros por defecto', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Ámbito de variables', duration: '11 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Proyecto Final: Calculadora', duration: '15 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 645,
  },
  'py-classes': {
    id: 'py-classes',
    title: 'Programación Orientada a Objetos',
    description: 'Domina las clases y objetos en Python. Contenido adaptado del curso DAM de Jose Vicente Carratalá.',
    icon: '🏗️',
    xp: 400,
    level: 'Intermedio',
    duration: '60 min',
    category: 'Python',
    objectives: [
      'Entender qué es una clase y un objeto',
      'Crear clases con __init__',
      'Definir propiedades y métodos',
      'Instanciar y usar objetos',
    ],
    lessons: [
      { id: '1', title: 'Qué es una clase', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '2', title: 'Atributos', duration: '11 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Métodos', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: '__str__ y __repr__', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Encapsulación', duration: '11 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Proyecto Final: Sistema de Clientes', duration: '15 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 532,
  },
  'py-files': {
    id: 'py-files',
    title: 'Archivos y Persistencia',
    description: 'Aprende a leer y escribir archivos en Python. Basado en ejercicios del repositorio dam2526.',
    icon: '📁',
    xp: 300,
    level: 'Intermedio',
    duration: '72 min',
    category: 'Python',
    objectives: [
      'Abrir y cerrar archivos',
      'Leer contenido de archivos',
      'Escribir y agregar datos',
      'Trabajar con rutas y directorios',
    ],
    lessons: [
      { id: '1', title: 'Archivos de texto', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '2', title: 'Leer línea por línea', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Append (agregar)', duration: '9 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Trabajar con rutas', duration: '11 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Try-except con archivos', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Proyecto Final: Agenda de Contactos', duration: '18 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 423,
  },
  'sql-intro': {
    id: 'sql-intro',
    title: 'Introducción a SQL',
    description: 'Aprende los fundamentos de SQL y bases de datos relacionales desde cero.',
    icon: '🗄️',
    xp: 300,
    level: 'Principiante',
    duration: '65 min',
    category: 'SQL',
    objectives: [
      'Entender qué es SQL y para qué sirve',
      'Conocer los tipos de bases de datos',
      'Realizar consultas SELECT básicas',
      'Filtrar datos con WHERE',
    ],
    lessons: [
      { id: '1', title: '¿Qué es SQL?', duration: '8 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Bases de datos relacionales', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'SELECT básico', duration: '12 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'WHERE y filtros', duration: '15 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'ORDER BY y LIMIT', duration: '10 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Operadores lógicos', duration: '10 min', status: 'locked' as const, xp: 50 },
    ],
    progress: 0,
    studentsEnrolled: 892,
  },
  'minecraft-intro': {
    id: 'minecraft-intro',
    title: 'Mods de Minecraft',
    description: 'Aprende Java creando mods para Minecraft. Desde configurar Forge hasta publicar tu mod.',
    icon: '⛏️',
    xp: 500,
    level: 'Intermedio',
    duration: '3 horas',
    category: 'Java',
    objectives: [
      'Instalar Java JDK y configurar entorno',
      'Configurar Minecraft Forge para modding',
      'Crear tu primer bloque personalizado',
      'Programar items, herramientas y recetas',
    ],
    lessons: [
      { id: '1', title: '¿Qué son los mods?', duration: '15 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Instalar Java y el JDK', duration: '20 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Forge y tu primer mod', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Tu primer bloque', duration: '20 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Items y herramientas', duration: '20 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Texturas personalizadas', duration: '18 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Recetas de crafteo', duration: '15 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Mobs personalizados', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Eventos y mecánicas', duration: '20 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Publicar tu mod', duration: '12 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 756,
  },
  'domotica-intro': {
    id: 'domotica-intro',
    title: 'Domótica & Smart Home',
    description: 'Automatiza tu hogar con ESP32 y Arduino. Controla luces, sensores y dispositivos por WiFi.',
    icon: '🏠',
    xp: 600,
    level: 'Intermedio-Avanzado',
    duration: '5 horas',
    category: 'IoT',
    objectives: [
      'Programar dispositivos ESP32',
      'Crear redes de sensores IoT',
      'Desarrollar apps móviles con Blynk',
      'Integrar con Alexa y Google Home',
    ],
    lessons: [
      { id: '1', title: '¿Qué es la domótica?', duration: '15 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Tu primer ESP32', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'Controlar LEDs por WiFi', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Sensores de temperatura', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Detector de movimiento', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'App móvil con Blynk', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Automatizaciones inteligentes', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'Asistente de voz', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Ahorro energético', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Tu sistema completo', duration: '45 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 432,
  },
  'impresion3d-intro': {
    id: 'impresion3d-intro',
    title: 'Impresión 3D',
    description: 'De la idea al objeto físico. Aprende diseño 3D, slicing y fabricación con impresoras 3D.',
    icon: '🖨️',
    xp: 500,
    level: 'Todos los niveles',
    duration: '6 horas',
    category: '3D',
    objectives: [
      'Diseñar modelos 3D desde cero',
      'Dominar software CAD profesional',
      'Optimizar impresiones para calidad',
      'Crear y vender tus diseños',
    ],
    lessons: [
      { id: '1', title: '¿Qué es la impresión 3D?', duration: '20 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Tu primera impresora', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Diseño 3D con Tinkercad', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Slicing con Cura', duration: '35 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Parámetros de impresión', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Modelado avanzado: Fusion 360', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Diseño orgánico con Blender', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Impresión multimaterial', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Post-procesado profesional', duration: '35 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyectos y venta online', duration: '25 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 612,
  },
  'redes-seguras-intro': {
    id: 'redes-seguras-intro',
    title: 'Redes Sociales Seguras',
    description: 'Protege tu privacidad online. Configuración, ciberseguridad y uso responsable de redes sociales.',
    icon: '🛡️',
    xp: 400,
    level: 'Para todos',
    duration: '4 horas',
    category: 'Digital',
    objectives: [
      'Configurar privacidad en todas tus redes',
      'Detectar amenazas y estafas online',
      'Proteger tu información personal',
      'Actuar ante situaciones de riesgo',
    ],
    lessons: [
      { id: '1', title: 'Tu huella digital', duration: '20 min', status: 'available' as const, xp: 40 },
      { id: '2', title: 'Configuración de privacidad', duration: '30 min', status: 'locked' as const, xp: 40 },
      { id: '3', title: 'Contraseñas seguras', duration: '25 min', status: 'locked' as const, xp: 40 },
      { id: '4', title: 'Detectar fake news', duration: '30 min', status: 'locked' as const, xp: 40 },
      { id: '5', title: 'Phishing y estafas', duration: '25 min', status: 'locked' as const, xp: 40 },
      { id: '6', title: 'Ciberbullying y acoso', duration: '35 min', status: 'locked' as const, xp: 40 },
      { id: '7', title: 'Sexting y sextorsión', duration: '30 min', status: 'locked' as const, xp: 40 },
      { id: '8', title: 'Tu reputación online', duration: '25 min', status: 'locked' as const, xp: 40 },
      { id: '9', title: 'Desconexión digital', duration: '30 min', status: 'locked' as const, xp: 40 },
      { id: '10', title: 'Tu plan de seguridad', duration: '20 min', status: 'locked' as const, xp: 60 },
    ],
    progress: 0,
    studentsEnrolled: 1123,
  },
  'ofimatica-intro': {
    id: 'ofimatica-intro',
    title: 'Ofimática Profesional',
    description: 'Excel avanzado, PowerPoint impactante y automatización. Habilidades esenciales para el trabajo.',
    icon: '📊',
    xp: 700,
    level: 'Básico a Avanzado',
    duration: '7 horas',
    category: 'Office',
    objectives: [
      'Dominar Excel desde básico hasta avanzado',
      'Crear presentaciones profesionales',
      'Automatizar tareas con macros',
      'Visualizar datos con dashboards',
    ],
    lessons: [
      { id: '1', title: 'Procesador de textos profesional', duration: '40 min', status: 'available' as const, xp: 70 },
      { id: '2', title: 'Excel nivel básico', duration: '45 min', status: 'locked' as const, xp: 70 },
      { id: '3', title: 'Excel nivel intermedio', duration: '50 min', status: 'locked' as const, xp: 70 },
      { id: '4', title: 'Excel nivel avanzado', duration: '60 min', status: 'locked' as const, xp: 70 },
      { id: '5', title: 'Presentaciones impactantes', duration: '35 min', status: 'locked' as const, xp: 70 },
      { id: '6', title: 'Google Workspace completo', duration: '40 min', status: 'locked' as const, xp: 70 },
      { id: '7', title: 'Automatización con macros', duration: '45 min', status: 'locked' as const, xp: 70 },
      { id: '8', title: 'Bases de datos con Access', duration: '50 min', status: 'locked' as const, xp: 70 },
      { id: '9', title: 'Visualización de datos', duration: '55 min', status: 'locked' as const, xp: 70 },
      { id: '10', title: 'Productividad y atajos', duration: '30 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 2145,
  },
  'raspberry-server-intro': {
    id: 'raspberry-server-intro',
    title: 'Servidor Casero con Raspberry Pi',
    description: 'Crea tu propio servidor doméstico. Web hosting, NAS, VPN, media server y más con Raspberry Pi.',
    icon: '🥧',
    xp: 600,
    level: 'Intermedio',
    duration: '5 horas',
    category: 'Linux',
    objectives: [
      'Instalar y configurar Raspberry Pi OS',
      'Crear servidores web, NAS y multimedia',
      'Configurar VPN y seguridad de red',
      'Administrar servicios con Docker',
    ],
    lessons: [
      { id: '1', title: '¿Qué es una Raspberry Pi?', duration: '15 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Instalación de Raspberry Pi OS', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'Configuración inicial y SSH', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Servidor web con Apache/Nginx', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Servidor de archivos (NAS)', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Servidor multimedia (Plex)', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Pi-hole: Bloquea anuncios', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'VPN casera con PiVPN', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Monitorización y backups', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Docker y contenedores', duration: '40 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 845,
  },
  'discord-bot-intro': {
    id: 'discord-bot-intro',
    title: 'Crea tu Bot de Discord',
    description: 'Programa bots de Discord con Node.js. Moderación, música, mini-juegos y más.',
    icon: '🤖',
    xp: 700,
    level: 'Intermedio',
    duration: '6 horas',
    category: 'JavaScript',
    objectives: [
      'Crear bots de Discord desde cero con Node.js',
      'Implementar comandos slash, eventos y moderación',
      'Construir sistemas de música, economía y mini-juegos',
      'Desplegar tu bot 24/7 en la nube',
    ],
    lessons: [
      { id: '1', title: '¿Qué es un bot de Discord?', duration: '15 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Configura Node.js y Discord.js', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'Tu primer bot: ¡Hola Mundo!', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Comandos slash (/) modernos', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Gestión de eventos', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Embeds y mensajes ricos', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Sistema de moderación', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'Bot de música', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Base de datos con MongoDB', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Mini-juegos y economía', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '11', title: 'Hosting 24/7', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '12', title: 'Bot verificado y avanzado', duration: '35 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1289,
  },
  'streaming-intro': {
    id: 'streaming-intro',
    title: 'Streaming Profesional',
    description: 'Configuración de OBS, overlays personalizados, bots, monetización y crecimiento en Twitch/YouTube.',
    icon: '🎥',
    xp: 650,
    level: 'Principiante-Intermedio',
    duration: '5.5 horas',
    category: 'Content',
    objectives: [
      'Configurar OBS Studio para streaming profesional',
      'Crear overlays, escenas y alertas personalizadas',
      'Monetizar tu canal desde el día uno',
      'Aumentar tu audiencia con estrategias probadas',
    ],
    lessons: [
      { id: '1', title: 'El mundo del streaming', duration: '15 min', status: 'available' as const, xp: 55 },
      { id: '2', title: 'Hardware necesario', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '3', title: 'Instalación de OBS Studio', duration: '20 min', status: 'locked' as const, xp: 55 },
      { id: '4', title: 'Escenas y transiciones', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '5', title: 'Overlays y diseño de stream', duration: '35 min', status: 'locked' as const, xp: 55 },
      { id: '6', title: 'Audio profesional', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '7', title: 'Bots de Twitch', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '8', title: 'Engagement de audiencia', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '9', title: 'Configuración de bitrate y calidad', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '10', title: 'Monetización', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '11', title: 'Networking y crecimiento', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '12', title: 'Grabación y clips', duration: '30 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 967,
  },
  'hacking-wifi-intro': {
    id: 'hacking-wifi-intro',
    title: 'Hacking Ético WiFi',
    description: 'Seguridad de redes con Kali Linux. Aprende cómo funcionan los ataques WiFi para protegerte.',
    icon: '🔐',
    xp: 700,
    level: 'Avanzado',
    duration: '6 horas',
    category: 'Security',
    objectives: [
      'Entender cómo funcionan los ataques a redes WiFi',
      'Usar herramientas profesionales (Kali, Wireshark, Aircrack)',
      'Realizar auditorías de seguridad en TU propia red',
      'Protegerte contra ataques comunes',
    ],
    lessons: [
      { id: '1', title: '¿Qué es el hacking ético?', duration: '15 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Legalidad y ética', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'Instala Kali Linux', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Fundamentos de redes', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Escaneo de redes con Nmap', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Análisis WiFi con Wireshark', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Ataques WEP y WPA/WPA2', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'Evil Twin y Phishing WiFi', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Sniffing y Man-in-the-Middle', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Protección y mitigación', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '11', title: 'WPA3 y redes modernas', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '12', title: 'Proyecto final: Auditoría completa', duration: '45 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 534,
  },
  'nfts-intro': {
    id: 'nfts-intro',
    title: 'Crea y Vende NFTs',
    description: 'Aprende blockchain, crea NFTs en OpenSea/Rarible, colecciones generativas y monetización con royalties.',
    icon: '🎨',
    xp: 700,
    level: 'Intermedio',
    duration: '6 horas',
    category: 'Blockchain',
    objectives: [
      'Crear y vender NFTs en OpenSea y Rarible',
      'Entender blockchain, wallets y smart contracts',
      'Generar colecciones de 10k+ NFTs automáticamente',
      'Monetizar con royalties en cada reventa',
    ],
    lessons: [
      { id: '1', title: '¿Qué son los NFTs?', duration: '20 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Wallets: MetaMask y más', duration: '15 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'Ethereum y gas fees', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Crea tu arte digital', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'OpenSea: Tu primera colección', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Rarible y otras marketplaces', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Marketing de NFTs', duration: '35 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'Smart contracts básicos', duration: '45 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Royalties y monetización', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Rareza y colecciones generativas', duration: '50 min', status: 'locked' as const, xp: 60 },
      { id: '11', title: 'Polygon y blockchains baratas', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '12', title: 'Vende tu primera colección', duration: '30 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 823,
  },
  'davinci-intro': {
    id: 'davinci-intro',
    title: 'Edición de Vídeo con DaVinci Resolve',
    description: 'Edición profesional, color grading, efectos visuales y exportación 4K con DaVinci Resolve (gratis).',
    icon: '🎬',
    xp: 650,
    level: 'Intermedio',
    duration: '5.5 horas',
    category: 'Video',
    objectives: [
      'Dominar la interfaz de DaVinci Resolve',
      'Editar vídeos con cortes, transiciones y efectos',
      'Color grading profesional para mood cinematográfico',
      'Exportar en múltiples formatos para YouTube/redes',
    ],
    lessons: [
      { id: '1', title: 'Introducción a DaVinci Resolve', duration: '15 min', status: 'available' as const, xp: 55 },
      { id: '2', title: 'Interfaz y configuración inicial', duration: '20 min', status: 'locked' as const, xp: 55 },
      { id: '3', title: 'Importación y organización', duration: '15 min', status: 'locked' as const, xp: 55 },
      { id: '4', title: 'Edición básica y timeline', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '5', title: 'Transiciones y efectos', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '6', title: 'Audio profesional', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '7', title: 'Títulos y gráficos', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '8', title: 'Color grading esencial', duration: '40 min', status: 'locked' as const, xp: 55 },
      { id: '9', title: 'Color grading avanzado', duration: '35 min', status: 'locked' as const, xp: 55 },
      { id: '10', title: 'Efectos visuales (Fusion)', duration: '40 min', status: 'locked' as const, xp: 55 },
      { id: '11', title: 'Exportación y formatos', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '12', title: 'Proyecto final completo', duration: '50 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1456,
  },
  'fotografia-movil-intro': {
    id: 'fotografia-movil-intro',
    title: 'Fotografía con Móvil',
    description: 'Composición, iluminación, edición y monetización. Conviértete en fotógrafo profesional con tu smartphone.',
    icon: '📱',
    xp: 550,
    level: 'Principiante',
    duration: '4.5 horas',
    category: 'Photography',
    objectives: [
      'Dominar composición, regla de tercios y perspectiva',
      'Editar fotos profesionalmente con apps móviles',
      'Crear contenido para Instagram y redes sociales',
      'Monetizar vendiendo fotos en plataformas stock',
    ],
    lessons: [
      { id: '1', title: 'Fundamentos de fotografía móvil', duration: '15 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Configuración de cámara', duration: '20 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Composición y regla de tercios', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Iluminación natural', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Edición con Lightroom Mobile', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Edición con Snapseed', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Retratos y personas', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Paisajes y arquitectura', duration: '25 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Instagram y engagement', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Vender fotos online', duration: '35 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1834,
  },
  'ml-intro': {
    id: 'ml-intro',
    title: 'Machine Learning Práctico',
    description: 'Python, TensorFlow, reconocimiento de imágenes, chatbots IA y proyectos reales de Machine Learning.',
    icon: '🤖',
    xp: 800,
    level: 'Avanzado',
    duration: '8 horas',
    category: 'AI',
    objectives: [
      'Fundamentos de Machine Learning y redes neuronales',
      'Crear modelos con TensorFlow y Keras',
      'Reconocimiento de imágenes y clasificación',
      'Chatbots inteligentes con procesamiento de lenguaje',
    ],
    lessons: [
      { id: '1', title: '¿Qué es Machine Learning?', duration: '20 min', status: 'available' as const, xp: 70 },
      { id: '2', title: 'Python para ML: NumPy y Pandas', duration: '30 min', status: 'locked' as const, xp: 70 },
      { id: '3', title: 'Tu primera red neuronal', duration: '35 min', status: 'locked' as const, xp: 70 },
      { id: '4', title: 'TensorFlow y Keras', duration: '40 min', status: 'locked' as const, xp: 70 },
      { id: '5', title: 'Clasificación de imágenes', duration: '45 min', status: 'locked' as const, xp: 70 },
      { id: '6', title: 'Transfer Learning', duration: '40 min', status: 'locked' as const, xp: 70 },
      { id: '7', title: 'Procesamiento de lenguaje (NLP)', duration: '45 min', status: 'locked' as const, xp: 70 },
      { id: '8', title: 'Chatbot inteligente', duration: '50 min', status: 'locked' as const, xp: 70 },
      { id: '9', title: 'Detección de objetos', duration: '45 min', status: 'locked' as const, xp: 70 },
      { id: '10', title: 'Proyecto final: IA completa', duration: '60 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 623,
  },
  'pc-gaming-intro': {
    id: 'pc-gaming-intro',
    title: 'Construye tu PC Gaming',
    description: 'Aprende a elegir componentes, montaje paso a paso, BIOS, drivers, overclocking y optimización.',
    icon: '🖥️',
    xp: 600,
    level: 'Principiante-Intermedio',
    duration: '5 horas',
    category: 'Hardware',
    objectives: [
      'Seleccionar componentes compatibles según presupuesto',
      'Ensamblar un PC gaming desde cero',
      'Instalar sistema operativo y drivers',
      'Optimizar rendimiento y overclocking básico',
    ],
    lessons: [
      { id: '1', title: 'Componentes esenciales', duration: '20 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'CPU: Intel vs AMD', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: 'GPU: Nvidia vs AMD', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'Placa base y RAM', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Almacenamiento: SSD NVMe', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Fuente de alimentación', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Montaje paso a paso', duration: '40 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'BIOS y primer arranque', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Windows y drivers', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Overclocking y RGB', duration: '35 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1923,
  },
  'python-automation-intro': {
    id: 'python-automation-intro',
    title: 'Automatiza tu Vida con Python',
    description: 'Scripts útiles, bots de Telegram, web scraping, automatización de tareas y productividad.',
    icon: '⚙️',
    xp: 650,
    level: 'Intermedio',
    duration: '5.5 horas',
    category: 'Python',
    objectives: [
      'Crear scripts Python para automatizar tareas diarias',
      'Desarrollar bots de Telegram funcionales',
      'Web scraping para extraer datos automáticamente',
      'Automatizar emails, archivos y procesos repetitivos',
    ],
    lessons: [
      { id: '1', title: 'Por qué automatizar', duration: '15 min', status: 'available' as const, xp: 55 },
      { id: '2', title: 'Automatización de archivos', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '3', title: 'Envío automático de emails', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '4', title: 'Web scraping con BeautifulSoup', duration: '35 min', status: 'locked' as const, xp: 55 },
      { id: '5', title: 'Selenium: Automatiza navegadores', duration: '40 min', status: 'locked' as const, xp: 55 },
      { id: '6', title: 'Bot de Telegram básico', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '7', title: 'Bot de Telegram avanzado', duration: '35 min', status: 'locked' as const, xp: 55 },
      { id: '8', title: 'Automatiza Excel y CSV', duration: '30 min', status: 'locked' as const, xp: 55 },
      { id: '9', title: 'Tareas programadas', duration: '25 min', status: 'locked' as const, xp: 55 },
      { id: '10', title: 'Dashboard de productividad', duration: '40 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1267,
  },
  'flstudio-intro': {
    id: 'flstudio-intro',
    title: 'Música Electrónica con FL Studio',
    description: 'Producción musical, beats, síntesis, mezcla, mastering y publicación en Spotify.',
    icon: '🎵',
    xp: 750,
    level: 'Principiante-Intermedio',
    duration: '7 horas',
    category: 'Music',
    objectives: [
      'Dominar la interfaz y workflow de FL Studio',
      'Crear beats, melodías y arreglos completos',
      'Mezcla y mastering profesional',
      'Publicar tu música en Spotify y plataformas',
    ],
    lessons: [
      { id: '1', title: 'Introducción a FL Studio', duration: '20 min', status: 'available' as const, xp: 65 },
      { id: '2', title: 'Interfaz y configuración', duration: '25 min', status: 'locked' as const, xp: 65 },
      { id: '3', title: 'Tu primer beat', duration: '30 min', status: 'locked' as const, xp: 65 },
      { id: '4', title: 'Piano roll y melodías', duration: '35 min', status: 'locked' as const, xp: 65 },
      { id: '5', title: 'Síntesis y sonidos', duration: '40 min', status: 'locked' as const, xp: 65 },
      { id: '6', title: 'Samples y librerías', duration: '30 min', status: 'locked' as const, xp: 65 },
      { id: '7', title: 'Arreglos y estructura', duration: '35 min', status: 'locked' as const, xp: 65 },
      { id: '8', title: 'Mezcla profesional', duration: '45 min', status: 'locked' as const, xp: 65 },
      { id: '9', title: 'Mastering y exportación', duration: '40 min', status: 'locked' as const, xp: 65 },
      { id: '10', title: 'Publicar en Spotify', duration: '35 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 892,
  },
  'robotica-avanzada-intro': {
    id: 'robotica-avanzada-intro',
    title: 'Robótica Arduino Avanzada',
    description: 'Brazos robóticos, drones DIY, visión artificial con IA y proyectos avanzados con Arduino.',
    icon: '🦾',
    xp: 800,
    level: 'Avanzado',
    duration: '8 horas',
    category: 'IoT',
    objectives: [
      'Construir brazos robóticos con servomotores',
      'Crear drones funcionales desde cero',
      'Integrar cámaras y visión artificial',
      'Combinar hardware con Machine Learning',
    ],
    lessons: [
      { id: '1', title: 'Robótica avanzada con Arduino', duration: '20 min', status: 'available' as const, xp: 80 },
      { id: '2', title: 'Servomotores y control preciso', duration: '30 min', status: 'locked' as const, xp: 80 },
      { id: '3', title: 'Brazo robótico de 4 ejes', duration: '45 min', status: 'locked' as const, xp: 80 },
      { id: '4', title: 'Control con joystick', duration: '35 min', status: 'locked' as const, xp: 80 },
      { id: '5', title: 'Drones: Fundamentos de vuelo', duration: '40 min', status: 'locked' as const, xp: 80 },
      { id: '6', title: 'Construye tu propio drone', duration: '50 min', status: 'locked' as const, xp: 80 },
      { id: '7', title: 'Cámara y FPV', duration: '40 min', status: 'locked' as const, xp: 80 },
      { id: '8', title: 'Visión artificial básica', duration: '45 min', status: 'locked' as const, xp: 80 },
      { id: '9', title: 'IA + Hardware (TinyML)', duration: '50 min', status: 'locked' as const, xp: 80 },
      { id: '10', title: 'Proyecto final integrado', duration: '60 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 378,
  },
  'ciberseguridad-personal-intro': {
    id: 'ciberseguridad-personal-intro',
    title: 'Ciberseguridad Personal',
    description: 'Anonimato online, VPN, encriptación, gestores de contraseñas y privacidad total en internet.',
    icon: '🛡️',
    xp: 600,
    level: 'Intermedio',
    duration: '5 horas',
    category: 'Security',
    objectives: [
      'Configurar VPN y navegación anónima (Tor)',
      'Usar gestores de contraseñas y 2FA correctamente',
      'Encriptar archivos y comunicaciones',
      'Proteger tu identidad digital completamente',
    ],
    lessons: [
      { id: '1', title: 'Tu huella digital', duration: '15 min', status: 'available' as const, xp: 60 },
      { id: '2', title: 'Gestores de contraseñas', duration: '20 min', status: 'locked' as const, xp: 60 },
      { id: '3', title: '2FA y autenticación', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '4', title: 'VPN: Qué son y cómo usarlas', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '5', title: 'Navegación anónima con Tor', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '6', title: 'Encriptación de archivos', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '7', title: 'Comunicación segura', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '8', title: 'Privacidad en redes sociales', duration: '25 min', status: 'locked' as const, xp: 60 },
      { id: '9', title: 'Protección de datos personales', duration: '30 min', status: 'locked' as const, xp: 60 },
      { id: '10', title: 'Plan de seguridad completo', duration: '40 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1145,
  },
  // ===== CURSOS DAM - PRIMER AÑO =====
  'dam-sistemas': {
    id: 'dam-sistemas',
    title: 'Sistemas Informáticos',
    description: 'Fundamentos de sistemas informáticos, arquitectura de computadores, sistemas operativos y redes básicas.',
    icon: '💻',
    xp: 600,
    level: 'Principiante',
    duration: '8 horas',
    category: 'DAM',
    objectives: [
      'Comprender la arquitectura de computadores',
      'Dominar sistemas operativos Windows y Linux',
      'Gestionar redes locales básicas',
      'Administrar usuarios y permisos',
    ],
    lessons: [
      { id: '1', title: 'Arquitectura de computadores', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Componentes hardware', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Sistemas operativos: conceptos', duration: '35 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Windows: administración', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Linux: comandos básicos', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Linux: gestión de usuarios', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Redes: fundamentos', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'TCP/IP y configuración de red', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Virtualización con VirtualBox', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: Servidor Linux completo', duration: '60 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 892,
  },
  'dam-bbdd': {
    id: 'dam-bbdd',
    title: 'Bases de Datos',
    description: 'Diseño, implementación y gestión de bases de datos relacionales con SQL. MySQL, PostgreSQL y normalización.',
    icon: '🗄️',
    xp: 650,
    level: 'Intermedio',
    duration: '9 horas',
    category: 'DAM',
    objectives: [
      'Diseñar bases de datos relacionales',
      'Dominar SQL para consultas y manipulación',
      'Aplicar normalización de bases de datos',
      'Gestionar MySQL y PostgreSQL',
    ],
    lessons: [
      { id: '1', title: 'Introducción a bases de datos', duration: '30 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Modelo relacional', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'SQL: SELECT y consultas básicas', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'SQL: JOIN y relaciones', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'INSERT, UPDATE, DELETE', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Funciones agregadas y GROUP BY', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Normalización de datos', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Índices y optimización', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Transacciones y ACID', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: Sistema de gestión completo', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1245,
  },
  'dam-programacion': {
    id: 'dam-programacion',
    title: 'Programación',
    description: 'Fundamentos de programación con Java. Estructuras de datos, POO, patrones de diseño y desarrollo de aplicaciones.',
    icon: '☕',
    xp: 800,
    level: 'Intermedio',
    duration: '12 horas',
    category: 'DAM',
    objectives: [
      'Dominar la sintaxis de Java',
      'Aplicar programación orientada a objetos',
      'Usar colecciones y estructuras de datos',
      'Implementar patrones de diseño',
    ],
    lessons: [
      { id: '1', title: 'Introducción a Java', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Variables y tipos de datos', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Estructuras de control', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Arrays y matrices', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Clases y objetos', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Herencia y polimorfismo', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Interfaces y clases abstractas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Colecciones: ArrayList, HashMap', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Excepciones y manejo de errores', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Patrones de diseño y buenas prácticas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '11', title: 'Proyecto: Aplicación de gestión completa', duration: '90 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 1678,
  },
  'dam-lenguajes-marcas': {
    id: 'dam-lenguajes-marcas',
    title: 'Lenguajes de Marcas',
    description: 'HTML5, CSS3, XML, JSON y transformaciones XSLT. Gestión de información con lenguajes de marcado.',
    icon: '🏷️',
    xp: 500,
    level: 'Principiante',
    duration: '7 horas',
    category: 'DAM',
    objectives: [
      'Crear páginas web con HTML5 semántico',
      'Diseñar con CSS3 y layouts responsive',
      'Trabajar con XML y JSON',
      'Aplicar transformaciones XSLT',
    ],
    lessons: [
      { id: '1', title: 'HTML5: estructura y semántica', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Formularios y validación HTML5', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'CSS3: selectores y propiedades', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Flexbox y Grid Layout', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Responsive design', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'XML: sintaxis y estructura', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'JSON y APIs REST', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'XSLT: transformaciones', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Sitio web completo responsive', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 956,
  },
  'dam-entornos': {
    id: 'dam-entornos',
    title: 'Entornos de Desarrollo',
    description: 'Control de versiones con Git, IDEs, testing, debugging y metodologías ágiles para desarrollo profesional.',
    icon: '🛠️',
    xp: 450,
    level: 'Principiante',
    duration: '6 horas',
    category: 'DAM',
    objectives: [
      'Dominar Git y GitHub para control de versiones',
      'Usar IDEs profesionales (IntelliJ, VS Code)',
      'Aplicar debugging y testing',
      'Conocer metodologías ágiles (Scrum, Kanban)',
    ],
    lessons: [
      { id: '1', title: 'Introducción a Git', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Comandos básicos de Git', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Branches y merging', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'GitHub y colaboración', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'IDEs: IntelliJ y VS Code', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Debugging y breakpoints', duration: '35 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Unit testing con JUnit', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Metodologías ágiles: Scrum', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Workflow completo con Git', duration: '60 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 823,
  },
  // ===== CURSOS DAM - SEGUNDO AÑO =====
  'dam-acceso-datos': {
    id: 'dam-acceso-datos',
    title: 'Acceso a Datos',
    description: 'Persistencia de datos con JDBC, Hibernate, JPA y gestión de archivos. Conexión a bases de datos desde Java.',
    icon: '🔌',
    xp: 700,
    level: 'Avanzado',
    duration: '10 horas',
    category: 'DAM',
    objectives: [
      'Conectar aplicaciones Java con bases de datos',
      'Usar JDBC para consultas SQL',
      'Implementar ORM con Hibernate y JPA',
      'Gestionar archivos XML y JSON',
    ],
    lessons: [
      { id: '1', title: 'Introducción a JDBC', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Conexión y consultas con JDBC', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Prepared Statements', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Introducción a Hibernate', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Mapeo objeto-relacional', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'JPA y EntityManager', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Relaciones entre entidades', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Gestión de archivos XML', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Gestión de archivos JSON', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: CRUD completo con Hibernate', duration: '80 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 734,
  },
  'dam-interfaces': {
    id: 'dam-interfaces',
    title: 'Desarrollo de Interfaces',
    description: 'Diseño de interfaces gráficas con JavaFX, Swing y conceptos de UX/UI para aplicaciones de escritorio.',
    icon: '🎨',
    xp: 650,
    level: 'Intermedio',
    duration: '9 horas',
    category: 'DAM',
    objectives: [
      'Crear interfaces con JavaFX',
      'Aplicar conceptos de UX/UI',
      'Gestionar eventos y controladores',
      'Diseñar aplicaciones responsive',
    ],
    lessons: [
      { id: '1', title: 'Introducción a JavaFX', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Layouts y contenedores', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Controles básicos', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Eventos y manejadores', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'FXML y Scene Builder', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'CSS en JavaFX', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Tablas y listas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Principios de UX/UI', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Aplicación de escritorio completa', duration: '75 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 645,
  },
  'dam-multimedia': {
    id: 'dam-multimedia',
    title: 'Programación Multimedia y Móviles',
    description: 'Desarrollo de aplicaciones Android con Kotlin, gestión multimedia y diseño de apps móviles.',
    icon: '📱',
    xp: 750,
    level: 'Avanzado',
    duration: '11 horas',
    category: 'DAM',
    objectives: [
      'Desarrollar apps Android con Kotlin',
      'Diseñar interfaces móviles con XML',
      'Gestionar multimedia (audio, vídeo, imágenes)',
      'Publicar apps en Google Play',
    ],
    lessons: [
      { id: '1', title: 'Introducción a Android y Kotlin', duration: '50 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Activities y layouts', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Intents y navegación', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'RecyclerView y listas', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Bases de datos SQLite', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Reproducción de audio y vídeo', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Cámara y galería', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Sensores y geolocalización', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Material Design', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: App multimedia completa', duration: '90 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 1123,
  },
  'dam-servicios': {
    id: 'dam-servicios',
    title: 'Programación de Servicios y Procesos',
    description: 'Programación multihilo, sockets, servicios web REST, comunicación en red y concurrencia en Java.',
    icon: '🔄',
    xp: 700,
    level: 'Avanzado',
    duration: '10 horas',
    category: 'DAM',
    objectives: [
      'Crear hilos y gestionar concurrencia',
      'Programar sockets para comunicación en red',
      'Desarrollar servicios web REST',
      'Implementar seguridad en comunicaciones',
    ],
    lessons: [
      { id: '1', title: 'Introducción a hilos (Threads)', duration: '50 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Sincronización y concurrencia', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Comunicación entre hilos', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Sockets TCP', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Sockets UDP', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Servicios web REST', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Consumo de APIs REST', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Seguridad en servicios', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Chat cliente-servidor', duration: '85 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 567,
  },
  'dam-sge': {
    id: 'dam-sge',
    title: 'Sistemas de Gestión Empresarial',
    description: 'ERP Odoo, CRM, gestión comercial y módulos empresariales. Personalización y desarrollo de módulos.',
    icon: '🏢',
    xp: 550,
    level: 'Intermedio',
    duration: '8 horas',
    category: 'DAM',
    objectives: [
      'Conocer sistemas ERP y CRM',
      'Trabajar con Odoo',
      'Personalizar módulos empresariales',
      'Implementar procesos de negocio',
    ],
    lessons: [
      { id: '1', title: 'Introducción a ERP y CRM', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Instalación de Odoo', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Módulos de Odoo', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Gestión de ventas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Gestión de compras', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Inventario y almacén', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Personalización de módulos', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Proyecto: Implementación ERP completa', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 423,
  },
  // ===== CURSOS SMR - PRIMER AÑO =====
  'smr-montaje': {
    id: 'smr-montaje',
    title: 'Montaje y Mantenimiento de Equipos',
    description: 'Ensamblaje de ordenadores, identificación de componentes, mantenimiento preventivo y resolución de averías.',
    icon: '🔧',
    xp: 550,
    level: 'Principiante',
    duration: '8 horas',
    category: 'SMR',
    objectives: [
      'Identificar componentes hardware',
      'Ensamblar equipos informáticos',
      'Realizar mantenimiento preventivo',
      'Diagnosticar y resolver averías',
    ],
    lessons: [
      { id: '1', title: 'Componentes de un PC', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Placa base y procesador', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Memoria RAM y almacenamiento', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Tarjetas gráficas y expansión', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Fuentes de alimentación', duration: '35 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Ensamblaje paso a paso', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Mantenimiento preventivo', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Diagnóstico de averías', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Montaje completo de PC', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 1034,
  },
  'smr-so-mono': {
    id: 'smr-so-mono',
    title: 'Sistemas Operativos Monopuesto',
    description: 'Instalación y administración de Windows y Linux en equipos individuales. Gestión de usuarios y recursos.',
    icon: '🖥️',
    xp: 500,
    level: 'Principiante',
    duration: '7 horas',
    category: 'SMR',
    objectives: [
      'Instalar y configurar Windows',
      'Instalar y configurar Linux',
      'Gestionar usuarios y permisos',
      'Administrar recursos del sistema',
    ],
    lessons: [
      { id: '1', title: 'Introducción a sistemas operativos', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Instalación de Windows 10/11', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Configuración de Windows', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Instalación de Ubuntu/Linux Mint', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Terminal Linux básico', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Gestión de usuarios', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Permisos y seguridad', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Proyecto: Configuración dual boot', duration: '65 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 945,
  },
  'smr-ofimatica': {
    id: 'smr-ofimatica',
    title: 'Aplicaciones Ofimáticas',
    description: 'Dominio de Microsoft Office, LibreOffice, Google Workspace y herramientas de productividad.',
    icon: '📄',
    xp: 450,
    level: 'Principiante',
    duration: '6 horas',
    category: 'SMR',
    objectives: [
      'Dominar procesadores de texto',
      'Crear hojas de cálculo avanzadas',
      'Diseñar presentaciones profesionales',
      'Trabajar con Google Workspace',
    ],
    lessons: [
      { id: '1', title: 'Word/Writer: formato y estilos', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Word/Writer: tablas y gráficos', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Excel/Calc: fórmulas básicas', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Excel/Calc: funciones avanzadas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Excel/Calc: tablas dinámicas', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'PowerPoint/Impress: diseño', duration: '40 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Google Workspace', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Proyecto: Informe empresarial completo', duration: '60 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 678,
  },
  'smr-so-red': {
    id: 'smr-so-red',
    title: 'Sistemas Operativos en Red',
    description: 'Instalación y administración de Windows Server y Linux Server. Active Directory, DNS, DHCP y servicios de red.',
    icon: '🌐',
    xp: 650,
    level: 'Intermedio',
    duration: '9 horas',
    category: 'SMR',
    objectives: [
      'Instalar y configurar Windows Server',
      'Gestionar Active Directory',
      'Configurar servicios DNS y DHCP',
      'Administrar servidores Linux',
    ],
    lessons: [
      { id: '1', title: 'Introducción a servidores', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Instalación Windows Server', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Active Directory: conceptos', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Active Directory: usuarios y grupos', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'DNS y resolución de nombres', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'DHCP y asignación de IPs', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Linux Server: Ubuntu Server', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Samba y compartición de archivos', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Dominio Active Directory completo', duration: '80 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 756,
  },
  'smr-redes': {
    id: 'smr-redes',
    title: 'Redes Locales',
    description: 'Diseño, instalación y configuración de redes locales. Cableado estructurado, switching, routing y WiFi.',
    icon: '🔌',
    xp: 700,
    level: 'Intermedio',
    duration: '10 horas',
    category: 'SMR',
    objectives: [
      'Diseñar redes locales',
      'Cablear redes estructuradas',
      'Configurar switches y routers',
      'Implementar redes WiFi',
    ],
    lessons: [
      { id: '1', title: 'Fundamentos de redes', duration: '50 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Modelo OSI y TCP/IP', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Direccionamiento IP y subnetting', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Cableado estructurado', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Configuración de switches', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'VLANs y segmentación', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Routing básico', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Redes WiFi y seguridad', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Diagnóstico y resolución de problemas', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: Red empresarial completa', duration: '90 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 1089,
  },
  // ===== CURSOS SMR - SEGUNDO AÑO =====
  'smr-seguridad': {
    id: 'smr-seguridad',
    title: 'Seguridad Informática',
    description: 'Seguridad en redes y sistemas, criptografía, firewall, antivirus y auditorías de seguridad.',
    icon: '🔒',
    xp: 650,
    level: 'Avanzado',
    duration: '9 horas',
    category: 'SMR',
    objectives: [
      'Implementar medidas de seguridad',
      'Configurar firewalls y antivirus',
      'Aplicar criptografía',
      'Realizar auditorías de seguridad',
    ],
    lessons: [
      { id: '1', title: 'Introducción a la seguridad', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Tipos de amenazas', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Criptografía básica', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Certificados digitales y PKI', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Firewalls y filtrado', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Antivirus y antimalware', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'VPN y conexiones seguras', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Auditorías y pentesting básico', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Plan de seguridad empresarial', duration: '75 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 834,
  },
  'smr-servicios-red': {
    id: 'smr-servicios-red',
    title: 'Servicios en Red',
    description: 'Configuración de servidores web, FTP, correo electrónico, proxy y servicios de red avanzados.',
    icon: '☁️',
    xp: 700,
    level: 'Avanzado',
    duration: '10 horas',
    category: 'SMR',
    objectives: [
      'Configurar servidores web (Apache, Nginx)',
      'Implementar servidores FTP y correo',
      'Gestionar servidores proxy',
      'Administrar servicios de streaming',
    ],
    lessons: [
      { id: '1', title: 'Servidor web Apache', duration: '55 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Virtual Hosts y SSL', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Nginx y reverse proxy', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Servidor FTP (vsftpd)', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Servidor de correo (Postfix)', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Webmail y gestión de correo', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Servidor proxy (Squid)', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Balanceo de carga', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Monitorización de servicios', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: Infraestructura de servicios completa', duration: '90 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 623,
  },
  'smr-web': {
    id: 'smr-web',
    title: 'Aplicaciones Web',
    description: 'Desarrollo web con HTML, CSS, JavaScript, PHP y gestores de contenido como WordPress.',
    icon: '🌍',
    xp: 600,
    level: 'Intermedio',
    duration: '8 horas',
    category: 'SMR',
    objectives: [
      'Desarrollar sitios web con HTML/CSS/JS',
      'Programar en PHP y MySQL',
      'Gestionar WordPress',
      'Implementar tiendas online',
    ],
    lessons: [
      { id: '1', title: 'HTML5 avanzado', duration: '50 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'CSS3 y diseño responsive', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'JavaScript: DOM y eventos', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'PHP básico', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'PHP y MySQL', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'WordPress: instalación y configuración', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'WordPress: temas y plugins', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'WooCommerce y tiendas online', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Sitio web dinámico completo', duration: '75 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 987,
  },
  'smr-bbdd-gestion': {
    id: 'smr-bbdd-gestion',
    title: 'Gestión de Bases de Datos',
    description: 'Administración de MySQL, PostgreSQL, backups, optimización y seguridad en bases de datos.',
    icon: '💾',
    xp: 550,
    level: 'Intermedio',
    duration: '7 horas',
    category: 'SMR',
    objectives: [
      'Administrar servidores de bases de datos',
      'Realizar copias de seguridad',
      'Optimizar consultas y rendimiento',
      'Implementar seguridad en bases de datos',
    ],
    lessons: [
      { id: '1', title: 'Instalación de MySQL', duration: '40 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Gestión de usuarios y permisos', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Backups y restauración', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Optimización de consultas', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Índices y performance', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Replicación y alta disponibilidad', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Monitorización de bases de datos', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Proyecto: Administración completa de BBDD', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 512,
  },
  // ===== CURSOS DESARROLLO WEB =====
  'web-cliente': {
    id: 'web-cliente',
    title: 'Desarrollo Web en Entorno Cliente',
    description: 'JavaScript moderno, TypeScript, React, Vue y frameworks frontend para aplicaciones web interactivas.',
    icon: '⚛️',
    xp: 750,
    level: 'Avanzado',
    duration: '11 horas',
    category: 'Web',
    objectives: [
      'Dominar JavaScript ES6+',
      'Desarrollar con React y Vue',
      'Gestionar estado con Redux/Pinia',
      'Consumir APIs REST',
    ],
    lessons: [
      { id: '1', title: 'JavaScript moderno ES6+', duration: '60 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'TypeScript: tipos y interfaces', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'React: componentes y JSX', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'React: hooks y estado', duration: '75 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'React: routing y navegación', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Redux: gestión de estado global', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Vue.js: fundamentos', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Consumo de APIs con fetch/axios', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Testing con Jest', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Proyecto: Aplicación React completa', duration: '90 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 1456,
  },
  'web-servidor': {
    id: 'web-servidor',
    title: 'Desarrollo Web en Entorno Servidor',
    description: 'Node.js, Express, Django, Laravel y desarrollo backend con APIs REST y autenticación.',
    icon: '🖧',
    xp: 800,
    level: 'Avanzado',
    duration: '12 horas',
    category: 'Web',
    objectives: [
      'Desarrollar APIs REST con Node.js/Express',
      'Implementar autenticación JWT',
      'Usar frameworks backend (Django, Laravel)',
      'Gestionar bases de datos desde el servidor',
    ],
    lessons: [
      { id: '1', title: 'Node.js: fundamentos', duration: '55 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Express: rutas y middleware', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'APIs REST con Express', duration: '75 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Autenticación JWT', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'MongoDB y Mongoose', duration: '80 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Django: MVT y ORM', duration: '75 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Django REST Framework', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Laravel: Eloquent y Blade', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Seguridad en backend', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Websockets y tiempo real', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '11', title: 'Proyecto: API REST completa con auth', duration: '100 min', status: 'locked' as const, xp: 150 },
    ],
    progress: 0,
    studentsEnrolled: 1289,
  },
  'web-despliegue': {
    id: 'web-despliegue',
    title: 'Despliegue de Aplicaciones Web',
    description: 'Docker, CI/CD, AWS, Vercel, Nginx y despliegue de aplicaciones web en producción.',
    icon: '🚀',
    xp: 600,
    level: 'Avanzado',
    duration: '8 horas',
    category: 'Web',
    objectives: [
      'Dominar Docker y contenedores',
      'Configurar CI/CD con GitHub Actions',
      'Desplegar en AWS y Vercel',
      'Configurar servidores de producción',
    ],
    lessons: [
      { id: '1', title: 'Introducción a Docker', duration: '50 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Dockerfiles y contenedores', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Docker Compose', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'GitHub Actions: CI/CD', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Despliegue en Vercel/Netlify', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'AWS: EC2 y S3', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Nginx como reverse proxy', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'SSL/TLS y HTTPS', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Proyecto: Despliegue fullstack completo', duration: '75 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 967,
  },
  'web-diseno': {
    id: 'web-diseno',
    title: 'Diseño de Interfaces Web',
    description: 'UX/UI, Figma, accesibilidad, responsive design y diseño centrado en el usuario.',
    icon: '🎨',
    xp: 550,
    level: 'Intermedio',
    duration: '7 horas',
    category: 'Web',
    objectives: [
      'Diseñar interfaces con Figma',
      'Aplicar principios de UX/UI',
      'Implementar accesibilidad web',
      'Crear diseños responsive',
    ],
    lessons: [
      { id: '1', title: 'Principios de UX/UI', duration: '45 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Figma: herramientas básicas', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Prototipado interactivo', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Design Systems', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Responsive design', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Accesibilidad (WCAG)', duration: '50 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Animaciones y microinteracciones', duration: '45 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'Proyecto: Diseño completo de aplicación', duration: '70 min', status: 'locked' as const, xp: 100 },
    ],
    progress: 0,
    studentsEnrolled: 778,
  },
  'web-avanzado': {
    id: 'web-avanzado',
    title: 'Desarrollo Web Avanzado',
    description: 'Next.js, GraphQL, WebAssembly, PWA y tecnologías de última generación para desarrollo web.',
    icon: '⚡',
    xp: 850,
    level: 'Experto',
    duration: '13 horas',
    category: 'Web',
    objectives: [
      'Dominar Next.js y SSR',
      'Trabajar con GraphQL',
      'Crear Progressive Web Apps',
      'Optimizar rendimiento web',
    ],
    lessons: [
      { id: '1', title: 'Next.js: fundamentos', duration: '60 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'SSR y SSG con Next.js', duration: '75 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'API Routes en Next.js', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'GraphQL: queries y mutations', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Apollo Client', duration: '75 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Progressive Web Apps', duration: '80 min', status: 'locked' as const, xp: 50 },
      { id: '7', title: 'Service Workers', duration: '65 min', status: 'locked' as const, xp: 50 },
      { id: '8', title: 'WebAssembly básico', duration: '60 min', status: 'locked' as const, xp: 50 },
      { id: '9', title: 'Optimización y performance', duration: '70 min', status: 'locked' as const, xp: 50 },
      { id: '10', title: 'Web Components', duration: '55 min', status: 'locked' as const, xp: 50 },
      { id: '11', title: 'Proyecto: Aplicación web fullstack moderna', duration: '120 min', status: 'locked' as const, xp: 200 },
    ],
    progress: 0,
    studentsEnrolled: 534,
  },
  'fundamentals': {
    id: 'fundamentals',
    title: 'Fundamentos: Piensa como un Programador',
    description: 'Aprende los conceptos básicos de programación y desarrolla tu pensamiento lógico',
    icon: '🧠',
    xp: 300,
    level: 'Principiante',
    duration: '3 horas',
    category: 'Fundamentos',
    objectives: [
      'Comprender qué es la programación',
      'Desarrollar pensamiento lógico',
      'Aprender a resolver problemas',
      'Dominar conceptos fundamentales',
    ],
    lessons: [
      { id: '1', title: '¿Qué es la Programación?', duration: '30 min', status: 'available' as const, xp: 50 },
      { id: '2', title: 'Variables y Datos', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '3', title: 'Operadores y Expresiones', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '4', title: 'Control de Flujo', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '5', title: 'Funciones', duration: '30 min', status: 'locked' as const, xp: 50 },
      { id: '6', title: 'Estructuras de Datos', duration: '30 min', status: 'locked' as const, xp: 50 },
    ],
    progress: 0,
    studentsEnrolled: 0,
  },
  'intro-programacion': {
    id: 'intro-programacion',
    title: 'Introducción a la Programación',
    description: 'Primeros pasos en el mundo de la programación',
    icon: '💻',
    xp: 150,
    level: 'Principiante',
    duration: '1 hora',
    category: 'Fundamentos',
    objectives: [
      'Entender qué es programar',
      'Conocer las variables',
      'Aprender sobre condiciones',
    ],
    lessons: [
      { id: '1', title: '¿Qué es programar?', duration: '20 min', status: 'available' as const, xp: 30 },
      { id: '2', title: 'Variables', duration: '20 min', status: 'locked' as const, xp: 30 },
      { id: '3', title: 'Condiciones', duration: '20 min', status: 'locked' as const, xp: 30 },
    ],
    progress: 0,
    studentsEnrolled: 0,
  },
};

export default function CoursePage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  const [lessonStatuses, setLessonStatuses] = useState<{[key: string]: string}>({});
  const [activeTab, setActiveTab] = useState<'lessons' | 'forum'>('lessons');
  
  const course = coursesData[courseId as keyof typeof coursesData];

  // Cargar estado de lecciones desde localStorage
  useEffect(() => {
    if (typeof window !== 'undefined' && course) {
      const statuses: {[key: string]: string} = {};
      let lastCompletedIndex = -1;
      
      course.lessons.forEach((lesson: any, index: number) => {
        const progressKey = `lesson_${courseId}_${lesson.id}`;
        const status = localStorage.getItem(progressKey);
        
        if (status === 'completed') {
          statuses[lesson.id] = 'completed';
          lastCompletedIndex = index;
        } else if (index === 0 && !status) {
          // Primera lección siempre disponible
          statuses[lesson.id] = 'available';
        } else if (index === lastCompletedIndex + 1 || (lastCompletedIndex >= 0 && index === lastCompletedIndex + 1)) {
          // Desbloquear la siguiente lección después de la última completada
          statuses[lesson.id] = 'available';
        } else if (index <= lastCompletedIndex + 1) {
          // Lecciones anteriores o la siguiente a la completada
          statuses[lesson.id] = lesson.status === 'locked' ? 'available' : lesson.status;
        } else {
          // Lecciones más adelante permanecen bloqueadas
          statuses[lesson.id] = 'locked';
        }
      });
      
      // Segunda pasada para actualizar basado en completadas
      course.lessons.forEach((lesson: any, index: number) => {
        const progressKey = `lesson_${courseId}_${lesson.id}`;
        const status = localStorage.getItem(progressKey);
        
        if (status === 'completed') {
          lastCompletedIndex = Math.max(lastCompletedIndex, index);
        }
      });
      
      // Tercera pasada para desbloquear correctamente
      course.lessons.forEach((lesson: any, index: number) => {
        const progressKey = `lesson_${courseId}_${lesson.id}`;
        const status = localStorage.getItem(progressKey);
        
        if (status === 'completed') {
          statuses[lesson.id] = 'completed';
        } else if (index === 0) {
          statuses[lesson.id] = 'available';
        } else if (index <= lastCompletedIndex + 1) {
          statuses[lesson.id] = 'available';
        } else {
          statuses[lesson.id] = 'locked';
        }
      });
      
      setLessonStatuses(statuses);
      console.log('Loaded lesson statuses:', statuses);
      console.log('Last completed index:', lastCompletedIndex);
    }
  }, [courseId, course]);

  if (!course) {
    return (
      <div className="min-h-screen bg-stone-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-stone-100 mb-4">Curso no encontrado</h1>
          <Link href="/skill-tree" className="text-amber-600 hover:text-amber-500">
            ← Volver al árbol de habilidades
          </Link>
        </div>
      </div>
    );
  }

  const completedLessons = course.lessons.filter((l: any) => {
    const status = lessonStatuses[l.id] || l.status;
    return status === 'completed';
  }).length;
  const totalLessons = course.lessons.length;

  const getLessonStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'in-progress':
        return <Circle className="w-5 h-5 text-stone-500 fill-blue-500/30" />;
      case 'available':
        return <Play className="w-5 h-5 text-stone-500" />;
      case 'locked':
        return <Lock className="w-5 h-5 text-gray-400" />;
      default:
        return <Lock className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800/50 backdrop-blur-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/skill-tree" className="text-white/80 hover:text-white flex items-center gap-2 font-medium">
            <ArrowLeft className="w-5 h-5" />
            Volver al árbol de habilidades
          </Link>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Course Header */}
            <div className="bg-stone-800 rounded-lg p-8 text-stone-100 border-2 border-stone-700">
              <div className="flex items-start gap-6">
                <div className="w-20 h-20 bg-amber-700/20 backdrop-blur-sm rounded-lg flex items-center justify-center text-5xl border-2 border-amber-800">
                  {course.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="px-3 py-1 bg-amber-700/20 rounded-lg text-sm font-semibold border-2 border-amber-800">
                      {course.category}
                    </span>
                    <span className="px-3 py-1 bg-amber-700/20 rounded-lg text-sm font-semibold border-2 border-amber-800">
                      {course.level}
                    </span>
                  </div>
                  <h1 className="text-4xl font-bold mb-3">{course.title}</h1>
                  <p className="text-stone-300 text-lg mb-4">{course.description}</p>
                  
                  <div className="flex items-center gap-6 text-sm">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      <span>{course.duration}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4" />
                      <span>{totalLessons} lecciones</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Trophy className="w-4 h-4 text-amber-600" />
                      <span>+{course.xp} XP</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Tu Progreso</span>
                  <span className="text-sm font-bold">{course.progress}%</span>
                </div>
                <div className="w-full bg-stone-700 rounded-full h-3">
                  <div
                    className="bg-amber-600 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${course.progress}%` }}
                  />
                </div>
                <p className="text-sm text-stone-300 mt-2">
                  {completedLessons} de {totalLessons} lecciones completadas
                </p>
              </div>
            </div>

            {/* Learning Objectives */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                <Target className="w-6 h-6 text-amber-600" />
                Objetivos de Aprendizaje
              </h2>
              <ul className="space-y-3">
                {course.objectives.map((objective, index) => (
                  <li key={index} className="flex items-start gap-3 text-stone-300">
                    <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    <span>{objective}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Tabs: Lecciones / Foro */}
            <div className="bg-stone-800 rounded-lg border-2 border-stone-700 overflow-hidden">
              <div className="flex border-b-2 border-stone-700">
                <button
                  onClick={() => setActiveTab('lessons')}
                  className={`flex-1 px-6 py-4 font-semibold transition flex items-center justify-center gap-2 ${
                    activeTab === 'lessons'
                      ? 'bg-amber-700 text-white'
                      : 'text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  <BookOpen className="w-5 h-5" />
                  Lecciones
                </button>
                <button
                  onClick={() => setActiveTab('forum')}
                  className={`flex-1 px-6 py-4 font-semibold transition flex items-center justify-center gap-2 ${
                    activeTab === 'forum'
                      ? 'bg-amber-700 text-white'
                      : 'text-stone-300 hover:bg-stone-700'
                  }`}
                >
                  <MessageSquare className="w-5 h-5" />
                  Foro del Curso
                </button>
              </div>

              <div className="p-6">
                {activeTab === 'lessons' ? (
                  <div className="space-y-3">{course.lessons.map((lesson: any, index: number) => {
                  const actualStatus = lessonStatuses[lesson.id] || lesson.status;
                  return (
                  <div
                    key={lesson.id}
                    className={`flex items-center justify-between p-4 rounded-lg border-2 transition-all ${
                      actualStatus === 'completed'
                        ? 'bg-green-900/20 border-green-700'
                        : actualStatus === 'in-progress'
                        ? 'bg-amber-900/20 border-amber-700'
                        : actualStatus === 'available'
                        ? 'bg-stone-900/20 border-stone-700 hover:bg-stone-900/40 cursor-pointer'
                        : 'bg-stone-900/10 border-stone-700 opacity-60'
                    }`}
                    onClick={() => {
                      if (actualStatus !== 'locked') {
                        router.push(`/course/${courseId}/lesson/${lesson.id}`);
                      }
                    }}
                  >
                    <div className="flex items-center gap-4 flex-1">
                      {getLessonStatusIcon(actualStatus)}
                      <div>
                        <h3 className={`font-semibold ${
                          actualStatus === 'locked' ? 'text-stone-400' : 'text-stone-100'
                        }`}>
                          Lección {index + 1}: {lesson.title}
                        </h3>
                        <div className="flex items-center gap-4 mt-1">
                          <p className="text-sm text-stone-400">{lesson.duration}</p>
                          <p className="text-sm text-amber-600 font-medium">+{lesson.xp} XP</p>
                        </div>
                      </div>
                    </div>
                    {actualStatus === 'available' && (
                      <Link
                        href={`/course/${courseId}/lesson/${lesson.id}`}
                        className="px-5 py-2 bg-amber-700 hover:bg-amber-600 text-white rounded-lg font-medium transition-colors border-2 border-amber-800"
                      >
                        Comenzar
                      </Link>
                    )}
                    {actualStatus === 'in-progress' && (
                      <Link
                        href={`/course/${courseId}/lesson/${lesson.id}`}
                        className="px-5 py-2 bg-amber-900/300 hover:bg-stone-600 text-white rounded-lg font-medium transition-colors"
                      >
                        Continuar
                      </Link>
                    )}
                    {actualStatus === 'completed' && (
                      <span className="text-green-400 font-medium flex items-center gap-2">
                        <CheckCircle className="w-5 h-5" />
                        Completado
                      </span>
                    )}
                  </div>
                  );
                })}
              </div>
                ) : (
                  <Forum 
                    courseId={courseId}
                    title={`Foro de ${course.title}`}
                    categories={['Preguntas', 'Ayuda con ejercicios', 'Proyectos', 'Recursos', 'Dudas generales']}
                  />
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">{/* Stats Card */}
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-4">Estadísticas</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Progreso</span>
                  <span className="text-white font-bold">{course.progress}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">XP Total</span>
                  <span className="text-yellow-400 font-bold">+{course.xp}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Lecciones</span>
                  <span className="text-white font-bold">{completedLessons}/{totalLessons}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-white/70">Duración</span>
                  <span className="text-white font-bold">{course.duration}</span>
                </div>
              </div>
            </div>

            {/* Achievements Preview */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-3 flex items-center gap-2">
                <Trophy className="w-6 h-6 text-amber-600" />
                Logros Desbloqueables
              </h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-full ${
                    course.progress >= 50 ? 'bg-amber-700' : 'bg-stone-700'
                  } flex items-center justify-center`}>
                    <Star className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-stone-100 font-semibold text-sm">Medio Camino</p>
                    <p className="text-stone-400 text-xs">Completa el 50% del curso</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-full ${
                    course.progress >= 100 ? 'bg-amber-700' : 'bg-stone-700'
                  } flex items-center justify-center`}>
                    <Trophy className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-stone-100 font-semibold text-sm">Maestro {course.category}</p>
                    <p className="text-stone-400 text-xs">Completa el 100% del curso</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Community Stats */}
            <div className="bg-stone-800 rounded-lg p-6 border-2 border-stone-700">
              <h3 className="text-xl font-bold text-stone-100 mb-4">Comunidad</h3>
              <div className="text-center">
                <p className="text-4xl font-bold text-amber-600 mb-2">{course.studentsEnrolled.toLocaleString()}</p>
                <p className="text-stone-400">estudiantes inscritos</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
