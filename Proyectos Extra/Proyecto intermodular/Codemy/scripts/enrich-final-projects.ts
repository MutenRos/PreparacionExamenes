import * as fs from 'fs';
import * as path from 'path';

const dataDir = path.join(__dirname, '..', 'apps', 'web', 'src', 'data');

// Proyectos detallados por tipo de curso
const projectTemplates: Record<string, any> = {
  // Data Science / ML
  'numpy': {
    theory: `Crea un sistema de análisis numérico completo que procese datasets reales, aplique operaciones vectorizadas y genere visualizaciones estadísticas.`,
    example: `import numpy as np
import matplotlib.pyplot as plt

# Cargar datos de ventas mensuales
ventas = np.array([
    [1200, 1500, 1800, 1600, 2000, 2200],  # Producto A
    [900, 1100, 1300, 1250, 1400, 1600],   # Producto B
    [1500, 1600, 1700, 1800, 1900, 2100]   # Producto C
])

# Análisis estadístico
print("📊 Análisis de Ventas")
print(f"Total ventas: ${ventas.sum():,.2f}")
print(f"Promedio mensual: ${ventas.mean():,.2f}")
print(f"Desviación estándar: ${ventas.std():,.2f}")

# Ventas por producto
ventas_producto = ventas.sum(axis=1)
productos = ['Producto A', 'Producto B', 'Producto C']

for i, prod in enumerate(productos):
    print(f"{prod}: ${ventas_producto[i]:,.2f}")

# Crecimiento mensual
crecimiento = np.diff(ventas.mean(axis=0)) / ventas.mean(axis=0)[:-1] * 100
print(f"\\nCrecimiento promedio: {crecimiento.mean():.2f}%")

# Predicción lineal simple
meses = np.arange(len(ventas[0]))
tendencia = np.polyfit(meses, ventas.mean(axis=0), 1)
prediccion = np.polyval(tendencia, len(meses))
print(f"Predicción próximo mes: ${prediccion:,.2f}")`,
    initialCode: `import numpy as np

# TODO: Implementa el sistema de análisis numérico
# 1. Carga un dataset de al menos 3 productos y 6 meses
# 2. Calcula estadísticas: total, promedio, desviación estándar
# 3. Analiza ventas por producto
# 4. Calcula crecimiento mensual
# 5. Genera una predicción simple

# Tu código aquí
ventas = np.array([
    # Agrega tus datos
])`,
    description: `Desarrolla un sistema de análisis numérico completo que:
- Procese datos de ventas de múltiples productos
- Calcule estadísticas descriptivas (media, mediana, desviación estándar)
- Identifique tendencias y patrones
- Genere predicciones básicas con regresión lineal
- Visualice resultados con gráficos

Este proyecto integra todos los conceptos de NumPy aprendidos: arrays, slicing, broadcasting, operaciones matemáticas y álgebra lineal.`
  },
  
  'pandas': {
    theory: `Desarrolla un sistema de análisis de datos completo usando Pandas para procesar, limpiar, transformar y visualizar un dataset real de e-commerce.`,
    example: `import pandas as pd
import numpy as np

# Simular dataset de e-commerce
np.random.seed(42)
n = 100

df = pd.DataFrame({
    'order_id': range(1000, 1000 + n),
    'customer': [f'Cliente_{i%30}' for i in range(n)],
    'product': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], n),
    'quantity': np.random.randint(1, 5, n),
    'price': np.random.choice([25.99, 89.99, 299.99, 449.99], n),
    'date': pd.date_range('2024-01-01', periods=n, freq='D'),
    'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n)
})

df['total'] = df['quantity'] * df['price']

print("📦 Análisis E-Commerce\\n")

# Estadísticas generales
print(f"Total órdenes: {len(df)}")
print(f"Ingresos totales: ${df['total'].sum():,.2f}")
print(f"Ticket promedio: ${df['total'].mean():,.2f}\\n")

# Top productos
print("🏆 Top Productos:")
print(df.groupby('product')['total'].sum().sort_values(ascending=False))

# Análisis temporal
print("\\n📅 Ventas por mes:")
df['month'] = df['date'].dt.to_period('M')
monthly = df.groupby('month')['total'].sum()
print(monthly)

# Clientes VIP
print("\\n⭐ Top 5 Clientes:")
top_customers = df.groupby('customer')['total'].sum().nlargest(5)
print(top_customers)

# Análisis regional
print("\\n🌎 Ventas por región:")
regional = df.groupby('region').agg({
    'total': ['sum', 'mean', 'count']
}).round(2)
print(regional)`,
    initialCode: `import pandas as pd
import numpy as np

# TODO: Crea un sistema de análisis de e-commerce
# 1. Genera o carga un dataset con: orders, customers, products, prices, dates, regions
# 2. Calcula estadísticas generales: total órdenes, ingresos, ticket promedio
# 3. Identifica top productos y clientes VIP
# 4. Analiza ventas por mes y por región
# 5. Genera insights y recomendaciones

# Tu código aquí`,
    description: `Crea un sistema completo de análisis de e-commerce que:
- Procese datos de órdenes, clientes y productos
- Limpie y transforme datos (fechas, categorías, valores nulos)
- Calcule KPIs: ingresos totales, ticket promedio, conversión
- Identifique top productos y clientes VIP
- Analice tendencias temporales (diario, mensual)
- Segmente por regiones geográficas
- Genere reportes con agregaciones y visualizaciones

Aplica merge, groupby, pivot tables y time series de Pandas.`
  },

  'matplotlib': {
    theory: `Construye un dashboard interactivo de visualización de datos que integre múltiples tipos de gráficos para análisis de métricas de negocio.`,
    example: `import matplotlib.pyplot as plt
import numpy as np

# Datos de ejemplo
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
ventas = [45000, 52000, 48000, 61000, 58000, 67000]
gastos = [35000, 38000, 36000, 42000, 41000, 45000]
usuarios = [1200, 1500, 1800, 2100, 2400, 2800]

# Crear dashboard con subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('📊 Dashboard de Métricas de Negocio', fontsize=16, fontweight='bold')

# 1. Ventas vs Gastos
ax1.plot(meses, ventas, marker='o', linewidth=2, label='Ventas', color='#2ecc71')
ax1.plot(meses, gastos, marker='s', linewidth=2, label='Gastos', color='#e74c3c')
ax1.fill_between(range(len(meses)), ventas, gastos, alpha=0.2)
ax1.set_title('Ventas vs Gastos', fontweight='bold')
ax1.set_ylabel('Monto ($)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Beneficio neto
beneficio = [v - g for v, g in zip(ventas, gastos)]
colors = ['#2ecc71' if b > 0 else '#e74c3c' for b in beneficio]
ax2.bar(meses, beneficio, color=colors, alpha=0.7)
ax2.set_title('Beneficio Neto Mensual', fontweight='bold')
ax2.set_ylabel('Beneficio ($)')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax2.grid(True, alpha=0.3, axis='y')

# 3. Crecimiento de usuarios
ax3.plot(meses, usuarios, marker='D', linewidth=2.5, color='#3498db', markersize=8)
ax3.fill_between(range(len(meses)), usuarios, alpha=0.3, color='#3498db')
ax3.set_title('Crecimiento de Usuarios', fontweight='bold')
ax3.set_ylabel('Usuarios')
ax3.grid(True, alpha=0.3)

# 4. Distribución de ingresos
categorias = ['Producto A', 'Producto B', 'Producto C', 'Servicios']
ingresos_cat = [120000, 95000, 78000, 62000]
ax4.pie(ingresos_cat, labels=categorias, autopct='%1.1f%%',
        colors=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'],
        startangle=90, explode=(0.05, 0, 0, 0))
ax4.set_title('Distribución de Ingresos', fontweight='bold')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard generado: dashboard.png")
plt.show()`,
    initialCode: `import matplotlib.pyplot as plt
import numpy as np

# TODO: Crea un dashboard completo de visualización
# 1. Prepara datos de al menos 6 meses
# 2. Crea 4 gráficos diferentes en un subplot 2x2
# 3. Incluye: líneas, barras, área, pie chart
# 4. Personaliza colores, títulos, leyendas
# 5. Guarda el dashboard como imagen

# Tu código aquí`,
    description: `Diseña un dashboard profesional de visualización que incluya:
- Gráficos de líneas con múltiples series (ventas, gastos, usuarios)
- Gráficos de barras comparativas con colores condicionales
- Áreas sombreadas para mostrar rangos y tendencias
- Gráficos circulares (pie charts) para distribuciones
- Personalización avanzada: colores, títulos, leyendas, grids
- Anotaciones y markers especiales
- Export de alta calidad (PNG, SVG)

Demuestra dominio de subplots, estilos y customización.`
  },

  'master-ai': {
    theory: `Desarrolla un sistema completo de IA que integre ML, Deep Learning, Computer Vision y NLP para resolver un problema real de negocio.`,
    example: `# Sistema de IA: Asistente Inteligente Multimodal
import tensorflow as tf
from transformers import pipeline
import cv2
import numpy as np

class AIAssistant:
    def __init__(self):
        # Modelos preentrenados
        self.classifier = pipeline("sentiment-analysis")
        self.nlp = pipeline("question-answering")
        self.detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        print("✅ Modelos cargados")
    
    def analyze_sentiment(self, text):
        """Análisis de sentimiento en texto"""
        result = self.classifier(text)[0]
        return {
            'sentiment': result['label'],
            'confidence': result['score']
        }
    
    def answer_question(self, context, question):
        """Responde preguntas sobre un contexto"""
        result = self.nlp(question=question, context=context)
        return result['answer']
    
    def detect_faces(self, image_path):
        """Detección de rostros en imágenes"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        return len(faces)
    
    def predict_customer_churn(self, features):
        """Predicción de abandono de clientes"""
        # Simula modelo de ML
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(len(features),)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        # En producción: model.load_weights('churn_model.h5')
        prediction = model.predict(np.array([features]))[0][0]
        return {
            'churn_probability': float(prediction),
            'risk_level': 'High' if prediction > 0.7 else 'Medium' if prediction > 0.4 else 'Low'
        }

# Demo del sistema
assistant = AIAssistant()

# 1. Análisis de sentimiento
review = "This product is absolutely amazing! Best purchase ever."
sentiment = assistant.analyze_sentiment(review)
print(f"\\n📝 Sentiment: {sentiment['sentiment']} ({sentiment['confidence']:.2%})")

# 2. Q&A
context = "Our company increased revenue by 45% in Q4 2024 through AI automation."
answer = assistant.answer_question(context, "What was the revenue increase?")
print(f"\\n❓ Answer: {answer}")

# 3. Customer Churn
features = [35, 12, 5, 3, 250, 0.8]  # age, tenure, complaints, support_calls, spending, satisfaction
churn = assistant.predict_customer_churn(features)
print(f"\\n⚠️  Churn Risk: {churn['risk_level']} ({churn['churn_probability']:.1%})")`,
    initialCode: `# TODO: Construye un sistema de IA completo
# Debe incluir al menos 3 de estos componentes:
# - Machine Learning (clasificación o regresión)
# - Deep Learning (red neuronal)
# - Computer Vision (detección de objetos/rostros)
# - NLP (análisis de texto o chatbot)
# - Reinforcement Learning (agente inteligente)

# Tu implementación aquí
class AISystem:
    def __init__(self):
        # Inicializa tus modelos
        pass`,
    description: `Crea un sistema de IA production-ready que integre:
- Machine Learning: modelo de clasificación o regresión con scikit-learn
- Deep Learning: red neuronal con TensorFlow/PyTorch
- Computer Vision: detección de objetos con OpenCV/YOLO
- NLP: procesamiento de texto con transformers
- MLOps: pipeline de entrenamiento, evaluación y deployment
- Monitoreo: métricas de performance y drift detection

Demuestra arquitectura escalable, manejo de datos, optimización de modelos y deployment en producción.`
  },

  'web3': {
    theory: `Construye una DApp (Aplicación Descentralizada) completa con smart contracts, frontend React y integración Web3.`,
    example: `// Smart Contract: TokenMarketplace.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TokenMarketplace {
    struct Item {
        uint256 id;
        address seller;
        string name;
        uint256 price;
        bool sold;
    }
    
    mapping(uint256 => Item) public items;
    uint256 public itemCount;
    uint256 public fee = 25; // 2.5% fee
    
    event ItemListed(uint256 id, address seller, string name, uint256 price);
    event ItemSold(uint256 id, address buyer, uint256 price);
    
    function listItem(string memory _name, uint256 _price) public {
        require(_price > 0, "Price must be positive");
        itemCount++;
        items[itemCount] = Item(itemCount, msg.sender, _name, _price, false);
        emit ItemListed(itemCount, msg.sender, _name, _price);
    }
    
    function buyItem(uint256 _id) public payable {
        Item storage item = items[_id];
        require(!item.sold, "Item already sold");
        require(msg.value == item.price, "Incorrect price");
        
        uint256 feeAmount = (item.price * fee) / 1000;
        uint256 sellerAmount = item.price - feeAmount;
        
        item.sold = true;
        payable(item.seller).transfer(sellerAmount);
        emit ItemSold(_id, msg.sender, item.price);
    }
}

// Frontend React + ethers.js
import { ethers } from 'ethers';
import { useState, useEffect } from 'react';

function MarketplaceDApp() {
    const [items, setItems] = useState([]);
    const [contract, setContract] = useState(null);
    const [account, setAccount] = useState('');

    const CONTRACT_ADDRESS = '0x...';
    const ABI = [...]; // Contract ABI
    
    useEffect(() => {
        connectWallet();
    }, []);
    
    async function connectWallet() {
        if (window.ethereum) {
            const provider = new ethers.BrowserProvider(window.ethereum);
            const signer = await provider.getSigner();
            const address = await signer.getAddress();
            
            const marketContract = new ethers.Contract(
                CONTRACT_ADDRESS, ABI, signer
            );
            
            setAccount(address);
            setContract(marketContract);
            loadItems();
        }
    }
    
    async function loadItems() {
        const count = await contract.itemCount();
        const itemsList = [];
        
        for (let i = 1; i <= count; i++) {
            const item = await contract.items(i);
            if (!item.sold) {
                itemsList.push({
                    id: item.id,
                    name: item.name,
                    price: ethers.formatEther(item.price),
                    seller: item.seller
                });
            }
        }
        setItems(itemsList);
    }
    
    async function buyItem(itemId, price) {
        const tx = await contract.buyItem(itemId, {
            value: ethers.parseEther(price)
        });
        await tx.wait();
        loadItems();
    }
    
    return (
        <div className="marketplace">
            <h1>🛒 Decentralized Marketplace</h1>
            <p>Connected: {account.slice(0, 6)}...{account.slice(-4)}</p>
            
            <div className="items">
                {items.map(item => (
                    <div key={item.id} className="item-card">
                        <h3>{item.name}</h3>
                        <p>Price: {item.price} ETH</p>
                        <button onClick={() => buyItem(item.id, item.price)}>
                            Buy Now
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}`,
    initialCode: `// TODO: Crea una DApp completa con:
// 1. Smart Contract en Solidity con funcionalidad útil
// 2. Deploy en testnet (Sepolia, Mumbai, etc.)
// 3. Frontend React con ethers.js o web3.js
// 4. Integración con MetaMask
// 5. IPFS para almacenamiento descentralizado (opcional)

// Smart Contract
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyDApp {
    // Tu lógica aquí
}

// Frontend
// Tu código React aquí`,
    description: `Desarrolla una DApp production-ready que incluya:
- Smart Contract en Solidity con funcionalidad real (marketplace, DAO, NFT, DeFi)
- Tests unitarios con Hardhat/Truffle
- Deploy en testnet (Sepolia, Polygon Mumbai)
- Frontend React con Web3 integration
- Wallet connection (MetaMask, WalletConnect)
- Event listening y estado sincronizado
- IPFS para archivos descentralizados
- UI/UX profesional con feedback de transacciones

Demuestra arquitectura Web3, manejo de gas, seguridad y UX.`
  }
};

