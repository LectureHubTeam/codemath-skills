# Guide: Quyết định Theory Extension (OPTIONAL)

Phần 4 - Theory Extension là **OPTIONAL**. Agent tự quyết định có sinh hay không dựa trên các tiêu chí dưới đây.

---

## ✅ SINH Theory Extension KHI...

### 1. Bài thuộc dạng kinh điển

**Dấu hiệu:**
- Có tên algorithm cụ thể (Dijkstra, KMP, Segment Tree)
- Được dạy trong các khóa học CP
- Có trong CP-Algorithms, Competitive Programming 3

**Ví dụ:**
- ✅ Bài DFS/BFS → Sinh lý thuyết Graph Traversal
- ✅ Bài LIS → Sinh lý thuyết DP cơ bản
- ✅ Bài KMP → Sinh lý thuyết String Matching

### 2. Có nhiều bài tương tự cùng chuyên đề

**Dấu hiệu:**
- Trên CMOJ/Codeforces có tag chung
- Có thể liệt kê 3+ bài cùng dạng
- Pattern áp dụng được cho nhiều bài

**Ví dụ:**
- ✅ DP với state dp[i] = ... → Có nhiều bài DP 1 chiều
- ✅ Segment Tree range sum → Có nhiều bài range queries

### 3. Có pattern tổng quát hóa được

**Dấu hiệu:**
- Từ bài cụ thể rút ra được template
- Template áp dụng được cho lớp bài
- Có thể viết thành function tổng quát

**Ví dụ:**
- ✅ `count = 0; for i in ...: if condition: count++` → Pattern counting
- ✅ `dp[i] = max(dp[i-1], dp[i-2] + val)` → Pattern DP 1 chiều

---

## ❌ BỎ QUA Theory Extension KHI...

### 1. Bài quá đơn giản

**Dấu hiệu:**
- Chỉ cần 1-2 dòng code
- Không có algorithm đáng nói
- Chỉ là bài tập cơ bản

**Ví dụ:**
- ❌ Tính tổng 2 số → Không cần lý thuyết
- ❌ Tìm max của mảng → Không cần lý thuyết

### 2. Pattern quá cụ thể cho bài này

**Dấu hiệu:**
- Chỉ áp dụng được cho bài này
- Không generalize được
- Không có bài tương tự

**Ví dụ:**
- ❌ Bài toán đố vui, logic puzzle
- ❌ Bài toán với constraints rất đặc biệt

### 3. Lý thuyết quá phức tạp so với level người học

**Dấu hiệu:**
- Bài level ⭐ nhưng algorithm level ⭐⭐⭐
- Người hỏi có vẻ mới học
- Solution đã AC là đủ

**Ví dụ:**
- ❌ Giải thích Flow Network cho bài toán đơn giản
- ❌ Dạy FFT cho bài polynomial multiplication cơ bản

---

## 📋 Decision Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│  Bắt đầu quyết định Theory Extension                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Bài có algorithm       │
         │ kinh điển không?       │
         └───────────┬────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
         YES                   NO
          │                     │
          │                     ▼
          │          ┌────────────────────────┐
          │          │ Pattern generalize     │
          │          │ được không?            │
          │          └───────────┬────────────┘
          │                      │
          │           ┌──────────┴──────────┐
          │           │                     │
          │          YES                   NO
          │           │                     │
          │           │                     ▼
          │           │          ┌────────────────────────┐
          │           │          │ SKIP Theory Extension  │
          │           │          │ (Chỉ làm 4 modules)    │
          │           │          └────────────────────────┘
          │           │
          ▼           ▼
         ┌────────────────────────┐
         │ Có 3+ bài tương tự     │
         │ trên OJ không?         │
         └───────────┬────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
         YES                   NO
          │                     │
          │                     ▼
          │          ┌────────────────────────┐
          │          │ SKIP Theory Extension  │
          │          └────────────────────────┘
          │
          ▼
         ┌────────────────────────┐
         │ GENERATE Theory        │
         │ Extension ✅           │
         └────────────────────────┘
