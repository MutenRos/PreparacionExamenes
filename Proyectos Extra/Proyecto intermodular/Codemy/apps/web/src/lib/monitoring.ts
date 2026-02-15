/**
 * Monitoring y Logging Utilities
 * Helper para tracking de eventos y errores
 */

type LogLevel = 'info' | 'warn' | 'error';

interface LogEvent {
  level: LogLevel;
  message: string;
  context?: Record<string, any>;
  timestamp: string;
  environment: string;
}

class Logger {
  private isDev = process.env.NODE_ENV === 'development';
  private isProd = process.env.NODE_ENV === 'production';

  private formatLog(event: LogEvent): string {
    return JSON.stringify({
      ...event,
      service: 'codeacademy-web',
    });
  }

  info(message: string, context?: Record<string, any>) {
    const event: LogEvent = {
      level: 'info',
      message,
      context,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
    };

    if (this.isDev) {
      console.log(`ℹ️ ${message}`, context || '');
    } else {
      console.log(this.formatLog(event));
    }
  }

  warn(message: string, context?: Record<string, any>) {
    const event: LogEvent = {
      level: 'warn',
      message,
      context,
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
    };

    if (this.isDev) {
      console.warn(`⚠️ ${message}`, context || '');
    } else {
      console.warn(this.formatLog(event));
    }
  }

  error(message: string, error?: Error | unknown, context?: Record<string, any>) {
    const event: LogEvent = {
      level: 'error',
      message,
      context: {
        ...context,
        error: error instanceof Error ? {
          name: error.name,
          message: error.message,
          stack: error.stack,
        } : error,
      },
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development',
    };

    if (this.isDev) {
      console.error(`❌ ${message}`, error, context || '');
    } else {
      console.error(this.formatLog(event));
    }

    // En producción, también enviar a Sentry si está configurado
    if (this.isProd && typeof window !== 'undefined' && (window as any).Sentry) {
      (window as any).Sentry.captureException(error, {
        tags: context,
      });
    }
  }
}

export const logger = new Logger();

/**
 * Track de eventos de analytics
 */
export function trackEvent(
  eventName: string,
  properties?: Record<string, any>
) {
  // PostHog
  if (typeof window !== 'undefined' && (window as any).posthog) {
    (window as any).posthog.capture(eventName, properties);
  }

  // Vercel Analytics
  if (typeof window !== 'undefined' && (window as any).va) {
    (window as any).va('event', eventName, properties);
  }

  logger.info(`Event: ${eventName}`, properties);
}

/**
 * Track de pageviews
 */
export function trackPageView(url: string) {
  trackEvent('pageview', { url });
}

/**
 * Track de conversión (signup, purchase, etc.)
 */
export function trackConversion(
  type: 'signup' | 'purchase' | 'trial_start' | 'subscription',
  properties?: Record<string, any>
) {
  trackEvent(`conversion_${type}`, properties);
}
