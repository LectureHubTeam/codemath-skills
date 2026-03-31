# CMOJ Website Structure Reference

## URL Patterns

| Page | URL Pattern | Login Required? |
|------|-------------|-----------------|
| Trang chủ | `https://laptrinh.codemath.vn/` | No |
| Danh sách bài | `https://laptrinh.codemath.vn/problems/` | No |
| Chi tiết bài | `https://laptrinh.codemath.vn/problem/<slug>` | No |
| Submit bài | `https://laptrinh.codemath.vn/problem/<slug>/submit` | **Yes** |
| Submissions | `https://laptrinh.codemath.vn/problem/<slug>/submissions/` | No |
| Ranking bài | `https://laptrinh.codemath.vn/problem/<slug>/rank/` | No |
| Login | `https://laptrinh.codemath.vn/accounts/login/` | No |
| Register | `https://laptrinh.codemath.vn/accounts/register/` | No |
| User Profile | `https://laptrinh.codemath.vn/user/<username>` | No |
| Contests | `https://laptrinh.codemath.vn/contests/` | No |

## Trang Problem Detail

### URL
```
https://laptrinh.codemath.vn/problem/<slug>
```

### Cấu trúc nội dung
Trang problem thường chứa các phần sau (theo thứ tự xuất hiện):

1. **Navigation Bar**: Menu chính (Trang chủ, Bài, Các bài nộp, Thành viên, Các kỳ thi...)
2. **Problem Title**: Tiêu đề bài (heading h2 hoặc h3)
3. **Action Links**:
   - "Xem dạng PDF"
   - "Gửi bài giải" → link đến `/problem/<slug>/submit`
   - "Danh sách bài nộp" → link đến `/problem/<slug>/submissions/`
   - "Bài nộp tốt nhất" → link đến `/problem/<slug>/rank/`
4. **Problem Statement**: Mô tả bài toán
5. **Requirements (Yêu cầu)**: Nhiệm vụ cần thực hiện
6. **Input Format (Dữ liệu vào)**: Mô tả format input
7. **Output Format (Kết quả)**: Mô tả format output
8. **Constraints (Ràng buộc)**: Giới hạn N, thời gian, bộ nhớ
9. **Sample I/O (Ví dụ)**: Các test mẫu với INPUT và OUTPUT
10. **Comments (Bình luận)**: Phần comment

### Lưu ý quan trọng
- Công thức toán học có thể được hiển thị bằng LaTeX/MathJax: `~(N \le 10^9)~`
- Một số bài có nhiều subtask với điểm khác nhau
- Sample I/O nằm trong `<pre>` hoặc `<code>` blocks

## Trang Login

### URL
```
https://laptrinh.codemath.vn/accounts/login/
```

### Form Elements (thường gặp)
- Input username: `name="username"` hoặc `id="id_username"`
- Input password: `name="password"` hoặc `id="id_password"`, `type="password"`
- Login button: `<button type="submit">` hoặc `<input type="submit">`
- Link "Quên mật khẩu?"
- Có thể có CSRF token hidden input

### Detect login state
- **Đã login**: Header hiển thị username, có link "Đăng xuất"
- **Chưa login**: Header hiển thị "Đăng nhập" và "Đăng ký"

## Trang Submit

### URL
```
https://laptrinh.codemath.vn/problem/<slug>/submit
```

### Form Elements (thường gặp)
- **Language selector**: `<select>` dropdown, `name="language"` hoặc `id="id_language"`
  - Các giá trị phổ biến: `CPP17`, `CPP20`, `PY3`, `JAVA`, `C`
- **Source code**: Có thể là:
  - `<textarea name="source">` - textarea thường
  - CodeMirror editor wrapper (`.CodeMirror` class)
  - ACE editor (`.ace_editor` class)
- **Submit button**: `<button type="submit">` hoặc `<input type="submit">`
- **CSRF Token**: Hidden input `name="csrfmiddlewaretoken"`

### Inject code vào editor (khi không phải textarea)

**CodeMirror:**
```javascript
const cm = document.querySelector('.CodeMirror');
if (cm && cm.CodeMirror) {
    cm.CodeMirror.setValue(codeString);
}
```

**ACE Editor:**
```javascript
const editor = ace.edit(document.querySelector('.ace_editor'));
editor.setValue(codeString, -1);
```

**Textarea (với fallback):**
```javascript
const ta = document.querySelector('#id_source, textarea[name="source"]');
if (ta) {
    ta.value = codeString;
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## Trang Kết quả Submit

### Verdict Codes

| Code | Meaning | Màu (thường) |
|------|---------|---------------|
| AC | Accepted - Đúng | Xanh lá |
| WA | Wrong Answer - Sai | Đỏ |
| TLE | Time Limit Exceeded | Vàng/Cam |
| MLE | Memory Limit Exceeded | Vàng/Cam |
| RE | Runtime Error | Xám/Tím |
| CE | Compilation Error | Xám |
| IR | Invalid Return | Xám |
| PE | Presentation Error | Vàng |

### Thông tin thường hiển thị
- Submission ID
- Thời gian submit
- Ngôn ngữ
- Verdict (AC/WA/TLE/...)
- Thời gian chạy (ms)
- Bộ nhớ sử dụng (KB)
- Điểm (nếu subtask)

## Supported Languages (thường gặp trên CMOJ)

| Display Name | Value (select) | File Extension |
|-------------|----------------|----------------|
| C++17 | CPP17 | .cpp |
| C++20 | CPP20 | .cpp |
| C | C | .c |
| Python 3 | PY3 | .py |
| Java | JAVA | .java |
| Pascal | PAS | .pas |

> **Lưu ý**: Danh sách language có thể khác cho từng bài hoặc từng contest. Luôn kiểm tra dropdown trên form submit thực tế.
