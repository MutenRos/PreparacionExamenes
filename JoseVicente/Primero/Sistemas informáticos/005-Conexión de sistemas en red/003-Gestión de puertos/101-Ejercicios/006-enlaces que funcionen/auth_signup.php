<?php
session_start();

function redirect_with(string $msg, string $to = 'login.php'): void {
  $_SESSION['flash'] = $msg;
  header("Location: $to");
  exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') redirect_with('Acceso no permitido.');

if (empty($_POST['csrf']) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], (string)$_POST['csrf'])) {
  redirect_with('Sesión caducada. Vuelve a intentarlo.');
}

$username = trim((string)($_POST['username'] ?? ''));
$email    = trim((string)($_POST['email'] ?? ''));
$pass     = (string)($_POST['password'] ?? '');
$pass2    = (string)($_POST['password2'] ?? '');
$terms    = isset($_POST['terms']);

if ($username === '' || $email === '' || $pass === '' || $pass2 === '') redirect_with('Completa todos los campos.');
if (!$terms) redirect_with('Debes aceptar las condiciones.');
if (mb_strlen($username) < 2 || mb_strlen($username) > 40) redirect_with('El nombre de usuario debe tener 2–40 caracteres.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) redirect_with('Email no válido.');
if (strlen($pass) < 8) redirect_with('La contraseña debe tener al menos 8 caracteres.');
if (!hash_equals($pass, $pass2)) redirect_with('Las contraseñas no coinciden.');

try {
  $db = new SQLite3(__DIR__ . '/recortables.db');
  $db->busyTimeout(2000);

  // Ensure table exists
  $db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
  )");
  $db->exec("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)");

  // Check email exists
  $stmt = $db->prepare("SELECT id FROM users WHERE email = :email LIMIT 1");
  $stmt->bindValue(':email', $email, SQLITE3_TEXT);
  $res = $stmt->execute();
  $row = $res ? $res->fetchArray(SQLITE3_ASSOC) : false;
  if ($row) redirect_with('Ese email ya está registrado.');

  $hash = password_hash($pass, PASSWORD_DEFAULT);

  $ins = $db->prepare("INSERT INTO users (username, email, password_hash) VALUES (:u, :e, :p)");
  $ins->bindValue(':u', $username, SQLITE3_TEXT);
  $ins->bindValue(':e', $email, SQLITE3_TEXT);
  $ins->bindValue(':p', $hash, SQLITE3_TEXT);
  $ok = $ins->execute();

  if (!$ok) redirect_with('No se pudo crear la cuenta. Inténtalo de nuevo.');

  // Auto-login after signup
  $userId = (int)$db->lastInsertRowID();
  session_regenerate_id(true);
  $_SESSION['user'] = [
    'id' => $userId,
    'username' => $username,
    'email' => $email,
  ];

  header("Location: index.php");
  exit;

} catch (Throwable $e) {
  redirect_with('Error interno. Inténtalo de nuevo.');
}

