"""
DisasterWatch — FastAPI Backend (Python)
========================================
Stack: FastAPI + SQLAlchemy + MySQL (PyMySQL) + python-jose (JWT auth)

Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import asyncio
import logging
import os

# Local imports
from database import engine, get_db, Base, SessionLocal
from models import Disaster, Alert, User
from schemas import (
    DisasterCreate, DisasterOut,
    AlertOut, AlertCreate,
    UserCreate, UserOut, Token
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="DisasterWatch API",
    description="Real-Time Disaster Alert & Monitoring System — Backend API",
    version="1.0.0",
)

# ── CORS (allows the HTML frontend to call this API) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Create tables + start poller on startup ───────────────────────────────────
@app.on_event("startup")
async def startup():
    # Create all MySQL tables
    Base.metadata.create_all(bind=engine)
    logging.info("✅ Database tables created")

    # Start the background disaster poller
    from poller import poll_all_sources
    asyncio.create_task(poll_all_sources())
    logging.info("🚀 Background disaster poller started")

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# ── Poller status endpoint ────────────────────────────────────────────────────
@app.get("/api/poller/status", tags=["System"])
def poller_status(db: Session = Depends(get_db)):
    """Check how many disasters have been fetched from external APIs."""
    from sqlalchemy import func
    total = db.query(Disaster).count()
    by_source = db.query(Disaster.source_api, func.count(Disaster.id)).group_by(Disaster.source_api).all()
    latest = db.query(Disaster).order_by(Disaster.timestamp.desc()).first()
    return {
        "total_disasters": total,
        "by_source": {src: cnt for src, cnt in by_source},
        "latest_event": latest.location if latest else None,
        "latest_timestamp": latest.timestamp.isoformat() if latest else None,
    }

# ── Manual poll trigger (for testing) ──────────────────────────────────────────
@app.post("/api/poller/trigger", tags=["System"])
async def trigger_poll():
    """Manually trigger a poll from all external APIs (for testing)."""
    import httpx
    from poller import fetch_usgs_earthquakes, fetch_gdacs_events, fetch_reliefweb_events, save_disasters_to_db

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            fetch_usgs_earthquakes(client),
            fetch_gdacs_events(client),
            fetch_reliefweb_events(client),
            return_exceptions=True,
        )

    all_disasters = []
    errors = []
    for result in results:
        if isinstance(result, list):
            all_disasters.extend(result)
        elif isinstance(result, Exception):
            errors.append(str(result))

    count = save_disasters_to_db(all_disasters) if all_disasters else 0
    return {
        "fetched": len(all_disasters),
        "new_saved": count,
        "errors": errors,
    }

# ── Seed endpoint (populate DB with mock data for demo) ────────────────────────
@app.post("/api/seed", tags=["System"])
def seed_database(db: Session = Depends(get_db)):
    """Populate DB with sample disasters for demo/testing. Safe to call multiple times."""
    SEED_DATA = [
        {"type":"earthquake","location":"Türkiye, Kahramanmaraş","lat":37.58,"lng":36.92,"severity":"critical","description":"M7.8 earthquake, major structural damage reported.","status":"active","external_id":"seed_1"},
        {"type":"flood","location":"Bangladesh, Dhaka","lat":23.81,"lng":90.41,"severity":"high","description":"Severe monsoon flooding. 200,000+ displaced.","status":"active","external_id":"seed_2"},
        {"type":"fire","location":"Australia, New South Wales","lat":-32.16,"lng":148.60,"severity":"high","description":"Bushfire spreading rapidly due to high winds.","status":"active","external_id":"seed_3"},
        {"type":"storm","location":"Philippines, Luzon","lat":16.11,"lng":120.35,"severity":"critical","description":"Super Typhoon with 195 km/h winds.","status":"active","external_id":"seed_4"},
        {"type":"landslide","location":"India, Kerala Hills","lat":10.16,"lng":76.80,"severity":"medium","description":"Heavy rains trigger landslides. Roads blocked.","status":"active","external_id":"seed_5"},
        {"type":"tsunami","location":"Japan, Pacific Coast","lat":38.30,"lng":141.50,"severity":"critical","description":"Tsunami warning after M7.5 offshore earthquake.","status":"resolved","external_id":"seed_6"},
        {"type":"earthquake","location":"Nepal, Kathmandu Valley","lat":27.69,"lng":85.31,"severity":"high","description":"M6.4 earthquake, buildings collapsed.","status":"active","external_id":"seed_7"},
        {"type":"flood","location":"Nigeria, Lagos State","lat":6.52,"lng":3.38,"severity":"medium","description":"Urban flooding after 220mm rainfall.","status":"active","external_id":"seed_8"},
        {"type":"fire","location":"Canada, British Columbia","lat":49.88,"lng":-119.49,"severity":"high","description":"Wildfire consuming 15,000 hectares.","status":"active","external_id":"seed_9"},
        {"type":"storm","location":"USA, Gulf Coast","lat":29.76,"lng":-95.37,"severity":"critical","description":"Category 4 hurricane with storm surge.","status":"resolved","external_id":"seed_10"},
        {"type":"earthquake","location":"Indonesia, Sulawesi","lat":-0.90,"lng":119.87,"severity":"critical","description":"M7.2 earthquake, tsunami warning.","status":"resolved","external_id":"seed_11"},
        {"type":"flood","location":"Pakistan, Balochistan","lat":30.18,"lng":67.03,"severity":"high","description":"Flash floods from melting glaciers.","status":"active","external_id":"seed_12"},
        {"type":"storm","location":"India, Bay of Bengal","lat":13.08,"lng":80.27,"severity":"high","description":"Cyclone alert for Tamil Nadu coast.","status":"active","external_id":"seed_13"},
        {"type":"fire","location":"USA, California","lat":34.05,"lng":-118.24,"severity":"critical","description":"Wind-driven wildfire. 50,000 under evacuation.","status":"active","external_id":"seed_14"},
        {"type":"flood","location":"Brazil, Bahia","lat":-14.86,"lng":-40.85,"severity":"critical","description":"Extreme flooding displaces 1 million.","status":"active","external_id":"seed_15"},
    ]

    added = 0
    for d in SEED_DATA:
        existing = db.query(Disaster).filter(Disaster.external_id == d["external_id"]).first()
        if existing:
            continue
        disaster = Disaster(**d, source_api="seed")
        db.add(disaster)
        db.flush()
        alert = Alert(
            disaster_id=disaster.id,
            message=f"🚨 {d['type'].upper()} ALERT: {d['description']}",
            severity=d["severity"],
        )
        db.add(alert)
        added += 1

    db.commit()
    return {"message": f"Seeded {added} disasters (skipped {len(SEED_DATA)-added} duplicates)"}


# ── Include routers ───────────────────────────────────────────────────────────
from routes.auth      import router as auth_router
from routes.disasters import router as disaster_router
from routes.alerts    import router as alert_router

app.include_router(auth_router,      prefix="/api/auth",      tags=["Auth"])
app.include_router(disaster_router,  prefix="/api/disasters",  tags=["Disasters"])
app.include_router(alert_router,     prefix="/api/alerts",     tags=["Alerts"])
