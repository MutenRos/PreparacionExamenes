# 📡 API Documentation

## Contact API

### Endpoint

```
POST /api/contact.php
```

### Description

Handles contact form submissions with validation, rate limiting, and email delivery.

---

## Request

### Headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | ✅ Yes |
| `Origin` | Allowed origin | ✅ Yes |

### Body Parameters

| Parameter | Type | Required | Min | Max | Description |
|-----------|------|----------|-----|-----|-------------|
| `name` | string | ✅ Yes | 2 | 100 | Sender's name |
| `email` | string | ✅ Yes | - | 254 | Valid email address |
| `subject` | string | ❌ No | 2 | 200 | Email subject |
| `message` | string | ✅ Yes | 10 | 5000 | Message content |

### Example Request

```bash
curl -X POST https://your-domain.com/api/contact.php \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-domain.com" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Project Inquiry",
    "message": "Hello, I am interested in collaborating..."
  }'
```

---

## Response

### Success Response

**Code:** `200 OK`

```json
{
    "success": true,
    "message": "Mensaje enviado correctamente",
    "data": {
        "timestamp": "2024-01-15T10:30:00+00:00"
    }
}
```

### Error Responses

#### 400 Bad Request - Invalid JSON

```json
{
    "success": false,
    "error": "JSON inválido en el cuerpo de la petición",
    "code": "INVALID_JSON"
}
```

#### 400 Bad Request - Validation Error

```json
{
    "success": false,
    "error": "El nombre es obligatorio",
    "code": "VALIDATION_ERROR"
}
```

#### 403 Forbidden - Invalid Origin

```json
{
    "success": false,
    "error": "Origen no permitido",
    "code": "FORBIDDEN"
}
```

#### 405 Method Not Allowed

```json
{
    "success": false,
    "error": "Método no permitido. Use POST",
    "code": "METHOD_NOT_ALLOWED"
}
```

#### 429 Too Many Requests

```json
{
    "success": false,
    "error": "Demasiadas solicitudes. Por favor espere antes de enviar otro mensaje",
    "code": "RATE_LIMIT_EXCEEDED"
}
```

#### 500 Internal Server Error

```json
{
    "success": false,
    "error": "Error interno del servidor",
    "code": "SERVER_ERROR"
}
```

---

## Validation Rules

### Name
- Required
- Minimum: 2 characters
- Maximum: 100 characters
- Stripped of HTML tags
- Trimmed whitespace

### Email
- Required
- Valid email format (RFC 5322)
- Maximum: 254 characters

### Subject
- Optional (defaults to "Mensaje desde Portfolio")
- Minimum: 2 characters (if provided)
- Maximum: 200 characters
- Stripped of HTML tags

### Message
- Required
- Minimum: 10 characters
- Maximum: 5000 characters
- Stripped of HTML tags

---

## Rate Limiting

| Setting | Value |
|---------|-------|
| Window | 1 hour |
| Max requests | 5 per IP |
| Storage | JSON file |

Rate limits are tracked per IP address. When exceeded, requests return `429 Too Many Requests`.

---

## Security Features

### Input Sanitization
- All text inputs are sanitized with `htmlspecialchars()`
- HTML tags are stripped from inputs
- Email is validated against RFC 5322 format

### CORS
- Allowed origins are whitelisted
- Preflight requests (OPTIONS) are handled
- Credentials are not allowed

### Headers
```
Access-Control-Allow-Origin: [whitelisted origin]
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

---

## Configuration

Located in `api/contact.php`:

```php
$CONFIG = [
    'email' => [
        'to' => 'your-email@example.com',
        'from' => 'noreply@your-domain.com',
        'subject_prefix' => '[Portfolio Contact]'
    ],
    'rate_limit' => [
        'max_requests' => 5,
        'window_seconds' => 3600
    ],
    'validation' => [
        'name_min' => 2,
        'name_max' => 100,
        'message_min' => 10,
        'message_max' => 5000,
        'subject_max' => 200
    ],
    'allowed_origins' => [
        'https://mutenros.github.io',
        'http://localhost'
    ]
];
```

---

## Logging

Submissions are logged to `logs/contact.log`:

```
[2024-01-15 10:30:00] Contact from: john@example.com | IP: 192.168.1.1 | Subject: Project Inquiry
```

Log directory is created automatically if it doesn't exist.

---

## Email Format

The sent email follows this format:

```
From: Portfolio Contact <noreply@your-domain.com>
To: your-email@example.com
Reply-To: john@example.com
Subject: [Portfolio Contact] Project Inquiry

=================================================
NUEVO MENSAJE DE CONTACTO
=================================================

Nombre: John Doe
Email: john@example.com
Fecha: 15/01/2024 10:30:00

-------------------------------------------------
MENSAJE:
-------------------------------------------------

Hello, I am interested in collaborating...

=================================================
IP del remitente: 192.168.1.1
Enviado desde: https://mutenros.github.io
=================================================
```

---

## Integration Example

### JavaScript (Fetch API)

```javascript
async function submitContactForm(formData) {
    try {
        const response = await fetch('/api/contact.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: formData.get('name'),
                email: formData.get('email'),
                subject: formData.get('subject'),
                message: formData.get('message')
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Error sending message');
        }

        return result;
    } catch (error) {
        console.error('Contact form error:', error);
        throw error;
    }
}
```

### Form HTML

```html
<form id="contact-form" class="contact-form">
    <div class="form-group">
        <label for="name">Nombre</label>
        <input type="text" id="name" name="name" required 
               minlength="2" maxlength="100">
    </div>
    
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required 
               maxlength="254">
    </div>
    
    <div class="form-group">
        <label for="subject">Asunto (opcional)</label>
        <input type="text" id="subject" name="subject" 
               maxlength="200">
    </div>
    
    <div class="form-group">
        <label for="message">Mensaje</label>
        <textarea id="message" name="message" required 
                  minlength="10" maxlength="5000" rows="5"></textarea>
    </div>
    
    <button type="submit" class="btn btn--primary">
        Enviar Mensaje
    </button>
</form>
```
