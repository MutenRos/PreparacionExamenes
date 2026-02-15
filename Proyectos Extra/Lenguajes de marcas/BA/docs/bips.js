/* ========================================
   BIPS - Selector de Bombas Asoin
   Base de datos de productos Asoin Murcia
   ======================================== */

// Base de datos de bombas Asoin
const bombasAsoin = [
    // Serie VIP V - Centrífuga Multietapa Vertical (Abastecimiento)
    { modelo: "VIP V 2-80", serie: "VIP V", categoria: "abastecimiento", caudalMax: 2.4, alturaMax: 56, potencia: 0.75, precio: 781 },
    { modelo: "VIP V 2-100", serie: "VIP V", categoria: "abastecimiento", caudalMax: 2.4, alturaMax: 71, potencia: 1.1, precio: 890 },
    { modelo: "VIP V 2-120", serie: "VIP V", categoria: "abastecimiento", caudalMax: 2.4, alturaMax: 85, potencia: 1.5, precio: 1020 },
    { modelo: "VIP V 4-80", serie: "VIP V", categoria: "abastecimiento", caudalMax: 4.5, alturaMax: 55, potencia: 1.1, precio: 950 },
    { modelo: "VIP V 4-100", serie: "VIP V", categoria: "abastecimiento", caudalMax: 4.5, alturaMax: 70, potencia: 1.5, precio: 1100 },
    { modelo: "VIP V 4-120", serie: "VIP V", categoria: "abastecimiento", caudalMax: 4.5, alturaMax: 85, potencia: 2.2, precio: 1350 },
    { modelo: "VIP V 4-150", serie: "VIP V", categoria: "abastecimiento", caudalMax: 4.5, alturaMax: 106, potencia: 3, precio: 1680 },
    { modelo: "VIP V 8-80", serie: "VIP V", categoria: "abastecimiento", caudalMax: 9, alturaMax: 54, potencia: 2.2, precio: 1450 },
    { modelo: "VIP V 8-100", serie: "VIP V", categoria: "abastecimiento", caudalMax: 9, alturaMax: 68, potencia: 3, precio: 1780 },
    { modelo: "VIP V 8-120", serie: "VIP V", categoria: "abastecimiento", caudalMax: 9, alturaMax: 82, potencia: 4, precio: 2100 },
    { modelo: "VIP V 16-80", serie: "VIP V", categoria: "abastecimiento", caudalMax: 18, alturaMax: 52, potencia: 4, precio: 2250 },
    { modelo: "VIP V 16-100", serie: "VIP V", categoria: "abastecimiento", caudalMax: 18, alturaMax: 66, potencia: 5.5, precio: 2562 },

    // Serie GIP - Grupo de Presión Doméstico (Abastecimiento)
    { modelo: "GIP 25", serie: "GIP", categoria: "abastecimiento", caudalMax: 3, alturaMax: 35, potencia: 0.55, precio: 650 },
    { modelo: "GIP 35", serie: "GIP", categoria: "abastecimiento", caudalMax: 4, alturaMax: 45, potencia: 0.75, precio: 720 },
    { modelo: "GIP 45", serie: "GIP", categoria: "abastecimiento", caudalMax: 5, alturaMax: 55, potencia: 1.1, precio: 810 },
    { modelo: "GIP 55", serie: "GIP", categoria: "abastecimiento", caudalMax: 6, alturaMax: 65, potencia: 1.5, precio: 890 },

    // Serie VIPH - Multicelular Horizontal (Agricultura)
    { modelo: "VIPH 2/3", serie: "VIPH", categoria: "agricultura", caudalMax: 3, alturaMax: 28, potencia: 0.37, precio: 331 },
    { modelo: "VIPH 2/4", serie: "VIPH", categoria: "agricultura", caudalMax: 3, alturaMax: 38, potencia: 0.55, precio: 385 },
    { modelo: "VIPH 2/5", serie: "VIPH", categoria: "agricultura", caudalMax: 3, alturaMax: 47, potencia: 0.75, precio: 440 },
    { modelo: "VIPH 4/3", serie: "VIPH", categoria: "agricultura", caudalMax: 5.5, alturaMax: 26, potencia: 0.55, precio: 410 },
    { modelo: "VIPH 4/4", serie: "VIPH", categoria: "agricultura", caudalMax: 5.5, alturaMax: 35, potencia: 0.75, precio: 465 },
    { modelo: "VIPH 4/5", serie: "VIPH", categoria: "agricultura", caudalMax: 5.5, alturaMax: 44, potencia: 1.1, precio: 540 },
    { modelo: "VIPH 4/6", serie: "VIPH", categoria: "agricultura", caudalMax: 5.5, alturaMax: 53, potencia: 1.5, precio: 620 },
    { modelo: "VIPH 8/3", serie: "VIPH", categoria: "agricultura", caudalMax: 10, alturaMax: 24, potencia: 0.75, precio: 520 },
    { modelo: "VIPH 8/4", serie: "VIPH", categoria: "agricultura", caudalMax: 10, alturaMax: 32, potencia: 1.1, precio: 610 },
    { modelo: "VIPH 8/5", serie: "VIPH", categoria: "agricultura", caudalMax: 10, alturaMax: 40, potencia: 1.5, precio: 720 },
    { modelo: "VIPH 8/6", serie: "VIPH", categoria: "agricultura", caudalMax: 10, alturaMax: 48, potencia: 2.2, precio: 850 },
    { modelo: "VIPH 12/4", serie: "VIPH", categoria: "agricultura", caudalMax: 15, alturaMax: 30, potencia: 1.5, precio: 780 },
    { modelo: "VIPH 12/5", serie: "VIPH", categoria: "agricultura", caudalMax: 15, alturaMax: 38, potencia: 2.2, precio: 890 },
    { modelo: "VIPH 12/6", serie: "VIPH", categoria: "agricultura", caudalMax: 15, alturaMax: 46, potencia: 3, precio: 945 },

    // Serie VIPH Industrial - Multicelular Horizontal Industrial (Agricultura)
    { modelo: "VIPH IND 15/4", serie: "VIPH Industrial", categoria: "agricultura", caudalMax: 18, alturaMax: 35, potencia: 2.2, precio: 799 },
    { modelo: "VIPH IND 15/5", serie: "VIPH Industrial", categoria: "agricultura", caudalMax: 18, alturaMax: 44, potencia: 3, precio: 850 },
    { modelo: "VIPH IND 15/6", serie: "VIPH Industrial", categoria: "agricultura", caudalMax: 18, alturaMax: 53, potencia: 4, precio: 920 },
    { modelo: "VIPH IND 20/4", serie: "VIPH Industrial", categoria: "agricultura", caudalMax: 24, alturaMax: 32, potencia: 3, precio: 870 },
    { modelo: "VIPH IND 20/5", serie: "VIPH Industrial", categoria: "agricultura", caudalMax: 24, alturaMax: 40, potencia: 4, precio: 945 },

    // Serie VARI IP - Autoaspirante Piscinas (Piscinas)
    { modelo: "VARI IP 750", serie: "VARI IP", categoria: "piscinas", caudalMax: 15, alturaMax: 12, potencia: 0.75, precio: 1150 },
    { modelo: "VARI IP 1000", serie: "VARI IP", categoria: "piscinas", caudalMax: 18, alturaMax: 14, potencia: 1.1, precio: 1250 },
    { modelo: "VARI IP 1500", serie: "VARI IP", categoria: "piscinas", caudalMax: 24, alturaMax: 15, potencia: 1.5, precio: 1355 },

    // Serie HHG Compact - Grupo Presión Compacto (Abastecimiento)
    { modelo: "HHG Compact 45", serie: "HHG Compact", categoria: "abastecimiento", caudalMax: 4.5, alturaMax: 48, potencia: 1.1, precio: 913 },
    { modelo: "HHG Compact 55", serie: "HHG Compact", categoria: "abastecimiento", caudalMax: 5.5, alturaMax: 58, potencia: 1.5, precio: 985 },
    { modelo: "HHG Compact 65", serie: "HHG Compact", categoria: "abastecimiento", caudalMax: 6.5, alturaMax: 68, potencia: 2.2, precio: 1011 },

    // Serie IPE 2 - Piscinas pequeñas/medianas (Piscinas)
    { modelo: "IPE 2-50", serie: "IPE 2", categoria: "piscinas", caudalMax: 12, alturaMax: 8, potencia: 0.37, precio: 381 },
    { modelo: "IPE 2-75", serie: "IPE 2", categoria: "piscinas", caudalMax: 14, alturaMax: 10, potencia: 0.55, precio: 420 },
    { modelo: "IPE 2-100", serie: "IPE 2", categoria: "piscinas", caudalMax: 16, alturaMax: 11, potencia: 0.75, precio: 456 },

    // Serie IPE 3 - Piscinas grandes (Piscinas)
    { modelo: "IPE 3-100", serie: "IPE 3", categoria: "piscinas", caudalMax: 20, alturaMax: 12, potencia: 0.75, precio: 812 },
    { modelo: "IPE 3-150", serie: "IPE 3", categoria: "piscinas", caudalMax: 24, alturaMax: 14, potencia: 1.1, precio: 840 },
    { modelo: "IPE 3-200", serie: "IPE 3", categoria: "piscinas", caudalMax: 28, alturaMax: 16, potencia: 1.5, precio: 865 },

    // Serie VORTEX - Sumergible Achique/Residuales (Achique)
    { modelo: "VORTEX 150", serie: "VORTEX", categoria: "achique", caudalMax: 18, alturaMax: 8, potencia: 1.1, precio: 822 },
    { modelo: "VORTEX 200", serie: "VORTEX", categoria: "achique", caudalMax: 24, alturaMax: 10, potencia: 1.5, precio: 980 },
    { modelo: "VORTEX 250", serie: "VORTEX", categoria: "achique", caudalMax: 30, alturaMax: 11, potencia: 2.2, precio: 1150 },
    { modelo: "VORTEX 300", serie: "VORTEX", categoria: "achique", caudalMax: 36, alturaMax: 12, potencia: 3, precio: 1420 },
    { modelo: "VORTEX 400", serie: "VORTEX", categoria: "achique", caudalMax: 48, alturaMax: 14, potencia: 4, precio: 1682 },

    // Serie HXN - Centrífuga Horizontal (Abastecimiento)
    { modelo: "HXN 3", serie: "HXN", categoria: "abastecimiento", caudalMax: 4.2, alturaMax: 22, potencia: 0.37, precio: 345 },
    { modelo: "HXN 4", serie: "HXN", categoria: "abastecimiento", caudalMax: 5.4, alturaMax: 28, potencia: 0.55, precio: 390 },
    { modelo: "HXN 5", serie: "HXN", categoria: "abastecimiento", caudalMax: 6.6, alturaMax: 32, potencia: 0.75, precio: 445 },
    { modelo: "HXN 6", serie: "HXN", categoria: "abastecimiento", caudalMax: 8, alturaMax: 36, potencia: 1.1, precio: 501 }
];

