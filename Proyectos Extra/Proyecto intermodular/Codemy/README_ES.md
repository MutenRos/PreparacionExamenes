# 🎓 Codemy - Plataforma de Aprendizaje de Programación

**Codemy** es una plataforma educativa interactiva diseñada para enseñar programación a estudiantes de forma gamificada y atractiva. Con un enfoque en Python, JavaScript y desarrollo web, la plataforma ofrece una experiencia de aprendizaje completa con ejercicios prácticos, seguimiento de progreso y recompensas.

## ✨ Características Principales

### 🎮 Sistema de Aprendizaje Gamificado
- **Árbol de Habilidades Interactivo**: Visualiza tu progreso a través de un skill tree dinámico
- **Sistema de XP y Niveles**: Gana experiencia completando lecciones (100 XP = 1 nivel)
- **15 Lecciones Completas**: Contenido estructurado en 3 cursos de Python
- **Progresión Secuencial**: Desbloquea cursos al completar prerrequisitos

### 🏆 Sistema de Logros
- **14 Achievements Desbloqueables**: Desde "Primer Paso" hasta "Leyenda"
- **4 Niveles de Rareza**: Common, Rare, Epic, Legendary
- **Categorías Variadas**: Learning, Completion, Mastery, Streak
- **Recompensas XP**: Gana XP extra al desbloquear logros
- **Seguimiento Visual**: Barras de progreso para logros bloqueados

### 📊 Estadísticas y Análisis
- **Gráficos de Actividad Semanal**: Visualiza tu progreso diario
- **Métricas Detalladas**: Lecciones completadas, XP ganado, promedio diario
- **Sistema de Rachas**: Mantén tu racha de días activos
- **Dashboard Personalizado**: Vista completa de tu progreso

### 💻 Playground de Código
- **3 Lenguajes Soportados**: Python, JavaScript, HTML/CSS
- **Ejecución en Tiempo Real**: Prueba código inmediatamente
- **Editor de Código**: Sintaxis highlighting y autocompletado
- **Funciones Útiles**:
  - Copiar código al portapapeles
  - Descargar como archivo
  - Reiniciar código
  - Vista previa en vivo (HTML)

### 📚 Contenido Educativo

#### Curso 1: Introducción a Python (4 lecciones)
1. ¿Qué es Python?
2. Instalación
3. Primer programa
4. print() básico

#### Curso 2: Variables y Tipos de Datos (5 lecciones)
1. Qué es una variable
2. Números enteros
3. Números decimales
4. Cadenas de texto
5. Booleanos

#### Curso 3: Control de Flujo (6 lecciones)
1. Condicionales if
2. if-else
3. elif múltiple
4. Bucle while
5. Bucle for
6. break y continue

### 🎯 Sistema de Validación
- **Validación Estricta**: Verifica keywords, longitud de código y estructura
- **Feedback Detallado**: Mensajes específicos sobre qué falta
- **Hints Progresivos**: Sistema de pistas para ayudar
- **Prevención de Trampas**: No acepta solo comentarios o código vacío

## 🛠️ Stack Tecnológico

### Frontend
- **Next.js 16.0.1** - Framework React con App Router
- **TypeScript** - Type safety en todo el proyecto
- **Tailwind CSS** - Estilos utility-first
- **Lucide React** - Iconos modernos

### Backend
- **Supabase** - Base de datos PostgreSQL y autenticación
- **Stripe** - Sistema de pagos y suscripciones
- **PM2** - Gestión de procesos Node.js

### DevOps
- **Turbo** - Monorepo con Turborepo
- **Git** - Control de versiones
- **GitHub** - Repositorio remoto

## 🚀 Inicio Rápido

### Prerrequisitos
```bash
Node.js 18+ 
npm o yarn
Git
```

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/MutenRos/Codemy.git
cd Codemy
```

2. **Instalar dependencias**
```bash
npm install --legacy-peer-deps
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env.local
# Edita .env.local con tus credenciales
```

4. **Iniciar en desarrollo**
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

### Producción con PM2

```bash
# Build
npm run build

