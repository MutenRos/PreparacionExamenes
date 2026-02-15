const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  'https://oubxugjtcxtvreyllsrb.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im91Ynh1Z2p0Y3h0dnJleWxsc3JiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzA2MjExOSwiZXhwIjoyMDc4NjM4MTE5fQ.8k-aiCQaOD5iMWmThB-keBpsNzgGFwGW02uknlXf72U'
);

async function updateFundamentals() {
  console.log('🔄 Actualizando curso fundamentals en la base de datos...');
  
  // Primero eliminar las lecciones antiguas
  const { error: deleteError } = await supabase
    .from('lessons')
    .delete()
    .eq('course_id', 'fundamentals');
  
  if (deleteError) {
    console.error('❌ Error eliminando lecciones:', deleteError);
    return;
  }
  
  console.log('✅ Lecciones antiguas eliminadas');
  
  // Crear las 6 nuevas lecciones
  const lessons = [
    { id: 'fundamentals-1', course_id: 'fundamentals', lesson_number: 1, title: 'Introducción a la Programación', xp: 50 },
    { id: 'fundamentals-2', course_id: 'fundamentals', lesson_number: 2, title: 'Variables y Datos', xp: 50 },
    { id: 'fundamentals-3', course_id: 'fundamentals', lesson_number: 3, title: 'Estructuras de Control: Decisiones', xp: 50 },
    { id: 'fundamentals-4', course_id: 'fundamentals', lesson_number: 4, title: 'Estructuras de Control: Bucles', xp: 50 },
    { id: 'fundamentals-5', course_id: 'fundamentals', lesson_number: 5, title: 'Funciones y Modularidad', xp: 50 },
    { id: 'fundamentals-6', course_id: 'fundamentals', lesson_number: 6, title: 'Resolución de Problemas y Pensamiento Algorítmico', xp: 50 }
  ];
  
  const { data, error } = await supabase
    .from('lessons')
    .insert(lessons);
  
  if (error) {
    console.error('❌ Error insertando lecciones:', error);
    return;
  }
  
  console.log('✅ 6 lecciones creadas exitosamente');
  
  // Actualizar el título y descripción del curso
  const { error: updateError } = await supabase
    .from('courses')
    .update({
      title: 'Fundamentos: Piensa como un Programador',
      description: 'Aprende los conceptos básicos de programación y desarrolla tu pensamiento lógico'
    })
    .eq('id', 'fundamentals');
  
  if (updateError) {
    console.error('❌ Error actualizando curso:', updateError);
    return;
  }
  
  console.log('✅ Curso actualizado en la base de datos');
  console.log('');
  console.log('🎉 Proceso completado! Ahora el curso tiene 6 lecciones completas.');
}

updateFundamentals().catch(console.error);
