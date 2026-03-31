# 🏗 CP-Solver & Codemath-Solver: Architecture Decision

**Date:** 2026-03-12  
**Decision:** Clear separation of concerns  
**Status:** ✅ Implemented

---

## 🎯 Problem Statement

### Trước ❌

**CP-Solver v1.0:**
- Có thể submit code trực tiếp
- Trigger bao gồm cả "giải bài cp"
- Không rõ ràng khi nào delegate, khi nào tự submit
- Risk: Infinite loop với codemath-solver

**Codemath-Solver:**
- Delegate sang cp-solver khi TLE
- Nhưng cp-solver có thể submit ngược lại
- → Loop: codemath → cp-solver → submit → TLE → codemath → ...

---

## ✅ Solution: Clear Separation

### Codemath-Solver v2.1+ (Automation Layer)

**Responsibilities:**
- ✅ Read problem from OJ (browser interaction)
- ✅ Generate brute force solution
- ✅ Submit code & get verdict
- ✅ Retry logic (max 3 times)
- ✅ Escalate to cp-solver when TLE/WA after 2+ attempts
- ✅ Submit optimized code from cp-solver
- ✅ Report final verdict to user

**NOT doing:**
- ❌ Deep algorithm analysis
- ❌ Advanced optimization patterns
- ❌ Complex debugging (delegate to cp-solver)

---

### CP-Solver v2.0+ (Analysis Layer)

**Responsibilities:**
- ✅ Deep algorithm analysis
- ✅ Complexity optimization
- ✅ Debug TLE/WA with reasoning
- ✅ Stress testing & test generation
- ✅ Return optimized code (NOT submit)

**NOT doing:**
- ❌ Submit code directly
- ❌ Read problem from URL (unless delegated)
- ❌ Retry logic
- ❌ Browser interaction for submission

---

## 🔄 Integration Flow

### Standard Flow

```
┌─────────────────────────────────────────────────────────────┐
│  User: "Giải bài https://..."                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  codemath-solver                                            │
│  1. Navigate to problem page                                │
│  2. Read problem statement & constraints                    │
│  3. Generate brute force solution                           │
│  4. Submit → Verdict: AC                                    │
│  5. Report to user ✅                                       │
└─────────────────────────────────────────────────────────────┘
```

### Optimization Flow (TLE/WA)

```
┌─────────────────────────────────────────────────────────────┐
│  codemath-solver                                            │
│  1. Submit brute force → Verdict: TLE                       │
│  2. Optimize once → Submit → TLE again                      │
│  3. Optimize twice → Submit → TLE again                     │
│  4. Decision: Need expert help                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Delegate to cp-solver (JSON handoff)                       │
│  {                                                          │
│    "task": "cp-solver",                                     │
│    "problem_url": "...",                                    │
│    "current_code": "...",                                   │
│    "verdict": "TLE",                                        │
│    "attempts": 2,                                           │
│    "constraints": "N ≤ 10^5",                               │
│    "reason": "O(N^2) too slow"                              │
│  }                                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  cp-solver                                                  │
│  1. Analyze constraints → Required complexity               │
│  2. Analyze current code → Why TLE                          │
│  3. Propose new algorithm (e.g., Segment Tree)              │
│  4. Implement optimized solution                            │
│  5. Stress test (200+ cases)                                │
│  6. Return code to codemath-solver (NOT submit)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  codemath-solver                                            │
│  1. Receive optimized code from cp-solver                   │
│  2. Submit code → Verdict: AC ✅                            │
│  3. Report to user with explanation                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Trigger Comparison

### Codemath-Solver Triggers

```
✅ "giải bài [URL]"
✅ "submit bài [URL]"
✅ "làm bài cp trên CMOJ"
✅ "solve problem [URL]"
✅ "/solve [URL]"
✅ "tìm bài chưa giải"
✅ "lấy code AC"
```

### CP-Solver Triggers

```
✅ "phân tích bài cp"
✅ "tìm algorithm cho bài này"
✅ "optimize solution"
✅ "debug TLE"
✅ "tại sao TLE?"
✅ "cải thiện complexity"
✅ "/cp-analyze"
✅ "code bị WA, giúp debug"
✅ (delegate từ codemath-solver)
```

### ❌ WRONG Triggers (should redirect)

```
User: "submit bài này giúp"
→ cp-solver: "Để submit, dùng codemath-solver skill"

