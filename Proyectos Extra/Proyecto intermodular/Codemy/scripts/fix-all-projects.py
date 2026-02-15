#!/usr/bin/env python3
import re
import os
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'apps' / 'web' / 'src' / 'data'

# Templates de proyectos por tipo de curso
project_templates = {
    'python': '''      example: {
        title: 'Proyecto Completo: {title}',
        code: `# {title} - Sistema Completo
import numpy as np
import pandas as pd

class DataAnalyzer:
    """Analizador de datos profesional"""
    
    def __init__(self):
        self.data = None
        print("✅ Sistema inicializado")
    
    def load_data(self, filepath):
        """Carga y valida datos"""
        self.data = pd.read_csv(filepath)
        print(f"📊 Datos cargados: {{self.data.shape}}")
        return self.data
    
    def analyze(self):
        """Análisis completo"""
        print("\\n📈 ANÁLISIS ESTADÍSTICO")
        print(f"Total registros: {{len(self.data)}}")
        print(f"Columnas: {{list(self.data.columns)}}")
        print(f"\\nEstadísticas:\\n{{self.data.describe()}}")
        
        # Análisis por columnas
        for col in self.data.select_dtypes(include=['float64', 'int64']).columns:
            print(f"\\n{{col}}:")
            print(f"  Media: {{self.data[col].mean():.2f}}")
            print(f"  Mediana: {{self.data[col].median():.2f}}")
            print(f"  Desv. Est: {{self.data[col].std():.2f}}")
    
    def generate_report(self):
        """Genera reporte ejecutivo"""
        print("\\n" + "="*50)
        print("REPORTE EJECUTIVO".center(50))
        print("="*50)
        self.analyze()
        print("\\n✅ Análisis completado")

# Uso del sistema
if __name__ == "__main__":
    analyzer = DataAnalyzer()
    # analyzer.load_data('dataset.csv')
    # analyzer.generate_report()
    print("🚀 Sistema listo para usar")`,
        explanation: 'Sistema completo que demuestra arquitectura profesional, procesamiento de datos, análisis estadístico y generación de reportes.'
      }''',
    
    'javascript': '''      example: {
        title: 'Proyecto Completo: {title}',
        code: `// {title} - Aplicación Completa
class AppManager {{
    constructor() {{
        this.data = [];
        this.config = {{}};
        this.init();
    }}
    
    init() {{
        console.log('🚀 Inicializando aplicación...');
        this.loadConfig();
        this.setupEventListeners();
    }}
    
    loadConfig() {{
        this.config = {{
            apiUrl: '/api/v1',
            timeout: 5000,
            retries: 3
        }};
        console.log('⚙️  Configuración cargada');
    }}
    
    async fetchData(endpoint) {{
        try {{
            const response = await fetch(this.config.apiUrl + endpoint);
            if (!response.ok) throw new Error('Network error');
            const data = await response.json();
            this.data = data;
            this.render();
            return data;
        }} catch (error) {{
            console.error('❌ Error:', error);
            this.handleError(error);
        }}
    }}
    
    setupEventListeners() {{
        document.addEventListener('DOMContentLoaded', () => {{
            console.log('📄 DOM listo');
            this.render();
        }});
    }}
    
    render() {{
        console.log('🎨 Renderizando UI...');
        // Renderizado de componentes
    }}
    
    handleError(error) {{
        console.error('Error:', error.message);
        // Manejo de errores
    }}
}}

// Inicializar aplicación
const app = new AppManager();
console.log('✅ Aplicación lista');`,
        explanation: 'Arquitectura completa con gestión de estado, llamadas asíncronas a APIs, event listeners y manejo robusto de errores.'
      }''',
    
    'java': '''      example: {
        title: 'Proyecto Completo: {title}',
        code: `// {title} - Sistema Completo
import java.util.*;
import java.util.stream.*;

public class SystemManager {{
    private List<Object> data;
    private Map<String, Object> config;
    
    public SystemManager() {{
        this.data = new ArrayList<>();
        this.config = new HashMap<>();
        initialize();
    }}
    
    private void initialize() {{
        System.out.println("🚀 Inicializando sistema...");
        loadConfiguration();
        System.out.println("✅ Sistema listo");
    }}
    
    private void loadConfiguration() {{
        config.put("version", "1.0.0");
        config.put("environment", "production");
        System.out.println("⚙️  Configuración cargada");
    }}
    
    public void processData() {{
        System.out.println("\\n📊 PROCESANDO DATOS");
        
        data.stream()
            .filter(Objects::nonNull)
            .forEach(item -> {{
                System.out.println("  Procesando: " + item);
            }});
        
        System.out.println("✅ Procesamiento completado");
    }}
    
    public void generateReport() {{
        System.out.println("\\n" + "=".repeat(50));
        System.out.println("REPORTE DEL SISTEMA");
        System.out.println("=".repeat(50));
        System.out.println("Total items: " + data.size());
        System.out.println("Configuración: " + config);
    }}
    
    public static void main(String[] args) {{
        SystemManager manager = new SystemManager();
        manager.processData();
        manager.generateReport();
        System.out.println("\\n🎉 Ejecución completada");
    }}
}}`,
        explanation: 'Sistema Java completo con POO, Collections Framework, Streams API y arquitectura profesional.'
      }'''
}

