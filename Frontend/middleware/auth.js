// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const { isAuthenticated } = useAuth();
    const token = localStorage.getItem('auth_token');
    
    // Vérification plus stricte
    if (!token || !isAuthenticated.value) {
      console.log('Redirection vers login depuis le middleware auth');
      return navigateTo('/login');
    }
  }
});