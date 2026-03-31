# Flow A: Giải Bài Nhất Định

## Pre-flight Checklist ✅

Trước khi bắt đầu flow, đảm bảo các yêu cầu sau:

- [ ] **Đã login**: Kiểm tra bằng `snapshot -i`, thấy "Hello, <username>." hoặc "Đăng xuất"
- [ ] **Có problem slug**: Extract từ URL hoặc user cung cấp
- [ ] **Code đã lưu file**: Lưu solution vào `/tmp/codemath_solution.py` hoặc `.cpp`
- [ ] **Đã test local**: Chạy với sample input, verify output đúng
- [ ] **Đã test edge cases**: Test với giá trị biên từ constraints

---

## Bước 1: Kiểm tra & Login

### 1.1. Kiểm tra trạng thái login

```bash
# Mở trang CMOJ và kiểm tra đã login chưa
agent-browser open https://laptrinh.codemath.vn/ && agent-browser wait --load networkidle
agent-browser snapshot -i
```

**Cách kiểm tra đã login**: Tìm trong snapshot:
- ✅ **Đã login**: Có text `"Hello, <username>."` hoặc link `"Đăng xuất"` / `"Logout"`
- ❌ **Chưa login**: Có link `"Đăng nhập"` hoặc `"Login"`

### 1.2. Thực hiện login (nếu chưa login)

```bash
# Navigate đến trang login
agent-browser open https://laptrinh.codemath.vn/accounts/login/ && agent-browser wait --load networkidle
agent-browser snapshot -i
```

**Tìm form login** trong snapshot: Thường có:
- Input **username** (type="text" hoặc name="username")
- Input **password** (type="password" hoặc name="password")
- Button **Đăng nhập** hoặc **Login**

```bash
# Fill form login - thay @eX bằng refs thực tế từ snapshot
agent-browser fill @eX "USERNAME_HERE"    # username field
agent-browser fill @eY "PASSWORD_HERE"    # password field
agent-browser click @eZ                   # login button
agent-browser wait --load networkidle
agent-browser snapshot -i                  # Verify login thành công
```

**⚠️ CÁC LỰA CHỌN ĐỂ LOGIN:**

**Option A: Dùng Headless Browser (Mặc định)**
1. **KHÔNG BAO GIỜ hardcode username/password** trong code hoặc output
2. Nếu chưa có credentials → **HỎI USER** cung cấp username và password
3. Sử dụng agent-browser auth vault nếu có sẵn:
   ```bash
   # Kiểm tra auth profile
   agent-browser auth list
   # Login bằng saved profile
   agent-browser auth login codemath
   ```
4. Lưu state để dùng lại sau:
   ```bash
   agent-browser state save codemath-auth.json
   ```

**Option B: Dùng Local Chrome với Remote Debugging (Khuyên Dùng)**
Thay vì để Agent login mỗi lần qua trình duyệt ảo, ta có thể kết nối `agent-browser` trực tiếp vào một tab của Google Chrome đã mở sẵn và chia sẻ phiên đăng nhập thực tế của hệ điều hành.

Các lệnh cài đặt để mở Chrome có gắn Remote Debugging Port (Thực thi trong terminal của User):
```bash
# B1. Tạo thư mục chứa config (làm 1 lần)
mkdir -p ~/chrome-debug-profile

# B2. Mở Chrome với remote debugging (để terminal này chạy nền)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/chrome-debug-profile \
  --no-first-run \
  --no-default-browser-check

# B3. Kết nối agent-browser vào local Chrome
agent-browser connect 9222
```
*Lưu ý Option B: Người dùng cần tự đăng nhập bằng tay 1 lần bằng trình duyệt vừa mở lên, sau đó các lần tiếp theo session auth sẽ được giữ mãi mãi.*

### 1.3. Lưu session sau login (nếu dùng Option A)

```bash
# Lưu state để dùng lại sau
agent-browser state save codemath-auth.json
```

---

