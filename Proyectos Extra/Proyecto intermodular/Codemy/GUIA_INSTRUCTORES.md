# 📚 Guía para Instructores - CodeAcademy

> **Manual completo para profesores que quieren usar CodeAcademy en sus aulas**

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Estructura de los Cursos](#estructura-de-los-cursos)
4. [Añadir Contenido Nuevo](#añadir-contenido-nuevo)
5. [Seguimiento de Estudiantes](#seguimiento-de-estudiantes)
6. [Criterios de Evaluación](#criterios-de-evaluación)
7. [Soluciones de Ejercicios](#soluciones-de-ejercicios)
8. [Troubleshooting](#troubleshooting)

---

## 👨‍🏫 Introducción

CodeAcademy es una plataforma educativa diseñada específicamente para la enseñanza de programación en entornos académicos. El contenido está basado en el material probado en aulas reales del profesor Jose Vicente Carratalá.

### Características Clave para Docentes

- ✅ **Contenido Curricular Completo**: 33 lecciones alineadas con DAM
- ✅ **Gamificación**: Sistema de XP y logros motiva a los estudiantes
- ✅ **Autocorrección**: Los ejercicios se validan automáticamente
- ✅ **Progreso Visual**: Skill tree muestra avance del estudiante
- ✅ **Extensible**: Fácil añadir nuevo contenido
- ✅ **Sin Backend**: Funciona completamente en el navegador

---

## 🛠️ Instalación y Configuración

### Opción 1: Instalación Local (Recomendada para Aulas)

```bash
# 1. Clonar el repositorio
git clone https://github.com/MutenRos/Codemy.git
cd Codemy

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev

# 4. Acceder a la plataforma
# http://localhost:3000
```

### Opción 2: Despliegue en Red Local

Para que los estudiantes accedan desde sus equipos:

```bash
# 1. Encontrar tu IP local
ip a  # Linux
ipconfig  # Windows

# 2. Asegúrate de que el firewall permita el puerto 3000
sudo ufw allow 3000/tcp  # Linux

# 3. Estudiantes acceden a:
# http://[TU_IP]:3000
# Ejemplo: http://192.168.1.157:3000
```

### Opción 3: Despliegue en la Nube (Vercel)

Para acceso remoto:

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Desplegar
cd codeacademy
vercel

# Vercel te dará una URL pública
# https://tu-codeacademy.vercel.app
```

---

## 📖 Estructura de los Cursos

### Cursos Actuales

| Curso ID | Título | Lecciones | XP Total | Nivel |
|----------|--------|-----------|----------|-------|
| `py-intro` | Introducción a Python | 4 | 200 | Básico |
| `py-variables` | Variables y Tipos | 5 | 250 | Básico |
| `py-control` | Estructuras de Control | 6 | 300 | Básico |
| `py-functions` | Funciones | 6 | 350 | Intermedio |
| `py-classes` | POO | 6 | 400 | Intermedio |
| `py-files` | Archivos y Persistencia | 6 | 300 | Intermedio |

### Anatomía de una Lección

Cada lección contiene:

1. **Teoría** (`theory`):
   - Introducción al concepto
   - Secciones con puntos clave
   - Ejemplo de código con explicación

2. **Ejercicio** (`exercise`):
   - Descripción clara del objetivo
   - Código inicial (starter code)
   - Solución de referencia
   - Criterio de validación
   - Sistema de pistas progresivas

3. **Metadata**:
   - Título y duración estimada
   - XP que otorga
   - Estado (locked/available/completed)

### Flujo de Aprendizaje

```
1. Estudiante selecciona curso → Skill Tree
2. Accede a lección → Teoría + Ejemplo
3. Resuelve ejercicio → Editor interactivo
4. Valida código → Sistema de autocorrección
5. Gana XP y desbloquea logros
6. Continúa a siguiente lección
```

---

## ➕ Añadir Contenido Nuevo

### Paso 1: Definir el Curso

Edita `apps/web/src/app/course/[courseId]/page.tsx`:

```typescript
const coursesData = {
  // ... cursos existentes
  'mi-nuevo-curso': {
    id: 'mi-nuevo-curso',
    title: 'Mi Nuevo Curso',
    description: 'Descripción breve del curso',
    icon: '🎯',  // Emoji que representa el curso
    xp: 350,
    lessons: [
      { 
        id: '1', 
        title: 'Primera Lección', 
        duration: '10 min', 
        status: 'available', 
        xp: 50 
      },
      { 
        id: '2', 
        title: 'Segunda Lección', 
        duration: '15 min', 
        status: 'locked', 
        xp: 50 
      },
      // ... más lecciones
    ],
  },
};
```

### Paso 2: Agregar al Skill Tree

Edita `apps/web/src/app/skill-tree/page.tsx`:

```typescript
const skillTrees = {
  python: [
    // ... nodos existentes
    {
      id: 'mi-nuevo-curso',
      title: 'Mi Nuevo Curso',
      description: 'Breve descripción',
      icon: '🎯',
      status: (courseProgress['mi-nuevo-curso'] === 100 ? 'completed' : 
               courseProgress['mi-nuevo-curso'] > 0 ? 'in-progress' : 
               courseProgress['CURSO_PREREQUISITO'] === 100 ? 'available' : 
               'locked'),
      xp: 350,
      lessons: [/* array de lecciones */],
      progress: courseProgress['mi-nuevo-curso'] || 0,
      prerequisites: ['CURSO_PREREQUISITO'],  // IDs de cursos que deben completarse antes
      category: 'intermediate' as const,  // 'foundation' | 'intermediate' | 'advanced' | 'expert'
      position: { x: 50, y: 80 },  // Posición en el árbol (0-100, 0-100)
    },
  ],
};
```

### Paso 3: Crear Contenido de Lecciones

Edita `apps/web/src/app/course/[courseId]/lesson/[lessonId]/page.tsx`:

```typescript
const lessonsContent = {
  // ... lecciones existentes
  'mi-nuevo-curso': {
    '1': {
      title: 'Primera Lección',
      duration: '10 min',
      xp: 50,
      theory: {
        introduction: 'Introducción al concepto...',
        sections: [
          {
            title: 'Subsección 1',
            content: 'Explicación del concepto',
            points: [
              'Punto clave 1',
              'Punto clave 2',
              'Punto clave 3',
            ],
          },
        ],
        example: {
          title: 'Ejemplo Práctico',
          code: `# Código de ejemplo
print("Hola mundo")`,
          explanation: 'Explicación del ejemplo',
        },
      },
      exercise: {
        title: 'Ejercicio: Tu primer programa',
        description: 'Escribe un programa que...',
        initialCode: `# Escribe tu código aquí


`,
        solution: `# Solución de referencia
print("Solución")`,
        test: 'output_contains',  // Tipo de validación
        expectedOutput: ['palabra1', 'palabra2'],  // Lo que debe aparecer en la salida
        minLines: 2,  // Mínimo de líneas de código
        hints: [
          'Pista 1: Usa la función print()',
          'Pista 2: El texto debe ir entre comillas',
          'Pista 3: Aquí está la solución completa...',
        ],
      },
    },
    '2': {
      // ... siguiente lección
    },
  },
};
```

### Paso 4: Actualizar Sistema de Logros

Edita `apps/web/src/lib/achievements.ts`:

```typescript
const COURSES: CourseDef[] = [
  // ... cursos existentes
  { id: 'mi-nuevo-curso', lessons: 6, xpPerLesson: 50 },
];
```

Y también actualiza el array `courses` en `apps/web/src/app/skill-tree/page.tsx`:

```typescript
const courses = [
  // ... existentes
  { id: 'mi-nuevo-curso', lessons: 6 },
];
```

---

## 📊 Seguimiento de Estudiantes

### Exportar Progreso de un Estudiante

Pide al estudiante que ejecute esto en la consola del navegador (F12):

```javascript
// Exportar progreso completo
const progreso = {
  datos: computeXP(),
  lecciones: Object.keys(localStorage)
    .filter(k => k.startsWith('lesson_'))
    .map(k => ({ 
      leccion: k, 
      completada: localStorage.getItem(k) === 'completed' 
    })),
  logros: JSON.parse(localStorage.getItem('unlocked_achievements') || '[]'),
  notificaciones: JSON.parse(localStorage.getItem('app_notifications') || '[]'),
};

// Copiar al portapapeles
copy(JSON.stringify(progreso, null, 2));
console.log('Progreso copiado al portapapeles');
```

### Interpretar los Datos

```json
{
  "datos": {
    "xp": 1250,
    "level": 13,
    "completedLessons": 20,
    "completedCourses": 3
  },
  "lecciones": [
    { "leccion": "lesson_py-intro_1", "completada": true },
    { "leccion": "lesson_py-intro_2", "completada": true },
    // ...
  ],
  "logros": [
    "first-steps",
    "python-basics",
    "level-5"
  ]
}
```

### Dashboard del Instructor (Opcional)

Puedes crear un script para recopilar el progreso de todos los estudiantes:

```javascript
// Script para que ejecuten los estudiantes
const enviarProgreso = async (nombreEstudiante) => {
  const progreso = {
    estudiante: nombreEstudiante,
    fecha: new Date().toISOString(),
    datos: computeXP(),
    // ... resto de datos
  };
  
  // Enviar a tu servidor o Google Sheets
  await fetch('TU_WEBHOOK_URL', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(progreso)
  });
  
  alert('Progreso enviado correctamente');
};

// Ejecutar
enviarProgreso('Juan Pérez');
```

---

## 📝 Criterios de Evaluación

### Evaluación Automática

La plataforma valida automáticamente:
- ✅ El código contiene las palabras clave esperadas
- ✅ La salida incluye los valores requeridos
- ✅ Cumple el mínimo de líneas de código
- ✅ Se ejecuta sin errores

### Evaluación Manual (Proyectos)

Para proyectos finales de cada curso, usa estos criterios:

#### py-functions - Proyecto: Agenda CRUD

**Criterios (sobre 10 puntos)**:
- [ ] 2 pts: Define funciones correctamente con `def`
- [ ] 2 pts: Usa parámetros en las funciones
- [ ] 2 pts: Retorna valores con `return`
- [ ] 2 pts: Implementa CRUD completo (Create, Read, Update, Delete)
- [ ] 1 pt: Código bien comentado
- [ ] 1 pt: Funciona sin errores

#### py-classes - Proyecto: Sistema de Clientes

**Criterios (sobre 10 puntos)**:
- [ ] 2 pts: Define clase correctamente
- [ ] 2 pts: Implementa `__init__` con parámetros
- [ ] 2 pts: Define propiedades de instancia
- [ ] 2 pts: Implementa métodos de instancia
- [ ] 1 pt: Crea múltiples objetos de la clase
- [ ] 1 pt: Código bien organizado

#### py-files - Proyecto: Lista de la Compra

**Criterios (sobre 10 puntos)**:
- [ ] 2 pts: Abre y cierra archivos correctamente
- [ ] 2 pts: Lee contenido de archivos
- [ ] 2 pts: Escribe datos en archivos
- [ ] 2 pts: Implementa persistencia (los datos se guardan)
- [ ] 1 pt: Maneja errores básicos
- [ ] 1 pt: Interfaz de usuario clara

### Rúbrica General

| Nivel | XP Ganado | Lecciones | Descripción |
|-------|-----------|-----------|-------------|
| **Principiante** | 0-500 | 0-10 | Entendiendo fundamentos |
| **Aprendiz** | 500-1000 | 10-20 | Aplicando conceptos básicos |
| **Competente** | 1000-1500 | 20-30 | Resolviendo problemas complejos |
| **Avanzado** | 1500-2000 | 30-33 | Dominando Python básico |
| **Maestro** | 2000+ | 33+ | Completó todo + proyectos extras |

---

## 💡 Soluciones de Ejercicios

### ⚠️ Uso Responsable

Las soluciones están disponibles en el código fuente (`solution` en cada ejercicio) pero **NO se muestran directamente a los estudiantes**.

### Acceder a Soluciones

Como instructor, puedes:

1. **Ver el código fuente**:
```bash
# Buscar soluciones
grep -r "solution:" apps/web/src/app/course/
```

2. **Ejecutar en el Playground**:
   - Ve a http://localhost:3000/playground
   - Copia la solución del código fuente
   - Pruébala y modifícala si es necesario

3. **Exportar todas las soluciones**:
```javascript
// Ejecutar en la consola del navegador
Object.entries(lessonsContent).forEach(([courseId, lessons]) => {
  Object.entries(lessons).forEach(([lessonId, lesson]) => {
    if (lesson.exercise?.solution) {
      console.log(`\n=== ${courseId} - Lección ${lessonId} ===`);
      console.log(lesson.exercise.solution);
    }
  });
});
```

### Ejemplo: Solución de py-functions Lección 1

```python
# Mi primera función
def saludar():
    print("¡Hola desde mi función!")

# Llamar a la función
saludar()
saludar()
saludar()
```

---

## 🔧 Troubleshooting

### Problema: Los estudiantes no ven su progreso

**Causa**: Diferentes navegadores o modo incógnito  
**Solución**: Asegúrate de que usen siempre el mismo navegador en modo normal

### Problema: El servidor no arranca (puerto ocupado)

```bash
# Verificar qué está usando el puerto 3000
lsof -i :3000  # Linux/Mac
netstat -ano | findstr :3000  # Windows

# Matar el proceso
kill -9 [PID]

# O usar otro puerto
PORT=3001 npm run dev
```

### Problema: Los estudiantes perdieron su progreso

**Solución**: Los datos están en localStorage del navegador. No se pueden recuperar si se borró la caché.

**Prevención**:
- Implementar sistema de exportación periódica
- Migrar a Supabase (próxima versión)
- Backup manual con el script de exportación

### Problema: Un ejercicio no valida correctamente

1. Revisa el criterio de validación en el código
2. Ajusta `expectedOutput` o `test` según sea necesario
3. Refresca la página para que los cambios se apliquen

---

## 📚 Recursos Adicionales

### Material Original

Todo el contenido de funciones, clases y archivos proviene de:
- **Repositorio**: https://github.com/jocarsa/dam2526
- **Ruta**: `Primero/Programación/`
- **Autor**: Jose Vicente Carratalá

### Comunidad y Soporte

- **Issues GitHub**: Reporta bugs o sugiere mejoras
- **Discusiones**: Comparte experiencias con otros instructores
- **Pull Requests**: Contribuye con nuevo contenido

### Próximas Funcionalidades

- [ ] Dashboard de instructor con vista de toda la clase
- [ ] Sistema de evaluación integrado
- [ ] Exportación a CSV/Excel de progreso
- [ ] Migración a Supabase para persistencia en la nube
- [ ] Certificados automatizados al completar cursos

---

## 📞 Contacto

¿Preguntas? ¿Necesitas ayuda?

- **GitHub**: https://github.com/MutenRos/Codemy
- **Email del Profesor Original**: [Ver repositorio jocarsa/dam2526]

---

<div align="center">

**¡Gracias por usar CodeAcademy en tu aula!**

🎓 Enseñando programación de forma moderna y efectiva 🎓

</div>
