# 🏗 Architecture Documentation

Tài liệu chi tiết về kiến trúc hệ thống của bộ skill tự động hóa giải bài tập CMOJ.

---

## 📐 Tổng Quan Kiến Trúc

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER LAYER                                      │
│  Natural Language Requests:                                              │
│  "Giải bài <slug>" / "Tối ưu code" / "Tạo bài giảng"                   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      SKILL ROUTER LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Intent Classification                                            │  │
│  │                                                                   │  │
│  │  • Mention "codemath", "CMOJ", "giải bài"                        │  │
│  │    → codemath-solver                                              │  │
│  │                                                                   │  │
│  │  • Mention "phân tích", "tối ưu", "tại sao TLE"                  │  │
│  │    → cp-solver                                                    │  │
│  │                                                                   │  │
│  │  • Mention "bài giảng", "lesson", "giảng chi tiết"               │  │
│  │    → cp-teacher                                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  CODEMATH      │  │   CP-SOLVER    │  │  CP-TEACHER    │
│  SOLVER        │  │                │  │                │
│                │  │  PHÂN TÍCH     │  │  BÀI GIẢNG     │
│ TỰ ĐỘNG GIẢI   │  │  & TỐI ƯU      │  │  CHI TIẾT      │
│                │  │                │  │                │
│ • 4 Flows      │  │ • Decision     │  │ • 5 Modules    │
│ • Auto submit  │  │   Tree         │  │ • 500+ dòng    │
│ • Contest      │  │ • Debug        │  │ • Manual walk  │
│ • Retrieve     │  │ • Stress test  │  │ • Line-by-line │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     SHARED TOOLING LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │    AGENT     │  │   DEFUDDLE   │  │   COMPILER   │                 │
│  │   BROWSER    │  │     .MD      │  │   LAYER      │                 │
│  │              │  │              │  │              │                 │
│  │ • Open URL   │  │ • curl       │  │ • python3    │                 │
│  │ • Snapshot   │  │   defuddle.md│  │ • g++        │                 │
│  │ • Fill form  │  │ /URL         │  │ • node       │                 │
│  │ • Click      │  │              │  │              │                 │
│  │ • Navigate   │  │              │  │              │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CMOJ PLATFORM LAYER                                 │
│  https://laptrinh.codemath.vn                                           │
│                                                                         │
│  • Problem Pages (DOM structure, CSS selectors)                        │
│  • Submission API (POST /submit/)                                       │
│  • Contest Pages (Problem lists)                                        │
│  • User Profiles (Submissions history)                                  │
│  • Login/Authentication (Session cookies)                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Chi Tiết

### Flow A: Giải Bài Cụ Thể

```
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: USER REQUEST                                            │
│  "Giải bài hsgthaibinh2425sodacbiet bằng Python"                │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 2: SKILL SELECTION                                         │
│  Router → codemath-solver                                        │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 3: LOGIN CMOJ                                              │
│  agent-browser:                                                  │
│  1. open /accounts/login/                                        │
│  2. fill username/password                                       │
│  3. click login button                                           │
│  4. snapshot → Verify logged in                                  │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 4: FETCH PROBLEM STATEMENT                                 │
│  agent-browser: open /problem/<slug>/                            │
│  defuddle: curl defuddle.md/.../problem/<slug>/                  │
│                                                                  │
│  Extract:                                                        │
│  • Problem description                                           │
│  • Input/Output format                                           │
│  • Constraints (N ≤ ?)                                           │
│  • Sample test cases                                             │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 5: ANALYZE & GENERATE CODE                                 │
│  Analysis:                                                       │
│  • Constraints → Required complexity                             │
│    - N ≤ 10^5 → O(N) or O(N log N)                               │
│    - N ≤ 1000 → O(N²) acceptable                                 │
│                                                                  │
│  Code Generation:                                                │
│  • Select algorithm pattern                                      │
│  • Generate Python/C++ code                                      │
│  • Add Fast I/O if N large                                       │
│  • Handle edge cases                                             │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 6: TEST LOCALLY                                            │
│  bash: python3 solution.py < sample.in                           │
│  Compare output with sample.out                                  │
│                                                                  │
│  If PASS → Continue                                              │
│  If FAIL → Debug & Fix                                           │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 7: SUBMIT                                                  │
│  agent-browser:                                                  │
│  1. open /problem/<slug>/submit/                                 │
│  2. fill source code                                             │
│  3. select language (Python 3 / C++17 / C++20)                   │
│  4. click submit                                                 │
│  5. wait for verdict                                             │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 8: CHECK VERDICT                                           │
│  defuddle: curl defuddle.md/.../submissions/<user>/              │
│                                                                  │
│  Verdicts:                                                       │
│  • AC (Accepted) ✅ → Done!                                      │
│  • WA (Wrong Answer) → Go to STEP 5                              │
│  • TLE (Time Limit) → Go to STEP 5 (optimize)                    │
│  • RE (Runtime Error) → Go to STEP 5 (fix bugs)                  │
│  • CE (Compilation Error) → Go to STEP 5 (fix syntax)            │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 9: REPORT RESULT                                           │
│  ✅ AC! Time: 0.05s, Memory: 2.3 MB                              │
│  hoặc                                                            │
│  ❌ TLE test #5 → Escalate to cp-solver                          │
└──────────────────────────────────────────────────────────────────┘
```

