"""Seed data for Bombas Omni - Water pump factory."""

from datetime import datetime, timedelta

# Tipos de bombas (6 líneas de producción)
TIPOS_BOMBAS = [
    {
        "id": "bomba-centrifuga",
        "nombre": "Bomba Centrífuga BC-100",
        "codigo": "BC-100",
        "seccion": "seccion-centrifuga",
        "descripcion": "Bomba centrífuga para uso industrial, 1HP",
    },
    {
        "id": "bomba-sumergible",
        "nombre": "Bomba Sumergible BS-200",
        "codigo": "BS-200",
        "seccion": "seccion-sumergible",
        "descripcion": "Bomba sumergible para pozos profundos, 2HP",
    },
    {
        "id": "bomba-autoaspirante",
        "nombre": "Bomba Autoaspirante BA-150",
        "codigo": "BA-150",
        "seccion": "seccion-autoaspirante",
        "descripcion": "Bomba autoaspirante para piscinas, 1.5HP",
    },
    {
        "id": "bomba-diesel",
        "nombre": "Bomba Diésel BD-300",
        "codigo": "BD-300",
        "seccion": "seccion-diesel",
        "descripcion": "Bomba con motor diésel para riego agrícola, 3HP",
    },
    {
        "id": "bomba-presion",
        "nombre": "Bomba de Presión BP-180",
        "codigo": "BP-180",
        "seccion": "seccion-presion",
        "descripcion": "Bomba de presión doméstica, 1.8HP",
    },
    {
        "id": "bomba-industrial",
        "nombre": "Bomba Industrial BI-500",
        "codigo": "BI-500",
        "seccion": "seccion-industrial",
        "descripcion": "Bomba industrial pesada para minería, 5HP",
    },
]

# Secciones de producción
SECCIONES_PRODUCCION = [
    {
        "id": "seccion-centrifuga",
        "nombre": "Sección Centrífuga",
        "tipo": "fabricacion",
        "producto_principal": "BC-100",
    },
    {
        "id": "seccion-sumergible",
        "nombre": "Sección Sumergible",
        "tipo": "fabricacion",
        "producto_principal": "BS-200",
    },
    {
        "id": "seccion-autoaspirante",
        "nombre": "Sección Autoaspirante",
        "tipo": "fabricacion",
        "producto_principal": "BA-150",
    },
    {
        "id": "seccion-diesel",
        "nombre": "Sección Diésel",
        "tipo": "fabricacion",
        "producto_principal": "BD-300",
    },
    {
        "id": "seccion-presion",
        "nombre": "Sección Presión",
        "tipo": "fabricacion",
        "producto_principal": "BP-180",
    },
    {
        "id": "seccion-industrial",
        "nombre": "Sección Industrial",
        "tipo": "fabricacion",
        "producto_principal": "BI-500",
    },
    {
        "id": "seccion-mecanizado",
        "nombre": "Sección Mecanizado",
        "tipo": "apoyo",
        "descripcion": "Mecanizado de cuerpos de bomba y piezas especiales",
    },
    {
        "id": "seccion-pintura",
        "nombre": "Sección Pintura",
        "tipo": "apoyo",
        "descripcion": "Acabado y pintura de componentes",
    },
    {
        "id": "seccion-embalaje",
        "nombre": "Sección Embalaje",
        "tipo": "apoyo",
        "descripcion": "Empaque y preparación para envío",
    },
]

