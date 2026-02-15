let articulos = document.querySelectorAll("article");

articulos.forEach(function (articulo) {
  articulo.onclick = function (e) {
    // Evitamos que el clic dispare el submit directo si cae en el botón
    if (e.target.tagName.toLowerCase() === "button" || e.target.tagName.toLowerCase() === "input") {
      return;
    }

    console.log("Has pulsado el bloque", this.id);
    this.scrollIntoView({ behavior: "smooth", block: "center" });
  };
});

