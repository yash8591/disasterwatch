# Project Synopsis — Real-Time Disaster Alert & Monitoring System

## 1. Introduction

Natural disasters such as earthquakes, floods, storms, and wildfires occur frequently around the world and cause severe damage to human life, infrastructure, and the environment. Traditional disaster monitoring systems often lack real-time updates, scalability, and automated deployment mechanisms.

This project proposes the development of a **Cloud-Native Real-Time Disaster Alert and Monitoring System** that collects disaster data from external APIs and provides real-time alerts through a web dashboard.

### Key Technologies
| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python) |
| Database | MySQL (AWS RDS) |
| Frontend | HTML, CSS, JavaScript |
| Maps | Leaflet.js |
| Charts | Chart.js |
| Containerization | Docker |
| Orchestration | Kubernetes (K8s) |
| Infrastructure | Terraform |
| Cloud | AWS |

---

## 2. Gap Identification

| Limitation | Solution in This Project |
|-----------|--------------------------|
| No real-time dashboards | Live-updating dashboard with Chart.js |
| Limited scalability | Kubernetes autoscaling |
| Manual deployment | Terraform IaC + CI/CD |
| Poor map visualization | Leaflet.js interactive map |
| No severity classification | Critical / High / Medium / Low badges |

---

## 3. Objectives

- Design a web-based disaster monitoring dashboard
- Collect disaster data from external APIs (USGS, GDACS)
- Provide real-time alerts and notifications
- Visualize disaster locations on an interactive map
- Store disaster alerts in MySQL for historical analysis
- Deploy using Docker containers
- Orchestrate containers with Kubernetes
- Automate AWS infrastructure with Terraform

---

## 4. System Architecture

```
[User Browser]
     │
     ▼
[Frontend — HTML/CSS/JS]  ←→  [External Disaster APIs]
     │                              (USGS, GDACS)
     │ REST API
     ▼
[FastAPI Backend — Python]
     │
     ▼
[MySQL — AWS RDS Cloud]
     │
[Docker Container Layer]
     │
[Kubernetes Orchestration]
     │
[Terraform → AWS Cloud]
```

---

## 5. Methodology

1. **Data Collection** — External disaster APIs are polled periodically
2. **Backend Processing** — FastAPI validates, stores, and exposes REST endpoints
3. **Database Management** — SQLAlchemy ORM manages MySQL schema
4. **Frontend Visualization** — Leaflet map + Chart.js dashboard
5. **Containerization** — Docker packages frontend + backend
6. **Orchestration** — Kubernetes manages scaling and availability
7. **IaC** — Terraform provisions AWS VPC, EKS, and RDS automatically
