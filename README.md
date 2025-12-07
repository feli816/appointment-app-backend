# Appointment App Backend

Backend FastAPI minimal pour une application de prise de rendez-vous. Cette V1 fournit une base SQLite, quelques modèles SQLModel et des routes simples pour tester le fonctionnement.

## Prérequis
- Python 3.10+

## Installation
1. Créez un environnement virtuel (optionnel mais recommandé) :
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancer le serveur
Depuis la racine du projet :
```bash
uvicorn app.main:app --reload
```
Le serveur démarre par défaut sur http://127.0.0.1:8000.

## Tester les routes
- **GET /** : Vérifie que l'API répond.
- **GET /services** : Liste les services pour le tenant `1` (générés au démarrage si absents).
- **POST /appointments** : Crée un rendez-vous. Exemple de payload :
  ```json
  {
    "tenant_id": 1,
    "service_id": 1,
    "user_id": 1,
    "start_datetime": "2024-01-01T10:00:00",
    "end_datetime": "2024-01-01T10:30:00",
    "status": "pending"
  }
  ```
- **GET /availability** : Retourne quelques créneaux fictifs.

La documentation interactive OpenAPI est disponible sur http://127.0.0.1:8000/docs.

## Arborescence
```
app/
├── core/
│   └── config.py
├── db.py
├── main.py
├── models/
│   ├── appointment.py
│   ├── service.py
│   ├── tenant.py
│   └── user.py
├── routes/
│   ├── appointments.py
│   ├── availability.py
│   └── services.py
└── schemas/
    ├── appointment.py
    ├── service.py
    ├── tenant.py
    └── user.py
```

## Base de données
- SQLite local (`database.db`).
- Les tables sont créées automatiquement au démarrage grâce à `SQLModel.create_all()`.
- Des données minimales (tenant, utilisateur, services) sont insérées si absentes.
