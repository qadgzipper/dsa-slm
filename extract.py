import os, json
import pymupdf
from pptx import Presentation
from docx import Document

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dsa")
chunks = []
failed = []

def add(text, src):
    text = text.strip()
    buf = ""
    for para in text.split("\n"):
        if len(buf) + len(para) > 1500 and len(buf) > 300:
            chunks.append({"source": src, "text": buf.strip()})
            buf = ""
        buf += para + "\n"
    if len(buf.strip()) > 300:
        chunks.append({"source": src, "text": buf.strip()})

for root, _, files in os.walk(folder):
    for fn in files:
        path = os.path.join(root, fn)
        low = fn.lower()
        try:
            if low.endswith(".pdf"):
                doc = pymupdf.open(path)
                add("\n".join(p.get_text() for p in doc), fn)
            elif low.endswith(".pptx"):
                prs = Presentation(path)
                txt = "\n".join(sh.text for s in prs.slides for sh in s.shapes if hasattr(sh, "text"))
                add(txt, fn)
            elif low.endswith(".docx"):
                d = Document(path)
                add("\n".join(p.text for p in d.paragraphs), fn)
            elif low.endswith((".ppt", ".doc")):
                failed.append(fn + " (old format, re-save as pptx/docx)")
        except Exception as e:
            failed.append(f"{fn} ({e})")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_chunks.jsonl"), "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print("Chunks:", len(chunks))
print("Files that produced text:", len({c['source'] for c in chunks}))
print("Failed or skipped:", failed)