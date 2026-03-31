#!/usr/bin/env python3
"""
Update codemath-solver skill with lessons learned
"""

from pathlib import Path
from datetime import datetime

skill_path = Path.home() / '.qwen/skills/codemath-solver/SKILL.md'

content = skill_path.read_text(encoding='utf-8')

# Add new section: CRITICAL WORKFLOW
new_section = """
## ⚡ CRITICAL WORKFLOW (BẮT BUỘC)

### Step 0: Đọc Đề Bài (QUAN TRỌNG NHẤT)
```bash
# ALWAYS fetch problem statement FIRST using curl
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>
```

**Phân tích:**
1. Đọc kỹ đề - KHÔNG assume problem type
2. Extract: Input format, Output format, Constraints
3. Identify: Đây là dạng bài gì? (DP, Greedy, Graph, Math, Simulation...)
4. Sample test: Tính bằng tay để verify understanding

### Step 1-5: Standard Flow (giữ nguyên)

### Step 6: Check Verdict (BẮT BUỘC)
```bash
# ALWAYS check verdict using curl (NOT browser snapshot)
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>/submissions/<username>
```

**Verdict Interpretation:**
| Verdict | Action |
|---------|--------|
| **AC** | ✅ Done! Report score |
| **IR** | ❌ Input/Output format issue → Fix I/O, resubmit |
| **WA** | ❌ Wrong logic → Debug with sample, resubmit |
| **TLE** | ❌ Too slow → Optimize complexity, resubmit |
| **RE** | ❌ Runtime error → Check edge cases, resubmit |

### Step 7: Iteration Loop (QUAN TRỌNG)
```
Submit → Check Verdict → Analyze → Fix → Resubmit
   ↓
[AC] or [3 attempts] → Stop
   ↓
[Not AC after 3 attempts] → Delegate to cp-solver
```

**Rules:**
- Max 3 attempts per problem
- After 3 IR/WA/TLE/RE → **DELEGATE to cp-solver immediately**
- Each attempt MUST have:
  - Verified with sample test
  - Clear hypothesis about what was wrong
  - Specific fix applied

### Step 8: Delegation to CP-Solver
```json
{
  "task": "cp-solver",
  "problem_url": "https://...",
  "current_code": "...",
  "verdict": "TLE",
  "attempts": 3,
  "constraints": "N ≤ 10^5, K ≤ 10^9",
  "reason": "O(N²) algorithm, need O(N log N)"
}
```

---

## 🛠 Technical Guidelines

### Using defuddle.md (CRITICAL)
```bash
# ✅ CORRECT: Use curl with defuddle.md
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>/submissions/<username>

# ❌ WRONG: Do NOT use browser snapshot for verdict
# Browser automation may not render dynamic content
```

### Input/Output Best Practices
```python
# ✅ CORRECT: Read all input at once
import sys
data = sys.stdin.read().split()
n = int(data[0])

# ✅ CORRECT: Print with newline (unless specified)
print(result)

# ❌ WRONG: Line by line reading (may fail on CMOJ)
# input()  # May fail with empty lines
```

### Common IR Causes & Fixes
| Issue | Fix |
|-------|-----|
| Empty input handling | `if not data: return` |
| Whitespace issues | Use `.split()` not `.split(' ')` |
| Missing newline | `print(result)` not `print(result, end='')` |
| Exception in code | Wrap in try-except, debug locally |

### Common WA Causes & Fixes
| Issue | Fix |
|-------|-----|
| Wrong algorithm | Re-read problem, check sample manually |
| Edge cases | Test n=1, n=max, k=0, k=max |
| Modulo missing | Add `% MOD` at each arithmetic step |
| Off-by-one | Check 0-indexed vs 1-indexed |

### Common TLE Causes & Fixes
| Issue | Fix |
|-------|-----|
| O(N²) with N=10^5 | Find O(N) or O(N log N) algorithm |
| Redundant computation | Use prefix sums, memoization |
| Python slow I/O | Use `sys.stdin.read()` |

---

"""

# Insert new section before "## Tổng quan"
if "## ⚡ CRITICAL WORKFLOW" not in content:
    content = content.replace("## Tổng quan", new_section + "## Tổng quan")

# Update version
content = content.replace('version: 2.1', 'version: 3.0')
content = content.replace('updated-on: 2026-03-12', f'updated-on: {datetime.now().strftime("%Y-%m-%d")}')

# Write back
skill_path.write_text(content, encoding='utf-8')

print("✅ Updated codemath-solver skill")
print("📏 Added: CRITICAL WORKFLOW section")
print("📏 Added: defuddle.md usage guidelines")
print("📏 Added: Iteration loop with max 3 attempts")
print("📏 Added: Delegation rules to cp-solver")
print("📏 Version: 2.1 → 3.0")
