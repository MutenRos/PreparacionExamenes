// BIPS v4.0 - Sistema Selector de Bombas Ideal
// Base de datos basada EXCLUSIVAMENTE en series reales de catalogos oficiales
// NO se recomiendan modelos especificos - solo series con rangos de operacion

// ============================================================
// BASE DE DATOS DE SERIES - Datos de catalogos oficiales Bombas Ideal
// ============================================================
// IMPORTANTE: Se recomienda la SERIE, el modelo exacto se determina
// consultando el catalogo o contactando con Bombas Ideal

const SERIES_DATABASE = [
    // ============================================
    // BOMBAS VERTICALES MULTICELULARES
    // ============================================
    
    // Serie NXA - Multicelulares Verticales Compactas AISI 304
    // Catalogo: Catalogo-NXA-Multicelulares.pdf
    // Datos reales: Caudal 0.3-20 m³/h, Altura hasta 100m, Potencia 0.37-7.5 kW
    { 
        id: 'NXA', 
        series: 'NXA', 
        name: 'Serie NXA', 
        type: 'Multicelular Vertical Compacta',
        description: 'Electrobombas verticales multicelulares de alta presión diseñadas para instalación "IN LINE". Acero inoxidable AISI 304.',
        flow: { min: 0.3, max: 20 }, 
        head: { min: 10, max: 100 }, 
        power: { min: 0.37, max: 7.5 },
        material: 'stainless', 
        maxTemp: 120, 
        rpm: 2900, 
        connection: 'DN25-DN50',
        efficiency: 65, 
        sectors: ['water', 'building', 'agriculture', 'fire'], 
        installation: 'surface', 
        phase: 'both', 
        solids: 0,
        catalog: 'Catalogo-NXA-Multicelulares.pdf',
        productPage: 'productos/serie-nxa.html',
        image: 'assets/images/serie-nxa-new.jpg'
    },

    // Serie VIPV - Multicelulares Verticales
    // Catalogo: Catalogo-VIPV-NX-NLX-NLV.pdf
    // Datos reales: Caudal 1-80 m³/h, Altura hasta 200m, Potencia hasta 37 kW
    { 
        id: 'VIPV', 
        series: 'VIPV', 
        name: 'Serie VIPV', 
        type: 'Multicelular Vertical',
        description: 'Bomba centrífuga multicelular especialmente indicada para grupos de presión. Funcionamiento silencioso.',
        flow: { min: 1, max: 80 }, 
        head: { min: 10, max: 200 }, 
        power: { min: 0.37, max: 37 },
        material: 'stainless', 
        maxTemp: 90, 
        rpm: 2900, 
        connection: 'DN40-DN100',
        efficiency: 72, 
        sectors: ['water', 'industrial', 'building'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-vipv.html',
        image: 'assets/images/serie-vipv-new.jpg'
    },

    // Serie VIPH - Multicelulares Horizontales
    // Datos reales: Caudal 1-120 m³/h, Altura hasta 250m, Potencia hasta 55 kW
    { 
        id: 'VIPH', 
        series: 'VIPH', 
        name: 'Serie VIPH', 
        type: 'Multicelular Horizontal',
        description: 'Bomba centrífuga multicelular horizontal de funcionamiento silencioso. Presión de servicio 11 bar máx.',
        flow: { min: 1, max: 120 }, 
        head: { min: 10, max: 250 }, 
        power: { min: 0.37, max: 55 },
        material: 'stainless', 
        maxTemp: 90, 
        rpm: 2900, 
        connection: 'DN40-DN100',
        efficiency: 72, 
        sectors: ['water', 'industrial', 'building'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-viph.html',
        image: 'assets/images/serie-viph-new.jpg'
    },

    // Serie NLX - Multicelulares In Line AISI 316
    // Datos reales: Caudal 0.5-70 m³/h, Altura hasta 220m
    { 
        id: 'NLX', 
        series: 'NLX', 
        name: 'Serie NLX', 
        type: 'Multicelular In Line AISI 316',
        description: 'Multicelulares verticales "In Line" en acero inoxidable AISI 316 para aguas limpias.',
        flow: { min: 0.5, max: 70 }, 
        head: { min: 10, max: 220 }, 
        power: { min: 0.55, max: 45 },
        material: 'stainless-316', 
        maxTemp: 90, 
        rpm: 2900, 
        connection: 'DN32-DN80',
        efficiency: 70, 
        sectors: ['water', 'industrial', 'building'], 
        installation: 'inline', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-nlx.html',
        image: 'assets/images/serie-nlx-new.jpg'
    },

    // Serie NLV - Multicelulares In Line
    // Datos reales: Caudal 1-50 m³/h, Altura hasta 180m
    { 
        id: 'NLV', 
        series: 'NLV', 
        name: 'Serie NLV', 
        type: 'Multicelular In Line',
        description: 'Multicelulares verticales "In Line" para instalaciones de presión y climatización.',
        flow: { min: 1, max: 50 }, 
        head: { min: 10, max: 180 }, 
        power: { min: 0.37, max: 37 },
        material: 'stainless', 
        maxTemp: 90, 
        rpm: 2900, 
        connection: 'DN32-DN80',
        efficiency: 70, 
        sectors: ['water', 'building'], 
        installation: 'inline', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf',
        productPage: 'productos/serie-nlv.html',
        image: 'assets/images/serie-nlv.jpg'
    },

    // Serie APM - Multicelulares Alta Presion
    // Datos reales: Caudal 1-120 m³/h, Altura hasta 250m, Potencia 0.37-45 kW
    { 
        id: 'APM', 
        series: 'APM', 
        name: 'Serie APM', 
        type: 'Multicelular Alta Presion',
        description: 'Bombas centrífugas multicelulares de alta presión. Motores IE3.',
        flow: { min: 1, max: 120 }, 
        head: { min: 20, max: 250 }, 
        power: { min: 0.37, max: 45 },
        material: 'cast-iron', 
        maxTemp: 80, 
        rpm: 2900, 
        connection: 'DN50-DN150',
        efficiency: 75, 
        sectors: ['water', 'industrial', 'fire'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-APM.pdf',
        productPage: 'productos/serie-apm.html',
        image: 'assets/images/serie-apm.jpg'
    },

    // ============================================
    // BOMBAS HORIZONTALES
    // ============================================

    // Serie CP - Camara Partida
    // Catalogo: Catalogo-CPH-Serie-CP.pdf
    { 
        id: 'CP', 
        series: 'CP', 
        name: 'Serie CP', 
        type: 'Centrifuga Camara Partida',
        description: 'Bombas centrifugas horizontales de camara partida. Grandes caudales.',
        flow: { min: 50, max: 10000 }, 
        head: { min: 10, max: 200 }, 
        power: { min: 7.5, max: 500 },
        material: 'cast-iron', 
        maxTemp: 100, 
        rpm: 1450, 
        connection: 'DN100-DN600',
        efficiency: 85, 
        sectors: ['water', 'industrial', 'fire'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-CPH-Serie-CP.pdf',
        productPage: 'productos/serie-cp.html',
        image: 'assets/images/serie-cp-new.jpg'
    },

    // Serie RN - Aspiracion Axial
    // Datos reales: Caudal 5-2500 m³/h, Altura hasta 160m, Potencia 0.37-315 kW
    { 
        id: 'RN', 
        series: 'RN', 
        name: 'Serie RN', 
        type: 'Centrifuga Aspiracion Axial',
        description: 'Bombas centrífugas horizontales de aspiración axial. Construcción robusta. Motores IE3.',
        flow: { min: 5, max: 2500 }, 
        head: { min: 5, max: 160 }, 
        power: { min: 0.37, max: 315 },
        material: 'cast-iron', 
        maxTemp: 90, 
        rpm: 1450, 
        connection: 'DN50-DN300',
        efficiency: 78, 
        sectors: ['water', 'industrial', 'agriculture'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-RN.pdf',
        productPage: 'productos/serie-rn.html',
        image: 'assets/images/serie-rn.jpg'
    },

    // Serie RNL - In Line
    // Datos reales: Caudal 5-1200 m³/h, Altura hasta 100m
    { 
        id: 'RNL', 
        series: 'RNL', 
        name: 'Serie RNL', 
        type: 'Centrifuga In Line',
        description: 'Bombas verticales con aspiración horizontal "In-Line". Instalación en tubería.',
        flow: { min: 5, max: 1200 }, 
        head: { min: 5, max: 100 }, 
        power: { min: 0.55, max: 160 },
        material: 'cast-iron', 
        maxTemp: 90, 
        rpm: 1450, 
        connection: 'DN50-DN300',
        efficiency: 78, 
        sectors: ['water', 'building'], 
        installation: 'inline', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-RNL.pdf',
        productPage: 'productos/serie-rnl.html',
        image: 'assets/images/serie-rnl.jpg'
    },

    // Serie RFXA - Monobloc Inox EN 733
    // Datos reales: Caudal hasta 400 m³/h, Altura hasta 90m
    { 
        id: 'RFXA', 
        series: 'RFXA', 
        name: 'Serie RFXA', 
        type: 'Monobloc Inox EN 733',
        description: 'Electrobomba monobloc inoxidable con bomba normalizada EN 733. Industria alimentaria.',
        flow: { min: 2, max: 400 }, 
        head: { min: 5, max: 90 }, 
        power: { min: 0.55, max: 45 },
        material: 'stainless', 
        maxTemp: 90, 
        rpm: 2900, 
        connection: 'DN32-DN150',
        efficiency: 72, 
        sectors: ['water', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-RFXA.pdf',
        productPage: 'productos/serie-rfxa.html',
        image: 'assets/images/serie-rfxa.jpg'
    },

    // ============================================
    // BOMBAS AUTOASPIRANTES
    // ============================================

    // Serie CEB - Autoaspirantes
    // Catalogo: Catalogo-CEB-Autoaspirantes.pdf
    // Datos reales: Caudal 5-400 m³/h, Altura 10-90m, Paso sólidos hasta 76mm
    { 
        id: 'CEB', 
        series: 'CEB', 
        name: 'Serie CEB', 
        type: 'Autoaspirante',
        description: 'Bombas centrífugas autoaspirantes para aguas residuales. Paso de sólidos hasta 76mm. Diseño anti-obstrucción.',
        flow: { min: 5, max: 400 }, 
        head: { min: 10, max: 90 }, 
        power: { min: 1.5, max: 75 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN50-DN200',
        efficiency: 55, 
        sectors: ['agriculture', 'drainage', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 76,
        catalog: 'Catalogo-CEB-Autoaspirantes.pdf',
        productPage: 'productos/serie-ceb.html',
        image: 'assets/images/serie-ceb-new.jpg'
    },

    // ============================================
    // BOMBAS SUMERGIDAS PARA POZOS
    // ============================================

    // Serie SD - Sumergidas 6" a 16"
    // Catalogo: Catalogo-SD-Sumergidas.pdf
    // Datos reales: Caudal 1-500 m³/h, Altura hasta 600m, Diámetros 4"-16"
    { 
        id: 'SD', 
        series: 'SD', 
        name: 'Serie SD', 
        type: 'Sumergida Pozos 4"-16"',
        description: 'Electrobombas centrífugas sumergidas multicelulares para pozos profundos. Diámetros 4", 6", 8", 10", 12", 14", 16".',
        flow: { min: 1, max: 500 }, 
        head: { min: 10, max: 600 }, 
        power: { min: 0.55, max: 350 },
        material: 'stainless', 
        maxTemp: 25, 
        rpm: 2900, 
        connection: 'DN80-DN300',
        efficiency: 78, 
        sectors: ['water', 'agriculture', 'industrial'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-SD-Sumergidas.pdf',
        productPage: 'productos/serie-sd.html',
        image: 'assets/images/serie-sd.jpg'
    },

    // Serie SDX - Sumergidas 4" a 16"
    // Datos reales: Caudal 1-300 m³/h, Altura hasta 500m
    { 
        id: 'SDX', 
        series: 'SDX', 
        name: 'Serie SDX', 
        type: 'Sumergida Pozos 4"-16"',
        description: 'Electrobombas sumergidas para pozos profundos. Acero inoxidable de alta resistencia.',
        flow: { min: 1, max: 300 }, 
        head: { min: 10, max: 500 }, 
        power: { min: 0.37, max: 220 },
        material: 'stainless', 
        maxTemp: 25, 
        rpm: 2900, 
        connection: 'DN50-DN250',
        efficiency: 75, 
        sectors: ['water', 'agriculture', 'industrial'], 
        installation: 'submerged', 
        phase: 'both', 
        solids: 0,
        catalog: 'Catalogo-SDX.pdf',
        productPage: 'productos/serie-sdx.html',
        image: 'assets/images/serie-sdx.jpg'
    },

    // Serie S - Sumergidas 4"
    // Datos reales: Caudal 1-400 m³/h, Altura hasta 600m
    { 
        id: 'S', 
        series: 'S', 
        name: 'Serie S', 
        type: 'Sumergida Pozos',
        description: 'Electrobombas sumergidas multicelulares para pozos profundos. Construcción modular.',
        flow: { min: 1, max: 400 }, 
        head: { min: 10, max: 600 }, 
        power: { min: 0.37, max: 220 },
        material: 'stainless', 
        maxTemp: 25, 
        rpm: 2900, 
        connection: 'DN40-DN65',
        efficiency: 68, 
        sectors: ['water', 'agriculture'], 
        installation: 'submerged', 
        phase: 'both', 
        solids: 0,
        catalog: 'Catalogo-S.pdf',
        productPage: 'productos/serie-s.html',
        image: 'assets/images/serie-s.jpg'
    },

    // Serie TRITON - Sumergidas 4" y 6"
    // Datos reales: Caudal 2-80 m³/h, Altura hasta 800m, Potencia hasta 150 kW
    { 
        id: 'TRITON', 
        series: 'TRITON', 
        name: 'Serie TRITON', 
        type: 'Sumergida 4" y 6"',
        description: 'Electrobombas sumergidas de 4" y 6" para grandes alturas manométricas. Ideal para captaciones profundas.',
        flow: { min: 2, max: 80 }, 
        head: { min: 20, max: 800 }, 
        power: { min: 0.55, max: 150 },
        material: 'stainless', 
        maxTemp: 30, 
        rpm: 2900, 
        connection: 'DN50-DN80',
        efficiency: 70, 
        sectors: ['water', 'agriculture'], 
        installation: 'submerged', 
        phase: 'both', 
        solids: 0,
        catalog: 'Catalogo-TRITON.pdf',
        productPage: 'productos/serie-triton.html',
        image: 'assets/images/serie-triton.jpg'
    },

    // Serie TXI/SXT - Sumergidas 4", 6", 8", 10"
    // Datos reales: Caudal 50-1500 m³/h, Altura hasta 400m
    { 
        id: 'TXI-SXT', 
        series: 'TXI-SXT', 
        name: 'Serie TXI/SXT', 
        type: 'Sumergida 8"-14"',
        description: 'Electrobombas sumergidas con impulsores radiales para grandes caudales. Diámetros 8", 10", 12" y 14".',
        flow: { min: 50, max: 1500 }, 
        head: { min: 10, max: 400 }, 
        power: { min: 5.5, max: 315 },
        material: 'stainless', 
        maxTemp: 30, 
        rpm: 2900, 
        connection: 'DN50-DN150',
        efficiency: 74, 
        sectors: ['water', 'agriculture', 'industrial'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-TXI-SXT.pdf',
        productPage: 'productos/serie-txi-sxt.html',
        image: 'assets/images/serie-txi-sxt.jpg'
    },

    // ============================================
    // BOMBAS RESIDUALES Y DRENAJE
    // ============================================

    // Serie ARS - Aguas Residuales Sumergibles
    // Catalogo: Catalogo-ARS-Residuales.pdf
    { 
        id: 'ARS', 
        series: 'ARS', 
        name: 'Serie ARS', 
        type: 'Residuales Sumergibles',
        description: 'Electrobombas sumergibles para aguas residuales. Rodetes Vortex, Monocanal, Multicanal, Trituradores. Paso solidos 6-105mm.',
        flow: { min: 5, max: 5000 }, 
        head: { min: 3, max: 80 }, 
        power: { min: 0.8, max: 100 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN40-DN300',
        efficiency: 65, 
        sectors: ['drainage', 'industrial'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 105,
        catalog: 'Catalogo-ARS-Residuales.pdf',
        productPage: 'productos/serie-ars.html',
        image: 'assets/images/serie-ars.jpg'
    },

    // Serie ARSA - Residuales Camara Seca
    // Datos reales: Caudal 5-400 m³/h, Altura hasta 50m, Potencia 1.5-75 kW
    { 
        id: 'ARSA', 
        series: 'ARSA', 
        name: 'Serie ARSA', 
        type: 'Residuales Cámara Seca',
        description: 'Bombas residuales para instalación en cámara seca. Eje prolongado para pozo.',
        flow: { min: 5, max: 400 }, 
        head: { min: 3, max: 50 }, 
        power: { min: 1.5, max: 75 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN50-DN250',
        efficiency: 68, 
        sectors: ['drainage', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 100,
        catalog: 'Catalogo-ARSA.pdf',
        productPage: 'productos/serie-arsa.html',
        image: 'assets/images/serie-arsa.jpg'
    },

    // Serie D - Drenaje/Aguas Sucias
    // Catalogo: Catalogo-D-Residuales.pdf
    // Datos reales: Caudal 5-80 m³/h, Altura hasta 25m, Potencia 0.25-5.5 kW
    { 
        id: 'D', 
        series: 'D', 
        name: 'Serie D', 
        type: 'Drenaje Aguas Sucias',
        description: 'Electrobombas sumergibles para elevación de aguas sucias. Diseño robusto para trabajos duros sin supervisión.',
        flow: { min: 5, max: 80 }, 
        head: { min: 3, max: 25 }, 
        power: { min: 0.25, max: 5.5 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN40-DN80',
        efficiency: 55, 
        sectors: ['drainage', 'building'], 
        installation: 'submerged', 
        phase: 'both', 
        solids: 50,
        catalog: 'Catalogo-D-Residuales.pdf',
        productPage: 'productos/serie-d.html',
        image: 'assets/images/serie-d.jpg'
    },

    // Serie BR - Recirculacion
    // Datos reales: Caudal 2-30 m³/h, Altura hasta 35m, Potencia 0.75-3 kW
    { 
        id: 'BR', 
        series: 'BR', 
        name: 'Serie BR', 
        type: 'Sumergible Recirculación',
        description: 'Bombas sumergibles de recirculación para depuradoras y piscifactorías.',
        flow: { min: 2, max: 30 }, 
        head: { min: 3, max: 35 }, 
        power: { min: 0.75, max: 3 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN100-DN300',
        efficiency: 60, 
        sectors: ['drainage', 'industrial'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 80,
        catalog: 'Catalogo-BR.pdf',
        productPage: 'productos/serie-br.html',
        image: 'assets/images/serie-br.jpg'
    },

    // Serie EBAR - Estacion Bombeo Prefabricada
    // Datos reales: Caudal 5-2000 m³/h, Altura hasta 80m
    { 
        id: 'EBAR', 
        series: 'EBAR', 
        name: 'Serie EBAR', 
        type: 'Estación Bombeo Prefabricada',
        description: 'Estaciones de bombeo prefabricadas para aguas residuales. Pozo de PRFV.',
        flow: { min: 5, max: 2000 }, 
        head: { min: 3, max: 80 }, 
        power: { min: 0.8, max: 132 },
        material: 'hdpe', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN50-DN200',
        efficiency: 65, 
        sectors: ['drainage', 'building'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 80,
        catalog: 'Catalogo-EBAR.pdf',
        productPage: 'productos/serie-ebar.html',
        image: 'assets/images/serie-ebar.jpg'
    },

    // ============================================
    // BOMBAS VERTICALES
    // ============================================

    // Serie VA/VHC - Verticales Helicoidales
    // Catalogo: Catalogo-VA-VHC-Verticales.pdf
    // Datos reales: Caudal 100-50000 m³/h, Altura 2-40m
    { 
        id: 'VA-VHC', 
        series: 'VA-VHC', 
        name: 'Serie VA/VHC', 
        type: 'Vertical Flujo Axial/Helicocentrífuga',
        description: 'Bombas verticales de flujo axial y helicocentrífugas para grandes caudales. Estaciones de bombeo y riego.',
        flow: { min: 100, max: 50000 }, 
        head: { min: 2, max: 40 }, 
        power: { min: 3, max: 500 },
        material: 'cast-iron', 
        maxTemp: 50, 
        rpm: 1450, 
        connection: 'DN100-DN500',
        efficiency: 80, 
        sectors: ['water', 'industrial', 'agriculture'], 
        installation: 'vertical', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VA-VHC-Verticales.pdf',
        productPage: 'productos/serie-va-vhc.html',
        image: 'assets/images/serie-va-vhc.jpg'
    },

    // Serie VHC
    // Datos reales: Caudal 100-10000 m³/h, Altura hasta 50m
    { 
        id: 'VHC', 
        series: 'VHC', 
        name: 'Serie VHC', 
        type: 'Vertical Helicocentrífuga',
        description: 'Bombas verticales helicocentrífugas para grandes caudales con alturas medias. Columna de fundición o acero.',
        flow: { min: 100, max: 10000 }, 
        head: { min: 5, max: 50 }, 
        power: { min: 7.5, max: 400 },
        material: 'cast-iron', 
        maxTemp: 50, 
        rpm: 1450, 
        connection: 'DN150-DN600',
        efficiency: 82, 
        sectors: ['water', 'industrial'], 
        installation: 'vertical', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VA-VHC-Verticales.pdf',
        productPage: 'productos/serie-vhc.html',
        image: 'assets/images/serie-vhc.jpg'
    },

    // Serie VS/VG
    // Catalogo: Catalogo-VS-VG.pdf
    // Datos reales: Caudal 10-2000 m³/h, Altura hasta 200m
    { 
        id: 'VS-VG', 
        series: 'VS-VG', 
        name: 'Serie VS/VG', 
        type: 'Vertical Multicelular',
        description: 'Bombas verticales centrífugas multicelulares para grandes alturas. Abastecimiento municipal y riego.',
        flow: { min: 10, max: 2000 }, 
        head: { min: 10, max: 200 }, 
        power: { min: 2.2, max: 315 },
        material: 'cast-iron', 
        maxTemp: 50, 
        rpm: 1450, 
        connection: 'DN80-DN400',
        efficiency: 78, 
        sectors: ['water', 'industrial'], 
        installation: 'vertical', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-VS-VG.pdf',
        productPage: 'productos/serie-vs-vg.html',
        image: 'assets/images/verticales-va-vgh.jpg'
    },

    // ============================================
    // BOMBAS CONTRAINCENDIOS
    // ============================================

    // Serie FOC UNE 23500
    // Catalogo: Catalogo-FOC-Contraincendios.pdf
    // Datos reales: Caudal 6-500 m³/h, Altura hasta 150m
    { 
        id: 'FOC-UNE', 
        series: 'FOC-UNE', 
        name: 'Grupos FOC UNE 23500', 
        type: 'Contraincendios UNE 23500',
        description: 'Grupos de presión contraincendios según norma UNE 23500. Bomba eléctrica + bomba jockey + depósito.',
        flow: { min: 6, max: 500 }, 
        head: { min: 15, max: 150 }, 
        power: { min: 2.2, max: 160 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN50-DN200',
        efficiency: 75, 
        sectors: ['fire'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-FOC-Contraincendios.pdf',
        productPage: 'productos/serie-une23500.html',
        image: 'assets/images/serie-une23500.jpg'
    },

    // Serie FOC NFPA 20
    { 
        id: 'FOC-NFPA', 
        series: 'FOC-NFPA', 
        name: 'Grupos FOC NFPA 20', 
        type: 'Contraincendios NFPA 20',
        description: 'Grupos de presion contraincendios segun norma NFPA 20 (UL/FM).',
        flow: { min: 20, max: 800 }, 
        head: { min: 30, max: 200 }, 
        power: { min: 7.5, max: 250 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1750, 
        connection: 'DN80-DN300',
        efficiency: 80, 
        sectors: ['fire'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-FOC-Contraincendios.pdf',
        productPage: 'productos/serie-nfpa20.html',
        image: 'assets/images/serie-nfpa20.jpg'
    },

    // Serie RT1-ROC Contraincendios
    // Datos reales: Caudal 12-500 m³/h, Altura hasta 150m
    { 
        id: 'RT1-ROC', 
        series: 'RT1-ROC', 
        name: 'Serie RT1-ROC', 
        type: 'Contraincendios Normalizada',
        description: 'Bombas contraincendios normalizadas EN 12845. Cuerpo de aspiración con entrada de rociadores.',
        flow: { min: 12, max: 500 }, 
        head: { min: 15, max: 150 }, 
        power: { min: 3, max: 132 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN65-DN200',
        efficiency: 76, 
        sectors: ['fire'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-RT1-ROC.pdf',
        productPage: 'productos/serie-rt1-roc.html',
        image: 'assets/images/serie-rt1-roc.jpg'
    },

    // Serie RT2-ABA Contraincendios
    // Datos reales: Caudal 12-1000 m³/h, Altura hasta 180m
    { 
        id: 'RT2-ABA', 
        series: 'RT2-ABA', 
        name: 'Serie RT2-ABA', 
        type: 'Contraincendios Abastecimiento',
        description: 'Bombas contraincendios para abastecimiento. Cuerpo espiral con bridas normalizadas.',
        flow: { min: 12, max: 1000 }, 
        head: { min: 10, max: 180 }, 
        power: { min: 5.5, max: 200 },
        material: 'cast-iron', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'DN80-DN250',
        efficiency: 78, 
        sectors: ['fire', 'water'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-RT2-ABA.pdf',
        productPage: 'productos/serie-rt2-aba.html',
        image: 'assets/images/serie-rt2-aba.jpg'
    },

    // ============================================
    // BOMBEO SOLAR
    // ============================================

    // Serie SBS - Bombeo Solar
    // Catalogo: Catalogo-SBS-Bombeo-Solar.pdf
    // Datos reales: Caudal 0.5-200 m³/día (convertido a m³/h), Profundidad hasta 350m
    { 
        id: 'SBS', 
        series: 'SBS', 
        name: 'Serie SBS', 
        type: 'Bombeo Solar',
        description: 'Sistema de bombeo solar para extracción de agua con energía fotovoltaica. Sin consumo eléctrico de red.',
        flow: { min: 0.02, max: 8.3 }, 
        head: { min: 10, max: 350 }, 
        power: { min: 0.15, max: 22 },
        material: 'stainless', 
        maxTemp: 30, 
        rpm: 0, 
        connection: 'DN40-DN100',
        efficiency: 70, 
        sectors: ['agriculture', 'water'], 
        installation: 'submerged', 
        phase: 'solar', 
        solids: 0,
        catalog: 'Catalogo-SBS-Bombeo-Solar.pdf',
        productPage: 'productos/serie-sbs.html',
        image: 'assets/images/serie-sbs.jpg'
    },

    // ============================================
    // AGITADORES Y AIREADORES
    // ============================================

    // Serie AGS - Agitadores Sumergidos
    // Datos reales: Caudal 10-200 m³/h, Altura hasta 40m, Potencia 2.2-30 kW
    { 
        id: 'AGS', 
        series: 'AGS', 
        name: 'Serie AGS', 
        type: 'Agitador Sumergido',
        description: 'Agitadores sumergidos para tratamiento de aguas y homogeneización. Hélice de alto rendimiento.',
        flow: { min: 10, max: 200 }, 
        head: { min: 3, max: 40 }, 
        power: { min: 2.2, max: 30 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'Propeller',
        efficiency: 70, 
        sectors: ['drainage', 'industrial'], 
        installation: 'submerged', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-AGS.pdf',
        productPage: 'productos/serie-ags.html',
        image: 'assets/images/serie-ags.jpg'
    },

    // Serie AR - Achique Industrial
    // Datos reales: Caudal 20-500 m³/h, Altura hasta 60m, Potencia 2.2-90 kW
    { 
        id: 'AR', 
        series: 'AR', 
        name: 'Serie AR/AJS', 
        type: 'Achique Industrial',
        description: 'Bombas sumergibles de achique para uso industrial. Portátiles de gran potencia para obras, minas y emergencias.',
        flow: { min: 20, max: 500 }, 
        head: { min: 5, max: 60 }, 
        power: { min: 2.2, max: 90 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 1450, 
        connection: 'Flotante',
        efficiency: 65, 
        sectors: ['drainage', 'industrial'], 
        installation: 'floating', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-AR.pdf',
        productPage: 'productos/serie-ar-ajs.html',
        image: 'assets/images/serie-ar.jpg'
    },

    // ============================================
    // GRUPOS HYDRO
    // ============================================

    // Serie HYDRO Domesticos
    { 
        id: 'HYDRO-DOM', 
        series: 'HYDRO-DOM', 
        name: 'Grupos HYDRO Domesticos', 
        type: 'Grupo Presion Domestico',
        description: 'Grupos de presion para viviendas y pequenas instalaciones.',
        flow: { min: 0.5, max: 8 }, 
        head: { min: 20, max: 60 }, 
        power: { min: 0.37, max: 1.5 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN25-DN32',
        efficiency: 60, 
        sectors: ['building', 'water'], 
        installation: 'surface', 
        phase: 'single', 
        solids: 0,
        catalog: 'Catalogo-Hydro.pdf',
        productPage: 'productos/grupos-domesticos.html',
        image: 'assets/images/hydro-domesticos.jpg'
    },

    // Serie HYDRO NXA
    { 
        id: 'HYDRO-NXA', 
        series: 'HYDRO-NXA', 
        name: 'Grupos HYDRO NXA', 
        type: 'Grupo Presion Multicelular',
        description: 'Grupos de presion con bombas multicelulares NXA.',
        flow: { min: 2, max: 40 }, 
        head: { min: 30, max: 120 }, 
        power: { min: 0.75, max: 15 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN40-DN80',
        efficiency: 68, 
        sectors: ['building', 'water', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-Hydro-NXA.pdf',
        productPage: 'productos/hydro-nxa.html',
        image: 'assets/images/hydro-nxa-new.jpg'
    },

    // Serie HYDRO V/H
    { 
        id: 'HYDRO-VH', 
        series: 'HYDRO-VH', 
        name: 'Grupos HYDRO V/H', 
        type: 'Grupo Presion Industrial',
        description: 'Grupos de presion con bombas verticales u horizontales.',
        flow: { min: 5, max: 200 }, 
        head: { min: 25, max: 180 }, 
        power: { min: 2.2, max: 90 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN50-DN150',
        efficiency: 72, 
        sectors: ['building', 'water', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-Hydro-VH.pdf',
        productPage: 'productos/hydro-v.html',
        image: 'assets/images/hydro-v-new.jpg'
    },

    // Serie HYDRO VIPH
    { 
        id: 'HYDRO-VIPH', 
        series: 'HYDRO-VIPH', 
        name: 'Grupos HYDRO VIPH', 
        type: 'Grupo Presion Alta Capacidad',
        description: 'Grupos de presion con bombas multicelulares horizontales de alta capacidad.',
        flow: { min: 10, max: 300 }, 
        head: { min: 30, max: 250 }, 
        power: { min: 4, max: 150 },
        material: 'stainless', 
        maxTemp: 40, 
        rpm: 2900, 
        connection: 'DN65-DN150',
        efficiency: 75, 
        sectors: ['building', 'water', 'industrial'], 
        installation: 'surface', 
        phase: 'three', 
        solids: 0,
        catalog: 'Catalogo-Hydro-VIPH.pdf',
        productPage: 'productos/hydro-viph.html',
        image: 'assets/images/hydro-viph.jpg'
    },
];

// Alias para compatibilidad con codigo existente
const PUMPS_DATABASE = SERIES_DATABASE;

// Info de las series para UI
const SERIES_INFO = {
    'NXA': { name: 'Multicelulares Compactas', icon: 'fa-layer-group', catalog: 'Catalogo-NXA-Multicelulares.pdf', color: '#0066cc' },
    'VIPV': { name: 'Multicelulares Verticales', icon: 'fa-arrows-alt-v', catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf', color: '#0077dd' },
    'VIPH': { name: 'Multicelulares Horizontales', icon: 'fa-arrows-alt-h', catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf', color: '#0088ee' },
    'NLX': { name: 'In Line AISI 316', icon: 'fa-compress-arrows-alt', catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf', color: '#0099ff' },
    'NLV': { name: 'In Line', icon: 'fa-compress-arrows-alt', catalog: 'Catalogo-VIPV-NX-NLX-NLV.pdf', color: '#00aaff' },
    'APM': { name: 'Alta Presion', icon: 'fa-tachometer-alt', catalog: 'Catalogo-APM.pdf', color: '#1155cc' },
    'CP': { name: 'Camara Partida', icon: 'fa-cogs', catalog: 'Catalogo-CPH-Serie-CP.pdf', color: '#2266dd' },
    'RN': { name: 'Aspiracion Axial', icon: 'fa-arrow-right', catalog: 'Catalogo-RN.pdf', color: '#3377ee' },
    'RNL': { name: 'In Line RN', icon: 'fa-exchange-alt', catalog: 'Catalogo-RNL.pdf', color: '#4488ff' },
    'RFXA': { name: 'Monobloc Inox', icon: 'fa-cube', catalog: 'Catalogo-RFXA.pdf', color: '#5599ff' },
    'CEB': { name: 'Autoaspirantes', icon: 'fa-sync-alt', catalog: 'Catalogo-CEB-Autoaspirantes.pdf', color: '#22aa44' },
    'SD': { name: 'Sumergidas Pozos', icon: 'fa-arrow-down', catalog: 'Catalogo-SD-Sumergidas.pdf', color: '#00aa88' },
    'SDX': { name: 'Sumergidas SDX', icon: 'fa-arrow-circle-down', catalog: 'Catalogo-SDX.pdf', color: '#00bb99' },
    'S': { name: 'Sumergidas 4"', icon: 'fa-arrow-alt-circle-down', catalog: 'Catalogo-S.pdf', color: '#00ccaa' },
    'TRITON': { name: 'Sumergidas Triton', icon: 'fa-water', catalog: 'Catalogo-TRITON.pdf', color: '#00ddbb' },
    'TXI-SXT': { name: 'Sumergidas TXI/SXT', icon: 'fa-level-down-alt', catalog: 'Catalogo-TXI-SXT.pdf', color: '#00eecc' },
    'ARS': { name: 'Residuales', icon: 'fa-recycle', catalog: 'Catalogo-ARS-Residuales.pdf', color: '#886622' },
    'ARSA': { name: 'Residuales Camara Seca', icon: 'fa-industry', catalog: 'Catalogo-ARSA.pdf', color: '#997733' },
    'D': { name: 'Drenaje', icon: 'fa-tint', catalog: 'Catalogo-D-Residuales.pdf', color: '#aa8844' },
    'BR': { name: 'Recirculacion', icon: 'fa-redo', catalog: 'Catalogo-BR.pdf', color: '#bb9955' },
    'EBAR': { name: 'Estacion Bombeo', icon: 'fa-building', catalog: 'Catalogo-EBAR.pdf', color: '#ccaa66' },
    'VA-VHC': { name: 'Verticales Turbina', icon: 'fa-sort-amount-up', catalog: 'Catalogo-VA-VHC-Verticales.pdf', color: '#6644aa' },
    'VHC': { name: 'Verticales Columna', icon: 'fa-align-center', catalog: 'Catalogo-VA-VHC-Verticales.pdf', color: '#7755bb' },
    'VS-VG': { name: 'Verticales Sumergidas', icon: 'fa-chevron-circle-down', catalog: 'Catalogo-VS-VG.pdf', color: '#8866cc' },
    'FOC-UNE': { name: 'Contraincendios UNE', icon: 'fa-fire-extinguisher', catalog: 'Catalogo-FOC-Contraincendios.pdf', color: '#cc2222' },
    'FOC-NFPA': { name: 'Contraincendios NFPA', icon: 'fa-fire-alt', catalog: 'Catalogo-FOC-Contraincendios.pdf', color: '#dd3333' },
    'RT1-ROC': { name: 'Contraincendios RT1', icon: 'fa-burn', catalog: 'Catalogo-RT1-ROC.pdf', color: '#ee4444' },
    'RT2-ABA': { name: 'Contraincendios RT2', icon: 'fa-fire', catalog: 'Catalogo-RT2-ABA.pdf', color: '#ff5555' },
    'SBS': { name: 'Bombeo Solar', icon: 'fa-sun', catalog: 'Catalogo-SBS-Bombeo-Solar.pdf', color: '#ffaa00' },
    'AGS': { name: 'Agitadores', icon: 'fa-fan', catalog: 'Catalogo-AGS.pdf', color: '#44aacc' },
    'AR': { name: 'Aireadores', icon: 'fa-wind', catalog: 'Catalogo-AR.pdf', color: '#55bbdd' },
    'HYDRO-DOM': { name: 'Hydro Domestico', icon: 'fa-home', catalog: 'Catalogo-Hydro.pdf', color: '#6688ff' },
    'HYDRO-NXA': { name: 'Hydro NXA', icon: 'fa-tachometer-alt', catalog: 'Catalogo-Hydro-NXA.pdf', color: '#7799ff' },
    'HYDRO-VH': { name: 'Hydro Industrial', icon: 'fa-industry', catalog: 'Catalogo-Hydro-VH.pdf', color: '#88aaff' },
    'HYDRO-VIPH': { name: 'Hydro Alta Capacidad', icon: 'fa-rocket', catalog: 'Catalogo-Hydro-VIPH.pdf', color: '#99bbff' }
};

// ============================================================
// ESTADO GLOBAL
// ============================================================
let searchHistory = JSON.parse(localStorage.getItem('bipsHistory') || '[]');
let compareList = JSON.parse(localStorage.getItem('bipsCompare') || '[]');
let currentResults = [];

// ============================================================
// INICIALIZACION
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('BIPS v4.0 - Inicializando...');
    
    // Actualizar contadores
    const totalEl = document.getElementById('total-pumps-count');
    if (totalEl) totalEl.textContent = SERIES_DATABASE.length;
    
    // Inicializar tema
    initTheme();
    
    // Vincular eventos
    bindEvents();
    
    // Inicializar sliders
    initSliders();
    
    // Actualizar historial
    updateHistoryBadge();
    
    // Mostrar campos condicionales
    updateConditionalFields();
    
    // Actualizar tabla de comparacion si hay items
    if (compareList.length > 0) {
        updateComparisonUI();
    }
    
    console.log('BIPS v4.0 - ' + SERIES_DATABASE.length + ' series de bombas cargadas (datos de catálogos oficiales)');
});

// ============================================================
// TEMA OSCURO/CLARO
// ============================================================
function initTheme() {
    const saved = localStorage.getItem('bips-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('bips-theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.innerHTML = theme === 'dark' 
            ? '<i class="fas fa-sun"></i>' 
            : '<i class="fas fa-moon"></i>';
    }
}

// ============================================================
// VINCULACION DE EVENTOS
// ============================================================
function bindEvents() {
    // Tema
    document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);
    
    // Historial
    document.getElementById('history-btn')?.addEventListener('click', toggleHistory);
    document.getElementById('sidebar-close')?.addEventListener('click', toggleHistory);
    document.getElementById('sidebar-overlay')?.addEventListener('click', toggleHistory);
    document.getElementById('clear-history')?.addEventListener('click', clearHistory);
    
    // Formulario
    const form = document.getElementById('pump-selector-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }
    
    document.getElementById('reset-btn')?.addEventListener('click', resetForm);
    
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            switchTab(tabId);
        });
    });
    
    // Presets
    document.querySelectorAll('.btn-preset').forEach(btn => {
        btn.addEventListener('click', function() {
            applyPreset(this.dataset.preset);
        });
    });
    
    // Calculadora
    ['calc-flow', 'calc-head', 'calc-density'].forEach(id => {
        document.getElementById(id)?.addEventListener('input', calculatePower);
    });
    
    // Comparacion
    document.getElementById('clear-comparison')?.addEventListener('click', clearComparison);
    document.getElementById('quote-selected')?.addEventListener('click', quoteSelected);
    
    // Export
    document.getElementById('export-pdf')?.addEventListener('click', exportToPDF);
    document.getElementById('export-excel')?.addEventListener('click', exportToExcel);
    document.getElementById('btn-print')?.addEventListener('click', () => window.print());
    
    // Modales
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) closeModal(modal.id);
        });
    });
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) closeModal(modal.id);
        });
    });
    
    // Quote form
    const quoteForm = document.getElementById('quote-form');
    if (quoteForm) {
        quoteForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitQuote();
        });
    }
    
    // Instalacion (mostrar campos de pozo)
    document.querySelectorAll('input[name="installation"]').forEach(radio => {
        radio.addEventListener('change', updateConditionalFields);
    });
}

// ============================================================
// SLIDERS
// ============================================================
function initSliders() {
    // Slider de solidos
    const solidSlider = document.getElementById('solid-size');
    const solidDisplay = document.getElementById('solid-display');
    if (solidSlider && solidDisplay) {
        solidSlider.addEventListener('input', function() {
            solidDisplay.textContent = this.value + ' mm';
        });
    }
    
    // Slider de eficiencia
    const effSlider = document.getElementById('min-efficiency');
    const effDisplay = document.getElementById('efficiency-value');
    if (effSlider && effDisplay) {
        effSlider.addEventListener('input', function() {
            effDisplay.textContent = this.value + '%';
        });
    }
}

// ============================================================
// TABS
// ============================================================
function switchTab(tabId) {
    // Desactivar todos los tabs y contenidos
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    // Activar el seleccionado
    document.querySelector('.tab[data-tab="' + tabId + '"]')?.classList.add('active');
    document.getElementById('tab-' + tabId)?.classList.add('active');
}

// ============================================================
// CAMPOS CONDICIONALES
// ============================================================
function updateConditionalFields() {
    const installation = document.querySelector('input[name="installation"]:checked')?.value;
    const wellFields = document.getElementById('well-data-fields');
    
    if (wellFields) {
        wellFields.style.display = installation === 'submerged' ? 'block' : 'none';
    }
}

// ============================================================
// HISTORIAL
// ============================================================
function toggleHistory() {
    const sidebar = document.getElementById('history-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        
        if (sidebar.classList.contains('active')) {
            renderHistory();
        }
    }
}

function renderHistory() {
    const container = document.getElementById('history-list');
    if (!container) return;
    
    if (searchHistory.length === 0) {
        container.innerHTML = '<p class="empty-message">No hay busquedas recientes</p>';
        return;
    }
    
    container.innerHTML = searchHistory.map(function(item, index) {
        return '<div class="history-item" onclick="loadFromHistory(' + index + ')">' +
            '<div class="history-item-header">' +
                '<i class="fas fa-search"></i>' +
                '<span>' + (getSectorName(item.sector) || 'General') + '</span>' +
            '</div>' +
            '<div class="history-item-details">' +
                (item.flow ? '<span>Q: ' + item.flow + ' m3/h</span>' : '') +
                (item.head ? '<span>H: ' + item.head + ' m</span>' : '') +
            '</div>' +
            '<small class="history-item-date">' + item.date + '</small>' +
        '</div>';
    }).join('');
}

function loadFromHistory(index) {
    const item = searchHistory[index];
    if (!item) return;
    
    // Restaurar valores del formulario
    if (item.sector) {
        const radio = document.querySelector('input[name="sector"][value="' + item.sector + '"]');
        if (radio) radio.checked = true;
    }
    if (item.flow) {
        const flowInput = document.getElementById('flow-value');
        if (flowInput) flowInput.value = item.flow;
    }
    if (item.head) {
        const headInput = document.getElementById('head-value');
        if (headInput) headInput.value = item.head;
    }
    
    toggleHistory();
    performSearch();
}

function addToHistory(params) {
    var now = new Date();
    var entry = Object.assign({}, params, {
        date: now.toLocaleDateString('es-ES') + ' ' + now.toLocaleTimeString('es-ES', {hour: '2-digit', minute: '2-digit'})
    });
    
    searchHistory.unshift(entry);
    if (searchHistory.length > 10) searchHistory.pop();
    
    localStorage.setItem('bipsHistory', JSON.stringify(searchHistory));
    updateHistoryBadge();
}

function clearHistory() {
    searchHistory = [];
    localStorage.setItem('bipsHistory', '[]');
    updateHistoryBadge();
    renderHistory();
    showToast('Historial borrado', 'success');
}

function updateHistoryBadge() {
    const badge = document.getElementById('history-count');
    if (badge) {
        badge.textContent = searchHistory.length;
        badge.style.display = searchHistory.length > 0 ? 'flex' : 'none';
    }
}

// ============================================================
// BUSQUEDA
// ============================================================
function performSearch() {
    const params = getFormParams();
    
    // Validar que hay al menos un parametro
    if (!params.flow && !params.head && !params.sector) {
        showToast('Indica caudal, altura o sector', 'warning');
        return;
    }
    
    // Guardar en historial
    addToHistory(params);
    
    // Mostrar loading
    const resultsContent = document.getElementById('results-content');
    if (resultsContent) {
        resultsContent.innerHTML = '<div class="loading"><div class="spinner"></div><p>Buscando bombas...</p></div>';
    }
    
    // Buscar con delay para UX
    setTimeout(function() {
        var searchResult = searchPumpsWithFallback(params);
        currentResults = searchResult.results;
        renderResults(searchResult.results, searchResult.isApproximate, params);
        updateResultsCount(searchResult.results.length);
    }, 400);
}

function getFormParams() {
    const params = {};
    
    // Sector
    const sector = document.querySelector('input[name="sector"]:checked');
    if (sector) params.sector = sector.value;
    
    // Prioridad
    const priority = document.querySelector('input[name="priority"]:checked');
    if (priority) params.priority = priority.value;
    
    // Liquido
    const liquid = document.getElementById('liquid-type');
    if (liquid && liquid.value) params.liquid = liquid.value;
    
    // Temperatura
    const temp = document.getElementById('liquid-temp');
    if (temp && temp.value) params.temperature = parseFloat(temp.value);
    
    // Solidos
    const solids = document.getElementById('solid-size');
    if (solids && parseInt(solids.value) > 0) params.solids = parseInt(solids.value);
    
    // Caudal
    const flowValue = document.getElementById('flow-value');
    const flowUnit = document.getElementById('flow-unit');
    if (flowValue && flowValue.value) {
        var flow = parseFloat(flowValue.value);
        // Convertir a m3/h
        if (flowUnit) {
            if (flowUnit.value === 'ls') flow = flow * 3.6;
            else if (flowUnit.value === 'lmin') flow = flow * 0.06;
        }
        params.flow = flow;
    }
    
    // Altura
    const headValue = document.getElementById('head-value');
    const headUnit = document.getElementById('head-unit');
    if (headValue && headValue.value) {
        var head = parseFloat(headValue.value);
        // Convertir a metros
        if (headUnit) {
            if (headUnit.value === 'bar') head = head * 10.2;
            else if (headUnit.value === 'psi') head = head * 0.703;
        }
        params.head = head;
    }
    
    // Instalacion
    const installation = document.querySelector('input[name="installation"]:checked');
    if (installation && installation.value !== 'any') params.installation = installation.value;
    
    // Energia
    const power = document.querySelector('input[name="power"]:checked');
    if (power && power.value !== 'any') params.phase = power.value;
    
    // Conexion
    const connection = document.getElementById('connection-size');
    if (connection && connection.value) params.connection = connection.value;
    
    // Avanzado: Material
    const material = document.getElementById('material');
    if (material && material.value) params.material = material.value;
    
    // Avanzado: Eficiencia
    const efficiency = document.getElementById('min-efficiency');
    if (efficiency && parseInt(efficiency.value) > 0) params.minEfficiency = parseInt(efficiency.value);
    
    // Avanzado: RPM
    const rpm = document.getElementById('rpm');
    if (rpm && rpm.value) params.rpm = parseInt(rpm.value);
    
    return params;
}

// Busqueda con fallback a resultados aproximados
function searchPumpsWithFallback(params) {
    // Primero busqueda estricta
    var exactResults = searchPumps(params, false);
    
    if (exactResults.length > 0) {
        return { results: exactResults, isApproximate: false };
    }
    
    // Si no hay resultados exactos, buscar aproximados
    var approximateResults = searchPumpsApproximate(params);
    
    return { results: approximateResults, isApproximate: true };
}

// Busqueda aproximada - encuentra los mas cercanos
function searchPumpsApproximate(params) {
    var results = PUMPS_DATABASE.slice();
    
    // Calcular distancia/similitud para cada bomba
    results = results.map(function(pump) {
        var similarity = 100;
        var reasons = [];
        
        // Penalizar por sector diferente
        if (params.sector && pump.sectors.indexOf(params.sector) < 0) {
            similarity -= 15;
            reasons.push('sector diferente');
        }
        
        // Calcular distancia de caudal
        if (params.flow) {
            var flowMid = (pump.flow.min + pump.flow.max) / 2;
            var flowRange = pump.flow.max - pump.flow.min;
            var flowDistance = Math.abs(params.flow - flowMid);
            
            if (params.flow >= pump.flow.min && params.flow <= pump.flow.max) {
                // Dentro del rango - perfecto
            } else if (params.flow < pump.flow.min) {
                var deficit = pump.flow.min - params.flow;
                var penaltyPercent = Math.min(50, (deficit / pump.flow.min) * 100);
                similarity -= penaltyPercent;
                reasons.push('caudal menor al minimo');
            } else {
                var excess = params.flow - pump.flow.max;
                var penaltyPercent = Math.min(50, (excess / pump.flow.max) * 100);
                similarity -= penaltyPercent;
                reasons.push('caudal mayor al maximo');
            }
        }
        
        // Calcular distancia de altura
        if (params.head) {
            if (params.head >= pump.head.min && params.head <= pump.head.max) {
                // Dentro del rango - perfecto
            } else if (params.head < pump.head.min) {
                var deficit = pump.head.min - params.head;
                var penaltyPercent = Math.min(50, (deficit / pump.head.min) * 100);
                similarity -= penaltyPercent;
                reasons.push('altura menor a la minima');
            } else {
                var excess = params.head - pump.head.max;
                var penaltyPercent = Math.min(50, (excess / pump.head.max) * 100);
                similarity -= penaltyPercent;
                reasons.push('altura mayor a la maxima');
            }
        }
        
        // Penalizar por instalacion diferente
        if (params.installation && pump.installation !== params.installation) {
            similarity -= 10;
            reasons.push('tipo instalacion diferente');
        }
        
        // Penalizar por fase diferente
        if (params.phase && pump.phase !== params.phase) {
            similarity -= 10;
            reasons.push('alimentacion diferente');
        }
        
        // Penalizar por temperatura
        if (params.temperature && pump.maxTemp < params.temperature) {
            similarity -= 15;
            reasons.push('temperatura maxima insuficiente');
        }
        
        // Penalizar por solidos
        if (params.solids && pump.solids < params.solids) {
            similarity -= 20;
            reasons.push('paso de solidos insuficiente');
        }
        
        return Object.assign({}, pump, { 
            score: Math.max(0, Math.round(similarity)),
            approximateReasons: reasons
        });
    });
    
    // Ordenar por similitud y tomar los 8 mejores
    results.sort(function(a, b) { return b.score - a.score; });
    
    return results.slice(0, 8);
}

function searchPumps(params) {
    var results = PUMPS_DATABASE.slice();
    
    // Filtrar por sector
    if (params.sector) {
        results = results.filter(function(p) { return p.sectors.indexOf(params.sector) >= 0; });
    }
    
    // Filtrar por caudal (con margen del 30%)
    if (params.flow) {
        results = results.filter(function(p) { 
            return params.flow >= p.flow.min * 0.7 && params.flow <= p.flow.max * 1.3;
        });
    }
    
    // Filtrar por altura (con margen del 30%)
    if (params.head) {
        results = results.filter(function(p) { 
            return params.head >= p.head.min * 0.7 && params.head <= p.head.max * 1.3;
        });
    }
    
    // Filtrar por instalacion
    if (params.installation) {
        results = results.filter(function(p) { return p.installation === params.installation; });
    }
    
    // Filtrar por fase electrica
    if (params.phase) {
        results = results.filter(function(p) { return p.phase === params.phase; });
    }
    
    // Filtrar por temperatura
    if (params.temperature) {
        results = results.filter(function(p) { return p.maxTemp >= params.temperature; });
    }
    
    // Filtrar por solidos
    if (params.solids) {
        results = results.filter(function(p) { return p.solids >= params.solids; });
    }
    
    // Filtrar por material
    if (params.material) {
        results = results.filter(function(p) { return p.material === params.material; });
    }
    
    // Filtrar por eficiencia minima
    if (params.minEfficiency) {
        results = results.filter(function(p) { return p.efficiency >= params.minEfficiency; });
    }
    
    // Filtrar por RPM
    if (params.rpm) {
        results = results.filter(function(p) { return p.rpm === params.rpm; });
    }
    
    // Filtrar por conexion
    if (params.connection) {
        results = results.filter(function(p) { return p.connection === params.connection; });
    }
    
    // Calcular puntuacion
    results = results.map(function(pump) {
        var score = 50;
        
        // Bonus por caudal en rango
        if (params.flow) {
            if (params.flow >= pump.flow.min && params.flow <= pump.flow.max) {
                score += 20;
                var mid = (pump.flow.min + pump.flow.max) / 2;
                var distance = Math.abs(params.flow - mid) / (pump.flow.max - pump.flow.min);
                score += Math.round((1 - distance) * 10);
            }
        }
        
        // Bonus por altura en rango
        if (params.head) {
            if (params.head >= pump.head.min && params.head <= pump.head.max) {
                score += 20;
                var midH = (pump.head.min + pump.head.max) / 2;
                var distanceH = Math.abs(params.head - midH) / (pump.head.max - pump.head.min);
                score += Math.round((1 - distanceH) * 10);
            }
        }
        
        // Ajuste por prioridad
        if (params.priority === 'efficiency') {
            score += pump.efficiency / 5;
        } else if (params.priority === 'cost') {
            score += Math.max(0, 15 - pump.power);
        } else if (params.priority === 'durability') {
            if (pump.material === 'stainless') score += 10;
        } else if (params.priority === 'compact') {
            score += Math.max(0, 10 - pump.power / 2);
        }
        
        return Object.assign({}, pump, { score: Math.min(100, Math.round(score)) });
    });
    
    // Ordenar por puntuacion
    results.sort(function(a, b) { return b.score - a.score; });
    
    return results;
}

function renderResults(results, isApproximate, params) {
    const container = document.getElementById('results-content');
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<div class="placeholder">' +
            '<i class="fas fa-search"></i>' +
            '<h4>Sin resultados</h4>' +
            '<p>No se encontraron bombas con estos parametros. Prueba a ajustar los filtros.</p>' +
        '</div>';
        return;
    }
    
    var html = '';
    
    // Mostrar aviso si son resultados aproximados
    if (isApproximate) {
        var searchDesc = [];
        if (params && params.flow) searchDesc.push(params.flow + ' m3/h');
        if (params && params.head) searchDesc.push(params.head + ' m');
        if (params && params.sector) searchDesc.push(getSectorName(params.sector));
        
        html += '<div class="approximate-warning">' +
            '<div class="warning-icon"><i class="fas fa-exclamation-triangle"></i></div>' +
            '<div class="warning-content">' +
                '<h4><i class="fas fa-info-circle"></i> No hay coincidencias exactas</h4>' +
                '<p>No encontramos bombas que cumplan exactamente con <strong>' + searchDesc.join(', ') + '</strong>.</p>' +
                '<p>Mostramos las <strong>' + results.length + ' bombas mas similares</strong> a tus requerimientos. Considera ajustar tus parametros o contactarnos para una solucion personalizada.</p>' +
            '</div>' +
        '</div>';
    }
    
    html += results.map(function(pump, index) {
        var isCompared = compareList.indexOf(pump.id) >= 0;
        var reasonsHtml = '';
        
        // Mostrar razones de aproximacion si existen
        if (isApproximate && pump.approximateReasons && pump.approximateReasons.length > 0) {
            reasonsHtml = '<div class="pump-approximate-reasons">' +
                '<i class="fas fa-info-circle"></i> ' + pump.approximateReasons.join(', ') +
            '</div>';
        }
        
        // Obtener rango de potencia para series
        var powerDisplay = typeof pump.power === 'object' 
            ? pump.power.min + '-' + pump.power.max + ' kW'
            : pump.power + ' kW';
        
        return '<div class="pump-card ' + (index === 0 ? 'best-match' : '') + (isApproximate ? ' approximate' : '') + '">' +
            '<div class="pump-score ' + (pump.score >= 80 ? 'high' : pump.score >= 60 ? 'medium' : 'low') + '">' +
                pump.score + '%' +
            '</div>' +
            '<div class="pump-icon">' +
                '<i class="fas ' + getSeriesIcon(pump.series) + '"></i>' +
            '</div>' +
            '<div class="pump-info">' +
                '<h4>' + pump.name + '</h4>' +
                '<span class="pump-series">' + pump.type + '</span>' +
                (pump.description ? '<p class="pump-description">' + pump.description + '</p>' : '') +
                '<div class="pump-specs">' +
                    '<span><i class="fas fa-tachometer-alt"></i> ' + pump.flow.min + '-' + pump.flow.max + ' m³/h</span>' +
                    '<span><i class="fas fa-arrows-alt-v"></i> ' + pump.head.min + '-' + pump.head.max + ' m</span>' +
                    '<span><i class="fas fa-bolt"></i> ' + powerDisplay + '</span>' +
                    (pump.solids > 0 ? '<span><i class="fas fa-circle"></i> Sólidos ≤' + pump.solids + 'mm</span>' : '') +
                '</div>' +
                reasonsHtml +
            '</div>' +
            '<div class="pump-actions">' +
                '<button class="btn-details" onclick="showPumpDetails(\'' + pump.id + '\')">' +
                    '<i class="fas fa-info-circle"></i> Detalles' +
                '</button>' +
                (pump.catalog ? '<a href="assets/docs/' + pump.catalog + '" target="_blank" class="btn-catalog">' +
                    '<i class="fas fa-file-pdf"></i>' +
                '</a>' : '') +
                '<button class="btn-compare ' + (isCompared ? 'active' : '') + '" onclick="toggleCompare(\'' + pump.id + '\')">' +
                    '<i class="fas fa-balance-scale"></i>' +
                '</button>' +
            '</div>' +
        '</div>';
    }).join('');
    
    container.innerHTML = html;
}

function updateResultsCount(count) {
    const el = document.getElementById('results-number');
    if (el) el.textContent = count;
}

function getSeriesIcon(series) {
    return SERIES_INFO[series]?.icon || 'fa-cogs';
}

function getSectorName(sector) {
    var names = {
        'water': 'Agua',
        'agriculture': 'Riego',
        'industrial': 'Industrial',
        'building': 'Edificios',
        'drainage': 'Drenaje',
        'fire': 'Incendios'
    };
    return names[sector] || sector;
}

// ============================================================
// PRESETS
// ============================================================
function applyPreset(preset) {
    resetForm();
    
    var sectorRadio, flowInput = document.getElementById('flow-value'), headInput = document.getElementById('head-value');
    var solidSlider = document.getElementById('solid-size'), solidDisplay = document.getElementById('solid-display');
    
    switch(preset) {
        case 'domestic':
            sectorRadio = document.querySelector('input[name="sector"][value="water"]');
            if (sectorRadio) sectorRadio.checked = true;
            if (flowInput) flowInput.value = 3;
            if (headInput) headInput.value = 40;
            break;
        case 'irrigation':
            sectorRadio = document.querySelector('input[name="sector"][value="agriculture"]');
            if (sectorRadio) sectorRadio.checked = true;
            if (flowInput) flowInput.value = 25;
            if (headInput) headInput.value = 50;
            break;
        case 'industrial':
            sectorRadio = document.querySelector('input[name="sector"][value="industrial"]');
            if (sectorRadio) sectorRadio.checked = true;
            if (flowInput) flowInput.value = 80;
            if (headInput) headInput.value = 60;
            break;
        case 'sewage':
            sectorRadio = document.querySelector('input[name="sector"][value="drainage"]');
            if (sectorRadio) sectorRadio.checked = true;
            if (flowInput) flowInput.value = 40;
            if (headInput) headInput.value = 15;
            if (solidSlider) solidSlider.value = 50;
            if (solidDisplay) solidDisplay.textContent = '50 mm';
            break;
    }
    
    performSearch();
}

// ============================================================
// RESET
// ============================================================
function resetForm() {
    const form = document.getElementById('pump-selector-form');
    if (form) form.reset();
    
    // Restaurar valores por defecto
    var solidSlider = document.getElementById('solid-size');
    var solidDisplay = document.getElementById('solid-display');
    var effSlider = document.getElementById('min-efficiency');
    var effDisplay = document.getElementById('efficiency-value');
    
    if (solidSlider) solidSlider.value = 0;
    if (solidDisplay) solidDisplay.textContent = '0 mm';
    if (effSlider) effSlider.value = 0;
    if (effDisplay) effDisplay.textContent = '0%';
    
    // Limpiar resultados
    const resultsContent = document.getElementById('results-content');
    if (resultsContent) {
        resultsContent.innerHTML = '<div class="placeholder">' +
            '<i class="fas fa-search"></i>' +
            '<h4>Busca tu bomba ideal</h4>' +
            '<p>Configura los parametros y pulsa "Buscar Bombas"</p>' +
            '<div class="quick-presets">' +
                '<p>O prueba un preset:</p>' +
                '<div class="preset-buttons">' +
                    '<button class="btn-preset" data-preset="domestic"><i class="fas fa-home"></i> Domestico</button>' +
                    '<button class="btn-preset" data-preset="irrigation"><i class="fas fa-seedling"></i> Riego</button>' +
                    '<button class="btn-preset" data-preset="industrial"><i class="fas fa-industry"></i> Industrial</button>' +
                    '<button class="btn-preset" data-preset="sewage"><i class="fas fa-recycle"></i> Residuales</button>' +
                '</div>' +
            '</div>' +
        '</div>';
        // Re-bind preset buttons
        resultsContent.querySelectorAll('.btn-preset').forEach(function(btn) {
            btn.addEventListener('click', function() {
                applyPreset(this.dataset.preset);
            });
        });
    }
    
    updateResultsCount(0);
    currentResults = [];
}

// ============================================================
// DETALLES DE BOMBA
// ============================================================
function showPumpDetails(pumpId) {
    const pump = PUMPS_DATABASE.find(function(p) { return p.id === pumpId; });
    if (!pump) return;
    
    const modalBody = document.getElementById('pump-modal-body');
    if (!modalBody) return;
    
    var materialName = pump.material === 'stainless' ? 'Acero Inoxidable AISI 304' : 
                       pump.material === 'stainless-316' ? 'Acero Inoxidable AISI 316' :
                       pump.material === 'cast-iron' ? 'Fundición GG-25' : 
                       pump.material === 'hdpe' ? 'HDPE' :
                       pump.material === 'bronze' ? 'Bronce' : pump.material;
    
    var phaseName = pump.phase === 'single' ? 'Monofásica' :
                    pump.phase === 'three' ? 'Trifásica' :
                    pump.phase === 'both' ? 'Mono/Trifásica' :
                    pump.phase === 'solar' ? 'Solar DC' : pump.phase;
    
    var installName = pump.installation === 'surface' ? 'Superficie' :
                      pump.installation === 'submerged' ? 'Sumergida' :
                      pump.installation === 'inline' ? 'En Línea' :
                      pump.installation === 'vertical' ? 'Vertical' :
                      pump.installation === 'floating' ? 'Flotante' : pump.installation;
    
    // Obtener rango de potencia para series
    var powerDisplay = typeof pump.power === 'object' 
        ? pump.power.min + ' - ' + pump.power.max + ' kW'
        : pump.power + ' kW (' + (pump.power * 1.341).toFixed(1) + ' HP)';
    
    var isCompared = compareList.indexOf(pump.id) >= 0;
    
    modalBody.innerHTML = '<div class="pump-detail-header">' +
        '<div class="pump-detail-icon"><i class="fas ' + getSeriesIcon(pump.series) + '"></i></div>' +
        '<div><h2>' + pump.name + '</h2><p>' + pump.type + '</p></div>' +
    '</div>' +
    (pump.description ? '<div class="pump-detail-description"><p>' + pump.description + '</p></div>' : '') +
    '<div class="pump-detail-grid">' +
        '<div class="detail-section">' +
            '<h4><i class="fas fa-chart-line"></i> Rango Hidráulico</h4>' +
            '<div class="detail-row"><span>Caudal:</span><strong>' + pump.flow.min + ' - ' + pump.flow.max + ' m³/h</strong></div>' +
            '<div class="detail-row"><span>Altura:</span><strong>' + pump.head.min + ' - ' + pump.head.max + ' m</strong></div>' +
            '<div class="detail-row"><span>Potencia:</span><strong>' + powerDisplay + '</strong></div>' +
            '<div class="detail-row"><span>Eficiencia:</span><strong>Hasta ' + pump.efficiency + '%</strong></div>' +
            (pump.solids > 0 ? '<div class="detail-row"><span>Paso sólidos:</span><strong>Hasta ' + pump.solids + ' mm</strong></div>' : '') +
        '</div>' +
        '<div class="detail-section">' +
            '<h4><i class="fas fa-tools"></i> Características Técnicas</h4>' +
            '<div class="detail-row"><span>Material:</span><strong>' + materialName + '</strong></div>' +
            '<div class="detail-row"><span>Temp. máx.:</span><strong>' + pump.maxTemp + '°C</strong></div>' +
            '<div class="detail-row"><span>RPM:</span><strong>' + (pump.rpm || 'Variable') + '</strong></div>' +
            '<div class="detail-row"><span>Conexiones:</span><strong>' + pump.connection + '</strong></div>' +
            '<div class="detail-row"><span>Alimentación:</span><strong>' + phaseName + '</strong></div>' +
            '<div class="detail-row"><span>Instalación:</span><strong>' + installName + '</strong></div>' +
        '</div>' +
    '</div>' +
    '<div class="detail-section">' +
        '<h4><i class="fas fa-industry"></i> Sectores de Aplicación</h4>' +
        '<div class="sector-tags">' + pump.sectors.map(function(s) { return '<span class="sector-tag">' + getSectorName(s) + '</span>'; }).join('') + '</div>' +
    '</div>' +
    '<div class="pump-detail-note">' +
        '<i class="fas fa-info-circle"></i> ' +
        '<span>El modelo específico se determina según los parámetros exactos de la instalación. Consulte el catálogo o contacte con nuestro departamento técnico.</span>' +
    '</div>' +
    '<div class="pump-detail-actions">' +
        (pump.catalog ? '<a href="assets/docs/' + pump.catalog + '" target="_blank" class="btn-primary">' +
            '<i class="fas fa-file-pdf"></i> Ver Catálogo</a>' : '') +
        (pump.productPage ? '<a href="' + pump.productPage + '" class="btn-secondary">' +
            '<i class="fas fa-external-link-alt"></i> Ver Producto</a>' : '') +
        '<button class="btn-primary" onclick="requestQuote(\'' + pump.id + '\')">' +
            '<i class="fas fa-envelope"></i> Solicitar Presupuesto</button>' +
        '<button class="btn-secondary ' + (isCompared ? 'active' : '') + '" onclick="toggleCompare(\'' + pump.id + '\'); closeModal(\'pump-modal\');">' +
            '<i class="fas fa-balance-scale"></i> Comparar</button>' +
    '</div>';
    
    openModal('pump-modal');
}

// ============================================================
// COMPARACION
// ============================================================
function toggleCompare(pumpId) {
    var index = compareList.indexOf(pumpId);
    
    if (index >= 0) {
        compareList.splice(index, 1);
        showToast('Bomba eliminada de comparacion', 'info');
    } else {
        if (compareList.length >= 4) {
            showToast('Maximo 4 bombas para comparar', 'warning');
            return;
        }
        compareList.push(pumpId);
        showToast('Bomba anadida a comparacion', 'success');
    }
    
    localStorage.setItem('bipsCompare', JSON.stringify(compareList));
    updateComparisonUI();
    
    // Re-render results si hay
    if (currentResults.length > 0) {
        renderResults(currentResults);
    }
}

function updateComparisonUI() {
    var section = document.getElementById('comparison-section');
    
    if (section) {
        section.style.display = compareList.length > 0 ? 'block' : 'none';
    }
    
    if (compareList.length > 0) {
        renderComparisonTable();
    }
}

function renderComparisonTable() {
    var tbody = document.getElementById('comparison-body');
    if (!tbody) return;
    
    var pumps = compareList.map(function(id) { 
        return PUMPS_DATABASE.find(function(p) { return p.id === id; }); 
    }).filter(Boolean);
    
    if (pumps.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7">No hay bombas seleccionadas</td></tr>';
        return;
    }
    
    // Encontrar mejores valores
    var maxFlow = Math.max.apply(null, pumps.map(function(p) { return p.flow.max; }));
    var maxHead = Math.max.apply(null, pumps.map(function(p) { return p.head.max; }));
    var minPower = Math.min.apply(null, pumps.map(function(p) { return p.power; }));
    var maxEff = Math.max.apply(null, pumps.map(function(p) { return p.efficiency; }));
    
    tbody.innerHTML = pumps.map(function(pump) {
        var materialName = pump.material === 'stainless' ? 'Inox' : 
                           pump.material === 'cast-iron' ? 'Fundicion' : pump.material;
        
        return '<tr>' +
            '<td><strong>' + pump.name + '</strong><br><small>Serie ' + pump.series + '</small></td>' +
            '<td class="' + (pump.flow.max === maxFlow ? 'highlight' : '') + '">' + pump.flow.min + '-' + pump.flow.max + ' m3/h</td>' +
            '<td class="' + (pump.head.max === maxHead ? 'highlight' : '') + '">' + pump.head.min + '-' + pump.head.max + ' m</td>' +
            '<td class="' + (pump.power === minPower ? 'highlight' : '') + '">' + pump.power + ' kW</td>' +
            '<td class="' + (pump.efficiency === maxEff ? 'highlight' : '') + '">' + pump.efficiency + '%</td>' +
            '<td>' + materialName + '</td>' +
            '<td><button class="btn-remove" onclick="toggleCompare(\'' + pump.id + '\')"><i class="fas fa-times"></i></button></td>' +
        '</tr>';
    }).join('');
}

function clearComparison() {
    compareList = [];
    localStorage.setItem('bipsCompare', '[]');
    updateComparisonUI();
    
    if (currentResults.length > 0) {
        renderResults(currentResults);
    }
    
    showToast('Comparacion limpiada', 'success');
}

function quoteSelected() {
    if (compareList.length === 0) {
        showToast('Selecciona bombas para presupuestar', 'warning');
        return;
    }
    
    var pumps = compareList.map(function(id) { 
        return PUMPS_DATABASE.find(function(p) { return p.id === id; }); 
    }).filter(Boolean);
    
    // Rellenar modal de presupuesto
    var list = document.getElementById('selected-pumps-list');
    if (list) {
        list.innerHTML = pumps.map(function(p) {
            return '<div class="selected-pump-item">' +
                '<strong>' + p.name + '</strong>' +
                '<span>' + p.flow.min + '-' + p.flow.max + ' m3/h, ' + p.head.min + '-' + p.head.max + ' m</span>' +
            '</div>';
        }).join('');
    }
    
    openModal('quote-modal');
}

// ============================================================
// PRESUPUESTO
// ============================================================
function requestQuote(pumpId) {
    var pump = PUMPS_DATABASE.find(function(p) { return p.id === pumpId; });
    if (!pump) return;
    
    closeModal('pump-modal');
    
    // Crear mailto
    var subject = encodeURIComponent('Presupuesto ' + pump.name + ' - BIPS');
    var body = encodeURIComponent(
        'Solicitud de presupuesto desde BIPS\n' +
        '=====================================\n\n' +
        'Modelo: ' + pump.name + '\n' +
        'Serie: ' + pump.series + '\n' +
        'Tipo: ' + pump.type + '\n\n' +
        'Especificaciones:\n' +
        '- Caudal: ' + pump.flow.min + ' - ' + pump.flow.max + ' m3/h\n' +
        '- Altura: ' + pump.head.min + ' - ' + pump.head.max + ' m\n' +
        '- Potencia: ' + pump.power + ' kW\n\n' +
        'Por favor, envienme informacion y precio.\n\n' +
        'Gracias.'
    );
    
    window.open('mailto:info@bombasideal.com?subject=' + subject + '&body=' + body, '_blank');
}

function submitQuote() {
    var form = document.getElementById('quote-form');
    if (!form) return;
    
    var formData = new FormData(form);
    var pumps = compareList.map(function(id) { 
        return PUMPS_DATABASE.find(function(p) { return p.id === id; }); 
    }).filter(Boolean);
    
    var subject = encodeURIComponent('Presupuesto BIPS - ' + pumps.length + ' bombas');
    var body = encodeURIComponent(
        'Solicitud de presupuesto desde BIPS\n' +
        '=====================================\n\n' +
        'Datos de contacto:\n' +
        '- Nombre: ' + formData.get('name') + '\n' +
        '- Email: ' + formData.get('email') + '\n' +
        '- Telefono: ' + (formData.get('phone') || 'No indicado') + '\n\n' +
        'Bombas seleccionadas:\n' +
        pumps.map(function(p) { return '- ' + p.name + ' (' + p.flow.max + ' m3/h, ' + p.head.max + ' m)'; }).join('\n') +
        '\n\nComentarios:\n' + (formData.get('comments') || 'Sin comentarios') + '\n'
    );
    
    window.open('mailto:info@bombasideal.com?subject=' + subject + '&body=' + body, '_blank');
    
    closeModal('quote-modal');
    showToast('Redirigiendo a email...', 'success');
}

// ============================================================
// CALCULADORA
// ============================================================
function calculatePower() {
    var flowEl = document.getElementById('calc-flow');
    var headEl = document.getElementById('calc-head');
    var densityEl = document.getElementById('calc-density');
    
    var flow = parseFloat(flowEl?.value) || 0;
    var head = parseFloat(headEl?.value) || 0;
    var density = parseFloat(densityEl?.value) || 1000;
    
    var resultKw = document.getElementById('calc-result-value');
    var resultHp = document.getElementById('calc-result-hp');
    
    if (flow > 0 && head > 0) {
        // P = (Q * H * rho * g) / (3600 * 1000 * eta)
        // Asumiendo eficiencia del 70%
        var efficiency = 0.7;
        var kw = (flow * head * density * 9.81) / (3600 * 1000 * efficiency);
        var hp = kw * 1.341;
        
        if (resultKw) resultKw.textContent = kw.toFixed(2) + ' kW';
        if (resultHp) resultHp.textContent = hp.toFixed(2) + ' HP';
    } else {
        if (resultKw) resultKw.textContent = '-- kW';
        if (resultHp) resultHp.textContent = '-- HP';
    }
}

// ============================================================
// EXPORTACION
// ============================================================
function exportToPDF() {
    if (currentResults.length === 0) {
        showToast('No hay resultados para exportar', 'warning');
        return;
    }
    
    if (typeof window.jspdf === 'undefined') {
        showToast('Libreria PDF no disponible', 'error');
        return;
    }
    
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF();
    
    // Titulo
    doc.setFontSize(20);
    doc.setFont(undefined, 'bold');
    doc.text('BIPS - Resultados de Busqueda', 20, 20);
    
    // Subtitulo
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    doc.text('Bombas Ideal Pump Selector', 20, 28);
    doc.text('Fecha: ' + new Date().toLocaleDateString('es-ES'), 20, 34);
    doc.text('Total: ' + currentResults.length + ' bombas encontradas', 20, 40);
    
    // Linea
    doc.setDrawColor(0, 91, 187);
    doc.line(20, 45, 190, 45);
    
    // Resultados
    var y = 55;
    currentResults.slice(0, 15).forEach(function(pump, i) {
        if (y > 270) {
            doc.addPage();
            y = 20;
        }
        
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.text((i + 1) + '. ' + pump.name, 20, y);
        
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text('Serie ' + pump.series + ' | ' + pump.type, 25, y + 5);
        doc.text('Caudal: ' + pump.flow.min + '-' + pump.flow.max + ' m3/h | Altura: ' + pump.head.min + '-' + pump.head.max + ' m | Potencia: ' + pump.power + ' kW | Eficiencia: ' + pump.efficiency + '%', 25, y + 10);
        
        y += 20;
    });
    
    // Footer
    doc.setFontSize(8);
    doc.text('www.bombasideal.com - BIPS v3.1', 20, 285);
    
    doc.save('bips-resultados.pdf');
    showToast('PDF exportado correctamente', 'success');
}

function exportToExcel() {
    if (currentResults.length === 0) {
        showToast('No hay resultados para exportar', 'warning');
        return;
    }
    
    if (typeof XLSX === 'undefined') {
        showToast('Libreria Excel no disponible', 'error');
        return;
    }
    
    var data = currentResults.map(function(pump) {
        return {
            'Modelo': pump.name,
            'Serie': pump.series,
            'Tipo': pump.type,
            'Caudal Min (m3/h)': pump.flow.min,
            'Caudal Max (m3/h)': pump.flow.max,
            'Altura Min (m)': pump.head.min,
            'Altura Max (m)': pump.head.max,
            'Potencia (kW)': pump.power,
            'Potencia (HP)': (pump.power * 1.341).toFixed(1),
            'Eficiencia (%)': pump.efficiency,
            'Material': pump.material,
            'Temp Max (C)': pump.maxTemp,
            'Conexion': pump.connection,
            'Puntuacion': pump.score
        };
    });
    
    var ws = XLSX.utils.json_to_sheet(data);
    var wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'BIPS Resultados');
    
    XLSX.writeFile(wb, 'bips-resultados.xlsx');
    showToast('Excel exportado correctamente', 'success');
}

// ============================================================
// MODALES
// ============================================================
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================================
// TOASTS
// ============================================================
function showToast(message, type) {
    type = type || 'info';
    var container = document.getElementById('toast-container');
    if (!container) return;
    
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    
    var icon = type === 'success' ? 'fa-check-circle' :
               type === 'warning' ? 'fa-exclamation-triangle' :
               type === 'error' ? 'fa-times-circle' : 'fa-info-circle';
    
    toast.innerHTML = '<i class="fas ' + icon + '"></i><span>' + message + '</span>';
    
    container.appendChild(toast);
    
    // Auto remove
    setTimeout(function() {
        toast.classList.add('fade-out');
        setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
}
