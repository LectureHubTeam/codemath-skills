# CP Solver - Competitive Programming Problem Solver

## 🎯 Overview

Bộ skill chuyên biệt để tự động giải các bài toán Competitive Programming trên CMOJ và các Online Judges khác.

## 📁 Structure

```
cp-solver/
├── SKILL.md                              # Main skill — flow, submit policy, ref strategy
├── README.md                             # This file
├── references/
│   ├── 01-problem-analysis.md            # Phân tích & nhận diện dạng bài
│   ├── 02-algorithm-selection.md         # Decision tree chọn thuật toán
│   ├── 03-optimization-patterns.md       # Pattern tối ưu hóa
│   ├── 04-advanced-algorithms.md         # Reference nhanh → link tới implementations/
│   ├── 05-debugging-strategies.md        # Debug WA/TLE/RE + Python-specific
│   ├── 06-test-generation.md             # Tự sinh test cases
│   ├── implementations/                  # Code files (C++ & Python)
│   │   ├── segment-tree/
│   │   │   ├── segment_tree.cpp/.py      # Point update, range query
│   │   │   └── segment_tree_lazy.cpp/.py # Range update, range query
│   │   ├── fenwick-tree/
│   │   │   └── fenwick_tree.cpp/.py      # Point update, prefix/range sum + 2D variant
│   │   ├── mo-algorithm/
│   │   │   └── mo_algorithm.cpp/.py      # Offline range queries
│   │   ├── digit-dp/
│   │   │   └── digit_dp.cpp/.py          # Đếm số thỏa điều kiện digit
│   │   ├── matrix-exp/
│   │   │   └── matrix_exp.cpp/.py        # Linear recurrence với N ≤ 10^18
│   │   ├── hld/
│   │   │   └── hld.cpp/.py               # Path queries trên cây
│   │   ├── centroid-decomp/
│   │   │   └── centroid.cpp              # Path counting trên cây
│   │   └── suffix-array/
│   │       └── suffix_array.cpp/.py      # String matching, LCS
│   └── patterns/
│       ├── number-theory.md
│       ├── dp.md
│       ├── graph.md
│       ├── string.md
│       ├── data-structures.md
│       ├── math.md
│       └── geometry.md
└── examples/
    ├── ex01-number-theory.md             # Tìm bộ số — Number Theory O(√N)
    └── ex02-tle-to-ac.md                # TLE → AC với Mo's Algorithm
```

## 🚀 Quick Start

### 1. Giải bài cụ thể

```
User: Giải bài https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
```

**Flow:**
1. → Đọc [references/01-problem-analysis.md](references/01-problem-analysis.md) để phân tích
2. → Qua [references/02-algorithm-selection.md](references/02-algorithm-selection.md) để chọn thuật toán
3. → Implement và test
4. → Submit

### 2. Tìm thuật toán cho bài

```
User: Bài này N=10^5, Q=10^5, có range queries, dùng thuật toán gì?
```

**Answer:**
1. → Check [references/02-algorithm-selection.md](references/02-algorithm-selection.md) - Decision Tree
2. → Range queries → Segment Tree / Fenwick Tree
3. → Xem [references/patterns/data-structures.md](references/patterns/data-structures.md) để lấy template

### 3. Debug TLE/WA

```
User: Code bị TLE test lớn, giúp optimize với
```

**Flow:**
1. → Qua [references/05-debugging-strategies.md](references/05-debugging-strategies.md) để debug
2. → Qua [references/03-optimization-patterns.md](references/03-optimization-patterns.md) để optimize
3. → Stress test với [references/06-test-generation.md](references/06-test-generation.md)

## 📚 Reference Guide

### Core References

| File | Nội dung | Khi nào dùng |
|------|----------|-------------|
| [01-problem-analysis.md](references/01-problem-analysis.md) | Phân tích đề, nhận diện dạng | Bước đầu tiên khi gặp bài mới |
| [02-algorithm-selection.md](references/02-algorithm-selection.md) | Decision tree chọn thuật toán | Sau khi phân tích, cần chọn algorithm |
| [03-optimization-patterns.md](references/03-optimization-patterns.md) | Pattern tối ưu hóa | Khi code bị TLE, cần optimize |
| [04-advanced-algorithms.md](references/04-advanced-algorithms.md) | Advanced algorithms | Khi cần algorithm nâng cao |
| [05-debugging-strategies.md](references/05-debugging-strategies.md) | Debug strategies | Khi bị WA/TLE/RE |
| [06-test-generation.md](references/06-test-generation.md) | Test generation | Để verify solution |

