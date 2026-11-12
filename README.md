# AI-Powered DevOps Incident Assistant

A Python command-line prototype for analyzing DevOps error messages with selectable mock and Groq providers.

The project demonstrates provider abstraction, prompt construction, API error handling, automated testing, and Jenkins CI. It is a learning and portfolio project for DevOps, Platform Engineering, and LLMOps concepts.

## Project status

- Mock and Groq providers are implemented.
- 24 automated tests are reported passing.
- The latest Jenkins CI build is reported successful.
- This is a CLI prototype, not a production deployment.

Test and Jenkins results above are the latest reported project results; they are not live status checks.

## Project overview

The application accepts one incident message, builds a structured troubleshooting prompt, passes the incident to the selected provider, validates the response shape, and prints a report.

- **Mock provider:** Applies local rules for Maven and Docker errors, with a fallback for unrecognized incidents. It does not call an AI service.
- **Groq provider:** Sends a prompt to the Groq API and returns the model's text with provider metadata.

The application analyzes text supplied by the user. It does not connect to Jenkins, Docker, Kubernetes, cloud accounts, or other infrastructure to collect incident data or perform actions.

## Architecture and provider abstraction

Both providers implement the `AIProvider` interface and return a dictionary with the same five fields: `provider`, `model`, `incident`, `analysis`, and `root_cause_confirmed`.

```text
Single-line incident input
             |
             v
          app.py
  validates input, builds and
  prints a troubleshooting prompt
             |
             v
    providers/manager.py
       selects a provider
        /           \
       v             v
 MockProvider     GroqProvider
       |             |
       v             +-- builds the API prompt again
ai_client_          |
simulation.py       v
 local rules      Groq API
       |             |
       |             v
       |       validates returned text
       |             |
       +------       |
              \     /
               v   v
     common five-field response
               |
               v
             app.py
       validates and prints report
```

**Current implementation detail:** `app.py` builds and prints a prompt before provider selection. `GroqProvider` then builds the prompt again for its API request. `MockProvider` passes the original incident text to the local simulation and formats its troubleshooting details into the `analysis` field; it does not use the printed prompt to produce its mock response.

| Field | Meaning |
|---|---|
| `provider` | Provider name, such as `mock` or `groq`. |
| `model` | Groq model identifier or a descriptive rule-based label for the mock provider. |
| `incident` | The incident text supplied by the user. |
| `analysis` | Troubleshooting analysis as readable text. |
| `root_cause_confirmed` | Whether the root cause is confirmed. The current providers return `False`. |

## Repository structure

```text
ai-devops-incident-assistant/
|-- app.py
|-- prompt_builder.py
|-- ai_client_simulation.py
|-- providers/
|   |-- __init__.py
|   |-- base.py
|   |-- manager.py
|   |-- mock_provider.py
|   `-- groq_provider.py
|-- test_ai_client_simulation.py
|-- test_app.py
|-- test_groq_provider.py
|-- test_incident_analyzer.py
|-- test_provider_manager.py
|-- incident_analyzer.py
|-- incident_analyzer_v2.py
|-- error_handling.py
|-- api_learning.py
|-- api_auth_learning.py
|-- incident.json
|-- prompts/
|   |-- incident_v1.md
|   |-- jenkins_structured.md
|   `-- jenkins_weak.md
|-- examples/
|   |-- crashloopbackoff.txt
|   |-- hello.py
|   |-- hour4_prompt_comparison.md
|   `-- mvnerror.txt
|-- Jenkinsfile
|-- .gitignore
`-- README.md
```

The incident analyzers, error-handling exercise, and API learning scripts are earlier standalone exercises rather than part of the provider-based application flow.

## Installation on Windows

Prerequisites:

- Python 3.10 or later
- Git
- A Groq API key only if using the Groq provider

In PowerShell, clone the repository and install the Groq SDK in a virtual environment:

```powershell
git clone https://github.com/MandyBandaru/ai-devops-incident-assistant.git
Set-Location ai-devops-incident-assistant
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install groq
```

The repository does not currently include `requirements.txt` or a dependency lockfile. The Jenkins pipeline also installs `groq` directly.

## Provider configuration and execution

Provider selection uses the `AI_PROVIDER` environment variable. Its value is case-insensitive.

| Setting | Result |
|---|---|
| `AI_PROVIDER` unset | Selects the mock provider. |
| `AI_PROVIDER=mock` | Selects the mock provider. |
| `AI_PROVIDER=groq` | Selects the Groq provider. |
| Any other value | Raises an unsupported-provider error. |

The Groq provider also requires `GROQ_API_KEY`. The Groq SDK is imported by the provider manager, so install it even when using the mock provider.

### Run with the mock provider

The mock provider is the default. To select it explicitly in the current PowerShell session:

```powershell
$env:AI_PROVIDER = "mock"
python .\app.py
```

Enter one incident message when prompted, for example:

```text
Enter your DevOps error: mvn: command not found
```

### Run with Groq

The following example uses the Windows credential prompt to hide the key while it is entered. The Groq SDK reads `GROQ_API_KEY` from the process environment, so the credential is temporarily converted to a string for the application and removed from the environment afterward. Do not print or save the value.

