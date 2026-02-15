#!/usr/bin/env ts-node
/**
 * Script para generar contenido educativo REAL para cursos con placeholders
 * Reemplaza "Contenido de la lección X" con contenido de calidad
 */

import * as fs from 'fs';
import * as path from 'path';

// Definiciones de contenido educativo por curso
const coursesContent: Record<string, any> = {
  'impresion3d-intro': {
    title: 'Impresión 3D',
    lessons: 10,
    content: [
      {
        title: 'Introducción a la Impresión 3D',
        intro: 'La impresión 3D revoluciona la fabricación permitiendo crear objetos físicos desde modelos digitales.',
        concepts: [
          'Tecnologías: FDM (más común), SLA (resina), SLS (sinterizado)',
          'Aplicaciones: prototipos, piezas funcionales, arte, medicina',
          'Ventajas: personalización, producción bajo demanda, diseño complejo'
        ],
        example: 'Impresoras populares: Ender 3 ($200), Prusa i3 ($800), Bambu Lab X1 ($1200)',
        practice: 'Investiga 3 impresoras FDM y compara especificaciones'
      },
      {
        title: 'Modelado 3D para Impresión',
        intro: 'Crear diseños optimizados para impresión requiere conocer software CAD y limitaciones técnicas.',
        concepts: [
          'Software gratuito: Tinkercad (web, principiantes), Blender (avanzado)',
          'Software profesional: Fusion 360, SolidWorks',
          'Consideraciones: grosor de paredes (mín. 2mm), ángulos de impresión, soportes'
        ],
        example: 'Diseñar soporte de móvil con tolerancias de 0.2mm para ajuste perfecto',
        practice: 'Crea un llavero personalizado en Tinkercad y expórtalo a STL'
      },
      {
        title: 'Slicing: Preparación de Modelos',
        intro: 'El slicing convierte modelos 3D en instrucciones G-code que la impresora puede ejecutar.',
        concepts: [
          'Software: Cura (gratis, versátil), PrusaSlicer, Simplify3D (pago)',
          'Altura de capa: 0.1mm (detalle) vs 0.3mm (velocidad)',
          'Relleno: 20% normal, 100% piezas funcionales, patrones (grid, gyroid)',
          'Soportes: automáticos vs manuales, tree supports para formas orgánicas'
        ],
        example: 'Slicing de Benchy (modelo de prueba) con configuración óptima',
        practice: 'Configura perfil de impresión para figura con voladizos de 60°'
      },
      {
        title: 'Calibración de Impresora',
        intro: 'Una impresora bien calibrada es la clave para impresiones perfectas y sin fallas.',
        concepts: [
          'Nivelación de cama: manual (papel) o automática (BLTouch)',
          'E-steps: calibrar flujo de filamento (100mm debe extruir exactamente 100mm)',
          'Temperature towers: encontrar temperatura óptima por filamento',
          'Retracción: evitar hilos ajustando distancia (5mm) y velocidad (45mm/s)'
        ],
        example: 'Cubo de calibración XYZ debe medir exactamente 20x20x20mm',
        practice: 'Imprime temperature tower para tu PLA y encuentra temp óptima'
      },
      {
        title: 'Materiales de Impresión',
        intro: 'Cada material tiene propiedades únicas que determinan sus aplicaciones ideales.',
        concepts: [
          'PLA: 190-220°C, fácil, biodegradable, frágil. Uso: prototipos, decoración',
          'ABS: 230-250°C, resistente al calor, vapores tóxicos. Uso: piezas funcionales',
          'PETG: 220-250°C, equilibrio PLA/ABS, resistente. Uso: piezas duraderas',
          'TPU: 210-230°C, flexible, difícil de imprimir. Uso: fundas, juntas'
        ],
        example: 'PLA para maquetas arquitectónicas, ABS para piezas de motor, TPU para amortiguadores',
        practice: 'Crea tabla comparativa de 5 materiales con pros/contras'
      },
      {
        title: 'Post-Procesado y Acabados',
        intro: 'El acabado profesional transforma impresiones rugosas en piezas pulidas y atractivas.',
        concepts: [
          'Lijado progresivo: lija 120 → 220 → 400 → 800 → 1500',
          'Relleno: masilla epóxica para grietas, XTC-3D para superficies lisas',
          'Pintado: imprimación → pintura acrílica/spray → barniz protector',
          'Acetona smoothing: solo ABS, vapores suavizan superficie'
        ],
        example: 'Figura de 20cm: 2h lijado + 1h relleno + pintado = acabado profesional',
        practice: 'Lija una pieza de PLA y documenta proceso con fotos'
      },
      {
        title: 'Solución de Problemas Comunes',
        intro: 'Diagnosticar y resolver problemas es esencial para mantener calidad de impresión.',
        concepts: [
          'Warping (esquinas levantadas): aumentar temp cama, usar brim/raft, cerrar impresora',
          'Stringing (hilos): optimizar retracción, bajar temperatura, secar filamento',
          'Layer shifting: apretar correas, verificar poleas, reducir velocidad',
          'Under-extrusion: limpiar nozzle, calibrar E-steps, verificar tensión extrusor'
        ],
        example: 'Warping en ABS: cama 100°C + recinto cerrado = éxito',
        practice: 'Diagnóstica 3 problemas comunes usando guía visual online'
      },
      {
        title: 'Diseño de Soportes Efectivos',
        intro: 'Soportes bien diseñados facilitan impresión compleja minimizando material y tiempo de limpieza.',
        concepts: [
          'Regla 45°: ángulos <45° necesitan soporte',
          'Soportes tree: menos material, fácil remoción, para formas orgánicas',
          'Soportes custom: diseñar manualmente en puntos críticos',
          'Interface layers: capas entre pieza y soporte para fácil remoción'
        ],
        example: 'Figura humana: soportes tree desde base ahorran 30% material vs lineales',
        practice: 'Optimiza soportes para busto minimizando marcas post-remoción'
      },
      {
        title: 'Impresión Multi-Material y Multi-Color',
        intro: 'Combinar materiales y colores expande posibilidades creativas y funcionales.',
        concepts: [
          'Cambio manual: pausar impresión en capa específica, cambiar filamento',
          'MMU (Multi Material Unit): hasta 5 filamentos automáticos',
          'Dual extrusión: 2 nozzles imprimen simultáneamente',
          'Materiales solubles: PVA para soportes complejos (se disuelve en agua)'
        ],
        example: 'Logo bicolor: capa base negra, letras blancas desde capa 3',
        practice: 'Imprime llavero con cambio de color manual a mitad de altura'
      },
      {
        title: 'Proyecto Final: Pieza Funcional Completa',
        intro: 'Diseña, imprime y ensambla una pieza funcional aplicando todo lo aprendido.',
        concepts: [
          'Diseño con tolerancias: holgura 0.2mm para piezas móviles',
          'Ensamblaje: bisagras impresas, roscas M3, insertos metálicos',
          'Testing iterativo: imprimir → probar → ajustar → reimprimir',
          'Documentación: fotos, medidas, configuraciones usadas'
        ],
        example: 'Caja con bisagra funcional: diseño paramétrico permite adaptar tamaño fácilmente',
        practice: 'PROYECTO: Caja organizadora con tapa a bisagra, compartimentos internos, cierre a presión'
      }
    ]
  },
  'domotica-intro': {
    title: 'Domótica y Casa Inteligente',
    lessons: 10,
    content: [
      {
        title: 'Fundamentos de Domótica',
        intro: 'La domótica integra tecnología en el hogar para automatizar tareas y mejorar calidad de vida.',
        concepts: [
          'Definición: automatización de vivienda mediante dispositivos inteligentes conectados',
          'Beneficios: ahorro energético 30%, seguridad 24/7, confort personalizado',
          'Protocolos: WiFi (más común), Zigbee (bajo consumo), Z-Wave (mesh robusto), Thread (nuevo estándar)'
        ],
        example: 'Sistema básico: bombilla Philips Hue + Google Home = control por voz ($80)',
        practice: 'Investiga 3 ecosistemas (Google, Alexa, HomeKit) y compara compatibilidad'
      },
      {
        title: 'Dispositivos Inteligentes Esenciales',
        intro: 'Los dispositivos básicos son el punto de entrada a la automatización del hogar.',
        concepts: [
          'Bombillas inteligentes: Philips Hue ($15-60), LIFX, Yeelight. Colores RGB + blanco ajustable',
          'Enchufes WiFi: TP-Link Kasa ($10), Shelly. Convierten cualquier aparato en "inteligente"',
          'Sensores: movimiento PIR, puerta/ventana magnéticos, temperatura/humedad DHT22'
        ],
        example: 'Enchufe inteligente en cafetera: programa café listo a las 7am automáticamente',
        practice: 'Configura bombilla inteligente con app móvil y crea 3 escenas'
      },
      {
        title: 'Asistentes de Voz',
        intro: 'Los asistentes permiten control manos libres y son el hub central del hogar inteligente.',
        concepts: [
          'Google Assistant: mejor comprensión natural, integración Android, Google Nest Hub',
          'Amazon Alexa: más skills (100k+), Echo Dot ($50), rutinas potentes',
          'Apple Siri/HomeKit: privacidad, ecosistema cerrado, HomePod',
          'Comandos básicos: "Enciende luz sala", "Pon temperatura a 22°", "Buenos días" (rutina)'
        ],
        example: 'Rutina matinal: "Ok Google, buenos días" → luces 100%, noticias, temperatura 21°',
        practice: 'Crea rutina "Llegar a casa" que active luces, abra persiana y ponga música'
      },
      {
        title: 'Automatizaciones Básicas con IFTTT',
        intro: 'IFTTT (If This Then That) conecta servicios y crea automatizaciones sin programación.',
        concepts: [
          'Estructura: Trigger (esto sucede) → Action (hacer esto)',
          'Ejemplos: "Si llueve → cerrar persianas", "Si salgo de casa → apagar todo"',
          'Servicios: 600+ (weather, location, smart home, redes sociales)',
          'Alternativas: Zapier (más profesional), Integromat/Make'
        ],
        example: 'Geofencing: al salir radio 500m de casa → apaga luces + activa alarma',
        practice: 'Crea applet que encienda luces al llegar a casa (basado en ubicación móvil)'
      },
      {
        title: 'Seguridad Inteligente para el Hogar',
        intro: 'Sistemas de seguridad conectados proporcionan tranquilidad y monitoreo remoto 24/7.',
        concepts: [
          'Cámaras IP: Wyze Cam ($25), Arlo, Ring. Detección movimiento, visión nocturna, nube',
          'Video doorbell: Ring ($100), Nest Hello. Ver quién toca antes de abrir',
          'Cerraduras inteligentes: August, Yale. Abrir con móvil, códigos temporales visitantes',
          'Sensores: humo/CO Nest Protect ($120), inundación, rotura cristal'
        ],
        example: 'Sistema completo: 2 cámaras + doorbell + sensores movimiento = $400',
        practice: 'Diseña sistema seguridad para apartamento 2 habitaciones con presupuesto $300'
      },
      {
        title: 'Control Inteligente de Clima',
        intro: 'Termostatos inteligentes optimizan confort y reducen factura energética hasta 25%.',
        concepts: [
          'Nest Learning Thermostat ($250): aprende rutinas, auto-programa',
          'Ecobee SmartThermostat ($200): sensores remotos, control habitación a habitación',
          'Programación inteligente: calefacción a 18° noche, 21° mañana, 16° trabajo',
          'Geofencing: detecta cuando sales y ajusta temperatura ahorro'
        ],
        example: 'Ahorro típico: $180/año con Nest vs termostato manual',
        practice: 'Programa termostato virtual con horarios optimizados para semana laboral'
      },
      {
        title: 'Home Assistant: Hub Central DIY',
        intro: 'Home Assistant es la plataforma open-source más potente para automatización del hogar.',
        concepts: [
          'Instalación: Raspberry Pi 4 ($75) + microSD ($15) + caja ($10) = $100',
          'Ventajas: privacidad local, 2000+ integraciones, automatizaciones ilimitadas',
          'Dashboard: personaliza UI con cards, gráficos históricos, control remoto',
          'Add-ons: Node-RED (visual programming), ESPHome (DIY devices)'
        ],
        example: 'Integra Philips Hue + Alexa + sensores Aqara en un solo dashboard',
        practice: 'Instala Home Assistant en VM virtual y conecta 3 dispositivos simulados'
      },
      {
        title: 'Automatizaciones Avanzadas con Node-RED',
        intro: 'Node-RED permite crear lógica compleja visual sin programar código.',
        concepts: [
          'Flow-based programming: arrastra nodos, conecta, deploy',
          'Nodos útiles: inject (trigger), switch (if/else), delay, debug',
          'Integración Home Assistant: enviar/recibir estados dispositivos',
          'Lógica compleja: "Si temperatura >25° Y hora >14:00 ENTONCES cerrar persianas + AC on"'
        ],
        example: 'Sistema riego: Si humedad_suelo <30% Y NO llueve → activar bomba 10min',
        practice: 'Crea flow que simule sistema anti-intrusión con múltiples sensores'
      },
      {
        title: 'Eficiencia Energética y Monitoreo',
        intro: 'Medir consumo permite identificar despilfarros y optimizar automáticamente.',
        concepts: [
          'Medidores: Shelly EM ($50) mide consumo total casa en tiempo real',
          'Enchufes medidores: conocer cuánto consume cada aparato',
          'Dashboards: gráficos históricos, identificar picos, comparar meses',
          'Automatizaciones ahorro: apagar standby noche, limitar calefacción, aprovechar tarifa valle'
        ],
        example: 'Descubrir que calentador agua viejo consume €40/mes → cambiar a solar ahorra €480/año',
        practice: 'Analiza factura eléctrica y propón 5 automatizaciones para reducir 20% consumo'
      },
      {
        title: 'Proyecto Final: Casa Inteligente Completa',
        intro: 'Diseña e implementa sistema domótico integral para vivienda real.',
        concepts: [
          'Planificación: listar necesidades por habitación, priorizar presupuesto',
          'Arquitectura: hub central (HA) + dispositivos por protocolo (WiFi, Zigbee)',
          'ROI: calcular ahorro energético, seguridad, tiempo ahorrado',
          'Escalabilidad: empezar pequeño, añadir dispositivos gradualmente'
        ],
        example: 'Apartamento 3 hab: $800 inicial → ahorro €300/año → amortización 2.7 años',
        practice: 'PROYECTO: Automatiza 3 habitaciones incluyendo iluminación, clima, seguridad. Documenta costos, instalación, automatizaciones creadas'
      }
    ]
  },
  'blockchain': {
    title: 'Blockchain y Criptomonedas',
    lessons: 8,
    content: [
      {
        title: '¿Qué es Blockchain?',
        intro: 'Blockchain es una base de datos distribuida e inmutable que revoluciona confianza digital.',
        concepts: [
          'Definición: cadena de bloques enlazados criptográficamente, distribuidos en red P2P',
          'Características: descentralizado, inmutable, transparente, seguro',
          'Casos de uso: criptomonedas (Bitcoin), contratos inteligentes (Ethereum), trazabilidad'
        ],
        example: 'Bitcoin: primera aplicación blockchain (2009), valor actual >$40,000',
        practice: 'Explica blockchain a alguien no técnico usando analogía del libro contable público'
      },
      {
        title: 'Criptografía y Hashing',
        intro: 'La criptografía asegura integridad y autenticidad de datos en blockchain.',
        concepts: [
          'Hash SHA-256: función unidireccional, mismo input = mismo output, cambio mínimo = hash totalmente diferente',
          'Criptografía asimétrica: par clave pública/privada, firmas digitales',
          'Merkle trees: estructura eficiente para verificar transacciones'
        ],
        example: 'Hash de "Hola": 185f8db32271fe25f561a6fc938b2e26... (cambiar a "hola" cambia todo el hash)',
        practice: 'Genera hash SHA-256 de tu nombre y verifica cómo cambio mínimo altera resultado'
      },
      {
        title: 'Bitcoin: La Primera Criptomoneda',
        intro: 'Bitcoin demostró que dinero digital descentralizado es posible sin intermediarios.',
        concepts: [
          'Creador: Satoshi Nakamoto (pseudónimo), whitepaper octubre 2008',
          'Minería: resolver problema matemático (Proof of Work) para crear nuevo bloque, recompensa actual 6.25 BTC',
          'Halving: recompensa se reduce a mitad cada 4 años, próximo 2024',
          'Oferta limitada: máximo 21 millones BTC, escasez digital'
        ],
        example: '1 BTC en 2010 = $0.08, en 2021 pico = $69,000 (aumento 862,400x)',
        practice: 'Crea wallet Bitcoin testnet y realiza transacción de prueba'
      },
      {
        title: 'Ethereum y Contratos Inteligentes',
        intro: 'Ethereum extendió blockchain para ejecutar código descentralizado (smart contracts).',
        concepts: [
          'Smart contracts: código que se ejecuta automáticamente cuando se cumplen condiciones',
          'Solidity: lenguaje de programación para Ethereum, similar a JavaScript',
          'Gas: tarifa que pagas por ejecutar operaciones, medida en Gwei',
          'EVM: Ethereum Virtual Machine ejecuta contratos en toda la red'
        ],
        example: 'Contrato escrow: retiene fondos hasta que ambas partes confirman, sin intermediario',
        practice: 'Escribe contrato Solidity básico que almacene y recupere número'
      },
      {
        title: 'DeFi: Finanzas Descentralizadas',
        intro: 'DeFi replica servicios financieros tradicionales sin bancos ni intermediarios.',
        concepts: [
          'DEX (exchanges descentralizados): Uniswap, PancakeSwap, intercambio P2P',
          'Lending/Borrowing: Aave, Compound, presta cripto y gana interés',
          'Stablecoins: USDC, DAI, atadas a dólar para reducir volatilidad',
          'Yield farming: mover cripto entre protocolos para maximizar rendimiento'
        ],
        example: 'Stake 1000 USDC en Aave → gana 5% APY vs 0.5% banco tradicional',
        practice: 'Compara APY de 3 protocolos DeFi diferentes para stablecoin'
      },
      {
        title: 'NFTs: Tokens No Fungibles',
        intro: 'NFTs representan propiedad única de activos digitales verificable en blockchain.',
        concepts: [
          'ERC-721: estándar Ethereum para NFTs únicos',
          'Metadata: JSON describe propiedades (nombre, imagen, atributos)',
          'Marketplaces: OpenSea, Rarible, LooksRare para comprar/vender',
          'Casos de uso: arte digital, coleccionables, gaming, música, real estate virtual'
        ],
        example: 'Beeple vendió NFT "Everydays" por $69 millones en Christie\'s',
        practice: 'Crea NFT de prueba en testnet con metadata e imagen IPFS'
      },
      {
        title: 'Consensus Mechanisms',
        intro: 'Mecanismos de consenso aseguran que red distribuida se ponga de acuerdo sin autoridad central.',
        concepts: [
          'Proof of Work (PoW): Bitcoin, mineros compiten resolviendo puzzle, alto consumo energético',
          'Proof of Stake (PoS): Ethereum 2.0, validadores apuestan tokens, 99.95% menos energía',
          'Delegated PoS: EOS, votan representantes que validan bloques',
          'Practical Byzantine Fault Tolerance: Hyperledger, voting entre nodos conocidos'
        ],
        example: 'Ethereum cambió de PoW a PoS (The Merge, septiembre 2022), consumo energía -99.95%',
        practice: 'Diagrama flujo de cómo funciona PoW vs PoS paso a paso'
      },
      {
        title: 'Proyecto: DApp Simple',
        intro: 'Desarrolla aplicación descentralizada completa con smart contract y frontend.',
        concepts: [
          'Stack: Solidity (backend) + Web3.js/Ethers.js + React (frontend)',
          'Hardhat/Truffle: frameworks para desarrollar y testear contratos',
          'MetaMask: wallet browser para interactuar con DApps',
          'Deployment: Infura/Alchemy como provider, deployar a testnet (Goerli, Sepolia)'
        ],
        example: 'Voting DApp: crear propuestas, votar con tokens, resultados transparentes',
        practice: 'PROYECTO: Crea DApp de votación simple con Solidity + React, deploy en testnet, documenta proceso completo'
      }
    ]
  },
  'iot': {
    title: 'Internet of Things (IoT)',
    lessons: 7,
    content: [
      {
        title: 'Introducción al IoT',
        intro: 'IoT conecta objetos físicos a internet para recopilar datos, automatizar y tomar decisiones inteligentes.',
        concepts: [
          'Definición: red de dispositivos con sensores, software, conectividad que intercambian datos',
          'Componentes: sensores (input) → microcontrolador (procesamiento) → actuadores (output) → comunicación',
          'Aplicaciones: smart home, ciudades inteligentes, agricultura, salud, industria 4.0'
        ],
        example: 'Termostato Nest: sensores temperatura + WiFi + cloud AI = ahorro energético automático',
        practice: 'Identifica 5 dispositivos IoT en tu entorno y describe su función'
      },
      {
        title: 'Sensores y Actuadores',
        intro: 'Sensores capturan datos del mundo físico, actuadores ejecutan acciones.',
        concepts: [
          'Sensores comunes: DHT22 (temp/humedad $3), PIR (movimiento $2), ultrasonido (distancia $5)',
          'Actuadores: relés (controlar 220V), servos (movimiento preciso), LEDs, bombas',
          'Comunicación: I2C (múltiples dispositivos 2 cables), SPI (rápido), UART (serial)'
        ],
        example: 'Sistema riego: sensor humedad suelo + relé + bomba = regar automáticamente cuando seco',
        practice: 'Conecta sensor DHT22 a Arduino y lee temperatura/humedad cada segundo'
      },
      {
        title: 'Microcontroladores: Arduino y ESP32',
        intro: 'Microcontroladores son el cerebro de proyectos IoT, ejecutan código y controlan componentes.',
        concepts: [
          'Arduino Uno: 16MHz, sin WiFi, ideal aprender, 14 GPIO, 6 analog, $25',
          'ESP32: 240MHz dual-core, WiFi+Bluetooth, 36 GPIO, $5 (mejor relación precio/potencia)',
          'Programación: Arduino IDE (C++), MicroPython, código estructurado setup() + loop()',
          'Shields: Ethernet, GSM, LoRa expanden funcionalidad'
        ],
        example: 'ESP32 lee sensor y envía datos a ThingSpeak cada 5min via WiFi',
        practice: 'Programa ESP32 para controlar LED con botón (digital input/output básico)'
      },
      {
        title: 'Protocolos de Comunicación IoT',
        intro: 'Protocolos eficientes permiten dispositivos comunicarse incluso con recursos limitados.',
        concepts: [
          'MQTT: ligero pub/sub, ideal IoT, broker (Mosquitto), topics jerárquicos',
          'HTTP/REST: estándar web, APIs simples, mayor overhead',
          'CoAP: HTTP para dispositivos limitados, UDP, confirmación',
          'LoRaWAN: largo alcance (km), bajo consumo, ideal sensores remotos'
        ],
        example: 'Sensor publica temperatura a broker MQTT topic "home/livingroom/temp", app subscribe y muestra',
        practice: 'Configura broker Mosquitto local y publica/subscribe mensajes con cliente'
      },
      {
        title: 'Plataformas Cloud IoT',
        intro: 'Plataformas cloud almacenan, procesan y visualizan datos IoT a escala.',
        concepts: [
          'AWS IoT Core: escalable, integra con Lambda, DynamoDB, ML',
          'Google Cloud IoT: analytics con BigQuery, ML con TensorFlow',
          'ThingSpeak: gratis hasta 3M mensajes/año, gráficos automáticos, MATLAB analytics',
          'Blynk: app móvil drag&drop, gratuito hasta 2 dispositivos'
        ],
        example: 'ESP32 envía datos a ThingSpeak → dashboard web muestra gráficos históricos',
        practice: 'Crea canal ThingSpeak y envía datos simulados desde ESP32'
      },
      {
        title: 'Seguridad en IoT',
        intro: 'Dispositivos IoT son frecuentes objetivos de ataques, seguridad es crítica.',
        concepts: [
          'Vulnerabilidades: contraseñas default, firmware desactualizado, tráfico sin cifrar',
          'Buenas prácticas: cambiar credenciales default, TLS/SSL para comunicación, actualizaciones OTA',
          'Autenticación: tokens JWT, OAuth para APIs, certificados X.509',
          'Segmentación red: VLAN separada para IoT, firewall restrictivo'
        ],
        example: 'Botnet Mirai infectó 600k dispositivos IoT con passwords default en 2016',
        practice: 'Lista 10 medidas seguridad para deployment IoT producción'
      },
      {
        title: 'Proyecto: Estación Meteorológica IoT',
        intro: 'Construye estación completa que mide, transmite y visualiza datos climáticos.',
        concepts: [
          'Hardware: ESP32 + DHT22 + sensor lluvia + panel solar + batería',
          'Software: leer sensores → enviar MQTT → Node-RED procesa → dashboard Grafana',
          'Features: alertas si temperatura extrema, predicción lluvia, históricos',
          'Deployment: caja IP65 resistente agua, montaje exterior'
        ],
        example: 'Estación completa: $50 hardware + cloud gratuito = datos climáticos 24/7',
        practice: 'PROYECTO: Construye estación con 3 sensores mínimo, envía datos cloud, crea dashboard con gráficos históricos'
      }
    ]
  }
};

