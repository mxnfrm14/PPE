<template>
    <nav class="navbar">
      <div class="nav-logo">
        <NuxtLink to="/">E-Garden</NuxtLink>
      </div>
      <div class="nav-links">
        <NuxtLink to="/" class="nav-link">Accueil</NuxtLink>
        <NuxtLink to="/ppe" class="nav-link">Gestion des Semis</NuxtLink>
        <NuxtLink v-if="isAdmin" to="/explore" class="nav-link">Admin</NuxtLink>
      </div>
      <div class="nav-auth">
        <template v-if="isAuthenticated">
          <div class="user-info">
            <span class="username">{{ user?.username }}</span>
            <button @click="handleLogout" class="logout-btn">Déconnexion</button>
          </div>
        </template>
        <template v-else>
          <NuxtLink to="/login" class="auth-btn login">Connexion</NuxtLink>
          <NuxtLink to="/register" class="auth-btn register">Inscription</NuxtLink>
        </template>
      </div>
    </nav>
  </template>
  
  <script setup>
  // Utilise le composable d'authentification
  const { user, isAuthenticated, logout } = useAuth();
  
  // Déconnexion de l'utilisateur
  const handleLogout = () => {
    logout();
    navigateTo('/login');
  };
  
  // On considère l'utilisateur "admin" si son nom d'utilisateur est "admin"
  // À adapter selon votre logique d'administration
  const isAdmin = computed(() => user.value?.username === 'admin');
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .nav-logo a {
    font-family: "Aeonik-Bold";
    font-size: 1.5rem;
    color: #4CAF50;
    text-decoration: none;
  }
  
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-link {
    font-family: "Aeonik-Regular";
    color: #333;
    text-decoration: none;
    position: relative;
  }
  
  .nav-link:hover {
    color: #4CAF50;
  }
  
  .nav-link:hover::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #4CAF50;
  }
  
  .nav-auth {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .auth-btn {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-family: "Aeonik-Medium";
    text-decoration: none;
    transition: background-color 0.3s;
  }
  
  .auth-btn.login {
    color: #4CAF50;
    border: 1px solid #4CAF50;
  }
  
  .auth-btn.login:hover {
    background-color: rgba(76, 175, 80, 0.1);
  }
  
  .auth-btn.register {
    background-color: #4CAF50;
    color: white;
  }
  
  .auth-btn.register:hover {
    background-color: #45a049;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .username {
    font-family: "Aeonik-Medium";
    color: #333;
  }
  
  .logout-btn {
    background-color: #f5f5f5;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-family: "Aeonik-Medium";
    color: #f44336;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .logout-btn:hover {
    background-color: #ffebee;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .navbar {
      flex-direction: column;
      padding: 1rem;
      gap: 1rem;
    }
    
    .nav-links {
      width: 100%;
      justify-content: center;
    }
    
    .nav-auth {
      width: 100%;
      justify-content: center;
    }
  }
  </style>