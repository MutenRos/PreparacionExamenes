<?php
/**
 * ==========================================================================
 * MUTENROS Portfolio - Contact Form API
 * ==========================================================================
 * 
 * RESTful API endpoint for handling contact form submissions.
 * Validates input, sanitizes data, and sends email notifications.
 * 
 * @author  Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * 
 * Endpoint: POST /api/contact.php
 * 
 * Request Body (JSON):
 * {
 *     "name": "string (required, 2-100 chars)",
 *     "email": "string (required, valid email)",
 *     "subject": "string (optional, max 200 chars)",
 *     "message": "string (required, 10-5000 chars)"
 * }
 * 
 * Response (JSON):
 * {
 *     "success": boolean,
 *     "message": "string",
 *     "errors": ["array of validation errors"] (only if success=false)
 * }
 * 
 * HTTP Status Codes:
 * - 200: Success
 * - 400: Validation error
 * - 405: Method not allowed
 * - 429: Rate limit exceeded
 * - 500: Server error
 * ==========================================================================
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

/**
 * Contact form configuration
 * Modify these values according to your needs
 */
$config = [
    // Email settings
    'recipient_email' => 'tu@email.com',
    'recipient_name'  => 'MutenRos',
    'from_email'      => 'noreply@mutenros.github.io',
    'from_name'       => 'Portfolio Contact Form',
    
    // Rate limiting (requests per IP per hour)
    'rate_limit'      => 5,
    'rate_limit_file' => __DIR__ . '/../logs/rate_limits.json',
    
    // Security
    'allowed_origins' => [
        'https://mutenros.github.io',
        'http://localhost',
        'http://127.0.0.1'
    ],
    
    // Validation rules
    'validation' => [
        'name_min'     => 2,
        'name_max'     => 100,
        'subject_max'  => 200,
        'message_min'  => 10,
        'message_max'  => 5000
    ]
];

// ============================================================================
// HEADERS & CORS
// ============================================================================

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');

// CORS handling
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $config['allowed_origins'])) {
    header("Access-Control-Allow-Origin: $origin");
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    header('Access-Control-Max-Age: 86400');
}

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Send JSON response and exit
 * 
 * @param bool   $success   Whether the request was successful
 * @param string $message   Response message
 * @param array  $errors    Array of validation errors
 * @param int    $httpCode  HTTP status code
 */
function sendResponse(bool $success, string $message, array $errors = [], int $httpCode = 200): void
{
    http_response_code($httpCode);
    
    $response = [
        'success' => $success,
        'message' => $message
    ];
    
    if (!empty($errors)) {
        $response['errors'] = $errors;
    }
    
    echo json_encode($response, JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Sanitize string input
 * 
 * @param string $input Raw input string
 * @return string Sanitized string
 */
function sanitizeString(string $input): string
{
    $input = trim($input);
    $input = stripslashes($input);
    $input = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
    return $input;
}

/**
 * Validate email address
 * 
 * @param string $email Email to validate
 * @return bool True if valid
 */
function isValidEmail(string $email): bool
{
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Get client IP address
 * 
 * @return string Client IP
 */
function getClientIP(): string
{
    $headers = [
        'HTTP_CF_CONNECTING_IP', // Cloudflare
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_REAL_IP',
        'REMOTE_ADDR'
    ];
    
    foreach ($headers as $header) {
        if (!empty($_SERVER[$header])) {
            $ip = $_SERVER[$header];
            // Handle comma-separated IPs (X-Forwarded-For)
            if (strpos($ip, ',') !== false) {
                $ip = trim(explode(',', $ip)[0]);
            }
            if (filter_var($ip, FILTER_VALIDATE_IP)) {
                return $ip;
            }
        }
    }
    
    return '0.0.0.0';
}

/**
 * Check rate limiting for client IP
 * 
 * @param string $ip     Client IP address
 * @param array  $config Configuration array
 * @return bool True if rate limit exceeded
 */
function isRateLimited(string $ip, array $config): bool
{
    $file = $config['rate_limit_file'];
    $limit = $config['rate_limit'];
    $window = 3600; // 1 hour in seconds
    
    // Ensure log directory exists
    $logDir = dirname($file);
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }
    
    // Load existing rate limit data
    $data = [];
    if (file_exists($file)) {
        $content = file_get_contents($file);
        $data = json_decode($content, true) ?: [];
    }
    
    $now = time();
    $ipHash = md5($ip); // Hash IP for privacy
    
    // Clean old entries
    foreach ($data as $hash => $entry) {
        if ($now - $entry['first_request'] > $window) {
            unset($data[$hash]);
        }
    }
    
    // Check current IP
    if (isset($data[$ipHash])) {
        if ($now - $data[$ipHash]['first_request'] > $window) {
            // Reset after window
            $data[$ipHash] = [
                'first_request' => $now,
                'count' => 1
            ];
        } else {
            $data[$ipHash]['count']++;
            if ($data[$ipHash]['count'] > $limit) {
                file_put_contents($file, json_encode($data));
                return true;
            }
        }
    } else {
        $data[$ipHash] = [
            'first_request' => $now,
            'count' => 1
        ];
    }
    
    file_put_contents($file, json_encode($data));
    return false;
}

/**
 * Send email using PHP mail() or configured mailer
 * 
 * @param array $data    Sanitized form data
 * @param array $config  Configuration array
 * @return bool True if email sent successfully
 */
function sendEmail(array $data, array $config): bool
{
    $to = $config['recipient_email'];
    $subject = "[Portfolio Contact] " . ($data['subject'] ?: 'Nuevo mensaje');
    
    // Build email body
    $body = "===========================================\n";
    $body .= "NUEVO MENSAJE DE CONTACTO - PORTFOLIO\n";
    $body .= "===========================================\n\n";
    $body .= "Nombre: {$data['name']}\n";
    $body .= "Email: {$data['email']}\n";
    $body .= "Asunto: " . ($data['subject'] ?: 'Sin asunto') . "\n\n";
    $body .= "-------------------------------------------\n";
    $body .= "MENSAJE:\n";
    $body .= "-------------------------------------------\n\n";
    $body .= $data['message'] . "\n\n";
    $body .= "-------------------------------------------\n";
    $body .= "Enviado desde: " . $data['ip'] . "\n";
    $body .= "Fecha: " . date('Y-m-d H:i:s') . "\n";
    $body .= "===========================================\n";
    
    // Email headers
    $headers = [
        'From' => "{$config['from_name']} <{$config['from_email']}>",
        'Reply-To' => "{$data['name']} <{$data['email']}>",
        'X-Mailer' => 'PHP/' . phpversion(),
        'Content-Type' => 'text/plain; charset=UTF-8'
    ];
    
    $headerString = '';
    foreach ($headers as $key => $value) {
        $headerString .= "$key: $value\r\n";
    }
    
    // Send email
    return mail($to, $subject, $body, $headerString);
}

/**
 * Log contact form submission
 * 
 * @param array $data   Form data
 * @param bool  $success Whether submission was successful
 */
function logSubmission(array $data, bool $success): void
{
    $logFile = __DIR__ . '/../logs/contact_submissions.log';
    $logDir = dirname($logFile);
    
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }
    
    $logEntry = sprintf(
        "[%s] %s | IP: %s | Name: %s | Email: %s | Status: %s\n",
        date('Y-m-d H:i:s'),
        $success ? 'SUCCESS' : 'FAILED',
        $data['ip'] ?? 'unknown',
        $data['name'] ?? 'unknown',
        $data['email'] ?? 'unknown',
        $success ? 'Email sent' : 'Email failed'
    );
    
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// ============================================================================
// MAIN REQUEST HANDLING
// ============================================================================

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendResponse(false, 'Metodo no permitido. Use POST.', [], 405);
}

// Check rate limiting
$clientIP = getClientIP();
if (isRateLimited($clientIP, $config)) {
    sendResponse(false, 'Demasiadas solicitudes. Intente de nuevo mas tarde.', [], 429);
}

// Get and parse JSON input
$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true);

