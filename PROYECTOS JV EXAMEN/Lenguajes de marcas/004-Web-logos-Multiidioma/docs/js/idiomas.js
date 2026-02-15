/* ============================================
   idiomas.js — Sistema de cambio de idioma
   Permite alternar entre ES, EN y FR
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {

    // Referencia a los botones del selector de idioma
    var botonesIdioma = document.querySelectorAll('.selector-idioma button');
    var idiomaActual = 'es';

    /**
     * Cambia el idioma de todos los elementos que tengan
     * atributos data-es, data-en o data-fr
     */
    function cambiarIdioma(idioma) {
        idiomaActual = idioma;

        // Buscar todos los elementos con el atributo data-[idioma]
        var elementos = document.querySelectorAll('[data-' + idioma + ']');

        elementos.forEach(function(el) {
            var texto = el.getAttribute('data-' + idioma);

            if (texto) {
                // Para inputs tipo text/email se cambia el placeholder
                if (el.tagName === 'INPUT' && el.type !== 'submit') {
                    el.placeholder = texto;
                }
                // Para inputs tipo submit se cambia el value
                else if (el.tagName === 'INPUT' && el.type === 'submit') {
                    el.value = texto;
                }
                // Para el resto de elementos se cambia el texto
                else {
                    el.textContent = texto;
                }
            }
        });

        // Marcar el boton activo y desmarcar los demas
        botonesIdioma.forEach(function(btn) {
            btn.classList.remove('activo');
            if (btn.getAttribute('data-lang') === idioma) {
                btn.classList.add('activo');
            }
        });

        // Actualizar el atributo lang del documento HTML
        document.documentElement.lang = idioma;

        // Mostrar mensaje en consola para depuracion
        console.log('Idioma cambiado a: ' + idioma.toUpperCase());
    }

    // Asignar evento click a cada boton de idioma
    botonesIdioma.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var idioma = this.getAttribute('data-lang');

            // Confirmacion antes de cambiar (mejora UX)
            if (idioma !== idiomaActual) {
                cambiarIdioma(idioma);
            }
        });
    });

    // Validacion basica del formulario de contacto
    var formulario = document.querySelector('#contacto form');

    if (formulario) {
        formulario.addEventListener('submit', function(evento) {
            evento.preventDefault();

            var nombre = document.getElementById('nombre');
            var email = document.getElementById('email');
            var mensaje = document.getElementById('mensaje');

            // Comprobar que los campos no estan vacios
            if (!nombre.value.trim() || !email.value.trim() || !mensaje.value.trim()) {
                alert(idiomaActual === 'es' ? '⚠️ Por favor, rellena todos los campos.' :
                      idiomaActual === 'en' ? '⚠️ Please fill in all fields.' :
                      '⚠️ Veuillez remplir tous les champs.');
                return;
            }

            // Comprobar formato de email basico
            if (email.value.indexOf('@') === -1 || email.value.indexOf('.') === -1) {
                alert(idiomaActual === 'es' ? '⚠️ El email no parece válido.' :
                      idiomaActual === 'en' ? '⚠️ The email does not appear valid.' :
                      '⚠️ L\'email ne semble pas valide.');
                return;
            }

            // Confirmacion de envio
            var confirmacion = confirm(
                idiomaActual === 'es' ? '¿Enviar el mensaje?' :
                idiomaActual === 'en' ? 'Send the message?' :
                'Envoyer le message ?'
            );

            if (confirmacion) {
                alert(idiomaActual === 'es' ? '✅ Mensaje enviado correctamente.' :
                      idiomaActual === 'en' ? '✅ Message sent successfully.' :
                      '✅ Message envoyé avec succès.');
                formulario.reset();
            }
        });
    }

});
