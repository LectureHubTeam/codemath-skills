# Guide: Tạo Manual Walkthrough

Manual Walkthrough là phần **QUAN TRỌNG NHẤT** trong Solution Breakdown. Đây là phần giúp người học hiểu cách suy nghĩ THỦ CÔNG trước khi code.

---

## 🎯 Mục đích của Manual Walkthrough

1. **Không dùng code** - Giải hoàn toàn bằng tay
2. **Thể hiện quá trình suy nghĩ** - Từng bước ra quyết định
3. **Rút ra pattern** - Từ ví dụ cụ thể → pattern tổng quát
4. **Làm nền cho code explanation** - Code sẽ map lại phần này

---

## 📋 Cấu trúc Manual Walkthrough

### Bước 1: Phân tích yêu cầu

```markdown
**Bước 1: Phân tích yêu cầu**
- Cần tìm ...
- Dữ liệu đầu vào ...
- Ràng buộc ...
- Output mong muốn ...
```

**Tips:**
- Viết ngắn gọn, không copy đề
- Nhấn mạnh vào yêu cầu chính
- Liệt kê rõ input/output

---

### Bước 2: Làm thử trên giấy

```markdown
**Bước 2: Làm thử trên giấy**

**Test case:** N=5, dãy = [3, 1, 4, 2, 5]

[Thể hiện từng bước bằng text/ASCII art]
```

**Yêu cầu BẮT BUỘC:**
1. ✅ Chọn test case cụ thể (sample hoặc tự tạo)
2. ✅ Thể hiện TỪNG BƯỚC, không nhảy cóc
3. ✅ Dùng ASCII art hoặc formatting để dễ đọc
4. ✅ Giải thích tại sao làm bước đó
5. ✅ Chỉ ra điểm quan trọng (dùng ✓, ✗, →)

**Ví dụ tốt:**
```
Dãy: [3, 1, 4, 2, 5]
     ^  ^  ^  ^  ^
     0  1  2  3  4  (vị trí)

Đợt 1:
- Bắt đầu từ vị trí 0
- Cần phiếu 1 → gặp ở vị trí 1 ✓ (đang ở vị trí 1)
- Cần phiếu 2 → gặp ở vị trí 3 ✓ (đang ở vị trí 3)
- Cần phiếu 3 → vị trí 0 ✗ (ĐÃ QUA MẤT RỒI!)
→ Kết thúc đợt 1, đã chọn: 1, 2
```

**Ví dụ KHÔNG tốt:**
```
Làm từ trái sang phải, chọn được 1,2 rồi qua đợt 2 chọn 3,4,5.
→ 2 đợt
```
❌ Quá nhanh, không thể hiện suy nghĩ
❌ Không có ASCII art
❌ Không giải thích tại sao

---

### Bước 3: Rút ra pattern

```markdown
**Bước 3: Rút ra pattern**

**Nhận xét:**
- ...

**Pattern:**
- ...

**Generalization:**
- ...
```

**Yêu cầu:**
1. ✅ Phát biểu thành quy tắc tổng quát
2. ✅ Có thể viết dưới dạng công thức/code giả
3. ✅ Link ngược lại với Bước 2

**Ví dụ:**
```
Nhận xét quan trọng:
- pos[1]=1, pos[2]=3 → pos[2] > pos[1] → CÙNG ĐỢT ✓
- pos[2]=3, pos[3]=0 → pos[3] < pos[2] → ĐỢT MỚI!

Pattern: pos[i] < pos[i-1] → cần đợt mới

Generalization:
Số đợt = 1 + số lần pos[i] < pos[i-1] với i từ 2 đến N
```

---

## 💡 Tips viết Manual Walkthrough hay

### 1. Dùng formatting hợp lý

```markdown
✅ GOOD:
- Dùng ✓ cho thành công
- Dùng ✗ cho thất bại
- Dùng → cho kết quả
- Dùng **bold** cho quan trọng

❌ BAD:
- Toàn text thường
- Không có highlights
```

### 2. ASCII art rõ ràng

```
✅ GOOD:
Dãy: [3, 1, 4, 2, 5]
     ^  ^  ^  ^  ^
     0  1  2  3  4

❌ BAD:
[3,1,4,2,5] ở các vị trí 0,1,2,3,4
```

### 3. Giải thích "TẠI SAO"

```markdown
✅ GOOD:
- Cần phiếu 3 → vị trí 0 ✗ (ĐÃ QUA MẤT RỒI!)
  → Vì đang ở vị trí 3, không quay lại được

❌ BAD:
- Cần phiếu 3 → qua rồi → đợt mới
```

### 4. Chọn test case phù hợp

| Loại test | Khi nào dùng | Ví dụ |
|-----------|-------------|-------|
| Sample từ đề | Luôn luôn đầu tiên | Sample của đề |
| Edge case | Để thể hiện edge | N=1, N=max |
| Custom case | Để illustrate pattern | Case có nhiều bước |

---

## 🔍 Checklist Manual Walkthrough

Trước khi xong, check:

- [ ] Có test case cụ thể
- [ ] Thể hiện TỪNG BƯỚC
- [ ] Dùng ASCII art / formatting
- [ ] Giải thích "tại sao" cho mỗi bước
- [ ] Rút ra pattern tổng quát
- [ ] Pattern có thể map sang code

---

## 📊 Example: Good vs Bad

### Bad Example

```
**Test case:** N=5, [3,1,4,2,5]

Làm từ trái qua phải:
- Đợt 1: chọn 1,2
- Đợt 2: chọn 3,4,5
→ 2 đợt
```

❌ Quá ngắn
❌ Không thể hiện suy nghĩ
❌ Không có ASCII art
❌ Không giải thích tại sao

### Good Example

```
**Test case:** N=5, dãy = [3, 1, 4, 2, 5]

**Bước 1: Phân tích yêu cầu**
- Cần chọn đủ 1,2,3,4,5 theo thứ tự
- Mỗi đợt: đi từ trái sang phải

**Bước 2: Làm thử trên giấy**
```
Dãy: [3, 1, 4, 2, 5]
     ^  ^  ^  ^  ^
     0  1  2  3  4

Đợt 1:
- Từ vị trí 0, cần 1 → gặp ở vị trí 1 ✓
- Từ vị trí 1, cần 2 → gặp ở vị trí 3 ✓
- Từ vị trí 3, cần 3 → ở vị trí 0 ✗ (QUA RỒI!)
→ Đợt 1: 1, 2

Đợt 2:
- Từ vị trí 0, cần 3 → gặp ở vị trí 0 ✓
- Từ vị trí 0, cần 4 → gặp ở vị trí 2 ✓
- Từ vị trí 2, cần 5 → gặp ở vị trí 4 ✓
→ Đợt 2: 3, 4, 5
```

**Bước 3: Rút ra pattern**
- Đợt mới khi: phiếu tiếp theo nằm TRƯỚC vị trí hiện tại
- Pattern: `pos[i] < pos[i-1]` → cần đợt mới
```

✅ Chi tiết, dễ follow
✅ Có ASCII art
✅ Giải thích tại sao
✅ Rút ra pattern

---

**Remember:** Manual Walkthrough hay = 50% thành công của lesson! 🎯