---

### Escalation Flow: Codemath Solver → CP Solver

```
┌──────────────────────────────────────────────────────────────────┐
│  TRIGGER: TLE 2+ lần dù optimize                                 │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  HANDOFF JSON                                                    │
│  {                                                               │
│    "problem_slug": "hsgthaibinh2425sodacbiet",                  │
│    "current_code": "...",                                        │
│    "verdict": "TLE",                                             │
│    "test_cases_failed": [5, 6, 7],                               │
│    "constraints": "N ≤ 10^5, Time: 1s",                          │
│    "current_complexity": "O(N²)"                                 │
│  }                                                               │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  CP-SOLVER ANALYSIS                                              │
│  1. Fetch problem via defuddle                                   │
│  2. Analyze current code                                         │
│  3. Identify bottleneck                                          │
│  4. Select optimization pattern:                                 │
│     - O(N²) → O(N log N): Sort + Binary Search                   │
│     - O(N²) → O(N): Prefix sums, Two pointers                    │
│     - Exponential → DP: Memoization                              │
│  5. Generate optimized code                                      │
│  6. Return to codemath-solver                                    │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  RESUME FLOW A                                                   │
│  codemath-solver submit optimized code → AC!                     │
└──────────────────────────────────────────────────────────────────┘
```

---

### CP Teacher Flow: Tạo Bài Giảng

