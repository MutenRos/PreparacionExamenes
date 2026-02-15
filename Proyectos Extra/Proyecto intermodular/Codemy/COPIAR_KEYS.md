# 🔑 PASO FINAL: Copiar las API Keys de Supabase

## Tu proyecto está casi listo!

Solo faltan 2 valores en el archivo `.env.local`:

### Pasos para copiar las keys:

1. **Abre el navegador** en: https://supabase.com/dashboard/project/oubxugjtcxtvreyllsrb/settings/api

2. **Busca la sección "Project API keys"** (bajando un poco)

3. **Copia estos 2 valores:**

   #### 📋 anon / public key
   - Aparece como: `anon` `public`
   - Es una key LARGA que empieza con: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **Cópiala completa**

   #### 📋 service_role key  
   - Aparece como: `service_role` `secret` 
   - También es MUY larga, empieza con: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **Cópiala completa**

4. **Pega ambas keys en el archivo:**
   ```
   apps/web/.env.local
   ```

   Reemplaza estas dos líneas:
   ```env
   NEXT_PUBLIC_SUPABASE_ANON_KEY=PENDIENTE_COPIAR_DEL_DASHBOARD
   SUPABASE_SERVICE_ROLE_KEY=PENDIENTE_COPIAR_DEL_DASHBOARD
   ```

   Por tus keys reales:
   ```env
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu_key_aqui...
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu_key_aqui...
   ```

5. **Guarda el archivo** y listo!

---

## ✅ Después de copiar las keys:

Reinicia el servidor:
```bash
cd apps/web
npm run dev
```

Y ya funcionará el registro de usuarios! 🎉

---

## ⚠️ Importante:
- Las keys son MUY largas (cientos de caracteres)
- NO agregues espacios ni saltos de línea
- Cópialas COMPLETAS desde Supabase
- La `anon key` es segura compartir (es pública)
- La `service_role key` es SECRETA (no la subas a GitHub)
