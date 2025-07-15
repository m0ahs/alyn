# Projet Alyn - Backend Mem0 Webhook

## 🚀 Installation locale

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancer le serveur :
```bash
uvicorn main:app --reload
```

Le serveur démarre sur `http://localhost:8000`

## 📋 Endpoints

- `POST /mem0/add` - Ajouter une mémoire manuellement
- `GET /mem0/memories` - Récupérer les mémoires (optionnel: `?user_id=...`)
- `POST /mem0/webhook` - Recevoir les webhooks de Mem0

## 🌐 Déploiement automatique avec Fly.io + GitHub

### 1. Prérequis
- Compte [Fly.io](https://fly.io) (gratuit)
- Compte GitHub

### 2. Configuration Fly.io
```bash
# Installer flyctl
curl -L https://fly.io/install.sh | sh

# Se connecter
flyctl auth login

# Créer l'app (une seule fois)
flyctl launch --name alyn-mem0-api --region fra
```

### 3. Configuration GitHub Actions
1. Créer un token Fly.io : `flyctl auth token`
2. Ajouter le secret `FLY_API_TOKEN` dans votre repo GitHub
3. Pusher sur la branche `main` → déploiement automatique

### 4. URL de production
Après déploiement : `https://alyn-mem0-api.fly.dev`

## 🔗 Configuration GPT Action

1. Utilise le fichier `openapi.yaml` pour configurer l'action GPT
2. Remplace l'URL du serveur par : `https://alyn-mem0-api.fly.dev`
3. Configure les webhooks Mem0 vers : `https://alyn-mem0-api.fly.dev/mem0/webhook`

## 🧪 Test de l'API

```bash
# Ajouter une mémoire
curl -X POST "https://alyn-mem0-api.fly.dev/mem0/add" \
  -H "Content-Type: application/json" \
  -d '{"memory": "L\'utilisateur préfère les réponses courtes"}'

# Récupérer les mémoires
curl "https://alyn-mem0-api.fly.dev/mem0/memories"
```

## 📁 Structure du projet

```
Alyn/
├── main.py                 # API FastAPI
├── requirements.txt        # Dépendances Python
├── Dockerfile             # Configuration Docker
├── fly.toml               # Configuration Fly.io
├── openapi.yaml           # Schéma OpenAPI pour GPT
├── .dockerignore          # Fichiers ignorés par Docker
├── .github/workflows/     # Actions GitHub
│   └── deploy.yml         # Déploiement automatique
└── README.md              # Documentation
```