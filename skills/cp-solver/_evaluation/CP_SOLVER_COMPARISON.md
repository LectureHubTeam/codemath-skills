# 📊 CP-Solver vs Codemath-Solver: Comparative Analysis

**Date:** 2026-03-12  
**Skills Reviewed:** cp-solver, codemath-solver

---

## 🎯 Skill Comparison

| Aspect | codemath-solver | cp-solver |
|--------|-----------------|-----------|
| **Purpose** | Auto-solve & submit on CMOJ | Deep algorithm analysis & optimization |
| **Target** | Routine problem solving | Hard problems needing expertise |
| **Flow** | 4 flows (A,B,C,D) | 6-phase deep analysis |
| **SKILL.md** | 192 lines (v2.1) | 228 lines (v1.0) |
| **References** | 12 files | 13 files |
| **Test Cases** | 5 evals | 6 evals (planned) |
| **Pass Rate** | 80% (4/5) | TBD |

---

## 🔄 Integration Points

### Delegation Flow: codemath-solver → cp-solver

```
codemath-solver (Flow A)
    ↓
TLE/WA after 2+ optimizations
    ↓
task: cp-solver (JSON handoff)
    ↓
cp-solver analyzes & solves
    ↓
Reports back to codemath-solver
```

### Handoff Format

```json
{
  "task": "cp-solver",
  "problem_url": "https://...",
  "current_code": "...",
  "verdict": "TLE",
  "attempts": 2,
  "constraints": "N ≤ 10^5",
  "reason": "O(N*Q) too slow"
}
```

---

## 📈 Refactoring Progress

### codemath-solver ✅ COMPLETE

| Step | Status | Notes |
|------|--------|-------|
| Refactor SKILL.md | ✅ v2.1 | 192 lines, metadata added |
| Create evals | ✅ 5 evals | All flows covered |
| Run evals | ✅ Complete | All graded |
| Aggregate | ✅ Complete | 80% pass rate |
| Improve skill | ✅ Complete | Flow C fixed |

### cp-solver 🟡 IN PROGRESS

| Step | Status | Notes |
|------|--------|-------|
| Refactor SKILL.md | ✅ v1.0 | 228 lines, metadata added |
| Create evals | ✅ 6 evals | Comprehensive coverage |
| Run evals | ⏳ Pending | Ready to run |
| Aggregate | ⏳ Pending | Awaiting results |
| Improve skill | ⏳ Pending | Awaiting analysis |

---

## 🎯 Key Differences

### codemath-solver
- **Focus:** Automation & efficiency
- **Success metric:** Problems solved per minute
- **Complexity:** Routine problems
- **User:** Students practicing

### cp-solver
- **Focus:** Deep analysis & optimization
- **Success metric:** Hard problems solved correctly
- **Complexity:** Advanced algorithms
- **User:** Competitive programmers

---

## 📊 Eval Coverage Comparison

### codemath-solver (5 evals)
1. ✅ solve-specific-problem (Flow A)
2. ✅ find-unsolved-problems (Flow B)
3. ✅ retrieve-ac-code (Flow D)
4. ⚠️ solve-contest (Flow C) - 80%
5. ✅ find-easiest-unsolved (Flow B)

### cp-solver (6 evals - Planned)
1. ⏳ solve-with-analysis (Full flow)
2. ⏳ algorithm-selection (Decision tree)
3. ⏳ debug-tle (Optimization)
4. ⏳ stress-testing (Test generation)
5. ⏳ delegate-from-codemath (Integration)
6. ⏳ advanced-algorithm (Advanced patterns)

---

## 🔍 Skill Quality Metrics

| Metric | codemath-solver | cp-solver (target) |
|--------|-----------------|-------------------|
| **SKILL.md lines** | 192 | <200 |
| **Metadata** | ✅ Full | ✅ Full |
| **Trigger clarity** | Good | Excellent |
| **Test coverage** | 5 evals | 6 evals |
| **Pass rate** | 80% | >85% |
| **Integration tested** | ⚠️ Partial | ✅ Full |

---

## 🚀 Next Steps

### codemath-solver ✅
- [ ] Optional: Re-run eval #4 to verify 100%
- [ ] Monitor production usage
- [ ] Collect user feedback

### cp-solver 🟡
- [ ] Copy evals to skill folder
- [ ] Run 6 evals
- [ ] Grade results
- [ ] Aggregate benchmark
- [ ] Improve based on failures
- [ ] Test integration with codemath-solver

---

## 📞 Quick Commands

```bash
# Setup cp-solver evals
cp cp-solver-evals.json ~/.qwen/skills/cp-solver/evals/evals.json

# Run cp-solver evals
/skill cp-solver
# Prompt: "Giải và phân tích bài https://..."

# After grading, aggregate
python3 aggregate-benchmark.py
```

---

## 📈 Timeline

```
codemath-solver:
  Day 1: Refactor ✅
  Day 2: Run evals ✅
  Day 3: Grade & improve ✅
  Status: COMPLETE (80% pass rate)

cp-solver:
  Day 1: Refactor ✅
  Day 2: Run evals ⏳
  Day 3: Grade & improve ⏳
  Status: IN PROGRESS
```

---

**Recommendation:** Complete cp-solver evaluation using same framework as codemath-solver for consistency.

---

*Generated: 2026-03-12*  
*Skills: codemath-solver v2.1, cp-solver v1.0*
