/*
  Este archivo gestiona la información que proviene del servidor
  Se encarga de poblar el menú y poblar la tabla en base al elemento de menú seleccionado
*/

let menu = document.querySelector("nav")

fetch("http://127.0.0.1:5000/api")
.then(function(respuesta){return respuesta.json();})
.then(function(datos){
  console.log(datos);
  // Quiero saber cuantas tablas tengo
  Object.entries(datos).forEach(function([clave, valor]){ // Por cada tabla
    let boton = document.createElement("button");         // Crea un boton
    boton.textContent = clave                             // Le pone texto
    menu.appendChild(boton)                               // Y lo añade al menu
    boton.onclick = function(){
      console.log("Has hecho click en el boton")
      pueblaTabla(boton.textContent,datos[boton.textContent])         // Llamo a la tabla del boton y le paso los datos
    }
  })
  
})

function pueblaTabla(mitabla,misdatos){                   // Recoge el nombre de la tabla y el pack de datos
  /*
    Función que se encarga de poblar la tabla:
    Parámetros de entrada: La tabla y los datos a poblar
    Salida: Las cabeceras de tabla y el cuerpo de la tabla
  */
  // Primero vacío lo que tuviera la tabla
  let cabeceratabla = document.querySelector("table thead tr"); // Selecciono la cabecera
  cabeceratabla.innerHTML = ""                            // Vacío la cabecera
  let cuerpotabla = document.querySelector("table tbody") // Selecciono el cuerpo de la tabla
  cuerpotabla.innerHTML = ""                              // Vacío el cuerpo de la tabla
  
  // Ahora quiero poblar una tabla
  let tabla = mitabla;                                  // Selecciono una tabla
  let contenido = misdatos                            // Cargo el contenido de la tabla
  
  // Primero pongo las cabeceras                         
  Object.entries(contenido[0]).forEach(function([clave, valor]){  // Seleccion las claves de la primera f
    let cabecera = document.createElement("th")           // Creo un elemento cabecera
    cabecera.textContent = clave;                         // Le pongo el texto
    cabeceratabla.appendChild(cabecera)                   // Y lo añado a la cabecera de la tabla
  })
  // Pongo el contenido de cada fila de la tabla          
  
  contenido.forEach(function(fila){                       // Por cada pieza de información  de los datos
    let filatabla = document.createElement("tr")          // Creo una fila de tabla en HTML
    Object.entries(fila).forEach(function([clave, valor]){  // Y entonces por cada uno de los objetos
      let celda = document.createElement("td")            // Creo una celda
      celda.textContent = valor                           // Le pongo valor a la celda
      filatabla.appendChild(celda)                        // Añado la celda a la fila
    })
    cuerpotabla.appendChild(filatabla);                   // Y añado la fila a tabla
  })
}


