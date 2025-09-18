# LLM-Assisted CI Bot: Failure Analysis & Workflow Optimization

An intelligent CI/CD failure analysis tool that uses local LLM models to automatically analyze GitHub Actions logs, provide detailed failure summaries, suggest specific remediations, and generate workflow improvements.

## 🚀 Features

- **Intelligent Log Parsing**: Automatically extracts key errors and context from GitHub Actions logs
- **LLM-Powered Analysis**: Uses Ollama with phi3:mini for detailed failure analysis
- **Failure Type Detection**: Recognizes npm, Docker, Python, test failures, and more
- **Actionable Remediations**: Provides specific steps to fix issues and prevent recurrence
- **Workflow Optimization**: Generates GitHub Actions YAML patches for better CI performance
- **Memory Optimized**: Configured to work efficiently on 8GB RAM systems

## 📋 Prerequisites

- **Python 3.8+**
- **Ollama** (for local LLM inference)
- **8GB+ RAM** (16GB recommended for better performance)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "LLM Assisted CI Bot"
   ```

2. **Set up Python environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
python3 run_analyzer.py --log path/to/actions-log.txt --model phi3:mini
```

### Example Output
```json
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
