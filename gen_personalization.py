import json, random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)

P = {
 "Arrays": [("Two Sum","Easy"),("Best Time to Buy and Sell Stock","Easy"),("Maximum Subarray","Medium"),("Product of Array Except Self","Medium"),("Container With Most Water","Medium"),("Trapping Rain Water","Hard")],
 "Strings": [("Valid Palindrome","Easy"),("Valid Anagram","Easy"),("Longest Substring Without Repeating Characters","Medium"),("Longest Palindromic Substring","Medium"),("Minimum Window Substring","Hard")],
 "Hashing": [("Contains Duplicate","Easy"),("Two Sum","Easy"),("Group Anagrams","Medium"),("Top K Frequent Elements","Medium"),("Longest Consecutive Sequence","Medium")],
 "Linked Lists": [("Reverse Linked List","Easy"),("Merge Two Sorted Lists","Easy"),("Linked List Cycle","Easy"),("Remove Nth Node From End of List","Medium"),("Reorder List","Medium"),("Merge k Sorted Lists","Hard")],
 "Stacks and Queues": [("Valid Parentheses","Easy"),("Implement Queue using Stacks","Easy"),("Min Stack","Medium"),("Daily Temperatures","Medium"),("Largest Rectangle in Histogram","Hard")],
 "Trees": [("Maximum Depth of Binary Tree","Easy"),("Invert Binary Tree","Easy"),("Same Tree","Easy"),("Binary Tree Level Order Traversal","Medium"),("Validate Binary Search Tree","Medium"),("Binary Tree Maximum Path Sum","Hard")],
 "Heaps": [("Last Stone Weight","Easy"),("Kth Largest Element in an Array","Medium"),("Top K Frequent Elements","Medium"),("Find Median from Data Stream","Hard")],
 "Graphs": [("Flood Fill","Easy"),("Number of Islands","Medium"),("Clone Graph","Medium"),("Course Schedule","Medium"),("Pacific Atlantic Water Flow","Medium"),("Word Ladder","Hard")],
 "Dynamic Programming": [("Climbing Stairs","Easy"),("House Robber","Medium"),("Coin Change","Medium"),("Longest Increasing Subsequence","Medium"),("Edit Distance","Medium"),("Burst Balloons","Hard")],
 "Binary Search": [("Binary Search","Easy"),("Search in Rotated Sorted Array","Medium"),("Find Minimum in Rotated Sorted Array","Medium"),("Koko Eating Bananas","Medium"),("Median of Two Sorted Arrays","Hard")],
 "Sorting": [("Merge Sorted Array","Easy"),("Meeting Rooms","Easy"),("Sort Colors","Medium"),("Merge Intervals","Medium"),("Largest Number","Medium")],
 "Recursion and Backtracking": [("Subsets","Medium"),("Permutations","Medium"),("Combination Sum","Medium"),("Word Search","Medium"),("N-Queens","Hard")],
 "Two Pointers and Sliding Window": [("Valid Palindrome","Easy"),("Two Sum II - Input Array Is Sorted","Medium"),("3Sum","Medium"),("Container With Most Water","Medium"),("Longest Substring Without Repeating Characters","Medium"),("Minimum Window Substring","Hard")],
}
ALL = list(P)
LEVEL_DIFFS = {"beginner": ["Easy"], "intermediate": ["Easy", "Medium"], "advanced": ["Medium", "Hard"]}
CORE = {
 "service": ["Arrays", "Strings", "Sorting", "Linked Lists", "Stacks and Queues", "Hashing"],
 "product": ["Trees", "Graphs", "Dynamic Programming", "Heaps", "Binary Search", "Two Pointers and Sliding Window"],
 "exam": ["Arrays", "Linked Lists", "Stacks and Queues", "Trees", "Sorting", "Graphs", "Hashing"],
}
COMPANIES = {"service": ["TCS", "Infosys", "Wipro", "Cognizant"], "product": ["Amazon", "Microsoft", "Google", "Flipkart"]}
NAMES = ["Arjun", "Priya", "Karthik", "Divya", "Rahul", "Sneha", "Vikram", "Ananya", "Harish", "Meera", "Suresh", "Kavya", "Naveen", "Lakshmi", "Rohit", "Pooja"]
HOURS = {1: "1 hour", 2: "2 hours", 3: "3 hours"}
NPROB = {1: 2, 2: 3, 3: 4}

