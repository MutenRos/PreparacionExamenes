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
?>
<!doctype html>
<html lang="<?= htmlspecialchars($currentLang) ?>">
<head>
    <meta charset="utf-8">
</head>
<body>

<select id="idioma">
    <?php foreach ($languages as $code => $label): ?>
        <option value="<?= htmlspecialchars($code) ?>"
            <?= $code === $currentLang ? 'selected' : '' ?>>
            <?= htmlspecialchars($label) ?>
        </option>
    <?php endforeach; ?>
</select>

<script>
document.getElementById("idioma").addEventListener("change", function () {
    const url = new URL(window.location.href);
    url.searchParams.set("lang", this.value);
    window.location.href = url.toString();
});
</script>

</body>
</html>