User: "giải bài [URL] trên CMOJ"
→ cp-solver: "Để giải và submit bài trên CMOJ, dùng codemath-solver skill"
```

---

## 🚫 Anti-Patterns to Avoid

### ❌ CP-Solver Submit Directly

```
User → cp-solver → submit → TLE
                      ↓
              cp-solver optimize
                      ↓
              submit again → TLE
                      ↓
              ∞ loop (no exit criteria)
```

### ❌ Codemath-Solver Deep Analysis

```
User → codemath-solver → TLE
                    ↓
            Try to optimize deeply
                    ↓
            Spend 10 minutes analyzing
                    ↓
            Still TLE (wrong algorithm)
                    ↓
            User frustrated
```

### ✅ Correct Pattern

```
User → codemath-solver → TLE (2 attempts)
                    ↓
            Delegate to cp-solver
                    ↓
            cp-solver analyzes (expert)
                    ↓
            Return optimized code
                    ↓
            codemath-solver submits
                    ↓
            AC ✅ → User happy
```

---

## 📊 Decision Matrix

| Scenario | Codemath-Solver | CP-Solver |
|----------|-----------------|-----------|
| User: "Giải bài [URL]" | ✅ Handle | ❌ Redirect |
| User: "Submit code" | ✅ Handle | ❌ Redirect |
| User: "Tìm bài chưa giải" | ✅ Handle | ❌ Redirect |
| User: "Lấy code AC" | ✅ Handle | ❌ Redirect |
| TLE after 2 attempts | ✅ Delegate | ✅ Analyze |
| User: "Phân tích algorithm" | ❌ Redirect | ✅ Handle |
| User: "Tại sao TLE?" | ❌ Redirect | ✅ Handle |
| User: "Optimize code" | ❌ Redirect | ✅ Handle |
| User: "Stress test" | ❌ Redirect | ✅ Handle |

---

## 🔧 Implementation Changes

### CP-Solver v2.0 Changes

**Description updated:**
```
Chuyên gia PHÂN TÍCH và TỐI ƯU algorithm cho Competitive Programming.
⚠️ CP-Solver KHÔNG submit code trực tiếp.
```

**Added scope clarification:**
```markdown
## ⚠️ Scope Clarification

CP-Solver KHÔNG làm gì:
- ❌ KHÔNG submit code trực tiếp lên OJ
- ❌ KHÔNG đọc đề từ URL (trừ khi được delegate)
- ❌ KHÔNG retry submit nhiều lần

CP-Solver làm gì:
- ✅ Phân tích algorithm, complexity
- ✅ Đề xuất optimization patterns
- ✅ Debug TLE/WA/RE với reasoning
- ✅ Return optimized code cho codemath-solver
```

**Added handoff instruction:**
```markdown
**Response template:**
...
**Next Step:**
→ Return code cho codemath-solver để submit
→ KHÔNG submit trực tiếp
```

---

## ✅ Benefits

### Clear Responsibilities
- Codemath-solver: Automation & workflow
- CP-solver: Deep analysis & optimization

### No Loop Risk
- One-way delegation: codemath → cp-solver
- No reverse submission

### Better User Experience
- Each skill does one thing well
- Clear error messages & redirects
- Predictable behavior

### Easier Maintenance
- Separate codebases
- Independent testing
- Clear failure points

---

## 📞 Quick Reference

### When to use Codemath-Solver

```
✅ "Giải bài trên CMOJ"
✅ "Submit code giúp mình"
✅ "Tìm bài chưa giải"
✅ "Lấy lại code AC"
✅ "Giải contest"
```

### When to use CP-Solver

```
✅ "Phân tích algorithm cho bài này"
✅ "Tại sao code bị TLE?"
✅ "Optimize solution này với"
✅ "Tìm algorithm tốt hơn"
✅ "Debug WA với N=10^5"
```

### When CP-Solver should redirect

```
User: "Submit bài này"
→ "Để submit code, vui lòng dùng codemath-solver skill"

User: "Giải bài [URL] trên CMOJ"
→ "Để giải và submit bài trên CMOJ, vui lòng dùng codemath-solver skill"
```

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| **codemath-solver v2.1** | 2026-03-12 | Fixed Flow C contest loop |
| **cp-solver v2.0** | 2026-03-12 | Clear scope separation, no submit |
| **codemath-solver v2.0** | 2026-03-11 | Refactored with metadata |
| **cp-solver v1.0** | 2026-03-11 | Initial version |

---

**Decision Status: ✅ Implemented in cp-solver v2.0**

---

*Generated: 2026-03-12*  
*Skills: codemath-solver v2.1, cp-solver v2.0*
