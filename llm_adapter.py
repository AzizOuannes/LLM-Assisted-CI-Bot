import os
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def summarize_with_llm(prompt: str, model: str = "phi-3-mini"):
    """Minimal adapter: call local Ollama HTTP API if available, else return a deterministic fallback."""
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "max_tokens": 256,
        }, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("text") or data.get("result") or ""

        # Very simple parsing assumption: model returns JSON-like text
        return {"summary": text.splitlines()[0] if text else "(no output)",
                "remediations": [],
                "patch": ""}
    except Exception:
        return {
            "summary": "LLM unavailable — install and run Ollama or configure OLLAMA_URL",
            "remediations": ["Install Ollama and pull phi-3-mini", "Or configure a remote LLM adapter"],
            "patch": "",
        }
