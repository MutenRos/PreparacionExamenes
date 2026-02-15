<?php
require __DIR__ . '/jvpug.php';

echo JVpug::renderFile(__DIR__ . '/perfil.jvpug', [
    'nombre' => 'Jose Vicente Carratalá',
    'titulo' => 'Desarrollador, profesor y diseñador de software',
    'descripcion' =>
        'Trabajo en el diseño y desarrollo de soluciones tecnológicas orientadas a la educación, '
      . 'la automatización y la creación de productos digitales útiles, claros y sostenibles.',
    'areas' => [
        'Desarrollo de software',
        'Formación técnica y docencia',
        'Diseño de herramientas educativas',
        'Automatización y sistemas',
        'Inteligencia artificial aplicada'
    ],
    'enfoque_html' =>
        '<strong>Aprender haciendo</strong>, construir sistemas simples pero sólidos, '
      . 'y utilizar la tecnología como una herramienta para amplificar el conocimiento '
      . 'y la autonomía de las personas.',
    'year' => date('Y')
]);

