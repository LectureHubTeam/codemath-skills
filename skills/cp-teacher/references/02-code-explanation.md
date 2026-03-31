# Guide: Code Explanation với Mapping

Sau khi có Manual Walkthrough, phần Code Explanation sẽ map code ngược lại với các bước đã làm thủ công.

---

## 🎯 Mục đích của Code Explanation

1. **Link code với manual walkthrough** - Người học thấy code implement ý tưởng từ đâu
2. **Giải thích TỪNG DÒNG/KHỐI** - Không bỏ qua chi tiết
3. **Nói "TẠI SAO" chứ không chỉ "CÁI GÌ"** - Giải thích lý do viết code như vậy

---

## 📋 Cấu trúc Code Explanation

### Template

```markdown
### 2.2. Giải thích code (mapping với manual walkthrough)

```python
# [Code đã AC]
```

**Mapping với phần mô phỏng:**

```python
# Comment giải thích
# Reference đến Bước X ở manual walkthrough
code_line_by_line()
```
```

---

## 💡 Cách viết Code Explanation hay

### 1. Group code thành khối logic

```python
# ❌ BAD: Giải thích từng dòng riêng lẻ
data = sys.stdin.read().split()  # Đọc data
n = int(data[0])  # Lấy n

# ✅ GOOD: Group thành khối
# Đọc input và parse
data = sys.stdin.read().split()
n = int(data[0])
```

### 2. Reference ngược lại Manual Walkthrough

```python
# ✅ GOOD:
# Mapping với Bước 2: Build position array
# Test case: pos[1]=1, pos[2]=3, pos[3]=0
pos = [0] * (n + 1)
for i in range(n):
    pos[int(data[i + 1])] = i

# Mapping với Bước 3: Count rounds
# Pattern: pos[i] < pos[i-1] → đợt mới
rounds = 1
for i in range(2, n + 1):
    if pos[i] < pos[i - 1]:
        rounds += 1
```

### 3. Giải thích "TẠI SAO"

```python
# ❌ BAD: Chỉ nói cái gì
rounds = 1  # Khởi tạo rounds

# ✅ GOOD: Giải thích tại sao
rounds = 1  # Ít nhất 1 đợt (trường hợp dãy đã sorted)
            # Nếu không có violations → giữ nguyên 1
```

### 4. Dùng comment multi-line cho khối phức tạp

```python
# ✅ GOOD:
# Duyệt i từ 2 đến N:
# - i=2: pos[2]=3 >= pos[1]=1 → OK (cùng đợt)
# - i=3: pos[3]=0 <  pos[2]=3 → Đợt mới! (rounds=2)
# - i=4: pos[4]=2 >= pos[3]=0 → OK (cùng đợt)
rounds = 1
for i in range(2, n + 1):
    if pos[i] < pos[i - 1]:
        rounds += 1
```

---

## 🔍 Checklist Code Explanation

Trước khi xong, check:

- [ ] Code được group thành khối logic
- [ ] Mỗi khối có comment giải thích mục đích
- [ ] Reference đến Manual Walkthrough
- [ ] Giải thích "tại sao" cho các decision
- [ ] Có ví dụ cụ thể trong comment (nếu cần)

---

## 📊 Example: Full Code Explanation

### Manual Walkthrough (reference)

```
Bước 2: Làm thử trên giấy
Dãy: [3, 1, 4, 2, 5]
pos[1]=1, pos[2]=3, pos[3]=0, pos[4]=2, pos[5]=4

Pattern: pos[i] < pos[i-1] → cần đợt mới
```

### Code Explanation

