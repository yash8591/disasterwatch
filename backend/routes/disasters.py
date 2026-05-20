"""Routes — Disaster CRUD + stats endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Disaster, Alert
from schemas import DisasterCreate, DisasterOut, DisasterStats

router = APIRouter()


@router.get("/stats", response_model=DisasterStats)
def get_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    total    = db.query(Disaster).count()
    active   = db.query(Disaster).filter(Disaster.status == "active").count()
    critical = db.query(Disaster).filter(Disaster.severity == "critical").count()
    resolved = db.query(Disaster).filter(Disaster.status == "resolved").count()
    regions  = db.query(func.count(func.distinct(Disaster.location))).scalar() or 0
    return DisasterStats(total=total, active=active, critical=critical, resolved=resolved, regions=regions)


@router.get("/", response_model=List[DisasterOut])
def list_disasters(
    type:     Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status:   Optional[str] = Query(None),
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    q = db.query(Disaster)
    if type:     q = q.filter(Disaster.type == type)
    if severity: q = q.filter(Disaster.severity == severity)
    if status:   q = q.filter(Disaster.status == status)
    return q.order_by(Disaster.timestamp.desc()).offset(skip).limit(limit).all()


@router.get("/{disaster_id}", response_model=DisasterOut)
def get_disaster(disaster_id: int, db: Session = Depends(get_db)):
    d = db.query(Disaster).filter(Disaster.id == disaster_id).first()
    if not d: raise HTTPException(404, "Disaster not found")
    return d


@router.post("/", response_model=DisasterOut, status_code=201)
def create_disaster(body: DisasterCreate, db: Session = Depends(get_db)):
    d = Disaster(**body.dict())
    db.add(d); db.commit(); db.refresh(d)
    # Auto-create alert
    alert = Alert(disaster_id=d.id, message=f"ALERT: {d.type} in {d.location}", severity=d.severity)
    db.add(alert); db.commit()
    return d


@router.patch("/{disaster_id}/resolve", response_model=DisasterOut)
def resolve_disaster(disaster_id: int, db: Session = Depends(get_db)):
    d = db.query(Disaster).filter(Disaster.id == disaster_id).first()
    if not d: raise HTTPException(404, "Disaster not found")
    d.status = "resolved"
    db.commit(); db.refresh(d)
    return d
