import json, random, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(42)

def load(p): return [json.loads(l) for l in open(p, encoding="utf-8")]

def clean_text(t):
    t = re.sub(r"\\\(|\\\)|\\\[|\\\]", "", t)
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", t)
    for a, b in (("\\log", "log"), ("\\alpha", "alpha"), ("\\cdot", "*"), ("\\times", "*"),
                 ("\\leq", "<="), ("\\geq", ">="), ("\\le ", "<= "), ("\\ge ", ">= "),
                 ("\\sum", "sum"), ("\\sqrt", "sqrt"), ("\\ldots", "..."), ("\\dots", "...")):
        t = t.replace(a, b)
    return t

def clean_latex(rows):
    for r in rows:
        parts = re.split(r"(```.*?```)", r["messages"][-1]["content"], flags=re.S)
        r["messages"][-1]["content"] = "".join(p if i % 2 else clean_text(p) for i, p in enumerate(parts))
    return rows

# 1. LeetCode: remove test-leak examples, keep 4,500
test = json.load(open("test_problems.json", encoding="utf-8"))
keys = [t["question_content"][:100] for t in test] + [t["question_content"][-150:] for t in test]
lc = [r for r in load("train.jsonl") if not any(k in r["messages"][0]["content"] for k in keys)]
random.shuffle(lc)
lc = clean_latex(lc[:4500])

# 2. notes: same 40 held out as before, rest repeated twice
notes = load("notes_train.jsonl")
random.shuffle(notes)
notes_test, notes_train = notes[:40], clean_latex(notes[40:])

# 3. personalization (as is)
pers = load("personalization_train.jsonl")

# 4. gap data: hold out 20, repeat the rest twice
gap = clean_latex(load("gap_train.jsonl"))
random.shuffle(gap)
gap_test, gap_train = gap[:20], gap[20:]

final = lc + notes_train * 2 + pers + gap_train * 2
random.shuffle(final)

def save(name, rows):
    with open(name, "w", encoding="utf-8") as f:
        for e in rows: f.write(json.dumps(e, ensure_ascii=False) + "\n")
save("final_train.jsonl", final)
save("notes_test.jsonl", notes_test)
save("gap_test.jsonl", gap_test)

LAT = re.compile(r"\\\(|\\\)|\\\[|\\\]|\\log|\\alpha|\\cdot|\\times|\\leq|\\geq|\\text\{|\\frac|\\sum|\\sqrt")
def outside(t): return any(LAT.search(p) for i, p in enumerate(re.split(r"(```.*?```)", t, flags=re.S)) if i % 2 == 0)
left = sum(1 for e in final if outside(e["messages"][-1]["content"]))
print("LeetCode:", len(lc), "| notes x2:", len(notes_train) * 2, "| personalization:", len(pers), "| gap x2:", len(gap_train) * 2)
print("TOTAL:", len(final))
print("answers still containing LaTeX:", left)
print("Held out: 50 problems + 40 notes + 20 gap + 30 personalization")