/**
 * MOCK DATA — matches MySQL schema exactly
 * Table: disasters (id, type, location, lat, lng, severity, description, timestamp, status)
 * Table: alerts    (id, disaster_id, message, severity, is_read, timestamp)
 *
 * When USE_MOCK = false in config.js, the backend (FastAPI) will serve this data from MySQL
 */

const MOCK_DISASTERS = [
    { id: 1, type: "earthquake", location: "Türkiye, Kahramanmaraş", lat: 37.58, lng: 36.92, severity: "critical", description: "M7.8 earthquake, major structural damage reported across southern provinces.", timestamp: "2026-04-09T06:15:00Z", status: "active" },
    { id: 2, type: "flood", location: "Bangladesh, Dhaka", lat: 23.81, lng: 90.41, severity: "high", description: "Severe monsoon flooding in low-lying areas. 200,000+ displaced.", timestamp: "2026-04-09T04:30:00Z", status: "active" },
    { id: 3, type: "fire", location: "Australia, New South Wales", lat: -32.16, lng: 148.60, severity: "high", description: "Bushfire spreading rapidly due to high winds and dry conditions.", timestamp: "2026-04-09T02:00:00Z", status: "active" },
    { id: 4, type: "storm", location: "Philippines, Luzon", lat: 16.11, lng: 120.35, severity: "critical", description: "Super Typhoon Maring with 195 km/h winds approaching landfall.", timestamp: "2026-04-08T22:00:00Z", status: "active" },
    { id: 5, type: "landslide", location: "India, Kerala Hills", lat: 10.16, lng: 76.80, severity: "medium", description: "Heavy rains trigger landslides in hilly terrain. Roads blocked.", timestamp: "2026-04-08T18:45:00Z", status: "active" },
    { id: 6, type: "tsunami", location: "Japan, Pacific Coast", lat: 38.30, lng: 141.50, severity: "critical", description: "Tsunami warning issued after M7.5 offshore earthquake.", timestamp: "2026-04-08T14:00:00Z", status: "resolved" },
    { id: 7, type: "earthquake", location: "Nepal, Kathmandu Valley", lat: 27.69, lng: 85.31, severity: "high", description: "M6.4 earthquake, several buildings collapsed in Kathmandu.", timestamp: "2026-04-08T11:20:00Z", status: "active" },
    { id: 8, type: "flood", location: "Nigeria, Lagos State", lat: 6.52, lng: 3.38, severity: "medium", description: "Urban flooding after record 220mm rainfall in 24 hours.", timestamp: "2026-04-08T08:00:00Z", status: "active" },
    { id: 9, type: "fire", location: "Canada, British Columbia", lat: 49.88, lng: -119.49, severity: "high", description: "Wildfire consuming 15,000 hectares. Evacuation orders in effect.", timestamp: "2026-04-07T20:00:00Z", status: "active" },
    { id: 10, type: "storm", location: "USA, Gulf Coast", lat: 29.76, lng: -95.37, severity: "critical", description: "Category 4 hurricane with storm surge warning for coastal areas.", timestamp: "2026-04-07T16:00:00Z", status: "resolved" },
    { id: 11, type: "landslide", location: "Colombia, Medellín", lat: 6.25, lng: -75.56, severity: "high", description: "Landslide following 3 days of continuous heavy rain.", timestamp: "2026-04-07T12:30:00Z", status: "resolved" },
    { id: 12, type: "earthquake", location: "Indonesia, Sulawesi", lat: -0.90, lng: 119.87, severity: "critical", description: "M7.2 earthquake, tsunami warning lifted after inspection.", timestamp: "2026-04-07T06:00:00Z", status: "resolved" },
    { id: 13, type: "flood", location: "Pakistan, Balochistan", lat: 30.18, lng: 67.03, severity: "high", description: "Flash floods from melting glaciers. Infrastructure severely damaged.", timestamp: "2026-04-06T20:00:00Z", status: "active" },
    { id: 14, type: "storm", location: "India, Cyclone, Bay of Bengal", lat: 13.08, lng: 80.27, severity: "high", description: "Cyclone alert for coastal Tamil Nadu and Andhra Pradesh.", timestamp: "2026-04-06T14:00:00Z", status: "active" },
    { id: 15, type: "fire", location: "Greece, Attica Region", lat: 38.02, lng: 23.80, severity: "medium", description: "Forest fires near Athens, strong winds hindering containment.", timestamp: "2026-04-06T10:00:00Z", status: "resolved" },
    { id: 16, type: "earthquake", location: "Mexico, Oaxaca", lat: 17.06, lng: -96.72, severity: "medium", description: "M5.8 earthquake, minor damage reported. No casualties.", timestamp: "2026-04-05T22:00:00Z", status: "resolved" },
    { id: 17, type: "tsunami", location: "Chile, Biobío Region", lat: -36.82, lng: -73.05, severity: "high", description: "Tsunami warning following M7.0 offshore seismic event.", timestamp: "2026-04-05T16:00:00Z", status: "resolved" },
    { id: 18, type: "flood", location: "Germany, Rhine Valley", lat: 51.22, lng: 6.77, severity: "medium", description: "Rhine river overflow affecting riverside towns.", timestamp: "2026-04-05T10:00:00Z", status: "active" },
    { id: 19, type: "storm", location: "Caribbean, Cuba", lat: 21.52, lng: -77.78, severity: "medium", description: "Tropical storm with 110 km/h winds passing over eastern Cuba.", timestamp: "2026-04-04T18:00:00Z", status: "resolved" },
    { id: 20, type: "landslide", location: "Vietnam, Quảng Ngãi", lat: 15.12, lng: 108.80, severity: "medium", description: "Landslide triggered by Typhoon aftermath. Village evacuation.", timestamp: "2026-04-04T12:00:00Z", status: "resolved" },
    { id: 21, type: "earthquake", location: "Iran, Hormozgan", lat: 27.20, lng: 56.27, severity: "high", description: "M6.1 earthquake affecting coastal communities.", timestamp: "2026-04-04T06:00:00Z", status: "resolved" },
    { id: 22, type: "fire", location: "Portugal, Algarve", lat: 37.32, lng: -8.10, severity: "medium", description: "Forest fire in Algarve region. 5,000 ha burned.", timestamp: "2026-04-03T14:00:00Z", status: "resolved" },
    { id: 23, type: "flood", location: "Brazil, Bahia", lat: -14.86, lng: -40.85, severity: "critical", description: "Extreme flooding displaces 1 million in northeastern Brazil.", timestamp: "2026-04-03T08:00:00Z", status: "active" },
    { id: 24, type: "storm", location: "Madagascar, East Coast", lat: -19.87, lng: 47.54, severity: "high", description: "Cyclone Delia makes landfall with 180 km/h gusts.", timestamp: "2026-04-02T20:00:00Z", status: "resolved" },
    { id: 25, type: "earthquake", location: "China, Sichuan Province", lat: 30.06, lng: 102.56, severity: "medium", description: "M5.5 earthquake near Kangding, felt across Sichuan.", timestamp: "2026-04-02T14:00:00Z", status: "resolved" },
    { id: 26, type: "landslide", location: "Peru, Loreto Region", lat: -3.75, lng: -73.25, severity: "high", description: "Landslides block main highway; 12 communities isolated.", timestamp: "2026-04-02T08:00:00Z", status: "resolved" },
    { id: 27, type: "fire", location: "USA, California", lat: 34.05, lng: -118.24, severity: "critical", description: "Wind-driven wildfire in LA County. 50,000 under evacuation.", timestamp: "2026-04-01T20:00:00Z", status: "active" },
    { id: 28, type: "tsunami", location: "Pacific Ring of Fire", lat: 2.30, lng: 128.18, severity: "medium", description: "Tsunami advisory issued. Waves up to 1m expected.", timestamp: "2026-04-01T14:00:00Z", status: "resolved" },
    { id: 29, type: "flood", location: "Sudan, Khartoum", lat: 15.55, lng: 32.53, severity: "high", description: "Nile river overflow submerging riverside districts.", timestamp: "2026-04-01T08:00:00Z", status: "active" },
    { id: 30, type: "storm", location: "Italy, Sardinia", lat: 40.12, lng: 9.02, severity: "medium", description: "Mediterranean storm with heavy rain and hail.", timestamp: "2026-03-31T20:00:00Z", status: "resolved" },
];

