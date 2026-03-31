#!/usr/bin/env python3
"""
Update cp-solver skill with lessons learned
"""

from pathlib import Path
from datetime import datetime

skill_path = Path.home() / '.qwen/skills/cp-solver/SKILL.md'

content = skill_path.read_text(encoding='utf-8')

# Add new section: CRITICAL WORKFLOW
new_section = """
## ⚡ CRITICAL WORKFLOW (BẮT BUỘC)

### Step 0: Fetch Problem Statement (QUAN TRỌNG)
```bash
# ALWAYS fetch problem statement FIRST
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>
```

**Phân tích đề:**
1. Đọc kỹ input/output format
2. Extract constraints (N, K, time limit, memory limit)
3. Identify problem type (DP, Greedy, Math, Graph, Simulation...)
4. Compute sample by hand to verify understanding

### Step 1-5: Standard Flow (giữ nguyên)

### Step 6: Check Verdict (BẮT BUỘC)
```bash
# ALWAYS check verdict using curl
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>/submissions/<username>
```

**Verdict Interpretation:**
| Verdict | Meaning | Action |
|---------|---------|--------|
| **AC** | Accepted ✅ | Report success |
| **WA** | Wrong Answer | Re-check logic, edge cases |
| **TLE** | Time Limit | Optimize complexity |
| **RE** | Runtime Error | Check exceptions, bounds |
| **IR** | Invalid Return | Fix I/O format |

### Step 7: Optimization Strategy (QUAN TRỌNG)

**For TLE:**
1. Analyze current complexity
2. Check constraints → Required complexity
3. Find bottleneck
4. Apply optimization:
   - O(N²) → O(N log N): Sort, Binary Search, Segment Tree
   - O(N²) → O(N): Prefix sums, Sliding window, Two pointers
   - Exponential → Polynomial: Dynamic Programming

**For WA:**
1. Re-read problem statement
2. Compute sample by hand
3. Test edge cases (n=1, n=max, k=0)
4. Check modulo arithmetic
5. Verify output format

### Step 8: Return Solution to Codemath-Solver
```markdown
🔍 **CP Solver Analysis**

**Problem:** [URL]
**Issue:** [TLE/WA after X attempts]

**Phân tích:**
- Constraints: ...
- Current approach: O(...)
- Required: O(...)
- Root cause: ...

**Solution:**
[Code với algorithm mới]

**Complexity:**
- Time: O(...)
- Space: O(...)

**Next Step:**
→ Return code cho codemath-solver để submit
```

---

## 🛠 Technical Guidelines

### Using defuddle.md (CRITICAL)
```bash
# ✅ CORRECT: Use curl with defuddle.md
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>/submissions/<username>

# ❌ WRONG: Do NOT use browser snapshot
```

### Complexity Analysis Template
```
Constraints → Required Complexity:
- N ≤ 10^5: O(N) or O(N log N)
- N ≤ 1000: O(N²) acceptable
- N ≤ 20: O(2^N) acceptable
- N ≤ 10^9: O(log N) or O(1) required
```

### Common Optimizations
| Pattern | Optimization |
|---------|-------------|
| Sum over range | Prefix sums |
| Min/Max over range | Segment Tree, Sparse Table |
| Count pairs with condition | Two pointers, Binary search |
| Repeated subproblems | Dynamic Programming |
| Large exponent | Modular exponentiation |

---

"""

# Insert new section before "## Tổng quan"
if "## ⚡ CRITICAL WORKFLOW" not in content:
    content = content.replace("## Tổng quan", new_section + "## Tổng quan")

# Update version
content = content.replace('version: 2.0', 'version: 3.0')
content = content.replace('updated-on: 2026-03-12', f'updated-on: {datetime.now().strftime("%Y-%m-%d")}')

# Write back
skill_path.write_text(content, encoding='utf-8')

print("✅ Updated cp-solver skill")
print("📏 Added: CRITICAL WORKFLOW section")
print("📏 Added: defuddle.md usage guidelines")
print("📏 Added: Optimization strategy")
print("📏 Version: 2.0 → 3.0")