### Pattern References

| Pattern | File | Topics |
|---------|------|--------|
| Number Theory | [patterns/number-theory.md](references/patterns/number-theory.md) | Prime, GCD, Modular, Combinatorics |
| Dynamic Programming | [patterns/dp.md](references/patterns/dp.md) | LIS, Knapsack, Tree DP, Digit DP |
| Graph | [patterns/graph.md](references/patterns/graph.md) | BFS, DFS, Dijkstra, MST, LCA |
| String | [patterns/string.md](references/patterns/string.md) | KMP, Z-algo, Suffix Array |
| Data Structures | [patterns/data-structures.md](references/patterns/data-structures.md) | Segment Tree, Fenwick, DSU |
| Math | [patterns/math.md](references/patterns/math.md) | Combinatorics, Game Theory, Probability |
| Geometry | [patterns/geometry.md](references/patterns/geometry.md) | Convex Hull, Polygon, Circle |

## 🎓 Learning Path

### Beginner (0-1000 rating)

1. Start with [01-problem-analysis.md](references/01-problem-analysis.md)
2. Learn basic algorithms from [02-algorithm-selection.md](references/02-algorithm-selection.md)
3. Practice patterns:
   - [patterns/number-theory.md](references/patterns/number-theory.md) - Basic number theory
   - [patterns/dp.md](references/patterns/dp.md) - Basic DP (LIS, Knapsack)
   - [patterns/graph.md](references/patterns/graph.md) - BFS, DFS

### Intermediate (1000-1800 rating)

1. Master [03-optimization-patterns.md](references/03-optimization-patterns.md)
2. Learn advanced data structures from [patterns/data-structures.md](references/patterns/data-structures.md)
3. Study advanced algorithms from [04-advanced-algorithms.md](references/04-advanced-algorithms.md)
4. Practice more patterns:
   - [patterns/string.md](references/patterns/string.md) - String algorithms
   - [patterns/math.md](references/patterns/math.md) - Combinatorics, Game Theory

### Advanced (1800+ rating)

1. Master all advanced algorithms from [04-advanced-algorithms.md](references/04-advanced-algorithms.md)
2. Learn geometry from [patterns/geometry.md](references/patterns/geometry.md)
3. Use [06-test-generation.md](references/06-test-generation.md) for stress testing
4. Master debugging with [05-debugging-strategies.md](references/05-debugging-strategies.md)

## 🔧 Usage Examples

### Example 1: Basic Problem Solving

```markdown
## Problem: Tìm bộ số (24thtbckhn1)

### Analysis (01-problem-analysis.md)
- Constraints: |N| ≤ 10^12 → Cần O(√N) hoặc O(log N)
- Keywords: "ước", "bội", "số nguyên tố" → Number Theory
- Input: N (có thể âm)
- Output: |a-b| nhỏ nhất với a×b=N

### Algorithm Selection (02-algorithm-selection.md)
- Number Theory → Tìm ước
- Approach: Duyệt ước từ √N xuống

### Implementation
[Code]

### Testing (06-test-generation.md)
[Test với edge cases: N=0, N=1, N âm]

### Result: AC 10/10
```

### Example 2: Optimization

```markdown
## Problem: Chia kẹo (24thtbckhn2)

### Initial Solution
- O(N*Q) → TLE

### Optimization (03-optimization-patterns.md)
- Pattern: O(N*Q) → O(N√N)
- Approach: Mo's Algorithm / Offline processing

### Result: Improved from 2/10 to 8/10
```

## 📝 Contributing

### Adding New Patterns

1. Create new file in `references/patterns/`
2. Follow template:
   - Description
   - When to use
   - Template code
   - Examples
   - Practice problems

### Adding Examples

1. Create new file in `examples/solved-problems/`
2. Include:
   - Problem statement
   - Analysis
   - Solution
   - Testing process

## 🏆 Solved Problems Log

| Problem | Contest | Result | Techniques Used |
|---------|---------|--------|----------------|
| Tìm bộ số | 24thtbckhn | ✅ 10/10 AC | Number Theory, O(√N) divisor |
| Sắp xếp chiếu | hsgnamdinh | ✅ 20/20 AC | Array scanning O(N) |

> Thêm bài mới vào đây sau mỗi lần giải thành công (chỉ ghi bài AC hoàn toàn).

## 📞 Support

- For bugs/issues: Create issue in repository
- For questions: Check references first, then ask
- For contributions: Submit PR

## 📄 License

This skill is part of the CodeMath Solver project.

---

**Happy Coding! 🚀**
