<?php include "motoridioma.php";?>
<!doctype html>
<html lang="<?= htmlspecialchars($currentLang) ?>">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title><?= htmlspecialchars($lang['Titulo de mi web'] ?? 'Mi web') ?></title>
</head>
<body>

<?php selectorIdioma(); ?>

<h1><?= $lang['Titulo de mi web'] ?></h1>
<p><?= $lang['Texto de mi web'] ?></p>
<p><?= $lang['Este es el texto que va a contener mi web'] ?></p>

<script>
document.getElementById("idioma").addEventListener("change", function () {
    const url = new URL(window.location.href);
    url.searchParams.set("lang", this.value);
    window.location.href = url.toString();
});
</script>

</body>
</html>

