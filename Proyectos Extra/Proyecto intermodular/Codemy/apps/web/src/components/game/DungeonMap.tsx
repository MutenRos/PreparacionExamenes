'use client';

import { useState } from 'react';
import Link from 'next/link';

interface DungeonRoom {
  id: number;
  title: string;
  type: 'entrance' | 'room' | 'boss' | 'treasure';
  status: 'locked' | 'available' | 'completed';
  enemies?: number;
  xp?: number;
}

interface DungeonMapProps {
  courseId: string;
  courseTitle: string;
  courseIcon: string;
  rooms: DungeonRoom[];
  totalXP: number;
  earnedXP: number;
}

export default function DungeonMap({ courseId, courseTitle, courseIcon, rooms, totalXP, earnedXP }: DungeonMapProps) {
  const [hoveredRoom, setHoveredRoom] = useState<number | null>(null);
  const progress = (earnedXP / totalXP) * 100;
  
  const getRoomStyle = (room: DungeonRoom) => {
    const base = "relative w-16 h-16 rounded-lg border-2 flex items-center justify-center transition-all cursor-pointer";
    if (room.status === 'completed') return base + " bg-green-900/50 border-green-500 text-green-400";
    if (room.status === 'available') return base + " bg-amber-900/50 border-amber-500 text-amber-400 animate-pulse";
    return base + " bg-gray-900/50 border-gray-700 text-gray-600";
  };
  
  const getRoomIcon = (room: DungeonRoom) => {
    if (room.status === 'locked') return '🔒';
    if (room.type === 'entrance') return '🚪';
    if (room.type === 'boss') return '💀';
    if (room.type === 'treasure') return '💎';
    return room.status === 'completed' ? '✅' : '⚔️';
  };
  
  return (
    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
      <div className="flex items-center gap-4 mb-6">
        <div className="text-4xl">{courseIcon}</div>
        <div>
          <h2 className="text-xl font-bold text-white">Mazmorra: {courseTitle}</h2>
          <div className="flex items-center gap-2 mt-1">
            <div className="flex-1 bg-gray-700 rounded-full h-2 w-48">
              <div className="h-full rounded-full bg-gradient-to-r from-amber-600 to-yellow-400" style={{ width: progress + '%' }} />
            </div>
            <span className="text-xs text-gray-400">{earnedXP}/{totalXP} XP</span>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-4 gap-4">
        {rooms.map((room) => (
          <Link key={room.id} href={room.status !== 'locked' ? '/course/' + courseId + '/lesson/' + room.id : '#'}
            className={getRoomStyle(room)}
            onMouseEnter={() => setHoveredRoom(room.id)}
            onMouseLeave={() => setHoveredRoom(null)}
            onClick={(e) => room.status === 'locked' && e.preventDefault()}>
            <span className="text-2xl">{getRoomIcon(room)}</span>
            <div className="absolute -top-2 -left-2 bg-gray-800 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold border border-gray-600">{room.id}</div>
            {room.enemies && room.status !== 'completed' && (
              <div className="absolute -top-2 -right-2 bg-red-600 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">{room.enemies}</div>
            )}
            {hoveredRoom === room.id && (
              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 bg-gray-800 rounded-lg px-3 py-2 text-sm whitespace-nowrap z-10 border border-gray-700">
                <div className="font-bold text-white">{room.title}</div>
                {room.xp && <div className="text-amber-400 text-xs">+{room.xp} XP</div>}
              </div>
            )}
          </Link>
        ))}
      </div>
      
      <div className="flex gap-6 mt-6 text-xs text-gray-400">
        <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-green-900 border border-green-500" /><span>Completada</span></div>
        <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-amber-900 border border-amber-500" /><span>Disponible</span></div>
        <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-gray-900 border border-gray-700" /><span>Bloqueada</span></div>
      </div>
    </div>
  );
}
