
import json

try:
    with open("incident.json", "r", encoding="utf-8") as file:
        incident = json.load(file)

    print("Incident loaded successfully")
    print("Service:", incident["service"])

except FileNotFoundError:
    print("Error: incident.json was not found.")

except json.JSONDecodeError:
    print("Error: incident.json contains invalid JSON.")

print("Program finished.")
