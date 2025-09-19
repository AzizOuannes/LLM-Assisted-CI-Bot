# LLM-Assisted CI Bot: Failure Analysis & Workflow Optimization

An intelligent CI/CD failure analysis tool that uses local LLM models to automatically analyze GitHub Actions logs, provide detailed failure summaries, suggest specific remediations, and generate workflow improvements.

## 🚀 Features

- **Intelligent Log Parsing**: Automatically extracts key errors and context from GitHub Actions logs
- **LLM-Powered Analysis**: Uses Ollama with phi3:mini for detailed failure analysis
- **Failure Type Detection**: Recognizes npm, Docker, Python, test failures, and more
- **Actionable Remediations**: Provides specific steps to fix issues and prevent recurrence
- **Workflow Optimization**: Generates GitHub Actions YAML patches for better CI performance
- **16GB Optimized**: Enhanced performance with larger context windows and faster processing

## 📋 Prerequisites

- **Python 3.8+**
- **Ollama** (for local LLM inference)
- **8GB+ RAM** (16GB recommended for optimal performance)

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
  "summary": "The CI/CD pipeline failed during a test run due to an unspecified error that caused npm tests to fail.",
  "remediations": [
    "Fix the identified issue",
    "Improve CI pipeline"
  ],
  "patch": "\nsteps:\n- name: Checkout code\n  uses: actions/checkout@v2\n- name: Setup Node.js and install dependencies\n  run: |\n    npm ci --cache .npm\n- name: Run tests with coverage report\n  run: |-\n    npm test -- --coverage",
  "failure_type": "test_failure"
}
```

## ⚙️ Performance Optimizations

This version is optimized for 16GB systems with:
- **4096 token context window** (vs 2048 in basic version)
- **8 CPU threads** for faster processing
- **90-second timeout** for quicker responses
- **Enhanced accuracy** with focused temperature settings

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
├── llm_adapter.py           # Ollama interface (16GB optimized)
├── parser_module.py         # Log parsing functionality
├── prompt_templates.py      # LLM prompts for analysis
├── requirements.txt         # Python dependencies
├── tests/fixtures/          # Test log files
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

### Model Options
- **phi3:mini** (default): 2.2GB, good quality, ~30-60s on 8GB RAM
- **qwen2:0.5b**: 352MB, faster but lower quality

### Memory Optimization
The tool is optimized for 8GB RAM systems with:
- 2048 token context window
- 5-minute timeout for analysis
- Aggressive JSON parsing with fallbacks

For 16GB+ systems, you can increase performance by modifying `llm_adapter.py`:
```python
"num_ctx": 4096,        # Larger context
"timeout": 120          # Faster timeout
```

## 🔧 Supported Failure Types

- **Test Failures**: Jest, pytest, unit test failures
- **Dependency Issues**: npm, pip, package resolution
- **Docker Build**: Container build and deployment issues
- **Python Errors**: Import errors, module issues
- **Infrastructure**: Timeout, network, resource constraints

## 📊 Performance

| System RAM | Model | Typical Response Time | Quality |
|------------|-------|----------------------|---------|
| 8GB | phi3:mini | 30-60 seconds | High |
| 8GB | qwen2:0.5b | 2-5 seconds | Medium |
| 16GB+ | phi3:mini | 10-20 seconds | High |
| 16GB+ | llama3:8b | 15-30 seconds | Very High |

## 🧪 Testing

Run the included test suite:
```bash
python3 -m pytest tests/
```

Test with sample logs:
```bash
python3 run_analyzer.py --log tests/fixtures/jest_failure.log
python3 run_analyzer.py --log tests/fixtures/docker_build_failure.log
python3 run_analyzer.py --log tests/fixtures/pytest_failure.log
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