```
┌──────────────────────────────────────────────────────────────────┐
│  INPUT: URL + AC Code                                            │
│  "Biến bài này thành bài giảng"                                 │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  MODULE 1: Problem Analysis                                      │
│  • Fetch problem via defuddle                                    │
│  • Extract constraints                                           │
│  • Identify problem type                                         │
│  • Output: 50-100 dòng                                           │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  MODULE 2: Solution Breakdown ⭐                                 │
│  2.1 Manual Walkthrough:                                         │
│      • Select test case                                          │
│      • Solve by hand (ASCII art)                                 │
│      • Extract pattern                                           │
│                                                                  │
│  2.2 Code Explanation:                                           │
│      • Map code with manual walkthrough                          │
│      • Line-by-line comments                                     │
│                                                                  │
│  2.3 Why AC?:                                                    │
│      • Complexity analysis                                       │
│      • Correctness proof                                         │
│      • Edge cases                                                │
│                                                                  │
│  Output: 200-400 dòng                                            │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  MODULE 3: Key Takeaways                                         │
│  • Recognition patterns                                          │
│  • Template code                                                 │
│  • Common mistakes (❌ SAI / ✅ ĐÚNG)                            │
│  • Tips & Tricks                                                 │
│  Output: 100-150 dòng                                            │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  DECISION: Theory Extension?                                     │
│  IF classic problem type → Generate Module 4                     │
│  ELSE → Skip                                                     │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  MODULE 5: Practice Problems                                     │
│  • Search CMOJ/Codeforces for similar problems                   │
│  • Categorize by difficulty (⭐⭐⭐)                              │
│  • Add hints & solutions                                         │
│  Output: 100-150 dòng                                            │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  EXPORT                                                        │
│  • Save as Markdown (.md)                                      │
│  • Export PDF via Pandoc                                       │
│  • Export Word/HTML/LaTeX (optional)                           │
│  • Location: ~/Desktop/cp-teacher-lessons/                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🗂 Component Details

### 1. Agent Browser

**Chức năng:**
- Tự động hóa thao tác browser (mở trang, click, fill form, snapshot)
- Tương tác với giao diện CMOJ

**Commands chính:**
```bash
agent-browser open <URL>
agent-browser snapshot -i
agent-browser fill @element "text"
agent-browser click @button
agent-browser wait --load networkidle
```

**Use cases:**
- Login CMOJ
- Navigate problem pages
- Submit solutions
- Parse submissions history

---

### 2. Defuddle.md

**Chức năng:**
- Đọc nội dung web, loại bỏ clutter (ads, navigation)
- Lấy content sạch để phân tích

**Usage:**
```bash
curl https://defuddle.md/<URL>
```

**Use cases:**
- Fetch problem statements
- Read submission results
- Parse contest pages

---

### 3. Compiler Layer

**Python3:**
```bash
python3 solution.py < input.in
```

**G++ (C++):**
```bash
g++ -std=c++17 -O2 solution.cpp -o solution
./solution < input.in
```

**Use cases:**
- Test solutions locally
- Stress testing
- Compile verification

---

## 📊 Performance Metrics

### Flow A: Giải Bài

| Step | Time (avg) | Success Rate |
|------|------------|--------------|
| Login | 5s | 99% |
| Fetch Problem | 3s | 98% |
| Generate Code | 10s | 95% |
| Test Local | 2s | 100% |
| Submit | 5s | 99% |
| Check Verdict | 3s | 98% |
| **Total** | **28s** | **~90% AC first try** |

---

### CP Teacher: Bài Giảng

| Module | Lines | Time to Generate |
|--------|-------|------------------|
| Module 1 | 50-100 | 30s |
| Module 2 | 200-400 | 60s |
| Module 3 | 100-150 | 30s |
| Module 4 (opt) | 100-200 | 40s |
| Module 5 | 100-150 | 30s |
| **Total** | **550-1000** | **~3-4 minutes** |

---

## 🔐 Security Considerations

### Authentication

```yaml
Credentials:
  - Store in environment variables
  - Never commit to git
  - Use .env file (gitignored)
  
Session:
  - Cookies stored in browser profile
  - Auto-expire after 24h
  - Re-login on expiry
```

### Code Execution

```yaml
Local Testing:
  - Run in sandboxed environment
  - No network access for solutions
  - Timeout after 5s (prevent infinite loops)
  
Submission:
  - User approval required
  - Max 3 retries per problem
  - Log all submissions
```

---

## 🛠 Error Handling

### Common Errors & Recovery

| Error | Cause | Recovery |
|-------|-------|----------|
| Login failed | Wrong credentials | Prompt user to re-enter |
| Element not found | DOM changed | Update CSS selectors |
| TLE | Wrong complexity | Escalate to cp-solver |
| WA | Logic error | Debug with edge cases |
| RE | Bounds/division | Check array sizes |

---

## 📈 Scalability

### Horizontal Scaling

```
Multiple Agents:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Agent 1    │  │  Agent 2    │  │  Agent 3    │
│  (Solve)    │  │  (Analyze)  │  │  (Teach)    │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
                        ▼
              Load Balancer
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   CMOJ Pool 1    CMOJ Pool 2    CMOJ Pool 3
```

### Rate Limiting

```yaml
CMOJ API:
  - Max 10 submissions/minute
  - Max 100 requests/hour
  - Delay 1s between requests
  
Defuddle:
  - Max 60 requests/minute
  - Cache responses (5min TTL)
```

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-01 | Initial architecture |
| 2.0 | 2026-03-11 | Add cp-solver escalation |
| 3.0 | 2026-03-12 | Add cp-teacher flow |
| 3.1 | 2026-03-30 | Document detailed flows |

---

**Last Updated:** 2026-03-30  
**Maintained By:** TechTus Team
