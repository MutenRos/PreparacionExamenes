export default function CourseLoading() {
  return (
    <div className="min-h-screen bg-stone-950 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header skeleton */}
        <div className="mb-8">
          <div className="h-8 w-48 bg-stone-800 rounded animate-pulse mb-4"></div>
          <div className="h-4 w-96 bg-stone-800/50 rounded animate-pulse"></div>
        </div>
        
        {/* Progress bar skeleton */}
        <div className="h-3 w-full bg-stone-800 rounded-full mb-8 overflow-hidden">
          <div className="h-full w-1/3 bg-stone-700 animate-pulse"></div>
        </div>
        
        {/* Lessons skeleton */}
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="bg-stone-900 border-2 border-stone-800 rounded-lg p-6 flex items-center gap-4">
              <div className="w-12 h-12 bg-stone-800 rounded-lg animate-pulse"></div>
              <div className="flex-1">
                <div className="h-5 w-48 bg-stone-800 rounded animate-pulse mb-2"></div>
                <div className="h-3 w-24 bg-stone-800/50 rounded animate-pulse"></div>
              </div>
              <div className="w-16 h-8 bg-stone-800 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
