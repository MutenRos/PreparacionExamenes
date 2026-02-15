'use client';

import { useState, useRef } from 'react';
import { useIsVisible } from '@/hooks/useOptimized';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
  placeholder?: 'blur' | 'empty';
  blurDataURL?: string;
}

/**
 * Componente de imagen optimizado con lazy loading nativo
 * y placeholder blur mientras carga
 */
export default function OptimizedImage({
  src,
  alt,
  width,
  height,
  className = '',
  priority = false,
  placeholder = 'blur',
  blurDataURL,
}: OptimizedImageProps) {
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);
  const imgRef = useRef<HTMLDivElement>(null);
  const isVisible = useIsVisible(imgRef);

  // Placeholder blur por defecto (1x1 pixel gris)
  const defaultBlur = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
  const blur = blurDataURL || defaultBlur;

  const shouldLoad = priority || isVisible;

  if (error) {
    return (
      <div
        className={`bg-stone-800 flex items-center justify-center ${className}`}
        style={{ width, height }}
      >
        <span className="text-stone-500 text-sm">Error al cargar imagen</span>
      </div>
    );
  }

  return (
    <div ref={imgRef} className={`relative overflow-hidden ${className}`} style={{ width, height }}>
      {/* Placeholder blur */}
      {placeholder === 'blur' && !loaded && (
        <div
          className="absolute inset-0 bg-cover bg-center blur-lg scale-110 transition-opacity duration-300"
          style={{ 
            backgroundImage: `url(${blur})`,
            opacity: loaded ? 0 : 1 
          }}
        />
      )}
      
      {/* Imagen real */}
      {shouldLoad && (
        <img
          src={src}
          alt={alt}
          width={width}
          height={height}
          loading={priority ? 'eager' : 'lazy'}
          decoding="async"
          onLoad={() => setLoaded(true)}
          onError={() => setError(true)}
          className={`
            w-full h-full object-cover transition-opacity duration-300
            ${loaded ? 'opacity-100' : 'opacity-0'}
          `}
        />
      )}
      
      {/* Skeleton mientras no es visible */}
      {!shouldLoad && (
        <div className="absolute inset-0 bg-stone-800 animate-pulse" />
      )}
    </div>
  );
}
