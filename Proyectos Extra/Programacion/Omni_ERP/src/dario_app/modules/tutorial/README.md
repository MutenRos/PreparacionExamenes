# 🎮 Sistema de Tutorial Interactivo

Tutorial tipo videojuego para nuevos usuarios del ERP Dario. Muestra todas las funciones principales con popups, highlights y navegación fluida.

## 📋 Características

### ✨ Experiencia de Usuario
- **15 pasos progresivos** cubriendo todos los módulos
- **Popups animados** con explicaciones claras
- **Highlights dinámicos** que resaltan elementos en la pantalla
- **Barra de progreso** en tiempo real (4px en la parte superior)
- **Botón flotante de ayuda** para reiniciar en cualquier momento
- **Atajos de teclado**:
  - `→` o `Espacio`: Siguiente paso
  - `←`: Paso anterior
  - `ESC`: Cerrar tutorial
  - `?`: Reiniciar tutorial

### 🎯 Flujo del Tutorial

1. **Bienvenida** - Modal inicial con opciones de iniciar o saltar
2. **Dashboard** - Centro de control y KPIs
3. **Ventas** - Gestión de órdenes y facturas
4. **Compras** - Control de proveedores
5. **Inventario** - Manejo de stock
6. **Clientes** - Base de datos de clientes
7. **Calendario** - Planificación y citas
8. **Documentos** - Centro de documentación
9. **Automatizaciones** - Reglas sin Zapier
10. **Reportes** - Análisis y gráficos
11. **Punto de Venta** - Caja rápida
12. **Usuarios y Roles** - Control de acceso
13. **Configuración** - Personalización
14. **Consejos** - Tips útiles
15. **Finalización** - Modal de celebración

### 🔒 Privacidad y Control

- **Se guarda en BD**: Qué paso vio cada usuario
- **No es obligatorio**: Puede saltarse en cualquier momento
- **Se reinicia**: Usuario puede reiniciar desde botón flotante
- **Por organización**: Cada tenant tiene su propio historial

## 🛠️ Integración

### 1. Incluir JS y CSS en el template

En `templates/base.html` o `templates/dashboard.html`, agregar en el `<head>`:

```html
<link rel="stylesheet" href="/static/css/tutorial.css">
<script src="/static/js/tutorial.js"></script>
```

### 2. API Endpoints

Todos requieren autenticación (`Authorization: Bearer <token>`):

#### `GET /api/tutorial/status`
Estado actual del usuario en el tutorial.

**Response:**
```json
{
    "has_completed": false,
    "current_step": 3,
    "total_steps": 15,
    "percentage_complete": 20.0
}
```

#### `GET /api/tutorial/steps`
Obtener todos los pasos del tutorial.

**Response:**
```json
[
    {
        "step": 1,
        "title": "🎉 ¡Bienvenido al ERP Dario!",
        "description": "...",
        "selector": "body",
        "position": "center",
        "highlight": false,
        "action_text": "Comenzar"
    },
    ...
]
```

#### `GET /api/tutorial/steps/{step_number}`
Obtener un paso específico (1-15).

#### `POST /api/tutorial/start`
Iniciar el tutorial desde el primer paso.

#### `POST /api/tutorial/step/{step_number}`
Actualizar el paso actual (para tracking).

#### `POST /api/tutorial/complete`
Marcar el tutorial como completado.

**Body:**
```json
{
    "completed": true,
    "final_step": 15
}
```

#### `POST /api/tutorial/skip`
Saltarse el tutorial (marca como completado sin verlo).

#### `DELETE /api/tutorial/reset`
Reiniciar el tutorial para que vuelva a mostrar.

## 🎨 Personalización

### Modificar pasos

Editar `src/dario_app/modules/tutorial/steps.py`:

```python
{
    "step": 2,
    "title": "📊 Dashboard",
    "description": "Tu centro de control...",
    "selector": "nav a[href*='dashboard']",  # CSS selector
    "position": "right",                      # top, bottom, left, right, center
    "highlight": True,                        # Resaltar elemento?
    "action_text": "Siguiente",
    "image_url": None                         # Imagen opcional
}
```

### Cambiar colores

Editar variables en `static/css/tutorial.css`:

```css
:root {
    --tutorial-primary: #667eea;        /* Color principal */
    --tutorial-secondary: #764ba2;      /* Color secundario */
    --tutorial-success: #48bb78;        /* Color éxito */
    --tutorial-overlay: rgba(0, 0, 0, 0.75);  /* Oscuridad */
}
```

