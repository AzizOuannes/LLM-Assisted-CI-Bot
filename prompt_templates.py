"""
Prompt templates for CI failure analysis - optimized for speed.
"""

def get_analysis_prompt(error_line: str, failure_context: str) -> str:
    """Generate a detailed prompt for quality CI failure analysis."""
    return f"""Analyze this CI failure and respond with EXACTLY this JSON structure:

ERROR: {error_line}
CONTEXT: {failure_context}

RESPOND WITH ONLY VALID JSON IN THIS EXACT FORMAT:
{{
    "summary": "one sentence explaining what failed",
    "remediations": [
        "specific command or action to fix this"
    ],
    "patch": "name: CI\\non: [push]\\njobs:\\n  test:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v3"
}}

RULES:
1. Keep "summary" to ONE clear sentence
2. "remediations" must be specific actionable commands
3. "patch" must be valid YAML on single line with \\n for newlines
4. NO nested objects, NO extra fields
5. Focus on the specific error shown"""


def detect_failure_type(error_line: str, log_snippet: str) -> str:
    """Detect the type of failure from error patterns."""
    error_lower = error_line.lower()
    
    if 'test' in error_lower or 'jest' in error_lower:
        return "test_failure"
    elif 'npm' in error_lower or 'package' in error_lower:
        return "npm_failure"
    elif 'docker' in error_lower:
        return "docker_failure"
    elif 'python' in error_lower or 'import' in error_lower:
        return "python_failure"
    else:
        return "general_failure"
