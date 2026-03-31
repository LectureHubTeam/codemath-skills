# Example Lesson: Sắp xếp chiếu

## Bài giảng mẫu cho CP Teacher

---

# Bài giảng: Sắp xếp chiếu - Đếm số đợt

> **URL:** https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
> 
> **Độ khó:** ⭐ (Cơ bản)
> 
> **Category:** Array Processing / Counting

---

## 1. Phân tích bài toán

### Đề bài
Có N phiếu với số hiệu 1..N (hoán vị). Mỗi đợt đi từ đầu đến cuối dãy, chọn các phiếu liên tiếp theo thứ tự 1, 2, 3, ... Hỏi cần ít nhất bao nhiêu đợt để chọn đủ các phiếu?

### Input/Output
- **Input:** 
  - Dòng 1: N (1 < N ≤ 10^7)
  - Dòng 2: N số nguyên là hoán vị của 1..N
- **Output:** Số đợt tối thiểu
- **Constraints:** N ≤ 10^7, thời gian 1s

### Nhận diện dạng
- **Keywords:** "số đợt", "ít nhất" → **Counting / Greedy**
- **Độ khó:** ⭐ (Cơ bản)
- **Category:** Array processing

### Tại sao chọn approach này?
- Simulate từng đợt: O(N²) → TLE
- Đếm violations: O(N) → AC

---

## 2. Solution Breakdown

### 2.1. Mô phỏng thủ công (KHÔNG DÙNG CODE)

**Test case:** N=5, dãy = [3, 1, 4, 2, 5]

**Bước 1: Phân tích yêu cầu**
- Cần chọn đủ các phiếu 1, 2, 3, 4, 5 theo thứ tự
- Mỗi đợt: đi từ trái sang phải, chọn phiếu tiếp theo nếu gặp
- Hỏi: cần bao nhiêu đợt?

**Bước 2: Làm thử trên giấy**

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

Đợt 2:
- Bắt đầu lại từ vị trí 0
- Cần phiếu 3 → gặp ở vị trí 0 ✓ (đang ở vị trí 0)
- Cần phiếu 4 → gặp ở vị trí 2 ✓ (đang ở vị trí 2)
- Cần phiếu 5 → gặp ở vị trí 4 ✓ (đang ở vị trí 4)
→ Kết thúc đợt 2, đã chọn: 3, 4, 5

Tổng: 2 đợt ✅
```

**Bước 3: Rút ra pattern**

```
Nhận xét quan trọng:
- Đợt 1: pos[1]=1, pos[2]=3 → pos[2] > pos[1] → CÙNG ĐỢT ✓
- Đợt 1→2: pos[2]=3, pos[3]=0 → pos[3] < pos[2] → ĐỢT MỚI!
- Đợt 2: pos[3]=0, pos[4]=2 → pos[4] > pos[3] → CÙNG ĐỢT ✓
- Đợt 2: pos[4]=2, pos[5]=4 → pos[5] > pos[4] → CÙNG ĐỢT ✓

Pattern: pos[i] < pos[i-1] → cần đợt mới
```

**Generalization:**
- Số đợt = 1 + số lần `pos[i] < pos[i-1]` với i từ 2 đến N
- Vì sao? Mỗi lần vi phạm monotonicity → cần đợt mới

### 2.2. Giải thích code (mapping với manual walkthrough)

```python
import sys

def solve():
    # Đọc input nhanh
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    
    # Mapping với Bước 2: Build position array
    # pos[x] = vị trí của phiếu x trong dãy
    # Test case: pos[1]=1, pos[2]=3, pos[3]=0, pos[4]=2, pos[5]=4
    pos = [0] * (n + 1)
    for i in range(n):
        pos[int(data[i + 1])] = i
    
    # Mapping với Bước 3: Count rounds
    # Pattern từ manual walkthrough:
    # pos[i] < pos[i-1] → đợt mới
    
    # Duyệt i từ 2 đến N:
    # i=2: pos[2]=3 >= pos[1]=1 → OK (cùng đợt)
    # i=3: pos[3]=0 <  pos[2]=3 → Đợt mới! (rounds=2)
    # i=4: pos[4]=2 >= pos[3]=0 → OK (cùng đợt)
    # i=5: pos[5]=4 >= pos[4]=2 → OK (cùng đợt)
    
    rounds = 1  # Ít nhất 1 đợt
    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            rounds += 1
    
    print(rounds)

