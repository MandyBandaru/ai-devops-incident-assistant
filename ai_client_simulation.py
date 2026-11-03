import os
import json


def get_ai_response(error_message):

    message = error_message.lower()

    if "mvn: command not found" in message:

        response = {
            "explanation": "Jenkins cannot find Maven.",
            "possible_causes": [
                "Maven is not installed.",
                "Maven is missing from PATH."
            ],
            "root_cause_confirmed": False,
            "recommended_action": "Check Maven installation and PATH."
        }

    elif "docker daemon" in message:

        response = {
            "explanation": "The Docker client cannot communicate with the daemon.",
            "possible_causes": [
                "Docker daemon is not running.",
                "Docker socket permissions are incorrect."
            ],
            "root_cause_confirmed": False,
            "recommended_action": "Check Docker service status and permissions."
        }

    else:

        response = {
            "explanation": "The error is not recognized.",
            "possible_causes": [
                "Unknown configuration or application issue."
            ],
            "root_cause_confirmed": False,
            "recommended_action": "Inspect the full error log."
        }

    return response


def main():

    error_message = input("Enter your DevOps error: ")

    if not error_message.strip():
        print("Error: Please enter an error message.")
        return

    result = get_ai_response(error_message)

    print("\nTroubleshooting Report:")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()