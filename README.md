# PhytoVision Frontend

Detection des maladies du mais par intelligence artificielle
IRAD Cameroun · Projet de fin d'etudes

[React] [Tailwind] [Status: Production Ready]

## Description

PhytoVision est un assistant intelligent d'aide a la decision phytosanitaire pour les techniciens de l'IRAD. L'interface permet d'analyser des feuilles de mais, visualiser l'historique des diagnostics, et suivre l'epidemiologie par zone agro-ecologique.

## Fonctionnalites

- **Analyse** — Upload d'image ou capture camera, prediction IA (maladie, confiance, severite, action)
- **Historique** — Tableau pagine, recherche/filtrage en temps reel, export CSV
- **Epidemiologie** — Dashboard par zone (Centre, Ouest, Nord, Extreme-Nord), graphiques Recharts, alerte prioritaire

## Stack Technique

| Technologie | Usage |
|-------------|-------|
| React 18 + Create React App | Framework UI |
| Tailwind CSS v3 | Styling (palette vert/blanc) |
| React Router DOM v6 | Navigation 3 pages |
| Recharts | Graphiques epidemiologie |
| Axios | Communication backend FastAPI |

## Palette de Couleurs

| Role | Hex | Usage |
|------|-----|-------|
| Fond principal | #0F172A | Arriere-plan global |
| Cartes / Panneaux | #1E293B | Sidebar, topbar, cartes |
| Vert principal | #22C55E | Boutons CTA, badges actifs |
| Danger / Critique | #EF4444 | Severite elevee |
| Attention / Modere | #F59E0B | Severite moyenne |
| Information / Faible | #3B82F6 | Severite faible |

## Demarrer le projet

