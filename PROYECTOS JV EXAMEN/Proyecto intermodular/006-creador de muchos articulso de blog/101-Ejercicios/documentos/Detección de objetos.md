---
slug: deteccion-de-objetos
title: Detección de objetos (comoprogramar.es)
description: Aprende detección de objetos con Deep Learning. Comprende y aplica modelos como R-CNN, SSD y YOLO para localizar y clasificar objetos en imágenes y vídeo, con enfoque práctico y criterios profesionales.
keywords:
  - detección de objetos
  - object detection
  - yolo
  - r-cnn
  - ssd
  - vision artificial deep learning
level: Intermedio–Avanzado
duration_estimate: "45-65 horas"
prerequisites:
  - "Redes convolucionales (CNN)"
  - "Deep Learning con Python"
  - "Visión por computador desde cero"
audience:
  - "Estudiantes de inteligencia artificial"
  - "Científicos de datos"
  - "Ingenieros de visión artificial"
updated: 2025-12-26
---

# Detección de objetos

## Objetivos del curso

## Cómo usar este curso

## Ver no es solo clasificar: es localizar

---

# Unidad 1 — Qué es la detección de objetos

## 1.1 — Clasificación vs detección

### Lección 1.1.1 — Qué significa localizar un objeto
### Lección 1.1.2 — Bounding boxes
### Lección 1.1.3 — Casos de uso reales

## 1.2 — Retos fundamentales

### Lección 1.2.1 — Múltiples objetos
### Lección 1.2.2 — Escalas y oclusiones
### Lección 1.2.3 — Velocidad vs precisión

---

# Unidad 2 — Representación del problema

## 2.1 — Bounding boxes y anotaciones

### Lección 2.1.1 — Formatos de cajas
### Lección 2.1.2 — Ground truth
### Lección 2.1.3 — Datasets comunes

## 2.2 — Métricas específicas

### Lección 2.2.1 — Intersection over Union (IoU)
### Lección 2.2.2 — Precision y Recall en detección
### Lección 2.2.3 — mAP

---

# Unidad 3 — Enfoques históricos de detección

## 3.1 — Ventanas deslizantes

### Lección 3.1.1 — Idea básica
### Lección 3.1.2 — Coste computacional
### Lección 3.1.3 — Limitaciones

## 3.2 — Detectores clásicos

### Lección 3.2.1 — Haar cascades
### Lección 3.2.2 — HOG + SVM
### Lección 3.2.3 — Transición al Deep Learning

---

# Unidad 4 — Familia R-CNN (two-stage)

## 4.1 — R-CNN original

### Lección 4.1.1 — Propuestas de región
### Lección 4.1.2 — Clasificación por regiones
### Lección 4.1.3 — Costes y problemas

## 4.2 — Fast y Faster R-CNN

### Lección 4.2.1 — ROI pooling
### Lección 4.2.2 — Region Proposal Network (RPN)
### Lección 4.2.3 — Precisión vs velocidad

---

# Unidad 5 — Detectores de una sola etapa (one-stage)

## 5.1 — SSD

### Lección 5.1.1 — Default boxes
### Lección 5.1.2 — Detección multi-escala
### Lección 5.1.3 — Casos de uso

## 5.2 — YOLO

### Lección 5.2.1 — Detección como regresión
### Lección 5.2.2 — Grid y anchors
### Lección 5.2.3 — Velocidad en tiempo real

---

# Unidad 6 — Arquitectura interna de YOLO

## 6.1 — Backbone, neck y head

### Lección 6.1.1 — Extracción de características
### Lección 6.1.2 — Fusión multi-escala
### Lección 6.1.3 — Predicción final

## 6.2 — Predicciones del modelo

### Lección 6.2.1 — Coordenadas
### Lección 6.2.2 — Confianza
### Lección 6.2.3 — Clases

---

# Unidad 7 — Entrenamiento de detectores

## 7.1 — Preparación del dataset

### Lección 7.1.1 — Anotación de imágenes
### Lección 7.1.2 — Data augmentation
### Lección 7.1.3 — Balance de clases

## 7.2 — Función de pérdida

### Lección 7.2.1 — Pérdida de localización
### Lección 7.2.2 — Pérdida de clasificación
### Lección 7.2.3 — Trade-offs

---

# Unidad 8 — Postprocesado de detecciones

## 8.1 — Non-Maximum Suppression (NMS)

### Lección 8.1.1 — Eliminar duplicados
### Lección 8.1.2 — Umbral de IoU
### Lección 8.1.3 — Impacto en resultados

## 8.2 — Ajuste de umbrales

### Lección 8.2.1 — Confianza mínima
### Lección 8.2.2 — Recall vs precisión
### Lección 8.2.3 — Casos reales

---

# Unidad 9 — Detección en vídeo y tiempo real

## 9.1 — Procesamiento frame a frame

### Lección 9.1.1 — Latencia
### Lección 9.1.2 — FPS
### Lección 9.1.3 — Limitaciones prácticas

## 9.2 — Integración con OpenCV

### Lección 9.2.1 — Captura de vídeo
### Lección 9.2.2 — Visualización de detecciones
### Lección 9.2.3 — Optimización básica

---

# Unidad 10 — Transfer learning en detección

## 10.1 — Uso de modelos preentrenados

### Lección 10.1.1 — COCO y otros datasets
### Lección 10.1.2 — Fine-tuning
### Lección 10.1.3 — Congelación de capas

## 10.2 — Cuándo entrenar desde cero

### Lección 10.2.1 — Dominio muy específico
### Lección 10.2.2 — Volumen de datos
### Lección 10.2.3 — Coste computacional

---

# Unidad 11 — Evaluación y errores comunes

## 11.1 — Analizar fallos del detector

### Lección 11.1.1 — Falsos positivos
### Lección 11.1.2 — Falsos negativos
### Lección 11.1.3 — Errores de localización

## 11.2 — Buenas prácticas profesionales

### Lección 11.2.1 — Validación realista
### Lección 11.2.2 — Evitar sobreajuste visual
### Lección 11.2.3 — Interpretación responsable

---

# Unidad 12 — Mini-proyecto de detección de objetos

## 12.1 — Proyecto guiado completo

### Lección 12.1.1 — Definición del problema
### Lección 12.1.2 — Preparación del dataset
### Lección 12.1.3 — Entrenamiento del detector
### Lección 12.1.4 — Evaluación y ajustes
### Lección 12.1.5 — Detección en imágenes o vídeo

---

# Unidad 13 — Siguientes pasos

## 13.1 — Qué aprender después

### Lección 13.1.1 — Segmentación semántica
### Lección 13.1.2 — Tracking de objetos
### Lección 13.1.3 — Visión artificial en producción

## 13.2 — Ruta recomendada en comoprogramar.es

### Lección 13.2.1 — Redes convolucionales (CNN)
### Lección 13.2.2 — Visión por computador con Deep Learning
### Lección 13.2.3 — Flujo completo de un proyecto de IA

---

## Recursos recomendados

## Glosario (opcional)

## Créditos

> Última actualización: **2025-12-26**