# Componentes base
COMPONENTES = [
    # Motores
    {"codigo": "MOT-E-1HP", "nombre": "Motor Eléctrico 1HP", "tipo": "motor", "subtipo": "electrico"},
    {"codigo": "MOT-E-1.5HP", "nombre": "Motor Eléctrico 1.5HP", "tipo": "motor", "subtipo": "electrico"},
    {"codigo": "MOT-E-1.8HP", "nombre": "Motor Eléctrico 1.8HP", "tipo": "motor", "subtipo": "electrico"},
    {"codigo": "MOT-E-2HP", "nombre": "Motor Eléctrico 2HP", "tipo": "motor", "subtipo": "electrico"},
    {"codigo": "MOT-E-5HP", "nombre": "Motor Eléctrico 5HP", "tipo": "motor", "subtipo": "electrico"},
    {"codigo": "MOT-D-3HP", "nombre": "Motor Diésel 3HP", "tipo": "motor", "subtipo": "diesel"},
    
    # Chasis
    {"codigo": "CHS-P", "nombre": "Chasis Pequeño", "tipo": "chasis", "material": "acero"},
    {"codigo": "CHS-M", "nombre": "Chasis Mediano", "tipo": "chasis", "material": "acero"},
    {"codigo": "CHS-G", "nombre": "Chasis Grande", "tipo": "chasis", "material": "acero_reforzado"},
    
    # Manguitos
    {"codigo": "MNG-50", "nombre": "Manguito Unión 50mm", "tipo": "manguito"},
    {"codigo": "MNG-75", "nombre": "Manguito Unión 75mm", "tipo": "manguito"},
    {"codigo": "MNG-100", "nombre": "Manguito Unión 100mm", "tipo": "manguito"},
    
    # Cuerpos de bomba (algunos mecanizados internos, otros externos)
    {"codigo": "CRP-CENT", "nombre": "Cuerpo Centrífugo", "tipo": "cuerpo", "mecanizado": "interno"},
    {"codigo": "CRP-SUMG", "nombre": "Cuerpo Sumergible", "tipo": "cuerpo", "mecanizado": "externo"},
    {"codigo": "CRP-AUTO", "nombre": "Cuerpo Autoaspirante", "tipo": "cuerpo", "mecanizado": "interno"},
    {"codigo": "CRP-DIES", "nombre": "Cuerpo Diésel", "tipo": "cuerpo", "mecanizado": "externo"},
    {"codigo": "CRP-PRES", "nombre": "Cuerpo Presión", "tipo": "cuerpo", "mecanizado": "interno"},
    {"codigo": "CRP-INDL", "nombre": "Cuerpo Industrial", "tipo": "cuerpo", "mecanizado": "externo"},
    
    # Hélices
    {"codigo": "HLC-5", "nombre": "Hélice 5 palas", "tipo": "helice", "palas": 5},
    {"codigo": "HLC-6", "nombre": "Hélice 6 palas", "tipo": "helice", "palas": 6},
    {"codigo": "HLC-8", "nombre": "Hélice 8 palas reforzada", "tipo": "helice", "palas": 8},
    
    # Fontanería
    {"codigo": "FTN-KIT-P", "nombre": "Kit Fontanería Pequeño", "tipo": "fontaneria"},
    {"codigo": "FTN-KIT-M", "nombre": "Kit Fontanería Mediano", "tipo": "fontaneria"},
    {"codigo": "FTN-KIT-G", "nombre": "Kit Fontanería Grande", "tipo": "fontaneria"},
    
    # Tornillería y varios
    {"codigo": "TRN-M8", "nombre": "Tornillos M8 (pack 50)", "tipo": "tornilleria"},
    {"codigo": "TRN-M10", "nombre": "Tornillos M10 (pack 50)", "tipo": "tornilleria"},
    {"codigo": "ARN-M8", "nombre": "Arandelas M8 (pack 100)", "tipo": "tornilleria"},
    {"codigo": "ARN-M10", "nombre": "Arandelas M10 (pack 100)", "tipo": "tornilleria"},
    {"codigo": "JNT-NBR", "nombre": "Juntas NBR (pack 10)", "tipo": "sellado"},
]

