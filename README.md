# AI-Powered DevOps Incident Assistant

**Project status:** Working Python prototype — simulated AI response engine

## 1. Project Overview

The AI-Powered DevOps Incident Assistant is a Python-based learning and portfolio project designed to help DevOps engineers understand and troubleshoot common infrastructure, build, and deployment errors.

The application accepts a DevOps error message, builds a structured troubleshooting prompt, and generates a troubleshooting report.

**Current implementation:** The response engine uses Python rule-based logic to simulate AI responses. A real AI model/API has not yet been integrated.

## 2. Project Objectives

The goal is to demonstrate practical knowledge of:

- Python application development
- Prompt engineering
- AI-assisted DevOps troubleshooting concepts
- HTTP requests and API integration fundamentals
- Error handling and input validation
- Automated testing with Python `unittest`
- Git, GitHub, Jenkins, and CI/CD
- AI application safety and responsible recommendations

## 3. Current Architecture

The application follows a modular Python architecture.

```text
User Input
    |
    v
app.py
    |
    v
prompt_builder.py
    |
    v
ai_client_simulation.py
    |
    v
Troubleshooting Report
```

### Component responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Handles user input, coordinates application execution, validates responses, and handles exceptions. |
| `prompt_builder.py` | Creates structured troubleshooting instructions using the supplied error message. |
| `ai_client_simulation.py` | Uses Python rules to generate simulated troubleshooting responses. |
| `test_ai_client_simulation.py` | Automatically tests response classification and prompt generation. |
| `prompts/` | Stores reusable troubleshooting prompts. |
| `examples/` | Stores example incidents and learning exercises. |

## 4. Current Features Implemented

- Accepts DevOps error messages from the user.
- Validates empty input.
- Generates structured troubleshooting prompts.
- Recognizes Maven-related errors.
- Recognizes Docker daemon-related errors.
- Handles unknown errors.
- Returns explanations, possible causes, and recommended actions.
- Distinguishes possible causes from confirmed root causes.
- Handles application interruptions and input/output errors.
- Includes automated unit tests.

**Important:** The application does not currently call an LLM. Its responses are based on predefined Python conditions.

## 5. Example Incident

Input:

```text
mvn: command not found
```

Example simulated response:

```json
{
    "explanation": "Jenkins cannot find Maven.",
    "possible_causes": [
        "Maven is not installed.",
        "Maven is missing from PATH."
    ],
    "root_cause_confirmed": false,
    "recommended_action": "Check Maven installation and PATH."
}
```

The report provides possible explanations, not a confirmed root cause. An engineer must investigate the Jenkins agent before deciding what caused the failure.

## 6. Project Structure

```text
ai-devops-incident-assistant/
|
|-- app.py
|-- prompt_builder.py
|-- ai_client_simulation.py
|-- test_ai_client_simulation.py
|
|-- incident_analyzer.py
|-- incident_analyzer_v2.py
|-- test_incident_analyzer.py
|
|-- incident.json
|-- incident_report.json
|-- incident_report_v2.json
|
|-- Jenkinsfile
|-- README.md
|-- .gitignore
|
|-- prompts/
|   |-- incident_v1.md
|   |-- jenkins_weak.md
|   |-- jenkins_structured.md
|
|-- examples/
```

Some files belong to earlier learning exercises. Generated reports and sample incident data should be reviewed before committing them.

## 7. Environment and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code (recommended)

### Clone the repository

```bash
git clone https://github.com/MandyBandaru/ai-devops-incident-assistant.git

cd ai-devops-incident-assistant
```

### Verify Python

```bash
python --version
```

The prototype currently uses Python 3.13.1.

No external AI API key is required to run the simulated application.

## 8. Run the Application

From the project root directory:

```bash
python app.py
```

Enter an error message when prompted.

Example:

```text
Enter your DevOps error: mvn: command not found
```

The application generates a structured troubleshooting prompt and a simulated troubleshooting report.

## 9. Run Automated Tests

The project uses Python's built-in `unittest` framework.

Run the tests:

```bash
python -m unittest -v test_ai_client_simulation
```

### Current verified test coverage

| Test | Purpose |
|---|---|
| `test_maven_error` | Verifies Maven error handling. |
| `test_docker_error` | Verifies Docker error handling. |
| `test_unknown_error` | Verifies unknown error handling. |
| `test_prompt_contains_error` | Verifies that the prompt includes the input error. |
| `test_prompt_is_not_empty` | Verifies prompt generation. |

**Latest verified result:** 5 tests passed.

## 10. HTTP and API Learning

As part of the development exercises, HTTP GET and POST requests were tested using Python's `requests` library and the HTTPBin testing service.

These exercises demonstrate:

- Sending HTTP GET requests.
- Sending JSON payloads using POST.
- Reading HTTP status codes.
- Parsing JSON responses.
- Handling request exceptions.
- Understanding API authentication and environment variables.

These exercises do not represent a live integration with an AI provider.

## 11. Safety and Reliability Principles

The project follows these principles:

- Never commit API keys, passwords, or secrets.
- Use sanitized incident data.
- Separate confirmed evidence from assumptions.
- Do not claim a root cause is confirmed without supporting evidence.
- Explain diagnostic commands before execution.
- Never automatically execute AI-generated remediation commands.
- Require engineer review before infrastructure changes.

## 12. Development Progress

### Completed and verified

- [x] Basic prompt engineering concepts.
- [x] Reusable incident-analysis prompt.
- [x] Weak and structured Jenkins prompts.
- [x] Prompt comparison exercises.
- [x] Python application structure.
- [x] Modular application architecture.
- [x] Rule-based Maven and Docker error classification.
- [x] Unknown error handling.
- [x] Input validation and exception handling.
- [x] HTTP GET and POST exercises.
- [x] Five automated tests passed.

### Planned improvements

- [ ] Integrate a real AI model through an API.
- [ ] Add more DevOps incident scenarios.
- [ ] Evaluate AI response accuracy and safety.
- [ ] Improve automated test coverage.
- [ ] Add structured logging.
- [ ] Make the Jenkins pipeline portable across agents.
- [ ] Integrate automated CI/CD validation.
- [ ] Add deployment and monitoring capabilities.

## 13. Future Architecture

The planned architecture will replace the simulated response engine with a real AI provider integration.

```text
User Input
    |
    v
Application
    |
    v
Prompt Builder
    |
    v
AI Provider API
    |
    v
Response Validation
    |
    v
Troubleshooting Report
    |
    v
Engineer Review
```

The application will continue to keep engineers in control of diagnosis and remediation.

## 14. Final Project Goal

Build a practical AI + DevOps incident troubleshooting assistant that demonstrates Python development, prompt engineering, LLM integration, automated testing, CI/CD, and responsible AI usage.

The final deliverable will be a portfolio project that demonstrates how AI can support real-world DevOps operations.