#!/bin/bash
# Script para contar archivos por procesar por categoría

DATA_DIR="apps/web/src/data"

echo "📊 ANÁLISIS DE PROYECTOS POR CATEGORÍA"
echo

# Data Science/ML
echo "🔬 Data Science/ML:"
grep -l 'console.log("Ejemplo de Proyecto:' $DATA_DIR/lessons-content-{pandas,matplotlib,scikit-learn,nlp,tensorflow,pytorch,llm,computer-vision}.ts 2>/dev/null | wc -l
echo "  pandas ✅, numpy ✅, matplotlib, scikit-learn, nlp, tensorflow, pytorch, llm, computer-vision"
echo

# JavaScript/Web
echo "🌐 JavaScript/Web:"  
grep -l 'console.log("Ejemplo de Proyecto:' $DATA_DIR/lessons-content-{express,react-native,flutter,node}.ts 2>/dev/null | wc -l
echo "  express, react-native, flutter, node"
echo

# Java
echo "☕ Java:"
grep -l 'console.log("Ejemplo de Proyecto:' $DATA_DIR/lessons-content-java-*.ts 2>/dev/null | wc -l  
echo "  java-collections, java-exceptions, java-fileio, java-jdbc, java-spring, java-threads"
echo

# Total general
echo "📦 TOTAL PENDIENTES:"
grep -l 'console.log("Ejemplo de Proyecto:' $DATA_DIR/lessons-content-*.ts 2>/dev/null | wc -l
