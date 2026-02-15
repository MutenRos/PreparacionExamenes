const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Leer variables de entorno del archivo .env.local
const envPath = path.join(__dirname, '../.env.local');
const envContent = fs.readFileSync(envPath, 'utf-8');
const env = {};
envContent.split('\n').forEach(line => {
  const [key, ...valueParts] = line.split('=');
  if (key && valueParts.length > 0) {
    env[key.trim()] = valueParts.join('=').trim();
  }
});

const supabase = createClient(
  env.NEXT_PUBLIC_SUPABASE_URL,
  env.SUPABASE_SERVICE_ROLE_KEY
);

async function cleanFundamentals() {
  try {
    console.log('🗑️  Eliminando lecciones viejas de fundamentals de Supabase...');
    
    // Eliminar todas las lecciones del curso fundamentals
    const { error: deleteError } = await supabase
      .from('lessons')
      .delete()
      .eq('course_id', 'fundamentals');
    
    if (deleteError) {
      console.error('❌ Error al eliminar lecciones:', deleteError);
      return;
    }
    
    console.log('✅ Lecciones eliminadas exitosamente');
    console.log('ℹ️  Ahora el curso fundamentals usará solo las lecciones del archivo fundamentals.ts');
    
  } catch (error) {
    console.error('Error:', error);
  }
}

cleanFundamentals();
