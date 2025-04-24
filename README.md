# GoutteAGoutte - Système de Jardinage Intelligent

GoutteAGoutte est une application web permettant de gérer et de surveiller un jardin connecté. L'application offre des fonctionnalités de suivi des plantes, d'arrosage a distance pour le jardin de l'ECE.

## Structure du Projet

Le projet est composé de deux parties principales :

- **Frontend** : Application Nuxt.js (Vue 3) pour l'interface utilisateur
- **Backend** : API FastAPI avec MongoDB pour la gestion des données

## Prérequis

- Node.js (version 18 ou supérieure)
- Python 3.9+
- MongoDB (local ou distant)
- Yarn (recommandé) ou npm

## Installation

### Configuration de l'environnement

1. Clonez ce dépôt :
   ```bash
   git clone <url-du-repository>
   cd e-garden
   ```

2. Créez un fichier `.env` à la racine du dossier Backend avec les variables suivantes :
   ```
   MONGODB_URL=<votre-url-mongodb>
   MONGODB_DB=e_garden
   JWT_SECRET_KEY=<votre-clé-secrète-jwt>
   ```

### Backend (FastAPI)

1. Naviguez vers le dossier Backend :
   ```bash
   cd Backend
   ```

2. Créez un environnement virtuel Python et activez-le :
   ```bash
   python -m venv venv
   
   # Sur Windows
   venv\Scripts\activate
   
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancez le serveur backend :
   ```bash
   python main.py
   ```
   Le serveur FastAPI sera accessible à l'adresse : http://localhost:8000

### Frontend (Nuxt.js)

1. Naviguez vers le dossier Frontend :
   ```bash
   cd Frontend
   ```

2. Installez les dépendances :
   ```bash
   yarn install
   # OU
   npm install
   ```

3. Lancez le serveur de développement :
   ```bash
   yarn dev
   # OU
   npm run dev
   ```
   L'application sera accessible à l'adresse : http://localhost:3000

## Fonctionnalités

### Authentification
- Inscription / Connexion utilisateur
- Protection des routes par authentification JWT

### Gestion des Semis
- Suivi de l'humidité des plantes
- Gestion de l'arrosage automatique et manuel
- Surveillance de la température
- Calendrier des plantations

### Mode de Fonctionnement
- Mode automatique / manuel pour l'arrosage des plantes

## Structure des Dossiers

### Frontend
- `components/` : Composants Vue.js réutilisables
- `pages/` : Pages de l'application (routage automatique par Nuxt)
- `composables/` : Fonctions et logique réutilisables (dont l'authentification)
- `middleware/` : Middleware d'authentification pour protéger les routes
- `plugins/` : Plugins Nuxt
- `public/assets/` : Ressources statiques (images, CSS, etc.)

### Backend
- `main.py` : Point d'entrée de l'API FastAPI
- `auth.py` : Routes et logique d'authentification
- `plant.py` : Route et logique d'arrosasage et de recupération des données des capteurs

Nous avons aussi les différents codes qui permettent l'activation des différents composants branchés sur notre Raspberry Pi 4, ainsi que des codes de récupérations des données des capteurs.

### Connexion 
Nous avons utilisé Tailscale, et particulièrement la fonctionnalité funnel, qui nous permet de communiquer entre notre front-end hosté via vercel, et notre backend directement sur la Raspberry Pi 4 situé dans la serre, dans le jardin sur le toit de l'école.

## Dépannage

### Problèmes de connexion à MongoDB
- Vérifiez que votre URL MongoDB est correcte dans le fichier `.env`
- Assurez-vous que votre IP est autorisée dans les paramètres du cluster MongoDB
- Vérifiez les logs du serveur pour plus de détails sur les erreurs

### Problèmes d'authentification
- Assurez-vous que JWT_SECRET_KEY est correctement défini
- Vérifiez que les requêtes incluent le token JWT dans l'en-tête Authorization

