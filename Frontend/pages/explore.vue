<template>
    <div class="wrapper_page">
        <navbar></navbar>
        <div class="header_bis">
            <Header_title title="Administration" subtitle="Gestion de la base de données" />
        </div>

        <div class="content">
            <div class="main">
                <div class="section database-section">
                    <h2>Test de connexion MongoDB</h2>
                    <button class="action-button" @click="testConnection" :disabled="isLoading">
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
                </div>

                <div class="section user-section">
                    <h2>Gestion des utilisateurs</h2>

                    <div class="card">
                        <div class="tabs">
                            <button class="tab-button" :class="{ active: activeTab === 'create' }"
                                @click="activeTab = 'create'">
                                Créer un utilisateur
                            </button>
                            <button class="tab-button" :class="{ active: activeTab === 'edit' && editingUser }"
                                @click="activeTab = 'edit'" 
                                :disabled="!editingUser">
                                Modifier un utilisateur
                            </button>
                            <button class="tab-button" :class="{ active: activeTab === 'list' }"
                                @click="activeTab = 'list'">
                                Liste des utilisateurs
                            </button>
                        </div>

                        <!-- Create User Form -->
                        <form v-if="activeTab === 'create'" @submit.prevent="createUser" class="form">
                            <div class="form-group">
                                <label for="username">Nom d'utilisateur</label>
                                <input type="text" id="username" v-model="newUser.username" required
                                    placeholder="Entrez un nom d'utilisateur" />
                            </div>

                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" id="email" v-model="newUser.email" required
                                    placeholder="Entrez une adresse email" />
                            </div>

                            <div class="form-group">
                                <label for="password">Mot de passe</label>
                                <input type="password" id="password" v-model="newUser.password" required
                                    placeholder="Entrez un mot de passe" />
                            </div>

                            <div class="form-group">
                                <label for="confirm-password">Confirmer le mot de passe</label>
                                <input type="password" id="confirm-password" v-model="newUser.confirmPassword" required
                                    placeholder="Confirmez le mot de passe" />
                            </div>

                            <div class="form-group">
                                <label for="role">Rôle</label>
                                <select id="role" v-model="newUser.role">
                                    <option value="user">Utilisateur</option>
                                    <option value="admin">Administrateur</option>
                                </select>
                            </div>

                            <div class="error-message" v-if="error">
                                {{ error }}
                            </div>

                            <button type="submit" class="action-button" :disabled="isCreatingUser">
                                {{ isCreatingUser ? 'Création en cours...' : 'Créer l\'utilisateur' }}
                            </button>
                        </form>

                        <!-- Edit User Form -->
                        <form v-if="activeTab === 'edit' && editingUser" @submit.prevent="updateUser" class="form">
                            <div class="form-group">
                                <label for="edit-username">Nom d'utilisateur</label>
                                <input type="text" id="edit-username" v-model="editingUser.username" required disabled
                                    placeholder="Nom d'utilisateur" />
                                <small>Le nom d'utilisateur ne peut pas être modifié</small>
                            </div>

                            <div class="form-group">
                                <label for="edit-email">Email</label>
                                <input type="email" id="edit-email" v-model="editingUser.email" required
                                    placeholder="Entrez une adresse email" />
                            </div>

                            <div class="form-group">
                                <label for="edit-password">Nouveau mot de passe (laisser vide pour ne pas changer)</label>
                                <input type="password" id="edit-password" v-model="editingUser.password"
                                    placeholder="Entrez un nouveau mot de passe" />
                            </div>

                            <div class="form-group">
                                <label for="edit-role">Rôle</label>
                                <select id="edit-role" v-model="editingUser.role">
                                    <option value="user">Utilisateur</option>
                                    <option value="admin">Administrateur</option>
                                </select>
                            </div>

                            <div class="error-message" v-if="error">
                                {{ error }}
                            </div>

                            <div class="form-actions">
                                <button type="submit" class="action-button" :disabled="isUpdatingUser">
                                    {{ isUpdatingUser ? 'Mise à jour en cours...' : 'Mettre à jour l\'utilisateur' }}
                                </button>
                                <button type="button" class="cancel-button" @click="cancelEdit">
                                    Annuler
                                </button>
                            </div>
                        </form>

                        <!-- User List -->
                        <div v-if="activeTab === 'list'" class="user-list">
                            <div v-if="isLoadingUsers" class="loading">Chargement des utilisateurs...</div>
                            <table v-else-if="users.length > 0" class="users-table">
                                <thead>
                                    <tr>
                                        <th>Nom</th>
                                        <th>Email</th>
                                        <th>Rôle</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in users" :key="user.id">
                                        <td>{{ user.username }}</td>
                                        <td>{{ user.email }}</td>
                                        <td><span class="role-badge" :class="user.role">{{ user.role }}</span></td>
                                        <td class="actions">
                                            <button class="action-icon edit" @click="editUser(user)">
                                                <span>Modifier</span>
                                            </button>
                                            <button class="action-icon delete" @click="confirmDeleteUser(user)">
                                                <span>Supprimer</span>
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div v-else class="no-users">
                                Aucun utilisateur trouvé.
                            </div>
                        </div>
                    </div>

                    <div v-if="userCreationResult" class="result-panel" :class="userCreationResult.status">
                        <h3>Résultat:</h3>
                        <p>{{ userCreationResult.message }}</p>
                        <p v-if="userCreationResult.user_id">ID: {{ userCreationResult.user_id }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Delete confirmation modal -->
        <div v-if="showDeleteConfirm" class="modal-overlay">
            <div class="modal-content">
                <h3>Confirmer la suppression</h3>
                <p>Êtes-vous sûr de vouloir supprimer l'utilisateur <strong>{{ userToDelete?.username }}</strong> ?</p>
                <p class="warning">Cette action est irréversible.</p>
                
                <div class="modal-actions">
                    <button class="action-button delete-button" @click="deleteUser" :disabled="isDeleting">
                        {{ isDeleting ? 'Suppression...' : 'Supprimer' }}
                    </button>
                    <button class="cancel-button" @click="cancelDelete">Annuler</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRuntimeConfig } from 'nuxt/app';
