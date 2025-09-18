# Test Commands

# Quick test with Jest failure:
python3 run_analyzer.py --log tests/fixtures/jest_failure.log --model phi3:mini

# Quick test with Docker failure:
python3 run_analyzer.py --log tests/fixtures/docker_build_failure.log --model phi3:mini
