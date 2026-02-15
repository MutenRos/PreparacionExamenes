---
slug: segmentacion-de-imagenes
title: Segmentación de imágenes (comoprogramar.es)
description: Aprende segmentación de imágenes con visión por computador y Deep Learning. Domina segmentación semántica, de instancias y panóptica, comprendiendo los modelos, métricas y aplicaciones reales.
keywords:
  - segmentación de imágenes
  - image segmentation
  - segmentación semántica
  - segmentación de instancias
  - visión artificial deep learning
  - computer vision avanzada
level: Intermedio–Avanzado
duration_estimate: "45-65 horas"
prerequisites:
  - "Redes convolucionales (CNN)"
  - "Procesamiento digital de imágenes"
  - "Detección de objetos"
  - "Deep Learning con Python"
audience:
  - "Estudiantes de inteligencia artificial"
  - "Científicos de datos"
  - "Ingenieros de visión artificial"
updated: 2025-12-26
---

# Segmentación de imágenes

## Objetivos del curso

## Cómo usar este curso

## Ver no es suficiente: hay que delimitar cada píxel

---

# Unidad 1 — Qué es la segmentación de imágenes

## 1.1 — Segmentación vs detección

### Lección 1.1.1 — Clasificación, detección y segmentación
### Lección 1.1.2 — Segmentación como etiquetado por píxel
### Lección 1.1.3 — Casos de uso reales

## 1.2 — Tipos de segmentación

### Lección 1.2.1 — Segmentación semántica
### Lección 1.2.2 — Segmentación de instancias
### Lección 1.2.3 — Segmentación panóptica

---

# Unidad 2 — Representación del problema

## 2.1 — Máscaras de segmentación

### Lección 2.1.1 — Etiquetas por píxel
### Lección 2.1.2 — Formatos de anotación
### Lección 2.1.3 — Ground truth

## 2.2 — Métricas específicas

### Lección 2.2.1 — IoU por clase
### Lección 2.2.2 — Dice coefficient
### Lección 2.2.3 — Mean IoU

---

# Unidad 3 — Segmentación clásica (pre-Deep Learning)

## 3.1 — Segmentación por umbral

### Lección 3.1.1 — Umbralización global
### Lección 3.1.2 — Umbral adaptativo
### Lección 3.1.3 — Limitaciones

## 3.2 — Segmentación por regiones

### Lección 3.2.1 — Crecimiento de regiones
### Lección 3.2.2 — Watershed
### Lección 3.2.3 — Fragilidad del enfoque clásico

---

# Unidad 4 — Segmentación semántica con Deep Learning

## 4.1 — Idea clave de la segmentación semántica

### Lección 4.1.1 — Clasificación por píxel
### Lección 4.1.2 — Contexto espacial
### Lección 4.1.3 — Resolución vs semántica

## 4.2 — Arquitecturas fundamentales

### Lección 4.2.1 — Fully Convolutional Networks (FCN)
### Lección 4.2.2 — Encoder–Decoder
### Lección 4.2.3 — Skip connections

---

# Unidad 5 — U-Net y arquitecturas similares

## 5.1 — U-Net en profundidad

### Lección 5.1.1 — Contracción y expansión
### Lección 5.1.2 — Concatenación de features
### Lección 5.1.3 — Por qué funciona tan bien

## 5.2 — Variantes modernas

### Lección 5.2.1 — U-Net++
### Lección 5.2.2 — Attention U-Net
### Lección 5.2.3 — Casos de uso

---

# Unidad 6 — Segmentación de instancias

## 6.1 — Separar objetos individuales

### Lección 6.1.1 — Diferencia con segmentación semántica
### Lección 6.1.2 — Máscaras por objeto
### Lección 6.1.3 — Retos técnicos

## 6.2 — Mask R-CNN

### Lección 6.2.1 — Extensión de Faster R-CNN
### Lección 6.2.2 — Head de máscaras
### Lección 6.2.3 — Pipeline completo

---

# Unidad 7 — Segmentación panóptica

## 7.1 — Unificar semántica e instancias

### Lección 7.1.1 — Qué resuelve la segmentación panóptica
### Lección 7.1.2 — Clases “things” y “stuff”
### Lección 7.1.3 — Complejidad del enfoque

## 7.2 — Modelos representativos

### Lección 7.2.1 — Panoptic FPN
### Lección 7.2.2 — Modelos híbridos
### Lección 7.2.3 — Tendencias actuales

---

# Unidad 8 — Funciones de pérdida para segmentación

## 8.1 — Pérdidas por píxel

### Lección 8.1.1 — Cross-entropy
### Lección 8.1.2 — Weighted losses
### Lección 8.1.3 — Clases desbalanceadas

## 8.2 — Pérdidas basadas en solapamiento

### Lección 8.2.1 — Dice loss
### Lección 8.2.2 — Jaccard loss
### Lección 8.2.3 — Combinaciones prácticas

---

# Unidad 9 — Preparación de datos para segmentación

## 9.1 — Anotación de máscaras

### Lección 9.1.1 — Herramientas de etiquetado
### Lección 9.1.2 — Errores comunes
### Lección 9.1.3 — Coste del etiquetado

## 9.2 — Data augmentation específico

### Lección 9.2.1 — Transformaciones geométricas
### Lección 9.2.2 — Consistencia imagen–máscara
### Lección 9.2.3 — Buenas prácticas

---

# Unidad 10 — Entrenamiento y evaluación

## 10.1 — Entrenar modelos de segmentación

### Lección 10.1.1 — Resolución de entrada
### Lección 10.1.2 — Batch size y memoria
### Lección 10.1.3 — Curvas de entrenamiento

## 10.2 — Análisis de errores

### Lección 10.2.1 — Bordes mal definidos
### Lección 10.2.2 — Confusión entre clases
### Lección 10.2.3 — Impacto visual del error

---

# Unidad 11 — Segmentación en aplicaciones reales

## 11.1 — Segmentación médica

### Lección 11.1.1 — Órganos y tejidos
### Lección 11.1.2 — Sensibilidad al error
### Lección 11.1.3 — Validación clínica

## 11.2 — Otras aplicaciones

### Lección 11.2.1 — Conducción autónoma
### Lección 11.2.2 — Industria
### Lección 11.2.3 — Análisis satelital

---

# Unidad 12 — Mini-proyecto de segmentación de imágenes

## 12.1 — Proyecto guiado completo

### Lección 12.1.1 — Definición del problema
### Lección 12.1.2 — Preparación del dataset
### Lección 12.1.3 — Elección del modelo
### Lección 12.1.4 — Entrenamiento y evaluación
### Lección 12.1.5 — Visualización de resultados

---

# Unidad 13 — Siguientes pasos

## 13.1 — Qué aprender después

### Lección 13.1.1 — Segmentación en tiempo real
### Lección 13.1.2 — Visión artificial en producción
### Lección 13.1.3 — Modelos multimodales

## 13.2 — Ruta recomendada en comoprogramar.es

### Lección 13.2.1 — Detección de objetos
### Lección 13.2.2 — Visión por computador con Deep Learning
### Lección 13.2.3 — Flujo completo de un proyecto de IA

---

## Recursos recomendados

## Glosario (opcional)

## Créditos

> Última actualización: **2025-12-26**

