# DisasterWatch — Build Walkthrough


---

## Pages Summary

| Page | File | Features |
|------|------|----------|
| Landing | `index.html` | Hero, live ticker, feature cards, stats |
| Login | `login.html` | Sign In / Register + JWT auth stub |
| Dashboard | `dashboard.html` | 4 stats, 3 Chart.js charts, disasters table |
| Live Map | `map.html` | Leaflet world map, 30 markers, filter sidebar |
| Alerts | `alerts.html` | Filters, pagination, read/unread toggle |
| History | `history.html` | Sortable table, 2 charts, CSV export |

---



## Full Project Structure (D:\final year project\testing)

```
testing/
├── README.md                   ← Project overview + quick start
│
├── index.html                  ← Landing page
├── login.html                  ← Auth (Login/Register)
├── dashboard.html              ← Operations dashboard
├── map.html                    ← Leaflet interactive map
├── alerts.html                 ← Alert management
├── history.html                ← Historical records + CSV export
│
├── styles/
│   ├── main.css                ← Global dark theme tokens
│   ├── dashboard.css
│   └── map.css
│
├── js/
│   ├── config.js               ← API stub (flip USE_MOCK=false to connect)
│   └── mockData.js             ← 30 disaster records (MySQL schema match)
│
├── backend/                    ← Python FastAPI backend
│   ├── main.py                 ← App entry + CORS
│   ├── models.py               ← SQLAlchemy ORM (disasters, alerts, users)
│   ├── database.py             ← MySQL connection via .env
│   ├── schemas.py              ← Pydantic schemas
│   ├── requirements.txt
│   ├── .env.example
│   └── routes/
│       ├── auth.py             ← JWT login/register
│       ├── disasters.py        ← CRUD + stats
│       └── alerts.py           ← List + mark read
│
├── Dockerfile.frontend         ← Nginx container
├── Dockerfile.backend          ← Python container
├── docker-compose.yml          ← Full stack orchestration
│
├── k8s/
│   └── deployment.yaml         ← K8s deployments + services + secrets
│
├── terraform/
│   ├── main.tf                 ← AWS VPC + EKS + RDS
│   └── variables.tf            ← Region, DB credentials
│
└── docs/
    ├── synopsis.md             ← Project synopsis
    └── walkthrough.md          ← This file
```

---

## How to Run

### Demo (Frontend Only)
```bash
cd "D:\final year project\testing"
python -m http.server 3456
# Open: http://127.0.0.1:3456
```

### With Backend
```bash
cd "D:\final year project\testing\backend"
copy .env.example .env          # Fill credentials
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Then in js/config.js: USE_MOCK: false
```

### With Docker
```bash
cd "D:\final year project\testing"
docker-compose up --build
```

---

## Key Design Decisions

- **`USE_MOCK` toggle** — single line switch connects frontend to real FastAPI
- **30 mock disaster records** — match MySQL schema exactly, zero data loss on switch
- **FastAPI CORS enabled** — frontend can call backend from any origin during dev
- **JWT auth** — `localStorage` token auto-attached to all API calls in `config.js`
