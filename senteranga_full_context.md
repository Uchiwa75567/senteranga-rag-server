# Senteranga - Plateforme Agricole Sénégalaise

## 📋 Vue d'ensemble

Senteranga est une plateforme digitale complète de marché agricole, d'élevage et de la pêche conçue spécifiquement pour le Sénégal. Pour chaque secteur (agriculture, élevage, pêche), la plateforme permet de connecter les différents acteurs de la chaîne de valeur : producteurs, acheteurs, industriels, institutions gouvernementales, investisseurs et conseillers techniques.

### 🎯 Objectifs
- **Digitalisation complète** des marchés agricoles, d'élevage et de pêche sénégalais
- **Connexion des acteurs** de chaque chaîne de valeur (agriculture, élevage, pêche)
- **Renforcement de la souveraineté alimentaire** du Sénégal
- **Accompagnement technique** des agriculteurs, éleveurs et pêcheurs
- **Transparence et traçabilité** des produits locaux
- **Intégration gouvernementale** pour les politiques sectorielles

## 🛠️ Stack Technique

### Technologies Principales
- **Framework Frontend**: Angular 17 (Standalone Components)
- **Langage**: TypeScript 5.2
- **Styling**: Tailwind CSS 3.4 avec thème personnalisé
- **Routing**: Angular Router (lazy loading)
- **Forms**: Reactive Forms avec validation avancée
- **Build Tool**: Angular CLI 17

### Backend & Services
- **Serveur Principal**: Express.js + JSON Server
- **IA Conversationnelle**: Google Gemini AI (Jokko)
- **Stockage Images**: Cloudinary
- **Base de données**: JSON Server (développement) + structure RESTful
- **IA Locale**: Système RAG avec FAISS (optionnel)

### Dépendances Clés
```json
{
  "@angular/core": "^17.3.12",
  "@angular/router": "^17.3.12",
  "@angular/forms": "^17.3.12",
  "@google/generative-ai": "^0.24.1",
  "cloudinary": "^2.8.0",
  "express": "^5.2.1",
  "json-server": "^1.0.0-beta.3",
  "tailwindcss": "^3.4.18",
  "sweetalert2": "^11.26.4"
}
```

## 🏗️ Architecture du Projet

### Structure des Dossiers
```
src/
├── app/
│   ├── components/              # Composants réutilisables
│   │   ├── hero/               # Section héros avec statistiques
│   │   ├── marketplace-section/ # Présentation des marchés
│   │   ├── jokko-chat/         # Chat IA avec reconnaissance vocale
│   │   └── [autres composants]
│   ├── pages/                   # Pages principales
│   │   ├── landing/            # Page d'accueil
│   │   ├── marketplace/        # Marché agricole général
│   │   ├── marketplace-fishing/ # Marché pêche
│   │   ├── marketplace-livestock/ # Marché élevage
│   │   ├── category-*/         # Pages de catégories (légumes, fruits, céréales)
│   │   ├── login/              # Connexion utilisateur
│   │   ├── register/           # Inscription multi-étapes
│   │   └── dashboard-*/        # Dashboards par rôle utilisateur
│   ├── data/                    # Données statiques et configurations
│   │   ├── senteranga-data.json # Base de données complète
│   │   ├── policies.data.ts    # Politiques agricoles
│   │   ├── reports.data.ts     # Rapports gouvernementaux
│   │   └── [catalogues produits]
│   ├── models/                  # Modèles TypeScript
│   │   ├── schema.ts           # Interfaces principales
│   │   ├── enums.ts            # Énumérations
│   │   ├── cart.schema.ts      # Schéma panier
│   │   ├── institutional.schema.ts # Dashboard institutionnel
│   │   └── policies.schema.ts  # Politiques agricoles
│   ├── services/               # Services Angular
│   ├── utils/                  # Utilitaires
│   ├── app.component.ts        # Composant racine
│   ├── app.routes.ts          # Configuration des routes
│   └── styles.css             # Styles globaux
├── server/                     # Serveurs backend
│   ├── index.js               # Serveur principal (JSON + Upload)
│   ├── upload-server.js       # Serveur upload Cloudinary
│   ├── gemini-chat-server.js  # Serveur IA Gemini
│   └── local_rag/             # Système RAG local
├── public/                    # Assets statiques
│   ├── images/                # Images produits et UI
│   ├── icons/                 # Icônes SVG
│   └── _redirects             # Configuration déploiement
└── [fichiers de configuration]
```

## 🎯 Fonctionnalités Complètes

### 🛒 Système de Marketplace

#### Marchés Spécialisés
- **Marché Agricole**: Légumes, fruits, céréales
- **Marché Élevage**: Produits animaux et dérivés
- **Marché Pêche**: Poissons, crustacés, fruits de mer

#### Gestion des Produits
- **Publication de produits** avec photos obligatoires
- **Système d'annonces** pour disponibilité future
- **Validation administrative** des publications
- **Gestion des stocks** et quantités minimales
- **Catégorisation** par type et région
- **Certifications** (Bio, Label Rouge, AOC, IGP)

