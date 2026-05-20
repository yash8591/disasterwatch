"""
SQLAlchemy ORM Models — matches MySQL schema
Tables: disasters, alerts, users
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class SeverityEnum(str, enum.Enum):
    low      = "low"
    medium   = "medium"
    high     = "high"
    critical = "critical"


class StatusEnum(str, enum.Enum):
    active   = "active"
    resolved = "resolved"


class DisasterTypeEnum(str, enum.Enum):
    earthquake = "earthquake"
    flood      = "flood"
    fire       = "fire"
    storm      = "storm"
    landslide  = "landslide"
    tsunami    = "tsunami"


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, index=True, nullable=False)
    org        = Column(String(200), nullable=True)
    hashed_pw  = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True)
    role       = Column(String(50), default="operator")
    created_at = Column(DateTime, default=datetime.utcnow)


class Disaster(Base):
    """Core disaster event — pulled from external APIs and stored here."""
    __tablename__ = "disasters"

    id          = Column(Integer, primary_key=True, index=True)
    type        = Column(Enum(DisasterTypeEnum), nullable=False, index=True)
    location    = Column(String(300), nullable=False)
    lat         = Column(Float, nullable=True)
    lng         = Column(Float, nullable=True)
    severity    = Column(Enum(SeverityEnum), nullable=False, index=True)
    description = Column(Text, nullable=True)
    timestamp   = Column(DateTime, default=datetime.utcnow, index=True)
    status      = Column(Enum(StatusEnum), default=StatusEnum.active, index=True)
    source_api  = Column(String(100), nullable=True)    # e.g. "USGS", "GDACS"
    external_id = Column(String(200), nullable=True, unique=True)  # dedup from API

    alerts = relationship("Alert", back_populates="disaster", cascade="all, delete-orphan")


class Alert(Base):
    """Notification records linked to disaster events."""
    __tablename__ = "alerts"

    id          = Column(Integer, primary_key=True, index=True)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)
    message     = Column(Text, nullable=False)
    severity    = Column(Enum(SeverityEnum), nullable=False)
    is_read     = Column(Boolean, default=False)
    timestamp   = Column(DateTime, default=datetime.utcnow, index=True)

    disaster = relationship("Disaster", back_populates="alerts")
