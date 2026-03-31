---
name: cp-teacher
description: "Biến bài toán CP đã AC thành bài giảng chi tiết (300+ dòng): phân tích, giải thích code dòng-by-dòng, chứng minh, edge cases, common mistakes. Triggers: 'biến thành bài giảng', 'tạo lesson', 'teach this problem', '/cp-teach'."
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(python3:*), Bash(g++:*)
---

# CP Teacher - Bài Giảng Competitive Programming

Skill chuyên biệt để biến một bài toán CP đã AC thành **bài giảng chi tiết** nhằm mục đích giảng dạy và học tập.

---

## ⚠️ CHẤT LƯỢNG BẮT BUỘC (Quality Requirements)

### Minimum Length
- **Tối thiểu:** 300 dòng
- **Lý tưởng:** 500-900+ dòng cho bài khó
- **Validation:** Kiểm tra trước khi export

### Required Sections (BẮT BUỘC)

```yaml
required_sections:
  - problem_statement_full: "Đề bài ĐẦY ĐỦ, không tóm tắt quá ngắn"
  - input_output_examples: "Input/Output với ví dụ cụ thể"
  - constraints_analysis: "Phân tích constraints → độ phức tạp yêu cầu"
  - manual_walkthrough: "Giải tay từng bước, KHÔNG DÙNG CODE"
  - algorithm_derivation: "Rút ra công thức/thuật toán"
  - code_ac: "Code AC (Python + C++)"
  - code_explanation_line_by_line: "Giải thích TỪNG DÒNG code"
  - why_ac_proof: "Chứng minh Bổ đề + Định lý"
  - complexity_analysis: "Time + Space complexity"
  - edge_cases: "5+ edge cases với giải thích"
  - common_mistakes: "❌ SAI / ✅ ĐÚNG với code examples"
  - practice_problems: "Test cases tự luyện + links"
```

### Quality Checklist

```yaml
quality_checks:
  - min_300_lines: true
  - has_line_by_line_explanation: true
  - has_mathematical_proof: true
  - has_5_plus_edge_cases: true
  - has_common_mistakes: true
  - has_practice_tests: true
```

---

## 🎯 Khi nào dùng CP Teacher

### Trigger trực tiếp
- "biến bài này thành bài giảng"
- "tạo lesson từ bài này"
- "teach this problem"
- "/cp-teach"
- "giảng chi tiết bài này cho em"

### Trigger từ solution AC
- User đã AC một bài và muốn hiểu sâu hơn
- User muốn có tài liệu học từ solution
- User muốn bài tập tương tự để luyện tập

---

## 🎯 Output Configuration

### Default Location
- **macOS:** `~/Desktop/cp-teacher-lessons/`
- **Linux:** `~/cp-teacher-lessons/`
- **Windows:** `C:\Users\<username>\Desktop\cp-teacher-lessons\`

### Custom Location
User có thể thay đổi output location:

```
User: Lưu bài giảng vào /path/to/custom/folder
User: Change output directory to ~/Documents/lessons
```

### Output Formats
- **Markdown (.md):** Default, easy to read/edit
- **Text (.txt):** Simple, printable
- **PDF (.pdf):** Professional, shareable (requires conversion)
- **Word (.docx):** Editable documents
- **HTML (.html):** Web-friendly
- **LaTeX (.tex):** For advanced typography

> **CƠ CHẾ TỰ ĐỘNG EXPORT (Pandoc)**
> Agent được trang bị script để tự động biến file `.md` thành các định dạng như PDF, Word, LaTeX.
> Lệnh sử dụng:
> ```bash
> python3 ~/.openclaw/skills/cp-teacher/scripts/export_lesson.py <đường_dẫn_file.md> --formats pdf docx latex
> ```
> Yêu cầu hệ thống: `pandoc` (và `xelatex`/`pdflatex` nếu xuất PDF).
> *(Lưu ý: Nếu command báo lỗi thiếu pandoc, báo cho user biết để cài đặt).*

### File Naming
- Format: `bai-giang-<problem-slug>.<ext>`
- Example: `bai-giang-dem-gia-tri.md`

---

## 📥 Input Handling

| Trường hợp | Action |
|-----------|--------|
| URL + code AC | ✅ Tạo lesson bình thường |
| Chỉ URL, không có code | Fetch problem statement; hỏi user: "Bạn có solution AC chưa? Paste vào đây!" |
| URL + code (chưa verify AC) | Hỏi: "Code này đã AC chưa?" trước khi tạo lesson |
| Chỉ code, không có URL | Tạo lesson, ghi rõ `URL: [chưa có]` trong output |
| Chỉ problem statement (paste text) | Tóm tắt lại, hỏi code AC |
| Không có gì | Yêu cầu: "Hãy cung cấp URL bài hoặc problem statement!" |

**Lưu ý:** Đừng tạo lesson từ code chưa AC — bài giảng dựa trên solution sai sẽ dạy sai cho người học.

---

## 📋 Output Structure

Bài giảng gồm **4-5 modules** (module 4 là optional):

```
┌─────────────────────────────────────────────────────────────┐
│  BÀI GIẢNG: [Tên bài]                                       │
├─────────────────────────────────────────────────────────────┤
│  1. Problem Analysis (Phân tích bài toán)                   │
│  2. Solution Breakdown (Giải pháp chi tiết) ⭐ TRỌNG TÂM   │
│     2.1. Manual Walkthrough (Mô phỏng thủ công)             │
│     2.2. Code Explanation (Giải thích code)                 │
│     2.3. Why AC? (Tại sao đúng?)                            │
│  3. Key Takeaways (Bài học tổng quát)                       │
│  4. Theory Extension (OPTIONAL - Chuyên đề mở rộng)         │
│  5. Practice Problems (Bài tập tương tự)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Chi tiết từng Module

