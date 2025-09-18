#!/usr/bin/env python3
import argparse
import json
from parser_module import parse_actions_log
from llm_adapter import summarize_with_llm


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", required=True, help="Path to Actions log file")
    p.add_argument("--model", default="phi-3-mini", help="LLM model name for adapter")
    args = p.parse_args()

    with open(args.log, "r", encoding="utf-8") as f:
        log = f.read()

    parsed = parse_actions_log(log)
    prompt = (
        f"Analyze this CI failure log and produce a concise 1-line summary, two remediation bullets, and a small YAML patch suggestion.\n\nLog snippet:\n{parsed['snippet']}"
    )

    response = summarize_with_llm(prompt, model=args.model)
    out = {
        "summary": response.get("summary", "(no summary)"),
        "remediations": response.get("remediations", []),
        "patch": response.get("patch", ""),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
