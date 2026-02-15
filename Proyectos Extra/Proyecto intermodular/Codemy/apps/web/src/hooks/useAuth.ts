'use client';

import { useSession, signOut as nextAuthSignOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';

export function useAuth() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const loading = status === 'loading';
  const user = session?.user;

  const signOut = async () => {
    await nextAuthSignOut({ redirect: false });
    router.push('/');
    router.refresh();
  };

  return {
    user: user ? {
      id: user.id,
      email: user.email,
      name: user.name,
      image: user.image,
      role: (user as any).role,
    } : null,
    session,
    loading,
    signOut,
    isAuthenticated: !!user,
  };
}