// Función para generar proyecto detallado
function generateDetailedProject(courseId: string, projectTitle: string, lessonNumber: number): string {
  const template = projectTemplates[courseId];
  
  if (!template) {
    // Template genérico para cursos sin plantilla específica
    return generateGenericProject(courseId, projectTitle, lessonNumber);
  }
  
  return `  '${lessonNumber}': {
    title: '${projectTitle}',
    duration: '${40 + lessonNumber * 5} min',
    xp: ${lessonNumber >= 10 ? 150 : 100},
    theory: {
      introduction: '${template.theory}',
      sections: [
        {
          title: 'Objetivos del Proyecto',
          content: 'En este proyecto final integrarás todos los conceptos aprendidos:',
          points: [
            'Aplicar técnicas avanzadas del curso',
            'Resolver un problema real de la industria',
            'Implementar best practices profesionales',
            'Crear código production-ready documentado'
          ]
        },
        {
          title: 'Arquitectura y Diseño',
          content: 'Planificación del proyecto:',
          points: [
            'Definir requisitos y casos de uso',
            'Diseñar arquitectura modular',
            'Seleccionar herramientas y librerías',
            'Establecer métricas de éxito'
          ]
        },
        {
          title: 'Implementación y Testing',
          content: 'Desarrollo completo:',
          points: [
            'Implementación incremental con commits',
            'Testing unitario y de integración',
            'Documentación de código y APIs',
            'Optimización de performance'
          ]
        }
      ],
      example: {
        title: 'Ejemplo Completo: ${projectTitle}',
        code: \`${template.example}\`,
        explanation: 'Este código demuestra la implementación completa del proyecto integrando todos los conceptos del curso. Analiza la arquitectura, patrones utilizados y best practices aplicadas.'
      }
    },
    exercise: {
      title: 'Proyecto Final: ${projectTitle}',
      description: \`${template.description}\`,
      initialCode: \`${template.initialCode}\`,
      solution: \`${template.example}\`,
      test: 'has_code',
      hints: [
        'Comienza por definir la estructura de datos y arquitectura',
        'Implementa funcionalidades una por una, testeando cada parte',
        'Sigue los ejemplos de la teoría como referencia',
        'Documenta tu código con comentarios claros',
        'Optimiza y refactoriza antes de considerar completo',
        'Agrega manejo de errores robusto',
        'Considera casos edge y validación de inputs'
      ]
    }
  }`;
}