# Iniciar con PM2
pm2 start npm --name "codeacademy" -- start
pm2 save
pm2 startup
```

## 📁 Estructura del Proyecto

```
codeacademy/
├── apps/
│   └── web/                    # Aplicación Next.js principal
│       ├── src/
│       │   ├── app/           # App Router páginas
│       │   │   ├── page.tsx                # Landing page
│       │   │   ├── dashboard/              # Dashboard estudiante
│       │   │   ├── skill-tree/             # Árbol de habilidades
│       │   │   ├── course/                 # Sistema de cursos
│       │   │   ├── playground/             # Editor de código
│       │   │   ├── achievements/           # Página de logros
│       │   │   └── api/                    # API routes
│       │   ├── components/    # Componentes React
│       │   │   ├── landing/                # Componentes landing
│       │   │   ├── dashboard/              # XP Tracker, Stats
│       │   │   ├── achievements/           # Sistema de logros
│       │   │   ├── course/                 # Lecciones
│       │   │   └── parent/                 # Panel parental
│       │   ├── data/          # Datos estáticos
│       │   │   ├── achievements.ts         # Definiciones de logros
│       │   │   └── free-course.ts          # Curso gratuito
│       │   └── lib/           # Utilidades
│       └── public/            # Assets estáticos
├── packages/
│   └── database/              # Package de Supabase
│       ├── client.ts          # Cliente configurado
│       ├── types.ts           # TypeScript types
│       └── schema.sql         # Esquema DB
└── docs/                      # Documentación
    ├── DEPLOYMENT.md
    └── STRIPE.md
```

## 🎨 Características de UI/UX

### Diseño
- **Tema Oscuro**: Gradientes morados y azules
- **Responsive**: Optimizado para móvil, tablet y desktop
- **Animaciones**: Transiciones suaves en todos los componentes
- **Glassmorphism**: Efectos de cristal en tarjetas
- **Gradientes**: Colores vibrantes y atractivos

### Interactividad
- **Drag & Drop**: (Próximamente en ejercicios)
- **Tooltips**: Información contextual al hacer hover
- **Loading States**: Indicadores de carga
- **Error Handling**: Mensajes claros de error

## 📊 Persistencia de Datos

### LocalStorage (Actual)
```javascript
// Lecciones completadas
localStorage.setItem('lesson_py-intro_1', 'completed')

// Racha de días
localStorage.setItem('streak_days', '5')

// Última visita
localStorage.setItem('last_visit_date', date)

// Logros desbloqueados
localStorage.setItem('unlocked_achievements', JSON.stringify([...]))
```

### Supabase (Próximamente)
- Sincronización entre dispositivos
- Backup automático
- Leaderboards globales
- Análisis de aprendizaje

## 🔐 Autenticación

### Supabase Auth
- Email/Password
- OAuth (Google, GitHub)
- Magic Links
- Row Level Security (RLS)

## 💳 Sistema de Pagos

### Planes Disponibles
1. **Free**: Curso de introducción gratuito
2. **Student ($9.99/mes)**: Acceso completo individual
3. **Family ($24.99/mes)**: Hasta 5 estudiantes

### Características
- Prueba gratuita de 14 días
- Cancelación en cualquier momento
- Portal de gestión de Stripe
- Webhooks para sincronización

## 🎯 Roadmap

### Fase 1: MVP (✅ Completado)
- [x] Sistema de cursos y lecciones
- [x] Validación de ejercicios
- [x] Persistencia con localStorage
- [x] Sistema de XP y niveles
- [x] Logros y badges
- [x] Playground de código
- [x] Estadísticas y gráficos

### Fase 2: En Desarrollo
- [ ] Integración completa con Supabase
- [ ] Sistema de autenticación funcional
- [ ] Leaderboards globales
- [ ] Más cursos (JavaScript, Web Dev)
- [ ] Ejecución real de código Python
- [ ] Sistema de hints inteligente
- [ ] Modo oscuro/claro

### Fase 3: Futuro
- [ ] Comunidad y foros
- [ ] Mentorías en vivo
- [ ] Proyectos colaborativos
- [ ] Certificados oficiales
- [ ] App móvil nativa
- [ ] IA para asistencia personalizada

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **MutenRos** - *Desarrollo inicial* - [GitHub](https://github.com/MutenRos)

## 🙏 Agradecimientos

- Next.js team por el excelente framework
- Supabase por el backend as a service
- Vercel por el hosting
- Comunidad de código abierto

## 📞 Contacto

- GitHub: [@MutenRos](https://github.com/MutenRos)
- Email: mutenros@gmail.com
- Proyecto: [https://github.com/MutenRos/Codemy](https://github.com/MutenRos/Codemy)

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor abre un issue con:
- Descripción del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si es posible
- Información del navegador/sistema

## 💡 Sugerencias

Las sugerencias de nuevas features son bienvenidas! Abre un issue con el tag `enhancement`.

---

Hecho con ❤️ para la comunidad de aprendizaje
