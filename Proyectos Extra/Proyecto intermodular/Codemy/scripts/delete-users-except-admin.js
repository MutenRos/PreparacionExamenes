#!/usr/bin/env node

/**
 * Script para eliminar todos los usuarios de Supabase excepto dariolacal94@gmail.com
 * 
 * Uso: node scripts/delete-users-except-admin.js
 */

const { createClient } = require('@supabase/supabase-js');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const ADMIN_EMAIL = 'dariolacal94@gmail.com';

// Leer variables de entorno desde .env.local
function loadEnv() {
  const envPath = path.join(__dirname, '..', '.env.local');
  if (!fs.existsSync(envPath)) {
    return {};
  }
  
  const envFile = fs.readFileSync(envPath, 'utf8');
  const env = {};
  
  envFile.split('\n').forEach(line => {
    const match = line.match(/^([^=:#]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim().replace(/^["']|["']$/g, '');
      env[key] = value;
    }
  });
  
  return env;
}

const env = loadEnv();
const supabaseUrl = env.NEXT_PUBLIC_SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseServiceKey = env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('❌ Error: Variables de entorno no configuradas');
  console.error('Asegúrate de tener NEXT_PUBLIC_SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en .env.local');
  process.exit(1);
}

// Cliente con service role para operaciones admin
const supabase = createClient(supabaseUrl, supabaseServiceKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false
  }
});

async function askConfirmation(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

async function deleteUsers() {
  console.log('\n🔍 Buscando usuarios en Supabase...\n');

  try {
    // Obtener todos los usuarios
    const { data: { users }, error: listError } = await supabase.auth.admin.listUsers();

    if (listError) {
      console.error('❌ Error al listar usuarios:', listError.message);
      process.exit(1);
    }

    if (!users || users.length === 0) {
      console.log('ℹ️  No hay usuarios en la base de datos');
      return;
    }

    console.log(`📊 Total de usuarios encontrados: ${users.length}\n`);

    // Filtrar usuarios que NO son el admin
    const usersToDelete = users.filter(user => user.email !== ADMIN_EMAIL);
    const adminUser = users.find(user => user.email === ADMIN_EMAIL);

    if (adminUser) {
      console.log(`✅ Usuario admin encontrado: ${adminUser.email} (ID: ${adminUser.id})`);
    } else {
      console.log(`⚠️  Usuario admin NO encontrado: ${ADMIN_EMAIL}`);
    }

    console.log(`\n🗑️  Usuarios a eliminar: ${usersToDelete.length}\n`);

    if (usersToDelete.length === 0) {
      console.log('ℹ️  No hay usuarios para eliminar');
      return;
    }

    // Mostrar lista de usuarios a eliminar
    usersToDelete.forEach((user, index) => {
      console.log(`   ${index + 1}. ${user.email || 'Sin email'} (ID: ${user.id})`);
    });

    console.log('\n');

    // Pedir confirmación
    const confirmed = await askConfirmation(
      `⚠️  ¿Estás seguro de eliminar ${usersToDelete.length} usuario(s)? (y/N): `
    );

    if (!confirmed) {
      console.log('\n❌ Operación cancelada por el usuario');
      process.exit(0);
    }

    console.log('\n🗑️  Eliminando usuarios...\n');

    let deletedCount = 0;
    let errorCount = 0;

    // Eliminar usuarios uno por uno
    for (const user of usersToDelete) {
      try {
        const { error } = await supabase.auth.admin.deleteUser(user.id);
        
        if (error) {
          console.error(`   ❌ Error al eliminar ${user.email}: ${error.message}`);
          errorCount++;
        } else {
          console.log(`   ✅ Eliminado: ${user.email || 'Sin email'}`);
          deletedCount++;
        }
      } catch (err) {
        console.error(`   ❌ Error al eliminar ${user.email}:`, err.message);
        errorCount++;
      }
    }

    console.log('\n📊 Resumen:');
    console.log(`   ✅ Usuarios eliminados: ${deletedCount}`);
    console.log(`   ❌ Errores: ${errorCount}`);
    console.log(`   👤 Usuario admin preservado: ${ADMIN_EMAIL}`);
    console.log('\n✅ Proceso completado\n');

  } catch (error) {
    console.error('\n❌ Error general:', error.message);
    process.exit(1);
  }
}

// Ejecutar
deleteUsers().catch(error => {
  console.error('❌ Error fatal:', error);
  process.exit(1);
});
