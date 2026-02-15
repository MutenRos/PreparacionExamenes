<?php
/**
 * ============================================================================
 * ESPECTÁCULOS DANI - API de Contacto
 * ============================================================================
 * 
 * Endpoint para procesar formularios de contacto.
 * Maneja validación, sanitización y envío de emails.
 * 
 * @author      Espectáculos Dani Dev Team
 * @version     1.0.0
 * @license     Proprietary
 * @since       2024
 * 
 * ENDPOINT: POST /api/contact.php
 * 
 * PARÁMETROS:
 * - nombre (string, required): Nombre del cliente
 * - email (string, required): Email del cliente
 * - telefono (string, optional): Teléfono del cliente
 * - servicio (string, required): Servicio solicitado
 * - fecha (string, optional): Fecha del evento
 * - mensaje (string, required): Mensaje del cliente
 * - llamar (bool, optional): Si desea ser contactado por teléfono
 * 
 * RESPUESTA:
 * {
 *   "success": true|false,
 *   "message": "Mensaje de respuesta",
 *   "data": {} // Datos adicionales (opcional)
 * }
 * 
 * ============================================================================
 */

declare(strict_types=1);

// Configuración de errores (desactivar en producción)
error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');

// Headers CORS y Content-Type
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
// Cabecera adicional de seguridad contra ataques XSS reflejados
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// Manejar preflight CORS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

/**
 * Configuración del sistema
 */
define('CONFIG', [
    // Email de destino para las notificaciones
    'email_to' => 'info@espectaculosdani.com',
    
    // Email de origen (debe ser del dominio)
    'email_from' => 'noreply@espectaculosdani.com',
    
    // Nombre del remitente
    'email_from_name' => 'Espectáculos Dani Web',
    
    // Directorio para guardar logs
    'log_dir' => __DIR__ . '/../logs',
    
    // Directorio para guardar solicitudes (backup)
    'data_dir' => __DIR__ . '/../data',
    
    // Rate limiting: máximo de solicitudes por IP
    'rate_limit' => 5,
    
    // Ventana de tiempo para rate limiting (segundos)
    'rate_window' => 3600,
    
    // Servicios válidos
    'valid_services' => [
        'hinchables',
        'hinchables-agua',
        'atracciones',
        'disco',
        'sonido',
        'espuma',
        'escenarios',
        'mobiliario',
        'otro'
    ]
]);

// ============================================================================
// FUNCIONES AUXILIARES
// ============================================================================

/**
 * Envía una respuesta JSON y termina la ejecución
 * 
 * @param bool $success Estado de la operación
 * @param string $message Mensaje descriptivo
 * @param array $data Datos adicionales (opcional)
 * @param int $httpCode Código HTTP (por defecto 200)
 */