```

---

## 📊 Examples

### Example 1: SINH Theory

**Problem:** Longest Increasing Subsequence (LIS)

**Decision:** ✅ SINH

**Lý do:**
- ✅ Algorithm kinh điển (có trong mọi sách CP)
- ✅ Có template tổng quát
- ✅ Nhiều bài tương tự (tag "lis" trên Codeforces)
- ✅ Level ⭐⭐ phù hợp với lý thuyết O(N log N)

**Theory content:**
```markdown
## 4. Chuyên đề: Longest Increasing Subsequence

### Lý thuyết
...

### Templates
- O(N²) DP
- O(N log N) Binary Search

### Đọc thêm
...
```

---

### Example 2: SKIP Theory

**Problem:** Tính tổng các phần tử trong mảng

**Decision:** ❌ SKIP

**Lý do:**
- ❌ Quá đơn giản
- ❌ Không có algorithm
- ❌ Không generalize được

**Action:** Chỉ làm 4 modules (bỏ module 4)

---

### Example 3: SINH Theory

**Problem:** Đếm số đường đi ngắn nhất (Dijkstra variant)

**Decision:** ✅ SINH

**Lý do:**
- ✅ Dijkstra là algorithm kinh điển
- ✅ Có thể generalize thành "Shortest Path on Graph"
- ✅ Nhiều bài tương tự (tag "shortest-path", "dijkstra")

**Theory content:**
```markdown
## 4. Chuyên đề: Shortest Path trên Graph

### Các algorithms
- BFS (unweighted)
- Dijkstra (non-negative weights)
- Bellman-Ford (có weight âm)

### Khi nào dùng cái nào?
...
```

---

## 💡 Tips ra quyết định

### Ask yourself:

1. **"Học xong bài này, học sinh có thể giải được bài nào khác?"**
   - Nếu có 3+ bài → SINH
   - Nếu chỉ giải được bài này → SKIP

2. **"Có trang web nào viết về algorithm này không?"**
   - Nếu có (CP-Algorithms, GeeksForGeeks) → SINH
   - Nếu không → SKIP

3. **"Liệu explanation này có áp dụng được cho bài khác không?"**
   - Nếu có → SINH
   - Nếu chỉ cho bài này → SKIP

---

## 📝 Template khi SKIP

Khi SKIP Theory Extension, chỉ cần ghi chú ngắn:

```markdown
## 4. Lý thuyết mở rộng

⚠️ **Bài này không có chuyên đề mở rộng** vì:
- Solution đã là optimal
- Pattern quá cụ thể cho bài này

📌 **Xem các bài tương tự ở Module 5 để luyện tập thêm.**
```

---

## 💡 Heuristic nhanh

> **"Nếu người học đặt câu hỏi: 'Bài này cần biết lý thuyết gì?' → CÓ lý do SINH."**

| Tín hiệu | Khả năng SINH |
|----------|--------------|
| Tên algorithm xuất hiện trong statement (\"BFS\", \"DP\", \"Segment Tree\") | Cao |
| Có thể search trên CP-Algorithms và tìm thấy trang riêng | Cao |
| Bài có tag trên Codeforces với 50+ bài cùng tag | Cao |
| Solution dùng 1 trick ad-hoc không tổng quát hóa được | Thấp |
| Bài chỉ 5-10 dòng code, không có algorithm đặc biệt | Thấp |
| Level ⭐ hoặc ⭐⭐ với solution O(N) đơn giản | Thấp |

**Nguyên tắc quan trọng nhất:**
> **Thà SKIP còn hơn forced theory không hữu ích!** 🎯
>
> Theory Extension tốt = người học học được pattern áp dụng cho 3+ bài khác.
> Theory Extension xấu = copy-paste lý thuyết từ Wikipedia, không liên quan đến bài.
