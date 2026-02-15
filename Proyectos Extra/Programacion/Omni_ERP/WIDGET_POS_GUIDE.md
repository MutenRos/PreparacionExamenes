# 🛒 POS Widget - Feature PRO

## Descripción

El **POS Widget** permite a tus clientes vender sus productos directamente en sus sitios web, manteniendo el inventario sincronizado con OmniERP en tiempo real.

## Características

✅ **Sincronización en Tiempo Real**: El inventario se actualiza automáticamente  
✅ **Carrito de Compras**: Sistema de carrito embebible en cualquier web  
✅ **Múltiples Widgets**: Crea widgets diferentes para diferentes productos  
✅ **Seguro**: Tokens únicos para cada widget, validación de origen  
✅ **Personalizable**: Colores, iconos, configuración flexible  
✅ **Sin Autenticación**: Los clientes no necesitan login para comprar  

## Cómo Usar

### 1. Crear un Widget

1. Ve a **POS → Widgets POS** (en el menú)
2. Haz click en **"+ Nuevo Widget"**
3. Completa la información:
   - **Nombre**: Nombre del widget (ej: "Tienda Online")
   - **URL Permitida**: El dominio donde se embebe (ej: https://mitienda.com)
   - **Colores**: Personaliza los colores primarios y del botón
   - **Opciones**: Elige qué mostrar (precios, stock, etc.)

4. Haz click en **"Guardar Widget"**

### 2. Embeber en tu Sitio Web

Una vez creado el widget, verás un código como este:

```html
<div id="omnierp-pos-widget"></div>
<script src="https://omnierp.com/static/widget-pos.js" data-token="YOUR_TOKEN"></script>
```

**Pasos:**

1. Copia el código completo (hay un botón "📋 Copiar Código")
2. Ve a tu sitio web (en el HTML donde quieras el carrito)
3. Pega el código en el `<body>` o donde desees que aparezca
4. ¡Listo! El widget aparecerá automáticamente

### 3. Configuración Avanzada

En el widget puedes filtrar:
- **Categorías específicas**: Solo mostrar ciertos productos
- **Productos específicos**: Solo los que selecciones
- **Stock disponible**: Solo mostrar productos en stock

## Ejemplo HTML Completo

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mi Tienda</title>
</head>
<body>
    <h1>Bienvenido a Mi Tienda</h1>
    
    <!-- Widget POS aquí -->
    <div id="omnierp-pos-widget"></div>
    <script src="https://omnierp.com/static/widget-pos.js" data-token="ABC123..."></script>
    
</body>
</html>
```

## Características del Widget

### Para el Cliente (Visitante de tu Web)

- 🛍️ **Catálogo**: Ve todos los productos disponibles
- 🛒 **Carrito**: Agrega productos y edita cantidades
- 💳 **Compra Rápida**: Completa la compra en segundos
- 📱 **Responsive**: Funciona en móvil y desktop

### Para ti (Administrador)

- 📊 **Dashboard**: Ve todas las compras del widget
- 🔧 **Control**: Edita o desactiva widgets cuando quieras
- 📈 **Analytics**: Cada venta queda registrada en OmniERP
- 🎨 **Personalización**: Cada widget puede tener colores diferentes

## Seguridad

✅ **Token único**: Cada widget tiene un token especial  
✅ **Validación de origen**: Solo funciona en el dominio permitido  
✅ **Sin datos sensibles**: No expone información de tu negocio  
✅ **Encriptado**: La comunicación es segura HTTPS  

## Transacciones

Cada compra realizada en el widget genera:
- ✅ Una venta POS registrada
- ✅ Actualización del inventario
- ✅ Número de transacción único
- ✅ Total con impuestos calculados

## Límites PRO

Este feature está disponible **solo para suscriptores PRO**. Puedes crear widgets ilimitados.

## Soporte

¿Problemas? Revisa:
1. El token sea válido
2. La URL permitida coincida con tu dominio
3. El widget esté activo (no desactivado)
4. La consola de errores del navegador (F12)

---

**¡Empieza a vender hoy mismo! 🚀**
