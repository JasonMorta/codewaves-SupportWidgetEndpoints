// Import the 'node-fetch' module if using Node.js version below 18.
// Uncomment the following line if necessary.
// const fetch = require('node-fetch');

// Bearer token (ensure you keep this secure)
const BEARER_TOKEN = "WXJJclVqVFhxS0VOU3pvNXJkSGc=";

// Base Freshdesk API URL
const FRESHDESK_BASE_URL = "https://newaccount1627234890025.freshdesk.com/api/v2";

// Utility function for consistent logging
const log = {
    info: (message) => console.log(`[INFO] ${new Date().toISOString()} - ${message}`),
    warn: (message) => console.warn(`[WARN] ${new Date().toISOString()} - ${message}`),
    error: (message) => console.error(`[ERROR] ${new Date().toISOString()} - ${message}`)
};

// Fetch tickets from Freshdesk API
async function fetchTickets(page, dateStamp) {
    const url = `${FRESHDESK_BASE_URL}/tickets?updated_since=${dateStamp}T00:00:00Z&order_by=created_at&order_type=asc&per_page=100&page=${page}`;
    log.info(`Constructed URL: ${url}`);

    const headers = {
        "Authorization": `Bearer ${BEARER_TOKEN}`,
        "Content-Type": "application/json",
        "Accept": "application/json"
    };

    try {
        log.info(`Fetching page ${page} of tickets...`);
        const response = await fetch(url, { method: 'GET', headers, timeout: 10000 }); // 10 seconds timeout

        // Check for HTTP errors
        if (response.status === 401) {
            log.error("Authentication failed: Invalid credentials (401 Unauthorized).");
            return { success: false, error: "Authentication failed: Invalid credentials." };
        }

        if (response.status === 400) {
            const errorData = await response.json().catch(() => ({}));
            log.error(`Bad Request (400): ${JSON.stringify(errorData)}`);
            return { success: false, error: "Bad Request: Invalid date format or parameters." };
        }

        if (!response.ok) {
            const errorText = await response.text().catch(() => 'No response body');
            log.error(`HTTP error! Status: ${response.status}. Message: ${errorText}`);
            return { success: false, error: `HTTP error! Status: ${response.status}` };
        }

        const data = await response.json().catch((err) => {
            log.error(`Failed to parse JSON response: ${err.message}`);
            throw new Error("Invalid JSON response");
        });

        log.info(`Successfully fetched page ${page} with ${data.length} tickets.`);
        return { success: true, data };

    } catch (error) {
        if (error.name === 'FetchError') {
            log.error(`Network error while fetching tickets: ${error.message}`);
            return { success: false, error: "Network error occurred while fetching tickets." };
        } else if (error.message === "Invalid JSON response") {
            // Already logged inside JSON parse catch
            return { success: false, error: "Failed to parse JSON response from server." };
        } else {
            log.error(`Unexpected error while fetching tickets: ${error.message}`);
            return { success: false, error: "An unexpected error occurred." };
        }
    }
}

// Fetch agents from Freshdesk API
async function fetchAgents() {
    const url = `${FRESHDESK_BASE_URL}/agents?per_page=100`;
    log.info(`Constructed URL for agents: ${url}`);

    const headers = {
        "Authorization": `Bearer ${BEARER_TOKEN}`,
        "Content-Type": "application/json",
        "Accept": "application/json"
    };

    try {
        log.info("Fetching agents...");
        const response = await fetch(url, { method: 'GET', headers, timeout: 10000 }); // 10 seconds timeout

        // Check for HTTP errors
        if (response.status === 401) {
            log.error("Authentication failed: Invalid credentials (401 Unauthorized).");
            return { success: false, error: "Authentication failed: Invalid credentials." };
        }

        if (!response.ok) {
            const errorText = await response.text().catch(() => 'No response body');
            log.error(`HTTP error while fetching agents! Status: ${response.status}. Message: ${errorText}`);
            return { success: false, error: `HTTP error! Status: ${response.status}` };
        }

        const agents = await response.json().catch((err) => {
            log.error(`Failed to parse JSON response for agents: ${err.message}`);
            throw new Error("Invalid JSON response");
        });

        log.info(`Successfully fetched ${agents.length} agents.`);
        return { success: true, data: agents };

    } catch (error) {
        if (error.name === 'FetchError') {
            log.error(`Network error while fetching agents: ${error.message}`);
            return { success: false, error: "Network error occurred while fetching agents." };
        } else if (error.message === "Invalid JSON response") {
            // Already logged inside JSON parse catch
            return { success: false, error: "Failed to parse JSON response from server." };
        } else {
            log.error(`Unexpected error while fetching agents: ${error.message}`);
            return { success: false, error: "An unexpected error occurred." };
        }
    }
}

// Fetch all tickets from Freshdesk API
async function fetchAllTickets(dateStamp) {
    log.info(`🏳️ Initiating fetch for all tickets since: ${dateStamp}...`);
    let page = 1;
    const allTickets = [];
    let errorDetails = null;

    while (true) {
        const { success, data, error } = await fetchTickets(page, dateStamp);

        if (!success) {
            log.error(`Failed to fetch tickets on page ${page}: ${error}`);
            errorDetails = error;
            break;
        }

        if (!Array.isArray(data)) {
            log.error(`Unexpected data format on page ${page}. Expected an array.`);
            errorDetails = "Unexpected data format received.";
            break;
        }

        allTickets.push(...data);
        log.info(`Page ${page} fetched. Total tickets accumulated: ${allTickets.length}`);

        if (data.length < 100) { // Indicates the last page
            log.info(`All tickets fetched up to page ${page}. Total tickets: ${allTickets.length}`);
            break;
        }

        page += 1;
    }

    if (errorDetails) {
        return { success: false, allTickets: [], error: errorDetails };
    } else {
        return { success: true, allTickets, error: null };
    }
}

fetchAllTickets('2024-10-08');


// Export the functions for use in other modules (if needed)
module.exports = { fetchTickets, fetchAgents, fetchAllTickets };
