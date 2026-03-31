# Escalation to CP-Solver

## Khi Nào Cần Escalate?

| Dấu hiệu | Nguyên nhân | Action |
|----------|-------------|--------|
| **TLE 2+ lần** | Algorithm chưa tối ưu | → `task: cp-solver` |
| **WA không rõ** | Logic sai khó debug | → `task: cp-solver` |
| **Algorithm khó** | Segment Tree, Mo's, HLD, Flow | → `task: cp-solver` |
| **User hỏi sâu** | "Tại sao TLE?", "Có cách nào tối ưu?" | → `task: cp-solver` |

## Algorithm Complexity Reference

### Khi nào cần escalate:

**Data Structures nâng cao:**
- Segment Tree / Fenwick Tree
- Square Root Decomposition / Mo's Algorithm
- Heavy-Light Decomposition (HLD)
- Link-Cut Tree

**Graph Algorithms:**
- LCA (Lowest Common Ancestor)
- Max Flow / Min Cut
- Strongly Connected Components
- 2-SAT

**String Algorithms:**
- Suffix Array / Suffix Tree
- Aho-Corasick
- KMP, Z-algorithm (nếu chưa quen)

**Dynamic Programming:**
- Digit DP
- DP Optimization (Convex Hull, Divide & Conquer)
- Bitmask DP với N > 20

**Math:**
- Game Theory (Nim, Sprague-Grundy)
- Number Theory nâng cao
- Computational Geometry

## Cách Delegate

```bash
task: "cp-solver"
prompt: "Giải bài https://laptrinh.codemath.vn/problem/SLUG với phân tích chi tiết.
         Lưu ý: Đã thử optimize 2 lần nhưng vẫn TLE. Code hiện tại: [paste code]"
```

## Example Thực Tế

```
User: Giải bài hsgquangnam2021chiasokẹo

Agent (codemath-solver):
1. Test local: ✅ Sample đúng
2. Submit lần 1: ❌ TLE (2/10) - O(N*Q)
3. Optimize lần 1: ❌ TLE (5/10) - O(N log N)
4. Optimize lần 2: ❌ TLE (8/10) - Fenwick Tree

→ ESCALATE:
"Bài này cần Mo's Algorithm hoặc offline processing.
Đang delegate sang cp-solver để phân tích chi tiết..."

[Call task: cp-solver]
```

## Sau Khi Escalate

1. **Theo dõi progress** của cp-solver
2. **Học hỏi** từ phân tích algorithm
3. **Update knowledge** cho lần sau gặp bài tương tự

---

*Reference: escalation.md | Version: 2.0*
