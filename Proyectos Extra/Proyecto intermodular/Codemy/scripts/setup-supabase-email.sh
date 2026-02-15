#!/bin/bash

# Script para configurar Supabase Email Verification
# Ejecutar: bash scripts/setup-supabase-email.sh

set -e

echo "🚀 Configuración de Email Verification en Supabase"
echo "=================================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Supabase CLI
if ! command -v supabase &> /dev/null; then
    echo -e "${YELLOW}⚠️  Supabase CLI no está instalado${NC}"
    echo ""
    echo "Instalando Supabase CLI..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -L https://github.com/supabase/cli/releases/latest/download/supabase_linux_amd64.tar.gz | tar -xz
        sudo mv supabase /usr/local/bin/
        echo -e "${GREEN}✅ Supabase CLI instalado${NC}"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install supabase/tap/supabase
        echo -e "${GREEN}✅ Supabase CLI instalado${NC}"
    else
        echo -e "${RED}❌ Sistema operativo no soportado. Instala manualmente desde: https://supabase.com/docs/guides/cli${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}📝 Necesitas configurar tu proyecto de Supabase${NC}"
echo ""
echo "Ve a: https://app.supabase.com/project/_/settings/api"
echo ""

# Pedir datos del proyecto
read -p "Ingresa tu SUPABASE_URL (https://xxxxx.supabase.co): " SUPABASE_URL
read -p "Ingresa tu ANON_KEY (eyJhbGciOi...): " ANON_KEY
read -p "Ingresa tu SERVICE_ROLE_KEY (eyJhbGciOi...): " SERVICE_ROLE_KEY

# Crear/actualizar .env.local en la raíz
echo ""
echo -e "${BLUE}📄 Actualizando .env.local...${NC}"

cat > .env.local << EOF
# =============================================
# CodeAcademy - Variables de Entorno LOCAL
# MVP AAA - Academia completa de programación
# =============================================

# ===== SUPABASE =====
NEXT_PUBLIC_SUPABASE_URL=$SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=$ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY

# ===== STRIPE (Desarrollo) =====
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_demo
STRIPE_SECRET_KEY=sk_test_demo
STRIPE_WEBHOOK_SECRET=whsec_demo

# ===== ANALYTICS =====
NEXT_PUBLIC_POSTHOG_KEY=phc_demo
SENTRY_DSN=your_sentry_dsn

# ===== CODE RUNNER =====
CODE_RUNNER_API_URL=http://localhost:8080
CODE_RUNNER_API_KEY=dev_key_demo

# ===== AI =====
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
EOF

# Crear/actualizar .env.local en apps/web
cat > apps/web/.env.local << EOF
# Supabase
NEXT_PUBLIC_SUPABASE_URL=$SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=$ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_demo
STRIPE_SECRET_KEY=sk_test_demo
STRIPE_WEBHOOK_SECRET=whsec_demo

# Analytics
NEXT_PUBLIC_POSTHOG_KEY=phc_demo
SENTRY_DSN=your_sentry_dsn

# Code Runner
CODE_RUNNER_API_URL=http://localhost:8080
CODE_RUNNER_API_KEY=dev_key_demo

# AI
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
EOF

echo -e "${GREEN}✅ Variables de entorno actualizadas${NC}"

echo ""
echo -e "${BLUE}🔧 Configuración Manual en Supabase Dashboard${NC}"
echo "=================================================="
echo ""
echo "1. Ve a tu proyecto en: https://app.supabase.com"
echo ""
echo "2. ${YELLOW}Authentication → Email Templates → Confirm signup${NC}"
echo "   Copia y pega este template:"
echo ""
echo "---"
cat << 'TEMPLATE'
<!DOCTYPE html>
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
</html>
TEMPLATE
echo "---"
echo ""
echo "3. ${YELLOW}Authentication → URL Configuration${NC}"
echo "   Agrega estas Redirect URLs:"
echo "   - http://localhost:3000/auth/verify-email"
echo "   - http://192.168.1.157:3000/auth/verify-email"
echo "   - http://88.17.157.221:3000/auth/verify-email"
if [ ! -z "$SUPABASE_URL" ]; then
    DOMAIN=$(echo $SUPABASE_URL | sed 's|https://||' | sed 's|http://||')
    echo "   - https://$DOMAIN/auth/verify-email (si usas dominio custom)"
fi
echo ""
echo "   Site URL: http://localhost:3000"
echo ""
echo "4. ${YELLOW}Authentication → Providers → Email${NC}"
echo "   - Asegúrate que 'Email' esté habilitado"
echo "   - Habilita 'Confirm email' ✓"
echo ""
echo "5. ${YELLOW}[OPCIONAL] Project Settings → Auth → SMTP Settings${NC}"
echo "   Para producción, configura SMTP custom (SendGrid, Mailgun, etc.)"
echo ""
echo -e "${GREEN}✅ Configuración completa!${NC}"
echo ""
echo -e "${BLUE}🧪 Para testear:${NC}"
echo "1. npm run dev"
echo "2. Ve a http://localhost:3000/auth/register"
echo "3. Crea una cuenta con un email real"
echo "4. Revisa tu inbox y haz clic en el enlace"
echo ""
echo -e "${GREEN}🎉 ¡Listo para usar!${NC}"
