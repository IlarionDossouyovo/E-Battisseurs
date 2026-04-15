# E-Battisseurs by ELECTRON

Plateforme dropshipping internationale tout-en-un

## Modules

- **M-01** - Moteur de vitrine (Frontend PWA)
- **M-02** - Intelligence d'approvisionnement (IA)
- **M-03** - Gestion des commandes
- **M-04** - Plateforme logistique
- **M-05** - Passerelle de paiement
- **M-06** - Pilote automatique marketing
- **M-07** - CRM et support
- **M-08** - Réseau de fournisseurs
- **M-09** - Analytics Pro
- **M-10** - Moteur de conformité
- **M-11** - Affilié et revendeur
- **M-12** - Orchestrateur IA

## Tech Stack

- Frontend: Next.js 14 + Tailwind CSS
- Backend: FastAPI (Python) + Node.js
- Database: PostgreSQL + Redis
- IA: N8N + Claude/GPT
- Paiements: Stripe, PayPal, Crypto

## Démarrage

```bash
# Backend
cd backend
uv venv
uv sync
uv run uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Docker

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.yml up -d --build
```

## N8N

Les workflows d'automatisation sont dans le dossier `n8n/`:
- `workflow-order.json` - Traitement des commandes
- `workflow-sourcing.json` - Sourcing quotidien
- `workflow-chatbot.json` - Support client IA

## API Documentation

Une fois le serveur lancé:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

Propriétaire - ELECTRON Group 2025