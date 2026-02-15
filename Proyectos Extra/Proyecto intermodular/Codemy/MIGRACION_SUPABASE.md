# 🚀 Guía de Migración a Supabase

> **Plan para migrar de localStorage a Supabase con persistencia en la nube**

---

## 📋 Índice

1. [¿Por qué migrar a Supabase?](#por-qué-migrar-a-supabase)
2. [Requisitos previos](#requisitos-previos)
3. [Configuración inicial](#configuración-inicial)
4. [Implementación paso a paso](#implementación-paso-a-paso)
5. [Script de migración de datos](#script-de-migración-de-datos)
6. [Testing](#testing)
7. [Despliegue](#despliegue)

---

## 🎯 ¿Por qué migrar a Supabase?

### Ventajas sobre localStorage

| Feature | localStorage | Supabase |
|---------|-------------|----------|
| **Persistencia** | Solo en navegador | Cloud (acceso desde cualquier dispositivo) |
| **Backup** | Manual | Automático |
| **Multi-dispositivo** | ❌ | ✅ |
| **Analíticas** | ❌ | ✅ |
| **Seguridad** | Básica | Avanzada (RLS) |
| **Límite de datos** | ~5-10MB | Sin límite práctico |
| **Colaboración** | ❌ | ✅ |
| **Dashboard instructor** | ❌ | ✅ |

### Estado Actual

✅ **Preparado**: El schema SQL ya está listo en `supabase/schema.sql`  
⏳ **Pendiente**: Implementar el helper client y actualizar componentes  
📝 **Documentado**: Esta guía cubre todo el proceso

---

## 📦 Requisitos Previos

### 1. Cuenta de Supabase

```bash
# Opción 1: Crear cuenta en https://supabase.com (GRATIS)
# - Plan Free: 500MB DB, 1GB file storage, 2GB bandwidth
# - Suficiente para empezar

# Opción 2: Self-hosted (avanzado)
npx supabase init
npx supabase start
```

### 2. Dependencias

```bash
# Instalar Supabase client
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs

# Instalar tipos de TypeScript (opcional pero recomendado)
npm install --save-dev @supabase/supabase-js
```

---

## ⚙️ Configuración Inicial

### Paso 1: Crear proyecto en Supabase

1. Ve a https://supabase.com/dashboard
2. Click en "New Project"
3. Rellena:
   - **Name**: CodeAcademy
   - **Database Password**: [genera una segura]
   - **Region**: Europe West (más cercana a España)
4. Espera ~2 minutos a que se cree

### Paso 2: Obtener credenciales

En tu proyecto de Supabase:
1. Ve a **Settings** → **API**
2. Copia:
   - `Project URL` → será tu `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public` key → será tu `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Paso 3: Configurar variables de entorno

```bash
# apps/web/.env.local
NEXT_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu-anon-key-aquí
```

⚠️ **Importante**: Añade `.env.local` a `.gitignore`

### Paso 4: Ejecutar schema SQL

1. Ve a **SQL Editor** en el dashboard de Supabase
2. Copia y pega el contenido de `supabase/schema.sql`
3. Click en **Run** (o F5)
4. Verifica que no haya errores

---

## 🛠️ Implementación Paso a Paso

### Paso 1: Crear helper client

```bash
# Crear archivo del cliente de Supabase
touch apps/web/src/lib/supabase.ts
```

```typescript
// apps/web/src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/database.types';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey);

// ===== HELPERS DE USUARIO =====

export async function getUserProfile(userId: string) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single();
  
  if (error) throw error;
  return data;
}

export async function updateUserProfile(userId: string, updates: Partial<Database['public']['Tables']['users']['Update']>) {
  const { error } = await supabase
    .from('users')
    .update(updates)
    .eq('id', userId);
  
  if (error) throw error;
}

// ===== HELPERS DE PROGRESO =====

export async function getUserProgress(userId: string) {
  const { data, error } = await supabase
    .from('user_progress')
    .select('*')
    .eq('user_id', userId);
  
  if (error) throw error;
  return data || [];
}

export async function completeLesson(
  userId: string,
  courseId: string,
  lessonId: string,
  code?: string
) {
  const { data, error } = await supabase
    .rpc('complete_lesson', {
      p_user_id: userId,
      p_course_id: courseId,
      p_lesson_id: lessonId,
      p_code: code,
    });
  
  if (error) throw error;
  return data;
}

// ===== HELPERS DE CURSOS =====

export async function getUserCourses(userId: string) {
  const { data, error } = await supabase
    .from('user_courses')
    .select(`
      *,
      courses (*)
    `)
    .eq('user_id', userId);
  
  if (error) throw error;
  return data || [];
}

export async function getCourseProgress(userId: string, courseId: string) {
  const { data, error } = await supabase
    .from('user_courses')
    .select('*')
    .eq('user_id', userId)
    .eq('course_id', courseId)
    .single();
  
  if (error) {
    if (error.code === 'PGRST116') return null; // No encontrado
    throw error;
  }
  return data;
}

// ===== HELPERS DE LOGROS =====

export async function getUserAchievements(userId: string) {
  const { data, error } = await supabase
    .from('user_achievements')
    .select(`
      *,
      achievements (*)
    `)
    .eq('user_id', userId);
  
  if (error) throw error;
  return data || [];
}

export async function unlockAchievement(userId: string, achievementId: string) {
  const { error } = await supabase
    .from('user_achievements')
    .insert({
      user_id: userId,
      achievement_id: achievementId,
    });
  
  if (error && error.code !== '23505') { // Ignorar duplicados
    throw error;
  }
}

// ===== HELPERS DE NOTIFICACIONES =====

export async function getUserNotifications(userId: string, unreadOnly: boolean = false) {
  let query = supabase
    .from('notifications')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });
  
  if (unreadOnly) {
    query = query.eq('read', false);
  }
  
  const { data, error } = await query;
  if (error) throw error;
  return data || [];
}

export async function markNotificationAsRead(notificationId: string) {
  const { error } = await supabase
    .from('notifications')
    .update({ read: true })
    .eq('id', notificationId);
  
  if (error) throw error;
}
```

### Paso 2: Generar tipos de TypeScript (opcional pero recomendado)

```bash
# Instalar CLI de Supabase
npm install supabase --save-dev

# Generar tipos
npx supabase gen types typescript --project-id "tu-project-id" > apps/web/src/types/database.types.ts
```

### Paso 3: Actualizar componentes

Ejemplo para actualizar `user_progress`:

**Antes (localStorage):**
```typescript
// Guardar progreso
localStorage.setItem(`lesson_${courseId}_${lessonId}`, 'completed');

// Leer progreso
const completed = localStorage.getItem(`lesson_${courseId}_${lessonId}`) === 'completed';
```

**Después (Supabase):**
```typescript
import { supabase, completeLesson, getUserProgress } from '@/lib/supabase';

// Guardar progreso
await completeLesson(userId, courseId, lessonId, code);

// Leer progreso
const progress = await getUserProgress(userId);
const completed = progress.some(p => p.lesson_id === `${courseId}_${lessonId}` && p.status === 'completed');
```

### Paso 4: Crear hook personalizado para simplificar

```typescript
// apps/web/src/hooks/useSupabaseProgress.ts
import { useEffect, useState } from 'react';
import { supabase, getUserProgress } from '@/lib/supabase';
import type { Database } from '@/types/database.types';

type UserProgress = Database['public']['Tables']['user_progress']['Row'];

export function useSupabaseProgress(userId: string) {
  const [progress, setProgress] = useState<UserProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!userId) return;

    const fetchProgress = async () => {
      try {
        setLoading(true);
        const data = await getUserProgress(userId);
        setProgress(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();

    // Suscribirse a cambios en tiempo real
    const subscription = supabase
      .channel('user_progress_changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'user_progress',
          filter: `user_id=eq.${userId}`,
        },
        (payload) => {
          console.log('Progress changed:', payload);
          fetchProgress(); // Refetch cuando hay cambios
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, [userId]);

  return { progress, loading, error };
}
```

---

## 🔄 Script de Migración de Datos

Script para migrar datos existentes de localStorage a Supabase:

```typescript
// apps/web/src/lib/migrate-to-supabase.ts
import { supabase, completeLesson } from './supabase';

export async function migrateLocalStorageToSupabase(userId: string) {
  try {
    console.log('🚀 Iniciando migración...');

    // 1. Migrar progreso de lecciones
    const lessonKeys = Object.keys(localStorage).filter(k => k.startsWith('lesson_'));
    
    for (const key of lessonKeys) {
      if (localStorage.getItem(key) === 'completed') {
        const [_, courseId, lessonId] = key.split('_');
        
        try {
          await completeLesson(userId, courseId, `${courseId}_${lessonId}`);
          console.log(`✅ Migrada: ${key}`);
        } catch (err) {
          console.warn(`⚠️ Error migrando ${key}:`, err);
        }
      }
    }

    // 2. Migrar logros
    const achievementsStr = localStorage.getItem('unlocked_achievements');
    if (achievementsStr) {
      const achievements = JSON.parse(achievementsStr);
      
      for (const achievementId of achievements) {
        try {
          await supabase
            .from('user_achievements')
            .insert({
              user_id: userId,
              achievement_id: achievementId,
            });
          console.log(`✅ Logro migrado: ${achievementId}`);
        } catch (err) {
          console.warn(`⚠️ Error migrando logro ${achievementId}:`, err);
        }
      }
    }

    // 3. Migrar notificaciones
    const notificationsStr = localStorage.getItem('app_notifications');
    if (notificationsStr) {
      const notifications = JSON.parse(notificationsStr);
      
      for (const notif of notifications) {
        try {
          await supabase
            .from('notifications')
            .insert({
              user_id: userId,
              type: notif.type,
              title: notif.title,
              message: notif.message,
              icon: notif.icon,
              read: notif.read,
            });
          console.log(`✅ Notificación migrada`);
        } catch (err) {
          console.warn('⚠️ Error migrando notificación:', err);
        }
      }
    }

    console.log('✨ Migración completada con éxito!');
    
    // Opcional: Limpiar localStorage después de migración exitosa
    // if (confirm('¿Limpiar datos locales ahora que están en la nube?')) {
    //   localStorage.clear();
    // }
    
    return { success: true };
  } catch (error) {
    console.error('❌ Error durante la migración:', error);
    return { success: false, error };
  }
}
```

### Uso del script de migración

```typescript
// En un componente o página
import { migrateLocalStorageToSupabase } from '@/lib/migrate-to-supabase';
import { useUser } from '@/hooks/useUser'; // Hook de auth

function MigrationPage() {
  const { user } = useUser();
  
  const handleMigrate = async () => {
    if (!user) {
      alert('Debes estar autenticado para migrar');
      return;
    }
    
    const result = await migrateLocalStorageToSupabase(user.id);
    
    if (result.success) {
      alert('✅ Datos migrados correctamente a la nube');
    } else {
      alert('❌ Error en la migración. Ver consola.');
    }
  };
  
  return (
    <button onClick={handleMigrate}>
      Migrar mis datos a la nube
    </button>
  );
}
```

---

## 🧪 Testing

### 1. Verificar conexión a Supabase

```typescript
// Test básico
import { supabase } from '@/lib/supabase';

async function testConnection() {
  const { data, error } = await supabase
    .from('courses')
    .select('count');
  
  if (error) {
    console.error('❌ Error de conexión:', error);
  } else {
    console.log('✅ Conectado a Supabase. Cursos:', data);
  }
}
```

### 2. Probar funciones RPC

```sql
-- En SQL Editor de Supabase
SELECT complete_lesson(
  'test-user-id'::uuid,
  'py-intro',
  'py-intro_1',
  'print("test")'
);
```

### 3. Test de RLS (Row Level Security)

```typescript
// Verificar que solo puedes ver tus propios datos
const { data } = await supabase
  .from('user_progress')
  .select('*');

console.log('Debería ver solo mis datos:', data);
```

---

## 🚀 Despliegue

### Checklist pre-despliegue

- [ ] Variables de entorno configuradas en producción
- [ ] Schema SQL ejecutado en Supabase
- [ ] RLS habilitado y probado
- [ ] Migraciones probadas en desarrollo
- [ ] Backup de localStorage (por si acaso)
- [ ] Autenticación configurada
- [ ] Tests E2E pasados

### Estrategia de despliegue gradual

**Fase 1: Modo híbrido (Recomendado)**
- Mantener localStorage como fallback
- Escribir a ambos (localStorage + Supabase)
- Leer preferentemente de Supabase, fallback a localStorage

**Fase 2: Solo Supabase**
- Después de 2-4 semanas sin incidencias
- Remover código de localStorage
- Usuarios nuevos solo usan Supabase

**Fase 3: Limpieza**
- Remover imports de localStorage
- Actualizar documentación
- Celebrar 🎉

---

## 📊 Monitoreo

### Dashboard de Supabase

Supabase provee:
- **Database** → Ver tablas y datos en tiempo real
- **Table Editor** → Editar datos manualmente
- **API Logs** → Ver todas las peticiones
- **Auth** → Gestionar usuarios
- **Storage** → Para archivos (futuro)

### Queries útiles

```sql
-- Ver usuarios más activos
SELECT 
  u.display_name,
  u.total_xp,
  u.current_level,
  COUNT(up.id) as lessons_completed
FROM users u
LEFT JOIN user_progress up ON up.user_id = u.id AND up.status = 'completed'
GROUP BY u.id
ORDER BY u.total_xp DESC
LIMIT 10;

-- Ver progreso de un curso específico
SELECT 
  u.display_name,
  uc.progress_percentage,
  uc.lessons_completed,
  uc.status
FROM user_courses uc
JOIN users u ON u.id = uc.user_id
WHERE uc.course_id = 'py-intro'
ORDER BY uc.progress_percentage DESC;

-- Logros más populares
SELECT 
  a.title,
  COUNT(ua.id) as unlocked_count
FROM achievements a
LEFT JOIN user_achievements ua ON ua.achievement_id = a.id
GROUP BY a.id
ORDER BY unlocked_count DESC;
```

---

## 🆘 Troubleshooting

### Error: "Row Level Security policy violation"

**Causa**: El usuario no tiene permisos  
**Solución**: Verifica que las políticas RLS estén correctas

```sql
-- Ver políticas existentes
SELECT * FROM pg_policies WHERE tablename = 'user_progress';

-- Re-crear política si es necesario
DROP POLICY IF EXISTS "Users can view own progress" ON public.user_progress;
CREATE POLICY "Users can view own progress"
  ON public.user_progress FOR SELECT
  USING (auth.uid() = user_id);
```

### Error: "relation does not exist"

**Causa**: Schema no ejecutado correctamente  
**Solución**: Re-ejecutar `schema.sql`

### Lentitud en queries

**Solución**: Añadir índices

```sql
-- Ver queries lentas
SELECT * FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Añadir índice si es necesario
CREATE INDEX idx_user_progress_status 
ON user_progress(user_id, status);
```

---

## 📚 Recursos Adicionales

- **Documentación oficial**: https://supabase.com/docs
- **Ejemplos Next.js**: https://github.com/supabase/supabase/tree/master/examples/auth/nextjs
- **Comunidad**: https://github.com/supabase/supabase/discussions
- **Discord**: https://discord.supabase.com

---

## ✅ Checklist Final

- [ ] Cuenta de Supabase creada
- [ ] Schema SQL ejecutado
- [ ] Variables de entorno configuradas
- [ ] Helper client creado (`lib/supabase.ts`)
- [ ] Componentes actualizados
- [ ] Hook `useSupabaseProgress` implementado
- [ ] Script de migración probado
- [ ] Tests pasados
- [ ] RLS verificado
- [ ] Desplegado en producción
- [ ] Usuarios migrados
- [ ] Monitoreo activo

---

<div align="center">

**¡Listo para migrar a la nube! 🚀**

Si tienes dudas, abre un issue en GitHub

</div>