## Bước 2: Truy cập & Đọc đề bài

### 2.1. Navigate đến bài tập

```bash
# Mở trang bài tập
agent-browser open "https://laptrinh.codemath.vn/problem/PROBLEM_SLUG" && agent-browser wait --load networkidle
```

**Thay `PROBLEM_SLUG`** bằng slug thực tế (ví dụ: `hsgthaibinh2425sodacbiet`).

### 2.2. Extract nội dung đề bài

**⚠️ QUAN TRỌNG:** `snapshot -i` thường **KHÔNG hiển thị nội dung đề bài** chi tiết.

**Cách đúng để lấy nội dung đề:**
```bash
# Dùng defuddle.md để extract content
curl "defuddle.md/https://laptrinh.codemath.vn/problem/PROBLEM_SLUG"
```

Từ output defuddle, extract các thông tin sau:
1. **Tên bài**: Tiêu đề bài tập
2. **Đề bài (Statement)**: Mô tả chi tiết bài toán
3. **Yêu cầu**: Nhiệm vụ cần thực hiện
4. **Input format**: Định dạng dữ liệu đầu vào
5. **Output format**: Định dạng kết quả đầu ra
6. **Constraints/Ràng buộc**: Giới hạn (N, thời gian, bộ nhớ)
7. **Sample Input/Output**: Các ví dụ mẫu

### 2.3. Cấu trúc trang CMOJ (tham khảo)

Trang problem trên CMOJ thường có cấu trúc:
```
URL pattern: https://laptrinh.codemath.vn/problem/<slug>
Submit URL:  https://laptrinh.codemath.vn/problem/<slug>/submit
Rank URL:    https://laptrinh.codemath.vn/problem/<slug>/rank/
```

Nội dung đề thường nằm trong phần content chính, bao gồm:
- Tiêu đề bài (h2 hoặc h3)
- Mô tả (paragraphs)
- "Dữ liệu vào" / "Kết quả" (h4 headings)
- Sample I/O trong code blocks
- Ràng buộc/Constraints

---

## Bước 3: Phân tích & Sinh code giải

### 3.1. Phân tích bài toán

Sau khi đọc đề, phân tích:
1. **Loại bài**: Math, DP, Graph, Greedy, String, etc.
2. **Complexity yêu cầu**: Dựa trên constraints (N ≤ 10^5 → O(NlogN), N ≤ 10^6 → O(N), etc.)
3. **Edge cases**: Giá trị biên, trường hợp đặc biệt
4. **Thuật toán phù hợp**: Chọn thuật toán tối ưu

### 3.2. Generate code

Viết code giải theo ngôn ngữ được chọn.

#### 📊 Constraint → Algorithm Selection

**QUAN TRỌNG**: Chọn thuật toán dựa trên constraints!

| Constraints | Max Complexity | Algorithm Pattern |
|-------------|---------------|-------------------|
| N ≤ 100 | O(N³), O(N⁴) | Brute force, Floyd |
| N ≤ 1000 | O(N²) | DP, DFS, BFS |
| N ≤ 10^5 | O(NlogN), O(N) | Sort, Binary Search, Greedy |
| N ≤ 10^6 | O(N), O(logN) | Linear scan |
| N ≤ 10^9 | **O(1), O(logN)** | **Math formula**, Binary Search |
| N ≤ 10^255 (string) | O(length of string) | String processing |

**🚨 Red flags cần optimize:**
- **Q queries với N ≤ 10^9** → Cần O(1) per query
- **Loop qua N lớn** → Tìm công thức toán
- **Time limit < 1s** → Ưu tiên O(N) hoặc O(NlogN)

**Cho Python 3 (PY3):**
```python
import sys
input = sys.stdin.readline

def solve():
    # Solution code here
    pass

solve()
```

