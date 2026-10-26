# AI-Powered DevOps Incident Assistant

## 1. What is this project?

This project aims to build an AI assistant that helps DevOps engineers troubleshoot common technical problems.

For example:
- Jenkins pipeline failures
- Kubernetes pod errors
- Build and deployment issues
- Missing tools or environment configuration

The AI will help explain errors, identify possible causes, and suggest safe troubleshooting steps.

**Important:** The AI provides suggestions. A DevOps engineer must verify the evidence before making changes.

## 2. Why am I building this project?

As a DevOps engineer, I want to learn how AI can help solve real-world infrastructure and CI/CD problems.

Through this project, I will learn:

- Prompt engineering
- AI-assisted troubleshooting
- Python and AI model integration
- Testing and evaluating AI responses
- Git and GitHub
- CI/CD automation
- AI application safety

## 3. How does it work?

The planned workflow is:

1. A user provides an error message or incident details.
2. The AI analyzes the information.
3. The AI separates confirmed facts from possible causes.
4. The AI suggests diagnostic steps.
5. The engineer verifies the results and decides what to do next.

## 4. Current project structure

```text
ai-devops-incident-assistant/
│
├── prompts/
│   ├── incident_v1.md
│   ├── jenkins_weak.md
│   └── jenkins_structured.md
│
├── examples/
│   ├── crashloopbackoff.txt
│   └── hour4_prompt_comparison.md
│
└── README.md
```

Your actual filenames may differ as the project develops.

### What do these files mean?

| File or folder | Purpose |
|---|---|
| `prompts/` | Stores reusable instructions for the AI. |
| `incident_v1.md` | Contains the first incident-analysis prompt. |
| `jenkins_weak.md` | Contains a simple prompt used for comparison. |
| `jenkins_structured.md` | Contains a detailed Jenkins troubleshooting prompt. |
| `examples/` | Stores fictional incidents and test results. |
| `crashloopbackoff.txt` | Contains an example Kubernetes incident. |
| `hour4_prompt_comparison.md` | Records observations from prompt testing. |
| `README.md` | Explains the project to other developers. |

## 5. Example: Jenkins pipeline failure

Imagine Jenkins reports this error:

```text
/bin/sh: 1: mvn: command not found
ERROR: script returned exit code 127
```

The assistant should help answer these questions:

- What does the error mean?
- What facts can we confirm from the log?
- What could be causing the problem?
- Which diagnostic commands can help?
- What should we investigate next?

For example, Maven might be unavailable in the current shell, or its installation directory might not be in `PATH`. More investigation is needed before confirming the root cause.

## 6. Safety rules

This project follows these principles:

- Use fictional or sanitized incident data.
- Never include passwords, API keys, or secrets in prompts or GitHub files.
- Separate confirmed evidence from assumptions.
- Explain diagnostic commands before running them.
- Do not automatically execute AI-generated commands.
- Verify recommendations before changing infrastructure.
- Avoid destructive actions unless they have been reviewed and explicitly approved.

## 7. Learning progress

- [x] Learn basic prompt engineering concepts.
- [x] Create a reusable incident-analysis prompt.
- [x] Create weak and structured Jenkins prompts.
- [x] Compare prompts using example incidents.
- [x] Record prompt comparison observations.
- [ ] Improve the incident test cases.
- [ ] Create a Python application.
- [ ] Integrate an AI model API.
- [ ] Evaluate AI responses automatically.
- [ ] Add automated tests and CI/CD.
- [ ] Document the completed project.

## 8. Technologies planned

- Git and GitHub
- Python
- Jenkins
- Linux
- AI model APIs
- Automated testing
- CI/CD pipelines

Additional tools may be introduced as the project grows.

## 9. How to get started

1. Install Git and Python.
2. Open this project folder in Visual Studio Code.
3. Explore the files in `prompts/` and `examples/`.
4. Read `jenkins_weak.md`.
5. Read `jenkins_structured.md`.
6. Compare the prompts and review the results in `hour4_prompt_comparison.md`.

You do not need an AI API key for the current prompt-testing exercises.

## 10. Future improvements

The next stages will turn this learning project into a working application.

Planned improvements include:

1. Build a Python-based incident assistant.
2. Connect an AI model through an API.
3. Add test cases for common DevOps incidents.
4. Evaluate the accuracy and safety of responses.
5. Add CI/CD checks using GitHub Actions or Jenkins.
6. Add monitoring, logging, and cost tracking.

## 11. Project objective

The final goal is to build a practical AI + DevOps portfolio project that demonstrates how AI can assist with incident analysis while keeping engineers in control of troubleshooting and remediation.

**Project status:** Learning and prototype development.
