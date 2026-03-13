# Driving School SaaS MVP (Backend API)

Prototype fonctionnel FastAPI pour une application mobile iOS/Android dédiée aux auto-écoles (modèle SaaS B2B multi-tenant).

## 1) Architecture technique proposée (MVP évolutif)

- **Mobile**: React Native (Expo) ou Flutter (clients iOS/Android uniques).
- **Backend API**: FastAPI (Python), architecture modulaire par domaines (`auth`, `users`, `slots`, `appointments`, `messages`, etc.).
- **Base de données**: SQLModel + SQLite (MVP local) ; migration simple vers PostgreSQL en production.
- **Auth**: OTP + JWT multi-tenant (isolation par `tenant_id`).
- **Notifications**: table interne + extension future vers FCM/APNs.
- **Scalabilité SaaS**:
  - `Tenant` = auto-école cliente.
  - Toutes les entités métier sont scoppées par `tenant_id`.
  - Possibilité future: facturation Stripe, RBAC avancé, webhooks, analytics avancées.

## 2) Modèle de données MVP

### Entités principales

- `tenants`: auto-écoles clientes.
- `users`: propriétaires, moniteurs, élèves (`role`: `owner`, `instructor`, `student`).
- `services`: types de cours (manuel, auto, etc.).
- `lesson_slots`: disponibilités créées par les moniteurs.
- `appointments`: réservations élève ↔ moniteur, point de rendez-vous possible.
- `messages`: messagerie interne élève/moniteur.
- `notifications`: notifications applicatives.
- `student_progress`: suivi des compétences par élève.

### Règles métier MVP implémentées

- Anti double-réservation (conflits élève et moniteur).
- Un créneau (`slot`) ne peut être réservé qu’une seule fois.
- Isolation stricte des données par tenant.
- Génération de notifications lors d’une réservation et d’un message.

## 3) Écrans mobiles principaux (à brancher sur cette API)

1. **Onboarding/Auth OTP**
   - Inscription/connexion par email + OTP.
2. **Dashboard propriétaire**
   - Vue activité globale, moniteurs, réservations, taux de remplissage (itération suivante pour analytics détaillés).
3. **Calendrier moniteur**
   - Création/suppression de créneaux, consultation du planning.
4. **Réservation élève**
   - Liste des créneaux disponibles, réservation rapide, détail du rendez-vous.
5. **Messagerie**
   - Conversation élève ↔ moniteur.
6. **Progression élève**
   - Compétences validées, notes moniteur.
7. **Notifications**
   - Leçons à venir, messages, nouvelles disponibilités.

## 4) API MVP disponible

- `POST /auth/register` : création/MAJ utilisateur + OTP.
- `POST /auth/verify-otp` : récupération JWT.
- `GET/POST /users` : gestion des utilisateurs.
- `GET /services` : services de l’auto-école courante.
- `GET/POST/DELETE /slots` : gestion des créneaux moniteur.
- `GET/POST /appointments` : réservation des leçons.
- `GET/POST /messages` : messagerie intégrée.
- `GET /notifications` : notifications utilisateur.
- `GET/POST /progress` : suivi compétences élève.

## 5) Lancer le prototype

### Prérequis
- Python 3.10+

### Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Démarrage
```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## 6) Données seedées

Au démarrage, le système crée un tenant de démo et 3 comptes:
- `owner@demo.local`
- `instructor@demo.local`
- `student@demo.local`

Ainsi que deux services de conduite.

## 7) Roadmap post-MVP

- Géolocalisation temps réel (recherche urgente de moniteur disponible).
- Matching intelligent pour maximiser le remplissage des créneaux.
- Paiements/abonnements SaaS (Stripe) + limites par palier.
- Notifications push mobiles (FCM/APNs).
- Tableau de bord analytics avancé propriétaire.