// Variables globales
let categoriaSeleccionada = 'all';

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Category buttons
    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            categoriaSeleccionada = this.dataset.category;
        });
    });
    
    // Search button
    const searchBtn = document.getElementById('searchBtn');
    searchBtn.addEventListener('click', buscarBombas);
    
    // Enter key
    document.getElementById('caudal').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') buscarBombas();
    });
    document.getElementById('altura').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') buscarBombas();
    });
});

function buscarBombas() {
    const caudal = parseFloat(document.getElementById('caudal').value) || 0;
    const altura = parseFloat(document.getElementById('altura').value) || 0;
    
    // Validar que al menos un campo tiene valor
    if (caudal <= 0 && altura <= 0) {
        alert('Introduce al menos un valor de caudal o altura para buscar.');
        return;
    }
    
    // Filter pumps
    let resultados = bombasAsoin.filter(bomba => {
        const cumpleCaudal = bomba.caudalMax >= caudal;
        const cumpleAltura = bomba.alturaMax >= altura;
        const cumpleCategoria = categoriaSeleccionada === 'all' || bomba.categoria === categoriaSeleccionada;
        
        return cumpleCaudal && cumpleAltura && cumpleCategoria;
    });
    
    // Sort by best fit (closest to requirements without exceeding)
    resultados.sort((a, b) => {
        const diffA = (a.caudalMax - caudal) + (a.alturaMax - altura);
        const diffB = (b.caudalMax - caudal) + (b.alturaMax - altura);
        return diffA - diffB;
    });
    
    mostrarResultados(resultados, caudal, altura);
}

