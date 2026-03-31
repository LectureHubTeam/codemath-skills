# Lesson Template — CP Teacher

## Template đầy đủ cho bài giảng

> **Cách dùng:** Dùng file này làm khung xương khi tạo lesson mới.
> Điền thông tin vào các chỗ `[...]`, xóa comment sau khi điền xong.
> **LaTeX:** Dùng `$...$` cho inline math, `$$...$$` cho block math.

---

```markdown
# Bài giảng: [Tên bài]

> **URL:** [Problem URL]
>
> **Độ khó:** ⭐⭐
>
> **Category:** [DP / Graph / String / Array / ...]

---

## 1. Phân tích bài toán

### Đề bài
[Tóm tắt ngắn gọn - KHÔNG copy paste toàn bộ đề]

### Input/Output
- **Input:** ...
- **Output:** ...
- **Constraints:** $N \leq 10^5$, $Q \leq 10^5$

### Nhận diện dạng
- **Keywords:** "..." → **Dạng bài**
- **Độ khó:** ⭐⭐
- **Category:** ...

### Tại sao chọn approach này?
- Brute force: $O(N^2)$ → TLE
- Optimal: $O(N \log N)$ → AC

---

## 2. Solution Breakdown

### 2.1. Mô phỏng thủ công (KHÔNG DÙNG CODE)

**Test case:** [Input cụ thể — từ sample hoặc tự tạo]

**Bước 1: Phân tích yêu cầu**
- Cần tìm ...
- Dữ liệu đầu vào ...
- Ràng buộc ...

**Bước 2: Làm thử trên giấy**
```
[Thể hiện từng bước bằng text/ASCII art]
Dùng ✓, ✗, → để highlight
```

**Bước 3: Rút ra pattern**
- Nhận xét: ...
- Pattern: ...
- Generalization: ...

### 2.2. Giải thích code (mapping với manual walkthrough)

```python
# [Code đã AC]
```

**Mapping với phần mô phỏng:**
```python
# === MAPPING VỚI BƯỚC 2 ===
# [Mục đích của khối code này]
# Từ manual: [reference cụ thể]
code_block_1()

# === MAPPING VỚI BƯỚC 3 ===
# Pattern: [từ bước 3 walkthrough]
code_block_2()
```

### 2.3. Tại sao solution này AC?

✅ **Complexity:** $O(N \log N)$ — đúng với constraints
✅ **Edge cases:** Xử lý $N=1$, ...
✅ **Correctness:** [Proof sketch / Lemma ngắn]

---

## 3. Bài học tổng quát

### Kinh nghiệm nhận diện
🎯 **Khi thấy các dấu hiệu sau, nghĩ đến [Dạng bài]:**
- Dấu hiệu 1: ...
- Dấu hiệu 2: ...

### Pattern cần nhớ
📌 **[Tên pattern]:**
```python
# Template code
pattern_template()
```

### Sai lầm thường gặp
❌ Sai lầm 1: ... → gây $O(N^2)$ TLE
❌ Sai lầm 2: ...

### Tips
💡 **Mẹo:** ...

---

## 4. Lý thuyết mở rộng [OPTIONAL]

<!-- Chỉ điền nếu bài thuộc dạng kinh điển. Nếu không, dùng template skip bên dưới -->

### Trường hợp SINH Theory:

### Lý thuyết nền tảng: [Tên chuyên đề]

**Khi nào dùng:**
- ...

**Template:**
```python
# Code template tổng quát
```

**Tham khảo:**
- [CP-Algorithms: Topic](https://cp-algorithms.com/...)
- [Codeforces Blog: ...](https://codeforces.com/blog/...)

---

### Trường hợp SKIP Theory (xóa phần trên, dùng phần này):

> ⚠️ **Bài này không có chuyên đề mở rộng** — [Lý do ngắn gọn].
>
> 📌 **Luyện tập thêm:** Xem Module 5 bên dưới.

---

## 5. Bài tập tương tự

### Dễ ⭐
**Bài 1:** [Tên] — [URL thật, không placeholder]
- **Gợi ý:** Giống bài chính, chỉ khác ...
- **Lời giải:** <details><summary>Click để xem</summary>

```python
# solution
```

</details>

### Trung bình ⭐⭐
**Bài 2:** [Tên] — [URL thật]
- **Gợi ý:** Thêm constraint ...
- **Lời giải:** <details><summary>Click để xem</summary>

```python
# solution
```

</details>

### Khó ⭐⭐⭐
**Bài 3:** [Tên] — [URL thật]
- **Gợi ý:** Cần optimization ...
- **Lời giải:** <details><summary>Click để xem</summary>

```python
# solution
```

</details>
```

---

## ✅ Checklist trước khi output

- [ ] Module 2.1: Có test case, đủ 3 bước, có ASCII art
- [ ] Module 2.2: Có comment mapping rõ ràng với walkthrough
- [ ] Module 2.3: Có complexity ($O(...)$ dạng LaTeX) và edge cases
- [ ] Module 3: Có ít nhất 1 pattern code template
- [ ] Module 4: Đã điền **hoặc** đã ghi Skip note
- [ ] Module 5: Ít nhất 2 bài có URL thật
- [ ] Công thức toán dùng LaTeX (`$...$`, `$$...$$`)
- [ ] File đã lưu vào `outputs/{problem-id}-lesson.md`