### Module 1: Problem Analysis

**Mục đích:** Giúp người học hiểu đề và nhận diện dạng bài.

**Nội dung:**
```markdown
## 1. Phân tích bài toán

### Đề bài
[Tóm tắt ngắn gọn - KHÔNG copy paste toàn bộ đề]

### Input/Output
- **Input:** ...
- **Output:** ...
- **Constraints:** ...

### Nhận diện dạng
- **Keywords:** "..." → **Dạng bài**
- **Độ khó:** ⭐⭐ (Dựa trên constraints và algorithm)
- **Category:** DP / Graph / String / ...

### Tại sao chọn approach này?
- Brute force: O(...) → TLE
- Optimal: O(...) → AC
- Pattern: ...
```

---

### Module 2: Solution Breakdown ⭐ (QUAN TRỌNG NHẤT)

**Mục đích:** Giúp người học hiểu TỪNG BƯỚC suy nghĩ và implement.

#### 2.1. Manual Walkthrough (Mô phỏng thủ công)

**YÊU CẦU BẮT BUỘC:**
- Chọn 1-2 test cases (sample hoặc tự tạo)
- Giải THỦ CÔNG trên giấy, KHÔNG DÙNG CODE
- Thể hiện từng bước suy nghĩ
- Rút ra pattern từ manual walkthrough

**Template:**
```markdown
### 2.1. Mô phỏng thủ công (KHÔNG DÙNG CODE)

**Test case:** [Input cụ thể]

**Bước 1: Phân tích yêu cầu**
- Cần tìm ...
- Dữ liệu đầu vào ...
- Ràng buộc ...

**Bước 2: Làm thử trên giấy**
```
[Thể hiện từng bước bằng text/ASCII art]
Ví dụ:
Dãy: [3, 1, 4, 2, 5]
     ^  ^  ^  ^  ^
     0  1  2  3  4  (vị trí)

Đợt 1:
- Cần phiếu 1 → ở vị trí 1 ✓
- Cần phiếu 2 → ở vị trí 3 ✓
- Cần phiếu 3 → ở vị trí 0 ✗ (QUA MẤT!)
→ Đợt 1 chọn được: 1, 2
```

**Bước 3: Rút ra pattern**
- Nhận xét: ...
- Pattern: `pos[i] < pos[i-1]` → cần đợt mới
- Generalization: ...
```

#### 2.2. Code Explanation (Giải thích code)

**YÊU CẦU:**
- Mapping code với manual walkthrough ở trên
- Giải thích TỪNG DÒNG hoặc TỪNG KHỐI
- Comment tại sao viết như vậy

**Template:**
```markdown
### 2.2. Giải thích code (mapping với manual walkthrough)

```python
# [Code đã AC]
```

**Mapping với phần mô phỏng:**
```python
# Dòng X-Y: [Mục đích]
# Tương ứng với Bước 2 ở trên:
# - pos[1] = 1, pos[2] = 3, ...
pos = [0] * (n + 1)
for i in range(n):
    pos[int(data[i + 1])] = i

# Dòng A-B: [Mục đích]
# Pattern rút ra từ manual walkthrough:
# - Nếu pos[i] < pos[i-1] → cần đợt mới
rounds = 1
for i in range(2, n + 1):
    if pos[i] < pos[i - 1]:
        rounds += 1
```
```

