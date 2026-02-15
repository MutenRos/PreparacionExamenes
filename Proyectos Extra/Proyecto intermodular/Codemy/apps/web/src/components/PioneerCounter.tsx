'use client';

import { useEffect, useState } from 'react';

export function PioneerCounter() {
  const [slotsRemaining, setSlotsRemaining] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSlots() {
      try {
        const response = await fetch('/api/pioneer/slots');
        const data = await response.json();
        setSlotsRemaining(data.slotsRemaining);
      } catch (error) {
        console.error('Error fetching pioneer slots:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchSlots();
    const interval = setInterval(fetchSlots, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading || slotsRemaining === null || slotsRemaining <= 0) {
    return null;
  }

  return (
    <div className="border border-stone-800 rounded-lg p-6 mb-8 bg-stone-900/50">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="text-lg font-semibold text-white mb-1">
            Programa Pionero
          </h3>
          <p className="text-stone-400 text-sm">
            Acceso gratuito permanente para las primeras 100 personas
          </p>
        </div>
        
        <div className="text-right">
          <div className="text-3xl font-bold text-purple-400">
            {slotsRemaining}
          </div>
          <div className="text-stone-500 text-xs">
            plazas disponibles
          </div>
        </div>
      </div>

      <div className="h-2 bg-stone-800 rounded-full overflow-hidden">
        <div 
          className="h-full bg-purple-600 transition-all duration-500"
          style={{ width: `${(slotsRemaining / 100) * 100}%` }}
        ></div>
      </div>
    </div>
  );
}