### Cambiar timing

En `static/js/tutorial.js`, modificar:

```javascript
this.autoplayDelay = 500;  // Delay para auto-avance
```

## 📊 Base de Datos

Tabla `user_tutorial_progress`:

```python
id                    INT PRIMARY KEY
user_id              INT (FK a usuarios)
org_id               INT (FK a organización)
has_completed_tutorial  BOOL (default: False)
current_step         INT (default: 0)
last_step_viewed     INT (default: 0)
started_at          DATETIME
completed_at        DATETIME (nullable)
last_accessed_at    DATETIME
```

## 🚀 Cómo Funciona

### Flujo de Inicio

1. **JavaScript se carga** (`tutorial.js`)
2. **Fetch a `/api/tutorial/status`** para obtener estado
3. **Si no completó**: Muestra modal inicial
4. **Usuario elige**: "Iniciar Tour" o "Saltar"
5. **Si inicia**: Carga pasos y comienza en paso 1

### Flujo de Cada Paso

1. **Obtener paso** del array `TUTORIAL_STEPS`
2. **Encontrar elemento** usando CSS selector
3. **Crear overlay** oscuro alrededor del elemento
4. **Animar el highlight** con pulsación
5. **Posicionar popup** según `position` especificada
6. **Mostrar controles**: Anterior, Siguiente/Finalizar
7. **Actualizar BD** con `POST /api/tutorial/step/{n}`

### Atajos de Teclado

```javascript
Escape  → closeTutorial()
→       → nextStep()
←       → previousStep()
?       → restartTutorial()
Espacio → nextStep()
```

## 📱 Responsive

- **Desktop**: Popups posicionados dinámicamente
- **Tablet**: Ancho reducido a 90vw
- **Mobile**: Layout adaptado, botones más grandes

## 🐛 Debugging

Abrir consola (`F12`) para ver logs:

```javascript
// Ver objeto tutorial
window.tutorial

// Ver pasos cargados
window.tutorial.steps

// Ver paso actual
window.tutorial.currentStep

// Saltar a paso específico
window.tutorial.showStep(5)

// Ver estado
window.tutorial.getTutorialStatus()
```

## 📝 Ejemplos de Uso

### Auto-iniciar tutorial para usuarios nuevos

En el endpoint de login, verificar si es primera vez:

```python
@router.post("/login")
async def login(credentials: LoginSchema):
    user = authenticate_user(credentials)
    # ...
    return {
        "access_token": token,
        "show_tutorial": user.is_new  # Flag para frontend
    }
```

Luego en frontend, si `show_tutorial`:

```javascript
if (response.show_tutorial) {
    window.tutorial.startTutorial();
}
```

### Mostrar tutorial sobre un módulo específico

```javascript
// Mostrar solo el paso de Ventas (paso 3)
window.tutorial.showStep(3);
```

### Personalizar para roles

En `routes.py`, agregar lógica por rol:

```python
@router.get("/status")
async def get_tutorial_status(current_user=Depends(get_current_user)):
    if current_user.role == "admin":
        # Mostrar todos los pasos
    elif current_user.role == "vendedor":
        # Mostrar solo pasos relevantes para vendedores
```

## ⚙️ Configuración en Producción

### 1. Minimizar JS/CSS (opcional)

```bash
# Instalar UglifyJS
npm install uglify-js

# Minimizar
npx uglifyjs static/js/tutorial.js -c -m -o static/js/tutorial.min.js
```

### 2. Habilitar GZIP en servidor

```nginx
gzip on;
gzip_types text/javascript text/css;
```

### 3. Caché del tutorial

En `routes.py`:

```python
from fastapi.responses import Response

@router.get("/steps", response_model=list[dict])
async def get_tutorial_steps():
    # Cachear por 24 horas
    headers = {"Cache-Control": "public, max-age=86400"}
    return Response(content=..., headers=headers)
```

## 🎯 Próximos Pasos

- [ ] Agregar videos para cada paso
- [ ] Tutorial contextual (mostrar solo pasos relevantes)
- [ ] Multi-idioma (i18n)
- [ ] Analytics (qué pasos ven más, cuáles no entienden)
- [ ] Tutorial por rol/perfil
- [ ] Notificaciones integradas con tutorial
- [ ] Gamificación (badges por completar)

## 📞 Soporte

Para reportar bugs o sugerencias, contactar a soporte@dario.io
