#!/usr/bin/env python3
"""
Reorganiza TODAS las posiciones del skill tree a tracks horizontales.
"""
import re
import sys

# Definir tracks con posiciones (X, Y) - IDS CORRECTOS
TRACKS = {
    # Fundamentals
    'fundamentals': (5, 50),
    
    # Python/AI track (Y=12-22%)
    'py-intro': (20, 12), 'py-variables': (35, 12), 'py-control': (35, 17), 
    'py-functions': (50, 12), 'py-classes': (50, 17), 
    'numpy': (65, 12), 'pandas': (65, 17), 'matplotlib': (80, 12),
    'scikit-learn': (80, 17), 'pytorch': (95, 12), 'tensorflow': (95, 17),
    'nlp': (95, 22), 'computer-vision': (95, 27), 'llm': (95, 32),
    'master-ai': (95, 37),
    
    # Web track (Y=45-55%)
    'web-html': (20, 45), 'web-css': (35, 45), 'web-flexbox': (35, 50),
    'js-intro': (50, 45), 'js-dom': (50, 50), 'js-async': (50, 55),
    'js-advanced': (65, 45), 'typescript': (65, 50),
    'react': (80, 45), 'nextjs': (80, 50),
    'web-responsive': (35, 55),
    'master-fullstack': (95, 45),
    
    # Backend/Database track (Y=60-70%)
    'java-intro': (20, 60), 'java-oop': (35, 60), 'java-collections': (50, 60),
    'sql-intro': (35, 65), 'sql-queries': (50, 65),
    'nodejs': (65, 60), 'express': (65, 65), 'graphql': (80, 65),
    'mongodb': (80, 60), 'postgresql': (80, 67),
    
    # Systems/C++ track (Y=75-85%)
    'cpp-intro': (20, 75), 'cpp-oop': (35, 75), 'cpp-stl': (50, 75),
    'cpp-memory': (50, 80), 'cpp-advanced': (65, 75),
    'bridge-oop': (35, 82), 'bridge-algorithms': (50, 87),
    
    # Arduino/IoT/Robotics track (Y=90-100%)
    'arduino-intro': (35, 90), 'arduino-sensors': (50, 90), 'arduino-actuators': (50, 95),
    'iot': (65, 90), 'esp32': (65, 95),
    'robotics': (80, 90), 'ros': (80, 95), 'ai-robotics': (95, 90),
    'master-robotics': (95, 95),
    
    # DevOps/Cloud track (Y=105-115%)
    'git': (20, 105), 'linux': (35, 105), 'docker': (50, 105),
    'kubernetes': (65, 105), 'cicd': (65, 110),
    'aws': (80, 105), 'azure': (80, 110), 'gcp': (80, 115),
    'master-cloud': (95, 105),
    
    # Security/Blockchain track (Y=120-130%)
    'security': (50, 120), 'pentesting': (65, 120),
    'blockchain': (80, 120), 'web3': (80, 125),
    'master-security': (95, 120),
    
    # Mobile/Game track (Y=135-145%)
    'flutter': (65, 135), 'react-native': (65, 140),
    'unity': (80, 135), 'godot': (80, 140),
    'master-mobile': (95, 135), 'master-gamedev': (95, 140),
}

def main():
    filepath = 'apps/web/src/app/skill-tree-general/page.tsx'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Para cada nodo en TRACKS, reemplazar su posición
    changes_made = 0
    for node_id, (new_x, new_y) in TRACKS.items():
        # Pattern para encontrar este nodo específico
        pattern = rf"(id: '{node_id}',.*?position: \{{ x: )\d+, y: \d+( \}})"
        replacement = rf"\g<1>{new_x}, y: {new_y}\g<2>"
        
        new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
        
        if new_content != content:
            changes_made += 1
            content = new_content
    
    # Guardar el archivo modificado
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Reorganizados {changes_made} nodos en tracks horizontales")
    print(f"📊 Total posiciones definidas: {len(TRACKS)}")

if __name__ == '__main__':
    main()
