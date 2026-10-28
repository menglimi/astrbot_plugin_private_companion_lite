"""Replace plugin-owned system guidance without duplicating it on retries."""

import re


def set_system_instruction(request, name, text=""):
    """Keep configuration guidance stable and replace only its complete owned block."""
    start = f"<!-- companion_v2_native_{name}:start -->"
    end = f"<!-- companion_v2_native_{name}:end -->"
    block = f"\n\n{start}\n{text.strip()}\n{end}" if text else ""
    prompt = str(getattr(request, "system_prompt", "") or "")
    pattern = re.compile(r"\n\n" + re.escape(start) + r"\n.*?\n" + re.escape(end), re.DOTALL)
    replaced = False

    def replace_owned(match):
        nonlocal replaced
        value = "" if replaced else block
        replaced = True
        return value

    prompt = pattern.sub(replace_owned, prompt)
    request.system_prompt = prompt if replaced else prompt + block
