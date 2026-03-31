# Troubleshooting Guide - CodeMath Solver

## Login Issues

### Problem: Redirect loop khi login
**Symptoms**: Sau khi fill form login → click submit → quay lại trang login
**Causes**:
- CSRF token không hợp lệ
- Cookie bị block

**Fix**:
```bash
# Thử clear state và login lại
agent-browser close
agent-browser open https://laptrinh.codemath.vn/accounts/login/ && agent-browser wait --load networkidle
agent-browser snapshot -i
# Fill form lại...
```

### Problem: Login page yêu cầu CAPTCHA
**Fix**: Pause và hỏi user giải CAPTCHA thủ công

### Problem: Credentials không worked
**Fix**:
1. Verify username/password đúng
2. Kiểm tra account có bị khóa không
3. Thử login manual qua browser headed mode:
   ```bash
   agent-browser --headed open https://laptrinh.codemath.vn/accounts/login/
   ```

---

## Code Submission Issues 🔴

### Problem: `SyntaxError: invalid syntax` sau khi submit

**Symptoms**: Code bị dính dòng, ví dụ: `print(a)import sys` thay vì xuống dòng

**Causes**:
- Dùng `agent-browser fill` với code nhiều dòng
- Newline characters (`\n`) không được xử lý đúng

**Fix**:
```bash
# ❌ KHÔNG DÙNG: fill cho code nhiều dòng
agent-browser fill @eCODE "import sys
def solve():
    ..."

# ✅ DÙNG: eval với template literal JavaScript
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value = `import sys

def solve():
    # code here
    pass`'
```

---

### Problem: `Action on "@eX" timed out` khi fill code

**Symptoms**: Lỗi timeout khi cố fill/click vào textarea

**Causes**:
- Element bị hidden bởi CodeMirror/ACE editor overlay
- Có popup/modal đang che trang

**Fix**:
```bash
# 1. Check overlay/modal
agent-browser snapshot -i
# Tìm element close modal và click trước

# 2. Nếu không có modal, dùng eval thay vì fill
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value = `code`'

# 3. Submit form trực tiếp nếu button bị block
agent-browser eval 'document.querySelector("form").submit()'
```

---

### Problem: Code length = 0 sau khi fill

**Symptoms**: Verify code thì `value.length` = 0

**Causes**:
- Selector sai (textarea bị ẩn, class name khác)
- Code chưa được inject thành công

**Fix**:
```bash
# 1. Verify selector đúng
agent-browser eval 'document.querySelectorAll("textarea").length'
# Should return > 0

# 2. Try multiple selectors
agent-browser eval 'document.querySelector("textarea[name=\"source\"], #id_source, .CodeMirror textarea").value'

# 3. Check code đã inject chưa
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'
# Should be > 0
```

---

### Problem: Submit bị CE (Compilation Error)

**Symptoms**: Code local chạy OK nhưng submit bị CE

**Causes**:
- Code bị corrupt khi inject (mất newline, sai indentation)
- Missing imports hoặc syntax errors

**Fix**:
```bash
# 1. Verify code trước submit
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.split("\\n")[0]'

# 2. Screenshot để verify visual
agent-browser screenshot --annotate
# 3. Nếu CE, đọc error message và fix
curl "defuddle.md/<current_url>"
# Tìm dòng "Compilation Error" và message lỗi
```

---

### Problem: Element bị overlay/modal che

**Symptoms**: `Element "@eX" is blocked by another element`

**Fix**:
```bash
# 1. Snapshot tìm modal
agent-browser snapshot -i

# 2. Click close modal (thường là @eX với icon X)
agent-browser click @eX

# 3. Hoặc scroll page
agent-browser scroll down 100

# 4. Retry action
agent-browser click @eCODE
```

---

## Submit Issues (General)

### Problem: Code editor là CodeMirror, không fill được bằng `fill` command

**Symptoms**: `agent-browser fill @eX "code"` không có effect hoặc bị lỗi timed out (không interactable).

**Fix**: Dùng JavaScript evaluation:

```bash
# Cách 1: Cho CodeMirror
agent-browser eval 'const cm = document.querySelector(".CodeMirror");
if (cm && cm.CodeMirror) {
    cm.CodeMirror.setValue(`CODE_HERE`);
}'

# Cách 2: Cho ACE Editor
agent-browser eval 'const ace = document.querySelector(".ace_editor");
if (ace && ace.env && ace.env.editor) {
    ace.env.editor.setValue(`CODE_HERE`, -1);
}'

# Cách 3: Fallback cho textarea thường
agent-browser eval 'const ta = document.querySelector("textarea[name=\"source\"], #id_source");
if (ta) {
    ta.value = `CODE_HERE`;
    ta.dispatchEvent(new Event("input", {bubbles: true}));
    ta.dispatchEvent(new Event("change", {bubbles: true}));
}'
```

