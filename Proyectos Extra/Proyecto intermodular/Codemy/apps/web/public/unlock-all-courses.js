// Script para desbloquear TODAS las lecciones para dariolacal94@gmail.com
// Ejecutar desde la consola del navegador (F12)

function unlockAllLessons() {
  console.log('🔓 Desbloqueando TODAS las lecciones de TODOS los cursos...');
  console.log('👤 Usuario: dariolacal94@gmail.com\n');
  
  const courses = {
    'py-intro': 4,       // Introducción a Python
    'py-variables': 5,   // Variables y Tipos de Datos
    'py-control': 6,     // Control de Flujo
    'py-functions': 6,   // Funciones en Python
    'py-classes': 6,     // Programación Orientada a Objetos
    'py-files': 6,       // Archivos y Persistencia
  };

  let totalUnlocked = 0;
  const results = [];

  Object.entries(courses).forEach(([courseId, lessonCount]) => {
    console.log(`📚 Curso: ${courseId}`);
    
    for (let i = 1; i <= lessonCount; i++) {
      const key = `lesson_${courseId}_${i}`;
      // Marcar como completada para desbloquear todas las siguientes
      localStorage.setItem(key, 'completed');
      totalUnlocked++;
      console.log(`  ✅ Lección ${i}/${lessonCount} desbloqueada`);
    }
    
    results.push({ course: courseId, lessons: lessonCount });
    console.log(`  ✔️  ${lessonCount} lecciones completadas\n`);
  });

  console.log('━'.repeat(50));
  console.log(`🎉 ¡COMPLETADO!`);
  console.log(`📊 Total: ${totalUnlocked} lecciones desbloqueadas`);
  console.log(`📚 Cursos afectados: ${Object.keys(courses).length}`);
  console.log('🔄 RECARGA LA PÁGINA para ver los cambios');
  console.log('━'.repeat(50));
  
  return {
    success: true,
    totalLessons: totalUnlocked,
    totalCourses: Object.keys(courses).length,
    details: results,
    message: '¡Todas las lecciones desbloqueadas! Recarga la página (F5 o Ctrl+R)'
  };
}

// Ejecutar automáticamente al cargar el script
const result = unlockAllLessons();
console.log('\n📋 Resultado:', result);
