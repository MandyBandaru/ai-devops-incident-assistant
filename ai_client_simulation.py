
import json


def get_ai_response(error_message):

    message = error_message.lower()

    # Maven error
    if "mvn: command not found" in message:

        response = {
            "explanation": "Jenkins cannot find Maven.",

            "possible_causes": [
                "Maven is not installed.",
                "Maven is missing from PATH."
            ],

            "root_cause_confirmed": False,

            "recommended_action": "Check Maven installation and PATH.",

            "diagnostic_commands": [
                "mvn -version",
                "where.exe mvn",
                "echo %PATH%"
            ],

            "troubleshooting_steps": [
                "Check whether Maven is installed.",
                "Verify that Maven's bin directory is included in PATH.",
                "Restart Jenkins after correcting the environment if necessary."
            ]
        }

    # Docker error
    elif "docker daemon" in message:

        response = {
            "explanation": "The Docker client cannot communicate with the daemon.",

            "possible_causes": [
                "Docker daemon is not running.",
                "Docker socket permissions are incorrect."
            ],

            "root_cause_confirmed": False,

            "recommended_action": "Check Docker service status and permissions.",

            "diagnostic_commands": [
                "docker version",
                "docker info",
                "docker ps",
                "Get-Service com.docker.service"
            ],

            "troubleshooting_steps": [
                "Check whether Docker Desktop is running.",
                "Verify that the Docker daemon is available.",
                "Check Docker permissions if the daemon is running.",
                "Restart Docker Desktop if necessary."
            ]
        }

    # Unknown error
    else:

        response = {
            "explanation": "The error is not recognized.",

            "possible_causes": [
                "Unknown configuration or application issue."
            ],

            "root_cause_confirmed": False,

            "recommended_action": "Inspect the full error log.",

            "diagnostic_commands": [
                "Get-Content application.log -Tail 50",
                "Get-Date",
                "Get-Process"
            ],

            "troubleshooting_steps": [
                "Collect the complete error log.",
                "Identify the affected service and pipeline stage.",
                "Check recent configuration or deployment changes.",
                "Investigate the error using supporting evidence."
            ]
        }

    return response


def main():

    try:
        error_message = input("Enter your DevOps error: ")

        if not error_message.strip():
            print("Error: Please enter an error message.")
            return

        result = get_ai_response(error_message)

        print("\nTroubleshooting Report:")
        print(json.dumps(result, indent=4))

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
