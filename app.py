import json

from prompt_builder import build_troubleshooting_prompt
from providers.manager import get_provider


def main():

    try:
        error_message = input("Enter your DevOps error: ")

        # Validate user input
        if not error_message.strip():
            print("Error: Please enter an error message.")
            return

        # Build prompt
        prompt = build_troubleshooting_prompt(error_message)

        print("\nGenerated AI Prompt:")
        print(prompt)

        # Get simulated response
        provider = get_provider()
        result = provider.analyze_incident(error_message)

        # Validate response
        if not isinstance(result, dict):
            raise TypeError("Invalid response format.")

        print("\nTroubleshooting Report:")
        print(json.dumps(result, indent=4))

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except (EOFError, OSError) as error:
        print("Input/output error:", error)

    except Exception as error:
        print("Unexpected application error:", error)


if __name__ == "__main__":
    main()