function generateGenericProject(courseId: string, projectTitle: string, lessonNumber: number): string {
  const courseType = getCourseType(courseId);
  
  return `  '${lessonNumber}': {
    title: '${projectTitle}',
    duration: '${40 + lessonNumber * 5} min',
    xp: ${lessonNumber >= 10 ? 150 : 100},
    theory: {
      introduction: 'Desarrolla un proyecto completo que integre todos los conceptos aprendidos en el curso, resolviendo un problema real con código production-ready.',
      sections: [
        {
          title: 'Planificación del Proyecto',
          content: 'Fase de diseño y arquitectura:',
          points: [
            'Análisis de requisitos funcionales y no funcionales',
            'Diseño de arquitectura modular y escalable',
            'Selección de tecnologías y herramientas apropiadas',
            'Definición de casos de prueba y métricas de éxito'
          ]
        },
        {
          title: 'Implementación',
          content: 'Desarrollo del proyecto:',
          points: [
            'Estructura de archivos y organización del código',
            'Implementación de funcionalidades core',
            'Integración de librerías y frameworks',
            'Manejo de errores y casos edge'
          ]
        },
        {
          title: 'Testing y Optimización',
          content: 'Aseguramiento de calidad:',
          points: [
            'Tests unitarios y de integración',
            'Refactorización y código limpio',
            'Optimización de performance',
            'Documentación completa'
          ]
        }
      ],
      example: {
        title: 'Estructura del Proyecto: ${projectTitle}',
        code: \`${getExampleCode(courseType, projectTitle)}\`,
        explanation: 'Esta estructura demuestra cómo organizar un proyecto profesional aplicando todos los conceptos aprendidos. Incluye arquitectura modular, separación de responsabilidades y buenas prácticas.'
      }
    },
    exercise: {
      title: 'Desarrolla: ${projectTitle}',
      description: \`Crea un proyecto completo que demuestre dominio de ${courseId}. El proyecto debe:
      
✅ Integrar al menos 5 conceptos clave del curso
✅ Resolver un problema real con aplicación práctica
✅ Incluir manejo de errores robusto
✅ Tener código bien documentado y estructurado
✅ Seguir best practices de la industria
✅ Ser extensible y mantenible

${getProjectRequirements(courseType)}\`,
      initialCode: \`${getInitialCode(courseType, projectTitle)}\`,
      solution: \`${getSolutionCode(courseType, projectTitle)}\`,
      test: 'has_code',
      hints: [
        'Empieza por el diseño antes de codificar',
        'Implementa incrementalmente, testeando cada parte',
        'Reutiliza código y aplica principios DRY',
        'Comenta secciones complejas del código',
        'Considera edge cases y manejo de errores',
        'Optimiza después de tener funcionalidad completa',
        'Revisa la documentación oficial ante dudas'
      ]
    }
  }`;
}

