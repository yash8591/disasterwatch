"""
Real-Time Disaster Data Poller
==============================
Fetches live disaster data from free public APIs:
  - USGS Earthquake API (updates every minute)
  - GDACS API (global disaster alerts)
  - ReliefWeb API (humanitarian disasters)

Runs as a background task inside FastAPI — polls every 5 minutes.
Saves new events to MySQL, skips duplicates via external_id.
"""

import httpx
import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Disaster, Alert

logger = logging.getLogger("poller")
logger.setLevel(logging.INFO)

# ── USGS Earthquake API ──────────────────────────────────────────────────────
USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

async def fetch_usgs_earthquakes(client: httpx.AsyncClient):
    """Fetch recent earthquakes from USGS (magnitude >= 4.0, last 7 days)"""
    try:
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        params = {
            "format": "geojson",
            "starttime": week_ago.strftime("%Y-%m-%d"),
            "endtime": now.strftime("%Y-%m-%d"),
            "minmagnitude": 4.0,
            "limit": 50,
            "orderby": "time",
        }
        resp = await client.get(USGS_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        disasters = []
        for feature in data.get("features", []):
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            mag = props.get("mag", 0)

            # Map magnitude to severity
            if mag >= 7.0:
                severity = "critical"
            elif mag >= 6.0:
                severity = "high"
            elif mag >= 5.0:
                severity = "medium"
            else:
                severity = "low"

            # Determine status based on alert level
            alert_level = props.get("alert", "")
            status = "active" if alert_level in ("red", "orange", "yellow", "") else "resolved"

            # Build location from place string
            place = props.get("place", "Unknown Location")
            timestamp = datetime.utcfromtimestamp(props["time"] / 1000) if props.get("time") else now

            disasters.append({
                "type": "earthquake",
                "location": place,
                "lat": coords[1] if len(coords) > 1 else None,
                "lng": coords[0] if len(coords) > 0 else None,
                "severity": severity,
                "description": f"M{mag:.1f} earthquake — {place}. Depth: {coords[2]:.1f} km." if len(coords) > 2 else f"M{mag:.1f} earthquake — {place}.",
                "timestamp": timestamp,
                "status": status,
                "source_api": "USGS",
                "external_id": f"usgs_{props.get('code', feature.get('id', ''))}",
            })

        logger.info(f"[USGS] Fetched {len(disasters)} earthquakes")
        return disasters

    except Exception as e:
        logger.error(f"[USGS] Error fetching: {e}")
        return []


# ── GDACS API ─────────────────────────────────────────────────────────────────
GDACS_URL = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"

async def fetch_gdacs_events(client: httpx.AsyncClient):
    """Fetch recent disasters from GDACS (floods, cyclones, etc.)"""
    try:
        params = {
            "fromDate": (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "toDate": datetime.utcnow().strftime("%Y-%m-%d"),
            "alertlevel": "Green;Orange;Red",
            "eventlist": "FL;TC;VO;DR;WF",   # Flood, Tropical Cyclone, Volcano, Drought, Wildfire
            "limit": 30,
        }
        resp = await client.get(GDACS_URL, params=params, timeout=30, headers={"Accept": "application/json"})
        resp.raise_for_status()
        data = resp.json()

        type_map = {"FL": "flood", "TC": "storm", "VO": "landslide", "DR": "flood", "WF": "fire", "EQ": "earthquake", "TS": "tsunami"}
        alert_map = {"Red": "critical", "Orange": "high", "Green": "medium"}

        disasters = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            coords = feature.get("geometry", {}).get("coordinates", [0, 0])

            event_type = type_map.get(props.get("eventtype", ""), "storm")
            severity = alert_map.get(props.get("alertlevel", "Green"), "medium")

            disasters.append({
                "type": event_type,
                "location": props.get("country", "Unknown") + ", " + props.get("name", ""),
                "lat": coords[1] if len(coords) > 1 else None,
                "lng": coords[0] if len(coords) > 0 else None,
                "severity": severity,
                "description": props.get("description", f"{event_type.title()} event reported by GDACS."),
                "timestamp": datetime.fromisoformat(props["fromdate"].replace("Z", "+00:00")).replace(tzinfo=None) if props.get("fromdate") else datetime.utcnow(),
                "status": "active" if props.get("iscurrent", "") == "true" else "resolved",
                "source_api": "GDACS",
                "external_id": f"gdacs_{props.get('eventid', '')}_{props.get('eventtype', '')}",
            })

        logger.info(f"[GDACS] Fetched {len(disasters)} events")
        return disasters

    except Exception as e:
        logger.error(f"[GDACS] Error fetching: {e}")
        return []


# ── ReliefWeb API ────────────────────────────────────────────────────────────
RELIEFWEB_URL = "https://api.reliefweb.int/v1/disasters"

async def fetch_reliefweb_events(client: httpx.AsyncClient):
    """Fetch recent disasters from ReliefWeb (UN OCHA)"""
    try:
        params = {
            "appname": "disasterwatch",
            "limit": 20,
            "fields[include][]": "name,date,country,type,status",
            "sort[]": "date:desc",
        }
        resp = await client.get(RELIEFWEB_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        type_map = {
            "Earthquake": "earthquake", "Flood": "flood", "Flash Flood": "flood",
            "Tropical Cyclone": "storm", "Storm Surge": "storm", "Severe Local Storm": "storm",
            "Wild Fire": "fire", "Forest Fire": "fire",
            "Land Slide": "landslide", "Mud Slide": "landslide",
            "Tsunami": "tsunami", "Volcano": "landslide",
            "Drought": "flood", "Cold Wave": "storm", "Heat Wave": "storm",
        }

        disasters = []
        for item in data.get("data", []):
            fields = item.get("fields", {})
            name = fields.get("name", "Unknown disaster")
            countries = fields.get("country", [])
            country_name = countries[0].get("name", "Unknown") if countries else "Unknown"
            d_types = fields.get("type", [])
            d_type_name = d_types[0].get("name", "Storm") if d_types else "Storm"
            event_type = type_map.get(d_type_name, "storm")

            disasters.append({
                "type": event_type,
                "location": f"{country_name}, {name[:60]}",
                "lat": None,
                "lng": None,
                "severity": "medium",
                "description": f"{d_type_name}: {name}",
                "timestamp": datetime.fromisoformat(fields["date"]["created"].replace("Z", "+00:00")).replace(tzinfo=None) if fields.get("date", {}).get("created") else datetime.utcnow(),
                "status": "active" if fields.get("status") == "current" else "resolved",
                "source_api": "ReliefWeb",
                "external_id": f"reliefweb_{item.get('id', '')}",
            })

        logger.info(f"[ReliefWeb] Fetched {len(disasters)} events")
        return disasters

    except Exception as e:
        logger.error(f"[ReliefWeb] Error fetching: {e}")
        return []


# ── Save to Database ──────────────────────────────────────────────────────────
def save_disasters_to_db(disaster_list: list) -> int:
    """Save new disasters to MySQL. Returns count of newly added records."""
    db: Session = SessionLocal()
    added = 0
    try:
        for d in disaster_list:
            # Skip if this external_id already exists (dedup)
            if d.get("external_id"):
                existing = db.query(Disaster).filter(Disaster.external_id == d["external_id"]).first()
                if existing:
                    continue

            disaster = Disaster(
                type=d["type"],
                location=d["location"],
                lat=d.get("lat"),
                lng=d.get("lng"),
                severity=d["severity"],
                description=d.get("description", ""),
                timestamp=d.get("timestamp", datetime.utcnow()),
                status=d.get("status", "active"),
                source_api=d.get("source_api", ""),
                external_id=d.get("external_id"),
            )
            db.add(disaster)
            db.flush()  # get the ID

            # Auto-create alert for this disaster
            alert = Alert(
                disaster_id=disaster.id,
                message=f"🚨 {d['type'].upper()} ALERT: {d.get('description', d['location'])[:150]}",
                severity=d["severity"],
                is_read=False,
                timestamp=d.get("timestamp", datetime.utcnow()),
            )
            db.add(alert)
            added += 1

        db.commit()
        logger.info(f"[DB] Saved {added} new disasters to MySQL")
    except Exception as e:
        db.rollback()
        logger.error(f"[DB] Error saving: {e}")
    finally:
        db.close()

    return added


# ── Main Polling Loop ─────────────────────────────────────────────────────────
POLL_INTERVAL = 300  # 5 minutes

async def poll_all_sources():
    """Background task — runs forever, polls all APIs every 5 minutes."""
    logger.info("🚀 Disaster poller started — polling every 5 minutes")

    # Small delay to let FastAPI fully start up
    await asyncio.sleep(5)

    while True:
        try:
            async with httpx.AsyncClient() as client:
                # Fetch from all sources in parallel
                usgs_task = fetch_usgs_earthquakes(client)
                gdacs_task = fetch_gdacs_events(client)
                reliefweb_task = fetch_reliefweb_events(client)

                results = await asyncio.gather(usgs_task, gdacs_task, reliefweb_task, return_exceptions=True)

                all_disasters = []
                for result in results:
                    if isinstance(result, list):
                        all_disasters.extend(result)
                    elif isinstance(result, Exception):
                        logger.error(f"[Poller] Source failed: {result}")

                if all_disasters:
                    count = save_disasters_to_db(all_disasters)
                    logger.info(f"✅ Poll complete — {len(all_disasters)} fetched, {count} new saved")
                else:
                    logger.info("⚠️ Poll complete — no data from any source")

        except Exception as e:
            logger.error(f"[Poller] Fatal error: {e}")

        # Wait before next poll
        await asyncio.sleep(POLL_INTERVAL)