ORDER = ["Easy", "Medium", "Hard"]
MAXD = {"beginner": "Medium", "intermediate": "Medium", "advanced": "Hard"}

def take(topic, diffs, k, used, level="advanced", widen=True):
    """pick up to k unused problems; if the pool runs dry, widen one level up (never past the level's cap)"""
    allowed = list(diffs)
    out = []
    for _ in range(3):
        cand = [n for n, d in P[topic] if d in allowed and n not in used and n not in out]
        random.shuffle(cand)
        out += cand[:k - len(out)]
        if len(out) >= k or not widen:
            break
        i = ORDER.index(allowed[-1]) + 1
        if i > ORDER.index(MAXD[level]):
            break
        allowed.append(ORDER[i])
    used.update(out)
    return out

def goal_text(gt):
    if gt == "exam":
        return "University data structures exam"
    return f"Placement drive at {random.choice(COMPANIES[gt])} ({'service' if gt == 'service' else 'product'}-based)"

def system_msg(name, goal, days, hours, level, weak, strong, solved):
    s = "You are a data structures tutor for placements and exams. Use the student profile below to personalize your answer.\n\nStudent profile:\n"
    s += f"- Name: {name}\n- Goal: {goal}\n- Days left: {days}\n- Study time: {HOURS[hours]} per day\n- Level: {level}\n"
    s += f"- Weak topics: {', '.join(weak)}\n- Strong topics: {', '.join(strong) if strong else 'none noted yet'}\n"
    if solved:
        s += "- Problems solved: " + ", ".join(f"{t} {n}" for t, n in solved.items())
    return s.strip()

def tip_for_goal(gt):
    return {
     "service": "Since service-based tests reward accuracy and speed on core problems, finish each day by re-solving one problem from memory against a timer.",
     "product": "Product-based interviews expect you to explain your approach, so after each problem say the brute force, the optimized idea and the time and space complexity out loud.",
     "exam": "For the exam, practice writing complete answers: a short definition, a labelled diagram or example, the steps, and the time complexity.",
    }[gt]

def has_left(t, level, used):
    return any(d in LEVEL_DIFFS[level] + [MAXD[level]] and n not in used for n, d in P[t])

