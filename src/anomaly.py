import re

NUM_RE = re.compile(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?%?")

def _to_float(s: str):
    s = s.replace(",", "")
    if s.endswith("%"):
        return float(s[:-1]) / 100.0
    return float(s)

def extract_numbers(text: str):
    vals = []
    for m in NUM_RE.finditer(text):
        try:
            vals.append((m.group(), _to_float(m.group())))
        except:
            pass
    return vals

def variance_flags(answer_text: str, context_texts: list[str], pct_thresh: float = 0.30):
    nums = [v for (_, v) in extract_numbers(answer_text)]
    if len(nums) < 2:
        return []

    flags = []
    for a, b in zip(nums, nums[1:]):
        if a == 0:
            continue
        delta = abs(b - a) / (abs(a) + 1e-6)
        if delta > pct_thresh:
            flags.append(
                f"Variance spike: values {a} → {b} differ by {delta:.0%} (threshold {pct_thresh:.0%})."
            )
    ctx_hint = (context_texts[0][:200] + "...") if context_texts else ""
    return flags + ([f"Context hint: {ctx_hint}"] if ctx_hint else [])