#### Fonctionnalités Avancées
- **Upload d'images** via Cloudinary (obligatoire)
- **Caméra intégrée** pour capture directe
- **Géolocalisation** des produits par région
- **Système de réservations** pour les acheteurs
- **Prix officiels** et comparaisons

### 👥 Gestion des Utilisateurs Multi-Rôles

#### Types d'Utilisateurs
1. **Agriculteurs/Producteurs** - Publication et gestion de produits
2. **Clients/Acheteurs** - Consultation et commandes
3. **Administrateurs** - Validation et modération
4. **Investisseurs** - Opportunités d'investissement
5. **Agronomes** - Conseils et alertes techniques
6. **Agents Terrain** - Vérifications sur site
7. **État/Institutionnel** - Politiques et rapports

#### Authentification
- **Connexion** par téléphone + PIN (6 chiffres)
- **Inscription multi-étapes** selon le profil
- **Validation administrative** pour les agriculteurs
- **Gestion des sessions** et sécurité

### 📊 Dashboards Personnalisés

#### Dashboard Agriculteur
- **Publication de produits** avec formulaire complet
- **Gestion des annonces** (disponible/réservé)
- **Suivi des réservations** et clients
- **Catalogue de semences** et intrants
- **Alertes régionales** et conseils techniques
- **Informations bancaires** pour paiements

#### Dashboard Client
- **Navigation des marchés** et catégories
- **Système de réservations** de produits
- **Historique des achats**
- **Préférences** et notifications

#### Dashboard Institutionnel
- **Statistiques nationales** agricoles
- **Rapports gouvernementaux** (production, commerce, sécurité)
- **Politiques agricoles** et subventions
- **Suivi des objectifs** nationaux
- **Alertes et notifications** importantes

#### Autres Dashboards
- **Investisseur**: Opportunités d'investissement
- **Agronome**: Alertes techniques et conseils
- **Admin**: Gestion utilisateurs et modération

### 🤖 Intelligence Artificielle - Jokko

#### Fonctionnalités IA
- **Chat conversationnel** spécialisé agriculture sénégalaise
- **Reconnaissance vocale** en français
- **Conseils techniques** adaptés au contexte local
- **Navigation assistée** dans la plateforme
- **Réponses contextuelles** selon le profil utilisateur

#### Technologies IA
- **Gemini AI** pour génération de réponses
- **Contexte Senteranga** intégré
- **RAG local** optionnel (FAISS + embeddings)
- **Fallback responses** en cas d'indisponibilité

### 🏛️ Intégration Gouvernementale

#### Politiques Agricoles
- **Catalogue des politiques** actives
- **Subventions et aides** disponibles
- **Calendrier des échéances** importantes
- **Suivi des bénéficiaires**

#### Rapports Gouvernementaux
- **Statistiques de production** par région
- **Bilan commercial** agricole
- **Évaluation sécurité alimentaire**
- **Téléchargement** de rapports officiels

### 📱 Fonctionnalités Techniques

#### Interface Utilisateur
- **Design responsive** mobile et desktop
- **Thème personnalisé** vert Senteranga
- **Animations fluides** et transitions
- **Accessibilité** et ergonomie

#### Sécurité et Validation
- **Validation temps réel** des formulaires
- **Upload sécurisé** des images
- **Authentification robuste**
- **Gestion des permissions** par rôle

#### Intégrations Externes
- **Cloudinary** pour gestion des médias
- **Google Gemini** pour IA conversationnelle
- **JSON Server** pour API RESTful
- **Speech Recognition** pour saisie vocale

## 📊 Modèles de Données

### Interfaces Principales

#### Utilisateur (`User`)
```typescript
interface User {
  id: string;
  nom: string;
  prenom: string;
  role: UserRole;
  region: SenegalRegion;
  email?: string;
  telephone: string;
  verified: boolean;
  dateInscription: Date;
  validationStatus?: 'pending' | 'approved' | 'rejected';
}
```

#### Produit (`Product`)
```typescript
interface Product {
  id: string;
  nom: string;
  categorie: string;
  type: ProductType;
  prix: number;
  unite: string;
  quantiteDisponible: number;
  quantiteMinimale: number;
  producteur: {
    nom: string;
    region: SenegalRegion;
  };
  certifications?: CertificationType[];
  images: string[];
  localisation: string;
  isAnnonce?: boolean;
  periodeApproximativeDebut?: string;
  periodeApproximativeFin?: string;
  statutAnnonce?: 'en_attente' | 'validee' | 'rejetee';
}
```

#### Réservation (`Reservation`)
```typescript
interface Reservation {
  id: string;
  productId: string;
  productTitle: string;
  clientId: string;
  clientName: string;
  quantity: number;
  reservationDate: Date;
  status: 'active' | 'cancelled' | 'fulfilled';
  notes?: string;
}
```

### Énumérations

#### Rôles Utilisateur (`UserRole`)
- `agriculteur` - Agriculteur/Producteur
- `client` - Client Acheteur
- `admin` - Administrateur
- `investisseur` - Investisseur Agricole
- `agronome` - Agronome/Conseiller
- `agent-terrain` - Agent Terrain
- `etat` - État/Institutionnel

