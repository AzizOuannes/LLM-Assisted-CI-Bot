import re

def parse_actions_log(log: str, max_lines: int = 200):
    """Naive parser: return the failing step name and the last max_lines lines as a snippet."""
    lines = log.strip().splitlines()
    snippet = "\n".join(lines[-max_lines:])

    # Try to find a failing step line
    m = re.search(r"##\[error\]([^\n]+)", log)
    failing = m.group(1).strip() if m else None

    # Try generic error message heuristics
    # Find lines that look like error messages or exception messages.
    err_lines = [l for l in lines if "ERROR" in l or "Traceback" in l or "Exception" in l or re.search(r"\bRuntimeError:|\bValueError:|\bTypeError:|\bAssertionError:", l)]
    # If we found exception message lines, prefer the last one (usually the actual message).
    if err_lines:
        # If the last line is 'Traceback...' then try to find the actual exception message after it.
        last = err_lines[-1]
        if last.strip().startswith("Traceback"):
            # search forward from traceback for a line that contains ':' which is likely the exception line
            for l in reversed(lines):
                if re.search(r":\s*\w+$", l) or re.search(r"\bRuntimeError:|\bValueError:|\bTypeError:|\bAssertionError:", l):
                    last = l
                    break
        top_error = last
    else:
        top_error = lines[-1] if lines else "No error lines found"

    return {
        "failing_step": failing,
        "snippet": snippet,
        "top_error": top_error,
    }