---

### Problem: Language selector không chọn được

**Fix**:
```bash
# Thử snapshot chi tiết hơn
agent-browser snapshot -i -C

# Hoặc dùng eval
agent-browser eval 'const sel = document.querySelector("#id_language, select[name=\"language\"]");
if (sel) {
    sel.value = "CPP17";
    sel.dispatchEvent(new Event("change", {bubbles: true}));
}'
```

---

### Problem: Submit button click nhưng không submit

**Causes**: CSRF token, form validation, JS event handlers

**Fix**:
```bash
# Try submitting form directly
agent-browser eval 'document.querySelector("form").submit()'
```

---

### Problem: Code bị truncated khi fill (code quá dài)

**Fix**:
1. Lưu code vào file tạm
2. Dùng `eval` để đọc file và inject:

```bash
# Lưu code vào file
cat > /tmp/solution_code.txt << 'CODEEOF'
...code...
CODEEOF

# Encode sang base64
CODE_B64=$(base64 < /tmp/solution_code.txt)

# Inject via eval
agent-browser eval 'atob("BASE64_CODE_HERE").split("\\n").forEach((line, i) => {
    const ta = document.querySelector("textarea[name=\"source\"]");
    ta.value += line + (i < totalLines - 1 ? "\\n" : "");
})'
```

---

## Snapshot Issues

### Problem: Refs không match elements mong đợi
**Causes**: Refs bị invalidated sau navigation/DOM changes

**Fix**: Luôn re-snapshot:
```bash
agent-browser snapshot -i    # Fresh snapshot
# Dùng refs mới
```

### Problem: Không thấy submit form elements
**Causes**: Cần login trước, hoặc page chưa load xong

**Fix**:
```bash
agent-browser wait --load networkidle
agent-browser snapshot -i -C    # Include cursor-interactive elements
```

### Problem: Đề bài bị cắt do page dài
**Fix**:
```bash
# Scroll và snapshot nhiều lần
agent-browser snapshot -i
agent-browser scroll down 500
agent-browser snapshot -i
agent-browser scroll down 500
agent-browser snapshot -i

# Hoặc get full text
curl "defuddle.md/<current_url>"
```

## Test Local Issues

### Problem: g++ not found
**Fix**:
```bash
# macOS
xcode-select --install
# hoặc
brew install gcc
```

### Problem: Python solution TLE nhưng C++ AC
**Notes**: Python thường chậm hơn C++ 5-10x. Nếu bài yêu cầu O(N) với N lớn, xem xét:
1. Dùng `sys.stdin.readline` thay `input()`
2. Dùng `sys.stdout.write` thay `print()`
3. Tránh recursion (dùng iterative)
4. Hoặc chuyển sang C++

## Result Interpretation

### AC nhưng chỉ 50% điểm
**Cause**: Bài có subtask, code chỉ pass subtask đơn giản
**Fix**: Kiểm tra constraints của subtask cao hơn, tối ưu thuật toán

### WA trên test ẩn nhưng đúng sample
**Fix**:
1. Kiểm tra edge cases: N=0, N=1, N rất lớn
2. Kiểm tra integer overflow
3. Kiểm tra output format chính xác (trailing spaces, newlines)
4. Thử sinh random test cases và brute force verify

### RE (Runtime Error)
**Common causes**:
- Array index out of bounds
- Division by zero
- Stack overflow (recursion quá sâu)
- Segfault (null pointer)

**Fix**: Kiểm tra và thêm bounds checking, dùng iterative thay recursion

---

## Advanced Issues (From Real Contest Experience) 🔴

### Problem: Code injection bị corrupt (encoding issues)

**Symptoms**: Submit bị CE với lỗi `invalid non-printable character U+001E` hoặc ký tự lạ

**Causes**:
- Code có comment tiếng Việt hoặc ký tự đặc biệt
- Base64 encoding/decoding bị lỗi với Unicode characters

**Fix**:
```bash
# ✅ BEST PRACTICE: Code không có comment tiếng Việt
import sys

def solve():
    # Use English comments only
    data = sys.stdin.read().split()
    if not data:
        return
    # ... rest of code

# ❌ TRÁNH: Comment tiếng Việt
def solve():
    # Tính toán giá trị lớn nhất  ← Có thể gây lỗi encoding
```

