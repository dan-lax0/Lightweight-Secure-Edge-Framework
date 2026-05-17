import random
from datetime import datetime
from audit_logger import log_event


def generate_edge_data():
    temperature = random.randint(25, 40)
    humidity = random.randint(40, 80)

    device_id = "EDGE_SIM_01"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status_options = ["Normal", "Warning: High Temp", "Sensor Calibration Required"]
    system_status = random.choice(status_options)

    edge_data = f"""
Timestamp: {timestamp}
DeviceID: {device_id}
Temperature: {temperature}C
Humidity: {humidity}%
SystemStatus: {system_status}
"""

    return edge_data


def save_to_file(data):
    with open("edge_data.txt", "w") as file:
        file.write(data)


if __name__ == "__main__":
    data = generate_edge_data()
    save_to_file(data)

    log_event("EDGE_DATA_GENERATION", "SUCCESS", "Edge data generated successfully")

    print("Edge data generated successfully!")
    print("\nGenerated Raw Data:")
    print(data)