#### 2.3. Why AC? (Tại sao đúng?)

**Template:**
```markdown
### 2.3. Tại sao solution này AC?

✅ **Complexity:** O(N) - đúng với constraints (N ≤ 10^7)
✅ **Edge cases:** Xử lý N=0, N=1, ...
✅ **Correctness:** Chứng minh/suy luận tại sao đúng
✅ **Optimization:** [Nếu có]

**Proof sketch:**
- Lemma 1: ...
- Lemma 2: ...
- Theorem: Algorithm đúng
```

---

### Module 3: Key Takeaways

**Mục đích:** Rút ra bài học tổng quát, kinh nghiệm.

**Template:**
```markdown
## 3. Bài học tổng quát

### Kinh nghiệm nhận diện
🎯 **Khi thấy các dấu hiệu sau, nghĩ đến [Dạng bài]:**
- Dấu hiệu 1: ...
- Dấu hiệu 2: ...
- Dấu hiệu 3: ...

### Pattern cần nhớ
📌 **[Tên pattern]:**
```python
# Template code
pattern_template()
```

### Sai lầm thường gặp
❌ Sai lầm 1: ...
❌ Sai lầm 2: ...
❌ Sai lầm 3: ...

### Tips
💡 **Mẹo:** ...
💡 **Mẹo:** ...
```

---

### Module 4: Theory Extension (OPTIONAL)

**QUYẾT ĐỊNH CỦA AGENT:**
- ✅ SINH nếu: Bài thuộc dạng kinh điển, có nhiều bài tương tự, có lý thuyết nền tảng
- ❌ BỎ QUA nếu: Bài đơn giản, không có pattern tổng quát, không có chuyên đề liên quan

**Template (khi sinh):**
```markdown
## 4. Chuyên đề: [Tên chuyên đề] (MỞ RỘNG)

### Lý thuyết nền tảng

#### 1. Định nghĩa
...

#### 2. Khi nào dùng?
- Dấu hiệu 1
- Dấu hiệu 2

#### 3. Các bước giải
1. ...
2. ...
3. ...

### Templates

#### Template 1: [Tên]
```cpp
// Code template
```

#### Template 2: [Tên]
```python
# Code template
```

### Đọc thêm
- [CP-Algorithms: Topic](link)
- [Codeforces Blog](link)
- [Video tutorial](link)


---

### Module 5: Practice Problems

**Mục đích:** Cung cấp bài tập tương tự để luyện tập.

**Chiến lược tìm bài (theo thứ tự ưu tiên):**
1. **CMOJ** — Dùng agent-browser tìm theo tag/keywords (ưu tiên vì cùng hệ sinh thái)
2. **Codeforces** — Search tag tương ứng ("binary-search", "dp", "greedy"...)
3. **Nếu không tìm được URL thật** — Liệt kê tên bài nổi tiếng kèm note: "[Tự tìm trên CMOJ/Codeforces]"

**KHÔNG để placeholder `[URL]` trong output** — Phải có URL thật hoặc thừa nhận không tìm được.

**Template:**
```markdown
## 5. Bài tập tương tự

### Dễ ⭐
**Bài 1:** [Tên] - [URL thật]
- **Gợi ý:** Giống bài chính, chỉ khác ...
- **Độ khó:** ⭐
- **Lời giải:** <details>...</details>

### Trung bình ⭐⭐
**Bài 2:** [Tên] - [URL thật]
- **Gợi ý:** Thêm constraint ...
- **Độ khó:** ⭐⭐
- **Lời giải:** <details>...</details>

### Khó ⭐⭐⭐
**Bài 3:** [Tên] - [URL thật]
- **Gợi ý:** Cần optimization ...
- **Độ khó:** ⭐⭐⭐
- **Lời giải:** <details>...</details>
```

---

## 🔧 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: URL bài + Code AC (hoặc fetch từ OJ)               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ 1. Fetch Problem       │
         │ - Lấy đề từ URL        │
         │ - Lấy code AC          │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ 2. Manual Walkthrough  │
         │ - Chọn test case       │
         │ - Giải thủ công        │
         │ - Rút pattern          │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ 3. Code Explanation    │
         │ - Map với manual       │
         │ - Giải thích từng dòng │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ 4. Key Takeaways       │
         │ - Rút kinh nghiệm      │
         │ - Pattern              │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ 5. Decide: Theory?     │
         │ - Có chuyên đề không?  │
         │ → YES: Generate        │
         │ → NO: Skip             │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ 6. Practice Problems   │
         │ - Tìm bài tương tự     │
         │ - Viết gợi ý + giải    │
         └────────────────────────┘
```