### Prevention:
1. **Chỉ dùng English comments** trong code
2. **Ưu tiên template literal** cho code ngắn (< 50 dòng):
   ```bash
   agent-browser eval 'const code = `import sys
   def solve():
       # English comment
       pass`; document.querySelector("textarea[name=\"source\"]").value = code;'
   ```
3. **Verify sau inject**:
   ```bash
   # Check length
   agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'
   
   # Check first line
   agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.split("\\n")[0]'
   ```

---

### Problem: TLE - Time Limit Exceeded (Algorithm too slow)

**Symptoms**: Pass test nhỏ nhưng TLE test lớn (N ≤ 10^9, Q ≤ 10^5)

**Causes**:
- Algorithm complexity quá cao (O(N*Q) thay vì O(1) per query)
- Loop thay vì dùng math formula

**Fix**:

#### 📊 Constraint → Complexity Guide:

| Constraints | Max Complexity | Algorithm Pattern |
|-------------|---------------|-------------------|
| N ≤ 100 | O(N³), O(N⁴) | Brute force, Floyd |
| N ≤ 1000 | O(N²) | DP, DFS, BFS |
| N ≤ 10^5 | O(NlogN), O(N) | Sort, Binary Search, Greedy |
| N ≤ 10^6 | O(N), O(logN) | Linear scan |
| N ≤ 10^9 | **O(1), O(logN)** | **Math formula**, Binary Search |

#### 🚨 Red flags cần optimize:

- **Q queries với N ≤ 10^9** → Cần O(1) per query
- **Loop qua N lớn** → Tìm công thức toán
- **Time limit < 1s** → Ưu tiên O(N) hoặc O(NlogN)

#### ✅ Pattern thường gặp:

```python
# ❌ SLOW: O(N) per query
for query in queries:
    total = 0
    for i in range(1, N+1):  # ← Loop N lần
        total += i

# ✅ FAST: O(1) per query
for query in queries:
    total = N * (N + 1) // 2  # ← Công thức
```

---

### Problem: Refs thay đổi sau navigation

**Symptoms**: `Element "@eX" not found` hoặc click nhầm element

**Causes**:
- Refs bị invalidate sau `open`, `click`, `wait --load`
- Dùng refs cũ sau khi page reload

**Fix**:

```bash
# ❌ WRONG: Dùng refs cũ sau navigation
agent-browser click @e15  # Navigate
agent-browser fill @e17 "code"  # @e17 có thể không còn đúng!

# ✅ CORRECT: LUÔN re-snapshot sau navigation
agent-browser click @e15
agent-browser wait --load networkidle
agent-browser snapshot -i  # ← Lấy refs MỚI
agent-browser fill @eNEW "code"  # ← Dùng refs từ snapshot mới
```

### Rule:
> **LUÔN re-snapshot** sau: `open`, `click`, `wait --load`, hoặc bất kỳ action nào làm thay đổi DOM.

---

### Problem: Không verify code trước submit

**Symptoms**: Submit xong bị CE hoặc code rỗng

**Causes**:
- Inject code không thành công
- Code bị corrupt nhưng không check trước

**Fix**:

```bash
# PRE-SUBMIT CHECKLIST (BẮT BUỘC):

# 1. Check code length (> 0)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'
# Output: 263 → OK

# 2. Check first line (verify encoding)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.split("\\n")[0]'
# Output: "import sys" → OK

# 3. Snapshot verify visual (nếu cần)
agent-browser snapshot -i
```

---

## Contest Retry Strategy 🔄

### Khi bài bị thất bại trong contest:

| Verdict | Nguyên nhân thường gặp | Hành động |
|---------|----------------------|-----------|
| **WA** | Logic sai, edge cases | 1. Check sample again 2. Test edge cases (N=0, N=1, N lớn) 3. Read problem again |
| **TLE** | Algorithm quá chậm | 1. Giảm complexity 2. Dùng math formula 3. Optimize I/O |
| **MLE** | Dùng nhiều bộ nhớ | 1. Giảm array size 2. Dùng kiểu nhỏ hơn 3. Xóa biến thừa |
| **CE** | Syntax error, encoding | 1. Check syntax 2. Verify encoding 3. Check language version |
| **RE** | Runtime error | 1. Check array bounds 2. Check division by zero 3. Check null |

### Retry pattern:

```
⏳ [i/N] <slug> - WA
├─ Phân tích: Sai test case #15 (N lớn)
├─ Nguyên nhân: O(N*Q) quá chậm
├─ Giải pháp: Dùng công thức O(1)
├─ Test local: ✅ Sample đúng
└─ Retry submit...
```

### Retry limit:
- Tối đa **3 lần retry** cho mỗi bài
- Sau 3 lần fail → Skip, qua bài tiếp theo, quay lại sau
