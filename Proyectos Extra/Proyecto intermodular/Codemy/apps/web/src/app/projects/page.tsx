'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, ArrowRight, Code2, Download, CheckCircle2, Target, Trophy, FileText } from 'lucide-react';

interface Project {
  id: string;
  title: string;
  description: string;
  courseId: string;
  courseName: string;
  icon: string;
  difficulty: 'Principiante' | 'Intermedio' | 'Avanzado';
  estimatedTime: string;
  xp: number;
  requirements: string[];
  objectives: string[];
  features: string[];
  rubric: {
    category: string;
    excellent: string;
    good: string;
    needsWork: string;
  }[];
  starterCode: string;
}

const projects: Project[] = [
  {
    id: 'agenda-crud',
    title: 'Agenda de Contactos CRUD',
    description: 'Sistema completo de gestión de contactos con operaciones Create, Read, Update y Delete. Aplica funciones, manejo de archivos y estructuras de datos.',
    courseId: 'py-functions',
    courseName: 'Funciones en Python',
    icon: '📇',
    difficulty: 'Intermedio',
    estimatedTime: '2-3 horas',
    xp: 200,
    requirements: [
      'Completar curso de Funciones',
      'Conocer estructuras de control (if, for, while)',
      'Entender lectura/escritura de archivos básica',
      'Dominar listas y diccionarios',
    ],
    objectives: [
      'Crear funciones modulares y reutilizables',
      'Implementar menú interactivo con bucles',
      'Gestionar datos con archivos de texto',
      'Validar entrada del usuario',
      'Manejar errores apropiadamente',
    ],
    features: [
      '✅ Agregar nuevo contacto (nombre, teléfono, email)',
      '✅ Ver lista completa de contactos',
      '✅ Buscar contacto por nombre',
      '✅ Editar contacto existente',
      '✅ Eliminar contacto',
      '✅ Guardar automáticamente en archivo',
      '✅ Validación de datos (email, teléfono)',
      '✅ Interfaz de menú clara y amigable',
    ],
    rubric: [
      {
        category: 'Funcionalidad (40%)',
        excellent: 'Todas las operaciones CRUD funcionan perfectamente. Validación robusta.',
        good: 'La mayoría de operaciones funcionan. Validación básica presente.',
        needsWork: 'Operaciones incompletas o con errores. Sin validación.',
      },
      {
        category: 'Código (30%)',
        excellent: 'Código limpio, funciones bien organizadas, nombres descriptivos.',
        good: 'Código funcional pero puede mejorar organización.',
        needsWork: 'Código desorganizado, difícil de entender.',
      },
      {
        category: 'Manejo de Archivos (20%)',
        excellent: 'Persistencia robusta, maneja errores de archivo correctamente.',
        good: 'Guarda y carga datos pero falta manejo de errores.',
        needsWork: 'Problemas al guardar/cargar o pierde datos.',
      },
      {
        category: 'Interfaz (10%)',
        excellent: 'Menú claro, mensajes informativos, fácil de usar.',
        good: 'Menú funcional pero puede mejorar claridad.',
        needsWork: 'Interfaz confusa o poco intuitiva.',
      },
    ],
    starterCode: `# Agenda de Contactos CRUD
# Tu nombre: _______________
# Fecha: _______________

import os

# Constantes
ARCHIVO_CONTACTOS = "contactos.txt"
SEPARADOR = "|"

def cargar_contactos():
    """Carga contactos desde el archivo"""
    contactos = []
    if os.path.exists(ARCHIVO_CONTACTOS):
        with open(ARCHIVO_CONTACTOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                # TODO: Implementar carga de contactos
                pass
    return contactos

def guardar_contactos(contactos):
    """Guarda contactos en el archivo"""
    # TODO: Implementar guardado de contactos
    pass

def agregar_contacto(contactos):
    """Agrega un nuevo contacto"""
    print("\\n=== AGREGAR CONTACTO ===")
    # TODO: Implementar agregar contacto
    pass

def ver_contactos(contactos):
    """Muestra todos los contactos"""
    print("\\n=== LISTA DE CONTACTOS ===")
    # TODO: Implementar visualización de contactos
    pass

def buscar_contacto(contactos):
    """Busca un contacto por nombre"""
    print("\\n=== BUSCAR CONTACTO ===")
    # TODO: Implementar búsqueda de contacto
    pass

def editar_contacto(contactos):
    """Edita un contacto existente"""
    print("\\n=== EDITAR CONTACTO ===")
    # TODO: Implementar edición de contacto
    pass

def eliminar_contacto(contactos):
    """Elimina un contacto"""
    print("\\n=== ELIMINAR CONTACTO ===")
    # TODO: Implementar eliminación de contacto
    pass

def mostrar_menu():
    """Muestra el menú principal"""
    print("\\n" + "="*40)
    print("📇 AGENDA DE CONTACTOS")
    print("="*40)
    print("1. Ver todos los contactos")
    print("2. Agregar contacto")
    print("3. Buscar contacto")
    print("4. Editar contacto")
    print("5. Eliminar contacto")
    print("6. Salir")
    print("="*40)

def main():
    """Función principal"""
    contactos = cargar_contactos()
    
    while True:
        mostrar_menu()
        opcion = input("\\nSelecciona una opción: ")
        
        if opcion == "1":
            ver_contactos(contactos)
        elif opcion == "2":
            agregar_contacto(contactos)
        elif opcion == "3":
            buscar_contacto(contactos)
        elif opcion == "4":
            editar_contacto(contactos)
        elif opcion == "5":
            eliminar_contacto(contactos)
        elif opcion == "6":
            print("\\n¡Hasta luego! 👋")
            break
        else:
            print("\\n❌ Opción inválida. Intenta de nuevo.")
        
        input("\\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
`,
  },
  {
    id: 'sistema-clientes',
    title: 'Sistema de Gestión de Clientes',
    description: 'Aplicación orientada a objetos para gestionar clientes de una tienda. Implementa clases, encapsulación, métodos y persistencia de datos.',
    courseId: 'py-classes',
    courseName: 'Clases y POO',
    icon: '👥',
    difficulty: 'Intermedio',
    estimatedTime: '3-4 horas',
    xp: 250,
    requirements: [
      'Completar curso de Clases y POO',
      'Dominar conceptos de encapsulación',
      'Conocer métodos especiales (__init__, __str__)',
      'Entender atributos privados y públicos',
    ],
    objectives: [
      'Diseñar clases con atributos y métodos apropiados',
      'Aplicar encapsulación para proteger datos',
      'Implementar métodos especiales',
      'Gestionar colecciones de objetos',
      'Persistir datos de objetos en archivos',
    ],
    features: [
      '✅ Clase Cliente con nombre, email, historial de compras',
      '✅ Agregar compras a un cliente',
      '✅ Calcular total gastado',
      '✅ Determinar status VIP (>1000€)',
      '✅ Ver estadísticas del cliente',
      '✅ Guardar/cargar clientes desde archivo',
      '✅ Sistema de descuentos para VIP',
      '✅ Ranking de mejores clientes',
    ],
    rubric: [
      {
        category: 'Diseño POO (40%)',
        excellent: 'Clases bien diseñadas, encapsulación correcta, métodos coherentes.',
        good: 'Estructura de clases funcional pero puede mejorar diseño.',
        needsWork: 'Clases mal diseñadas o sin usar POO apropiadamente.',
      },
      {
        category: 'Implementación (30%)',
        excellent: 'Todos los métodos funcionan, validaciones presentes, código limpio.',
        good: 'Funcionalidad básica completa, falta algunas validaciones.',
        needsWork: 'Funcionalidad incompleta o con errores significativos.',
      },
      {
        category: 'Encapsulación (20%)',
        excellent: 'Usa atributos privados, getters/setters apropiados, datos protegidos.',
        good: 'Alguna encapsulación pero inconsistente.',
        needsWork: 'No usa encapsulación o todos los atributos públicos.',
      },
      {
        category: 'Persistencia (10%)',
        excellent: 'Guarda y carga objetos correctamente, maneja errores.',
        good: 'Persistencia básica funciona pero puede mejorar.',
        needsWork: 'No persiste datos o pierde información.',
      },
    ],
    starterCode: `# Sistema de Gestión de Clientes
# Tu nombre: _______________
# Fecha: _______________

import json
import os
from datetime import datetime

class Cliente:
    """Clase para representar un cliente de la tienda"""
    
    def __init__(self, nombre, email):
        """Inicializa un cliente"""
        # TODO: Implementar constructor
        # Atributos sugeridos:
        # - self.nombre (público)
        # - self.__email (privado)
        # - self.__compras (lista privada)
        # - self.__total_gastado (privado)
        # - self.__fecha_registro (privado)
        pass
    
    def agregar_compra(self, producto, precio):
        """Agrega una compra al historial"""
        # TODO: Implementar agregar compra
        # Validar que precio > 0
        # Agregar a lista de compras
        # Actualizar total gastado
        pass
    
    def obtener_total(self):
        """Retorna el total gastado"""
        # TODO: Implementar getter
        pass
    
    def es_vip(self):
        """Determina si el cliente es VIP (>1000€)"""
        # TODO: Implementar lógica VIP
        pass
    
    def aplicar_descuento(self, precio):
        """Aplica descuento si es VIP (15%)"""
        # TODO: Implementar descuento
        pass
    
    def ver_historial(self):
        """Muestra el historial de compras"""
        # TODO: Implementar visualización
        pass
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del cliente"""
        # TODO: Calcular:
        # - Número de compras
        # - Compra promedio
        # - Compra más alta
        # - Status (VIP o Regular)
        pass
    
    def __str__(self):
        """Representación en string"""
        # TODO: Implementar __str__
        pass
    
    def to_dict(self):
        """Convierte el cliente a diccionario para JSON"""
        # TODO: Implementar serialización
        pass
    
    @staticmethod
    def from_dict(data):
        """Crea un cliente desde diccionario"""
        # TODO: Implementar deserialización
        pass

class SistemaClientes:
    """Clase para gestionar múltiples clientes"""
    
    def __init__(self, archivo="clientes.json"):
        """Inicializa el sistema"""
        self.archivo = archivo
        self.clientes = []
        self.cargar_clientes()
    
    def cargar_clientes(self):
        """Carga clientes desde archivo"""
        # TODO: Implementar carga desde JSON
        pass
    
    def guardar_clientes(self):
        """Guarda clientes en archivo"""
        # TODO: Implementar guardado en JSON
        pass
    
    def agregar_cliente(self, nombre, email):
        """Agrega un nuevo cliente"""
        # TODO: Implementar agregar cliente
        pass
    
    def buscar_cliente(self, nombre):
        """Busca un cliente por nombre"""
        # TODO: Implementar búsqueda
        pass
    
    def ver_todos_clientes(self):
        """Muestra todos los clientes"""
        # TODO: Implementar visualización
        pass
    
    def ranking_clientes(self):
        """Muestra ranking de clientes por gastos"""
        # TODO: Ordenar clientes por total gastado
        pass
    
    def estadisticas_generales(self):
        """Muestra estadísticas del sistema"""
        # TODO: Implementar estadísticas:
        # - Total clientes
        # - Clientes VIP
        # - Total facturado
        # - Cliente con más gastos
        pass

def mostrar_menu():
    """Muestra el menú principal"""
    print("\\n" + "="*50)
    print("👥 SISTEMA DE GESTIÓN DE CLIENTES")
    print("="*50)
    print("1. Ver todos los clientes")
    print("2. Agregar nuevo cliente")
    print("3. Buscar cliente")
    print("4. Agregar compra a cliente")
    print("5. Ver historial de cliente")
    print("6. Ranking de clientes")
    print("7. Estadísticas generales")
    print("8. Salir")
    print("="*50)

def main():
    """Función principal"""
    sistema = SistemaClientes()
    
    while True:
        mostrar_menu()
        opcion = input("\\nSelecciona una opción: ")
        
        # TODO: Implementar manejo de opciones
        
        if opcion == "8":
            sistema.guardar_clientes()
            print("\\n✅ Datos guardados. ¡Hasta luego! 👋")
            break
        
        input("\\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
`,
  },
  {
    id: 'lista-compra',
    title: 'Lista de Compra Inteligente',
    description: 'Aplicación completa para gestionar listas de compra con múltiples categorías, persistencia, estadísticas y exportación a diferentes formatos.',
    courseId: 'py-files',
    courseName: 'Trabajo con Archivos',
    icon: '🛒',
    difficulty: 'Avanzado',
    estimatedTime: '4-5 horas',
    xp: 300,
    requirements: [
      'Completar curso de Archivos',
      'Dominar lectura/escritura de archivos',
      'Conocer manejo de excepciones',
      'Entender módulos os y datetime',
    ],
    objectives: [
      'Implementar múltiples formatos de archivo (txt, csv, json)',
      'Crear sistema robusto de manejo de errores',
      'Gestionar directorios y rutas',
      'Implementar funciones de backup y restauración',
      'Generar reportes y estadísticas',
    ],
    features: [
      '✅ Crear múltiples listas de compra',
      '✅ Agregar items con cantidad, precio y categoría',
      '✅ Marcar items como comprados',
      '✅ Calcular total de la lista',
      '✅ Filtrar por categoría',
      '✅ Exportar a TXT, CSV y JSON',
      '✅ Generar reporte de gastos',
      '✅ Sistema de backup automático',
      '✅ Historial de compras',
    ],
    rubric: [
      {
        category: 'Manejo de Archivos (40%)',
        excellent: 'Múltiples formatos, robusto manejo de errores, backup automático.',
        good: 'Guardado y carga funciona, manejo básico de errores.',
        needsWork: 'Problemas con archivos o pierde datos.',
      },
      {
        category: 'Funcionalidad (30%)',
        excellent: 'Todas las características implementadas y funcionando perfectamente.',
        good: 'Funcionalidad principal completa, faltan algunas características.',
        needsWork: 'Funcionalidad incompleta o con muchos errores.',
      },
      {
        category: 'Robustez (20%)',
        excellent: 'Manejo excepcional de errores, validaciones completas, no crashea.',
        good: 'Maneja errores comunes, algunas validaciones presentes.',
        needsWork: 'Crashea fácilmente, sin manejo de errores.',
      },
      {
        category: 'Exportación (10%)',
        excellent: 'Exporta a múltiples formatos correctamente, datos bien formateados.',
        good: 'Exporta a al menos un formato correctamente.',
        needsWork: 'No exporta o formato incorrecto.',
      },
    ],
    starterCode: `# Lista de Compra Inteligente
# Tu nombre: _______________
# Fecha: _______________

import os
import json
import csv
from datetime import datetime

# Constantes
DIRECTORIO_DATOS = "datos_compras"
ARCHIVO_LISTAS = os.path.join(DIRECTORIO_DATOS, "listas.json")
DIRECTORIO_BACKUPS = os.path.join(DIRECTORIO_DATOS, "backups")

# Categorías disponibles
CATEGORIAS = ["Frutas", "Verduras", "Lácteos", "Carnes", "Panadería", "Bebidas", "Limpieza", "Otros"]

def inicializar_sistema():
    """Crea directorios necesarios"""
    # TODO: Crear DIRECTORIO_DATOS y DIRECTORIO_BACKUPS si no existen
    pass

def cargar_listas():
    """Carga todas las listas desde JSON"""
    # TODO: Implementar carga desde archivo JSON
    # Manejar caso de archivo inexistente
    # Retornar diccionario de listas
    pass

def guardar_listas(listas):
    """Guarda todas las listas en JSON"""
    # TODO: Implementar guardado en JSON
    # Usar indent=2 para formato legible
    pass

def crear_backup():
    """Crea un backup de los datos"""
    # TODO: Copiar archivo actual a carpeta backups
    # Nombre del backup: listas_backup_YYYYMMDD_HHMMSS.json
    pass

def crear_lista(listas):
    """Crea una nueva lista de compra"""
    print("\\n=== CREAR LISTA ===")
    # TODO: Implementar creación de lista
    # Estructura sugerida:
    # {
    #   "nombre": str,
    #   "fecha_creacion": str,
    #   "items": [],
    #   "completada": bool
    # }
    pass

def agregar_item(listas):
    """Agrega un item a una lista"""
    print("\\n=== AGREGAR ITEM ===")
    # TODO: Implementar agregar item
    # Estructura de item:
    # {
    #   "nombre": str,
    #   "cantidad": int,
    #   "precio": float,
    #   "categoria": str,
    #   "comprado": bool
    # }
    pass

def ver_lista(listas):
    """Muestra una lista con todos sus items"""
    print("\\n=== VER LISTA ===")
    # TODO: Implementar visualización
    # Mostrar items organizados por categoría
    # Calcular total
    pass

def marcar_comprado(listas):
    """Marca un item como comprado"""
    print("\\n=== MARCAR ITEM ===")
    # TODO: Implementar marcar como comprado
    pass

def estadisticas_lista(listas):
    """Muestra estadísticas de una lista"""
    print("\\n=== ESTADÍSTICAS ===")
    # TODO: Implementar estadísticas:
    # - Total de items
    # - Items comprados vs pendientes
    # - Total gastado vs presupuestado
    # - Categoría con más items
    # - Categoría con más gasto
    pass

def exportar_txt(listas):
    """Exporta una lista a archivo TXT"""
    print("\\n=== EXPORTAR A TXT ===")
    # TODO: Implementar exportación a TXT
    # Formato legible para humanos
    pass

def exportar_csv(listas):
    """Exporta una lista a archivo CSV"""
    print("\\n=== EXPORTAR A CSV ===")
    # TODO: Implementar exportación a CSV
    # Columnas: nombre, cantidad, precio, categoria, comprado
    pass

def generar_reporte_gastos(listas):
    """Genera un reporte de gastos totales"""
    print("\\n=== REPORTE DE GASTOS ===")
    # TODO: Implementar reporte:
    # - Gastos por lista
    # - Gastos por categoría
    # - Total general
    # - Guardar en archivo de texto
    pass

def buscar_items(listas):
    """Busca items en todas las listas"""
    print("\\n=== BUSCAR ITEMS ===")
    # TODO: Implementar búsqueda por nombre
    # Mostrar en qué lista está y su estado
    pass

def mostrar_menu():
    """Muestra el menú principal"""
    print("\\n" + "="*50)
    print("🛒 LISTA DE COMPRA INTELIGENTE")
    print("="*50)
    print("1. Crear nueva lista")
    print("2. Ver lista")
    print("3. Agregar item a lista")
    print("4. Marcar item como comprado")
    print("5. Estadísticas de lista")
    print("6. Exportar lista a TXT")
    print("7. Exportar lista a CSV")
    print("8. Generar reporte de gastos")
    print("9. Buscar item")
    print("10. Crear backup")
    print("11. Salir")
    print("="*50)

def main():
    """Función principal"""
    print("Inicializando sistema...")
    inicializar_sistema()
    listas = cargar_listas()
    
    while True:
        mostrar_menu()
        opcion = input("\\nSelecciona una opción: ")
        
        try:
            if opcion == "1":
                crear_lista(listas)
            elif opcion == "2":
                ver_lista(listas)
            elif opcion == "3":
                agregar_item(listas)
            elif opcion == "4":
                marcar_comprado(listas)
            elif opcion == "5":
                estadisticas_lista(listas)
            elif opcion == "6":
                exportar_txt(listas)
            elif opcion == "7":
                exportar_csv(listas)
            elif opcion == "8":
                generar_reporte_gastos(listas)
            elif opcion == "9":
                buscar_items(listas)
            elif opcion == "10":
                crear_backup()
                print("✅ Backup creado exitosamente")
            elif opcion == "11":
                guardar_listas(listas)
                crear_backup()
                print("\\n✅ Datos guardados. ¡Hasta luego! 👋")
                break
            else:
                print("\\n❌ Opción inválida")
        except Exception as e:
            print(f"\\n❌ Error: {e}")
        
        input("\\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
`,
  },
];

