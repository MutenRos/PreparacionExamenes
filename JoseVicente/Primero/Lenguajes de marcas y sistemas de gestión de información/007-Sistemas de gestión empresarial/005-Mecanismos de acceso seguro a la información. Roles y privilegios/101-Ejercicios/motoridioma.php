<?php
session_start();

/* 1. Available languages */
$languages = [
    "es" => "Español 🇪🇸",
    "en" => "English 🇬🇧",
    "fr" => "Français 🇫🇷",
    "de" => "Deutsch 🇩🇪",
    "it" => "Italiano 🇮🇹",
    "pt" => "Português 🇵🇹",
    "nl" => "Nederlands 🇳🇱",
    "sv" => "Svenska 🇸🇪",
    "da" => "Dansk 🇩🇰",
    "fi" => "Suomi 🇫🇮",
    "no" => "Norsk 🇳🇴",
    "pl" => "Polski 🇵🇱",
    "cs" => "Čeština 🇨🇿",
    "sk" => "Slovenčina 🇸🇰",
    "hu" => "Magyar 🇭🇺",
    "ro" => "Română 🇷🇴",
    "bg" => "Български 🇧🇬",
    "el" => "Ελληνικά 🇬🇷",
    "hr" => "Hrvatski 🇭🇷",
    "sl" => "Slovenščina 🇸🇮",
    "et" => "Eesti 🇪🇪",
    "lv" => "Latviešu 🇱🇻",
    "lt" => "Lietuvių 🇱🇹",
    "mt" => "Malti 🇲🇹",
    "ga" => "Gaeilge 🇮🇪"
];

/* 2. Default language */
if (!isset($_SESSION['lang'])) {
    $_SESSION['lang'] = "es";
}

/* 3. Change language (only if valid) */
if (isset($_GET['lang']) && array_key_exists($_GET['lang'], $languages)) {
    $_SESSION['lang'] = $_GET['lang'];
}

$currentLang = $_SESSION['lang'];

/* 4. Load translations from CSV into $lang array (Spanish column is the KEY) */
$lang = [];

$csvPath = __DIR__ . "/idiomas.csv";
$fh = fopen($csvPath, "r");
if ($fh === false) {
    http_response_code(500);
    die("Cannot open translation file: " . htmlspecialchars($csvPath));
}

/* Read header row: "es","en","fr",... */
$headers = fgetcsv($fh);
if ($headers === false) {
    fclose($fh);
    http_response_code(500);
    die("Translation CSV is empty or invalid.");
}

$baseIndex = array_search("es", $headers, true);
$currentIndex = array_search($currentLang, $headers, true);

if ($baseIndex === false) {
    fclose($fh);
    http_response_code(500);
    die('Translation CSV must include an "es" column header.');
}

/* If current language column missing, fallback to ES */
if ($currentIndex === false) {
    $currentIndex = $baseIndex;
}

while (($row = fgetcsv($fh)) !== false) {
    if (!isset($row[$baseIndex])) {
        continue;
    }

    $key = $row[$baseIndex];

    /* Value in selected language or fallback to ES or key */
    $value = $row[$currentIndex] ?? ($row[$baseIndex] ?? $key);

    $lang[$key] = $value;
}

fclose($fh);

function selectorIdioma(){
    global $languages, $currentLang;

    echo '<select id="idioma">';
    foreach ($languages as $code => $label){
        echo '<option value="'.htmlspecialchars($code).'"';
        if ($code === $currentLang) {
            echo ' selected';
        }
        echo '>'.$label.'</option>';
    }
    echo '</select>';
}


?>















