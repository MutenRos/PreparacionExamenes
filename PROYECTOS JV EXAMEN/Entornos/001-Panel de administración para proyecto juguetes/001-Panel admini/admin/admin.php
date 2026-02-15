<?php
// admin.php
session_start();
$db_path = '../recortables.db';

// Create user 'jocarsa' if not exists
try {
    $db = new PDO('sqlite:' . $db_path);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $check_user = $db->query("SELECT * FROM users WHERE username = 'jocarsa'")->fetch();
    if (!$check_user) {
        $password_hash = password_hash('jocarsa', PASSWORD_DEFAULT);
        $db->exec("INSERT INTO users (username, email, password_hash) VALUES ('jocarsa', 'jocarsa@example.com', '$password_hash')");
    }
} catch (PDOException $e) {
    die("Error: " . $e->getMessage());
}

// Login logic
if (isset($_POST['login'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $stmt = $db->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password_hash'])) {
        $_SESSION['user_id'] = $user['id'];
        header("Location: admin.php");
        exit;
    } else {
        $error = "Usuario o contraseña incorrectos";
    }
}

// Logout logic
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: admin.php");
    exit;
}

// CRUD logic for categories and products
if (isset($_SESSION['user_id'])) {
    // Add/Edit/Delete logic here (for categories and products)
    // Example for adding a category:
    if (isset($_POST['add_category'])) {
        $titulo = $_POST['titulo'];
        $imagen = $_POST['imagen'];
        $db->exec("INSERT INTO categorias (titulo, imagen) VALUES ('$titulo', '$imagen')");
    }
    // Similar logic for products and other operations...
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="estilo.css">
</head>
<body>
    <?php if (!isset($_SESSION['user_id'])): ?>
        <!-- Login Form -->
        <div class="login-container">
            <h2>Iniciar Sesión</h2>
            <?php if (isset($error)) echo "<p style='color:red;'>$error</p>"; ?>
            <form method="post">
                <input type="text" name="username" placeholder="Usuario" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit" name="login">Entrar</button>
            </form>
        </div>
    <?php else: ?>
        <!-- Dashboard -->
        <div class="dashboard">
            <div class="sidebar">
                <h2>Admin Panel</h2>
                <a href="?section=categorias">Categorías</a>
                <a href="?section=productos">Productos</a>
                <a href="?logout=1">Cerrar Sesión</a>
            </div>
            <div class="main-content">
                <?php
                $section = isset($_GET['section']) ? $_GET['section'] : 'categorias';
                if ($section === 'categorias') {
                    // Show categories CRUD
                    $categorias = $db->query("SELECT * FROM categorias")->fetchAll(PDO::FETCH_ASSOC);
                    echo "<h2>Categorías</h2>";
                    echo "<form method='post'><input type='text' name='titulo' placeholder='Título' required><input type='text' name='imagen' placeholder='Imagen'><button type='submit' name='add_category'>Añadir</button></form>";
                    echo "<table><tr><th>ID</th><th>Título</th><th>Imagen</th><th>Acciones</th></tr>";
                    foreach ($categorias as $cat) {
                        echo "<tr><td>{$cat['Identificador']}</td><td>{$cat['titulo']}</td><td>{$cat['imagen']}</td><td><a href='?edit_cat={$cat['Identificador']}'>Editar</a> | <a href='?delete_cat={$cat['Identificador']}'>Borrar</a></td></tr>";
                    }
                    echo "</table>";
                } elseif ($section === 'productos') {
                    // Show products CRUD
                    $productos = $db->query("SELECT * FROM productos")->fetchAll(PDO::FETCH_ASSOC);
                    echo "<h2>Productos</h2>";
                    echo "<form method='post'><input type='text' name='titulo' placeholder='Título' required><textarea name='descripcion' placeholder='Descripción'></textarea><input type='text' name='precio' placeholder='Precio'><input type='text' name='archivo' placeholder='Archivo'><input type='text' name='categoria' placeholder='Categoría ID'><input type='text' name='imagen' placeholder='Imagen'><button type='submit' name='add_product'>Añadir</button></form>";
                    echo "<table><tr><th>ID</th><th>Título</th><th>Descripción</th><th>Precio</th><th>Archivo</th><th>Categoría</th><th>Imagen</th><th>Acciones</th></tr>";
                    foreach ($productos as $prod) {
                        echo "<tr><td>{$prod['Identificador']}</td><td>{$prod['titulo']}</td><td>{$prod['descripcion']}</td><td>{$prod['precio']}</td><td>{$prod['archivo']}</td><td>{$prod['categoria']}</td><td>{$prod['imagen']}</td><td><a href='?edit_prod={$prod['Identificador']}'>Editar</a> | <a href='?delete_prod={$prod['Identificador']}'>Borrar</a></td></tr>";
                    }
                    echo "</table>";
                }
                ?>
            </div>
        </div>
    <?php endif; ?>
</body>
</html>

