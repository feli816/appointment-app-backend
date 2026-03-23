# DriveSchool SaaS MVP

Prototype fonctionnel mobile-first pour une application SaaS B2B d'auto-ecole.

## Lancer le prototype

Ouvrir `index.html` dans un navigateur.

## Contenu

- `index.html` : structure de l'application
- `styles.css` : interface mobile-first
- `app.js` : logique du prototype MVP
- `docs/architecture.md` : architecture technique cible et schema de donnees

## Parcours MVP inclus

- Connexion rapide avec trois roles : proprietaire, moniteur, eleve
- Gestion des utilisateurs de l'ecole
- Calendrier et disponibilites moniteur
- Reservation de lecons avec prevention des doubles reservations
- Notifications internes
- Messagerie integree
- Suivi de progression eleve
- Tableau de bord SaaS pour le proprietaire

## Commandes Git pour mettre a jour `projet-finances` sur ta machine

Si ton projet est deja clone sur ta machine et que tu es **dans le dossier du projet**, utilise simplement :

```bash
git pull origin main
```

Si tu veux d'abord aller dans le dossier du projet depuis n'importe ou sur ta machine Windows :

```bat
cd /d C:\Projet_prog\projet-finances
git pull origin main
```

Si le projet n'est pas encore present sur ta machine, clone-le une premiere fois dans `C:\Projet_prog` :

```bat
cd /d C:\Projet_prog
git clone https://github.com/feli816/projet-finances.git
```

Puis pour les mises a jour suivantes :

```bat
cd /d C:\Projet_prog\projet-finances
git pull origin main
```

Si ta branche par defaut n'est pas `main`, remplace `main` par `master` ou par le nom reel de ta branche distante.