```bash
# Installation
npm install

# Demarrer le serveur de developpement
npm start

# Build production
npm run build

# Verifier les erreurs ESLint
npm run lint

# Lancer les tests
npm test
Configuration
Creer un fichier .env a la racine :

text
REACT_APP_API_URL=http://localhost:8000/api
Architecture
Le frontend respecte une architecture MVC stricte :

text
Vue → Controleur → Service API → Backend FastAPI
Aucune vue n'importe directement ApiService. Tout passe par le controleur correspondant.

Structure des dossiers
text
src/
├── assets/              # Logos, icones, images statiques
├── components/          # 10 composants reutilisables
│   ├── Sidebar.jsx
│   ├── Logo.jsx
│   ├── StatisticCard.jsx
│   ├── UploadZone.jsx
│   ├── ResultCards.jsx
│   ├── SearchBar.jsx
│   ├── HistoriqueTable.jsx
│   ├── DiagnosticModal.jsx
│   ├── Spinner.jsx
│   └── EmptyState.jsx
├── models/
│   └── DiagnosticModel.js
├── views/               # 3 pages principales
│   ├── AnalyseView.jsx
│   ├── HistoriqueView.jsx
│   └── EpidemiologieView.jsx
├── controllers/
│   ├── AnalyseController.js
│   ├── HistoriqueController.js
│   └── DashboardController.js
├── services/
│   └── ApiService.js    # Point unique de communication backend
├── routes/
│   └── AppRoutes.jsx
├── App.jsx
└── index.js
Pages
Page 1 — Analyse (page principale)
Zone	Description
Topbar	Titre 'Tableau de bord — Analyse', contexte 'IRAD Cameroun · Mais', badge 'Systeme actif'
Dashboard (4 cartes)	Total analyses, Maladies detectees, Feuilles saines, Maladie dominante
Zone d'import	Drag-and-drop, boutons 'Choisir fichier' et 'Prendre photo'
Previsualisation	Affiche l'image selectionnee avant analyse
Bouton Analyser	Bouton vert desactive si aucun fichier, Spinner pendant traitement
Cartes resultat	Maladie, Confiance (barre progression), Severite (couleur dynamique), Action
Page 2 — Historique
Fonctionnalite	Description
3 cartes resume	Compteurs par maladie (Virus Strie, Brulure Foliaire, Tache Grise)
Barre de recherche	Filtre temps reel par maladie ou zone
Boutons de filtre	Toutes / Maladies / Saines
Tableau historique	Colonnes : #, Date, Maladie, Severite, Action, Confiance, Zone, Details
Bouton Details	Ouvre DiagnosticModal avec toutes informations
Export CSV	Telechargement fichier CSV
Etat vide	Message si aucun resultat
Page 3 — Epidemiologie
Fonctionnalite	Description
4 cartes resume	Total cas, Zone plus touchee, Feuilles saines, Zones surveillees
Filtre par zone	Boutons : Toutes, Centre, Ouest, Nord, Extreme-Nord
Cartes par zone	Nom zone, total cas, niveau alerte, barres repartition par maladie
Bar chart Recharts	Graphique a barres groupees (4 maladies par zone)
Table d'alerte	Top zones prioritaires avec action IRAD recommandee
Zones Agro-Ecologiques
Zone	Cas detectes	Niveau alerte	Maladie dominante
Centre	47	Critique	Virus de la Strie
Ouest	38	Eleve	Brulure Foliaire
Nord	31	Modere	Tache Grise
Extreme-Nord	24	Modere	Virus de la Strie
Logique niveau alerte : Critique > 40 cas, Eleve > 25 cas, Modere > 10 cas, Faible sinon.

Communication Backend
ApiService.js — Methodes
Methode	Endpoint	Fonction
POST	/api/analyse	analyseImage(file)
GET	/api/diagnostics	getDiagnostics()
GET	/api/dashboard	getDashboard()
GET	/api/epidemiologie	getEpidemiologie()
Strategie de fallback
Tous les controleurs implementent un fallback : si l'appel API echoue, des donnees mock realistes sont affichees automatiquement. L'utilisateur ne voit jamais d'ecran vide.

Modele de Donnees — DiagnosticModel.js
Champ	Type	Description
id	Integer	Identifiant unique
image	String	Nom du fichier image
culture_id	Integer	1 = Mais
maladie_id	Integer	0=Sain, 1=Virus Strie, 2=Brulure, 3=Tache Grise
confiance	Float	Score 0-100%
severite_id	Integer	1=Faible, 2=Moyenne, 3=Elevee
zone_id	Integer	1=Centre, 2=Ouest, 3=Nord, 4=Extreme-Nord
action_id	Integer	1=Surveillance, 2=Traitement preventif, 3=Traitement curatif, 4=Elimination
date_diagnostic	String	Format ISO
Gestion de la Camera
Solution actuelle — capture mobile
L'attribut capture="environment" sur un input file HTML5 ouvre la camera arriere du smartphone sur les navigateurs mobiles compatibles (Chrome Android, Safari iOS).

Choisir fichier : input file standard — ouvre le gestionnaire de fichiers

Prendre photo : input file avec capture="environment" — ouvre directement la camera sur mobile

Limitation : Sur ordinateur portable, capture="environment" est ignore par la plupart des navigateurs de bureau. Le gestionnaire de fichiers s'ouvre a la place.

Solution recommandee — Web Camera API (post-prototype)
Pour acceder a la webcam d'un ordinateur portable, implementer navigator.mediaDevices.getUserMedia() avec un composant CameraModal.jsx dedie.

Flux complet d'une analyse
Etape	Composant	Action
1	AnalyseView.jsx	Selection image via UploadZone
2	UploadZone.jsx	Previsualisation, mise a jour state
3	AnalyseView.jsx	Clic 'Lancer l'analyse', Spinner affiche
4	AnalyseController.js	Appel ApiService.analyseImage(file)
5	ApiService.js	POST /api/analyse multipart/form-data
6	Backend FastAPI	CNN → K-Means → MDP, retour JSON
7	AnalyseController.js	Reception reponse, setResult(data)
8	ResultCards.jsx	Affichage 4 cartes avec couleurs dynamiques
9	Base de donnees	Enregistrement automatique diagnostic
10	HistoriqueView.jsx	Nouveau diagnostic en tete du tableau
Scenario de demonstration jury
Etape	Ce que le jury voit
1	Page Analyse — Dashboard : 153 analyses, maladie dominante
2	Upload d'une image de feuille — drag-and-drop fluide
3	Clic sur Lancer l'analyse — Spinner anime
4	Affichage des 4 cartes resultat (maladie, confiance 92%, severite Elevee rouge, action)
5	Navigation vers Historique — tableau complet
6	Recherche et filtrage — temps reel
7	Ouverture d'une modale Details
8	Export CSV — telechargement fichier
9	Navigation vers Epidemiologie — cartes par zone, bar chart, table alerte
10	Filtre par zone (ex. Centre) — mise a jour instantanee
Limitations et ameliorations
Limitation	Priorite	Plan d'amelioration
Page Epidemiologie utilise donnees mock	Haute	Connecter a GET /api/epidemiologie
Camera ne fonctionne pas sur PC	Haute	Implementer CameraModal.jsx avec getUserMedia
URL API codee en dur	Haute	Utiliser .env
Grilles non responsives	Moyenne	Ajouter classes Tailwind responsives
Aucun test automatique	Moyenne	Ajouter Jest / React Testing Library
Validation API non robuste	Basse	Gestion champs null ou manquants
References techniques
React.js Documentation : https://react.dev

Tailwind CSS v3 : https://tailwindcss.com/docs

React Router DOM v6 : https://reactrouter.com

Recharts : https://recharts.org

Axios : https://axios-http.com

Web Camera API MDN : https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia

IRAD Cameroun : https://www.irad-cameroon.org

Projet academique — IRAD Cameroun / Ucac-Icam
Documentation complete disponible dans ARCHITECTURE.md