function getCourseType(courseId: string): string {
  if (courseId.includes('python') || courseId.includes('numpy') || courseId.includes('pandas') || courseId.includes('scikit')) return 'python-ml';
  if (courseId.includes('java')) return 'java';
  if (courseId.includes('js') || courseId.includes('react') || courseId.includes('node')) return 'javascript';
  if (courseId.includes('cpp') || courseId.includes('c++')) return 'cpp';
  if (courseId.includes('web')) return 'web';
  if (courseId.includes('master')) return 'advanced';
  return 'general';
}

function getExampleCode(type: string, title: string): string {
  const examples: Record<string, string> = {
    'python-ml': `# ${title} - Sistema Completo
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    """Procesador de datos con pipeline completo"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.data = None
    
    def load_data(self, filepath):
        """Carga y valida datos"""
        self.data = pd.read_csv(filepath)
        print(f"✅ Datos cargados: {self.data.shape}")
        return self.data
    
    def clean_data(self):
        """Limpieza de datos"""
        # Eliminar duplicados
        self.data = self.data.drop_duplicates()
        
        # Manejar valores nulos
        self.data = self.data.fillna(self.data.mean())
        
        print(f"✅ Datos limpios: {self.data.shape}")
        return self.data
    
    def process(self):
        """Pipeline completo"""
        self.clean_data()
        # Más procesamiento aquí
        return self.data

# Uso
processor = DataProcessor()
data = processor.load_data('dataset.csv')
processed = processor.process()`,
    
    'javascript': `// ${title} - Aplicación Completa
class ${title.replace(/[^a-zA-Z]/g, '')} {
    constructor() {
        this.data = [];
        this.init();
    }
    
    init() {
        console.log('🚀 Inicializando aplicación...');
        this.loadData();
        this.setupEventListeners();
    }
    
    async loadData() {
        try {
            const response = await fetch('/api/data');
            this.data = await response.json();
            this.render();
        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }
    
    setupEventListeners() {
        document.getElementById('submit')
            .addEventListener('click', () => this.handleSubmit());
    }
    
    handleSubmit() {
        // Lógica de submit
        console.log('✅ Datos procesados');
    }
    
    render() {
        // Renderizado de UI
        console.log('🎨 UI actualizada');
    }
}

// Inicializar
const app = new ${title.replace(/[^a-zA-Z]/g, '')}();`,
    
    'java': `// ${title} - Sistema Completo
import java.util.*;
import java.util.stream.*;

public class ${title.replace(/[^a-zA-Z]/g, '')} {
    private List<Object> data;
    
    public ${title.replace(/[^a-zA-Z]/g, '')}() {
        this.data = new ArrayList<>();
        initialize();
    }
    
    private void initialize() {
        System.out.println("🚀 Inicializando sistema...");
        loadData();
    }
    
    public void loadData() {
        // Cargar datos
        System.out.println("✅ Datos cargados");
    }
    
    public void process() {
        data.stream()
            .filter(Objects::nonNull)
            .forEach(System.out::println);
    }
    
    public static void main(String[] args) {
        ${title.replace(/[^a-zA-Z]/g, '')} app = new ${title.replace(/[^a-zA-Z]/g, '')}();
        app.process();
    }
}`,
    
    'general': `# ${title} - Proyecto Completo

def main():
    """Función principal del proyecto"""
    print("🚀 Iniciando ${title}...")
    
    # Inicialización
    data = load_data()
    
    # Procesamiento
    result = process(data)
    
    # Resultados
    display_results(result)
    print("✅ Proyecto completado")

def load_data():
    """Carga de datos"""
    return []

def process(data):
    """Procesamiento principal"""
    return data

def display_results(result):
    """Muestra resultados"""
    print(f"Resultados: {len(result)} items procesados")

if __name__ == "__main__":
    main()`
  };
  
  return examples[type] || examples['general'];
}

