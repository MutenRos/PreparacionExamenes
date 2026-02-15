export default function DashboardLoading() {
  return (
    <div className="min-h-screen bg-stone-950 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Stats row skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-stone-900 border-2 border-stone-800 rounded-lg p-6">
              <div className="h-4 w-20 bg-stone-800 rounded animate-pulse mb-3"></div>
              <div className="h-8 w-24 bg-stone-700 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
        
        {/* Main content skeleton */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-stone-900 border-2 border-stone-800 rounded-lg p-6">
            <div className="h-6 w-40 bg-stone-800 rounded animate-pulse mb-6"></div>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-16 bg-stone-800/50 rounded animate-pulse"></div>
              ))}
            </div>
          </div>
          <div className="bg-stone-900 border-2 border-stone-800 rounded-lg p-6">
            <div className="h-6 w-32 bg-stone-800 rounded animate-pulse mb-6"></div>
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-10 bg-stone-800/50 rounded animate-pulse"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
