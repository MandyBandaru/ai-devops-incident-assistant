def build_troubleshooting_prompt(error_message):

    prompt = f"""
You are a senior DevOps engineer.

Analyze the following DevOps error:

{error_message}

Provide the following information:

1. Explain the error in simple English.
2. List possible causes.
3. Suggest safe diagnostic commands.
4. Recommend troubleshooting steps.
5. Clearly distinguish possible causes from confirmed root causes.

Do not invent facts or claim a root cause is confirmed
without supporting evidence.
"""

    return prompt