// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const { isAuthenticated } = useAuth();
    const token = localStorage.getItem('auth_token');
    
    // If route requires auth and no token exists, redirect to login
    if (!token && !isAuthenticated.value) {
      return navigateTo('/login');
    }
  }
});