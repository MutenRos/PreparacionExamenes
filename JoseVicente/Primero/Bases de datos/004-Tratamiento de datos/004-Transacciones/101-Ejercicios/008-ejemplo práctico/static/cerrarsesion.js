let cerrarsesion = document.querySelector("#cerrarsesion")

cerrarsesion.onclick = function(){
  localStorage.setItem("logeado",false)
  window.location = window.location
}