def get_course_type(filename):
    """Detecta el tipo de curso por el nombre del archivo"""
    name = filename.lower()
    if any(x in name for x in ['python', 'numpy', 'pandas', 'matplotlib', 'scikit', 'tensorflow', 'pytorch', 'nlp', 'ml', 'ai']):
        return 'python'
    elif any(x in name for x in ['java']):
        return 'java'
    elif any(x in name for x in ['js', 'javascript', 'react', 'node', 'express', 'next']):
        return 'javascript'
    else:
        return 'javascript'  # Default

def create_project_content(course_type, title):
    """Crea contenido de proyecto basado en el tipo"""
    template = project_templates.get(course_type, project_templates['javascript'])
    template = template.replace('{title}', title)
    
    initial_code = f'''      initialCode: `// TODO: Implementa {title}
// 
// Requisitos del proyecto:
// 1. Arquitectura modular y escalable
// 2. Manejo de errores robusto
// 3. Documentación clara del código
// 4. Tests básicos de funcionalidad
// 5. Código limpio siguiendo best practices
//
// Estructura sugerida:
// - Clase/Módulo principal
// - Métodos de inicialización
// - Procesamiento de datos
// - Generación de reportes
// - Manejo de errores
//
// ¡Éxito en tu proyecto final!

// Tu código aquí`'''
    
    description = f'''      description: `Desarrolla {title} integrando todos los conceptos del curso.

**Objetivos:**
✅ Aplicar técnicas avanzadas aprendidas
✅ Resolver un problema real de la industria  
✅ Implementar arquitectura profesional
✅ Código production-ready con documentación

**Requisitos técnicos:**
- Código modular y reutilizable
- Manejo de errores completo
- Comentarios y documentación
- Tests básicos de funcionalidad
- Seguir best practices

**Entregables:**
- Código fuente completo
- Documentación de uso
- Ejemplos de ejecución
- Casos de prueba

Demuestra tu dominio del curso con un proyecto que podrías incluir en tu portfolio profesional.`,'''
    
    return template, initial_code, description

def fix_project(content, filename):
    """Arregla un proyecto final genérico"""
    course_type = get_course_type(filename)
    
    # Buscar proyectos con contenido genérico
    pattern = r"(  '\d+':\s*\{\s*title:\s*'(Proyecto:[^']+)'[^}]*?)(example:\s*\{\s*title:[^}]*?code:\s*`[^`]*?console\.log\(\"Ejemplo de Proyecto:[^`]*?`[^}]*?\})"
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if not matches:
        return content, 0
    
    modified_content = content
    replacements = 0
    
    for match in reversed(matches):  # Reverse para no afectar índices
        project_title = match.group(2)
        
        # Crear nuevo contenido
        new_example, new_initial, new_description = create_project_content(course_type, project_title)
        
        # Encontrar el bloque completo del proyecto
        start = match.start()
        
        # Buscar el final del objeto (siguiente '  }' que cierra el proyecto)
        rest = modified_content[start:]
        end_pattern = r"(  \})\s*(?=\n\s*(?:'|};))"
        end_match = re.search(end_pattern, rest)
        
        if end_match:
            end = start + end_match.end()
            
            # Reconstruir el proyecto completo
            new_project = f'''  '{match.group(0).split("'")[1]}'¨ {{
    title: '{project_title}',
    duration: '45 min',
    xp: 150,
    theory: {{
      introduction: 'Proyecto final que integra todos los conceptos del curso en una aplicación real y completa.',
      sections: [
        {{
          title: 'Objetivos del Proyecto',
          content: 'Metas de aprendizaje:',
          points: [
            'Integrar todos los conceptos aprendidos',
            'Resolver un problema real de la industria',
            'Aplicar best practices profesionales',
            'Crear código production-ready'
          ]
        }},
        {{
          title: 'Arquitectura',
          content: 'Diseño del sistema:',
          points: [
            'Estructura modular y escalable',
            'Separación de responsabilidades',
            'Manejo de estado y datos',
            'Interfaces claras y documentadas'
          ]
        }}
      ],
{new_example}
    }},
    exercise: {{
      title: 'Proyecto Final: {project_title}',
{new_description}
{new_initial},
      solution: {new_example.split('code: ')[1].split(',')[0]},
      test: 'has_code',
      hints: [
        'Planifica la arquitectura antes de codificar',
        'Implementa incrementalmente y prueba cada parte',
        'Documenta decisiones técnicas importantes',
        'Sigue el ejemplo de la teoría como guía',
        'Considera casos edge y validaciones',
        'Refactoriza para mejorar la calidad del código'
      ]
    }}
  }}'''
            
            # Reemplazar
            modified_content = modified_content[:start] + new_project + modified_content[end:]
            replacements += 1
    
    return modified_content, replacements

# Procesar archivos
files = sorted([f for f in os.listdir(data_dir) if f.startswith('lessons-content-') and f.endswith('.ts')])
total_fixed = 0

print(f"🔍 Procesando {len(files)} archivos...\\n")

for filename in files:
    filepath = data_dir / filename
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene proyectos genéricos
        if 'console.log("Ejemplo de Proyecto:' in content:
            new_content, fixes = fix_project(content, filename)
            
            if fixes > 0:
                # Guardar
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                total_fixed += fixes
                print(f"✅ {filename}: {fixes} proyecto(s) mejorado(s)")
    
    except Exception as e:
        print(f"❌ Error en {filename}: {e}")

print(f"\\n🎉 Completado: {total_fixed} proyectos finales mejorados en total")
