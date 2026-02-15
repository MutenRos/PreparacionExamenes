export default function Loading() {
  return (
    <div className="min-h-screen bg-stone-950 flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-amber-700/30 rounded-full"></div>
          <div className="absolute top-0 left-0 w-16 h-16 border-4 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
        <p className="text-stone-400 text-sm animate-pulse">Cargando...</p>
      </div>
    </div>
  );
}