**Cho C++ (CPP17/CPP20):**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    // Solution code here
    return 0;
}
```

**Nguyên tắc quan trọng:**
- Đọc input từ **stdin**, ghi output ra **stdout**
- Không sử dụng file I/O trừ khi đề yêu cầu
- Tối ưu hóa I/O: `sys.stdin.readline` cho Python, `ios_base::sync_with_stdio(false)` cho C++
- Xử lý tất cả edge cases từ constraints
- **KHÔNG dùng comment tiếng Việt** trong code (chỉ English hoặc không comment)

### 3.3. Lưu code vào file

```bash
# Lưu vào file để test
# File path: /tmp/codemath_solution.py (Python) hoặc /tmp/codemath_solution.cpp (C++)
```

---

## Bước 4: Test local với sample

### 4.1. Compile (cho C++)

```bash
g++ -std=c++17 -O2 -o /tmp/codemath_solution /tmp/codemath_solution.cpp
```

### 4.2. Chạy test với sample input

**Cho Python:**
```bash
python3 /tmp/codemath_solution.py < /tmp/codemath_input.txt
```

**Cho C++:**
```bash
/tmp/codemath_solution < /tmp/codemath_input.txt
```

### 4.3. Verify kết quả

- So sánh output với expected output từ sample
- **Nếu sai (WA):** Phân tích lỗi, sửa code, test lại (tối đa 3 lần retry)
- **Nếu đúng:** Tiến hành submit

### 4.4. Test thêm edge cases

Tạo thêm test cases dựa trên constraints:
```bash
# Ví dụ: test với edge cases
echo "1" > /tmp/codemath_edge1.txt
python3 /tmp/codemath_solution.py < /tmp/codemath_edge1.txt

echo "999999999999999999999999999999999999999999999999999" > /tmp/codemath_edge2.txt
python3 /tmp/codemath_solution.py < /tmp/codemath_edge2.txt
```

---

## Bước 5: Submit bài

### 5.1. Navigate đến trang submit

```bash
agent-browser open "https://laptrinh.codemath.vn/problem/PROBLEM_SLUG/submit" && agent-browser wait --load networkidle
agent-browser snapshot -i
```

### 5.2. Xác định form elements

Snapshot sẽ hiển thị form submit với các elements:
- **Textarea/Button "Paste"**: Vùng nhập code (tìm ref có text "Paste your source code" hoặc `textarea`)
- **Language selector**: Dropdown để chọn ngôn ngữ (Python 3, C++17, etc.)
- **Submit button**: Nút gửi bài (tìm ref có text "Submit!" hoặc "Gửi bài")

### 5.3. Inject code vào form

**⚠️ QUAN TRỌNG:** Shell security chặn backticks (`` ` ``) và command substitution `$()`.

**KHÔNG DÙNG:** `` `code` `` hoặc `$(command)` - sẽ bị lỗi security.

#### 🟢 Cách 1: `eval` với escaped newlines (cho code ≤ 20 dòng)

```bash
# Dùng double quotes, escape newlines thành \n
agent-browser eval "document.querySelector('textarea[name=\"source\"]').value = 'import sys\n\ndef solve():\n    # Code here\n    pass\n'"
```

**Lưu ý:**
- Dùng **double quotes** `"` bao ngoài command
- Dùng **single quotes** `'` bao JavaScript string
- Escape newlines thành `\n`
- Escape quotes trong code Python thành `\'`

#### 🟢 Cách 2: `eval -b` với base64 (RECOMMENDED - cho mọi độ dài)

```bash
# Bước 1: Encode code sang base64
base64 -i /tmp/codemath_solution.py
# Output: TU9EID0gMjAxNwo...

# Bước 2: Decode và inject (dùng atob trong JavaScript)
agent-browser eval "atob('TU9EID0gMjAxNwo...')"
```

**Hoặc gộp 2 bước (nếu shell hỗ trợ):**
```bash
CODE_B64=$(base64 -i /tmp/codemath_solution.py) && agent-browser eval "atob('$CODE_B64')"
```

