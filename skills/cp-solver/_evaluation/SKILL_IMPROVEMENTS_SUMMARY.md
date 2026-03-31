# 🔄 Skill Improvements - Lessons Learned

**Date:** 2026-03-12  
**Skills Updated:** codemath-solver v3.0, cp-solver v3.0

---

## 📊 Problem Encountered

### Task
Solve: https://laptrinh.codemath.vn/problem/daknong2223virus

### Journey

| Attempt | Verdict | Score | Issue |
|---------|---------|-------|-------|
| V1-3 (codemath) | IR | 0/15 | Wrong problem type (BFS instead of simulation) |
| V4 (codemath) | WA | 0/15 | Still wrong approach |
| CP-V1 | TLE | 2/15 | O(k²) too slow |
| CP-V2 | WA | 0/15 | Wrong recurrence |
| **CP-V3** | **AC** ✅ | **15/15** | **Correct O(k) solution** |

---

## 🔍 Root Causes Identified

### 1. ❌ Did Not Read Problem Statement
**Issue:** Assumed problem type without reading
**Fix:** **Mandatory** problem statement fetch before coding

### 2. ❌ Used Browser Snapshot for Verdict
**Issue:** Browser automation doesn't render dynamic content
**Fix:** Use `curl defuddle.md/<url>` for verdict

### 3. ❌ No Clear Iteration Loop
**Issue:** No max attempts, no clear stop condition
**Fix:** Max 3 attempts → delegate to cp-solver

### 4. ❌ Delegated Too Late
**Issue:** Spent too long fixing without progress
**Fix:** Rule: 3 IR/WA/TLE/RE → immediate delegation

### 5. ❌ web_fetch Instead of curl
**Issue:** web_fetch tool less reliable
**Fix:** Use `curl defuddle.md/<url>` format

---

## ✅ Skill Improvements

### Codemath-Solver v3.0

**New Sections Added:**

1. **CRITICAL WORKFLOW**
   - Step 0: Fetch problem statement (MANDATORY)
   - Step 6: Check verdict with curl (MANDATORY)
   - Step 7: Iteration loop (max 3 attempts)
   - Step 8: Delegation to cp-solver

2. **Technical Guidelines**
   - defuddle.md usage with curl
   - Input/Output best practices
   - Common IR/WA/TLE causes & fixes

3. **Verdict Interpretation Table**
   - Clear action for each verdict type

### CP-Solver v3.0

**New Sections Added:**

1. **CRITICAL WORKFLOW**
   - Step 0: Fetch problem statement
   - Step 6: Check verdict with curl
   - Step 7: Optimization strategy
   - Step 8: Return solution format

2. **Optimization Strategy**
   - For TLE: Complexity analysis
   - For WA: Debug checklist

3. **Technical Guidelines**
   - Complexity analysis template
   - Common optimizations table

---

## 📋 New Flow (codemath-solver v3.0)

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 0: FETCH PROBLEM (MANDATORY)                         │
│  curl defuddle.md/laptrinh.codemath.vn/problem/<slug>      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1-5: Standard Flow                                    │
│  - Login, Navigate, Generate, Test, Submit                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: CHECK VERDICT (MANDATORY)                          │
│  curl defuddle.md/.../submissions/<username>               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   Verdict = AC?      │
          └──────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │ NO                    │ YES
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ Attempt < 3?    │     │ ✅ DONE         │
└────────┬────────┘     │ Report score    │
         │              └─────────────────┘
    ┌────┴────┐
    │ YES     │ NO
    ▼         ▼
┌─────────┐ ┌─────────────────────┐
│ Fix &   │ │ DELEGATE TO         │
│ Resubmit│ │ CP-SOLVER           │
└─────────┘ └─────────────────────┘
```

---

## 🛠 Key Technical Changes

### Before ❌
```bash
# Browser automation for everything
npx agent-browser snapshot -i  # Doesn't show verdict

# web_fetch (less reliable)
web_fetch(url, prompt)
```

### After ✅
```bash
# curl for text content (RELIABLE)
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>
curl https://defuddle.md/laptrinh.codemath.vn/problem/<slug>/submissions/<username>

# Browser only for interaction (submit, click)
npx agent-browser click e18  # Submit button
```

---

## 📊 Impact

| Metric | Before | After |
|--------|--------|-------|
| **Problem Understanding** | Assume | Read first |
| **Verdict Check** | Browser snapshot | curl defuddle.md |
| **Iteration Limit** | None | Max 3 |
| **Delegation** | Too late | After 3 attempts |
| **Tool Usage** | web_fetch | curl |

---

## 🎯 Success Criteria

**Codemath-Solver v3.0 is successful when:**
- ✅ Always fetches problem statement first
- ✅ Uses curl for verdict checking
- ✅ Delegates after 3 failed attempts
- ✅ Clear iteration loop with max attempts

**CP-Solver v3.0 is successful when:**
- ✅ Fetches problem before analysis
- ✅ Provides complexity analysis
- ✅ Returns optimized solution
- ✅ Clear handoff format to codemath-solver

---

## 📞 Quick Reference

### Fetch Problem
```bash
curl https://defuddle.md/laptrinh.codemath.vn/problem/daknong2223virus
```

### Check Verdict
```bash
curl https://defuddle.md/laptrinh.codemath.vn/problem/daknong2223virus/submissions/hnkhangdev
```

### Delegate to CP-Solver
```json
{
  "task": "cp-solver",
  "problem_url": "https://...",
  "current_code": "...",
  "verdict": "TLE",
  "attempts": 3,
  "constraints": "N ≤ 10^5",
  "reason": "O(N²) too slow"
}
```

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| **codemath-solver v3.0** | 2026-03-12 | Added CRITICAL WORKFLOW, curl usage, iteration loop |
| **cp-solver v3.0** | 2026-03-12 | Added CRITICAL WORKFLOW, optimization strategy |
| codemath-solver v2.1 | 2026-03-12 | Fixed Flow C contest loop |
| cp-solver v2.0 | 2026-03-12 | Clear scope separation |
| codemath-solver v2.0 | 2026-03-11 | Refactored with metadata |

---

*Generated: 2026-03-12*  
*Skills: codemath-solver v3.0, cp-solver v3.0*
