'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function CoursesPage() {
  const router = useRouter();
  
  useEffect(() => {
    router.replace('/skill-tree');
  }, [router]);
  
  return (
    <div className="min-h-screen bg-stone-900 flex items-center justify-center">
      <div className="text-stone-100 text-xl">Redirigiendo al árbol de habilidades...</div>
    </div>
  );
}