**Ưu điểm:**
- ✅ Không lo escape characters
- ✅ Giữ nguyên indentation, newlines
- ✅ Làm việc với code dài

#### 🟢 Cách 3: Đọc file và inject trực tiếp (cho code ngắn)

```bash
# Đọc file, replace newlines thành \n
CODE=$(cat /tmp/codemath_solution.py | tr '\n' '\\' | sed 's/\\/\\n/g')
agent-browser eval "document.querySelector('textarea[name=\"source\"]').value = '$CODE'"
```

#### 🔴 Cách 4: CodeMirror/ACE Editor API (nếu textarea không hoạt động)

```bash
# Cho CodeMirror
agent-browser eval 'const cm = document.querySelector(".CodeMirror");
if (cm && cm.CodeMirror) {
    cm.CodeMirror.setValue(atob("BASE64_CODE"));
}'

# Cho ACE Editor  
agent-browser eval 'const editor = ace.edit(document.querySelector(".ace_editor"));
editor.setValue(atob("BASE64_CODE"), -1);'
```

**Khi nào dùng:** Nếu `textarea[name="source"]` không tồn tại hoặc code không inject được.

### 5.4. Verify code đã inject thành công

**LUÔN verify trước khi submit:**

```bash
# Check độ dài code (> 0 là OK)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'
# Output: 427 → OK

# Check dòng đầu tiên (verify không bị corrupt)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.split("\\n")[0]'
# Output: "import sys" → OK
```

