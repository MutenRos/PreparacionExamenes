#!/usr/bin/env node

/**
 * Script para configurar Supabase Email Verification
 * Ejecutar: node scripts/configure-supabase.js
 */

const { createClient } = require('@supabase/supabase-js');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

// Colores para la terminal
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function main() {
  console.log('\n');
  log('🚀 Configuración de Email Verification en Supabase', 'cyan');
  log('====================================================', 'cyan');
  console.log('\n');

  // Instrucciones
  log('📝 Necesitas tu información de Supabase:', 'blue');
  log('   Ve a: https://app.supabase.com/project/_/settings/api', 'blue');
  console.log('\n');

  // Obtener credenciales
  const supabaseUrl = await question('Ingresa tu SUPABASE_URL: ');
  const serviceRoleKey = await question('Ingresa tu SERVICE_ROLE_KEY: ');

  console.log('\n');
  log('🔧 Conectando a Supabase...', 'blue');

  // Crear cliente con service role (admin)
  const supabase = createClient(supabaseUrl, serviceRoleKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  });

  // Verificar conexión
  try {
    const { data, error } = await supabase.from('_test').select('*').limit(1);
    if (error && !error.message.includes('relation "_test" does not exist')) {
      throw error;
    }
    log('✅ Conexión exitosa', 'green');
  } catch (error) {
    log(`❌ Error de conexión: ${error.message}`, 'red');
    process.exit(1);
  }

  console.log('\n');
  log('📊 Verificando configuración actual...', 'blue');

  // Verificar usuarios
  try {
    const { data: users, error } = await supabase.auth.admin.listUsers();
    
    if (error) throw error;

    log(`   Total de usuarios: ${users.users.length}`, 'cyan');
    
    const verified = users.users.filter(u => u.email_confirmed_at).length;
    const unverified = users.users.length - verified;
    
    log(`   Verificados: ${verified}`, 'green');
    log(`   No verificados: ${unverified}`, 'yellow');
    
  } catch (error) {
    log(`   ⚠️  No se pudo obtener estadísticas: ${error.message}`, 'yellow');
  }

  console.log('\n');
  log('📧 Configuración de Email Templates', 'blue');
  log('====================================', 'blue');
  console.log('\n');
  
  log('⚠️  Los email templates deben configurarse manualmente en el dashboard:', 'yellow');
  console.log('\n');
  log('1. Ve a: Authentication → Email Templates → Confirm signup', 'cyan');
  console.log('\n');
  log('2. Usa este template HTML:', 'cyan');
  console.log('\n');
  
  const emailTemplate = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifica tu email - CodeAcademy</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #0f172a;">
  <table role="presentation" style="width: 100%; border-collapse: collapse;">
    <tr>
      <td align="center" style="padding: 40px 0;">
        <table role="presentation" style="width: 600px; border-collapse: collapse;">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(to right, #9333ea, #ec4899); padding: 40px; text-align: center; border-radius: 8px 8px 0 0;">
              <h1 style="margin: 0; color: white; font-size: 32px; font-weight: bold;">CodeAcademy</h1>
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td style="background-color: #1e293b; padding: 40px; border-radius: 0 0 8px 8px;">
              <h2 style="color: white; margin-top: 0;">¡Bienvenido a CodeAcademy! 🎉</h2>
              <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                Estás a un paso de comenzar tu viaje en programación.
              </p>
              <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                Haz clic en el botón para verificar tu cuenta:
              </p>
              <!-- Button -->
              <table role="presentation" style="margin: 30px 0;">
                <tr>
                  <td align="center">
                    <a href="{{ .ConfirmationURL }}" 
                       style="background: linear-gradient(to right, #9333ea, #ec4899); 
                              color: white; 
                              padding: 16px 32px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              display: inline-block;
                              font-weight: bold;
                              font-size: 16px;">
                      Verificar mi email
                    </a>
                  </td>
                </tr>
              </table>
              <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">
                O copia y pega esta URL en tu navegador:
              </p>
              <p style="background-color: #0f172a; 
                        padding: 12px; 
                        border-radius: 4px; 
                        color: #a78bfa; 
                        font-size: 12px; 
                        word-break: break-all;
                        border: 1px solid #334155;">
                {{ .ConfirmationURL }}
              </p>
              <hr style="border: none; border-top: 1px solid #334155; margin: 30px 0;">
              <p style="color: #64748b; font-size: 12px; line-height: 1.6; margin: 0;">
                Si no creaste una cuenta en CodeAcademy, puedes ignorar este email.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;

  log('--- COPIAR DESDE AQUÍ ---', 'green');
  console.log(emailTemplate);
  log('--- HASTA AQUÍ ---', 'green');

  console.log('\n');
  log('3. Configurar Redirect URLs:', 'cyan');
  log('   Ve a: Authentication → URL Configuration', 'cyan');
  console.log('\n');
  log('   Agrega estas URLs:', 'yellow');
  log('   - http://localhost:3000/auth/verify-email', 'cyan');
  log('   - http://192.168.1.157:3000/auth/verify-email', 'cyan');
  log('   - http://88.17.157.221:3000/auth/verify-email', 'cyan');
  console.log('\n');

  log('4. Habilitar Email Confirmation:', 'cyan');
  log('   Ve a: Authentication → Providers → Email', 'cyan');
  log('   Asegúrate que "Confirm email" esté habilitado ✓', 'yellow');
  console.log('\n');

  console.log('\n');
  log('✅ Script completado', 'green');
  console.log('\n');
  log('🧪 Para testear:', 'blue');
  log('1. npm run dev', 'cyan');
  log('2. Ve a http://localhost:3000/auth/register', 'cyan');
  log('3. Crea una cuenta con un email real', 'cyan');
  log('4. Revisa tu inbox y haz clic en el enlace', 'cyan');
  console.log('\n');

  rl.close();
}

main().catch((error) => {
  log(`❌ Error: ${error.message}`, 'red');
  console.error(error);
  process.exit(1);
});
