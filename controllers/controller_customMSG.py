from flask import jsonify

# Fetch tickets from Freshdesk API or return a custom message
def welcome():
    return jsonify({"message": "Welcome to my API!"}), 200