function getInitialCode(type: string, title: string): string {
  return `// TODO: Implementa ${title}
// 
// Requisitos:
// 1. [Completa según el tipo de proyecto]
// 2. [Agrega más requisitos]
// 3. [...]
//
// Tu código aquí`;
}

function getSolutionCode(type: string, title: string): string {
  return getExampleCode(type, title);
}

function getProjectRequirements(type: string): string {
  const requirements: Record<string, string> = {
    'python-ml': `
Requisitos técnicos:
- Procesamiento de datos con Pandas/NumPy
- Modelo de ML con métricas de evaluación
- Visualizaciones con Matplotlib
- Pipeline de entrenamiento automatizado`,
    'javascript': `
Requisitos técnicos:
- Arquitectura modular con clases/módulos
- Manejo asíncrono (Promises/async-await)
- Interacción con APIs
- UI responsiva y funcional`,
    'java': `
Requisitos técnicos:
- POO con herencia y polimorfismo
- Collections Framework
- Manejo de excepciones robusto
- Tests unitarios con JUnit`,
    'general': `
Requisitos técnicos:
- Código modular y reutilizable
- Documentación clara
- Manejo de errores
- Tests básicos`
  };
  
  return requirements[type] || requirements['general'];
}

// Procesar archivos
const files = fs.readdirSync(dataDir).filter(f => f.startsWith('lessons-content-') && f.endsWith('.ts'));
let updated = 0;

