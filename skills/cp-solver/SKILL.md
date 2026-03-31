---
name: cp-solver
description: Chuyên gia PHÂN TÍCH và TỐI ƯU algorithm cho Competitive Programming. Dùng skill này khi user cần: (1) Phân tích algorithm sâu, (2) Chọn algorithm tối ưu, (3) Debug TLE/WA/RE, (4) Stress testing, (5) Được delegate từ codemath-solver để optimize code. Trigger: 'phân tích bài cp', 'tìm algorithm', 'optimize solution', 'debug TLE', 'tại sao TLE', 'cải thiện complexity', '/cp-analyze', hoặc khi codemath-solver delegate task với verdict TLE/WA. ⚠️ CP-Solver KHÔNG submit code trực tiếp. Chỉ phân tích và đề xuất solution. Việc submit do codemath-solver thực hiện.
metadata:
  version: 3.0
  updated-on: /Users/macbook_118
  tags:
    - competitive-programming
    - algorithms
    - optimization
    - debugging
    - stress-testing
  author: TechTus Team
  dependencies:
    - agent-browser
    - python3
    - g++Cacsi
  integrates-with:
    - codemath-solver (delegation)
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(python3:*), Bash(g++:*), Bash(node:*)
---

# CP Solver - Competitive Programming Problem Solver


## ⚠️ Scope Clarification (QUAN TRỌNG)

**CP-Solver KHÔNG làm gì:**
- ❌ KHÔNG submit code trực tiếp lên OJ
- ❌ KHÔNG đọc đề từ URL (trừ khi được cung cấp trong delegation)
- ❌ KHÔNG retry submit nhiều lần
- ❌ KHÔNG tương tác với browser để submit

**CP-Solver làm gì:**
- ✅ Phân tích algorithm, complexity
- ✅ Đề xuất optimization patterns
- ✅ Debug TLE/WA/RE với reasoning
- ✅ Stress testing với test generation
- ✅ Return optimized code cho codemath-solver

**Integration với Codemath-Solver:**
```
codemath-solver (submit → TLE)
    ↓
Delegate sang cp-solver (JSON handoff)
    ↓
cp-solver (phân tích → optimize)
    ↓
Return code mới cho codemath-solver
    ↓
codemath-solver submit → Report verdict
```

**Khi user yêu cầu submit:**
→ Redirect về codemath-solver: "Để submit bài này, dùng codemath-solver skill"


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

## Tổng quan

CP Solver khác với codemath-solver ở chỗ:
- **Tập trung vào algorithm optimization** thay vì chỉ submit
- **Có decision tree** để chọn thuật toán tối ưu
- **Có debugging strategies** cho WA/TLE/RE
- **Có test generation** để stress testing
- **Cover advanced patterns**: Segment Tree, Mo's, Digit DP, etc.

## Flow chính

```
┌─────────────────────────────────────────────────────────────┐
│  CP SOLVER FLOW                                             │
├─────────────────────────────────────────────────────────────┤
│  1. Problem Analysis (Phân tích đề)                         │
│     ├─ Đọc constraints → Complexity cho phép                │
│     ├─ Identify keywords → Dạng bài                         │
│     └─ Edge cases check                                     │
│                                                             │
│  2. Algorithm Selection (Chọn thuật toán)                   │
│     ├─ Decision tree                                        │
│     ├─ Pattern matching                                     │
│     └─ Trade-off analysis                                   │
│                                                             │
│  3. Solution Design (Thiết kế giải pháp)                    │
│     ├─ Brute force (để verify)                              │
│     ├─ Optimized solution                                   │
│     └─ Complexity analysis                                  │
│                                                             │
│  4. Implementation (Code)                                   │
│     ├─ Templates                                            │
│     ├─ Fast I/O                                             │
│     └─ Edge case handling                                   │
│                                                             │
│  5. Testing & Debugging                                     │
│     ├─ Sample testing                                       │
│     ├─ Stress testing (vs brute force)                      │
│     ├─ Edge cases                                           │
│     └─ Debug WA/TLE/RE                                      │
│                                                             │
│  6. Submit & Retry                                          │
│     ├─ Submit                                               │
│     ├─ Analyze verdict                                      │
│     └─ Retry if needed (max 3 lần)                          │
└─────────────────────────────────────────────────────────────┘
```

## Tham số

- **problem_url**: URL bài toán (CMOJ, Codeforces, etc.)
- **problem_statement**: Nội dung đề (nếu không có URL)
- **constraints**: Giới hạn (N, time limit, memory limit)
- **language**: Ngôn ngữ (PY3, CPP17, CPP20) - default: PY3
- **difficulty**: Độ khó dự kiến (Easy, Medium, Hard)
- **auto_submit**: Tự động submit hay không (default: false)

## Deep-Dive References

| Reference | Nội dung |
|-----------|----------|
| [references/01-problem-analysis.md](references/01-problem-analysis.md) | Phân tích & nhận diện dạng bài |
| [references/02-algorithm-selection.md](references/02-algorithm-selection.md) | Decision tree chọn thuật toán |
| [references/03-optimization-patterns.md](references/03-optimization-patterns.md) | Pattern tối ưu hóa |
| [references/04-advanced-algorithms.md](references/04-advanced-algorithms.md) | Advanced algorithms |
| [references/05-debugging-strategies.md](references/05-debugging-strategies.md) | Debug WA/TLE/RE |
| [references/06-test-generation.md](references/06-test-generation.md) | Tự sinh test cases |

## Patterns by Topic

