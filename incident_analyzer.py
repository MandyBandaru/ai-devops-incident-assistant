def classify_error(error_message):
    if "mvn: command not found" in error_message:
        return "Possible Maven installation or PATH issue"

    elif "Permission denied" in error_message:
        return "Possible permissions issue"

    else:
        return "Unknown error - investigate further"


incident = {
    "service": "Jenkins",
    "stage": "Build",
    "build_number": 42,
    "error": "Connection timed out"
}

category = classify_error(incident["error"])

print("Service:", incident["service"])
print("Stage:", incident["stage"])
print("Error:", incident["error"])
print("Classification:", category)



import json

with open("incident.json", "r", encoding="utf-8") as file:
    incident_data = json.load(file)


# Classify the error
category = classify_error(incident_data["error"])

# Create a report containing the original incident and classification
report = {
    "service": incident_data["service"],
    "stage": incident_data["stage"],
    "build_number": incident_data["build_number"],
    "error": incident_data["error"],
    "classification": category
}

# Save the report as JSON
with open("incident_report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("Incident report saved successfully.")
print("Classification:", category)