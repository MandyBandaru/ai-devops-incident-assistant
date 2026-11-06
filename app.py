
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

        # Select the configured AI provider
        provider = get_provider()
        result = provider.analyze_incident(error_message)

        # Validate response
        if not isinstance(result, dict):
            raise TypeError("Invalid response format.")

        required_fields = [
            "provider",
            "model",
            "incident",
            "analysis",
            "root_cause_confirmed"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing response field: {field}")

        # Display readable troubleshooting report
        print("\n" + "=" * 65)
        print("             AI DEVOPS INCIDENT REPORT")
        print("=" * 65)

        print(f"\nProvider              : {result['provider']}")
        print(f"Model                 : {result['model']}")
        print(f"Incident              : {result['incident']}")
        print(f"Root cause confirmed  : {result['root_cause_confirmed']}")

        print("\n" + "-" * 65)
        print("AI TROUBLESHOOTING ANALYSIS")
        print("-" * 65)

        print(result["analysis"])

        print("\n" + "=" * 65)
        print("                 END OF REPORT")
        print("=" * 65)

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")

    except (EOFError, OSError) as error:
        print("Input/output error:", error)

    except Exception as error:
        print("Unexpected application error:", error)


if __name__ == "__main__":
    main()
