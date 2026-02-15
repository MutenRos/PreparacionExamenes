import Forum from '@/components/Forum'

export default function ForoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-stone-900 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <Forum 
          title="Foro General de Code Dungeon"
          categories={['General', 'Preguntas', 'Proyectos', 'Recursos', 'Eventos', 'Off-Topic']}
        />
      </div>
    </div>
  )
}
