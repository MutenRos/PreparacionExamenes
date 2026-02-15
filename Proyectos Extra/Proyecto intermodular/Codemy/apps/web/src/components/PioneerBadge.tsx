'use client';

import { useEffect, useState } from 'react';
import { Star, Zap } from 'lucide-react';

interface PioneerBadgeProps {
  userId?: string;
}

export function PioneerBadge({ userId }: PioneerBadgeProps) {
  const [pioneerInfo, setPioneerInfo] = useState<{
    isPioneer: boolean;
    pioneerNumber?: number;
    grantedAt?: string;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPioneerInfo() {
      try {
        const response = await fetch(`/api/pioneer/info${userId ? `?userId=${userId}` : ''}`);
        const data = await response.json();
        setPioneerInfo(data);
      } catch (error) {
        console.error('Error fetching pioneer info:', error);
        setPioneerInfo({ isPioneer: false });
      } finally {
        setLoading(false);
      }
    }

    fetchPioneerInfo();
  }, [userId]);

  if (loading) {
    return (
      <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-stone-800 rounded-lg animate-pulse">
        <div className="w-20 h-4 bg-stone-700 rounded"></div>
      </div>
    );
  }

  if (!pioneerInfo?.isPioneer) {
    return null;
  }

  return (
    <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-amber-900/30 to-amber-800/30 border-2 border-amber-700/50 rounded-lg shadow-lg backdrop-blur-sm">
      <div className="relative">
        <Star className="w-5 h-5 text-amber-400 fill-amber-400" />
        <Zap className="w-3 h-3 text-amber-300 absolute -top-1 -right-1 animate-pulse" />
      </div>
      <div className="flex flex-col">
        <span className="text-sm font-bold text-amber-400">
          Usuario Pionero #{pioneerInfo.pioneerNumber}
        </span>
        <span className="text-xs text-amber-500/80">
          Acceso de por vida
        </span>
      </div>
    </div>
  );
}
