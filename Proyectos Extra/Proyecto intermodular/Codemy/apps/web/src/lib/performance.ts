// Utilidades de optimización de rendimiento

import { useEffect, useRef } from 'react';

// Debounce para evitar ejecuciones excesivas
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeoutId = null;
      func(...args);
    };

    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(later, wait);
  };
}

// Throttle para limitar frecuencia de ejecución
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  
  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Hook para detectar si un elemento está visible (lazy loading)
export function useIntersectionObserver(
  elementRef: React.RefObject<Element>,
  options: IntersectionObserverInit = {}
): boolean {
  const [isVisible, setIsVisible] = React.useState(false);

  React.useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsVisible(entry.isIntersecting);
    }, options);

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [elementRef, options]);

  return isVisible;
}

// Preload de datos críticos
export function preloadData(moduleLoader: () => Promise<any>) {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = 'fetch';
  link.crossOrigin = 'anonymous';
  
  moduleLoader().catch(() => {
    // Silently fail preload
  });
}

// Caché en memoria para evitar recálculos
class MemoryCache<T> {
  private cache: Map<string, { data: T; timestamp: number }> = new Map();
  private maxAge: number;

  constructor(maxAgeMs: number = 5 * 60 * 1000) {
    this.maxAge = maxAgeMs;
  }

  set(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });
  }

  get(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) return null;

    const age = Date.now() - item.timestamp;
    if (age > this.maxAge) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  clear(): void {
    this.cache.clear();
  }

  has(key: string): boolean {
    return this.get(key) !== null;
  }
}

export const lessonCache = new MemoryCache<any>(10 * 60 * 1000); // 10 minutos

// Optimizar localStorage con caché
export const optimizedLocalStorage = {
  cache: new Map<string, any>(),

  getItem(key: string): string | null {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const value = localStorage.getItem(key);
    if (value !== null) {
      this.cache.set(key, value);
    }
    return value;
  },

  setItem(key: string, value: string): void {
    this.cache.set(key, value);
    localStorage.setItem(key, value);
  },

  removeItem(key: string): void {
    this.cache.delete(key);
    localStorage.removeItem(key);
  },

  clear(): void {
    this.cache.clear();
    localStorage.clear();
  },
};

// Comprimir datos JSON antes de guardar en localStorage
export function compressJSON(data: any): string {
  const json = JSON.stringify(data);
  // Simple compression: remove whitespace
  return json;
}

export function decompressJSON(compressed: string): any {
  return JSON.parse(compressed);
}

// Batch updates para evitar re-renders excesivos
export function batchUpdates<T>(
  updates: Array<() => void>,
  callback?: () => void
): void {
  React.startTransition(() => {
    updates.forEach(update => update());
    callback?.();
  });
}

// Virtual scrolling helper
export function calculateVisibleItems(
  scrollTop: number,
  itemHeight: number,
  containerHeight: number,
  totalItems: number
): { start: number; end: number } {
  const start = Math.floor(scrollTop / itemHeight);
  const visibleCount = Math.ceil(containerHeight / itemHeight);
  const end = Math.min(start + visibleCount + 1, totalItems);

  return { start, end };
}

// Lazy load images
export function lazyLoadImage(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = reject;
    img.src = src;
  });
}

// Prefetch para navigation
export function prefetchRoute(href: string): void {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = href;
  document.head.appendChild(link);
}

// Hook para prevenir re-renders innecesarios
export function useDeepCompareMemo<T>(factory: () => T, deps: any[]): T {
  const ref = useRef<any[]>(undefined);
  const signalRef = useRef<number>(0);

  if (!ref.current || !deepEqual(deps, ref.current)) {
    ref.current = deps;
    signalRef.current += 1;
  }

  return React.useMemo(factory, [signalRef.current]);
}

function deepEqual(a: any, b: any): boolean {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (typeof a !== 'object' || typeof b !== 'object') return false;

  const keysA = Object.keys(a);
  const keysB = Object.keys(b);

  if (keysA.length !== keysB.length) return false;

  return keysA.every(key => deepEqual(a[key], b[key]));
}

// React import for hooks
import React from 'react';
