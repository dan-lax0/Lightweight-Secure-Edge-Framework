import json
import hashlib
from datetime import datetime

LOG_FILE = "audit_log.json"


def calculate_hash(log_entry):
    log_string = (
        log_entry["timestamp"]
        + log_entry["event_type"]
        + log_entry["status"]
        + log_entry["message"]
        + log_entry["previous_hash"]
    )
    return hashlib.sha256(log_string.encode()).hexdigest()


def log_event(event_type, status, message):
    new_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "status": status,
        "message": message,
        "previous_hash": ""
    }

    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    # Set previous hash
    if logs:
        new_log["previous_hash"] = logs[-1]["current_hash"]
    else:
        new_log["previous_hash"] = "0"  # Genesis entry

    # Calculate current hash
    new_log["current_hash"] = calculate_hash(new_log)

    logs.append(new_log)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def verify_log_integrity():
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        print("Log file not found.")
        return False

    for i in range(1, len(logs)):
        expected_hash = calculate_hash(logs[i])
        if logs[i]["current_hash"] != expected_hash:
            print("Tampering detected at entry:", i)
            return False

        if logs[i]["previous_hash"] != logs[i - 1]["current_hash"]:
            print("Chain broken at entry:", i)
            return False

    print("Log integrity verified. No tampering detected.")
    return True