# Architecture cible du MVP SaaS

## Positionnement

DriveSchool est pense comme un SaaS B2B multi-tenant pour auto-ecoles :

- un tenant = une auto-ecole
- plusieurs roles par tenant : proprietaire, moniteur, eleve
- un moteur central de reservation reutilisable plus tard pour d'autres metiers

Le prototype de ce depot est une version front autonome destinee a valider l'experience produit.

## Stack recommandee pour la version evolutive

### Mobile

- React Native avec Expo
- TypeScript
- Expo Router
- React Query
- Zustand ou Redux Toolkit

### Backend

- NestJS en TypeScript
- API REST pour le MVP
- WebSocket pour la messagerie temps reel
- Worker asynchrone pour rappels et notifications

### Donnees et services

- PostgreSQL
- Prisma ORM
- Redis pour cache, presence et jobs
- Stripe Billing pour le SaaS
- Expo Notifications / FCM / APNs pour le push

## Architecture modulaire

### Modules backend

1. `identity`
   - utilisateurs
   - roles
   - auth
   - permissions multi-tenant

2. `schools`
   - auto-ecoles
   - agences
   - abonnement
   - parametrage

3. `scheduling`
   - disponibilites
   - creneaux
   - contraintes
   - prevention double booking

4. `bookings`
   - reservations
   - confirmations
   - annulations
   - statut des cours

5. `messaging`
   - conversations
   - messages
   - lecture

6. `progress`
   - competences
   - evaluations
   - progression examen

7. `notifications`
   - rappels
   - alertes creneaux libres
   - demandes urgentes geolocalisees

8. `geo`
   - points de rendez-vous
   - moniteurs proches
   - zones de couverture

9. `analytics`
   - taux de remplissage
   - heures realisees
   - activite moniteurs
   - usage SaaS

## Structure de base de donnees

### `schools`

- `id`
- `name`
- `slug`
- `owner_user_id`
- `subscription_plan`
- `subscription_status`
- `timezone`
- `created_at`

### `users`

- `id`
- `school_id`
- `role` (`owner`, `instructor`, `student`)
- `first_name`
- `last_name`
- `email`
- `phone`
- `auth_provider_id`
- `status`
- `created_at`

### `instructor_profiles`

- `user_id`
- `bio`
- `meeting_radius_km`
- `default_start_location`
- `vehicle_type`

### `student_profiles`

- `user_id`
- `exam_target_date`
- `current_level`

### `instructor_availabilities`

- `id`
- `school_id`
- `instructor_id`
- `weekday`
- `start_time`
- `end_time`
- `recurrence_type`

### `lesson_slots`

- `id`
- `school_id`
- `instructor_id`
- `start_at`
- `end_at`
- `status` (`available`, `held`, `booked`, `cancelled`, `completed`)
- `meeting_point_lat`
- `meeting_point_lng`
- `meeting_label`

### `bookings`

- `id`
- `school_id`
- `slot_id`
- `student_id`
- `booking_status`
- `booked_at`
- `cancelled_at`

### `conversations`

- `id`
- `school_id`
- `type`
- `created_at`

### `conversation_participants`

- `conversation_id`
- `user_id`

### `messages`

- `id`
- `conversation_id`
- `sender_id`
- `body`
- `sent_at`
- `read_at`

### `skills`

- `id`
- `school_id`
- `label`
- `category`

### `student_skill_progress`

- `id`
- `student_id`
- `skill_id`
- `status`
- `validated_by`
- `validated_at`
- `notes`

### `notifications`

- `id`
- `school_id`
- `user_id`
- `type`
- `title`
- `body`
- `status`
- `scheduled_at`
- `sent_at`

## Ecrans principaux du MVP

### Proprietaire

- onboarding creation ecole
- dashboard KPIs
- gestion moniteurs et eleves
- planning global
- abonnement et facturation

### Moniteur

- agenda
- creation/modification de creneaux
- vue eleves suivis
- fiche progression
- messagerie

### Eleve

- accueil
- recherche / reservation
- calendrier personnel
- messagerie
- progression
- disponibilite immediate

## Regles fonctionnelles critiques

- un slot ne peut etre reserve qu'une fois
- un eleve ne peut pas reserver deux lecons au meme horaire
- les notifications doivent etre ciblees par role et par utilisateur
- toutes les donnees metier sont cloisonnees par `school_id`

## Roadmap

### Phase 1

- auth reelle
- API REST
- PostgreSQL
- push mobiles
- paiement SaaS

### Phase 2

- matching geolocalise intelligent
- scoring de no-show
- suggestion automatique de remplissage
- paiement des lecons a l'unite

### Phase 3

- marque blanche
- multi-agences
- CRM leads
- extension a d'autres verticales de reservation