function generateLessonContent(courseId: string, lessonNum: number, lessonData: any): string {
  const duration = 15 + lessonNum * 2; // Incrementa duración
  const xp = lessonNum <= 3 ? 50 : lessonNum <= 6 ? 75 : 100;
  
  return `  '${lessonNum}': {
    title: '${lessonData.title}',
    duration: '${duration} min',
    xp: ${xp},
    theory: {
      introduction: '${lessonData.intro.replace(/'/g, "\\'")}',
      sections: [
        {
          title: 'Conceptos clave',
          content: 'En esta lección aprenderás:',
          points: ${JSON.stringify(lessonData.concepts)}
        }
      ],
      example: {
        title: 'Ejemplo práctico',
        code: \`${lessonData.example}\`,
        explanation: 'Aplicación real de los conceptos vistos.'
      }
    },
    exercise: {
      title: 'Práctica: ${lessonData.title}',
      description: '${lessonData.practice.replace(/'/g, "\\'")}',
      initialCode: \`// Completa este ejercicio sobre ${lessonData.title.toLowerCase()}\n// ${lessonData.practice}\`,
      solution: \`// Solución propuesta para ${lessonData.title}\`,
      test: 'has_code',
      hints: ['Revisa los conceptos clave de la teoría', 'Consulta el ejemplo práctico', 'Experimenta con diferentes enfoques']
    }
  }`;
}

function generateCourseFile(courseId: string, courseData: any): string {
  const varName = courseId.replace(/-/g, '_');
  let content = `// Curso: ${courseData.title}\n// ${courseData.lessons} lecciones\n\n`;
  content += `export const ${varName}Content = {\n`;
  
  courseData.content.forEach((lesson: any, idx: number) => {
    content += generateLessonContent(courseId, idx + 1, lesson);
    if (idx < courseData.content.length - 1) {
      content += ',\n\n';
    }
  });
  
  content += '\n};\n';
  return content;
}

// Generar archivos
const dataDir = path.join(__dirname, '..', 'apps', 'web', 'src', 'data');

Object.keys(coursesContent).forEach(courseId => {
  const filePath = path.join(dataDir, `lessons-content-${courseId}.ts`);
  const content = generateCourseFile(courseId, coursesContent[courseId]);
  
  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`✓ Generado: lessons-content-${courseId}.ts`);
});

console.log('\n✅ Contenido generado exitosamente para 4 cursos');
console.log('📝 Archivos actualizados con contenido educativo real');
