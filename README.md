# 🛰️ DisasterWatch — Real-Time Disaster Alert & Monitoring System

> **Final Year Project** | Cloud-Native Disaster Management Platform  
> **Tech Stack:** FastAPI (Python) · MySQL · HTML · CSS · JavaScript · Docker · Kubernetes · Terraform · AWS

---

## 📋 Project Synopsis

A cloud-native real-time disaster alert and monitoring system that collects disaster data from external APIs and delivers instant alerts through a web dashboard. Built using modern DevOps practices including containerization, orchestration, and infrastructure as code.

---

## 🗂️ Project Structure

```
testing/
├── 📄 README.md                    ← You are here
│
├── 🌐 Frontend (HTML/CSS/JS)
│   ├── index.html                  ← Landing page
│   ├── login.html                  ← Authentication page
│   ├── dashboard.html              ← Operations dashboard
│   ├── map.html                    ← Interactive disaster map
│   ├── alerts.html                 ← Alert notifications
│   ├── history.html                ← Historical records
│   ├── styles/
│   │   ├── main.css                ← Global design system (dark theme)
│   │   ├── dashboard.css           ← Dashboard styles
│   │   └── map.css                 ← Map layout styles
│   └── js/
│       ├── config.js               ← API config (swap USE_MOCK to connect backend)
│       └── mockData.js             ← 30 mock records matching MySQL schema
│
├── 🐍 Backend (Python / FastAPI)
│   └── backend/
│       ├── main.py                 ← FastAPI entry point with CORS
│       ├── models.py               ← SQLAlchemy ORM models
│       ├── database.py             ← MySQL connection
│       ├── schemas.py              ← Pydantic request/response schemas
│       ├── requirements.txt        ← Python dependencies
│       ├── .env.example            ← Environment variable template
│       └── routes/
│           ├── auth.py             ← POST /api/auth/login, /register
│           ├── disasters.py        ← GET/POST /api/disasters
│           └── alerts.py          ← GET/PATCH /api/alerts
│
├── 🐳 Docker
│   ├── Dockerfile.frontend         ← Nginx container for frontend
│   ├── Dockerfile.backend          ← Python container for FastAPI
│   └── docker-compose.yml          ← Multi-container orchestration
│
├── ☸️ Kubernetes (k8s/)
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── mysql-deployment.yaml
│   └── ingress.yaml
│
├── 🏗️ Terraform (terraform/)
│   ├── main.tf                     ← AWS provider & resources
│   ├── variables.tf
│   └── outputs.tf
│
└── 📚 docs/
    ├── synopsis.md                 ← Full project synopsis
    ├── architecture.md             ← System architecture
    └── walkthrough.md              ← Build walkthrough with screenshots
```

---

## 🚀 Quick Start

### Run Frontend Only (Demo Mode)
```bash
cd "D:\final year project\testing"
python -m http.server 3456
# Open: http://127.0.0.1:3456
```

### Run with Python Backend
```bash
# 1. Create MySQL database
mysql -u root -p -e "CREATE DATABASE disaster_db;"

# 2. Configure environment
cd backend
copy .env.example .env
# Edit .env with your MySQL credentials

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start FastAPI server
uvicorn main:app --reload --port 8000

# 5. Connect frontend — in js/config.js:
#    Change: USE_MOCK: true → USE_MOCK: false
```

### Run with Docker (Full Stack)
```bash
cd "D:\final year project\testing"
docker-compose up --build
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🗄️ MySQL Database Schema

```sql
CREATE DATABASE disaster_db;

CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    org         VARCHAR(200),
    hashed_pw   VARCHAR(255) NOT NULL,
    role        VARCHAR(50) DEFAULT 'operator',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disasters (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    type        ENUM('earthquake','flood','fire','storm','landslide','tsunami') NOT NULL,
    location    VARCHAR(300) NOT NULL,
    lat         FLOAT,
    lng         FLOAT,
    severity    ENUM('low','medium','high','critical') NOT NULL,
    description TEXT,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
    status      ENUM('active','resolved') DEFAULT 'active',
    source_api  VARCHAR(100),
    external_id VARCHAR(200) UNIQUE
);

CREATE TABLE alerts (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    disaster_id INT NOT NULL,
    message     TEXT NOT NULL,
    severity    ENUM('low','medium','high','critical') NOT NULL,
    is_read     BOOLEAN DEFAULT FALSE,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disaster_id) REFERENCES disasters(id) ON DELETE CASCADE
);
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login → returns JWT |
| GET | `/api/disasters` | List all disasters (filterable) |
| POST | `/api/disasters` | Create disaster event |
| GET | `/api/disasters/stats` | Stats (active, critical, regions) |
| PATCH | `/api/disasters/{id}/resolve` | Mark resolved |
| GET | `/api/alerts` | List all alerts |
| GET | `/api/alerts/unread` | Unread alerts |
| PATCH | `/api/alerts/{id}/read` | Mark alert as read |
| GET | `/health` | Health check |

---

## 🏗️ System Architecture

```
User Browser
    │
    ▼
Frontend (HTML/CSS/JS)          External Disaster APIs
    │                               (USGS, GDACS)
    │ REST API calls                     │
    ▼                                    ▼
FastAPI Backend (Python) ←──────── Data Collector
    │
    ▼
MySQL Database (RDS on AWS)
    │
    ▼
Docker Container Layer
    │
    ▼
Kubernetes (K8s) Orchestration
    │
    ▼
Terraform → AWS Cloud Infrastructure
```

---

## 👥 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Database | MySQL 8.0, SQLAlchemy ORM |
| Auth | JWT (python-jose), bcrypt |
| Maps | Leaflet.js |
| Charts | Chart.js |
| Container | Docker |
| Orchestration | Kubernetes (K8s) |
| IaC | Terraform |
| Cloud | AWS (EC2, RDS, EKS) |

---

## 📄 License
This project is developed as a Final Year Project (FYP). All rights reserved © 2026.