if ($input === null && json_last_error() !== JSON_ERROR_NONE) {
    sendResponse(false, 'JSON invalido en la solicitud.', [], 400);
}

// ============================================================================
// VALIDATION
// ============================================================================

$errors = [];
$rules = $config['validation'];

// Validate name
$name = isset($input['name']) ? sanitizeString($input['name']) : '';
if (empty($name)) {
    $errors[] = 'El nombre es obligatorio.';
} elseif (strlen($name) < $rules['name_min']) {
    $errors[] = "El nombre debe tener al menos {$rules['name_min']} caracteres.";
} elseif (strlen($name) > $rules['name_max']) {
    $errors[] = "El nombre no puede exceder {$rules['name_max']} caracteres.";
}

// Validate email
$email = isset($input['email']) ? sanitizeString($input['email']) : '';
if (empty($email)) {
    $errors[] = 'El email es obligatorio.';
} elseif (!isValidEmail($email)) {
    $errors[] = 'El email no es valido.';
}

// Validate subject (optional)
$subject = isset($input['subject']) ? sanitizeString($input['subject']) : '';
if (!empty($subject) && strlen($subject) > $rules['subject_max']) {
    $errors[] = "El asunto no puede exceder {$rules['subject_max']} caracteres.";
}

// Validate message
$message = isset($input['message']) ? sanitizeString($input['message']) : '';
if (empty($message)) {
    $errors[] = 'El mensaje es obligatorio.';
} elseif (strlen($message) < $rules['message_min']) {
    $errors[] = "El mensaje debe tener al menos {$rules['message_min']} caracteres.";
} elseif (strlen($message) > $rules['message_max']) {
    $errors[] = "El mensaje no puede exceder {$rules['message_max']} caracteres.";
}

// Return validation errors if any
if (!empty($errors)) {
    sendResponse(false, 'Error de validacion.', $errors, 400);
}

// ============================================================================
// PROCESS SUBMISSION
// ============================================================================

$formData = [
    'name'    => $name,
    'email'   => $email,
    'subject' => $subject,
    'message' => html_entity_decode($message, ENT_QUOTES, 'UTF-8'),
    'ip'      => $clientIP
];

try {
    $emailSent = sendEmail($formData, $config);
    logSubmission($formData, $emailSent);
    
    if ($emailSent) {
        sendResponse(true, 'Mensaje enviado correctamente. Te respondere pronto!');
    } else {
        sendResponse(false, 'Error al enviar el mensaje. Intenta mas tarde.', [], 500);
    }
} catch (Exception $e) {
    error_log('Contact form error: ' . $e->getMessage());
    logSubmission($formData, false);
    sendResponse(false, 'Error interno del servidor.', [], 500);
}