console.log(`🔍 Procesando ${files.length} archivos...\\n`);

files.forEach(filename => {
  const filepath = path.join(dataDir, filename);
  let content = fs.readFileSync(filepath, 'utf-8');
  
  // Buscar proyectos finales con contenido genérico
  const projectRegex = /('(\d+)':\s*\{[^}]*title:\s*'Proyecto:[^']+')[^}]*?console\.log\("Ejemplo de Proyecto:/g;
  
  if (projectRegex.test(content)) {
    const courseId = filename.replace('lessons-content-', '').replace('.ts', '');
    
    // Recargar para procesar
    content = fs.readFileSync(filepath, 'utf-8');
    
    // Extraer número de lección y título del proyecto
    const matches = content.matchAll(/('(\d+)':\s*\{[^}]*title:\s*'(Proyecto:[^']+)')/g);
    
    for (const match of matches) {
      const lessonNum = match[2];
      const projectTitle = match[3];
      
      // Generar proyecto detallado
      const detailedProject = generateDetailedProject(courseId, projectTitle, parseInt(lessonNum));
      
      // Buscar y reemplazar la lección completa
      const lessonRegex = new RegExp(`'${lessonNum}':\\s*\\{[^}]*title:\\s*'${projectTitle.replace(/[()]/g, '\\$&')}'[\\s\\S]*?\\}(?=\\s*(?:,\\s*'\\d+':|\\};))`, 'g');
      
      if (lessonRegex.test(content)) {
        content = content.replace(lessonRegex, detailedProject);
        updated++;
        console.log(`✅ ${filename} - Lección ${lessonNum}: ${projectTitle}`);
      }
    }
    
    fs.writeFileSync(filepath, content, 'utf-8');
  }
});

console.log(`\\n🎉 Proyectos finales enriquecidos: ${updated} archivos actualizados`);
