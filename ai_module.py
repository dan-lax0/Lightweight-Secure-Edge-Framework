import json
from sklearn.ensemble import IsolationForest

LOG_FILE = "audit_log.json"


def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def extract_features(logs):
    data = []

    failure_count = 0

    for log in logs:
        temp = 25  # default

        # Extract temperature if available
        if "Temperature" in log["message"]:
            try:
                temp = int(log["message"].split(":")[-1].replace("C", "").strip())
            except:
                temp = 25

        # Status encoding
        status = 0
        if "Warning" in log["message"]:
            status = 1

        # Count failures
        if log["status"] == "FAILED":
            failure_count += 1

        data.append([temp, status, failure_count])

    return data


def run_ai_detection():
    logs = load_logs()

    if len(logs) < 5:
        print("Not enough data for AI analysis.")
        return

    data = extract_features(logs)

    # Train model
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(data)

    # Check latest entry
    latest = [data[-1]]
    result = model.predict(latest)

    print("\n===== AI ANALYSIS RESULT =====")

    if result[0] == -1:
        print("🚨 Anomaly Detected! Suspicious Activity!")
    else:
        print("✅ System Behavior Normal")


if __name__ == "__main__":
    run_ai_detection()