```python
import sys

def solve():
    # Đọc input nhanh (quan trọng với N ≤ 10^7)
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    
    # === MAPPING VỚI BƯỚC 2: BUILD POSITION ARRAY ===
    # pos[x] = vị trí của phiếu x trong dãy
    # Từ manual walkthrough:
    #   pos[1]=1, pos[2]=3, pos[3]=0, pos[4]=2, pos[5]=4
    pos = [0] * (n + 1)  # Index 0 không dùng
    for i in range(n):
        # data[i+1] vì data[0] là N
        pos[int(data[i + 1])] = i
    
    # === MAPPING VỚI BƯỚC 3: COUNT ROUNDS ===
    # Pattern từ manual walkthrough:
    #   pos[i] < pos[i-1] → cần đợt mới
    # 
    # Duyệt i từ 2 đến N:
    #   i=2: pos[2]=3 >= pos[1]=1 → OK (cùng đợt)
    #   i=3: pos[3]=0 <  pos[2]=3 → Đợt mới! (rounds=2)
    #   i=4: pos[4]=2 >= pos[3]=0 → OK (cùng đợt)
    #   i=5: pos[5]=4 >= pos[4]=2 → OK (cùng đợt)
    
    rounds = 1  # Ít nhất 1 đợt (trường hợp dãy sorted)
    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            rounds += 1  # Thêm đợt khi gặp violation
    
    print(rounds)

solve()
```

---

## 💡 Pro Tips

### 1. Dùng emoji để highlight

```python
✅ # Check điều kiện
❌ # Violation
⚠️ # Edge case
💡 # Optimization
```

### 2. Include test case trong comment

```python
# Test case: N=5
# pos = [0, 1, 3, 0, 2, 4]  # index 0 không dùng
# i=2: pos[2]=3 >= pos[1]=1 → OK
# i=3: pos[3]=0 <  pos[2]=3 → rounds=2
```

### 3. So sánh với cách khác

```python
# Cách này O(N) thay vì O(N²) như simulate
# Vì ta chỉ duyệt 1 vòng, không simulate từng đợt
```

---

**Remember:** Code Explanation hay giúp người học hiểu MỐI LIÊN HỆ giữa ý tưởng và code! 🔗

---

## 🔥 Khi code phức tạp (> 50 dòng)

### 1. Chia thành sections rõ ràng

```python
# ========================
# SECTION 1: INPUT PARSING
# ========================
# ... code đọc input

# ========================
# SECTION 2: PREPROCESSING
# ========================
# ... code tiền xử lý

# ========================
# SECTION 3: MAIN ALGORITHM
# ========================
# ... thuật toán chính

# ========================
# SECTION 4: OUTPUT
# ========================
# ... xuất kết quả
```

Giải thích **từng section** thay vì từng dòng.

### 2. Data Structure phức tạp — Giải thích usage, không cần giải thích implementation

```markdown
❌ BAD (quá chi tiết, người mới không cần biết):
"Segment Tree dùng `tree[2*node]` và `tree[2*node+1]`
để lưu con trái và con phải của node hiện tại..."

✅ GOOD (giải thích cách dùng):
"Chúng ta dùng Segment Tree để query max trong đoạn [l, r] — O(log N).
- `st.update(i, val)` → cập nhật giá trị tại vị trí i
- `st.query(l, r)` → lấy max trong [l, r]
Chi tiết Segment Tree → xem [04-advanced-algorithms.md]"
```

### 3. Nhiều helper functions — Giải thích theo luồng (flow), không theo function

```markdown
✅ Luồng chính trong bài:
1. `read_input()` → đọc đồ thị
2. `build_hld()` → phân rã heavy-light (preprocessing)
3. Mỗi query → `path_query(u, v)` gọi `segment_query()` O(log² N)

Quan trọng nhất: `path_query()` — đây là nơi HLD phát huy tác dụng.
```

### 4. Checklist cho code phức tạp

- [ ] Chia thành ít nhất 3-4 sections có tên rõ ràng
- [ ] Mỗi section có 1 câu mô tả mục đích
- [ ] Data structure phức tạp → giải thích interface (update/query), không giải thích internals
- [ ] Vẽ sơ đồ luồng nếu có nhiều functions gọi nhau
- [ ] Chú thích đặc biệt `# ⚠️ Lưu ý:` cho phần dễ nhầm