def make_plan(days, hours, weak, strong, gt, level):
    n = NPROB[hours]
    used = set()
    study_days = days - 1
    per_weak = min(3, max(1, round(study_days * 0.6) // len(weak)))
    sched = []
    for t in weak:
        for j in range(per_weak):
            sched.append((t, "weak", j))
    rotation = []
    for t in weak + strong + CORE[gt]:
        if t not in rotation:
            rotation.append(t)
    k = 0
    while len(sched) < study_days:
        nxt = None
        for off in range(len(rotation)):
            t = rotation[(k + off) % len(rotation)]
            if has_left(t, level, used):
                nxt = t
                k = (k + off + 1)
                break
        if nxt is None:
            sched.append((None, "mixed", 0))
        else:
            sched.append((nxt, "revisit" if nxt in weak else "revise", 0))
    sched = sched[:study_days]
    lines = []
    for d, (t, kind, j) in enumerate(sched, 1):
        if kind == "mixed":
            act = "Mixed revision: re-solve problems you got wrong earlier from scratch, and write down the approach and complexity for each."
        elif kind == "weak" and j == 0:
            probs = take(t, ["Easy"], n, used, level, widen=False)
            act = f"{t}: review the concept (definitions, core operations, time complexity)" + (f", then solve {', '.join(probs)}." if probs else ".")
        else:
            probs = take(t, LEVEL_DIFFS[level], n if kind == "weak" else max(2, n - 1), used, level)
            if not probs:
                act = f"{t}: re-solve earlier problems from scratch without looking at your solutions, and write down the approach and complexity for each."
            elif kind == "weak":
                act = f"{t}: practice problems at your level: {', '.join(probs)}."
            elif kind == "revisit":
                act = f"Revisit {t} with {', '.join(probs)}."
            else:
                act = f"Revise {t} with {', '.join(probs)}."
        lines.append(f"Day {d}: {act}")
    lines.append(f"Day {days}: Timed mock test with 3 mixed problems, review every mistake, and re-read the complexities of all topics covered.")
    intro = f"Here's a {days}-day plan based on {HOURS[hours]} a day. Your weak areas ({', '.join(weak)}) get the most focused time, and the rest goes to revision."
    return intro + "\n\n" + "\n".join(lines) + "\n\n" + tip_for_goal(gt)

def make_profile():
    gt = random.choice(["service", "product", "exam"])
    days = random.randint(4, 30)
    hours = random.choice([1, 2, 3])
    level = random.choice(list(LEVEL_DIFFS))
    cands = list(dict.fromkeys(CORE[gt] + random.sample(ALL, 4)))
    pool = random.sample(cands, min(7, len(cands)))
    nweak = random.randint(1, min(3, days - 1))
    weak = pool[:nweak]
    strong = pool[nweak:nweak + random.randint(0, 3)]
    solved = {}
    for t in weak:
        solved[t] = random.randint(0, 12)
    for t in strong:
        solved[t] = random.randint(15, 45)
    return dict(gt=gt, days=days, hours=hours, level=level, weak=weak, strong=strong, solved=solved,
                name=random.choice(NAMES), goal=goal_text(gt))

PLAN_Q = ["Make me a study plan.", "Can you plan my preparation for the days I have left?", "I need a day-by-day schedule to prepare. Can you build one for me?",
          "How should I use my remaining time?", "Plan my revision, please.", "Give me a preparation plan based on my profile.",
          "I'm short on time, what should I study each day?", "Help me prepare for my {g} with a schedule."]
NEXT_Q = ["What should I practice next?", "Which topic should I focus on now?", "I have a free evening, what should I work on?",
          "Suggest what to practice today.", "Where should I put my effort this week?", "What's my next step?"]
PROG_Q = ["Here's where I am. How am I doing?", "Review my progress.", "Am I balanced across topics?", "Based on my solved counts, what's lagging?", "Give me feedback on my preparation so far."]

def ex(p, user, assistant):
    return {"messages": [
        {"role": "system", "content": system_msg(p["name"], p["goal"], p["days"], p["hours"], p["level"], p["weak"], p["strong"], p["solved"])},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant}]}

def plan_example():
    p = make_profile()
    q = random.choice(PLAN_Q).format(g="exam" if p["gt"] == "exam" else "placements")
    return ex(p, q, make_plan(p["days"], p["hours"], p["weak"], p["strong"], p["gt"], p["level"]))

def next_example():
    p = make_profile()
    weak = sorted(p["weak"], key=lambda t: p["solved"][t])
    first = weak[0]
    probs = take(first, LEVEL_DIFFS[p["level"]], 3, set(), p["level"])
    a = f"Start with {first}. You've solved only {p['solved'][first]} problem{'s' if p['solved'][first] != 1 else ''} there, so it's your biggest gap. "
    a += f"For your {p['level']} level, try {', '.join(probs)}."
    if len(weak) > 1:
        a += f" Once {first} feels comfortable, move on to {weak[1]}."
    if p["strong"]:
        a += f" Keep one short session this week on {p['strong'][0]} so it stays fresh."
    return ex(p, random.choice(NEXT_Q), a)

def progress_example():
    p = make_profile()
    if len(p["solved"]) < 3:
        return progress_example()
    r = sorted(p["solved"].items(), key=lambda x: x[1])
    (a, na), (b, nb), (c, nc) = r[0], r[1], r[-1]
    tips = {"beginner": "Stick to Easy problems until you can solve them without hints.",
            "intermediate": "Aim for mostly Medium problems and write out the time complexity every time.",
            "advanced": "Add timed Hard problems and practice explaining the trade-offs between approaches."}
    ans = (f"Your counts show {a} ({na} solved) and {b} ({nb} solved) are the thinnest areas, while {c} ({nc} solved) is furthest along. "
           f"For the next week I'd split your time roughly 60% on {a}, 25% on {b} and 15% on revising {c}. {tips[p['level']]}")
    return ex(p, random.choice(PROG_Q), ans)

data = [plan_example() for _ in range(350)] + [next_example() for _ in range(200)] + [progress_example() for _ in range(150)]
random.shuffle(data)
test, train = data[:30], data[30:]
for name, rows in (("personalization_train.jsonl", train), ("personalization_test.jsonl", test)):
    with open(name, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("train:", len(train), "| test:", len(test))
for r in random.sample(train, 2):
    print("\n--- SYSTEM:\n" + r["messages"][0]["content"] + "\n--- USER: " + r["messages"][1]["content"] + "\n--- ANSWER:\n" + r["messages"][2]["content"])
