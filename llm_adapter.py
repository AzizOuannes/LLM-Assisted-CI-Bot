import os
import json
import requests
import re

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def summarize_with_llm(prompt: str, model: str = "phi3:mini"):
    """Call local Ollama API with optimized settings for 8GB RAM."""
    try:
        # Optimized for quality on 8GB RAM - patient settings
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 2048,        # Reasonable context for good analysis
                "temperature": 0.2,     # Slightly creative but focused
                "top_p": 0.8,          # Good token diversity
                "num_predict": 300,    # Allow longer, better responses
                "num_thread": 4        # Use more CPU threads (adjust if needed)
            }
        }, timeout=300)  # 5 minutes timeout - patient for quality
        
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "").strip()

        # More aggressive JSON cleaning for smaller models
        cleaned_text = text.replace("```json", "").replace("```", "").replace("\\n", "\n").strip()
        
        # Try multiple JSON extraction strategies
        try:
            # Strategy 1: Direct parsing
            if cleaned_text.startswith("{") and cleaned_text.endswith("}"):
                return json.loads(cleaned_text)
        except:
            pass
            
        try:
            # Strategy 2: Find any JSON object with our expected fields
            json_pattern = r'\{[^{}]*(?:"summary"|"remediations"|"patch")[^{}]*\}'
            json_match = re.search(json_pattern, cleaned_text, re.DOTALL | re.IGNORECASE)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
            
        try:
            # Strategy 3: Extract values manually from any JSON-like structure
            summary_match = re.search(r'"summary":\s*"([^"]*)"', cleaned_text, re.IGNORECASE)
            remediations_match = re.search(r'"remediations":\s*\[([^\]]*)\]', cleaned_text, re.IGNORECASE)
            patch_match = re.search(r'"patch":\s*"([^"]*)"', cleaned_text, re.IGNORECASE)
            
            if summary_match:
                return {
                    "summary": summary_match.group(1),
                    "remediations": ["Fix the identified issue", "Improve CI pipeline"],
                    "patch": patch_match.group(1) if patch_match else "# Add caching for faster builds"
                }
        except:
            pass
            
        # Last resort - return the raw text but formatted
        return {
            "summary": f"Analysis: {text[:200]}...",
            "remediations": ["Review the full response", "Check the specific error"],
            "patch": "# Add appropriate caching"
        }
        
    except requests.exceptions.Timeout:
        return {
            "summary": "LLM analysis timed out after 5 minutes - the model may be struggling with memory constraints",
            "remediations": ["Try freeing up system memory", "Consider restarting Ollama service"],
            "patch": ""
        }
    except Exception as e:
        return {
            "summary": f"LLM error: {str(e)}",
            "remediations": ["Check if Ollama is running", "Verify the model is available"],
            "patch": ""
        }


def get_llm_analysis(error_line: str, failure_context: str, model: str = "phi3:mini"):
    """Simplified function for direct LLM analysis."""
    from prompt_templates import get_analysis_prompt
    prompt = get_analysis_prompt(error_line, failure_context)
    return summarize_with_llm(prompt, model)