function mostrarResultados(resultados, caudal, altura) {
    const section = document.getElementById('resultsSection');
    const grid = document.getElementById('resultsGrid');
    const count = document.getElementById('resultsCount');
    
    section.classList.add('visible');
    count.textContent = resultados.length;
    
    if (resultados.length === 0) {
        grid.innerHTML = `
            <div class="no-results" style="grid-column: 1 / -1;">
                <i class="fas fa-search"></i>
                <h3>No se encontraron resultados</h3>
                <p>Prueba con otros valores de caudal o altura, o contacta con nosotros para asesoramiento personalizado.</p>
                <a href="contacto.html" class="btn btn-primary"><i class="fas fa-phone"></i> Contactar</a>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = resultados.map((bomba, index) => {
        const isBestMatch = index === 0 && (caudal > 0 || altura > 0);
        const icon = getCategoryIcon(bomba.categoria);
        const categoryLabel = getCategoryLabel(bomba.categoria);
        
        return `
            <div class="result-card ${isBestMatch ? 'best-match' : ''}">
                <div class="result-header">
                    <div class="result-icon">
                        <i class="fas ${icon}"></i>
                    </div>
                    <div>
                        <h3>${bomba.modelo}</h3>
                        <span class="result-series">Serie ${bomba.serie}</span>
                    </div>
                </div>
                
                <span class="result-category">${categoryLabel}</span>
                
                <div class="result-specs">
                    <div class="spec-item">
                        <label>Caudal máx.</label>
                        <value>${bomba.caudalMax} m³/h</value>
                    </div>
                    <div class="spec-item">
                        <label>Altura máx.</label>
                        <value>${bomba.alturaMax} m</value>
                    </div>
                    <div class="spec-item">
                        <label>Potencia</label>
                        <value>${bomba.potencia} kW</value>
                    </div>
                    <div class="spec-item">
                        <label>Precio</label>
                        <value>${bomba.precio.toLocaleString('es-ES')} €</value>
                    </div>
                </div>
                
                <a href="contacto.html?producto=${encodeURIComponent(bomba.modelo)}" class="btn btn-primary">
                    <i class="fas fa-info-circle"></i> Solicitar información
                </a>
            </div>
        `;
    }).join('');
    
    // Scroll to results
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function getCategoryIcon(categoria) {
    const icons = {
        'agricultura': 'fa-seedling',
        'abastecimiento': 'fa-faucet',
        'achique': 'fa-water',
        'piscinas': 'fa-swimming-pool'
    };
    return icons[categoria] || 'fa-tint';
}

function getCategoryLabel(categoria) {
    const labels = {
        'agricultura': 'Agricultura',
        'abastecimiento': 'Abastecimiento',
        'achique': 'Achique',
        'piscinas': 'Piscinas'
    };
    return labels[categoria] || categoria;
}
