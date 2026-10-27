
import json


def classify_error(error_message):
    """Suggest a possible category based on the error text."""
    message = error_message.lower()

    if "mvn: command not found" in message:
        return "Possible Maven installation or PATH issue"
    elif "permission denied" in message:
        return "Possible permissions issue"
    elif "connection timed out" in message:
        return "Possible network connectivity issue"
    else:
        return "Unknown error - investigate further"


def main():
    try:
        # Read the incident input
        with open("incident.json", "r", encoding="utf-8") as file:
            incident = json.load(file)

        # Validate required fields
        required_fields = [
            "service",
            "stage",
            "build_number",
            "error",
        ]

        for field in required_fields:
            if field not in incident:
                raise KeyError(field)

        if not isinstance(incident["error"], str):
            raise TypeError("The error field must be text.")

        # Classify the error
        classification = classify_error(incident["error"])

        report = {
            "service": incident["service"],
            "stage": incident["stage"],
            "build_number": incident["build_number"],
            "error": incident["error"],
            "classification": classification,
            "root_cause_confirmed": False,
        }

        # Write the report
        with open(
            "incident_report_v2.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(report, file, indent=4)

        print("Incident analysis completed.")
        print("Classification:", classification)
        print("Report saved to incident_report_v2.json")

    except FileNotFoundError:
        print("Error: incident.json was not found.")

    except json.JSONDecodeError:
        print("Error: incident.json contains invalid JSON.")

    except KeyError as error:
        print("Error: required field is missing:", error)

    except TypeError as error:
        print("Error: invalid incident data:", error)

    except OSError as error:
        print("File operation error:", error)


if __name__ == "__main__":
    main()
