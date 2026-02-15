'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Play, RotateCcw, Download, Copy, Check } from 'lucide-react';

export default function PlaygroundPage() {
  const [language, setLanguage] = useState<'python' | 'javascript' | 'html'>('python');
  const [code, setCode] = useState({
    python: `# Playground de Python
# Escribe tu código aquí y pruébalo

print("¡Hola desde el Playground!")

# Ejemplo: calculadora simple
num1 = 10
num2 = 5

print(f"Suma: {num1 + num2}")
print(f"Resta: {num1 - num2}")
print(f"Multiplicación: {num1 * num2}")
print(f"División: {num1 / num2}")
`,
    javascript: `// Playground de JavaScript
// Escribe tu código aquí y pruébalo

console.log("¡Hola desde el Playground!");

// Ejemplo: función saludos
function saludar(nombre) {
  return \`Hola, \${nombre}! Bienvenido al playground\`;
}

console.log(saludar("Estudiante"));

// Ejemplo: array de números
const numeros = [1, 2, 3, 4, 5];
const dobles = numeros.map(n => n * 2);
console.log("Números originales:", numeros);
console.log("Números duplicados:", dobles);
`,
    html: `<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .container {
      background: white;
      color: #333;
      padding: 30px;
      border-radius: 10px;
      max-width: 600px;
      margin: 0 auto;
    }
    button {
      background: #667eea;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover {
      background: #764ba2;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>¡Hola desde HTML!</h1>
    <p>Este es tu playground de HTML/CSS/JS</p>
    <button onclick="alert('¡Botón presionado!')">
      Haz clic aquí
    </button>
  </div>
</body>
</html>
`,
  });

  const [output, setOutput] = useState('Presiona "Ejecutar" para ver el resultado...');
  const [copied, setCopied] = useState(false);

  const runCode = () => {
    setOutput('Ejecutando código...\n\n');
    
    setTimeout(() => {
      if (language === 'python') {
        // Simulación de ejecución de Python
        let result = '';
        const lines = code.python.split('\n');
        
        lines.forEach(line => {
          if (line.includes('print(')) {
            const match = line.match(/print\((.*)\)/);
            if (match) {
              try {
                // Evaluar la expresión de forma segura (simulada)
                let content = match[1];
                
                // Manejar f-strings simples
                if (content.includes('f"') || content.includes("f'")) {
                  content = content.replace(/f["'](.+?)["']/, (_: any, str: string) => {
                    return str.replace(/\{(.+?)\}/g, (_match: any, expr: string) => {
                      // Evaluar expresiones simples
                      try {
                        return eval(expr);
                      } catch {
                        return expr;
                      }
                    });
                  });
                } else {
                  content = content.replace(/["']/g, '');
                }
                
                result += content + '\n';
              } catch (e) {
                result += `Error en línea: ${line}\n`;
              }
            }
          }
        });
        
        setOutput(result || 'No hay salida');
      } else if (language === 'javascript') {
        // Simulación de ejecución de JavaScript
        let result = '';
        const originalLog = console.log;
        
        // Capturar console.log
        const logs: any[] = [];
        console.log = (...args) => {
          logs.push(args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
          ).join(' '));
        };
        
        try {
          eval(code.javascript);
          result = logs.join('\n');
        } catch (e: any) {
          result = `Error: ${e.message}`;
        }
        
        // Restaurar console.log
        console.log = originalLog;
        
        setOutput(result || 'No hay salida');
      } else if (language === 'html') {
        setOutput('Vista previa cargada abajo ⬇️');
      }
    }, 500);
  };

  const resetCode = () => {
    setCode({
      ...code,
      [language]: getDefaultCode(language),
    });
    setOutput('Código reiniciado. Presiona "Ejecutar" para ver el resultado...');
  };

  const getDefaultCode = (lang: string) => {
    const defaults: any = {
      python: `# Playground de Python
print("¡Hola, mundo!")
`,
      javascript: `// Playground de JavaScript
console.log("¡Hola, mundo!");
`,
      html: `<!DOCTYPE html>
<html>
<head>
  <title>Mi Página</title>
</head>
<body>
  <h1>¡Hola, mundo!</h1>
</body>
</html>
`,
    };
    return defaults[lang];
  };

  const copyCode = () => {
    navigator.clipboard.writeText(code[language]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCode = () => {
    const extensions: any = {
      python: 'py',
      javascript: 'js',
      html: 'html',
    };
    
    const blob = new Blob([code[language]], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `playground.${extensions[language]}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-stone-900">
      {/* Header */}
      <div className="bg-stone-800 backdrop-blur-sm border-b-2 border-stone-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/dashboard" className="text-stone-300 hover:text-stone-100 flex items-center gap-2 font-medium">
              <ArrowLeft className="w-5 h-5" />
              Volver al dashboard
            </Link>
            <h1 className="text-2xl font-bold text-stone-100">🎮 Playground</h1>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Selector de lenguaje */}
        <div className="bg-stone-800 backdrop-blur-sm rounded-xl p-4 mb-6 border-2 border-stone-700">
          <div className="flex gap-4 items-center justify-between flex-wrap">
            <div className="flex gap-2">
              <button
                onClick={() => setLanguage('python')}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  language === 'python'
                    ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                    : 'bg-stone-700 border-2 border-stone-600 text-stone-300 hover:bg-stone-600'
                }`}
              >
                🐍 Python
              </button>
              <button
                onClick={() => setLanguage('javascript')}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  language === 'javascript'
                    ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                    : 'bg-stone-700 border-2 border-stone-600 text-stone-300 hover:bg-stone-600'
                }`}
              >
                ⚡ JavaScript
              </button>
              <button
                onClick={() => setLanguage('html')}
                className={`px-6 py-2 rounded-lg font-medium transition-all ${
                  language === 'html'
                    ? 'bg-amber-700 border-2 border-amber-800 text-stone-100 shadow-lg'
                    : 'bg-stone-700 border-2 border-stone-600 text-stone-300 hover:bg-stone-600'
                }`}
              >
                🌐 HTML/CSS
              </button>
            </div>

            <div className="flex gap-2">
              <button
                onClick={copyCode}
                className="px-4 py-2 bg-stone-700 border-2 border-stone-600 hover:bg-stone-600 text-stone-100 rounded-lg font-medium flex items-center gap-2 transition-all"
              >
                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                {copied ? 'Copiado' : 'Copiar'}
              </button>
              <button
                onClick={downloadCode}
                className="px-4 py-2 bg-stone-700 border-2 border-stone-600 hover:bg-stone-600 text-stone-100 rounded-lg font-medium flex items-center gap-2 transition-all"
              >
                <Download className="w-4 h-4" />
                Descargar
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Editor */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-stone-100">Editor</h2>
              <div className="flex gap-2">
                <button
                  onClick={resetCode}
                  className="px-4 py-2 bg-red-600 border-2 border-red-700 hover:bg-red-700 text-stone-100 rounded-lg font-medium flex items-center gap-2 transition-all"
                >
                  <RotateCcw className="w-4 h-4" />
                  Reiniciar
                </button>
                <button
                  onClick={runCode}
                  className="px-6 py-2 bg-green-600 border-2 border-green-700 hover:bg-green-700 text-stone-100 rounded-lg font-medium flex items-center gap-2 transition-all shadow-lg"
                >
                  <Play className="w-4 h-4" />
                  Ejecutar
                </button>
              </div>
            </div>

            <textarea
              value={code[language]}
              onChange={(e) => setCode({ ...code, [language]: e.target.value })}
              className="w-full h-[600px] bg-stone-950 text-stone-100 font-mono text-sm p-4 rounded-xl border-2 border-stone-700 focus:border-amber-700 focus:ring-2 focus:ring-amber-700 focus:outline-none resize-none"
              spellCheck={false}
              placeholder="Escribe tu código aquí..."
            />
          </div>

          {/* Output */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-stone-100">Salida</h2>
            
            {language === 'html' ? (
              <div className="bg-stone-800 backdrop-blur-sm rounded-xl overflow-hidden border-2 border-stone-700 h-[600px]">
                <iframe
                  srcDoc={code.html}
                  className="w-full h-full"
                  title="HTML Preview"
                  sandbox="allow-scripts"
                />
              </div>
            ) : (
              <div className="bg-stone-950 text-green-400 font-mono text-sm p-4 rounded-xl border-2 border-stone-700 h-[600px] overflow-auto whitespace-pre-wrap">
                {output}
              </div>
            )}
          </div>
        </div>

        {/* Tips */}
        <div className="mt-8 bg-stone-800 backdrop-blur-sm rounded-xl p-6 border-2 border-stone-700">
          <h3 className="text-lg font-bold text-stone-100 mb-4">💡 Tips del Playground</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-stone-300 text-sm">
            <div>
              <strong className="text-amber-600">Python:</strong> Usa print() para mostrar resultados. Soporta operaciones básicas y f-strings.
            </div>
            <div>
              <strong className="text-amber-600">JavaScript:</strong> Usa console.log() para mostrar resultados. Puedes usar todas las funciones de JS moderno.
            </div>
            <div>
              <strong className="text-amber-600">HTML/CSS:</strong> Escribe HTML completo con estilos CSS y JavaScript. ¡Se muestra en vivo!
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
