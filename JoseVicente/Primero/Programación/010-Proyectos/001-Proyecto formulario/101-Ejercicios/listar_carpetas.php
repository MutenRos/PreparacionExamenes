<?php
$host = '{imap.ionos.es:993/imap/ssl}';
$user = 'python@jocarsa.com';
$pass = 'TAME123$';

$mbox = imap_open($host . 'INBOX', $user, $pass);

if (!$mbox) {
    die('Error IMAP: ' . imap_last_error());
}

$folders = imap_getmailboxes($mbox, $host, '*');

if ($folders === false) {
    echo "Error al obtener carpetas: " . imap_last_error();
} else {
    echo "<pre>";
    foreach ($folders as $folder) {
        // Nombre completo que debes usar en PHP (incluyendo el prefijo)
        echo $folder->name . "\n";
    }
    echo "</pre>";
}

imap_close($mbox);

