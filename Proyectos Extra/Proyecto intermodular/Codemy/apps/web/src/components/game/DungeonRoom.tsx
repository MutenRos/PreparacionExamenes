'use client';

import { useState } from 'react';
import SpriteGenerator from './SpriteGenerator';
import EnemySprite, { EnemyType } from './EnemySprite';

interface Exercise {
  id: number;
  question: string;
  options?: string[];
  correctAnswer: string | number;
  xpReward: number;
  enemyType: EnemyType;
  enemyName: string;
}

interface DungeonRoomProps {
  lessonId: number;
  lessonTitle: string;
  content: string;
  exercises: Exercise[];
  userId: string;
  onComplete: (xpEarned: number) => void;
}

export default function DungeonRoom({ lessonId, lessonTitle, content, exercises, userId, onComplete }: DungeonRoomProps) {
  const [currentExercise, setCurrentExercise] = useState(0);
  const [defeatedEnemies, setDefeatedEnemies] = useState<number[]>([]);
  const [playerHP, setPlayerHP] = useState(100);
  const [showBattle, setShowBattle] = useState(false);
  const [battleResult, setBattleResult] = useState<'none' | 'victory' | 'defeat'>('none');
  const [answer, setAnswer] = useState('');
  const [totalXP, setTotalXP] = useState(0);
  const [showContent, setShowContent] = useState(true);

  const currentEnemy = exercises[currentExercise];
  const allDefeated = defeatedEnemies.length === exercises.length;

  const handleAnswer = () => {
    if (!currentEnemy) return;
    const isCorrect = answer.toLowerCase().trim() === String(currentEnemy.correctAnswer).toLowerCase().trim() ||
                      (currentEnemy.options && Number(answer) === currentEnemy.correctAnswer);
    if (isCorrect) {
      setDefeatedEnemies([...defeatedEnemies, currentEnemy.id]);
      setTotalXP(prev => prev + currentEnemy.xpReward);
      setBattleResult('victory');
      setTimeout(() => {
        setBattleResult('none');
        setAnswer('');
        if (currentExercise < exercises.length - 1) setCurrentExercise(prev => prev + 1);
        else { setShowBattle(false); onComplete(totalXP + currentEnemy.xpReward); }
      }, 1500);
    } else {
      setPlayerHP(prev => Math.max(0, prev - 20));
      setBattleResult('defeat');
      setTimeout(() => { setBattleResult('none'); setAnswer(''); }, 1000);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="bg-gray-900 border-b border-gray-800 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <SpriteGenerator seed={userId} size={48} />
            <div>
              <h1 className="font-bold">Cámara {lessonId}: {lessonTitle}</h1>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-red-400">❤️</span>
                <div className="w-32 bg-gray-700 rounded-full h-2">
                  <div className="h-full rounded-full bg-gradient-to-r from-red-600 to-red-400" style={{ width: playerHP + '%' }} />
                </div>
                <span className="text-xs text-gray-400">{playerHP}/100</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-amber-400 font-bold">⭐ {totalXP} XP</div>
            <div className="text-xs text-gray-400">Enemigos: {defeatedEnemies.length}/{exercises.length}</div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6">
        <div className="flex gap-2 mb-6">
          <button onClick={() => { setShowContent(true); setShowBattle(false); }}
            className={'px-4 py-2 rounded-lg font-bold ' + (showContent && !showBattle ? 'bg-blue-600' : 'bg-gray-800')}>📜 Contenido</button>
          <button onClick={() => { setShowContent(false); setShowBattle(true); }}
            className={'px-4 py-2 rounded-lg font-bold ' + (showBattle ? 'bg-red-600' : 'bg-gray-800')} disabled={allDefeated}>⚔️ Batalla {allDefeated && '✅'}</button>
        </div>

        {showContent && !showBattle && (
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: content }} />
        )}

        {showBattle && currentEnemy && (
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-red-400 mb-2">⚔️ ¡BATALLA!</h2>
            </div>
            <div className="flex justify-between items-center mb-8 px-12">
              <div className="text-center">
                <SpriteGenerator seed={userId} size={96} showStats stats={{ level: 1, hp: playerHP, maxHp: 100, attack: 10, defense: 5 }} />
                <div className="mt-2 font-bold">Tú</div>
              </div>
              <div className="text-4xl animate-pulse">⚔️</div>
              <div className="text-center">
                <EnemySprite type={currentEnemy.enemyType} size={96} name={currentEnemy.enemyName} hp={defeatedEnemies.includes(currentEnemy.id) ? 0 : 100} maxHp={100} defeated={defeatedEnemies.includes(currentEnemy.id)} />
              </div>
            </div>
            {battleResult !== 'none' && (
              <div className={'text-center text-2xl font-bold mb-4 animate-bounce ' + (battleResult === 'victory' ? 'text-green-400' : 'text-red-400')}>
                {battleResult === 'victory' ? '✨ ¡VICTORIA! +' + currentEnemy.xpReward + ' XP' : '💥 -20 HP'}
              </div>
            )}
            {!defeatedEnemies.includes(currentEnemy.id) && battleResult === 'none' && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-bold mb-4">{currentEnemy.question}</h3>
                {currentEnemy.options ? (
                  <div className="grid grid-cols-2 gap-3">
                    {currentEnemy.options.map((opt, i) => (
                      <button key={i} onClick={() => setAnswer(String(i))} className={'p-3 rounded-lg border-2 ' + (answer === String(i) ? 'border-blue-500 bg-blue-900/30' : 'border-gray-600')}>{opt}</button>
                    ))}
                  </div>
                ) : (
                  <input type="text" value={answer} onChange={(e) => setAnswer(e.target.value)} className="w-full bg-gray-700 rounded-lg px-4 py-3 border border-gray-600 outline-none" placeholder="Respuesta..." onKeyDown={(e) => e.key === 'Enter' && handleAnswer()} />
                )}
                <button onClick={handleAnswer} className="mt-4 w-full bg-red-600 hover:bg-red-500 px-6 py-3 rounded-lg font-bold" disabled={!answer}>⚔️ ¡ATACAR!</button>
              </div>
            )}
            {allDefeated && (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">🏆</div>
                <h3 className="text-2xl font-bold text-green-400">¡Cámara Completada!</h3>
                <p className="text-amber-400 font-bold mt-2">Total: +{totalXP} XP</p>
              </div>
            )}
          </div>
        )}

        <div className="mt-6 bg-gray-900 rounded-xl p-4 border border-gray-800">
          <h3 className="font-bold mb-3">Enemigos:</h3>
          <div className="flex gap-4 flex-wrap">
            {exercises.map((ex, i) => (
              <div key={ex.id} className={'p-2 rounded-lg border ' + (i === currentExercise && showBattle ? 'border-red-500' : 'border-gray-700')}>
                <EnemySprite type={ex.enemyType} size={48} defeated={defeatedEnemies.includes(ex.id)} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
