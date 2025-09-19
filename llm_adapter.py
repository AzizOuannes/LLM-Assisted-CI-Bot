import os
import json
import requests
import re

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def summarize_with_llm(prompt: str, model: str = "phi3:mini"):
    """Call local Ollama API with optimized settings for 16GB RAM (enhanced performance)."""
    try:
        
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,        
                "temperature": 0.1,     # More focused for CI analysis
                "top_p": 0.9,          # Better token diversity
                "num_predict": 800,    # Increased from 400 for complete responses
                "num_thread": 8        # More threads for 16GB systems
            }
        }, timeout=90)  
        
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "").strip()

       
        cleaned_text = text.replace("```json", "").replace("```", "").strip()
        
        # Remove any leading/trailing text that's not JSON
        start_idx = cleaned_text.find("{")
        end_idx = cleaned_text.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            cleaned_text = cleaned_text[start_idx:end_idx]
        
        # Try multiple JSON extraction strategies
        try:
            # Strategy 1: Direct parsing of cleaned text
            return json.loads(cleaned_text)
        except:
            pass
            
        try:
            # Strategy 2: Fix common JSON issues with multiline strings
            import re
            # Handle multiline patch field by finding the content between quotes
            # This pattern handles the patch field that spans multiple lines
            
            # First, let's find where the patch field starts and ends
            patch_start = cleaned_text.find('"patch": "')
            if patch_start >= 0:
                content_start = patch_start + len('"patch": "')
                # Find the closing quote, accounting for escaped quotes
                quote_pos = content_start
                while quote_pos < len(cleaned_text):
                    quote_pos = cleaned_text.find('"', quote_pos)
                    if quote_pos == -1:
                        break
                    # Check if this quote is escaped
                    if quote_pos > 0 and cleaned_text[quote_pos - 1] != '\\':
                        # Found the closing quote
                        patch_content = cleaned_text[content_start:quote_pos]
                        # Escape the newlines and other control characters
                        escaped_content = patch_content.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                        # Replace the patch content in the text
                        fixed_text = cleaned_text[:content_start] + escaped_content + cleaned_text[quote_pos:]
                        result = json.loads(fixed_text)
                        
                        # Convert the escaped newlines back to actual newlines in patch field
                        if "patch" in result and isinstance(result["patch"], str):
                            result["patch"] = result["patch"].replace("\\n", "\n")
                        return result
                    quote_pos += 1
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
            "summary": "LLM analysis timed out after 90 seconds - try a smaller context or check system resources",
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