const MOCK_ALERTS = MOCK_DISASTERS.map((d, i) => ({
    id: i + 1,
    disaster_id: d.id,
    type: d.type,
    location: d.location,
    message: `⚠️ ${d.type.toUpperCase()} ALERT: ${d.description.slice(0, 90)}...`,
    severity: d.severity,
    is_read: d.status === "resolved",
    timestamp: d.timestamp,
}));

const DISASTER_STATS = {
    total: MOCK_DISASTERS.length,
    active: MOCK_DISASTERS.filter(d => d.status === "active").length,
    critical: MOCK_DISASTERS.filter(d => d.severity === "critical").length,
    resolved: MOCK_DISASTERS.filter(d => d.status === "resolved").length,
    regions: new Set(MOCK_DISASTERS.map(d => d.location.split(",")[1]?.trim() || d.location)).size,
    types: {
        earthquake: MOCK_DISASTERS.filter(d => d.type === "earthquake").length,
        flood: MOCK_DISASTERS.filter(d => d.type === "flood").length,
        fire: MOCK_DISASTERS.filter(d => d.type === "fire").length,
        storm: MOCK_DISASTERS.filter(d => d.type === "storm").length,
        landslide: MOCK_DISASTERS.filter(d => d.type === "landslide").length,
        tsunami: MOCK_DISASTERS.filter(d => d.type === "tsunami").length,
    }
};

// Disaster type emoji and color maps
const TYPE_CONFIG = {
    earthquake: { emoji: "🌍", color: "#ff4757", label: "Earthquake" },
    flood: { emoji: "🌊", color: "#00d4ff", label: "Flood" },
    fire: { emoji: "🔥", color: "#ff6b35", label: "Wildfire" },
    storm: { emoji: "🌪️", color: "#a855f7", label: "Storm" },
    landslide: { emoji: "⛰️", color: "#f1c40f", label: "Landslide" },
    tsunami: { emoji: "🌊", color: "#0084a8", label: "Tsunami" },
};

// Helper: format timestamp to readable
function formatTime(isoString) {
    const d = new Date(isoString);
    return d.toLocaleString("en-US", { month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}

// Helper: time ago
function timeAgo(isoString) {
    const secs = Math.floor((new Date() - new Date(isoString)) / 1000);
    if (secs < 60) return "Just now";
    if (secs < 3600) return `${Math.floor(secs / 60)}m ago`;
    if (secs < 86400) return `${Math.floor(secs / 3600)}h ago`;
    return `${Math.floor(secs / 86400)}d ago`;
}
