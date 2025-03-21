<template>
    <div class="db-test-page">
        <Header_title title="Test MongoDB" subtitle="Vérification de la connexion à la base de données" />
        
        <div class="test-panel">
            <h2>Test de connexion MongoDB</h2>
            <button class="test-button" @click="testConnection" :disabled="isLoading">
                {{ isLoading ? 'Test en cours...' : 'Tester la connexion' }}
            </button>
            
            <div v-if="connectionStatus" class="result-panel" :class="connectionStatus.status">
                <h3>Résultat:</h3>
                <p>{{ connectionStatus.message }}</p>
                <div v-if="connectionStatus.collections">
                    <h4>Collections trouvées:</h4>
                    <ul>
                        <li v-for="(collection, index) in connectionStatus.collections" :key="index">
                            {{ collection }}
                        </li>
                    </ul>
                    <p v-if="connectionStatus.collections.length === 0">
                        Aucune collection trouvée dans la base de données.
                    </p>
                </div>
            </div>
            
            <div class="error-message" v-if="error">
                <p>{{ error }}</p>
            </div>
        </div>
        
        <div class="user-test-panel">
            <h2>Test création utilisateur</h2>
            
            <div class="input-group">
                <label for="username">Nom d'utilisateur:</label>
                <input 
                    type="text" 
                    id="username" 
                    v-model="testUser.username" 
                    placeholder="Entrez un nom d'utilisateur"
                />
            </div>
            
            <div class="input-group">
                <label for="email">Email:</label>
                <input 
                    type="email" 
                    id="email" 
                    v-model="testUser.email" 
                    placeholder="Entrez un email"
                />
            </div>
            
            <button class="test-button" @click="createTestUser" :disabled="isCreatingUser || !testUser.username">
                {{ isCreatingUser ? 'Création en cours...' : 'Créer utilisateur test' }}
            </button>
            
            <div v-if="userCreationResult" class="result-panel" :class="userCreationResult.status">
                <h3>Résultat:</h3>
                <p>{{ userCreationResult.message }}</p>
                <p v-if="userCreationResult.user_id">ID: {{ userCreationResult.user_id }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Header_title from '~/components/header_title.vue';

// États pour le test de connexion
const isLoading = ref(false);
const connectionStatus = ref(null);
const error = ref(null);

// États pour le test de création d'utilisateur
const testUser = ref({
    username: '',
    email: ''
});
const isCreatingUser = ref(false);
const userCreationResult = ref(null);

// Fonction pour tester la connexion à MongoDB
const testConnection = async () => {
    isLoading.value = true;
    connectionStatus.value = null;
    error.value = null;
    
    try {
        
        const response = await $fetch("/api/mongodb", {
            method: 'GET'
        });
        console.log(response);
        connectionStatus.value = response;
    } catch (err) {
        error.value = err.message || 'Une erreur s\'est produite lors du test de connexion';
        connectionStatus.value = {
            status: 'error',
            message: 'Échec de la connexion à MongoDB'
        };
    } finally {
        isLoading.value = false;
    }
};

// Fonction pour créer un utilisateur test
const createTestUser = async () => {
    if (!testUser.value.username) {
        error.value = 'Le nom d\'utilisateur est requis';
        return;
    }
    
    isCreatingUser.value = true;
    userCreationResult.value = null;
    error.value = null;
    
    try {
        const response = await $fetch('/api/users/test', {
            method: 'POST',
            body: testUser.value
        });
        
        userCreationResult.value = response;
        
        // Réinitialiser le formulaire en cas de succès
        if (response.status === 'success') {
            testUser.value = {
                username: '',
                email: ''
            };
        }
    } catch (err) {
        error.value = err.message || 'Une erreur s\'est produite lors de la création de l\'utilisateur';
        userCreationResult.value = {
            status: 'error',
            message: 'Échec de la création de l\'utilisateur'
        };
    } finally {
        isCreatingUser.value = false;
    }
};
</script>

<style scoped>
.db-test-page {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.test-panel, .user-test-panel {
    background-color: #f5f5f5;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-test-panel {
    margin-top: 30px;
}

h2 {
    font-family: "Aeonik-Bold";
    color: #4CAF50;
    margin-bottom: 20px;
}

.test-button {
    font-family: "Aeonik-Bold";
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.test-button:hover:not(:disabled) {
    background-color: #45a049;
}

.test-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.result-panel {
    margin-top: 20px;
    padding: 15px;
    border-radius: 5px;
    background-color: #e8f5e9;
    border-left: 4px solid #4CAF50;
}

.result-panel.error {
    background-color: #ffebee;
    border-left-color: #f44336;
}

.result-panel h3 {
    font-family: "Aeonik-Bold";
    margin-bottom: 10px;
    color: #333;
}

.result-panel p {
    font-family: "Aeonik-Regular";
    color: #555;
}

.error-message {
    margin-top: 15px;
    color: #f44336;
    font-family: "Aeonik-Regular";
}

.input-group {
    margin-bottom: 15px;
}

.input-group label {
    display: block;
    font-family: "Aeonik-Bold";
    margin-bottom: 5px;
    color: #333;
}

.input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: "Aeonik-Regular";
    font-size: 1rem;
}

ul {
    margin-top: 10px;
    padding-left: 20px;
}

li {
    font-family: "Aeonik-Regular";
    margin-bottom: 5px;
}
</style>