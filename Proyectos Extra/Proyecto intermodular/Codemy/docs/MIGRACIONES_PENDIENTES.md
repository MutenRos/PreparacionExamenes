# Aplicar Migraciones de Base de Datos

## Migraciones Pendientes

1. **20241116000000_create_purchases.sql** - Sistema de pagos PayPal
2. **20241116000001_create_pioneer_system.sql** - Sistema de usuarios pioneros (primeros 100)

## Opción 1: Desde la CLI de Supabase (Local)

```bash
cd /home/dario/codeacademy
supabase db push
```

## Opción 2: Desde el Dashboard de Supabase (Web)

1. Ve a https://supabase.com/dashboard/project/YOUR_PROJECT_ID
2. Navega a **SQL Editor**
3. Crea una nueva query
4. Copia y pega el contenido de cada archivo de migración en orden:
   - Primero: `supabase/migrations/20241116000000_create_purchases.sql`
   - Segundo: `supabase/migrations/20241116000001_create_pioneer_system.sql`
5. Ejecuta cada query haciendo clic en **Run**

## Opción 3: Copiar y ejecutar manualmente

### Migración 1: Sistema de Compras

```bash
cd /home/dario/codeacademy
cat supabase/migrations/20241116000000_create_purchases.sql
```

Copia el contenido y ejecútalo en el SQL Editor de Supabase.

### Migración 2: Sistema de Pioneros

```bash
cat supabase/migrations/20241116000001_create_pioneer_system.sql
```

Copia el contenido y ejecútalo en el SQL Editor de Supabase.

## Verificar que las migraciones se aplicaron correctamente

Ejecuta en SQL Editor:

```sql
-- Verificar tabla purchases
SELECT COUNT(*) FROM purchases;

-- Verificar tabla pioneer_users
SELECT COUNT(*) FROM pioneer_users;

-- Verificar tabla pioneer_config
SELECT * FROM pioneer_config;

-- Verificar función is_pioneer_user
SELECT is_pioneer_user('00000000-0000-0000-0000-000000000000');

-- Verificar slots disponibles
SELECT get_pioneer_slots_remaining();
```

Deberías ver:
- `pioneer_config` con `slots_remaining = 100`
- Las funciones deberían ejecutarse sin error
- Las tablas deberían existir sin errores

## Siguiente paso

Una vez aplicadas las migraciones, el sistema estará listo para:
- ✅ Registrar pagos de PayPal
- ✅ Asignar automáticamente status de pionero a los primeros 100 usuarios
- ✅ Verificar acceso basado en suscripción o status pionero