#### Types de Produit (`ProductType`)
- `agricol` - Produits agricoles
- `elevage` - Produits d'élevage
- `peche` - Produits de pêche

#### Régions du Sénégal (`SenegalRegion`)
- Dakar, Thiès, Saint-Louis, Kaolack, Ziguinchor, Louga, Matam, Kolda, Tambacounda, Fatick, Kaffrine, Kédougou, Sédhiou, Diourbel

## 🚀 Installation et Configuration

### Prérequis
- **Node.js** version 18+
- **npm** ou yarn
- **Angular CLI** 17+
- **Git**

### Installation Complète
```bash
# 1. Cloner le repository
git clone <repository-url>
cd projet3d

# 2. Installer les dépendances
npm install

# 3. Configuration des variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API (Cloudinary, Gemini)

# 4. Démarrer tous les services
npm run dev:full

# Services démarrés:
# - Angular: http://localhost:4200
# - JSON Server: http://localhost:3004/api
# - Upload Server: http://localhost:4201
# - Gemini Chat: http://localhost:4202
```

### Scripts Disponibles
```json
{
  "start": "ng serve",
  "build": "ng build",
  "dev": "concurrently \"npm run server\" \"npm start\"",
  "dev:full": "concurrently \"npm run server\" \"npm run start:gemini-server\" \"npm start\"",
  "server": "node server/index.js",
  "start:upload-server": "node server/upload-server.js",
  "start:gemini-server": "node server/gemini-chat-server.js",
  "json-server": "json-server --watch db.json --port 3004"
}
```

### Configuration des APIs
```bash
# Variables d'environnement (.env)
CLOUDINARY_CLOUD_NAME=votre_cloud_name
CLOUDINARY_API_KEY=votre_api_key
CLOUDINARY_API_SECRET=votre_api_secret
GEMINI_API_KEY=votre_gemini_key
```

## 🗄️ Architecture des Données

### Endpoints API (JSON Server)
```
GET    /api/regions           # Régions du Sénégal
GET    /api/userTypes         # Types d'utilisateurs
GET    /api/users             # Utilisateurs
GET    /api/products          # Catalogue produits
GET    /api/orders            # Commandes
GET    /api/reservations      # Réservations
GET    /api/notifications     # Notifications
POST   /upload-images         # Upload Cloudinary
POST   /chat                  # Chat IA
```

### Structure Base de Données
- **users**: Profils utilisateurs avec rôles
- **products**: Catalogue produits avec images
- **regions**: 14 régions + départements
- **userTypes**: Configurations par rôle
- **orders**: Historique des transactions
- **reservations**: Système de réservations
- **notifications**: Messagerie système

## 🎨 Design System

### Palette de Couleurs
- **Primaire**: `#00843d` (Vert Senteranga)
- **Secondaire**: `#ffd100` (Jaune)
- **Accent**: `#e31b23` (Rouge)
- **Neutres**: Grille de gris

### Composants UI
- **Cartes** avec ombres et bordures arrondies
- **Boutons** avec états interactifs
- **Formulaires** avec validation visuelle
- **Modales** et notifications (SweetAlert2)
- **Animations** CSS fluides

## 🔮 Fonctionnalités Futures

### Phase 2 - Production
- [ ] **API Backend** (Node.js/Express + PostgreSQL)
- [ ] **Authentification JWT** sécurisée
- [ ] **Paiements intégrés** (Wave, Orange Money)
- [ ] **Géolocalisation** temps réel
- [ ] **Application mobile** (Ionic/Capacitor)

### Phase 3 - Écosystème
- [ ] **Blockchain** pour traçabilité
- [ ] **IA prédictive** pour prix et récoltes
- [ ] **Marketplace B2B** avancé
- [ ] **Intégration logistique**
- [ ] **API tierces** (météo, sols)

### Améliorations Techniques
- [ ] **Tests unitaires** complets
- [ ] **Progressive Web App** (PWA)
- [ ] **Internationalisation** (i18n)
- [ ] **Performance** et optimisation
- [ ] **Accessibilité** WCAG complète

## 🤝 Contribution

### Structure des Commits
```
feat: nouvelle fonctionnalité
fix: correction de bug
docs: documentation
style: formatage
refactor: refactorisation
test: tests
chore: maintenance
```

### Code Quality
- **ESLint** + **Prettier** configurés
- **TypeScript strict** activé
- **Composants standalone** Angular
- **Conventionnal commits**

## 📄 Licence

**ISC License** - Voir fichier LICENSE

## 👥 Équipe & Support

- **Développement**: Kilo Code
- **Design UI/UX**: Adapté au contexte sénégalais
- **Données**: Catalogue agricole sénégalais
- **IA**: Jokko - Assistant agricole intelligent

### Contact
- **Email**: support@senteranga.sn
- **Site**: https://senteranga.sn
- **Documentation**: https://docs.senteranga.sn

---

**🌾 Senteranga - Pour une agriculture sénégalaise moderne et souveraine**
