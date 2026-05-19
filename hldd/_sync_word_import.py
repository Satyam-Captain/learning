from pathlib import Path

BASE = Path(__file__).resolve().parent
draft = (BASE / "GoF_HLDD_Draft.md").read_text(encoding="utf-8")
word = draft.replace(
    "**Document status:** Draft 0.3 — architecture-board level (second pass complete)",
    "**Document status:** Draft 0.3 — Word import (standalone, architecture-board level)",
)
old_hdr = "**Governing template:** `00_raw_inputs/HLDD_template.txt.txt`  \n**Sources:** Architecture workspace synthesis (S1–S7, ~88 use cases) — see §7 Reference Documents  \n"
new_hdr = (
    "**Format:** Complete HLDD for Microsoft Word (standalone).  \n"
    "**Template:** HLDD_template.txt.txt.  \n"
    "**Diagrams:** Export PNG from `10_diagrams/hldd/*.drawio` at each [Insert Diagram: …] marker.  \n"
    "Open via diagrams.net → Open Existing Diagram (not Import).  \n"
)
if old_hdr in word:
    word = word.replace(old_hdr, new_hdr)
else:
    word = word.replace(
        "**Governing template:** `00_raw_inputs/HLDD_template.txt.txt`",
        new_hdr.strip(),
        1,
    )
(BASE / "GoF_HLDD_Word_Import.md").write_text(word, encoding="utf-8")
print(f"Wrote Word import: {len(word.splitlines())} lines (draft: {len(draft.splitlines())})")
