'use client';

import SupportWidget from './SupportWidget';
import NotificationToast from './notifications/NotificationToast';

export function ClientComponents() {
  console.log('🟢 ClientComponents renderizando');
  return (
    <>
      <NotificationToast />
      <SupportWidget />
    </>
  );
}
