# 🚀 Déploiement SENTERANGA RAG Server sur Render

## ✅ Prérequis

- Compte Render (gratuit)
- Clé API Gemini (gratuit)

## 📋 Étapes de déploiement

### 1. Préparer le code
```bash
# Depuis le dossier racine du projet
mkdir deploy-rag-server
cp -r server/local_rag/* deploy-rag-server/
cp render.yaml deploy-rag-server/
```

### 2. Créer un repository Git séparé
```bash
cd deploy-rag-server
git init
git add .
git commit -m "Initial commit - SENTERANGA RAG Server"
# Créer un repo sur GitHub/GitLab et pousser
```

### 3. Déployer sur Render

1. Aller sur [Render.com](https://render.com)
2. Cliquer "New" → "Web Service"
3. Connecter votre repo Git
4. Configuration :
   - **Name**: `senteranga-rag-server`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn server:app --host 0.0.0.0 --port $PORT`

### 4. Configurer les variables d'environnement

Dans Render Dashboard → Environment :
```
GEMINI_API_KEY=AIzaSyA... (votre clé Gemini)
```

### 5. Obtenir l'URL du serveur déployé

Après déploiement, Render vous donne une URL comme :
```
https://senteranga-rag-server.onrender.com
```

## 🔧 Mettre à jour Angular pour utiliser l'URL de production

### Modifier `src/app/components/jokko-chat/jokko-chat.component.ts`

Remplacer :
```typescript
this.http.post('http://localhost:8000/chat', {
```

Par :
```typescript
this.http.post('https://senteranga-rag-server.onrender.com/chat', {
```

### Ou utiliser une variable d'environnement

Ajouter dans `src/environments/environment.prod.ts` :
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://json-server-senteranga.onrender.com/api',
  ragApiUrl: 'https://senteranga-rag-server.onrender.com'
};
```

Puis dans le composant :
```typescript
import { environment } from '../../../environments/environment';

this.http.post(`${environment.ragApiUrl}/chat`, {
```

## 🧪 Tester le déploiement

### Health Check :
```bash
curl https://senteranga-rag-server.onrender.com/health
```

### Test Chat :
```bash
curl -X POST https://senteranga-rag-server.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Bonjour Jokko","userContext":{}}'
```

## 💰 Coûts Render

- **Free Tier**: 750 heures/mois (~22j/mois)
- **Usage**: ~50-100MB RAM, très peu de CPU
- **Coût estimé**: 0-2$/mois selon l'usage

## 🚨 Dépannage

### Build échoue :
- Vérifier que `requirements.txt` est présent
- Python version 3.11 recommandée

### Index FAISS non trouvé :
- S'assurer que `index_data/` est dans le repo
- Les fichiers FAISS sont inclus dans le commit

### API Gemini ne marche pas :
- Vérifier la variable `GEMINI_API_KEY`
- Tester avec une clé valide

## ✅ Checklist avant déploiement

- [ ] Dossier `deploy-rag-server/` créé
- [ ] Tous les fichiers copiés (`server.py`, `requirements.txt`, `index_data/`)
- [ ] `render.yaml` présent
- [ ] Repository Git créé et poussé
- [ ] Clé API Gemini configurée
- [ ] URL du serveur notée pour Angular

---

**🎉 Une fois déployé, votre IA Jokko sera disponible en ligne !**