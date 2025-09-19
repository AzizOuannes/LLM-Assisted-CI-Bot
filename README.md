# LLM-Assisted CI Bot: Failure Analysis & Workflow Optimization

An intelligent CI/CD failure analysis tool that uses local LLM models to automatically analyze GitHub Actions logs, provide detailed failure summaries, suggest specific remediations, and generate workflow improvements.

## 🚀 Features

- **Intelligent Log Parsing**: Automatically extracts key errors and context from GitHub Actions logs
- **LLM-Powered Analysis**: Uses Ollama with phi3:mini for detailed failure analysis
- **Failure Type Detection**: Recognizes npm, Docker, Python, test failures, and more
- **Actionable Remediations**: Provides specific steps to fix issues and prevent recurrence
- **Workflow Optimization**: Generates GitHub Actions YAML patches for better CI performance
- **Fast & Accurate**: Optimized for quick analysis with high-quality results

## 📋 Prerequisites

- **Python 3.8+**
- **Ollama** (for local LLM inference)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AzizOuannes/LLM-Assisted-CI-Bot.git
   cd LLM-Assisted-CI-Bot
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Install and configure Ollama**:
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   ollama pull phi3:mini
   ollama serve  # Start the Ollama service
   ```

## 🎯 Usage

### Basic Analysis
```bash
python run_analyzer.py --log path/to/actions-log.txt --model phi3:mini
```

### Example Output
```json
{
  "summary": "React test failed due to TestingLibraryElementError - unable to find navigation element with text 'Home'",
  "remediations": [
    "Update Header.test.js to search for 'Homepage' instead of 'Home' text",
    "Verify the Header component renders the correct navigation text"
  ],
  "patch": "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Setup Node.js\n        uses: actions/setup-node@v3\n        with:\n          node-version: '18'\n          cache: 'npm'\n      - run: npm ci\n      - run: npm test",
  "failure_type": "test_failure"
}
```

## 🔧 Configuration

The tool automatically detects different failure types:
- **Test failures** (Jest, pytest, JUnit)
- **Build failures** (npm, webpack, Docker)
- **Dependency issues** (package installation, conflicts)
- **Infrastructure problems** (timeouts, resource limits)

## 📁 Project Structure

```
LLM-Assisted-CI-Bot/
├── run_analyzer.py          # Main CLI tool
├── llm_adapter.py           # Ollama interface
├── parser_module.py         # Log parsing functionality
├── prompt_templates.py      # LLM prompts for analysis
├── requirements.txt         # Python dependencies
├── tests/fixtures/          # Real test log files
└── README.md               # This file
```
{
  "summary": "The CI pipeline failed during 'npm test' due to missing test dependencies",
  "remediations": [
    "Install missing test dependencies with npm ci",
    "Add caching for node_modules to prevent future dependency issues"
  ],
  "patch": "- name: Cache Node Modules\n  uses: actions/cache@v3\n  with:\n    path: ~/.npm\n    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}",
  "failure_type": "npm_failure"
}
```

## 🏗️ Project Structure

```
├── run_analyzer.py          # Main CLI application
├── llm_adapter.py           # Ollama LLM interface
├── parser_module.py         # Log parsing utilities
├── prompt_templates.py      # LLM prompts and failure detection
├── action.yml              # GitHub Action metadata
├── requirements.txt        # Python dependencies
└── tests/
    ├── fixtures/           # Sample CI failure logs
    └── test_parser.py      # Unit tests
```

## ⚙️ Configuration

## 🧪 Testing

Run the included test suite:
```bash
python3 -m pytest tests/
```

Test with sample logs:
```bash
python3 run_analyzer.py --log tests/fixtures/react_test_failure.log
python3 run_analyzer.py --log tests/fixtures/docker_npm_failure.log
python3 run_analyzer.py --log tests/fixtures/python_pytest_failure.log
python3 run_analyzer.py --log tests/fixtures/typescript_lint_failure.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM inference
- [Microsoft phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) for the base model
- GitHub Actions for CI/CD platform integration
