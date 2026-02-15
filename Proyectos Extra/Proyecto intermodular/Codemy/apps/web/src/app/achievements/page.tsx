'use client';

import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import AchievementsDisplay from '@/components/achievements/AchievementsDisplay';

export default function AchievementsPage() {
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
            <h1 className="text-2xl font-bold text-stone-100">🏆 Logros</h1>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AchievementsDisplay />
      </div>
    </div>
  );
}
