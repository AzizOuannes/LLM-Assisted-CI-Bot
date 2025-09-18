LLM-Assisted CI Bot (minimal scaffold)

What this is
- A small starter project that parses GitHub Actions logs and produces a concise failure summary and suggested remediations.
- This scaffold includes a simple parser, a CLI entrypoint, a placeholder LLM adapter (Ollama), a reusable `action.yml`, a GitHub Actions CI workflow, and a basic test fixture.

Quick start (scaffold only)

1) Activate the venv you already created:
```bash
source .venv/bin/activate
```

2) (Optional) Install dependencies if you want to run tests or call Ollama:
```bash
pip install -r requirements.txt
```

3) Run the analyzer on the sample fixture:
```bash
python run_analyzer.py --log tests/fixtures/sample_actions.log
```

Notes
- The `llm_adapter` is a minimal placeholder that attempts to call an Ollama HTTP endpoint; if you don't run Ollama locally, the CLI will print a fallback message.
- This scaffold is intentionally small so you can iterate. Next steps: improve parsing heuristics, add prompt templates, and wire the action to create PRs with suggested workflow patches.