**Troubleshooting:**
| Triệu chứng | Nguyên nhân | Giải pháp |
|-------------|-------------|-----------|
| Code length = 0 | Selector sai | Check selector: `textarea[name="source"]` |
| Syntax Error | Code bị dính dòng | Dùng `\n` escape, không dùng backticks |
| Element blocked | Overlay che | Tìm và close modal, hoặc scroll |
| Command substitution blocked | Dùng `` ` `` hoặc `$()` | Dùng double quotes + escape `\n` hoặc base64 |
| Backticks error | Security policy chặn | Chuyển sang `atob('BASE64')` |

### 5.5. Click submit

```bash
# Tìm ref của button "Submit!" từ snapshot
agent-browser click @eX && agent-browser wait --load networkidle
```

**⚠️ LƯU Ý:** Flow tự động submit sau khi test pass, không cần confirm user.

### 5.6. Kiểm tra kết quả submit

Sau khi submit, CMOJ sẽ chuyển đến trang submission detail.

```bash
agent-browser snapshot -i
```

**Nếu snapshot không hiện verdict chi tiết:**
```bash
# Extract text từ page
agent-browser eval "document.body.innerText.substring(0, 800)"
```

**Verdict codes:**
| Code | Meaning | Màu (thường) | Action |
|------|---------|--------------|--------|
| AC | Accepted - Đúng | Xanh lá | ✅ Done |
| WA | Wrong Answer - Sai | Đỏ | Fix logic, edge cases |
| TLE | Time Limit Exceeded | Vàng/Cam | Optimize algorithm |
| MLE | Memory Limit Exceeded | Vàng/Cam | Reduce memory |
| RE | Runtime Error | Xám/Tím | Check bounds, div by zero |
| CE | Compilation Error | Xám | Fix syntax |

---

## Bước 6: Retry nếu thất bại

### 6.1. Phân tích lỗi

| Verdict | Nguyên nhân thường gặp | Hành động |
|---------|----------------------|-----------|
| **WA** | Logic sai, edge cases thiếu, đọc đề không kỹ | Đọc lại đề, test edge cases, sửa code |
| **TLE** | Algorithm quá chậm, I/O chậm | Optimize complexity, dùng I/O nhanh |
| **MLE** | Dùng quá nhiều bộ nhớ | Giảm data structures, dùng kiểu nhỏ hơn |
| **RE** | Array out of bounds, div by zero, stack overflow | Check bounds, null checks |
| **CE** | Syntax errors, wrong language version | Fix syntax, check compiler version |

### 6.2. Retry flow

- Tối đa **3 lần retry** cho mỗi bài
- Mỗi lần retry: phân tích lỗi → sửa code → test local → submit lại
- Nếu sau 3 lần vẫn fail → báo user và cung cấp phân tích chi tiết

### 6.3. Escalation to CP-Solver

**Khi nào cần escalate sang [cp-solver](../cp-solver/SKILL.md):**

| Dấu hiệu | Action |
|----------|--------|
| TLE 2+ lần dù optimize | → `task: cp-solver` |
| Algorithm khó (Segment Tree, Mo's, DP optimization) | → `task: cp-solver` |
| User hỏi sâu ("Tại sao TLE?", "Có cách nào tối ưu?") | → `task: cp-solver` |

**Chi tiết escalation:** Xem [references/escalation.md](escalation.md)

---

## Xử lý tình huống đặc biệt

### CAPTCHA
Nếu gặp CAPTCHA:
1. Pause ngay lập tức
2. Thông báo user: "Trang yêu cầu giải CAPTCHA"
3. Chờ user giải thủ công hoặc hướng dẫn tiếp

### Rate Limit
Nếu bị rate limit:
1. Thông báo user
2. Đợi 60-120 giây
3. Retry

### Bài yêu cầu file I/O
Một số bài CMOJ yêu cầu đọc/ghi file (ví dụ: `INPUT.INP`, `OUTPUT.OUT`):
- Phát hiện qua đề bài (tìm mention `.INP`, `.OUT`, `freopen`)
- Adjust code để dùng `freopen()` cho C++ hoặc file open cho Python

---

## Ví dụ sử dụng đầy đủ

### Ví dụ 1: Giải bài "Số đặc biệt" bằng Python

```
User: Giải bài hsgthaibinh2425sodacbiet trên codemath bằng Python
```

Agent sẽ:
1. Mở https://laptrinh.codemath.vn/problem/hsgthaibinh2425sodacbiet
2. Đọc đề bằng defuddle: "Kiểm tra tổng chữ số có phải số nguyên tố"
3. Sinh code Python:
   ```python
   import sys

   def is_prime(n):
       if n < 2: return False
       if n == 2: return True
       if n % 2 == 0: return False
       i = 3
       while i * i <= n:
           if n % i == 0: return False
           i += 2
       return True

   def solve():
       s = sys.stdin.readline().strip()
       digit_sum = sum(int(c) for c in s)
       print("YES" if is_prime(digit_sum) else "NO")

   solve()
   ```
4. Test local: 23 → YES ✅, 17 → NO ✅
5. Submit tự động → AC

---

## Quick Commands Reference

```bash
# 1. Check login
agent-browser open https://laptrinh.codemath.vn && agent-browser wait --load networkidle
agent-browser snapshot -i
# Look for: "Hello, <username>." = logged in

# 2. Read problem
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG" && agent-browser wait --load networkidle
curl "defuddle.md/https://laptrinh.codemath.vn/problem/SLUG"

# 3. Test solution
echo "23" | python3 /tmp/codemath_solution.py

# 4. Submit
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submit" && agent-browser wait --load networkidle
agent-browser snapshot -i

# Inject code - OPTION A: Escaped newlines (short code)
agent-browser eval "document.querySelector('textarea[name=\"source\"]').value = 'import sys\n\ndef solve():\n    pass\n'"

# Inject code - OPTION B: Base64 (recommended for long code)
base64 -i /tmp/codemath_solution.py  # Copy output
agent-browser eval "atob('PASTE_BASE64_HERE')"

# Verify
agent-browser eval "document.querySelector('textarea[name=\"source\"]').value.length"
# Output > 0 = OK

# Submit
agent-browser click @eX && agent-browser wait --load networkidle

# 5. Check result
agent-browser snapshot -i
agent-browser eval "document.body.innerText.substring(0, 800)"
# Look for: "Accepted", "Wrong Answer", "Time Limit", etc.
```

---
