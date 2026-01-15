import json
import os
from datetime import datetime

# --- CONFIGURATION ---
DATA_DIR = "data"
SUMMARY_FILE = "summary.json"
# ---------------------

def main():
    # 1. Get inputs
    send_val = os.environ.get('SEND_VAL')
    fail_val = os.environ.get('FAIL_VAL')

    if not send_val or not fail_val:
        print("Error: Missing parameters.")
        return

    try:
        current_send = int(send_val)
        current_fail = int(fail_val)
    except ValueError:
        print("Error: Parameters must be numbers.")
        return

    # 2. Setup Data Directory
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # 3. Handle Daily Data (e.g., data/25-10-23.json)
    date_str = datetime.now().strftime("%d-%m-%y")
    daily_filename = os.path.join(DATA_DIR, f"{date_str}.json")

    new_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "paramSend": current_send,
        "paramFaild": current_fail
    }

    # Read or Create Daily File
    daily_data = []
    if os.path.exists(daily_filename):
        with open(daily_filename, 'r') as f:
            try:
                daily_data = json.load(f)
            except json.JSONDecodeError:
                daily_data = []

    daily_data.append(new_entry)

    # Save Daily File
    with open(daily_filename, 'w') as f:
        json.dump(daily_data, f, indent=4)

    # 4. Handle Summary (Totals & File Paths)
    summary_data = {
        "totalSend": 0,
        "totalFaild": 0,
        "files": []
    }

    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as f:
            try:
                summary_data = json.load(f)
            except json.JSONDecodeError:
                pass

    # Update Totals
    summary_data["totalSend"] += current_send
    summary_data["totalFaild"] += current_fail

    # Update File List (Avoid duplicates)
    if daily_filename not in summary_data["files"]:
        summary_data["files"].append(daily_filename)

    # Save Summary File
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(summary_data, f, indent=4)

    print(f"Success: Updated {daily_filename} and {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
