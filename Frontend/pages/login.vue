<template>
    <div class="login-page">
      <Header_title title="E-Garden" subtitle="Connexion à votre jardin intelligent" />
      
      <div class="login-container">
        <div class="login-card">
          <div class="tabs">
            <button 
              class="tab-button" 
              :class="{ active: activeTab === 'login' }" 
              @click="activeTab = 'login'"
            >
              Connexion
            </button>
            <button 
              class="tab-button" 
              :class="{ active: activeTab === 'register' }" 
              @click="activeTab = 'register'"
            >
              Inscription
            </button>
          </div>
          
          <!-- Login Form -->
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="form">
            <div class="form-group">
              <label for="login-username">Nom d'utilisateur</label>
              <input 
                type="text" 
                id="login-username" 
                v-model="loginForm.username" 
                required
                placeholder="Entrez votre nom d'utilisateur"
              />
            </div>
            
            <div class="form-group">
              <label for="login-password">Mot de passe</label>
              <input 
                type="password" 
                id="login-password" 
                v-model="loginForm.password" 
                required
                placeholder="Entrez votre mot de passe"
              />
            </div>
            
            <div class="error-message" v-if="loginError">
              {{ loginError }}
            </div>
            
            <button type="submit" class="submit-button" :disabled="isLoading">
              {{ isLoading ? 'Connexion en cours...' : 'Se connecter' }}
            </button>
          </form>
          
          <!-- Register Form -->
          <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="form">
            <div class="form-group">
              <label for="register-username">Nom d'utilisateur</label>
              <input 
                type="text" 
                id="register-username" 
                v-model="registerForm.username" 
                required
                placeholder="Choisissez un nom d'utilisateur"
              />
            </div>
            
            <div class="form-group">
              <label for="register-email">Email</label>
              <input 
                type="email" 
                id="register-email" 
                v-model="registerForm.email" 
                required
                placeholder="Entrez votre adresse email"
              />
            </div>
            
            <div class="form-group">
              <label for="register-password">Mot de passe</label>
              <input 
                type="password" 
                id="register-password" 
                v-model="registerForm.password" 
                required
                placeholder="Choisissez un mot de passe"
              />
            </div>
            
            <div class="form-group">
              <label for="register-confirm-password">Confirmer le mot de passe</label>
              <input 
                type="password" 
                id="register-confirm-password" 
                v-model="registerForm.confirmPassword" 
                required
                placeholder="Confirmez votre mot de passe"
              />
            </div>
            
            <div class="error-message" v-if="registerError">
              {{ registerError }}
            </div>
            
            <button type="submit" class="submit-button" :disabled="isLoading">
              {{ isLoading ? 'Inscription en cours...' : 'S\'inscrire' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuth } from '~/composables/useAuth';
  import Header_title from '~/components/header_title.vue';
  
  const router = useRouter();
  const activeTab = ref('login');
  
  // Use the auth composable
  const { login, register, isLoading, error } = useAuth();
  
  // Local form state
  const loginForm = ref({
    username: '',
    password: ''
  });
  
  const registerForm = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  // Local error state
  const loginError = ref('');
  const registerError = ref('');
  
  // Handle login
  const handleLogin = async () => {
    loginError.value = '';
    
    try {
      await login({
        username: loginForm.value.username,
        password: loginForm.value.password
      });
      
      // Navigate to PPE page after successful login
      router.push('/ppe');
    } catch (err) {
      loginError.value = err.message || 'Erreur de connexion';
      console.error('Login error:', err);
    }
  };
  
  // Handle registration
  const handleRegister = async () => {
    registerError.value = '';
    
    // Validate passwords match
    if (registerForm.value.password !== registerForm.value.confirmPassword) {
      registerError.value = 'Les mots de passe ne correspondent pas';
      return;
    }
    
    try {
      await register({
        username: registerForm.value.username,
        email: registerForm.value.email,
        password: registerForm.value.password
      });
      
      // Switch to login tab after successful registration
      activeTab.value = 'login';
      
      // Pre-fill the login form with the registered username
      loginForm.value.username = registerForm.value.username;
      loginForm.value.password = '';
      
      // Reset register form
      registerForm.value = {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      };
      
      // Show success message
      alert('Inscription réussie ! Vous pouvez maintenant vous connecter.');
    } catch (err) {
      registerError.value = err.message || 'Erreur lors de l\'inscription';
      console.error('Registration error:', err);
    }
  };
  </script>
  
  <style scoped>
  .login-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 20px;
  }
  
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
    padding: 2rem 0;
  }
  
  .login-card {
    background-color: white;
    border-radius: 1rem;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .tabs {
    display: flex;
    border-bottom: 1px solid #eee;
  }
  
  .tab-button {
    flex: 1;
    padding: 1rem;
    background: none;
    border: none;
    font-family: 'Aeonik-Medium';
    font-size: 1rem;
    color: #888;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .tab-button.active {
    color: #4caf50;
    border-bottom: 2px solid #4caf50;
  }
  
  .form {
    padding: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    font-family: 'Aeonik-Medium';
    color: #333;
    margin-bottom: 0.5rem;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: border-color 0.3s;
  }
  
  .form-group input:focus {
    border-color: #4caf50;
    outline: none;
  }
  
  .submit-button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-family: 'Aeonik-Bold';
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .submit-button:hover:not(:disabled) {
    background-color: #45a049;
  }
  
  .submit-button:disabled {
    background-color: #a5d6a7;
    cursor: not-allowed;
  }
  
  .error-message {
    color: #f44336;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 600px) {
    .login-card {
      max-width: 100%;
    }
    
    .form {
      padding: 1.5rem;
    }
  }
  </style>