---

## 📊 Example Output

### Input:
```
User: Biến bài này thành bài giảng
URL: https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
```

### Output:
```markdown
# Bài giảng: Sắp xếp chiếu - Đếm số đợt

## 1. Phân tích bài toán

### Đề bài
Có N phiếu với số hiệu 1..N (hoán vị). Mỗi đợt đi từ đầu đến cuối dãy,
chọn các phiếu liên tiếp theo thứ tự 1, 2, 3, ...
Hỏi cần ít nhất bao nhiêu đợt?

### Input/Output
- **Input:** N và hoán vị A[1..N]
- **Output:** Số đợt tối thiểu
- **Constraints:** N ≤ 10^7

### Nhận diện dạng
- **Keywords:** "số đợt", "ít nhất" → **Counting / Greedy**
- **Độ khó:** ⭐ (Cơ bản)
- **Category:** Array processing

## 2. Solution Breakdown

### 2.1. Mô phỏng thủ công (KHÔNG DÙNG CODE)

**Test case:** N=5, dãy = [3, 1, 4, 2, 5]

**Bước 1: Phân tích yêu cầu**
- Cần chọn đủ các phiếu 1, 2, 3, 4, 5 theo thứ tự
- Mỗi đợt: đi từ trái sang phải, chọn phiếu tiếp theo nếu gặp

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
- Cần phiếu 3 → gặp ở vị trí 0 ✓
- Cần phiếu 4 → gặp ở vị trí 2 ✓
- Cần phiếu 5 → gặp ở vị trí 4 ✓
→ Kết thúc đợt 2, đã chọn: 3, 4, 5

Tổng: 2 đợt ✅

**Bước 3: Rút ra pattern**
- Nhận xét: Đợt mới cần khi phiếu tiếp theo nằm TRƯỚC vị trí hiện tại
- Pattern: `pos[i] < pos[i-1]` → cần đợt mới
- Generalization: Đếm số lần vi phạm monotonicity của positions

### 2.2. Giải thích code (mapping với manual walkthrough)

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    
    # Mapping với Bước 2: Build position array
    # pos[x] = vị trí của phiếu x trong dãy
    # Test case: pos[1]=1, pos[2]=3, pos[3]=0, pos[4]=2, pos[5]=4
    pos = [0] * (n + 1)
    for i in range(n):
        pos[int(data[i + 1])] = i
    
    # Mapping với Bước 3: Count rounds
    # Pattern: pos[i] < pos[i-1] → đợt mới
    # i=2: pos[2]=3 >= pos[1]=1 → OK (cùng đợt)
    # i=3: pos[3]=0 <  pos[2]=3 → Đợt mới! (rounds=2)
    # i=4: pos[4]=2 >= pos[3]=0 → OK
    # i=5: pos[5]=4 >= pos[4]=2 → OK
    rounds = 1
    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            rounds += 1
    
    print(rounds)

solve()
```

### 2.3. Tại sao solution này AC?

✅ **Complexity:** O(N) - đúng với constraints (N ≤ 10^7)
✅ **Edge cases:** Xử lý N=1 (rounds=1)
✅ **Correctness:** 
   - Lemma: Số đợt = 1 + số lần pos[i] < pos[i-1]
   - Proof: Mỗi lần vi phạm → cần đợt mới
✅ **Memory:** O(N) cho position array

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

### Sai lầm thường gặp
❌ Simulate từng đợt → O(N²) TLE
❌ Quên case N=1
❌ Dùng input() thay vì sys.stdin.buffer.read()

### Tips
💡 Dùng position array để O(1) lookup
💡 Đọc input nhanh với sys.stdin.buffer.read()

## 5. Bài tập tương tự

### Dễ ⭐
**Bài 1:** Đếm số lần giảm dần trong dãy
- **Gợi ý:** Đếm số lần a[i] < a[i-1]
- **Độ khó:** ⭐

### Trung bình ⭐⭐
**Bài 2:** Đếm số đoạn liên tiếp tăng dần
- **Gợi ý:** Dùng sliding window
- **Độ khó:** ⭐⭐

### Khó ⭐⭐⭐
**Bài 3:** Đếm số đợt với nhiều điều kiện
- **Gợi ý:** Kết hợp nhiều patterns
- **Độ khó:** ⭐⭐⭐

---

## 🎨 Output Formats và Destination

### Format 1: Markdown (Default)
- Dễ đọc, dễ share
- Support code blocks, tables, LaTeX (với Obsidian/Typora)

