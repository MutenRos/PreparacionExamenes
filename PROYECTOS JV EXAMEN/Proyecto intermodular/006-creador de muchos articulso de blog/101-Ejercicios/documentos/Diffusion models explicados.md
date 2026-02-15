---
slug: diffusion-models-explicados
title: Diffusion models explicados (comoprogramar.es)
description: Aprende cómo funcionan los modelos de difusión desde cero. Comprende el proceso de ruido y denoising, su base probabilística y por qué dominan la generación moderna de imágenes, audio y vídeo.
keywords:
  - diffusion models
  - modelos de difusion
  - stable diffusion fundamentos
  - generacion de imagenes ia
  - ia generativa moderna
  - deep learning generativo
level: Intermedio–Avanzado
duration_estimate: "40-60 horas"
prerequisites:
  - "Modelos generativos: GANs y VAEs"
  - "Deep Learning con Python"
  - "Probabilidad y estadística para IA (recomendado)"
audience:
  - "Estudiantes de IA"
  - "Científicos de datos"
  - "Ingenieros de Deep Learning"
  - "Autodidactas avanzados"
updated: 2025-12-26
---

# Diffusion models explicados

## Objetivos del curso

## Cómo usar este curso

## Generar es aprender a deshacer el ruido

---

# Unidad 1 — Por qué surgen los modelos de difusión

## 1.1 — Límites de GANs y VAEs

### Lección 1.1.1 — Inestabilidad en GANs
### Lección 1.1.2 — Compromisos en VAEs
### Lección 1.1.3 — Necesidad de un nuevo enfoque

## 1.2 — Idea central de la difusión

### Lección 1.2.1 — Añadir ruido progresivamente
### Lección 1.2.2 — Aprender a eliminar ruido
### Lección 1.2.3 — Intuición probabilística

---

# Unidad 2 — Proceso de difusión directa (forward)

## 2.1 — Añadir ruido paso a paso

### Lección 2.1.1 — Cadena de Markov
### Lección 2.1.2 — Ruido gaussiano
### Lección 2.1.3 — Pérdida de información

## 2.2 — Propiedades del proceso forward

### Lección 2.2.1 — Independencia del modelo
### Lección 2.2.2 — Destrucción controlada
### Lección 2.2.3 — Punto final: ruido puro

---

# Unidad 3 — Proceso inverso (denoising)

## 3.1 — Aprender a revertir el ruido

### Lección 3.1.1 — Modelo como eliminador de ruido
### Lección 3.1.2 — Predicción del ruido
### Lección 3.1.3 — Reconstrucción progresiva

## 3.2 — Intuición geométrica

### Lección 3.2.1 — Trayectoria en el espacio de datos
### Lección 3.2.2 — Generación paso a paso
### Lección 3.2.3 — Por qué es estable

---

# Unidad 4 — Fundamentos probabilísticos

## 4.1 — Distribuciones condicionadas

### Lección 4.1.1 — q(x_t | x_0)
### Lección 4.1.2 — p(x_{t-1} | x_t)
### Lección 4.1.3 — Aproximación aprendida

## 4.2 — Función de pérdida

### Lección 4.2.1 — Predicción de ruido ε
### Lección 4.2.2 — MSE como objetivo
### Lección 4.2.3 — Simplicidad engañosa

---

# Unidad 5 — Arquitectura típica de un diffusion model

## 5.1 — U-Net como backbone

### Lección 5.1.1 — Encoder–decoder
### Lección 5.1.2 — Skip connections
### Lección 5.1.3 — Multi-scale features

## 5.2 — Time embedding

### Lección 5.2.1 — Representar el paso temporal
### Lección 5.2.2 — Sincronización del ruido
### Lección 5.2.3 — Impacto en la calidad

---

# Unidad 6 — Sampling y velocidad

## 6.1 — Por qué es lento generar

### Lección 6.1.1 — Muchos pasos
### Lección 6.1.2 — Coste computacional
### Lección 6.1.3 — Trade-off calidad–tiempo

## 6.2 — Técnicas de aceleración

### Lección 6.2.1 — DDPM vs DDIM
### Lección 6.2.2 — Reducción de pasos
### Lección 6.2.3 — Impacto visual

---

# Unidad 7 — Condicionamiento en difusión

## 7.1 — Difusión condicional

### Lección 7.1.1 — Clases y etiquetas
### Lección 7.1.2 — Texto como condición
### Lección 7.1.3 — Control del resultado

## 7.2 — Classifier-free guidance

### Lección 7.2.1 — Mezcla guiada
### Lección 7.2.2 — Fuerza de la guía
### Lección 7.2.3 — Compromiso creatividad–fidelidad

---

# Unidad 8 — Texto a imagen: Stable Diffusion

## 8.1 — Latent diffusion models

### Lección 8.1.1 — Difusión en espacio latente
### Lección 8.1.2 — Autoencoder previo
### Lección 8.1.3 — Ahorro computacional

## 8.2 — Pipeline completo

### Lección 8.2.1 — Prompt → embedding
### Lección 8.2.2 — Denoising guiado
### Lección 8.2.3 — Decodificación final

---

# Unidad 9 — Comparación con otros modelos generativos

## 9.1 — Difusión vs GANs

### Lección 9.1.1 — Estabilidad
### Lección 9.1.2 — Diversidad
### Lección 9.1.3 — Control

## 9.2 — Difusión vs VAEs

### Lección 9.2.1 — Calidad visual
### Lección 9.2.2 — Interpretabilidad
### Lección 9.2.3 — Coste computacional

---

# Unidad 10 — Evaluación de modelos de difusión

## 10.1 — Métricas habituales

### Lección 10.1.1 — FID
### Lección 10.1.2 — IS
### Lección 10.1.3 — Limitaciones de métricas

## 10.2 — Evaluación humana

### Lección 10.2.1 — Realismo
### Lección 10.2.2 — Diversidad
### Lección 10.2.3 — Sesgos perceptivos

---

# Unidad 11 — Riesgos y ética

## 11.1 — Riesgos técnicos

### Lección 11.1.1 — Generación de deepfakes
### Lección 11.1.2 — Memorización de datos
### Lección 11.1.3 — Uso indebido

## 11.2 — Uso responsable

### Lección 11.2.1 — Transparencia
### Lección 11.2.2 — Límites de uso
### Lección 11.2.3 — Buenas prácticas

---

# Unidad 12 — Mini-proyecto con diffusion models

## 12.1 — Proyecto guiado completo

### Lección 12.1.1 — Preparación del dataset
### Lección 12.1.2 — Entrenamiento de un modelo simple
### Lección 12.1.3 — Generación de imágenes
### Lección 12.1.4 — Ajuste de parámetros
### Lección 12.1.5 — Análisis de resultados

---

# Unidad 13 — Siguientes pasos

## 13.1 — Qué aprender después

### Lección 13.1.1 — Fine-tuning de diffusion models
### Lección 13.1.2 — ControlNet y control estructural
### Lección 13.1.3 — Generación multimodal

## 13.2 — Ruta recomendada en comoprogramar.es

### Lección 13.2.1 — Modelos generativos: GANs y VAEs
### Lección 13.2.2 — Generación de imágenes con IA
### Lección 13.2.3 — IA generativa avanzada

---

## Recursos recomendados

## Glosario (opcional)

## Créditos

> Última actualización: **2025-12-26**

