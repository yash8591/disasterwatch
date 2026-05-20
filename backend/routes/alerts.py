"""Routes — Alert read/list/mark-read endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import Alert, Disaster
from schemas import AlertCreate, AlertOut

router = APIRouter()


def alert_to_dict(alert: Alert) -> dict:
    """Convert alert ORM object to dict with disaster type/location."""
    data = {
        "id": alert.id,
        "disaster_id": alert.disaster_id,
        "message": alert.message,
        "severity": alert.severity.value if hasattr(alert.severity, 'value') else alert.severity,
        "is_read": alert.is_read,
        "timestamp": alert.timestamp,
        "type": None,
        "location": None,
    }
    if alert.disaster:
        data["type"] = alert.disaster.type.value if hasattr(alert.disaster.type, 'value') else alert.disaster.type
        data["location"] = alert.disaster.location
    return data


@router.get("/", response_model=List[AlertOut])
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(Alert).options(joinedload(Alert.disaster)).order_by(Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return [alert_to_dict(a) for a in alerts]


@router.get("/unread", response_model=List[AlertOut])
def unread_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).options(joinedload(Alert.disaster)).filter(Alert.is_read == False).order_by(Alert.timestamp.desc()).all()
    return [alert_to_dict(a) for a in alerts]


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    a = db.query(Alert).options(joinedload(Alert.disaster)).filter(Alert.id == alert_id).first()
    if not a: raise HTTPException(404, "Alert not found")
    return alert_to_dict(a)


@router.patch("/{alert_id}/read", response_model=AlertOut)
def mark_read(alert_id: int, db: Session = Depends(get_db)):
    a = db.query(Alert).options(joinedload(Alert.disaster)).filter(Alert.id == alert_id).first()
    if not a: raise HTTPException(404, "Alert not found")
    a.is_read = True
    db.commit(); db.refresh(a)
    return alert_to_dict(a)


@router.post("/", response_model=AlertOut, status_code=201)
def create_alert(body: AlertCreate, db: Session = Depends(get_db)):
    alert = Alert(**body.dict())
    db.add(alert); db.commit(); db.refresh(alert)
    return alert_to_dict(alert)
