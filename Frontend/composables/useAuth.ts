// composables/useAuth.js
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useRuntimeConfig } from "nuxt/app";

export const useAuth = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBaseUrl;

  const token = ref(null);
  const user = ref(null);
  const error = ref(null);
  const isLoading = ref(false);
  const isAuthenticated = ref(false);

  // Check if we're in the browser
  const isClient = process.client;

  // Initialize auth state from localStorage if in browser
  const initAuth = () => {
    if (isClient) {
      const storedToken = localStorage.getItem("auth_token");
      const storedUser = localStorage.getItem("user");

      if (storedToken) {
        token.value = storedToken;
        isAuthenticated.value = true;
      }

      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser);
        } catch (e) {
          console.error("Failed to parse stored user data");
        }
      }
    }
  };

  // Call initAuth when the composable is used
  initAuth();

  // Register a new user
  const register = async (userData) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $fetch(`${apiBase}/auth/register`, {
        method: "POST",
        body: userData,
      });

      return response;
    } catch (err) {
      console.error("Registration error:", err);
      error.value =
        err.message || "Une erreur s'est produite lors de l'inscription";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Login a user
  const login = async (credentials) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Convert credentials to FormData for OAuth2 password flow
      const formData = new FormData();
      formData.append("username", credentials.username);
      formData.append("password", credentials.password);

      const response = await $fetch(`${apiBase}/auth/token`, {
        method: "POST",
        body: formData,
      });

      // Store token and user info
      if (response.access_token) {
        token.value = response.access_token;
        isAuthenticated.value = true;

        // Get user profile
        await fetchUserProfile();

        // Save to localStorage if in browser
        if (isClient) {
          localStorage.setItem("auth_token", token.value);
          if (user.value) {
            localStorage.setItem("user", JSON.stringify(user.value));
          }
        }

        return response;
      } else {
        throw new Error("Échec de connexion: jeton d'accès manquant");
      }
    } catch (err) {
      console.error("Login error:", err);
      error.value =
        err.message || "Nom d'utilisateur ou mot de passe incorrect";
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Fetch the user profile
  const fetchUserProfile = async () => {
    if (!token.value) return null;

    try {
      const response = await $fetch(`${apiBase}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      user.value = response;
      return response;
    } catch (err) {
      console.error("Error fetching user profile:", err);
      return null;
    }
  };

  // Logout
  // Modification de la fonction logout pour qu'elle soit asynchrone et utilise navigateTo
  const logout = async () => {
    token.value = null;
    user.value = null;
    isAuthenticated.value = false;

    // Clear localStorage if in browser
    if (isClient) {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
    }

    // Utiliser navigateTo au lieu de router.push
    return navigateTo("/login", { replace: true });
  };

  // Provide the auth state and methods
  return {
    user,
    token,
    error,
    isLoading,
    isAuthenticated,
    register,
    login,
    logout,
    fetchUserProfile,
  };
};
