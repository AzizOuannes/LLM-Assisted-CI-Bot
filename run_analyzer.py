#!/usr/bin/env python3
import argparse
import json
from parser_module import parse_actions_log
from llm_adapter import get_llm_analysis
from prompt_templates import detect_failure_type


def main():
    parser = argparse.ArgumentParser(description="Analyze GitHub Actions CI failures using LLM")
    parser.add_argument("--log", required=True, help="Path to Actions log file")
    parser.add_argument("--model", default="phi3:mini", help="LLM model name")
    args = parser.parse_args()

    # Read and parse the log file
    with open(args.log, "r", encoding="utf-8") as f:
        log_content = f.read()

    parsed_data = parse_actions_log(log_content)
    failure_type = detect_failure_type(parsed_data['top_error'], parsed_data['snippet'])
    
    # Get LLM analysis with optimized prompt - include more context for detailed analysis
    context = f"Failure type: {failure_type}\nLog context: {parsed_data['snippet'][:1000]}"
    result = get_llm_analysis(
        error_line=parsed_data['top_error'],
        failure_context=context,
        model=args.model
    )
    
    # Add detected failure type to output
    if isinstance(result, dict):
        result["failure_type"] = failure_type
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
