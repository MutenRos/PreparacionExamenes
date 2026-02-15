---
slug: modelos-de-lenguaje
title: Modelos de lenguaje (comoprogramar.es)
description: Aprende cómo funcionan los modelos de lenguaje. Comprende modelos probabilísticos, neuronales y contextuales para predecir, generar y evaluar texto, sentando las bases de los modelos de lenguaje modernos.
keywords:
  - modelos de lenguaje
  - language models
  - modelado del lenguaje
  - nlp avanzado
  - prediccion de texto
  - fundamentos llm
level: Intermedio–Avanzado
duration_estimate: "35-55 horas"
prerequisites:
  - "NLP desde cero"
  - "Tokenización, embeddings y vectores"
  - "Probabilidad y estadística para IA (recomendado)"
audience:
  - "Estudiantes de NLP"
  - "Científicos de datos"
  - "Desarrolladores de IA"
  - "Autodidactas avanzados"
updated: 2025-12-26
---

# Modelos de lenguaje

## Objetivos del curso

## Cómo usar este curso

## Modelar el lenguaje es modelar probabilidad

---

# Unidad 1 — Qué es un modelo de lenguaje

## 1.1 — Definición formal

### Lección 1.1.1 — Probabilidad de una secuencia
### Lección 1.1.2 — Predicción del siguiente token
### Lección 1.1.3 — Generación de texto

## 1.2 — Para qué sirven los modelos de lenguaje

### Lección 1.2.1 — Autocompletado
### Lección 1.2.2 — Corrección y resumen
### Lección 1.2.3 — Sistemas conversacionales

---

# Unidad 2 — Modelos de lenguaje clásicos

## 2.1 — Modelos n-gram

### Lección 2.1.1 — Probabilidades condicionales
### Lección 2.1.2 — Markov y contexto limitado
### Lección 2.1.3 — Explosión combinatoria

## 2.2 — Suavizado y generalización

### Lección 2.2.1 — Laplace
### Lección 2.2.2 — Kneser–Ney
### Lección 2.2.3 — Compromisos prácticos

---

# Unidad 3 — Evaluación de modelos de lenguaje

## 3.1 — Perplejidad

### Lección 3.1.1 — Qué mide la perplejidad
### Lección 3.1.2 — Interpretación intuitiva
### Lección 3.1.3 — Comparación entre modelos

## 3.2 — Límites de las métricas clásicas

### Lección 3.2.1 — Texto plausible pero incorrecto
### Lección 3.2.2 — Falta de semántica
### Lección 3.2.3 — Evaluación humana

---

# Unidad 4 — Transición a modelos neuronales

## 4.1 — Por qué los n-gram no escalan

### Lección 4.1.1 — Contexto corto
### Lección 4.1.2 — Sparsity
### Lección 4.1.3 — Generalización deficiente

## 4.2 — Idea del modelo neuronal

### Lección 4.2.1 — Embeddings compartidos
### Lección 4.2.2 — Aprender representaciones
### Lección 4.2.3 — Ventajas clave

---

# Unidad 5 — Modelos de lenguaje neuronales básicos

## 5.1 — Feedforward language models

### Lección 5.1.1 — Contexto fijo
### Lección 5.1.2 — Arquitectura general
### Lección 5.1.3 — Limitaciones

## 5.2 — Introducción a secuencias

### Lección 5.2.1 — Dependencias temporales
### Lección 5.2.2 — Orden importa
### Lección 5.2.3 — Necesidad de memoria

---

# Unidad 6 — Modelos recurrentes para lenguaje

## 6.1 — RNN como modelos de lenguaje

### Lección 6.1.1 — Estado oculto
### Lección 6.1.2 — Procesamiento secuencial
### Lección 6.1.3 — Costes computacionales

## 6.2 — LSTM y GRU (visión conceptual)

### Lección 6.2.1 — Problema del gradiente
### Lección 6.2.2 — Memoria a largo plazo
### Lección 6.2.3 — Mejora sobre RNN simples

---

# Unidad 7 — Entrenamiento de modelos de lenguaje

## 7.1 — Dataset y preparación

### Lección 7.1.1 — Corpus de texto
### Lección 7.1.2 — Ventanas de contexto
### Lección 7.1.3 — Tokenización consistente

## 7.2 — Función de pérdida

### Lección 7.2.1 — Cross-entropy
### Lección 7.2.2 — Teacher forcing
### Lección 7.2.3 — Señales de buen entrenamiento

---

# Unidad 8 — Generación de texto

## 8.1 — Decodificación básica

### Lección 8.1.1 — Greedy decoding
### Lección 8.1.2 — Beam search
### Lección 8.1.3 — Problemas comunes

## 8.2 — Control de diversidad

### Lección 8.2.1 — Temperature
### Lección 8.2.2 — Top-k
### Lección 8.2.3 — Top-p (nucleus sampling)

---

# Unidad 9 — Modelos de lenguaje y contexto

## 9.1 — Qué significa “entender contexto”

### Lección 9.1.1 — Dependencias largas
### Lección 9.1.2 — Coherencia global
### Lección 9.1.3 — Limitaciones prácticas

## 9.2 — Fallos típicos

### Lección 9.2.1 — Repetición
### Lección 9.2.2 — Contradicciones
### Lección 9.2.3 — Alucinaciones tempranas

---

# Unidad 10 — Sesgos y riesgos en modelos de lenguaje

## 10.1 — Origen de los sesgos

### Lección 10.1.1 — Datos de entrenamiento
### Lección 10.1.2 — Frecuencias dominantes
### Lección 10.1.3 — Amplificación estadística

## 10.2 — Uso responsable

### Lección 10.2.1 — Limitaciones explícitas
### Lección 10.2.2 — Validación humana
### Lección 10.2.3 — Casos sensibles

---

# Unidad 11 — Límites de los modelos pre-transformer

## 11.1 — Problemas de escalado

### Lección 11.1.1 — Procesamiento secuencial
### Lección 11.1.2 — Coste temporal
### Lección 11.1.3 — Memoria limitada

## 11.2 — Por qué surge el Transformer

### Lección 11.2.1 — Necesidad de paralelismo
### Lección 11.2.2 — Atención al contexto completo
### Lección 11.2.3 — Cambio de paradigma

---

# Unidad 12 — Mini-proyecto de modelo de lenguaje

## 12.1 — Proyecto guiado

### Lección 12.1.1 — Preparación del corpus
### Lección 12.1.2 — Entrenamiento de un modelo simple
### Lección 12.1.3 — Generación de texto
### Lección 12.1.4 — Evaluación básica
### Lección 12.1.5 — Análisis crítico

---

# Unidad 13 — Siguientes pasos

## 13.1 — Qué aprender después

### Lección 13.1.1 — Arquitectura Transformer explicada
### Lección 13.1.2 — LLMs y modelos fundacionales
### Lección 13.1.3 — Sistemas RAG

## 13.2 — Ruta recomendada en comoprogramar.es

### Lección 13.2.1 — Tokenización, embeddings y vectores
### Lección 13.2.2 — NLP con Deep Learning
### Lección 13.2.3 — Arquitectura Transformer explicada

---

## Recursos recomendados

## Glosario (opcional)

## Créditos

> Última actualización: **2025-12-26**

