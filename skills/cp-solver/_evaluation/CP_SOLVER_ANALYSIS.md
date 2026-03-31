# 🧪 CP-Solver Skill Evaluation Plan

**Skill:** cp-solver  
**Date:** 2026-03-12  
**Status:** Planning Phase

---

## 📊 Skill Overview

### Current State
- **SKILL.md:** 11.8KB (~300 lines)
- **References:** 10 files (01-06 + patterns)
- **Examples:** 4 examples
- **Templates:** Available
- **Workspace:** iteration-1 created

### Trigger Description
```
Skill chuyên biệt để tự động giải các bài toán Competitive Programming
Triggers: "giải bài cp", "solve competitive programming", "phân tích bài này",
          "optimize solution", "debug TLE/WA", "/cp-solve", "/cp-analyze"
```

---

## 🎯 Eval Coverage (6 evals)

| # | Eval Name | Flow | Assertions |
|---|-----------|------|------------|
| 1 | solve-with-analysis | Full solve | 8 |
| 2 | algorithm-selection | Decision tree | 5 |
| 3 | debug-tle | Optimization | 6 |
| 4 | stress-testing | Test generation | 5 |
| 5 | delegate-from-codemath | Delegation | 7 |
| 6 | advanced-algorithm | Advanced patterns | 6 |

**Total:** 37 assertions

---

## 📋 Eval Prompts

### Eval #1: solve-with-analysis
```
Giải và phân tích bài https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu trên CMOJ
```
**Expected:** Full flow với analysis, algorithm selection, code, test, submit

### Eval #2: algorithm-selection
```
Bài này N=10^5, Q=10^5, có range queries và point updates, dùng thuật toán gì? Giải thích trade-off.
```
**Expected:** Segment Tree/Fenwick Tree recommendation với comparison

### Eval #3: debug-tle
```
Code bị TLE test lớn với N=10^5, giúp optimize với. [Kèm code O(N*Q)]
```
**Expected:** Complexity analysis + optimization + refactor

### Eval #4: stress-testing
```
Generate test cases để stress test cho bài sorting với N ≤ 10^5
```
**Expected:** Brute force + optimized + generator + comparison

### Eval #5: delegate-from-codemath
```
task: cp-solver
problem_url: https://laptrinh.codemath.vn/problem/example
verdict: TLE
attempts: 2
constraints: N ≤ 10^5
reason: O(N^2) too slow
```
**Expected:** CP Solver Analysis format với optimized solution

### Eval #6: advanced-algorithm
```
Giải bài tree path queries với N=10^5, Q=10^5 trên cây. Cần tìm algorithm phù hợp.
```
**Expected:** LCA/HLD identification + implementation

---

## 🔍 Preliminary Analysis

### Strengths (Pre-Assessment)

✅ **Comprehensive coverage:**
- 6 main reference files (analysis → testing)
- 7 pattern references (number theory, DP, graph, etc.)
- Clear flow diagram
- Submit policy rõ ràng

✅ **Good trigger description:**
- Multiple trigger phrases
- Delegation from codemath-solver documented
- Complexity indicators table

✅ **Strong documentation:**
- Quality standards section
- Reference reading strategy
- Tips & best practices

### Potential Issues (Hypothesis)

⚠️ **SKILL.md length:** ~300 lines (target: <200)
- Could benefit from progressive disclosure
- Move detailed patterns to references

⚠️ **No metadata:**
- Missing version tracking
- No author/tags/dependencies

⚠️ **No evals:**
- No test cases to verify skill works
- No benchmark for improvements

⚠️ **Complex trigger:**
- Many trigger conditions might confuse model
- Could simplify decision tree

---

## 📈 Improvement Recommendations

### P0: Critical (Do First)

1. **Add metadata to frontmatter**
   ```yaml
   metadata:
     version: 1.0
     updated-on: 2026-03-12
     tags: [competitive-programming, algorithms, optimization]
     author: TechTus Team
     dependencies: [agent-browser, python3, g++]
     integrates-with: codemath-solver (delegation)
   ```

2. **Create evals.json**
   - 6 evals covering all flows
   - Run & grade each eval
   - Establish baseline metrics

3. **Shorten SKILL.md**
   - Move pattern tables to references/
   - Keep only essential flows in main file
   - Target: <200 lines

### P1: Important

4. **Improve trigger description**
   - Make it more "pushy" for CP-related queries
   - Simplify delegation detection
   - Add more keywords (algorithm, optimization, TLE)

5. **Add exit criteria**
   - Each flow should have clear completion checklist
   - When to stop vs escalate
   - Success metrics

6. **Enhance examples**
   - Add real examples with solutions
   - Show delegation flow from codemath-solver
   - Include failure & recovery examples

### P2: Nice to Have

7. **Create integration tests**
   - Test codemath-solver → cp-solver handoff
   - Verify JSON format parsing
   - Test retry logic

8. **Performance benchmarks**
   - Target solve times per difficulty
   - Token usage optimization
   - Success rate tracking

---

## 📁 Proposed Structure

```
cp-solver/
├── SKILL.md (refactored, <200 lines)
├── evals/
│   └── evals.json (6 test cases)
├── references/
│   ├── 01-problem-analysis.md
│   ├── 02-algorithm-selection.md
│   ├── 03-optimization-patterns.md
│   ├── 04-advanced-algorithms.md
│   ├── 05-debugging-strategies.md
│   ├── 06-test-generation.md
│   └── patterns/
│       ├── number-theory.md
│       ├── dp.md
│       ├── graph.md
│       ├── string.md
│       ├── data-structures.md
│       ├── math.md
│       └── geometry.md
├── templates/
├── examples/
└── workspace/
    └── iteration-1/
```

---

## 🚀 Next Steps

### Phase 1: Setup (Today)
- [ ] Create evals.json ✅
- [ ] Setup workspace ✅
- [ ] Read & analyze current skill ✅
- [ ] Create evaluation plan ✅

### Phase 2: Run Evals (Next)
- [ ] Run eval #1: solve-with-analysis
- [ ] Run eval #2: algorithm-selection
- [ ] Run eval #3: debug-tle
- [ ] Run eval #4: stress-testing
- [ ] Run eval #5: delegate-from-codemath
- [ ] Run eval #6: advanced-algorithm

### Phase 3: Grade & Analyze
- [ ] Grade all 6 evals
- [ ] Identify failure patterns
- [ ] Generate benchmark report
- [ ] Propose improvements

### Phase 4: Improve Skill
- [ ] Add metadata
- [ ] Refactor SKILL.md (lean)
- [ ] Improve trigger description
- [ ] Add exit criteria
- [ ] Update version to 2.0

---

## 📊 Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| **SKILL.md lines** | ~300 | <200 |
| **Metadata** | None | Full |
| **Test cases** | 0 | 6 |
| **Pass rate** | - | >85% |
| **Trigger clarity** | Good | Excellent |
| **Integration** | Documented | Tested |

---

## 📞 Quick Commands

```bash
# Copy evals to skill folder
cp /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/cp-solver-evals.json \
   ~/.qwen/skills/cp-solver/evals/evals.json

# Setup eval workspace
mkdir -p ~/.qwen/skills/cp-solver/workspace/iteration-1/eval-{1..6}-*/with_skill/outputs

# Run aggregation (after grading)
python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/aggregate-benchmark.py
```

---

*Generated: 2026-03-12*  
*Skill: cp-solver*  
*Phase: Planning*
