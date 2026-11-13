# Project Instructions

These instructions apply to work in this repository.

## 1. PROJECT OVERVIEW

This repository is a Python command-line incident assistant for learning and demonstrating AI + DevOps concepts. It accepts one incident message, creates troubleshooting guidance, and displays a report.

Two providers are implemented:

- **Mock provider:** Uses local rules for Maven and Docker errors and a fallback for unrecognized errors. It does not make an AI API request.
- **Groq provider:** Sends a prompt to the Groq API and returns the model response with provider metadata. It requires `GROQ_API_KEY`.

Provider selection uses `AI_PROVIDER`. If it is unset, the mock provider is selected. The current implementation is a CLI prototype, not a production deployment. It does not connect to infrastructure to collect incidents or apply changes.

### Implemented features

- CLI input validation and report display.
- A common provider interface and environment-based selection.
- Mock and Groq providers with a shared response contract.
- Prompt construction.
- Groq API exception handling and response validation.
- `unittest` coverage for simulation, application flows, provider behavior, incident classification, and provider selection.
- A Jenkins pipeline that installs the Groq SDK and runs test discovery.

### Planned features

The README identifies possible future work such as more incident scenarios, accuracy and safety evaluation, improved logging and error reporting, dependency pinning, Jenkins portability, model configuration, and possibly a user interface or deployment after requirements are defined.

Do not describe planned work as implemented. AWS Bedrock and Ollama providers are not implemented. Do not claim production deployment, automatic remediation, or real infrastructure connectivity.

## 2. PROJECT ARCHITECTURE

Preserve the existing provider architecture unless the user approves a change.

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
       +------       v
              common provider response
                     |
                     v
                   app.py
             validates and prints report
```

Current implementation detail: `app.py` builds and prints a prompt before selecting a provider. `GroqProvider` builds the prompt again for the API request. `MockProvider` passes the original incident text to the local simulation and formats its response into the common contract; it does not use the prompt printed by `app.py`.

### Main files

- `app.py`: Reads one incident line, rejects blank input, builds and prints a prompt, selects a provider, validates required response fields, and displays the report.
- `providers/base.py`: Defines the abstract `AIProvider.analyze_incident()` interface. Its return annotation is `dict`; the application performs the required-field checks.
- `providers/manager.py`: Reads `AI_PROVIDER`, defaults to `mock`, and returns the selected provider. Supported values are `mock` and `groq`.
- `providers/mock_provider.py`: Calls the local simulation and adapts its troubleshooting data to the provider response contract.
- `providers/groq_provider.py`: Reads `GROQ_API_KEY`, builds the API prompt, calls Groq, translates supported API exceptions, validates response choices and text, handles truncation warnings, and returns the provider response.
- `prompt_builder.py`: Creates troubleshooting instructions from the incident text.
- `ai_client_simulation.py`: Contains local rules for Maven, Docker, and unrecognized errors.

### Provider response contract

Both providers must return a dictionary containing these five fields:

1. `provider`
2. `model`
3. `incident`
4. `analysis`
5. `root_cause_confirmed`

Keep the mock provider's useful troubleshooting details in `analysis`: explanation, possible causes, recommended action, diagnostic commands, and troubleshooting steps.

## 3. CODING STANDARDS

- Write readable, beginner-friendly Python.
- Follow PEP 8 where practical.
- Prefer small, maintainable functions with clear names.
- Avoid unnecessary dependencies.
- Preserve existing behavior unless a change is approved.
- Do not introduce breaking changes without approval.
- Keep application, test, and documentation changes within the approved task scope.

## 4. TESTING RULES

- Use Python's built-in `unittest` framework.
- Run relevant tests after implementation.
- Run the complete suite with:

  ```text
  python -m unittest discover -v
  ```

- Never claim tests passed unless they were actually executed. Report the command and result accurately.
- Explain failures instead of hiding them or changing expectations just to make tests pass.
- Do not make real API requests during automated tests. Mock external clients and responses.
- Do not run manual connection scripts as part of automated testing unless the user explicitly requests a live API check.
- The tracked project currently contains 24 test methods across five test modules. Recheck the current suite before relying on this count.

## 5. SECURITY RULES

- Never hardcode API keys, passwords, or other credentials.
- Never print, expose in conversation, or commit credentials.
- Use environment variables for provider configuration: `AI_PROVIDER` and `GROQ_API_KEY`.
- Use dummy values only in tests, and mock external API calls.
- Do not introduce automatic fallbacks to a paid provider.
- Do not make live API requests unless the user explicitly authorizes them.
- Do not automatically execute diagnostic or remediation commands.

## 6. GIT RULES

- Never stage, commit, push, reset, or delete files without explicit user approval.
- Never include unrelated files in a commit.
- Explain Git changes before asking for approval.
- Keep application, test, and documentation commits logically separated.
- Suggest Git commands when useful, but do not execute Git changes without approval.
- Do not modify files outside the approved task.

## 7. PERSONAL LEARNING WORKFLOW - VERY IMPORTANT

The user is learning AI + DevOps and wants to understand each change.

Follow this workflow:

1. Explain the concept in simple English.
2. Explain why the change is necessary.
3. Show the proposed architecture or code changes.
4. Explain important code line by line.
5. Wait for the user's approval before implementation.
6. Implement only the approved changes.
7. Explain how to run and test the code.
8. Wait for the user's test output.
9. Review the results and explain any errors.
10. Suggest Git commands, but never execute Git changes without approval.

After an approved implementation:

- Explain exactly what was changed.
- Explain the important code line by line.
- Provide the commands for the user to run tests.
- Do not run tests automatically unless the user explicitly asks Codex to do so.
- Wait for the user's test output.
- Help the user understand failures and successful results.
- Never mark a task complete without appropriate verification evidence.

Additional learning preferences:

- ChatGPT acts as the user's personal tutor and reviewer.
- Codex acts as the user's coding assistant.
- Do not assume planned roadmap features are complete.
- Ask before installing new dependencies.
- Prefer explanations suitable for a beginner with IT experience.