export default function ProjectsPage() {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const handleDownload = (project: Project) => {
    const element = document.createElement('a');
    const file = new Blob([project.starterCode], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${project.id}.py`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (selectedProject) {
    return (
      <div className="min-h-screen bg-stone-900 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <button
            onClick={() => setSelectedProject(null)}
            className="mb-6 flex items-center gap-2 text-stone-400 hover:text-stone-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Volver a proyectos
          </button>

          <div className="bg-stone-800 backdrop-blur-sm rounded-2xl border-2 border-stone-700 overflow-hidden">
            {/* Header */}
            <div className="bg-amber-700 border-b-2 border-amber-800 p-8">
              <div className="flex items-start gap-4">
                <div className="text-6xl">{selectedProject.icon}</div>
                <div className="flex-1">
                  <h1 className="text-4xl font-bold text-stone-100 mb-2">{selectedProject.title}</h1>
                  <p className="text-stone-200 text-lg">{selectedProject.description}</p>
                  <div className="flex flex-wrap gap-4 mt-4">
                    <span className="px-3 py-1 bg-stone-900/30 rounded-full text-stone-100 text-sm">
                      {selectedProject.difficulty}
                    </span>
                    <span className="px-3 py-1 bg-stone-900/30 rounded-full text-stone-100 text-sm">
                      ⏱️ {selectedProject.estimatedTime}
                    </span>
                    <span className="px-3 py-1 bg-stone-900/30 rounded-full text-yellow-300 text-sm">
                      <Trophy className="w-4 h-4 inline mr-1" />
                      {selectedProject.xp} XP
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="p-8 space-y-8">
              {/* Requirements */}
              <section>
                <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                  <CheckCircle2 className="w-6 h-6 text-green-400" />
                  Requisitos Previos
                </h2>
                <ul className="space-y-2">
                  {selectedProject.requirements.map((req, idx) => (
                    <li key={idx} className="text-stone-300 flex items-start gap-2">
                      <span className="text-stone-500 mt-1">▪</span>
                      {req}
                    </li>
                  ))}
                </ul>
              </section>

              {/* Objectives */}
              <section>
                <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                  <Target className="w-6 h-6 text-amber-600" />
                  Objetivos de Aprendizaje
                </h2>
                <ul className="space-y-2">
                  {selectedProject.objectives.map((obj, idx) => (
                    <li key={idx} className="text-stone-300 flex items-start gap-2">
                      <span className="text-stone-500 mt-1">●</span>
                      {obj}
                    </li>
                  ))}
                </ul>
              </section>

              {/* Features */}
              <section>
                <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                  <Code2 className="w-6 h-6 text-amber-600" />
                  Características a Implementar
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {selectedProject.features.map((feature, idx) => (
                    <div key={idx} className="text-stone-300 flex items-start gap-2">
                      <span className="text-green-400">{feature.split(' ')[0]}</span>
                      <span>{feature.substring(feature.indexOf(' ') + 1)}</span>
                    </div>
                  ))}
                </div>
              </section>

              {/* Rubric */}
              <section>
                <h2 className="text-2xl font-bold text-stone-100 mb-4 flex items-center gap-2">
                  <FileText className="w-6 h-6 text-yellow-400" />
                  Rúbrica de Evaluación
                </h2>
                <div className="space-y-4">
                  {selectedProject.rubric.map((item, idx) => (
                    <div key={idx} className="bg-stone-950 rounded-lg p-4 border-2 border-stone-700">
                      <h3 className="text-lg font-semibold text-stone-100 mb-3">{item.category}</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                        <div>
                          <p className="text-green-400 font-semibold mb-1">Excelente</p>
                          <p className="text-stone-400 text-sm">{item.excellent}</p>
                        </div>
                        <div>
                          <p className="text-yellow-400 font-semibold mb-1">Bien</p>
                          <p className="text-stone-400 text-sm">{item.good}</p>
                        </div>
                        <div>
                          <p className="text-red-400 font-semibold mb-1">Necesita Mejorar</p>
                          <p className="text-stone-400 text-sm">{item.needsWork}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Download Button */}
              <div className="flex justify-center pt-6">
                <button
                  onClick={() => handleDownload(selectedProject)}
                  className="flex items-center gap-3 px-8 py-4 bg-amber-700 border-2 border-amber-800 hover:bg-amber-800 text-stone-100 rounded-xl font-semibold text-lg shadow-lg transform hover:scale-105 transition-all"
                >
                  <Download className="w-6 h-6" />
                  Descargar Código Inicial
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-stone-900 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-stone-400 hover:text-stone-100 transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver al Dashboard
        </Link>

        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-stone-100 mb-4">
            Proyectos Finales
          </h1>
          <p className="text-xl text-stone-300 max-w-3xl mx-auto">
            Pon a prueba tus habilidades con estos proyectos completos. Cada uno integra todos los conceptos aprendidos en su curso correspondiente.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-stone-800 backdrop-blur-sm rounded-2xl border-2 border-stone-700 overflow-hidden hover:border-amber-600 transition-all hover:scale-105 cursor-pointer"
              onClick={() => setSelectedProject(project)}
            >
              <div className="bg-amber-700 border-b-2 border-amber-800 p-6">
                <div className="text-5xl mb-3">{project.icon}</div>
                <h3 className="text-2xl font-bold text-stone-100 mb-2">{project.title}</h3>
                <p className="text-stone-200 text-sm">{project.courseName}</p>
              </div>

              <div className="p-6 space-y-4">
                <p className="text-stone-300">{project.description}</p>

                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-amber-700/30 rounded-full text-stone-200 text-xs">
                    {project.difficulty}
                  </span>
                  <span className="px-3 py-1 bg-amber-700/30 rounded-full text-stone-200 text-xs">
                    ⏱️ {project.estimatedTime}
                  </span>
                  <span className="px-3 py-1 bg-yellow-600/30 rounded-full text-yellow-200 text-xs">
                    <Trophy className="w-3 h-3 inline mr-1" />
                    {project.xp} XP
                  </span>
                </div>

                <div className="pt-4 border-t border-stone-700">
                  <p className="text-stone-400 text-sm font-semibold mb-2">Características principales:</p>
                  <ul className="space-y-1">
                    {project.features.slice(0, 3).map((feature, idx) => (
                      <li key={idx} className="text-stone-300 text-xs flex items-start gap-1">
                        <span className="text-green-400">{feature.split(' ')[0]}</span>
                        <span className="line-clamp-1">{feature.substring(feature.indexOf(' ') + 1)}</span>
                      </li>
                    ))}
                  </ul>
                  <p className="text-stone-400 text-xs mt-2">+{project.features.length - 3} más...</p>
                </div>

                <button
                  className="w-full py-3 bg-amber-700 border-2 border-amber-800 hover:bg-amber-800 text-stone-100 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedProject(project);
                  }}
                >
                  Ver Detalles
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
