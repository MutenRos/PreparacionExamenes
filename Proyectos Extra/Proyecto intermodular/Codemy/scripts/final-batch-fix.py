#!/usr/bin/env python3
import re
import os
from pathlib import Path

data_dir = Path("apps/web/src/data")

# Template mejorado genérico
def get_enhanced_content(title, course_type):
    if 'python' in course_type or 'data' in course_type or 'ml' in course_type:
        lang = "python"
        code_example = f"""import pandas as pd
import numpy as np

# Sistema: {title}
class ProjectSystem:
    def __init__(self):
        self.data = None
        print(f"✅ Sistema {title} inicializado")
    
    def load_data(self):
        # Cargar y procesar datos
        self.data = pd.DataFrame({{'values': np.random.rand(100)}})
        print(f"📊 Datos cargados: {{len(self.data)}} registros")
    
    def analyze(self):
        # Análisis principal
        results = self.data.describe()
        print(f"\\n📈 RESULTADOS:\\n{{results}}")
        return results
    
    def run(self):
        self.load_data()
        results = self.analyze()
        print("\\n✅ Proyecto completado exitosamente")
        return results

# Ejecutar
if __name__ == "__main__":
    system = ProjectSystem()
    system.run()"""
    else:
        lang = "javascript"
        code_example = f"""// Sistema: {title}
class ProjectManager {{
    constructor() {{
        this.data = [];
        this.config = {{}};
        this.init();
    }}
    
    init() {{
        console.log('🚀 Sistema {title} inicializado');
        this.loadConfig();
    }}
    
    loadConfig() {{
        this.config = {{
            environment: 'production',
            version: '1.0.0',
            features: ['analytics', 'security', 'optimization']
        }};
        console.log('⚙️ Configuración lista');
    }}
    
    async processData() {{
        try {{
            // Procesamiento principal
            console.log('📊 Procesando datos...');
            this.data = await this.fetchData();
            const results = this.analyze();
            return results;
        }} catch (error) {{
            console.error('❌ Error:', error.message);
            throw error;
        }}
    }}
    
    async fetchData() {{
        // Simular carga de datos
        return new Promise(resolve => {{
            setTimeout(() => {{
                resolve([1, 2, 3, 4, 5]);
            }}, 100);
        }});
    }}
    
    analyze() {{
        console.log('📈 Analizando resultados...');
        const summary = {{
            total: this.data.length,
            sum: this.data.reduce((a, b) => a + b, 0),
            avg: this.data.reduce((a, b) => a + b, 0) / this.data.length
        }};
        console.log('✅ Análisis completado:', summary);
        return summary;
    }}
    
    async run() {{
        const results = await this.processData();
        console.log('🎉 Proyecto finalizado exitosamente');
        return results;
    }}
}}

// Ejecutar
const manager = new ProjectManager();
manager.run().then(results => console.log('Resultados:', results));"""
    
    return {
        "code": code_example,
        "description": f"""Desarrolla {title} aplicando los conceptos del curso:

✅ **Arquitectura Profesional**
   - Diseño modular y escalable
   - Separación de responsabilidades
   - Código limpio y documentado

✅ **Funcionalidad Completa**
   - Carga y procesamiento de datos
   - Lógica de negocio robusta
   - Manejo de errores

✅ **Best Practices**
   - Código idiomático
   - Tests y validación
   - Documentación clara

Demuestra dominio de los conceptos creando un proyecto production-ready.""",
        "initialCode": f"""// TODO: Implementar {title}
//
// Requisitos:
// 1. Estructura modular (clases/funciones)
// 2. Procesamiento de datos
// 3. Manejo de errores
// 4. Resultados/outputs claros
// 5. Código documentado
//
// Sigue el ejemplo de la teoría

console.log("Iniciando {title}...");""",
        "hints": [
            f"Revisa el ejemplo completo en la sección de teoría",
            "Implementa incrementalmente, probando cada parte",
            f"Aplica los conceptos aprendidos de {title}",
            "Documenta decisiones técnicas importantes",
            "Considera casos edge y validaciones",
            "Mantén el código limpio y legible"
        ]
    }

# Procesar archivos
files = list(data_dir.glob("lessons-content-*.ts"))
fixed = 0

for filepath in files:
    try:
        content = filepath.read_text(encoding='utf-8')
        
        # Buscar placeholders
        if 'console.log("Ejemplo de Proyecto:' not in content:
            continue
        
        # Determinar tipo de curso
        course_name = filepath.stem.replace('lessons-content-', '')
        course_type = course_name
        
        # Extraer título del proyecto
        match = re.search(r'console\.log\("Ejemplo de Proyecto: ([^"]+)"\)', content)
        if not match:
            continue
        
        project_title = match.group(1)
        enhanced = get_enhanced_content(project_title, course_type)
        
        # Reemplazar el bloque completo
        pattern = r'(code: `[^`]*console\.log\("Ejemplo de Proyecto:[^`]+)`)'
        replacement = f'code: `{enhanced["code"]}`'
        content = re.sub(pattern, replacement, content)
        
        # Mejorar description
        pattern_desc = r"description: 'Implementa Proyecto: [^']+en un proyecto práctico[^']*'"
        content = re.sub(pattern_desc, f"description: `{enhanced['description']}`", content)
        
        # Mejorar initialCode
        pattern_init = r'(initialCode: `[^`]*TODO: Implementa aquí[^`]*`)'
        content = re.sub(pattern_init, f'initialCode: `{enhanced["initialCode"]}`', content)
        
        # Mejorar hints
        hints_str = ',\n        '.join(f"'{h}'" for h in enhanced['hints'])
        pattern_hints = r"hints: \[[^\]]+\]"
        content = re.sub(pattern_hints, f"hints: [\n        {hints_str}\n      ]", content)
        
        # Incrementar XP a 150
        content = re.sub(r"(title: 'Proyecto:[^']+',\s+duration: '[^']+',\s+)xp: 100", r"\1xp: 150", content)
        
        # Guardar
        filepath.write_text(content, encoding='utf-8')
        fixed += 1
        print(f"✅ {filepath.name}")
        
    except Exception as e:
        print(f"❌ Error en {filepath.name}: {e}")

print(f"\n🎉 Completado: {fixed} archivos mejorados")