# BOMs (Bill of Materials) - componentes por bomba
BOMS = {
    "BC-100": [
        "MOT-E-1HP", "CHS-P", "MNG-50", "CRP-CENT", "HLC-5", 
        "FTN-KIT-P", "TRN-M8", "ARN-M8", "JNT-NBR"
    ],
    "BS-200": [
        "MOT-E-2HP", "CHS-M", "MNG-75", "CRP-SUMG", "HLC-6",
        "FTN-KIT-M", "TRN-M10", "ARN-M10", "JNT-NBR"
    ],
    "BA-150": [
        "MOT-E-1.5HP", "CHS-P", "MNG-50", "CRP-AUTO", "HLC-5",
        "FTN-KIT-P", "TRN-M8", "ARN-M8", "JNT-NBR"
    ],
    "BD-300": [
        "MOT-D-3HP", "CHS-M", "MNG-75", "CRP-DIES", "HLC-6",
        "FTN-KIT-M", "TRN-M10", "ARN-M10", "JNT-NBR"
    ],
    "BP-180": [
        "MOT-E-1.8HP", "CHS-M", "MNG-75", "CRP-PRES", "HLC-6",
        "FTN-KIT-M", "TRN-M8", "ARN-M8", "JNT-NBR"
    ],
    "BI-500": [
        "MOT-E-5HP", "CHS-G", "MNG-100", "CRP-INDL", "HLC-8",
        "FTN-KIT-G", "TRN-M10", "ARN-M10", "JNT-NBR"
    ],
}

# Órdenes de producción ejemplo
ORDENES_EJEMPLO = [
    # Bomba Centrífuga - en ensamble
    {
        "numero": "OP-2401",
        "producto": "Bomba Centrífuga BC-100",
        "codigo_producto": "BC-100",
        "seccion": "seccion-centrifuga",
        "etapa": "Ensamble",
        "avance": 45,
        "estado": "en_curso",
        "dias_desde_inicio": 2,
        "dias_hasta_prevista": 3,
    },
    # Bomba Sumergible - esperando mecanizado externo
    {
        "numero": "OP-2402",
        "producto": "Bomba Sumergible BS-200",
        "codigo_producto": "BS-200",
        "seccion": "seccion-sumergible",
        "etapa": "Mecanizado externo",
        "avance": 25,
        "estado": "en_espera_externo",
        "dias_desde_inicio": 5,
        "dias_hasta_prevista": 7,
        "proveedor_externo": "Mecanizados Pérez S.L.",
    },
    # Bomba Autoaspirante - en pintura
    {
        "numero": "OP-2403",
        "producto": "Bomba Autoaspirante BA-150",
        "codigo_producto": "BA-150",
        "seccion": "seccion-autoaspirante",
        "etapa": "Pintura",
        "avance": 75,
        "estado": "en_curso",
        "dias_desde_inicio": 4,
        "dias_hasta_prevista": 1,
    },
    # Bomba Diésel - en picking
    {
        "numero": "OP-2404",
        "producto": "Bomba Diésel BD-300",
        "codigo_producto": "BD-300",
        "seccion": "seccion-diesel",
        "etapa": "Picking",
        "avance": 10,
        "estado": "picking",
        "dias_desde_inicio": 0,
        "dias_hasta_prevista": 8,
    },
    # Bomba Presión - en embalaje
    {
        "numero": "OP-2405",
        "producto": "Bomba de Presión BP-180",
        "codigo_producto": "BP-180",
        "seccion": "seccion-presion",
        "etapa": "Embalaje",
        "avance": 90,
        "estado": "en_curso",
        "dias_desde_inicio": 6,
        "dias_hasta_prevista": 1,
    },
    # Bomba Industrial - mecanizado interno
    {
        "numero": "OP-2406",
        "producto": "Bomba Industrial BI-500",
        "codigo_producto": "BI-500",
        "seccion": "seccion-industrial",
        "etapa": "Mecanizado",
        "avance": 35,
        "estado": "en_curso",
        "dias_desde_inicio": 3,
        "dias_hasta_prevista": 5,
    },
    # Más órdenes variadas
    {
        "numero": "OP-2407",
        "producto": "Bomba Centrífuga BC-100",
        "codigo_producto": "BC-100",
        "seccion": "seccion-centrifuga",
        "etapa": "Picking",
        "avance": 5,
        "estado": "picking",
        "dias_desde_inicio": 0,
        "dias_hasta_prevista": 5,
    },
    {
        "numero": "OP-2408",
        "producto": "Bomba Sumergible BS-200",
        "codigo_producto": "BS-200",
        "seccion": "seccion-sumergible",
        "etapa": "Ensamble",
        "avance": 60,
        "estado": "en_curso",
        "dias_desde_inicio": 3,
        "dias_hasta_prevista": 2,
    },
]
