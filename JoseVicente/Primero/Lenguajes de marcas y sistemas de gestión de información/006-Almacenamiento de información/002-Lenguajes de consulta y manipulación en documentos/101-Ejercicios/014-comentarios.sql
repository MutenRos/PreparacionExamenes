ALTER TABLE inscripciones
    MODIFY id INT AUTO_INCREMENT PRIMARY KEY
        COMMENT 'Identificador único y autoincrementado de cada inscripción registrada en el sistema';

ALTER TABLE inscripciones
    MODIFY nombre VARCHAR(100) NOT NULL
        COMMENT 'Nombre propio del alumno tal como debe aparecer en los documentos oficiales del centro';

ALTER TABLE inscripciones
    MODIFY apellidos VARCHAR(150) NOT NULL
        COMMENT 'Apellidos del alumno, utilizados para certificados, facturación y listados administrativos';

ALTER TABLE inscripciones
    MODIFY email VARCHAR(150) UNIQUE NOT NULL
        COMMENT 'Correo electrónico del alumno; se utiliza como identificador de contacto y debe ser único';

ALTER TABLE inscripciones
    MODIFY telefono VARCHAR(20)
        COMMENT 'Número de teléfono del alumno para comunicación directa sobre el curso';

ALTER TABLE inscripciones
    MODIFY curso VARCHAR(200) NOT NULL
        COMMENT 'Nombre del curso al que el alumno se inscribe (título comercial o académico)';

ALTER TABLE inscripciones
    MODIFY fecha_inscripcion DATE NOT NULL
        COMMENT 'Fecha exacta en la que se registró la inscripción en el sistema';

ALTER TABLE inscripciones
    MODIFY edad INT
        COMMENT 'Edad del alumno en el momento de realizar la inscripción';

ALTER TABLE inscripciones
    MODIFY precio DECIMAL(10,2)
        COMMENT 'Coste total del curso en euros, incluyendo descuentos si los hubiera';

ALTER TABLE inscripciones
    MODIFY pagado BOOLEAN DEFAULT 0
        COMMENT 'Indica si el alumno ha completado el pago del curso (0 = no pagado, 1 = pagado)';

ALTER TABLE inscripciones
    MODIFY modalidad ENUM('presencial','online','mixto')
        COMMENT 'Tipo de impartición: presencial en aula, online en plataforma, o modalidad mixta';

ALTER TABLE inscripciones
    MODIFY notas TEXT
        COMMENT 'Campo de texto libre para observaciones internas: peticiones, incidencias, nivel previo, etc.';

ALTER TABLE inscripciones
    MODIFY documento BLOB
        COMMENT 'Archivo adjunto opcional (DNI escaneado, justificante de pago, documentos administrativos, etc.)';

ALTER TABLE inscripciones
    MODIFY creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        COMMENT 'Marca de tiempo que registra automáticamente cuándo se creó la inscripción';

ALTER TABLE inscripciones
    COMMENT = 'Registra todas las inscripciones de alumnos con sus datos personales, curso, modalidad y estado de pago.';


