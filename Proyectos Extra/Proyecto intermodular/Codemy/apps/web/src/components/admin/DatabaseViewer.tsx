'use client';

import { useState, useEffect } from 'react';
import { Database, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react';

interface DatabaseViewerProps {
  tables: string[];
}

export default function DatabaseViewer({ tables }: DatabaseViewerProps) {
  const [selectedTable, setSelectedTable] = useState(tables[0] || '');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [limit] = useState(20);

  useEffect(() => {
    if (selectedTable) {
      fetchTableData();
    }
  }, [selectedTable, currentPage]);

  async function fetchTableData() {
    setLoading(true);
    try {
      const offset = (currentPage - 1) * limit;
      const response = await fetch(
        `/api/admin/database?table=${selectedTable}&limit=${limit}&offset=${offset}`
      );
      const result = await response.json();

      if (response.ok) {
        setData(result.data || []);
        setTotalCount(result.count || 0);
      } else {
        console.error('Error fetching table data:', result.error);
        setData([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setData([]);
    } finally {
      setLoading(false);
    }
  }

  const totalPages = Math.ceil(totalCount / limit);
  const columns = data.length > 0 ? Object.keys(data[0]) : [];

  return (
    <div className="bg-stone-800 border border-stone-700 rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Database className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Base de Datos</h2>
        </div>
        <button
          onClick={fetchTableData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Actualizar
        </button>
      </div>

      {/* Selector de tablas */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-stone-300 mb-2">
          Tabla
        </label>
        <select
          value={selectedTable}
          onChange={(e) => {
            setSelectedTable(e.target.value);
            setCurrentPage(1);
          }}
          className="w-full px-4 py-2 bg-stone-900 border border-stone-700 rounded-lg text-stone-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {tables.map((table) => (
            <option key={table} value={table}>
              {table}
            </option>
          ))}
        </select>
      </div>

      {/* Info */}
      <div className="mb-4 text-sm text-stone-400">
        Total de registros: <span className="text-white font-semibold">{totalCount}</span>
      </div>

      {/* Tabla de datos */}
      <div className="overflow-x-auto">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
          </div>
        ) : data.length === 0 ? (
          <div className="text-center py-12 text-stone-400">
            No hay datos en esta tabla
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-700">
                {columns.map((col) => (
                  <th
                    key={col}
                    className="text-left py-3 px-4 text-stone-300 font-semibold whitespace-nowrap"
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr
                  key={idx}
                  className="border-b border-stone-800 hover:bg-stone-700/50 transition-colors"
                >
                  {columns.map((col) => (
                    <td
                      key={col}
                      className="py-3 px-4 text-stone-300 max-w-xs truncate"
                      title={String(row[col])}
                    >
                      {typeof row[col] === 'object' && row[col] !== null
                        ? JSON.stringify(row[col])
                        : String(row[col] ?? '-')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Paginación */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <div className="text-sm text-stone-400">
            Página {currentPage} de {totalPages}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="flex items-center gap-1 px-3 py-2 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
              Anterior
            </button>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="flex items-center gap-1 px-3 py-2 bg-stone-700 text-stone-200 rounded-lg hover:bg-stone-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
