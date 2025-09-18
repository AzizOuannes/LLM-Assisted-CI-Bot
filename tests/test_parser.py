from parser_module import parse_actions_log


def test_parse_basic():
    log = """
Run step 1
ERROR: something failed
Traceback (most recent call last):
  File \"script.py\", line 1, in <module>
    raise RuntimeError('boom')
RuntimeError: boom
"""
    out = parse_actions_log(log)
    assert "Traceback" in out["snippet"]
    assert "boom" in out["top_error"]