| Pattern | File |
|---------|------|
| Number Theory | [patterns/number-theory.md](references/patterns/number-theory.md) |
| Dynamic Programming | [patterns/dp.md](references/patterns/dp.md) |
| Graph Algorithms | [patterns/graph.md](references/patterns/graph.md) |
| String Algorithms | [patterns/string.md](references/patterns/string.md) |
| Data Structures | [patterns/data-structures.md](references/patterns/data-structures.md) |
| Math & Combinatorics | [patterns/math.md](references/patterns/math.md) |
| Geometry | [patterns/geometry.md](references/patterns/geometry.md) |

## Ví dụ sử dụng

### Ví dụ 1: Giải bài cụ thể với phân tích
```
User: Giải và phân tích bài https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
```

→ Agent sẽ:
1. Đọc đề, extract constraints
2. Phân tích dạng bài (Sequence/Array)
3. Chọn thuật toán (O(n) scanning)
4. Code + test sample
5. Stress test (nếu cần)
6. Submit

### Ví dụ 2: Tìm thuật toán cho bài
```
User: Bài này N=10^5, Q=10^5, có range queries và updates, dùng thuật toán gì?
```

→ Agent sẽ:
1. Identify: Range queries + updates → Segment Tree / Fenwick Tree
2. Giải thích trade-off
3. Cung cấp template

### Ví dụ 3: Debug TLE
```
User: Code bị TLE test lớn, N=10^5, giúp optimize với
```

→ Agent sẽ:
1. Xem code hiện tại
2. Phân tích complexity
3. Đề xuất optimization pattern
4. Refactor code

### Ví dụ 4: Stress testing
```
User: Generate test cases để stress test bài này
```

→ Agent sẽ:
1. Viết brute force solution
2. Viết optimized solution
3. Generate random tests
4. So sánh kết quả

## Tips & Best Practices

1. **LUÔN đọc constraints trước** → Quyết định complexity
2. **Viết brute force trước** → Để verify và stress test
3. **Test edge cases** → N=0, N=1, max values
4. **Dùng fast I/O** → Đặc biệt với Python/C++
5. **Profile trước khi optimize** → Tìm bottleneck
6. **Document assumptions** → Ghi chú các giả định khi giải

---

## Submit Policy

**KHÔNG được submit nếu chưa thỏa mãn tất cả điều kiện sau:**

1. ✅ **Pass sample tests**: Tất cả test cases từ đề phải đúng
2. ✅ **Pass edge cases**: N=0, N=1, max N, tất cả giống nhau, sorted
3. ✅ **Complexity hợp lệ**: Đã tính và xác nhận complexity phù hợp constraints
4. ✅ **Stress test** (nếu có brute force): Ít nhất 200 random tests không có WA
5. ✅ **Fast I/O** đã bật (nếu N ≥ 10^4)

**Retry policy:** Tối đa 3 lần submit. Sau 3 lần, báo cáo verdict và dừng — KHÔNG submit tiếp.

**Sau mỗi lần submit thất bại:**
- TLE → Tăng optimization level, xem xét đổi algorithm
- WA → Chạy thêm edge cases, so sánh với brute force
- RE → Check array bounds, division by zero, recursion depth
- MLE → Giảm memory footprint

---

## Reference Reading Strategy

**QUAN TRỌNG: Lazy-load references — chỉ đọc khi cần, KHÔNG đọc tất cả cùng lúc.**

| Khi nào | Đọc file nào |
|---------|-------------|
| Bắt đầu bài mới | [references/01-problem-analysis.md](references/01-problem-analysis.md) |
| Sau khi phân tích xong, cần chọn algorithm | [references/02-algorithm-selection.md](references/02-algorithm-selection.md) |
| Identify dạng Number Theory | [references/patterns/number-theory.md](references/patterns/number-theory.md) |
| Identify dạng DP | [references/patterns/dp.md](references/patterns/dp.md) |
| Identify dạng Graph/Tree | [references/patterns/graph.md](references/patterns/graph.md) |
| Identify dạng String | [references/patterns/string.md](references/patterns/string.md) |
| Identify dạng Data Structure (Seg Tree, Fenwick...) | [references/patterns/data-structures.md](references/patterns/data-structures.md) |
| Identify dạng Math/Combinatorics | [references/patterns/math.md](references/patterns/math.md) |
| Identify dạng Geometry | [references/patterns/geometry.md](references/patterns/geometry.md) |
| Code bị TLE và cần optimization patterns | [references/03-optimization-patterns.md](references/03-optimization-patterns.md) |
| Cần implement advanced algorithm (HLD, Centroid...) | [references/04-advanced-algorithms.md](references/04-advanced-algorithms.md) |
| Bị WA/TLE/RE cần debug | [references/05-debugging-strategies.md](references/05-debugging-strategies.md) |
| Cần viết stress test hoặc gen test cases | [references/06-test-generation.md](references/06-test-generation.md) |

---

## Quality Standards

- ✅ Code phải có comments giải thích logic chính
- ✅ Complexity analysis rõ ràng (ghi O(...) cụ thể)
- ✅ Test với sample trước khi submit
- ✅ Stress test với random cases khi có brute force
- ✅ Handle edge cases (N=0, N=1, overflow, negative)
- ✅ Fast I/O cho N lớn
- ✅ Python: `sys.setrecursionlimit(300000)` nếu dùng đệ quy sâu
- ✅ Python: `input = sys.stdin.readline` khi N ≥ 10^4

---

## Allowed Tools

- Bash: python3, g++, node
- Browser: agent-browser (để access OJ)
- File operations: read, write, edit
