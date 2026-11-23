import json, re, os, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rows = [json.loads(l) for l in open("final_train.jsonl", encoding="utf-8")]

KEYS = {
 "Arrays": ["array"], "Strings": ["string", "palindrome", "anagram"],
 "Linked Lists": ["linked list", "singly", "doubly", "circular list"],
 "Stacks": ["stack", "lifo"], "Queues": ["queue", "fifo", "deque"],
 "Trees (general/BST)": ["binary tree", "binary search tree", "bst", "tree traversal", "inorder", "preorder", "postorder"],
 "Advanced trees": ["avl", "b-tree", "b+ tree", "trie", "red-black", "segment tree", "fenwick", "binomial"],
 "Heaps/Priority queues": ["heap", "priority queue"], "Hashing": ["hash"],
 "Graphs": ["graph", "bfs", "dfs", "dijkstra", "adjacency", "topological", "spanning tree"],
 "Dynamic programming": ["dynamic programming", "memoiz", "knapsack"],
 "Sorting": ["sort"], "Searching": ["binary search", "linear search"],
 "Recursion/Backtracking": ["recursion", "recursive", "backtrack"],
 "Greedy": ["greedy"], "Union-Find": ["union find", "union-find", "disjoint set"],
 "Complexity analysis": ["time complexity", "big o", "big-o", "space complexity", "amortized"],
 "Bit manipulation": ["bit manipulation", "bitwise"],
}

def kind(r):
    m = r["messages"]
    u = m[-2]["content"]
    if m[0]["role"] == "system": return "personal"
    if "Topics:" in u or "hint for this problem" in u: return "leetcode"
    return "notes"

cnt = {t: collections.Counter() for t in KEYS}
kinds = collections.Counter()
style = collections.Counter()
for r in rows:
    k = kind(r); kinds[k] += 1
    if k == "personal": continue
    u = r["messages"][-2]["content"]
    text = (u if k == "leetcode" else u + " " + r["messages"][-1]["content"]).lower()
    for t, ks in KEYS.items():
        if any(x in text for x in ks): cnt[t][k] += 1
    if k == "notes":
        if "which option is correct" in u.lower(): style["MCQ"] += 1
        if re.search(r"difference between|compare|advantages|disadvantages|when would you|real-world|applications|why ", u.lower()): style["compare/why/applications"] += 1

print("example types:", dict(kinds), "\n")
print(f"{'Topic':26}{'LeetCode':>9}{'Notes':>7}")
for t in sorted(KEYS, key=lambda t: cnt[t]["notes"]):
    flag = "  <-- THIN in notes" if cnt[t]["notes"] < 30 else ""
    print(f"{t:26}{cnt[t]['leetcode']:>9}{cnt[t]['notes']:>7}{flag}")
print("\nnotes question styles:", dict(style))