### Format 2: PDF (Key use case)
- Export từ Markdown qua Pandoc hoặc Typora/Obsidian
- **LaTeX render đẹp** với công thức, complexity
- Print-friendly, Worksheet style

### Format 3: HTML (Optional)
- Interactive elements
- Collapsible sections

### 📂 Output Destination

Lesson được lưu tại:
```
skills/cp-teacher/outputs/{problem-id}-lesson.md
Ví dụ: outputs/hsgnamdinh2223sapxepchieu-lesson.md
```

**Sau khi tạo xong, agent phải:**
1. Lưu file vào đường dẫn trên
2. Thông báo: `✅ Lesson đã lưu tại outputs/{id}-lesson.md`
3. In tóm tắt: Module 1 + 3 key takeaways chính

---

## 📀 LaTeX Formatting Rules

**Mục đích:** Lesson được thiết kế hướng tới PDF export — dùng LaTeX cho công thức toán để render đẹp.

**Dùng inline LaTeX `$...$` cho:**
- Complexity: `$O(N \log N)$`, `$O(N\sqrt{N})$`, `$O(2^N)$`
- Subscript/superscript: `$a_i$`, `$dp[i][j]$`, `$10^9 + 7$`
- Điều kiện toán học: `$pos[i] < pos[i-1]$`, `$f(n) \geq 0$`
- Công thức đơn: `$\gcd(a, b)$`, `$\binom{n}{k}$`, `$\lfloor N/2 \rfloor$`

**Dùng block LaTeX `$$...$$` cho:**
- Recurrence relation phức tạp:
  ```
  $$dp[i][j] = \max\bigl(dp[i-1][j],\; dp[i-1][j-w_i] + v_i\bigr)$$
  ```
- Proof step quan trọng:
  ```
  $$\text{Số đợt} = 1 + \sum_{i=2}^{N} \mathbf{1}[pos[i] < pos[i-1]]$$
  ```
- Sum/series/limit:
  ```
  $$\sum_{i=1}^{N} \frac{1}{i} = O(\log N)$$
  ```

**KHÔNG dùng LaTeX cho:**
- Code trong fenced code blocks (dùng Python/C++ syntax bình thường)
- ASCII art trong Manual Walkthrough
- Mô tả thuần văn không có ký hiệu toán

**Tương thích:**
- ✅ Obsidian, Typora, Pandoc PDF: render tốt
- ⚠️ GitHub Markdown: không render (cần KaTeX plugin)
- ✅ CMOJ lesson viewer (nếu support MathJax)

---

## 💡 Best Practices

1. **Manual Walkthrough trước Code**
   - Luôn giải thủ công trước
   - Rút pattern từ manual walkthrough

2. **Mapping rõ ràng**
   - Code comment phải reference đến manual walkthrough

3. **Theory chỉ khi cần**
   - Đừng forced theory vào mọi bài
   - Chỉ sinh khi có chuyên đề thực sự liên quan

4. **Practice problems có chọn lọc**
   - Từ dễ → khó
   - Có gợi ý và lời giải, **URL thật** (không placeholder)

5. **LaTeX cho công thức toán**
   - Dùng `$...$` cho inline, `$$...$$` cho block
   - Đảm bảo đẹp khi export PDF

---

## ✅ Quality Gate — Kiểm tra trước khi output

Agent **PHẢI** tự check trước khi xuất lesson:

**Nội dung:**
- [ ] Module 2.1 (Manual Walkthrough): Có ít nhất 1 test case, đủ 3 bước, có ASCII art/formatting
- [ ] Module 2.2 (Code Explanation): Có comment mapping rõ ràng đến walkthrough
- [ ] Module 2.3 (Why AC): Có complexity analysis và ít nhất 1 edge case cụ thể
- [ ] Module 3 (Key Takeaways): Có ít nhất 1 pattern code template
- [ ] Module 4: Hoặc có Theory Extension đầy đủ, hoặc có note "Module 4: Không có chuyên đề mở rộng"
- [ ] Module 5: Có ít nhất 2 bài có URL thật (không phải placeholder)

**Format:**
- [ ] Công thức toán dùng LaTeX (không phải plain text)
- [ ] Lesson file được lưu vào `outputs/{problem-id}-lesson.md`
- [ ] Thông báo cho user file đã được tạo tại đường dẫn nào

**Nếu thiếu bất kỳ điều nào trên → bổ sung trước khi output.**

---

## 🔗 Related Skills

- [codemath-solver](../codemath-solver/SKILL.md) - Để fetch problem và solution
- [cp-solver](../cp-solver/SKILL.md) - Để phân tích algorithm phức tạp

---

**Happy Teaching! 🎓**
