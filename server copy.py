from flask import Flask, jsonify, request
from flask_cors import CORS
from freshDesk.tickets import fetch_all_tickets, fetch_agents
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
import threading
import datetime
import atexit
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global data structures to store tickets, agents, and errors
monthly_data = {
    'tickets': [],
    'agents': [],
    'error': None,
    'fetch_in_progress': False
}

daily_data = {
    'tickets': [],
    'agents': [],
    'error': None,
    'fetch_in_progress': False
}

# Lock for thread-safe operations
data_lock = threading.Lock()

def get_month_start_date():
    """Returns the first day of the current month in YYYY-MM-01 format."""
    now = datetime.datetime.utcnow()
    return now.replace(day=1).strftime('%Y-%m-%d')

def get_current_day_date():
    """Returns the current day in YYYY-MM-DD format."""
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')

def fetch_and_store_data(period='monthly'):
    """
    Fetches tickets and agents for the specified period ('monthly' or 'daily') and stores them.
    Ensures that fetches do not overlap.
    """
    global monthly_data, daily_data

    if period == 'monthly':
        data = monthly_data
        date_stamp = get_month_start_date()
        logger.info(f"🔄 Starting fetch for monthly tickets from: {date_stamp}")
    elif period == 'daily':
        data = daily_data
        date_stamp = get_current_day_date()
        logger.info(f"🔄 Starting fetch for daily tickets from: {date_stamp}")
    else:
        logger.error("Invalid period specified for fetching data.")
        return

    with data_lock:
        if data['fetch_in_progress']:
            logger.warning(f"{period.capitalize()} fetch already in progress. Skipping this run.")
            return
        data['fetch_in_progress'] = True

    try:
        # Fetch Tickets
        tickets, ticket_error = fetch_all_tickets(date_stamp)
        if tickets:
            data['tickets'] = tickets
            data['error'] = None
            logger.info(f"✅ Successfully fetched {len(tickets)} {period} tickets.")
        else:
            data['tickets'] = []
            data['error'] = ticket_error or f"No {period} tickets found."
            logger.error(f"❌ Failed to fetch {period} tickets. Error: {data['error']}")

        # Fetch Agents Only if Tickets were Successfully Fetched
        if tickets:
            agents, agent_error = fetch_agents()
            if agents:
                data['agents'] = agents
                logger.info(f"✅ Successfully fetched {len(agents)} agents for {period} tickets.")
            else:
                data['agents'] = []
                data['error'] = agent_error or f"No agents found for {period} tickets."
                logger.error(f"❌ Failed to fetch agents for {period} tickets. Error: {data['error']}")
        else:
            data['agents'] = []  # Clear agents if tickets fetch failed

    except Exception as e:
        data['tickets'] = []
        data['agents'] = []
        data['error'] = str(e)
        logger.error(f"❌ Exception during {period} fetch: {data['error']}")
    finally:
        with data_lock:
            data['fetch_in_progress'] = False
            logger.info(f"🔄 Completed fetch for {period} tickets.")

def fetch_tickets_periodically():
    """
    Periodically fetches both monthly and daily tickets.
    Ensures that fetches do not overlap.
    """
    fetch_and_store_data('monthly')
    fetch_and_store_data('daily')

@app.route('/tickets', methods=['GET'])
def get_tickets():
    """
    Endpoint to retrieve either monthly or daily tickets based on 'date-req' header.
    Responds with data if available, else with a message.
    """
    date_req = request.headers.get('date-req')

    if not date_req:
        return jsonify({"error": "The 'date-req' header is required."}), 400

    # Determine if the request is for monthly or daily tickets
    month_start_date = get_month_start_date()
    current_day_date = get_current_day_date()

    with data_lock:
        if date_req == month_start_date:
            # Handle Monthly Tickets
            data = monthly_data
            period = 'monthly'
        elif date_req == current_day_date:
            # Handle Daily Tickets
            data = daily_data
            period = 'daily'
        else:
            return jsonify({"error": "Invalid 'date-req' header value."}), 400

        # Check if fetch is in progress or data is missing
        if data['fetch_in_progress'] or not data['tickets'] or not data['agents']:
            return jsonify({"message": "Data is being fetched. Please try again later."}), 202

        # Check for errors
        if data['error']:
            return jsonify({"error": data['error']}), 500

        # Copy data to avoid race conditions
        tickets = data['tickets'].copy()
        agents = data['agents'].copy()

    # Process the tickets with agents information
    try:
        # Create a map of agent_id to agent_name for quick lookup
        agent_map = {agent["id"]: agent["contact"]["name"] for agent in agents}

        # Group tickets by responder_id
        responder_ticket_map = defaultdict(list)
        for ticket in tickets:
            if isinstance(ticket, dict):
                if (
                    ticket.get("status") in [4, 5]
                    and ticket.get("responder_id") is not None
                    and ticket.get("updated_at") >= date_req
                ):
                    responder_id = ticket["responder_id"]
                    responder_ticket_map[responder_id].append(ticket)

        # Construct the response
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

    except Exception as e:
        logger.error(f"❌ Exception while processing tickets: {str(e)}")
        return jsonify({"error": f"Exception while processing tickets: {str(e)}"}), 500

def start_scheduler():
    """
    Initializes and starts the APScheduler to fetch tickets every 5 minutes.
    Ensures that fetches do not overlap by using max_instances=1.
    """
    executors = {
        'default': ThreadPoolExecutor(2),
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    scheduler = BackgroundScheduler(
        executors=executors,
        job_defaults=job_defaults,
        timezone="UTC"
    )
    scheduler.add_job(
        func=fetch_tickets_periodically,
        trigger="interval",
        minutes=5,
        next_run_time=datetime.datetime.utcnow()  # Start immediately
    )
    scheduler.start()
    logger.info("🗓 Scheduler started to fetch tickets every 5 minutes.")

    # Ensure scheduler shuts down when the app exits
    atexit.register(lambda: scheduler.shutdown())
    return scheduler

if __name__ == '__main__':
    # Initial fetch before starting the scheduler
    logger.info("🚀 Starting initial ticket and agent fetch...")
    fetch_tickets_periodically()
    logger.info("✅ Initial ticket and agent fetch completed.")

    # Start the scheduler
    scheduler = start_scheduler()

    # Run the Flask app
    app.run(host='0.0.0.0', port=3001)
