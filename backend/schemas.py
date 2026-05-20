"""
Pydantic Schemas — request/response validation for FastAPI endpoints
Matches the mock data structure in mockData.js exactly
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class SeverityEnum(str, Enum):
    low      = "low"
    medium   = "medium"
    high     = "high"
    critical = "critical"


class StatusEnum(str, Enum):
    active   = "active"
    resolved = "resolved"


class DisasterTypeEnum(str, Enum):
    earthquake = "earthquake"
    flood      = "flood"
    fire       = "fire"
    storm      = "storm"
    landslide  = "landslide"
    tsunami    = "tsunami"


# ── Auth ──────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name:  str
    email: EmailStr
    org:   Optional[str] = None
    password: str

class UserOut(BaseModel):
    id: int; name: str; email: str; role: str
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"

class LoginRequest(BaseModel):
    email:    str
    password: str


# ── Disasters ─────────────────────────────────────────────────────────────────
class DisasterCreate(BaseModel):
    type:        DisasterTypeEnum
    location:    str
    lat:         Optional[float] = None
    lng:         Optional[float] = None
    severity:    SeverityEnum
    description: Optional[str] = None
    status:      StatusEnum = StatusEnum.active
    source_api:  Optional[str] = None
    external_id: Optional[str] = None

class DisasterOut(BaseModel):
    id:          int
    type:        str
    location:    str
    lat:         Optional[float]
    lng:         Optional[float]
    severity:    str
    description: Optional[str]
    timestamp:   datetime
    status:      str
    source_api:  Optional[str] = None
    external_id: Optional[str] = None
    class Config: from_attributes = True

class DisasterStats(BaseModel):
    total:    int
    active:   int
    critical: int
    resolved: int
    regions:  int


# ── Alerts ────────────────────────────────────────────────────────────────────
class AlertCreate(BaseModel):
    disaster_id: int
    message:     str
    severity:    SeverityEnum

class AlertOut(BaseModel):
    id:          int
    disaster_id: int
    message:     str
    severity:    str
    is_read:     bool
    timestamp:   datetime
    # Populated from joined disaster data
    type:        Optional[str] = None
    location:    Optional[str] = None
    class Config: from_attributes = True
