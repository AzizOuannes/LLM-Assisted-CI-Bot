"""
Prompt templates for CI failure analysis - optimized for speed.
"""

def get_analysis_prompt(error_line: str, failure_context: str) -> str:
    """Generate a detailed prompt for quality CI failure analysis."""
    return f"""You are a DevOps expert analyzing a CI/CD failure. Provide a detailed analysis in JSON format.

ERROR: {error_line}
CONTEXT: {failure_context}

Analyze this CI failure and respond with valid JSON:
{{
    "summary": "Clear description of what failed and why",
    "remediations": [
        "Specific action to fix this immediate issue",
        "Preventive measure to avoid this in the future"
    ],
    "patch": "GitHub Actions YAML snippet to improve the workflow"
}}

Focus on actionable solutions and include relevant caching, dependency management, or workflow optimizations in the patch."""


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
