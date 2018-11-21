#!/usr/bin/env python3
"""Format editor contents/selection in Pythonista with Black formatter."""
import editor
import black
import console
import time

# Options
LINE_LEN = 88  # Default: 88
FAST = False  # True = skip syntax check

# Get text and selection
text = editor.get_text()
start, end = editor.get_selection()
selection = text[start:end]

if len(selection) > 0:
    raw_text = selection
else:
    raw_text = text

try:
    start_tm = time.time()
    formatted = black.format_file_contents(
        raw_text, line_length=LINE_LEN, fast=int(FAST)
    )
except black.NothingChanged:
    console.hud_alert(
        f"No formatting needed! ({time.time() - start_tm:.4f}s)", "success"
    )
except Exception as err:
    console.hud_alert(err, "error")
else:
    new_text = formatted[:-1]
    if len(selection) > 0:
        editor.replace_text(start, end, new_text)
        editor.set_selection(start, start + len(new_text))
    else:
        editor.replace_text(0, len(text), new_text)
        editor.set_selection(start, end)
    console.hud_alert(
        f"Reformatted! ({time.time() - start_tm:.4f}s)", "success")