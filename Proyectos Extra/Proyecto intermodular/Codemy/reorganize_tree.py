#!/usr/bin/env python3
"""
Reorganiza el skill tree en un flujo horizontal claro con tracks definidos.
"""

import re
import sys

# Definir tracks (filas horizontales) por categoría de tecnología
TRACKS = {
    # Python/Data Science track (Y=15%)
    'python': {
        'y': 15,
        'nodes': [
            'py-intro', 'py-variables', 'py-control', 'py-functions', 'py-classes', 
            'py-files', 'pandas', 'numpy', 'ml-intro', 'deep-learning', 'tensorflow'
        ]
    },
    # Web Frontend track (Y=35%)
    'web': {
        'y': 35,
        'nodes': [
            'html-intro', 'css-intro', 'js-intro', 'js-dom', 'js-async',
            'react-intro', 'react-hooks', 'nextjs', 'vue', 'angular'
        ]
    },
    # Backend/Database track (Y=55%)
    'backend': {
        'y': 55,
        'nodes': [
            'sql-intro', 'node-intro', 'express', 'postgresql', 'mongodb',
            'java-intro', 'java-oop', 'java-spring', 'django', 'flask'
        ]
    },
    # Systems/Low-level track (Y=75%)
    'systems': {
        'y': 75,
        'nodes': [
            'cpp-intro', 'cpp-pointers', 'cpp-oop', 'c-intro', 'rust',
            'arduino', 'iot', 'embedded', 'os', 'networking'
        ]
    },
    # DevOps/Cloud track (Y=90%)
    'devops': {
        'y': 90,
        'nodes': [
            'git', 'linux', 'docker', 'kubernetes', 'aws', 'azure', 'ci-cd',
            'terraform', 'jenkins', 'monitoring'
        ]
    },
    # Security/Blockchain track (Y=105%)
    'security': {
        'y': 105,
        'nodes': [
            'security-intro', 'cryptography', 'pentesting', 'blockchain',
            'solidity', 'web3', 'smart-contracts', 'defi', 'nfts'
        ]
    },
    # Mobile/Game Dev track (Y=120%)
    'special': {
        'y': 120,
        'nodes': [
            'react-native', 'flutter', 'kotlin', 'swift', 'unity',
            'godot', 'game-dev', 'graphics', 'ar-vr', 'mobile-design'
        ]
    },
}

# Niveles de progresión (X axis)
LEVELS = [5, 20, 35, 50, 65, 80, 95]

def find_track(node_id):
    """Encuentra en qué track debe estar un nodo."""
    for track_name, track_data in TRACKS.items():
        if node_id in track_data['nodes']:
            return track_data['y']
    # Default: fundamentos
    return 50

def calculate_x_level(prereqs, node_map):
    """Calcula el nivel X basado en los prerrequisitos."""
    if not prereqs or prereqs == ['fundamentals']:
        return LEVELS[1]  # 20%
    
    # Encontrar el nivel máximo de los prerrequisitos y sumar 1
    max_prereq_level = 0
    for prereq in prereqs:
        if prereq in node_map:
            prereq_x = node_map[prereq].get('x', LEVELS[0])
            try:
                prereq_level_idx = LEVELS.index(prereq_x)
                max_prereq_level = max(max_prereq_level, prereq_level_idx)
            except ValueError:
                pass
    
    next_level_idx = min(max_prereq_level + 1, len(LEVELS) - 1)
    return LEVELS[next_level_idx]

print("Script para reorganizar skill tree - ¡Ejecuta esto manualmente después de revisar los tracks!")
print("\nTracks definidos:")
for track_name, track_data in TRACKS.items():
    print(f"  {track_name} (Y={track_data['y']}%): {', '.join(track_data['nodes'][:5])}...")

print("\nNiveles X:", LEVELS)
print("\n¡Listo para implementar la reorganización!")