function sendResponse(bool $success, string $message, array $data = [], int $httpCode = 200): void
{
    http_response_code($httpCode);
    
    echo json_encode([
        'success' => $success,
        'message' => $message,
        'data' => $data,
        'timestamp' => date('c')
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    
    exit;
}

/**
 * Registra un mensaje en el log
 * 
 * @param string $level Nivel de log (info, warning, error)
 * @param string $message Mensaje a registrar
 * @param array $context Contexto adicional
 */
function logMessage(string $level, string $message, array $context = []): void
{
    $logDir = CONFIG['log_dir'];
    
    // Crear directorio si no existe
    if (!is_dir($logDir)) {
        @mkdir($logDir, 0755, true);
    }
    
    $logFile = $logDir . '/contact_' . date('Y-m') . '.log';
    $timestamp = date('Y-m-d H:i:s');
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $contextJson = !empty($context) ? ' ' . json_encode($context) : '';
    
    $logEntry = "[{$timestamp}] [{$level}] [{$ip}] {$message}{$contextJson}\n";
    
    @file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

/**
 * Sanitiza una cadena de texto
 * 
 * @param mixed $input Entrada a sanitizar
 * @return string Cadena sanitizada
 */
function sanitizeString($input): string
{
    if (!is_string($input)) {
        return '';
    }
    
    // Eliminar etiquetas HTML
    $clean = strip_tags($input);
    
    // Eliminar caracteres de control
    $clean = preg_replace('/[\x00-\x1F\x7F]/u', '', $clean);
    
    // Normalizar espacios
    $clean = preg_replace('/\s+/', ' ', $clean);
    
    // Trim
    $clean = trim($clean);
    
    return $clean;
}

/**
 * Valida un email
 * 
 * @param string $email Email a validar
 * @return bool
 */
function isValidEmail(string $email): bool
{
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Valida un teléfono español
 * 
 * @param string $phone Teléfono a validar
 * @return bool
 */
function isValidPhone(string $phone): bool
{
    // Permitir vacío (es opcional)
    if (empty($phone)) {
        return true;
    }
    
    // Eliminar espacios y guiones
    $clean = preg_replace('/[\s\-]/', '', $phone);
    
    // Validar formato español (9 dígitos, empieza por 6, 7, 8 o 9)
    return preg_match('/^[6-9]\d{8}$/', $clean) === 1;
}

/**
 * Valida una fecha
 * 
 * @param string $date Fecha en formato Y-m-d
 * @return bool
 */
function isValidDate(string $date): bool
{
    // Permitir vacío (es opcional)
    if (empty($date)) {
        return true;
    }
    
    $d = DateTime::createFromFormat('Y-m-d', $date);
    
    if (!$d || $d->format('Y-m-d') !== $date) {
        return false;
    }
    
    // La fecha debe ser hoy o en el futuro
    $today = new DateTime('today');
    return $d >= $today;
}

/**
 * Comprueba el rate limiting
 * 
 * @param string $ip Dirección IP
 * @return bool True si está permitido, false si excede el límite
 */
function checkRateLimit(string $ip): bool
{
    $dataDir = CONFIG['data_dir'];
    $rateFile = $dataDir . '/rate_limits.json';
    
    // Crear directorio si no existe
    if (!is_dir($dataDir)) {
        @mkdir($dataDir, 0755, true);
    }
    
    // Cargar datos actuales
    $limits = [];
    if (file_exists($rateFile)) {
        $limits = json_decode(file_get_contents($rateFile), true) ?? [];
    }
    
    $now = time();
    $window = CONFIG['rate_window'];
    $maxRequests = CONFIG['rate_limit'];
    
    // Limpiar entradas antiguas
    foreach ($limits as $key => $data) {
        if ($data['timestamp'] < ($now - $window)) {
            unset($limits[$key]);
        }
    }
    
    // Verificar límite para esta IP
    $ipHash = md5($ip);
    
    if (isset($limits[$ipHash])) {
        if ($limits[$ipHash]['count'] >= $maxRequests) {
            return false;
        }
        $limits[$ipHash]['count']++;
    } else {
        $limits[$ipHash] = [
            'count' => 1,
            'timestamp' => $now
        ];
    }
    
    // Guardar
    @file_put_contents($rateFile, json_encode($limits), LOCK_EX);
    
    return true;
}

/**
 * Guarda la solicitud en un archivo JSON
 * 
 * @param array $data Datos del formulario
 * @return bool
 */
function saveRequest(array $data): bool
{
    $dataDir = CONFIG['data_dir'];
    $requestsFile = $dataDir . '/requests.json';
    
    // Crear directorio si no existe
    if (!is_dir($dataDir)) {
        if (!@mkdir($dataDir, 0755, true)) {
            return false;
        }
    }
    
    // Cargar solicitudes existentes
    $requests = [];
    if (file_exists($requestsFile)) {
        $requests = json_decode(file_get_contents($requestsFile), true) ?? [];
    }
    
    // Añadir nueva solicitud
    $requests[] = array_merge($data, [
        'id' => uniqid('req_', true),
        'created_at' => date('c'),
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown',
        'status' => 'pending'
    ]);
    
    // Guardar
    return @file_put_contents(
        $requestsFile, 
        json_encode($requests, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT),
        LOCK_EX
    ) !== false;
}

/**
 * Envía el email de notificación
 * 
 * @param array $data Datos del formulario
 * @return bool
 */
function sendNotificationEmail(array $data): bool
{
    $to = CONFIG['email_to'];
    $fromEmail = CONFIG['email_from'];
    $fromName = CONFIG['email_from_name'];
    
    // Asunto
    $subject = "Nueva solicitud de contacto - {$data['servicio']}";
    
    // Cuerpo del email (HTML)
    $body = buildEmailBody($data);
    
    // Headers
    $headers = [
        'MIME-Version: 1.0',
        'Content-type: text/html; charset=UTF-8',
        "From: {$fromName} <{$fromEmail}>",
        "Reply-To: {$data['email']}",
        'X-Mailer: PHP/' . phpversion(),
        'X-Priority: 1'
    ];
    
    // Enviar
    return @mail($to, $subject, $body, implode("\r\n", $headers));
}

/**
 * Construye el cuerpo del email HTML
 * 
 * @param array $data Datos del formulario
 * @return string HTML del email
 */
function buildEmailBody(array $data): string
{
    $nombre = htmlspecialchars($data['nombre']);
    $email = htmlspecialchars($data['email']);
    $telefono = htmlspecialchars($data['telefono'] ?? 'No proporcionado');
    $servicio = htmlspecialchars($data['servicio']);
    $fecha = !empty($data['fecha']) ? date('d/m/Y', strtotime($data['fecha'])) : 'No especificada';
    $mensaje = nl2br(htmlspecialchars($data['mensaje']));
    $llamar = !empty($data['llamar']) ? 'Sí' : 'No';
    $fechaActual = date('d/m/Y H:i');
    
    return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #ff6b35; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .field { margin-bottom: 15px; }
        .label { font-weight: bold; color: #555; }
        .value { margin-top: 5px; padding: 10px; background: white; border-radius: 4px; }
        .footer { text-align: center; padding: 20px; color: #888; font-size: 12px; }
        .highlight { background: #fff3e0; border-left: 4px solid #ff6b35; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📬 Nueva Solicitud de Contacto</h1>
            <p>Recibida el {$fechaActual}</p>
        </div>
        
        <div class="content">
            <div class="field">
                <div class="label">👤 Nombre:</div>
                <div class="value">{$nombre}</div>
            </div>
            
            <div class="field">
                <div class="label">📧 Email:</div>
                <div class="value"><a href="mailto:{$email}">{$email}</a></div>
            </div>
            
            <div class="field">
                <div class="label">📞 Teléfono:</div>
                <div class="value">{$telefono}</div>
            </div>
            
            <div class="field">
                <div class="label">🎯 Servicio solicitado:</div>
                <div class="value highlight">{$servicio}</div>
            </div>
            
            <div class="field">
                <div class="label">📅 Fecha del evento:</div>
                <div class="value">{$fecha}</div>
            </div>
            
            <div class="field">
                <div class="label">💬 Mensaje:</div>
                <div class="value">{$mensaje}</div>
            </div>
            
            <div class="field">
                <div class="label">📱 ¿Desea ser contactado por teléfono?</div>
                <div class="value">{$llamar}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Este mensaje fue enviado desde el formulario de contacto de espectaculosdani.es</p>
        </div>
    </div>
</body>
</html>
HTML;
}

// ============================================================================
// PROCESAMIENTO PRINCIPAL
// ============================================================================

// Solo aceptar POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendResponse(false, 'Método no permitido. Use POST.', [], 405);
}

// Verificar Content-Type
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
if (strpos($contentType, 'application/json') === false) {
    // Intentar leer como form-data
    $input = $_POST;
} else {
    // Leer JSON
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        logMessage('warning', 'Invalid JSON received');
        sendResponse(false, 'JSON inválido.', [], 400);
    }
}

// Verificar que hay datos
if (empty($input)) {
    sendResponse(false, 'No se recibieron datos.', [], 400);
}

// Rate limiting
$clientIp = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
if (!checkRateLimit($clientIp)) {
    logMessage('warning', 'Rate limit exceeded');
    sendResponse(false, 'Has excedido el límite de solicitudes. Intenta de nuevo más tarde.', [], 429);
}

// Honeypot check (anti-spam)
if (!empty($input['website'])) {
    logMessage('warning', 'Honeypot triggered - spam detected');
    // Responder como si fuera exitoso para no alertar al bot
    sendResponse(true, 'Mensaje enviado correctamente.');
}

// ============================================================================
// VALIDACIÓN
// ============================================================================

$errors = [];

// Nombre (requerido)
$nombre = sanitizeString($input['nombre'] ?? '');
if (empty($nombre)) {
    $errors['nombre'] = 'El nombre es obligatorio';
} elseif (strlen($nombre) < 2) {
    $errors['nombre'] = 'El nombre debe tener al menos 2 caracteres';
} elseif (strlen($nombre) > 100) {
    $errors['nombre'] = 'El nombre es demasiado largo';
}

// Email (requerido)
$email = sanitizeString($input['email'] ?? '');
if (empty($email)) {
    $errors['email'] = 'El email es obligatorio';
} elseif (!isValidEmail($email)) {
    $errors['email'] = 'El email no es válido';
}

// Teléfono (opcional pero validado si se proporciona)
$telefono = sanitizeString($input['telefono'] ?? '');
if (!isValidPhone($telefono)) {
    $errors['telefono'] = 'El teléfono no es válido (debe tener 9 dígitos)';
}

// Servicio (requerido)
$servicio = sanitizeString($input['servicio'] ?? '');
if (empty($servicio)) {
    $errors['servicio'] = 'Debes seleccionar un servicio';
} elseif (!in_array($servicio, CONFIG['valid_services'])) {
    $errors['servicio'] = 'Servicio no válido';
}

// Fecha (opcional pero validada si se proporciona)
$fecha = sanitizeString($input['fecha'] ?? '');
if (!isValidDate($fecha)) {
    $errors['fecha'] = 'La fecha no es válida o es anterior a hoy';
}

// Mensaje (requerido)
$mensaje = sanitizeString($input['mensaje'] ?? '');
if (empty($mensaje)) {
    $errors['mensaje'] = 'El mensaje es obligatorio';
} elseif (strlen($mensaje) < 10) {
    $errors['mensaje'] = 'El mensaje debe tener al menos 10 caracteres';
} elseif (strlen($mensaje) > 1000) {
    $errors['mensaje'] = 'El mensaje es demasiado largo (máximo 1000 caracteres)';
}

// Llamar (opcional, booleano)
$llamar = !empty($input['llamar']);

// Si hay errores, devolver
if (!empty($errors)) {
    logMessage('info', 'Validation failed', $errors);
    sendResponse(false, 'Por favor, corrige los errores del formulario.', ['errors' => $errors], 422);
}

// ============================================================================
// PROCESAMIENTO
// ============================================================================

// Datos validados
$validatedData = [
    'nombre' => $nombre,
    'email' => $email,
    'telefono' => $telefono,
    'servicio' => $servicio,
    'fecha' => $fecha,
    'mensaje' => $mensaje,
    'llamar' => $llamar
];

// Guardar solicitud (siempre, como backup)
$saved = saveRequest($validatedData);
if (!$saved) {
    logMessage('error', 'Failed to save request');
}

// Enviar email
$emailSent = sendNotificationEmail($validatedData);

if ($emailSent) {
    logMessage('info', 'Contact form submitted successfully', ['email' => $email]);
    sendResponse(true, 'Tu mensaje ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.');
} else {
    logMessage('warning', 'Email could not be sent, but request was saved', ['email' => $email]);
    
    // El email falló pero la solicitud se guardó
    if ($saved) {
        sendResponse(true, 'Tu mensaje ha sido registrado. Te contactaremos pronto.');
    } else {
        sendResponse(false, 'Hubo un problema al procesar tu solicitud. Por favor, inténtalo de nuevo.', [], 500);
    }
}
