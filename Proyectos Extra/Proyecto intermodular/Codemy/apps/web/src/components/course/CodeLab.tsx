'use client';

import { useState } from 'react';

interface CodeLabProps {
  challenge?: string;
  starterCode?: string;
  solution?: string;
  language?: string;
  lab?: any;
  lessonId?: string;
}

export function CodeLab({ challenge, starterCode, solution, language, lab, lessonId }: CodeLabProps) {
  const labData = lab || { title: challenge, description: '', exercises: [] };
  const [code, setCode] = useState(starterCode || '// Escribe tu código aquí');
  const [output, setOutput] = useState('');
  const [showSolution, setShowSolution] = useState(false);

  const handleRun = () => {
    setOutput('// Ejecutando código...\n// Sandbox de ejecución en desarrollo\n// Tu código será evaluado aquí');
  };

  const handleReset = () => {
    setCode(starterCode || '// Escribe tu código aquí');
    setOutput('');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="bg-gray-900 text-white p-4">
        <h3 className="font-bold mb-2">🚀 Laboratorio de Código</h3>
        <p className="text-sm text-gray-300">{challenge || labData.title}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4 p-4">
        {/* Editor */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Editor ({language || 'code'})</span>
            <div className="space-x-2">
              <button
                onClick={handleReset}
                className="text-xs px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
              >
                Resetear
              </button>
              <button
                onClick={() => setShowSolution(!showSolution)}
                className="text-xs px-3 py-1 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
              >
                {showSolution ? 'Ocultar' : 'Ver'} Solución
              </button>
            </div>
          </div>
          <textarea
            value={showSolution ? (solution || code) : code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-64 p-4 font-mono text-sm bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            spellCheck={false}
          />
          <button
            onClick={handleRun}
            className="mt-2 w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
          >
            ▶ Ejecutar Código
          </button>
        </div>

        {/* Output */}
        <div>
          <span className="text-sm font-medium text-gray-700 block mb-2">Salida</span>
          <div className="w-full h-64 p-4 font-mono text-sm bg-gray-900 text-green-400 rounded-lg overflow-auto">
            {output || '// La salida aparecerá aquí...'}
          </div>
          
          <div className="mt-4 p-4 bg-stone-50 border-l-4 border-stone-500 rounded">
            <p className="text-sm text-stone-900">
              <strong>💡 Tip:</strong> Prueba diferentes enfoques y experimenta con el código.
              El aprendizaje viene de la práctica.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
