---
slug: tokenizacion-embeddings-y-vectores
title: Tokenización, embeddings y vectores (comoprogramar.es)
description: Aprende cómo el texto se transforma en números mediante tokenización y embeddings. Comprende vectores semánticos, espacios vectoriales y similitud, base del NLP moderno, buscadores semánticos y modelos de lenguaje.
keywords:
  - tokenizacion nlp
  - embeddings
  - vectores semanticos
  - representacion del texto
  - nlp moderno
  - modelos de lenguaje fundamentos
level: Intermedio
duration_estimate: "35-50 horas"
prerequisites:
  - "NLP desde cero"
  - "Procesamiento de texto con Python"
  - "Álgebra lineal básica (recomendado)"
audience:
  - "Estudiantes de NLP"
  - "Científicos de datos"
  - "Desarrolladores de IA"
  - "Autodidactas"
updated: 2025-12-26
---

# Tokenización, embeddings y vectores

## Objetivos del curso

## Cómo usar este curso

## Convertir lenguaje en geometría

---

# Unidad 1 — Por qué el lenguaje debe convertirse en números

## 1.1 — Texto vs modelos matemáticos

### Lección 1.1.1 — Las máquinas no entienden palabras
### Lección 1.1.2 — Representaciones numéricas
### Lección 1.1.3 — Consecuencias prácticas

## 1.2 — Evolución histórica

### Lección 1.2.1 — Conteos y frecuencias
### Lección 1.2.2 — Vectores dispersos
### Lección 1.2.3 — Vectores densos

---

# Unidad 2 — Tokenización: dividir el lenguaje

## 2.1 — Qué es un token

### Lección 2.1.1 — Palabras como tokens
### Lección 2.1.2 — Subpalabras
### Lección 2.1.3 — Caracteres

## 2.2 — Problemas de tokenización

### Lección 2.2.1 — Idiomas flexivos (español)
### Lección 2.2.2 — Palabras desconocidas
### Lección 2.2.3 — Compromisos de diseño

---

# Unidad 3 — Tokenización moderna

## 3.1 — Subword tokenization

### Lección 3.1.1 — BPE (Byte Pair Encoding)
### Lección 3.1.2 — WordPiece
### Lección 3.1.3 — Unigram LM

## 3.2 — Tokenización en modelos reales

### Lección 3.2.1 — Tokens especiales
### Lección 3.2.2 — Longitud de secuencia
### Lección 3.2.3 — Impacto en rendimiento

---

# Unidad 4 — Vectores y espacios vectoriales

## 4.1 — Qué es un vector

### Lección 4.1.1 — Dimensión
### Lección 4.1.2 — Magnitud y dirección
### Lección 4.1.3 — Interpretación geométrica

## 4.2 — Espacios vectoriales semánticos

### Lección 4.2.1 — Proximidad semántica
### Lección 4.2.2 — Clusters de significado
### Lección 4.2.3 — Analogías vectoriales

---

# Unidad 5 — De tokens a vectores

## 5.1 — One-hot encoding

### Lección 5.1.1 — Representación básica
### Lección 5.1.2 — Alta dimensionalidad
### Lección 5.1.3 — Limitaciones graves

## 5.2 — Representaciones distribuidas

### Lección 5.2.1 — Idea clave de embeddings
### Lección 5.2.2 — Información distribuida
### Lección 5.2.3 — Ventajas frente a one-hot

---

# Unidad 6 — Word embeddings clásicos

## 6.1 — Word2Vec

### Lección 6.1.1 — CBOW
### Lección 6.1.2 — Skip-gram
### Lección 6.1.3 — Qué aprende realmente

## 6.2 — GloVe y FastText

### Lección 6.2.1 — Co-ocurrencias globales
### Lección 6.2.2 — Subpalabras en FastText
### Lección 6.2.3 — Casos de uso

---

# Unidad 7 — Embeddings contextuales

## 7.1 — El problema del contexto

### Lección 7.1.1 — Polisemia
### Lección 7.1.2 — Limitaciones de embeddings clásicos
### Lección 7.1.3 — Necesidad de contexto

## 7.2 — Embeddings basados en modelos

### Lección 7.2.1 — Representaciones dependientes del contexto
### Lección 7.2.2 — Tokens vs frases
### Lección 7.2.3 — Cambio de paradigma

---

# Unidad 8 — Similitud y distancia en espacios vectoriales

## 8.1 — Medidas de similitud

### Lección 8.1.1 — Cosine similarity
### Lección 8.1.2 — Distancia euclídea
### Lección 8.1.3 — Cuándo usar cada una

## 8.2 — Búsqueda semántica

### Lección 8.2.1 — Consultas por significado
### Lección 8.2.2 — Ranking de textos
### Lección 8.2.3 — Casos reales

---

# Unidad 9 — Frases, documentos y agregación

## 9.1 — De palabras a frases

### Lección 9.1.1 — Promedios de embeddings
### Lección 9.1.2 — Limitaciones
### Lección 9.1.3 — Estrategias simples

## 9.2 — Representación de documentos

### Lección 9.2.1 — Vectores de documento
### Lección 9.2.2 — Escalabilidad
### Lección 9.2.3 — Persistencia vectorial

---

# Unidad 10 — Preparar embeddings para producción

## 10.1 — Normalización y almacenamiento

### Lección 10.1.1 — Normalización de vectores
### Lección 10.1.2 — Índices vectoriales
### Lección 10.1.3 — Coste y memoria

## 10.2 — Errores comunes

### Lección 10.2.1 — Mezclar espacios incompatibles
### Lección 10.2.2 — Longitudes inconsistentes
### Lección 10.2.3 — Evaluación deficiente

---

# Unidad 11 — Sesgos y riesgos en embeddings

## 11.1 — Sesgos semánticos

### Lección 11.1.1 — Origen del sesgo
### Lección 11.1.2 — Ejemplos reales
### Lección 11.1.3 — Impacto social

## 11.2 — Mitigación básica

### Lección 11.2.1 — Análisis de embeddings
### Lección 11.2.2 — Filtrado de datos
### Lección 11.2.3 — Uso responsable

---

# Unidad 12 — Mini-proyecto de embeddings

## 12.1 — Proyecto guiado

### Lección 12.1.1 — Construcción de un vocabulario
### Lección 12.1.2 — Generación de embeddings
### Lección 12.1.3 — Búsqueda semántica básica
### Lección 12.1.4 — Evaluación de similitud
### Lección 12.1.5 — Conclusiones técnicas

---

# Unidad 13 — Siguientes pasos

## 13.1 — Qué aprender después

### Lección 13.1.1 — Modelos de lenguaje
### Lección 13.1.2 — Transformers
### Lección 13.1.3 — LLMs y sistemas RAG

## 13.2 — Ruta recomendada en comoprogramar.es

### Lección 13.2.1 — Modelos de lenguaje
### Lección 13.2.2 — NLP con Deep Learning
### Lección 13.2.3 — Arquitectura Transformer explicada

---

## Recursos recomendados

## Glosario (opcional)

## Créditos

> Última actualización: **2025-12-26**

