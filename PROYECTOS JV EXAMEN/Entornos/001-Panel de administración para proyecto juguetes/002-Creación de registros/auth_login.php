<?php
session_start();

function redirect_with(string $msg, string $to = 'login.php'): void {
  $_SESSION['flash'] = $msg;
  header("Location: $to");
  exit;
}
function e(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') redirect_with('Acceso no permitido.');

if (empty($_POST['csrf']) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], (string)$_POST['csrf'])) {
  redirect_with('Sesión caducada. Vuelve a intentarlo.');
}

$email = trim((string)($_POST['email'] ?? ''));
$pass  = (string)($_POST['password'] ?? '');

if ($email === '' || $pass === '') redirect_with('Completa email y contraseña.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) redirect_with('Email no válido.');

try {
  $db = new SQLite3(__DIR__ . '/recortables.db');
  $db->busyTimeout(2000);

  // Ensure table exists (safe if you already created it)
  $db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
  )");
  $db->exec("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)");

  $stmt = $db->prepare("SELECT id, username, email, password_hash FROM users WHERE email = :email LIMIT 1");
  $stmt->bindValue(':email', $email, SQLITE3_TEXT);
  $res = $stmt->execute();
  $row = $res ? $res->fetchArray(SQLITE3_ASSOC) : false;

  if (!$row || !password_verify($pass, $row['password_hash'])) {
    redirect_with('Credenciales incorrectas.');
  }

  // Session login
  session_regenerate_id(true);
  $_SESSION['user'] = [
    'id' => (int)$row['id'],
    'username' => $row['username'],
    'email' => $row['email'],
  ];

  header("Location: index.php");
  exit;

} catch (Throwable $e) {
  redirect_with('Error interno. Inténtalo de nuevo.');
}

