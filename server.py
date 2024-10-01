from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fetch tickets from Freshdesk API
def fetch_tickets(page, dateStamp):
    url = f"https://newaccount1627234890025.freshdesk.com/api/v2/tickets?updated_since={dateStamp}T00:00:00Z&order_by=created_at&order_type=asc&per_page=100&page={page}"
    print('url = ', url)

    bearer_token = "WXJJclVqVFhxS0VOU3pvNXJkSGc="

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        print(f"Fetching page {page}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4xx/5xx responses

        if response.status_code == 401:
            print("Authentication failed: Invalid credentials.")
            return None

        if response.status_code == 400:
            print(f"Bad Request: Invalid date format. response: {response}")
            return None

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return []

# Fetch agents from Freshdesk API
def fetch_agents():
    url = "https://newaccount1627234890025.freshdesk.com/api/v2/agents?per_page=100"
    bearer_token = "WXJJclVqVFhxS0VOU3pvNXJkSGc="

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        print(f"Fetching agents...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.status_code == 401:
            print("Authentication failed: Invalid credentials.")
            return None

        agents = response.json()
        print(f"{len(agents)} agents fetched.")
        return agents

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

    return []

# Fetch all tickets from Freshdesk API
def fetch_all_tickets(dateStamp):
    print(f"🏳️ Fetching all tickets since: {dateStamp}...")
    page = 1
    all_tickets = []
    error_details = None

    while True:
        try:
            tickets = fetch_tickets(page, dateStamp)

            if tickets is None:
                return [], "Authentication failure or no tickets."

            if len(tickets) < 100:  # Stop if fewer than 100 tickets are returned
                all_tickets.extend(tickets)
                print(f"Fetched all tickets up to page {page}. Total tickets: {len(all_tickets)}")
                break

            all_tickets.extend(tickets)
            print(f"Page {page} fetched. Total tickets so far: {len(all_tickets)}")
            page += 1

        except Exception as err:
            print(f"An error occurred while fetching tickets: {err}")
            error_details = str(err)
            break

    return all_tickets, error_details

@app.route('/tickets', methods=['GET'])
def get_tickets():
    # print('headers: ', request.headers)  # Debug print to see all headers
    # print('request: ', request) 
    dateStamp = request.headers.get('date-req')
    print(f"🔞 DATE: {dateStamp}")

    # Check if the date_req header is provided
    if not dateStamp:
        return jsonify({"error": "The 'date_req' header is required."}), 400

    print(f"🔞 DATE: {dateStamp}")

    # Fetch tickets
    all_tickets, ticket_error = fetch_all_tickets(dateStamp)

    # If there was an error fetching tickets, return an error response
    if not all_tickets:
        error_message = f"Failed to fetch tickets. Date: {dateStamp}. Error: {ticket_error or 'No tickets found.'}"
        return jsonify({"error": error_message}), 500

    # Fetch agents only if fetching tickets was successful
    agents = fetch_agents()

    # If fetching agents failed, return an error response
    if not agents:
        return jsonify({"error": "Failed to fetch agents."}), 500

    # Group tickets by responder/agent ID
    responder_ticket_map = defaultdict(list)

    for ticket in all_tickets:
        if isinstance(ticket, dict):
            if ticket.get("status") in [4, 5] and ticket.get("responder_id") is not None and ticket.get("updated_at") >= dateStamp:
                responder_id = ticket["responder_id"]
                responder_ticket_map[responder_id].append(ticket)

    agent_map = {agent["id"]: agent["contact"]["name"] for agent in agents}

    result = [
        {
            "responder_id": responder_id,
            "name": agent_map.get(responder_id, "Unknown"),
            "tickets_completed": len(tickets),
            "ticket_items": tickets
        }
        for responder_id, tickets in responder_ticket_map.items()
    ]

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