import Header_title from '~/components/header_title.vue';
import navbar from '~/components/navbar.vue';
import { useAuth } from '~/composables/useAuth';

definePageMeta({
    middleware: ['auth']
});

// Obtenir l'URL de base de l'API depuis la configuration
const config = useRuntimeConfig();
const apiBase = config.public.apiBaseUrl;

// États de l'interface
const isLoading = ref(false);
const connectionStatus = ref(null);
const error = ref(null);
const activeTab = ref('create');

// États pour la gestion des utilisateurs
const newUser = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'user'
});
const isCreatingUser = ref(false);
const userCreationResult = ref(null);
const users = ref([]);
const isLoadingUsers = ref(false);

// États pour l'édition et la suppression
const editingUser = ref(null);
const showDeleteConfirm = ref(false);
const userToDelete = ref(null);
const isUpdatingUser = ref(false);
const updateResult = ref(null);
const isDeleting = ref(false);

// Fonction pour tester la connexion à MongoDB
const testConnection = async () => {
    isLoading.value = true;
    connectionStatus.value = null;
    error.value = null;

    try {
        const response = await $fetch(`${apiBase}/mongodb`, {
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

// Fonction pour créer un utilisateur
const createUser = async () => {
    if (!newUser.value.username) {
        error.value = 'Le nom d\'utilisateur est requis';
        return;
    }

    if (newUser.value.password !== newUser.value.confirmPassword) {
        error.value = 'Les mots de passe ne correspondent pas';
        return;
    }

    isCreatingUser.value = true;
    userCreationResult.value = null;
    error.value = null;

    try {
        // Structurer les données pour l'API
        const userData = {
            username: newUser.value.username,
            email: newUser.value.email,
            password: newUser.value.password,
            role: newUser.value.role || 'user'
        };

        // Utiliser l'URL complète avec apiBase
        const response = await $fetch(`${apiBase}/auth/register`, {
            method: 'POST',
            body: userData,
            onResponseError({ response }) {
                console.error("Détails de l'erreur:", response._data);
                throw new Error(response._data?.detail || 'Erreur lors de la création de l\'utilisateur');
            }
        });

        userCreationResult.value = {
            status: 'success',
            message: 'Utilisateur créé avec succès',
            user_id: response.id || response._id || response.user_id
        };

        // Réinitialiser le formulaire en cas de succès
        newUser.value = {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            role: 'user'
        };

        // Recharger la liste des utilisateurs si on est dans l'onglet liste
        if (activeTab.value === 'list') {
            await fetchUsers();
        }
    } catch (err) {
        console.error('Erreur complète:', err);
        error.value = err.message || 'Une erreur s\'est produite lors de la création de l\'utilisateur';
        userCreationResult.value = {
            status: 'error',
            message: error.value
        };
    } finally {
        isCreatingUser.value = false;
    }
};

// Fonction pour charger la liste des utilisateurs
const fetchUsers = async () => {
    isLoadingUsers.value = true;
    
    try {
        // Récupérer le token depuis useAuth
        const { token } = useAuth();
        
        const response = await $fetch(`${apiBase}/auth/users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        users.value = response || [];
    } catch (err) {
        console.error('Erreur lors du chargement des utilisateurs:', err);
        users.value = [];
        error.value = err.message || 'Erreur lors du chargement des utilisateurs';
    } finally {
        isLoadingUsers.value = false;
    }
};

// Fonction pour éditer un utilisateur
const editUser = (user) => {
    // Copier l'utilisateur pour éviter de modifier directement les données
    editingUser.value = {
        username: user.username,
        email: user.email,
        password: '', // Vide par défaut, ne pas afficher le mot de passe actuel
        role: user.role
    };
    activeTab.value = 'edit'; // Basculer vers l'onglet d'édition
};

// Méthode pour annuler l'édition
const cancelEdit = () => {
    editingUser.value = null;
    error.value = null;
    activeTab.value = 'list'; // Retourner à la liste
};

// Méthode pour mettre à jour un utilisateur
const updateUser = async () => {
    if (!editingUser.value) return;
    
    isUpdatingUser.value = true;
    error.value = null;
    updateResult.value = null;
    
    try {
        const updateData = {
            email: editingUser.value.email,
            role: editingUser.value.role
        };
        
        // N'inclure le mot de passe que s'il est fourni
        if (editingUser.value.password) {
            updateData.password = editingUser.value.password;
        }
        
        // Récupérer le token depuis useAuth
        const { token } = useAuth();
        
        const response = await $fetch(`${apiBase}/auth/users/${editingUser.value.username}`, {
            method: 'PUT',
            body: updateData,
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        // Notification de succès
        updateResult.value = {
            status: 'success',
            message: `Utilisateur ${editingUser.value.username} mis à jour avec succès`
        };
        
        // Recharger la liste et revenir à celle-ci
        await fetchUsers();
        activeTab.value = 'list';
        editingUser.value = null;
    } catch (err) {
        error.value = err.message || 'Erreur lors de la mise à jour de l\'utilisateur';
    } finally {
        isUpdatingUser.value = false;
    }
};

// Méthode pour afficher la confirmation de suppression
const confirmDeleteUser = (user) => {
    userToDelete.value = user;
    showDeleteConfirm.value = true;
};

// Méthode pour annuler la suppression
const cancelDelete = () => {
    userToDelete.value = null;
    showDeleteConfirm.value = false;
};

// Méthode pour supprimer un utilisateur
const deleteUser = async () => {
    if (!userToDelete.value) return;
    
    isDeleting.value = true;
    error.value = null;
    
    try {
        // Récupérer le token depuis useAuth
        const { token } = useAuth();
        
        await $fetch(`${apiBase}/auth/users/${userToDelete.value.username}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token.value}`
            }
        });
        
        // Notification et rafraîchissement
        userCreationResult.value = {
            status: 'success',
            message: `Utilisateur ${userToDelete.value.username} supprimé avec succès`
        };
        
        // Masquer la modale et recharger la liste
        showDeleteConfirm.value = false;
        userToDelete.value = null;
        await fetchUsers();
    } catch (err) {
        error.value = err.message || 'Erreur lors de la suppression de l\'utilisateur';
        userCreationResult.value = {
            status: 'error',
            message: `Échec de la suppression: ${error.value}`
        };
    } finally {
        isDeleting.value = false;
    }
};

// Charger la liste des utilisateurs quand on change d'onglet
watch(activeTab, (newValue) => {
    if (newValue === 'list') {
        fetchUsers();
    }
});

// Charger les données au montage du composant
onMounted(() => {
    // Vous pouvez décommenter si vous voulez tester la connexion automatiquement
    // testConnection();
});
</script>

<style scoped>
.wrapper_page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.header_bis {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    margin: 1rem;
}

.content {
    flex: 1;
    padding: 0 1rem;
    margin-left: 80px;
    /* Ajouter de l'espace pour la navbar verticale */
}

.main {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.section {
    background-color: #f5f5f5;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.database-section {
    margin-bottom: 1rem;
}

h2 {
    font-family: "Aeonik-Bold";
    color: #4CAF50;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.card {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
    padding: 1.5rem;
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

.form-group input,
.form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
    border-color: #4caf50;
    outline: none;
}

.action-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-family: "Aeonik-Bold";
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.action-button:hover:not(:disabled) {
    background-color: #45a049;
}

.action-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.result-panel {
    margin-top: 1.5rem;
    padding: 1rem;
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
    color: #f44336;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

ul {
    margin-top: 10px;
    padding-left: 20px;
}

li {
    font-family: "Aeonik-Regular";
    margin-bottom: 5px;
}

/* Styles pour la liste utilisateurs */
.user-list {
    padding: 1.5rem;
}

.users-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.users-table th,
.users-table td {
    text-align: left;
    padding: 0.8rem;
    border-bottom: 1px solid #eee;
}

.users-table th {
    background-color: #f9f9f9;
    font-family: "Aeonik-Bold";
    color: #333;
}

.role-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-family: "Aeonik-Medium";
}

.role-badge.admin {
    background-color: #ffecb3;
    color: #ff9800;
}

.role-badge.user {
    background-color: #e8f5e9;
    color: #4caf50;
}

.actions {
    display: flex;
    gap: 0.5rem;
}

.action-icon {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.4rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
}

.action-icon.edit {
    color: #2196f3;
}

.action-icon.delete {
    color: #f44336;
}

.action-icon:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.no-users {
    padding: 2rem;
    text-align: center;
    color: #888;
    font-family: "Aeonik-Regular";
}

.loading {
    padding: 2rem;
    text-align: center;
    color: #666;
    font-family: "Aeonik-Regular";
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.delete-button {
    background-color: #f44336;
}

.delete-button:hover:not(:disabled) {
    background-color: #e53935;
}

.cancel-button {
    background-color: #ccc;
}

.cancel-button:hover:not(:disabled) {
    background-color: #b3b3b3;
}

.warning {
    color: #f44336;
    font-weight: bold;
}

@media (max-width: 768px) {
    .wrapper_page {
        flex-direction: column;
    }

    .form {
        padding: 1rem;
    }

    .section {
        padding: 1rem;
    }

    .content {
        margin-left: 0;
    }
}
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
    font-family: "Aeonik-Bold";
    color: #333;
    margin-bottom: 1rem;
}

.warning {
    color: #f44336;
    font-size: 0.9rem;
    margin: 1rem 0;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.delete-button {
    background-color: #f44336;
}

.delete-button:hover:not(:disabled) {
    background-color: #d32f2f;
}

.cancel-button {
    background-color: #e0e0e0;
    color: #333;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-family: "Aeonik-Bold";
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.cancel-button:hover {
    background-color: #d5d5d5;
}

.form-actions {
    display: flex;
    gap: 1rem;
}

small {
    display: block;
    color: #757575;
    margin-top: 0.25rem;
    font-size: 0.8rem;
}
</style>