```powershell
$groqCredential = Get-Credential -UserName "groq" -Message "Enter your Groq API key in the password field"
$secretPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($groqCredential.Password)

try {
    $env:GROQ_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($secretPointer)
    $env:AI_PROVIDER = "groq"
    python .\app.py
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($secretPointer)
    Remove-Item Env:GROQ_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:AI_PROVIDER -ErrorAction SilentlyContinue
    Remove-Variable groqCredential, secretPointer -ErrorAction SilentlyContinue
}
```

Running with Groq can make a real API request and may incur usage on the configured account. Never commit API keys or place them in source code, README examples, or shell commands.

## Example incident report excerpt

The following is a representative mock-provider report for `mvn: command not found`. It is an example; the exact output depends on the selected provider and incident.

```text
AI DEVOPS INCIDENT REPORT

Provider              : mock
Model                 : rule-based mock
Incident              : mvn: command not found
Root cause confirmed  : False

AI TROUBLESHOOTING ANALYSIS
Jenkins cannot find Maven.

Possible causes:
- Maven is not installed.
- Maven is missing from PATH.

Recommended action:
Check Maven installation and PATH.

Diagnostic commands:
- mvn -version
- where.exe mvn
- echo %PATH%

Troubleshooting steps:
- Check whether Maven is installed.
- Verify that Maven's bin directory is included in PATH.
- Restart Jenkins after correcting the environment if necessary.
```

The report offers possible explanations; it does not confirm a root cause. An engineer must investigate and review evidence.

## API error handling

`GroqProvider` translates these Groq SDK exceptions into clearer `RuntimeError` messages:

- `AuthenticationError`
- `RateLimitError`
- `APITimeoutError`
- `APIConnectionError`
- `APIStatusError`

The provider also reports missing API-key configuration, empty response choices, and empty response text. If the model response is marked as truncated, it appends a warning to the analysis.

There is no automatic retry or backoff behavior. At the application level, keyboard interruption and input/output errors receive specific handling; other exceptions are displayed as unexpected application errors.

## Tests

The project uses Python's built-in `unittest` framework. Run all discoverable unit tests from the repository directory:

```powershell
python -m unittest discover -v
```

There are 24 test methods across five test modules.

### `test_ai_client_simulation.py` (5 tests)

- `test_maven_error`
- `test_docker_error`
- `test_unknown_error`
- `test_prompt_contains_error`
- `test_prompt_is_not_empty`

### `test_app.py` (2 tests)

- `test_main_with_default_mock_provider`
- `test_main_with_groq_provider`

The Groq application test replaces the SDK client with a mock and does not send a real API request.

### `test_groq_provider.py` (10 tests)

- `test_missing_api_key`
- `test_successful_analysis`
- `test_model_selection`
- `test_empty_choices`
- `test_empty_analysis`
- `test_authentication_error`
- `test_rate_limit_error`
- `test_api_timeout_error`
- `test_api_connection_error`
- `test_api_status_error`

The API failure tests use mocked Groq clients and local HTTPX request/response objects.

### `test_incident_analyzer.py` (4 tests)

- `test_maven_error`
- `test_permission_error`
- `test_timeout_error`
- `test_unknown_error`

### `test_provider_manager.py` (3 tests)

- `test_default_provider`
- `test_mock_provider_selection`
- `test_unsupported_provider`

**Latest reported verification:** 24/24 local tests passed. The latest Jenkins CI build is reported successful. These are reported project results, not live status checks.

## Jenkins CI

The pipeline is defined in `Jenkinsfile` and has five explicit stages:

1. **Checkout Source**: Checks out the `main` branch from GitHub.
2. **Verify Python**: Prints the configured Python version.
3. **Install Dependencies**: Installs the Groq SDK.
4. **Quality Gate - Unit Tests**: Runs `python -m unittest discover -v`.
5. **Post-Test Verification**: Prints a success message after the tests pass.

Jenkins UI also displays Declarative Pipeline's automatic SCM checkout as a separate visual node. This is additional to the five explicit Jenkinsfile stages.

The current Jenkinsfile uses a machine-specific Windows Python path and Windows `bat` steps. It needs configuration changes to run on other Jenkins agents.

## Implemented features

- Python CLI for single-line incident input.
- Provider interface and environment-based provider selection.
- Mock provider with local Maven, Docker, and fallback rules.
- Common five-field provider response shape for mock and Groq.
- Groq API integration with API exception handling and response validation.
- Structured troubleshooting prompt generation.
- Unit tests for simulation, provider selection, provider behavior, and application-level flows.
- Jenkins pipeline for dependency installation and the test quality gate.

## Limitations

- This is a CLI prototype, not a production deployment.
- It analyzes text supplied by the user; it does not connect to Jenkins, Kubernetes, Docker, cloud accounts, or other infrastructure to collect incident data.
- It does not automatically execute diagnostic commands or remediation.
- The mock provider uses a small set of text rules; unrecognized incidents receive generic guidance.
- The Groq model is configured in source code.
- Dependency versions are not pinned in a project dependency file.
- Jenkins uses a hard-coded Windows Python path and is not portable across agents without configuration changes.
- The project does not include structured logging, service monitoring, deployment infrastructure, or production controls.
- AWS Bedrock and Ollama providers are not implemented.

## Planned future work

- Add more incident scenarios and test coverage.
- Evaluate troubleshooting accuracy and safety.
- Improve logging and user-facing error reporting.
- Add a dependency file with pinned or constrained package versions.
- Make the Jenkins pipeline portable across Windows and other agent environments.
- Improve configuration for model selection.
- Explore a user interface and deployment only after application behavior and operational requirements are defined.
