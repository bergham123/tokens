import json
import os
from datetime import datetime

# 1. Get values from Environment Variables (set by GitHub Action)
send_val = os.environ.get('SEND_VAL')
fail_val = os.environ.get('FAIL_VAL')

if not send_val or not fail_val:
    print("Error: Missing input parameters.")
    exit(1)

# 2. Create filename based on Today's Date (e.g., 25-10-23.json)
today_date = datetime.now().strftime("%d-%m-%y")
filename = f"{today_date}.json"

# 3. Structure the new data entry
new_entry = {
    "time": datetime.now().strftime("%H:%M:%S"),
    "paramSend": int(send_val),
    "paramFaild": int(fail_val) # Keeping your variable name 'paramFaild'
}

# 4. Read existing data or create new list
data = []
if os.path.exists(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except:
        data = [] # Handle empty or corrupt file

data.append(new_entry)

# 5. Save the updated data
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated {filename} successfully.")
