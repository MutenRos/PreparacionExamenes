/**
 * Script para poblar la base de datos de Supabase con todos los cursos
 */

import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Faltan variables de entorno NEXT_PUBLIC_SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

interface CourseModule {
  id: string;
  title: string;
  description: string;
  lessons: Array<{
    title: string;
    content: string;
  }>;
}

async function getCourseFiles() {
  const coursesDir = path.join(process.cwd(), 'apps/web/src/data/courses');
  const files = fs.readdirSync(coursesDir);
  
  return files
    .filter(f => f.endsWith('.ts') && f !== 'index.ts')
    .map(f => path.join(coursesDir, f));
}

async function extractCourseData(filePath: string): Promise<CourseModule | null> {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Extraer el nombre de la variable exportada
    const exportMatch = content.match(/export const (\w+) = {/);
    if (!exportMatch) return null;
    
    // Extraer id
    const idMatch = content.match(/id: ['"]([^'"]+)['"]/);
    if (!idMatch) return null;
    
    // Extraer title
    const titleMatch = content.match(/title: ['"]([^'"]+)['"]/);
    if (!titleMatch) return null;
    
    // Extraer description
    const descriptionMatch = content.match(/description: ['"]([^'"]+)['"]/);
    
    // Contar lecciones
    const lessonsMatches = content.match(/{\s*title:/g);
    const lessonsCount = lessonsMatches ? lessonsMatches.length : 2;
    
    return {
      id: idMatch[1],
      title: titleMatch[1],
      description: descriptionMatch ? descriptionMatch[1] : '',
      lessons: Array(lessonsCount).fill(null).map((_, i) => ({
        title: `Lección ${i + 1}`,
        content: ''
      }))
    };
  } catch (error) {
    console.error(`Error procesando ${filePath}:`, error);
    return null;
  }
}

function getCategoryFromId(id: string): string {
  if (id.startsWith('py-')) return 'python';
  if (id.startsWith('js-')) return 'javascript';
  if (id.startsWith('web-')) return 'web';
  if (id.startsWith('java-')) return 'java';
  if (id.startsWith('cpp-')) return 'cpp';
  if (id.startsWith('arduino-')) return 'arduino';
  if (id.includes('react')) return 'react';
  if (id.includes('next')) return 'nextjs';
  if (id.includes('node')) return 'nodejs';
  if (id.includes('sql') || id.includes('database') || id.includes('postgres') || id.includes('mongodb')) return 'database';
  if (id.includes('docker') || id.includes('kubernetes') || id.includes('devops')) return 'devops';
  if (id.includes('security') || id.includes('pentesting')) return 'security';
  if (id.includes('3d') || id.includes('blender') || id.includes('fusion')) return '3d';
  if (id.includes('dam-') || id.includes('smr-')) return 'ciclo';
  return 'general';
}

function getDifficulty(id: string): string {
  if (id.includes('intro') || id.includes('fundament')) return 'foundation';
  if (id.includes('advanced') || id.includes('master')) return 'advanced';
  if (id.includes('expert')) return 'expert';
  return 'intermediate';
}

async function populateCourses() {
  console.log('🚀 Iniciando población de cursos...\n');
  
  const courseFiles = await getCourseFiles();
  console.log(`📚 Encontrados ${courseFiles.length} archivos de cursos\n`);
  
  let inserted = 0;
  let updated = 0;
  let errors = 0;
  
  for (const filePath of courseFiles) {
    const courseData = await extractCourseData(filePath);
    
    if (!courseData) {
      console.log(`⏭️  Saltando ${path.basename(filePath)} (no se pudo extraer datos)`);
      errors++;
      continue;
    }
    
    const category = getCategoryFromId(courseData.id);
    const difficulty = getDifficulty(courseData.id);
    const totalLessons = courseData.lessons.length;
    const xpPerLesson = 50;
    const totalXp = totalLessons * xpPerLesson + 100; // +100 bonus
    
    // Insertar o actualizar curso
    const { data: existingCourse } = await supabase
      .from('courses')
      .select('id')
      .eq('id', courseData.id)
      .single();
    
    if (existingCourse) {
      // Actualizar
      const { error } = await supabase
        .from('courses')
        .update({
          title: courseData.title,
          description: courseData.description,
          category,
          difficulty,
          total_lessons: totalLessons,
          total_xp: totalXp,
          xp_per_lesson: xpPerLesson,
          bonus_xp: 100,
          updated_at: new Date().toISOString()
        })
        .eq('id', courseData.id);
      
      if (error) {
        console.log(`❌ Error actualizando ${courseData.id}:`, error.message);
        errors++;
      } else {
        console.log(`✅ Actualizado: ${courseData.id} - ${courseData.title}`);
        updated++;
      }
    } else {
      // Insertar
      const { error } = await supabase
        .from('courses')
        .insert({
          id: courseData.id,
          title: courseData.title,
          description: courseData.description,
          icon: '📚',
          category,
          difficulty,
          total_lessons: totalLessons,
          total_xp: totalXp,
          xp_per_lesson: xpPerLesson,
          bonus_xp: 100,
          is_active: true
        });
      
      if (error) {
        console.log(`❌ Error insertando ${courseData.id}:`, error.message);
        errors++;
      } else {
        console.log(`✅ Insertado: ${courseData.id} - ${courseData.title}`);
        inserted++;
      }
    }
    
    // Insertar lecciones
    for (let i = 0; i < courseData.lessons.length; i++) {
      const lesson = courseData.lessons[i];
      const lessonId = `${courseData.id}-lesson-${i + 1}`;
      
      const { error: lessonError } = await supabase
        .from('lessons')
        .upsert({
          id: lessonId,
          course_id: courseData.id,
          lesson_number: i + 1,
          title: lesson.title,
          duration: '30 min',
          xp: xpPerLesson,
          is_active: true
        }, {
          onConflict: 'id'
        });
      
      if (lessonError) {
        console.log(`  ⚠️  Error con lección ${i + 1}: ${lessonError.message}`);
      }
    }
  }
  
  console.log('\n📊 Resumen:');
  console.log(`✅ Insertados: ${inserted}`);
  console.log(`🔄 Actualizados: ${updated}`);
  console.log(`❌ Errores: ${errors}`);
  console.log(`📚 Total procesados: ${courseFiles.length}`);
}

populateCourses()
  .then(() => {
    console.log('\n✨ Proceso completado!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\n💥 Error fatal:', error);
    process.exit(1);
  });
