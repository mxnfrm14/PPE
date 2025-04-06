import { useRuntimeConfig } from 'nuxt/app';
import { useAuth } from '~/composables/useAuth';

export function useApi() {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBaseUrl;
  const { token } = useAuth();

  const getHeaders = () => {
    return {
      'Authorization': `Bearer ${token.value}`
    };
  };

  const checkAuth = () => {
    if (!token.value) {
      throw new Error('Vous devez être connecté pour accéder à cette fonctionnalité');
    }
  };

  return {
    apiBase,
    token,
    getHeaders,
    checkAuth
  };
}
