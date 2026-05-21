/**
 * DISASTER MANAGEMENT SYSTEM — API Configuration
 * -----------------------------------------------
 * To connect to the FastAPI + MySQL backend:
 *   1. Set USE_MOCK = false
 *   2. Ensure FastAPI server is running: uvicorn main:app --reload --port 8000
 *   3. Update API_BASE_URL if deployed to a different host
 */

const CONFIG = {
    // ─── Backend URL (FastAPI / Python) ───────────────────────────────────────
    API_BASE_URL: "http://127.0.0.1:8000",

    // ─── Toggle: true = use mock data, false = call real FastAPI endpoints ─────
    USE_MOCK: false,

    // ─── Polling interval for live dashboard updates (ms) ────────────────────
    POLL_INTERVAL: 30000,

    // ─── API Endpoints (matches FastAPI path operations) ─────────────────────
    ENDPOINTS: {
        // Auth
        LOGIN: "/api/auth/login",
        REGISTER: "/api/auth/register",

        // Disasters
        DISASTERS: "/api/disasters",
        DISASTER_BY_ID: "/api/disasters/{id}",
        DISASTER_STATS: "/api/disasters/stats",

        // Alerts
        ALERTS: "/api/alerts",
        ALERT_BY_ID: "/api/alerts/{id}",
        ALERTS_UNREAD: "/api/alerts/unread",
        ALERTS_MARK_READ: "/api/alerts/{id}/read",

        // System
        HEALTH: "/health",
        SEED: "/api/seed",
        POLLER_STATUS: "/api/poller/status",
        POLLER_TRIGGER: "/api/poller/trigger",
    }
};

/**
 * Generic API call helper — switches between mock and real backend
 * @param {string} endpointKey - Key from CONFIG.ENDPOINTS (e.g. 'DISASTERS')
 * @param {object} params      - URL/body params
 * @param {string} method      - HTTP method
 * @returns {Promise<any>}     - Parsed JSON response or null in mock mode
 */
async function apiCall(endpointKey, params = {}, method = "GET") {
    if (CONFIG.USE_MOCK) {
        console.info(`[MOCK] ${method} ${endpointKey}`, params);
        return null; // Pages handle mock data locally
    }

    let url = CONFIG.API_BASE_URL + CONFIG.ENDPOINTS[endpointKey];

    // Replace path params e.g. {id}
    const paramsCopy = { ...params };
    Object.keys(paramsCopy).forEach(k => {
        if (url.includes(`{${k}}`)) {
            url = url.replace(`{${k}}`, paramsCopy[k]);
            delete paramsCopy[k];
        }
    });

    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
            ...(localStorage.getItem("auth_token")
                ? { Authorization: `Bearer ${localStorage.getItem("auth_token")}` }
                : {}),
        },
    };

    if (method !== "GET" && method !== "HEAD") {
        options.body = JSON.stringify(paramsCopy);
    } else if (Object.keys(paramsCopy).length) {
        url += "?" + new URLSearchParams(paramsCopy);
    }

    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`API Error: ${response.status} ${response.statusText}`);
    return response.json();
}

/**
 * Fetch disasters — works in both mock and live mode
 */
async function fetchDisasters(filters = {}) {
    if (CONFIG.USE_MOCK) return MOCK_DISASTERS;
    try {
        return await apiCall("DISASTERS", filters);
    } catch (e) {
        console.error("Failed to fetch disasters:", e);
        return [];
    }
}

/**
 * Fetch stats — works in both mock and live mode
 */
async function fetchStats() {
    if (CONFIG.USE_MOCK) return DISASTER_STATS;
    try {
        return await apiCall("DISASTER_STATS");
    } catch (e) {
        console.error("Failed to fetch stats:", e);
        return { total: 0, active: 0, critical: 0, resolved: 0, regions: 0 };
    }
}

/**
 * Fetch alerts — works in both mock and live mode
 */
async function fetchAlerts() {
    if (CONFIG.USE_MOCK) return MOCK_ALERTS;
    try {
        return await apiCall("ALERTS");
    } catch (e) {
        console.error("Failed to fetch alerts:", e);
        return [];
    }
}

/**
 * Fetch unread alerts — works in both mock and live mode
 */
async function fetchUnreadAlerts() {
    if (CONFIG.USE_MOCK) return MOCK_ALERTS.filter(a => !a.is_read);
    try {
        return await apiCall("ALERTS_UNREAD");
    } catch (e) {
        console.error("Failed to fetch unread alerts:", e);
        return [];
    }
}

// ─── ROUTE PROTECTION & SECURE LOGOUT ─────────────────────────────────────────
(function() {
    // Pages that require a user to be authenticated
    const protectedPages = ["dashboard.html", "map.html", "alerts.html", "history.html"];
    
    // Get the current page filename (e.g. "dashboard.html")
    const currentPage = window.location.pathname.split("/").pop().toLowerCase();
    
    // If we are on a protected page, and NOT in mock mode, check credentials
    if (protectedPages.includes(currentPage) && !CONFIG.USE_MOCK) {
        const token = localStorage.getItem("auth_token");
        if (!token) {
            console.warn("🔐 Access denied. Redirecting to login.html...");
            window.location.href = "login.html";
        }
    }

    // Secure Logout handler
    document.addEventListener("DOMContentLoaded", () => {
        // Find any logout links (links pointing to login.html)
        const logoutLinks = document.querySelectorAll('a[href="login.html"]');
        logoutLinks.forEach(link => {
            link.addEventListener("click", (e) => {
                console.info("🔒 Logging out... Clearing secure session.");
                localStorage.removeItem("auth_token");
                localStorage.removeItem("user_email");
            });
        });
    });
})();
