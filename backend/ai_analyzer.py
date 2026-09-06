import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_ai_analysis(code, bugs):

    bug_summary = "\n".join(
        [
            f"- {bug['type']} | Severity: {bug['severity']} | "
            f"Line: {bug.get('line')} | {bug['message']}"
            for bug in bugs
        ]
    )

    prompt = f"""
You are an expert software testing engineer.

Analyze the following Python code.

PYTHON CODE:
{code}

STATIC ANALYSIS RESULTS:
{bug_summary if bug_summary else "No static bugs detected."}

Provide a concise software testing analysis.

Explain:
1. Bug title
2. Root cause
3. Why it is a problem
4. Recommended fix
5. Testing recommendation

Then provide a corrected version of the complete Python code.

IMPORTANT:
Return the corrected code inside a Python code block.
Do not include unnecessary explanation inside the code block.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        explanation = response.output_text

        fixed_code = extract_code(explanation)

        return [{
            "title": "AI Code Analysis",
            "summary": "AI-powered analysis completed.",
            "explanation": explanation,
            "suggestion": "Review the AI recommendations and validate the suggested fix with additional test cases.",
            "fix": fixed_code
        }]

    except Exception as error:

        return [{
            "title": "AI Analysis Error",
            "summary": "AI analysis could not be completed.",
            "explanation": str(error),
            "suggestion": "Check your API key, internet connection, and OpenAI API configuration.",
            "fix": "No automatic fix available."
        }]


def extract_code(text):

    if "```python" in text:

        code = text.split("```python", 1)[1]

        if "```" in code:
            code = code.split("```", 1)[0]

        return code.strip()

    if "```" in text:

        code = text.split("```", 1)[1]

        if "```" in code:
            code = code.split("```", 1)[0]

        return code.strip()

    return text.strip()


def generate_ai_test_cases(code):

    prompt = f"""
You are an expert software test engineer.

Analyze this Python code:

{code}

Generate 5 important test cases based on the actual logic of the code.

Focus on:
- Normal input
- Boundary values
- Invalid input
- Edge cases
- Error conditions

For each test case provide:
1. Test case name
2. Input
3. Expected result
4. Reason for testing

Keep the response concise and easy to understand.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text

    except Exception as error:

        return f"AI test generation error: {error}"