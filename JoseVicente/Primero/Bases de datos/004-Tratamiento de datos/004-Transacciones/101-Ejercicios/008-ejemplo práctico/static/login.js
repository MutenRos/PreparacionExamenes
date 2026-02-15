/*
  Este archivo gestiona el login en la aplicación
  De momento se realiza un login estático
*/

// Antes de mostrar el login, quizás ya había iniciado sesión

var logeado = localStorage.getItem("logeado")
if(logeado == "true"){
  document.querySelector("footer").style.display = "none"     // Oculto el footer
    document.querySelector("header").style.display = "flex"    // Muestro el header
    document.querySelector("main").style.display = "flex"      // Muestro el main
}

let botonlogin = document.querySelector("footer button")        // Selecciono el boton
botonlogin.onclick = function(){                                // Y cuando lo pulso
  let usuario = document.querySelector("#usuario").value        // Selecciono el usuario
  let contrasena = document.querySelector("#contrasena").value  // Selecciono la contrase
  
  if(usuario == "jocarsa" && contrasena == "jocarsa"){          // Si el usuario y la c son "jocarsa"
    document.querySelector("footer").style.display = "none"     // Oculto el footer
    document.querySelector("header").style.display = "flex"    // Muestro el header
    document.querySelector("main").style.display = "flex"      // Muestro el main
    localStorage.setItem("logeado",true)
  }else{
    document.querySelector("#advertencia").textContent = "Usuario y/o contraseña incorrectos";
  }
}
