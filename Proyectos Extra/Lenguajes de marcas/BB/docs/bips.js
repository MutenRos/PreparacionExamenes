// BIPS - Bloch Intelligent Pump Selector
// Base de datos de productos Bombas Bloch

const bombasBloch = [
    // SERIE H - Horizontales Domésticas
    { modelo: "H-40/1", caudal: 3.6, altura: 32, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Riego jardín, trasvase", serie: "H" },
    { modelo: "H-50/1", caudal: 4.2, altura: 38, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Riego jardín, presión doméstica", serie: "H" },
    { modelo: "H-60/1", caudal: 4.8, altura: 45, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Riego, pequeñas instalaciones", serie: "H" },
    { modelo: "H-80/1", caudal: 6.0, altura: 52, potencia: 1.1, categoria: "Horizontales Domésticas", aplicacion: "Presión doméstica, riego", serie: "H" },
    { modelo: "H-100/1", caudal: 7.2, altura: 60, potencia: 1.5, categoria: "Horizontales Domésticas", aplicacion: "Grupos de presión", serie: "H" },
    
    // SERIE H INDUSTRIAL
    { modelo: "H-125/2", caudal: 12, altura: 45, potencia: 2.2, categoria: "Horizontales Industriales", aplicacion: "Industria, climatización", serie: "H Industrial" },
    { modelo: "H-150/2", caudal: 18, altura: 52, potencia: 3.0, categoria: "Horizontales Industriales", aplicacion: "Industria, refrigeración", serie: "H Industrial" },
    { modelo: "H-200/2", caudal: 24, altura: 58, potencia: 4.0, categoria: "Horizontales Industriales", aplicacion: "Procesos industriales", serie: "H Industrial" },
    { modelo: "H-250/2", caudal: 36, altura: 65, potencia: 5.5, categoria: "Horizontales Industriales", aplicacion: "Grandes instalaciones", serie: "H Industrial" },
    { modelo: "H-300/2", caudal: 48, altura: 72, potencia: 7.5, categoria: "Horizontales Industriales", aplicacion: "Industria pesada", serie: "H Industrial" },
    
    // SERIE HXN - Horizontales Inox
    { modelo: "HXN-40", caudal: 3.0, altura: 30, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Agua potable, alimentaria", serie: "HXN" },
    { modelo: "HXN-50", caudal: 3.6, altura: 36, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Agua potable, presión", serie: "HXN" },
    { modelo: "HXN-60", caudal: 4.2, altura: 42, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Instalaciones sanitarias", serie: "HXN" },
    { modelo: "HXN-80", caudal: 5.4, altura: 48, potencia: 1.1, categoria: "Horizontales Domésticas", aplicacion: "Edificios, viviendas", serie: "HXN" },
    { modelo: "HXN-100", caudal: 6.6, altura: 55, potencia: 1.5, categoria: "Horizontales Domésticas", aplicacion: "Grupos presión inox", serie: "HXN" },
    
    // SERIE JET - Autoaspirantes
    { modelo: "JET-60", caudal: 2.4, altura: 35, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Pozos poca profundidad", serie: "JET" },
    { modelo: "JET-80", caudal: 3.0, altura: 40, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Aspiración hasta 8m", serie: "JET" },
    { modelo: "JET-100", caudal: 3.6, altura: 45, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Riego desde pozo", serie: "JET" },
    { modelo: "JET-150", caudal: 4.8, altura: 50, potencia: 1.1, categoria: "Horizontales Domésticas", aplicacion: "Autoaspirante potente", serie: "JET" },
    
    // SERIE JET INOX
    { modelo: "JET-60 INOX", caudal: 2.4, altura: 35, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Agua potable, pozos", serie: "JET Inox" },
    { modelo: "JET-80 INOX", caudal: 3.0, altura: 40, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Instalaciones sanitarias", serie: "JET Inox" },
    { modelo: "JET-100 INOX", caudal: 3.6, altura: 45, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Calidad alimentaria", serie: "JET Inox" },
    
    // SERIE PR - Periféricas
    { modelo: "PR-05", caudal: 2.1, altura: 28, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Pequeño riego, trasvase", serie: "PR" },
    { modelo: "PR-10", caudal: 2.4, altura: 35, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Presión baja, jardín", serie: "PR" },
    { modelo: "PR-15", caudal: 2.7, altura: 42, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Alta presión doméstica", serie: "PR" },
    
    // SERIE CPA - Centrífugas
    { modelo: "CPA-130", caudal: 7.8, altura: 25, potencia: 0.55, categoria: "Horizontales Domésticas", aplicacion: "Alto caudal, bajo altura", serie: "CPA" },
    { modelo: "CPA-160", caudal: 9.6, altura: 30, potencia: 0.75, categoria: "Horizontales Domésticas", aplicacion: "Riego extensivo", serie: "CPA" },
    { modelo: "CPA-200", caudal: 12, altura: 35, potencia: 1.1, categoria: "Horizontales Domésticas", aplicacion: "Trasvase gran caudal", serie: "CPA" },
    
    // SERIE DA - Doble Rodete
    { modelo: "DA-80", caudal: 4.8, altura: 55, potencia: 1.1, categoria: "Horizontales Domésticas", aplicacion: "Alta presión, edificios", serie: "DA" },
    { modelo: "DA-100", caudal: 6.0, altura: 65, potencia: 1.5, categoria: "Horizontales Domésticas", aplicacion: "Grupos de presión", serie: "DA" },
    { modelo: "DA-130", caudal: 7.8, altura: 75, potencia: 2.2, categoria: "Horizontales Domésticas", aplicacion: "Alta presión potente", serie: "DA" },
    
    // SERIE HG/HGB - Circuladoras
    { modelo: "HG-32/8", caudal: 3.6, altura: 8, potencia: 0.18, categoria: "Horizontales Domésticas", aplicacion: "Calefacción, ACS", serie: "HG" },
    { modelo: "HG-40/8", caudal: 6.0, altura: 8, potencia: 0.25, categoria: "Horizontales Domésticas", aplicacion: "Climatización", serie: "HG" },
    { modelo: "HGB-50/12", caudal: 9.0, altura: 12, potencia: 0.37, categoria: "Horizontales Domésticas", aplicacion: "Recirculación industrial", serie: "HGB" },
    
    // VERTICALES DE SUPERFICIE - Multicelulares
    { modelo: "VE-120/3", caudal: 4.8, altura: 45, potencia: 0.75, categoria: "Verticales de Superficie", aplicacion: "Presión constante", serie: "VE" },
    { modelo: "VE-120/4", caudal: 4.8, altura: 58, potencia: 1.1, categoria: "Verticales de Superficie", aplicacion: "Edificios, hoteles", serie: "VE" },
    { modelo: "VE-120/5", caudal: 4.8, altura: 72, potencia: 1.5, categoria: "Verticales de Superficie", aplicacion: "Alta presión", serie: "VE" },
    { modelo: "VE-150/3", caudal: 7.2, altura: 42, potencia: 1.1, categoria: "Verticales de Superficie", aplicacion: "Mayor caudal", serie: "VE" },
    { modelo: "VE-150/4", caudal: 7.2, altura: 55, potencia: 1.5, categoria: "Verticales de Superficie", aplicacion: "Comunidades", serie: "VE" },
    { modelo: "VE-150/5", caudal: 7.2, altura: 68, potencia: 2.2, categoria: "Verticales de Superficie", aplicacion: "Industria", serie: "VE" },
    { modelo: "VE-200/3", caudal: 12, altura: 38, potencia: 1.5, categoria: "Verticales de Superficie", aplicacion: "Alto caudal", serie: "VE" },
    { modelo: "VE-200/4", caudal: 12, altura: 50, potencia: 2.2, categoria: "Verticales de Superficie", aplicacion: "Grandes edificios", serie: "VE" },
    { modelo: "VE-200/5", caudal: 12, altura: 62, potencia: 3.0, categoria: "Verticales de Superficie", aplicacion: "Industria pesada", serie: "VE" },
    
    // SUMERGIBLES PARA POZOS 4"
    { modelo: "SP4-0508", caudal: 1.8, altura: 52, potencia: 0.37, categoria: "Sumergibles para Pozos", aplicacion: "Pozos 4\" pequeños", serie: "SP4" },
    { modelo: "SP4-0512", caudal: 1.8, altura: 78, potencia: 0.55, categoria: "Sumergibles para Pozos", aplicacion: "Pozos profundos", serie: "SP4" },
    { modelo: "SP4-0516", caudal: 1.8, altura: 104, potencia: 0.75, categoria: "Sumergibles para Pozos", aplicacion: "Gran profundidad", serie: "SP4" },
    { modelo: "SP4-1008", caudal: 3.6, altura: 55, potencia: 0.55, categoria: "Sumergibles para Pozos", aplicacion: "Riego desde pozo", serie: "SP4" },
    { modelo: "SP4-1012", caudal: 3.6, altura: 82, potencia: 0.75, categoria: "Sumergibles para Pozos", aplicacion: "Abastecimiento", serie: "SP4" },
    { modelo: "SP4-1016", caudal: 3.6, altura: 110, potencia: 1.1, categoria: "Sumergibles para Pozos", aplicacion: "Pozos muy profundos", serie: "SP4" },
    { modelo: "SP4-1512", caudal: 5.4, altura: 75, potencia: 1.1, categoria: "Sumergibles para Pozos", aplicacion: "Mayor caudal", serie: "SP4" },
    { modelo: "SP4-1516", caudal: 5.4, altura: 100, potencia: 1.5, categoria: "Sumergibles para Pozos", aplicacion: "Agricultura", serie: "SP4" },
    { modelo: "SP4-2012", caudal: 7.2, altura: 68, potencia: 1.5, categoria: "Sumergibles para Pozos", aplicacion: "Riego intensivo", serie: "SP4" },
    { modelo: "SP4-2016", caudal: 7.2, altura: 90, potencia: 2.2, categoria: "Sumergibles para Pozos", aplicacion: "Grandes explotaciones", serie: "SP4" },
    
    // SUMERGIBLES PARA POZOS 6"
    { modelo: "SP6-2510", caudal: 12, altura: 55, potencia: 2.2, categoria: "Sumergibles para Pozos", aplicacion: "Pozos 6\" caudal medio", serie: "SP6" },
    { modelo: "SP6-2515", caudal: 12, altura: 82, potencia: 3.0, categoria: "Sumergibles para Pozos", aplicacion: "Agricultura intensiva", serie: "SP6" },
    { modelo: "SP6-3010", caudal: 18, altura: 52, potencia: 3.0, categoria: "Sumergibles para Pozos", aplicacion: "Alto caudal", serie: "SP6" },
    { modelo: "SP6-3015", caudal: 18, altura: 78, potencia: 4.0, categoria: "Sumergibles para Pozos", aplicacion: "Riego extensivo", serie: "SP6" },
    { modelo: "SP6-4010", caudal: 24, altura: 48, potencia: 4.0, categoria: "Sumergibles para Pozos", aplicacion: "Gran caudal", serie: "SP6" },
    { modelo: "SP6-4015", caudal: 24, altura: 72, potencia: 5.5, categoria: "Sumergibles para Pozos", aplicacion: "Comunidades de regantes", serie: "SP6" },
    
    // SUMERGIBLES PARA ACHIQUE
    { modelo: "VORTEX-150", caudal: 10.8, altura: 7, potencia: 0.25, categoria: "Sumergibles para Achique", aplicacion: "Achique aguas sucias", serie: "VORTEX" },
    { modelo: "VORTEX-250", caudal: 15, altura: 8.5, potencia: 0.37, categoria: "Sumergibles para Achique", aplicacion: "Drenaje con sólidos", serie: "VORTEX" },
    { modelo: "VORTEX-450", caudal: 21, altura: 10, potencia: 0.55, categoria: "Sumergibles para Achique", aplicacion: "Achique potente", serie: "VORTEX" },
    { modelo: "DRAIN-100", caudal: 6.0, altura: 7, potencia: 0.25, categoria: "Sumergibles para Achique", aplicacion: "Aguas limpias", serie: "DRAIN" },
    { modelo: "DRAIN-200", caudal: 10.8, altura: 9, potencia: 0.37, categoria: "Sumergibles para Achique", aplicacion: "Vaciado piscinas", serie: "DRAIN" },
    { modelo: "DRAIN-400", caudal: 15, altura: 11, potencia: 0.55, categoria: "Sumergibles para Achique", aplicacion: "Sótanos, garajes", serie: "DRAIN" },
    { modelo: "FEKA-600", caudal: 18, altura: 9, potencia: 0.75, categoria: "Sumergibles para Achique", aplicacion: "Aguas fecales", serie: "FEKA" },
    { modelo: "FEKA-1000", caudal: 24, altura: 11, potencia: 1.1, categoria: "Sumergibles para Achique", aplicacion: "Estaciones de bombeo", serie: "FEKA" },
    
    // SISTEMAS SOLAR DE BOMBEO
    { modelo: "SOLAR-SP4-05", caudal: 1.5, altura: 50, potencia: 0.37, categoria: "Sistemas Solar", aplicacion: "Solar pozo 4\"", serie: "SOLAR" },
    { modelo: "SOLAR-SP4-10", caudal: 3.0, altura: 55, potencia: 0.55, categoria: "Sistemas Solar", aplicacion: "Riego solar", serie: "SOLAR" },
    { modelo: "SOLAR-SP4-15", caudal: 4.5, altura: 70, potencia: 0.75, categoria: "Sistemas Solar", aplicacion: "Agricultura sostenible", serie: "SOLAR" },
    { modelo: "SOLAR-SURF", caudal: 3.6, altura: 35, potencia: 0.55, categoria: "Sistemas Solar", aplicacion: "Superficie solar", serie: "SOLAR" },
    
    // EQUIPOS DE PRESIÓN
    { modelo: "GP-H50", caudal: 4.2, altura: 38, potencia: 0.55, categoria: "Equipos de Presión", aplicacion: "Grupo presión doméstico", serie: "GP" },
    { modelo: "GP-H60", caudal: 4.8, altura: 45, potencia: 0.75, categoria: "Equipos de Presión", aplicacion: "Vivienda unifamiliar", serie: "GP" },
    { modelo: "GP-H80", caudal: 6.0, altura: 52, potencia: 1.1, categoria: "Equipos de Presión", aplicacion: "Chalet grande", serie: "GP" },
    { modelo: "VARIBLOCH-1", caudal: 5.4, altura: 55, potencia: 1.1, categoria: "Equipos de Presión", aplicacion: "Variador integrado", serie: "VARIBLOCH" },
    { modelo: "VARIBLOCH-2", caudal: 7.2, altura: 65, potencia: 1.5, categoria: "Equipos de Presión", aplicacion: "Edificios pequeños", serie: "VARIBLOCH" },
    { modelo: "VARIBLOCH-3", caudal: 10.8, altura: 75, potencia: 2.2, categoria: "Equipos de Presión", aplicacion: "Comunidades", serie: "VARIBLOCH" },
    
    // EQUIPOS CONTRA INCENDIOS
    { modelo: "CI-12/50", caudal: 12, altura: 50, potencia: 4.0, categoria: "Equipos Contra Incendios", aplicacion: "BIE 25mm", serie: "CI" },
    { modelo: "CI-24/60", caudal: 24, altura: 60, potencia: 7.5, categoria: "Equipos Contra Incendios", aplicacion: "BIE 45mm", serie: "CI" },
    { modelo: "CI-48/70", caudal: 48, altura: 70, potencia: 15, categoria: "Equipos Contra Incendios", aplicacion: "Rociadores", serie: "CI" },
    { modelo: "CI-72/80", caudal: 72, altura: 80, potencia: 22, categoria: "Equipos Contra Incendios", aplicacion: "Hidrantes", serie: "CI" }
];

// Función para buscar bombas según criterios
function buscarBomba(caudalRequerido, alturaRequerida, tolerancia = 0.2) {
    // Validar que al menos un parámetro tiene valor
    if (caudalRequerido <= 0 && alturaRequerida <= 0) {
        return [];
    }
    const resultados = bombasBloch.filter(bomba => {
        const caudalMin = caudalRequerido * (1 - tolerancia);
        const caudalMax = caudalRequerido * (1 + tolerancia * 2);
        const alturaMin = alturaRequerida * (1 - tolerancia);
        const alturaMax = alturaRequerida * (1 + tolerancia * 2);
        
        return bomba.caudal >= caudalMin && 
               bomba.caudal <= caudalMax && 
               bomba.altura >= alturaMin && 
               bomba.altura <= alturaMax;
    });
    
    // Ordenar por eficiencia (menor potencia para cumplir requisitos)
    resultados.sort((a, b) => {
        const efA = (a.caudal * a.altura) / a.potencia;
        const efB = (b.caudal * b.altura) / b.potencia;
        return efB - efA;
    });
    
    return resultados;
}

// Función para búsqueda aproximada
function buscarBombaAproximada(caudalRequerido, alturaRequerida) {
    // Primero buscar con tolerancia normal
    let resultados = buscarBomba(caudalRequerido, alturaRequerida, 0.2);
    
    // Si no hay resultados, ampliar tolerancia
    if (resultados.length === 0) {
        resultados = buscarBomba(caudalRequerido, alturaRequerida, 0.4);
    }
    
    // Si aún no hay, buscar las más cercanas
    if (resultados.length === 0) {
        resultados = bombasBloch.map(bomba => {
            const distancia = Math.sqrt(
                Math.pow((bomba.caudal - caudalRequerido) / caudalRequerido, 2) +
                Math.pow((bomba.altura - alturaRequerida) / alturaRequerida, 2)
            );
            return { ...bomba, distancia };
        })
        .sort((a, b) => a.distancia - b.distancia)
        .slice(0, 5);
    }
    
    return resultados;
}

// Función para filtrar por categoría
function filtrarPorCategoria(categoria) {
    if (!categoria || categoria === 'Todas') {
        return bombasBloch;
    }
    return bombasBloch.filter(bomba => bomba.categoria === categoria);
}

// Función para filtrar por serie
function filtrarPorSerie(serie) {
    if (!serie || serie === 'Todas') {
        return bombasBloch;
    }
    return bombasBloch.filter(bomba => bomba.serie === serie);
}

// Obtener categorías únicas
function getCategorias() {
    return [...new Set(bombasBloch.map(b => b.categoria))];
}

// Obtener series únicas
function getSeries() {
    return [...new Set(bombasBloch.map(b => b.serie))];
}

// Exportar para uso
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { bombasBloch, buscarBomba, buscarBombaAproximada, filtrarPorCategoria, filtrarPorSerie, getCategorias, getSeries };
}