solve()
```

### 2.3. Tại sao solution này AC?

✅ **Complexity:** $O(N)$ — đúng với constraints ($N \leq 10^7$)

✅ **Edge cases:** 
- $N=1$: rounds=1 (đúng)
- Dãy đã sorted: rounds=1 (đúng)
- Dãy reverse sorted: rounds=$N$ (đúng)

✅ **Correctness:**
- Lemma: $\text{Số đợt} = 1 + \sum_{i=2}^{N} \mathbf{1}[pos[i] < pos[i-1]]$
- Proof: 
  - Mỗi lần $pos[i] < pos[i-1]$ → $i$ và $i-1$ không cùng đợt
  - Ngược lại, nếu $pos[i] \geq pos[i-1]$ → cùng đợt
  - Vậy số đợt = 1 + số lần vi phạm

✅ **Memory:** $O(N)$ cho position array — OK với 1GB

---

## 3. Bài học tổng quát

### Kinh nghiệm nhận diện
🎯 **Khi thấy "số đợt", "số lần":**
- Đếm số lần vi phạm điều kiện
- Tìm pattern đơn giản thay vì simulate

### Pattern cần nhớ
📌 **Counting violations:**
```python
count = 0
for i in range(...):
    if not satisfies_condition(i):
        count += 1
```

📌 **Position array:**
```python
pos = [0] * (n + 1)
for i in range(n):
    pos[value[i]] = i  # pos[x] = vị trí của x
```

### Sai lầm thường gặp
❌ Simulate từng đợt → $O(N^2)$ TLE
❌ Quên case $N=1$
❌ Dùng `input()` thay vì `sys.stdin.buffer.read()`
❌ Không build position array mà tìm kiếm tuyến tính

### Tips
💡 Dùng position array để $O(1)$ lookup
💡 Đọc input nhanh với `sys.stdin.buffer.read()`
💡 Luôn nghĩ đến counting thay vì simulate

---

## 4. Lý thuyết mở rộng

> ⚠️ **Bài này không có chuyên đề mở rộng** — Pattern "counting violations" quá đơn giản và cụ thể cho bài này.
>
> 📌 **Luyện tập thêm:** Xem Module 5 bên dưới.

---

## 5. Bài tập tương tự

### Dễ ⭐
**Bài 1:** Đếm số lần giảm dần trong dãy
- **URL:** [Tìm trên CMOJ]
- **Gợi ý:** Đếm số lần a[i] < a[i-1]
- **Độ khó:** ⭐
- **Lời giải:**
<details>
<summary>Click để xem</summary>

```python
count = 0
for i in range(1, n):
    if a[i] < a[i-1]:
        count += 1
print(count)
```
</details>

### Trung bình ⭐⭐
**Bài 2:** Đếm số đoạn liên tiếp tăng dần
- **URL:** [Tìm trên CMOJ]
- **Gợi ý:** Dùng sliding window, đếm số đoạn
- **Độ khó:** ⭐⭐
- **Lời giải:**
<details>
<summary>Click để xem</summary>

```python
count = 0
length = 1
for i in range(1, n):
    if a[i] > a[i-1]:
        length += 1
    else:
        count += length * (length + 1) // 2
        length = 1
count += length * (length + 1) // 2
print(count)
```
</details>

### Khó ⭐⭐⭐
**Bài 3:** Đếm số đợt với nhiều điều kiện
- **URL:** [Tìm trên CMOJ]
- **Gợi ý:** Kết hợp nhiều patterns, đếm violations với nhiều điều kiện
- **Độ khó:** ⭐⭐⭐
- **Lời giải:**
<details>
<summary>Click để xem</summary>

```python
# Kết hợp position array và counting
pos = [0] * (n + 1)
for i in range(n):
    pos[a[i]] = i

rounds = 1
for i in range(2, n + 1):
    if pos[i] < pos[i-1] or condition2(i) or condition3(i):
        rounds += 1
print(rounds)
```
</details>

---

## Tổng kết

| Aspect | Takeaway |
|--------|----------|
| **Pattern** | Counting violations |
| **Technique** | Position array |
| **Complexity** | O(N) time, O(N) space |
| **Key insight** | pos[i] < pos[i-1] → new round |

---

**Học xong bài này, bạn có thể:**
- ✅ Nhận diện bài counting violations
- ✅ Dùng position array để O(1) lookup
- ✅ Đọc input nhanh với sys.stdin.buffer.read()
- ✅ Giải các bài tương tự
