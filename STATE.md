# 📌 PROJECT STATE FILE — DisasterWatch
**Last Updated:** 2026-04-10  
**Session:** Initial frontend + FYP structure build  
**Status:** ✅ Frontend complete · ⏳ Backend not yet connected

> Use this file to resume work without starting from scratch.

---

## 📍 Where Everything Lives

| Part | Location |
|------|----------|
| **Working project** | `c:\Users\saind\.gemini\antigravity\playground\ionic-pinwheel\` |
| **Final year project** | `D:\final year project\testing\` |
| Both folders have identical code — `testing\` is the submission copy. |

---

## ✅ What Is Complete

### Frontend (6 pages — fully working)
| File | Status | Notes |
|------|--------|-------|
| `index.html` | ✅ Done | Landing page, live ticker, stats |
| `login.html` | ✅ Done | Login + Register tabs, mock auth |
| `dashboard.html` | ✅ Done | 4 stats, 3 Chart.js charts, table |
| `map.html` | ✅ Done | Leaflet map, 30 markers, filter panel |
| `alerts.html` | ✅ Done | Search, filters, pagination, read toggle |
| `history.html` | ✅ Done | Sortable table, 2 charts, CSV export |

### Styles
| File | Status |
|------|--------|
| `styles/main.css` | ✅ Done — dark theme, all shared components |
| `styles/dashboard.css` | ✅ Done |
| `styles/map.css` | ✅ Done |

### JavaScript
| File | Status | Notes |
|------|--------|-------|
| `js/config.js` | ✅ Done | API stub — **USE_MOCK = true** currently |
| `js/mockData.js` | ✅ Done | 30 disaster records matching MySQL schema |

### Python Backend (structure only — not running)
| File | Status |
|------|--------|
| `backend/main.py` | ✅ Done — FastAPI app with CORS |
| `backend/models.py` | ✅ Done — SQLAlchemy ORM (disasters, alerts, users) |
| `backend/database.py` | ✅ Done — MySQL via .env |
| `backend/schemas.py` | ✅ Done — Pydantic schemas |
| `backend/routes/auth.py` | ✅ Done — JWT login/register |
| `backend/routes/disasters.py` | ✅ Done — CRUD + stats |
| `backend/routes/alerts.py` | ✅ Done — list + mark read |
| `backend/requirements.txt` | ✅ Done |
| `backend/.env.example` | ✅ Done |

### DevOps / FYP Structure
| File | Status |
|------|--------|
| `README.md` | ✅ Done |
| `Dockerfile.frontend` | ✅ Done — Nginx container |
| `Dockerfile.backend` | ✅ Done — Python container |
| `docker-compose.yml` | ✅ Done — frontend + backend + MySQL |
| `k8s/deployment.yaml` | ✅ Done — K8s manifests |
| `terraform/main.tf` | ✅ Done — AWS VPC + EKS + RDS |
| `terraform/variables.tf` | ✅ Done |
| `terraform/outputs.tf` | ✅ Done |
| `docs/synopsis.md` | ✅ Done |
| `docs/walkthrough.md` | ✅ Done |

---

## ⏳ What Is NOT Done (Next Steps)

| Task | Priority | Notes |
|------|----------|-------|
| Connect frontend to FastAPI backend | 🔴 High | Set `USE_MOCK: false` in `js/config.js` |
| Set up MySQL database | 🔴 High | Create `disaster_db`, run schema from README |
| Fill `backend/.env` | 🔴 High | Copy `.env.example` → `.env`, add DB credentials |
| Connect external disaster APIs | 🟡 Medium | USGS (earthquakes), GDACS (all hazards) |
| Add real data ingestion (poller script) | 🟡 Medium | Background task in FastAPI |
| Build Docker images and test | 🟡 Medium | `docker-compose up --build` |
| Deploy to AWS via Terraform | 🟢 Later | Need AWS account + credentials |
| Add login protection (auth guard) | 🟡 Medium | Redirect to login if no JWT token |
| Add AI integration | 🟢 Future | Per system diagram — future phase |

---

## 🔑 Critical Config Points

### Switch from mock → real backend
```js
// js/config.js — change this ONE line:
USE_MOCK: false    // was: true
```

### FastAPI backend URL
```js
// js/config.js
API_BASE_URL: "http://localhost:8000"  // change if deployed
```

### Database credentials
```
# backend/.env  (copy from .env.example)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
DB_NAME=disaster_db
SECRET_KEY=generate-a-long-random-key
```

---

## 🚀 How to Run (Resume Commands)

### Frontend demo (mock data)
```bash
cd "D:\final year project\testing"
python -m http.server 3456
# Browser: http://127.0.0.1:3456
```

### Backend (when ready)
```bash
cd "D:\final year project\testing\backend"
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# API docs: http://127.0.0.1:8000/docs
```

### Full stack with Docker
```bash
cd "D:\final year project\testing"
docker-compose up --build
```

---

## 🎨 Design System (for consistency in future changes)

| Token | Value |
|-------|-------|
| Background primary | `#080d14` |
| Background card | `#0f1c2e` |
| Accent cyan | `#00d4ff` |
| Accent red (danger) | `#ff4757` |
| Accent orange | `#ff6b35` |
| Accent purple | `#a855f7` |
| Text primary | `#e8f4fd` |
| Text muted | `#8ba7c5` |
| Font heading | Outfit |
| Font body | Inter |
| Border radius card | `20px` |

---

## 📦 Python Dependencies (if pip install fails)
```
fastapi
uvicorn[standard]
sqlalchemy
pymysql
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
pydantic[email]
```

---

## 🗄️ MySQL Schema (run once to set up DB)
```sql
CREATE DATABASE IF NOT EXISTS disaster_db;
USE disaster_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100), email VARCHAR(255) UNIQUE,
    org VARCHAR(200), hashed_pw VARCHAR(255),
    role VARCHAR(50) DEFAULT 'operator',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disasters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('earthquake','flood','fire','storm','landslide','tsunami'),
    location VARCHAR(300), lat FLOAT, lng FLOAT,
    severity ENUM('low','medium','high','critical'),
    description TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active','resolved') DEFAULT 'active',
    source_api VARCHAR(100), external_id VARCHAR(200) UNIQUE
);

CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disaster_id INT, message TEXT,
    severity ENUM('low','medium','high','critical'),
    is_read BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disaster_id) REFERENCES disasters(id) ON DELETE CASCADE
);
```
