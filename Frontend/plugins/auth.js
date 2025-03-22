// plugins/auth.js
export default defineNuxtPlugin(async () => {
    // Only run on client-side
    if (process.client) {
      const { fetchUserProfile } = useAuth();
      
      // Try to restore user session on page refresh if token exists
      const token = localStorage.getItem('auth_token');
      if (token) {
        await fetchUserProfile();
      }
    }
  });