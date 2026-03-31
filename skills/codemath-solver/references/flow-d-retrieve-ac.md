# Flow D: Hồi phục code đã AC (Retrieve AC Code)

Khi một AI Agent nhận được yêu cầu lấy lại source code của bài tập mà người dùng đã giải (AC), hãy làm theo các bước dưới đây để điều khiển `agent-browser` trích xuất source code.

---

## 🔧 Xác định Username

**Cách 1: User cung cấp trực tiếp (RECOMMENDED)**
- Hỏi user: "Username CMOJ của bạn là gì?"
- Hoặc dùng username từ session hiện tại (nếu đã login)

**Cách 2: Auto-discover từ session**
```bash
# Lấy username từ trang chủ
agent-browser open https://laptrinh.codemath.vn && agent-browser wait --load networkidle
agent-browser snapshot -i
# Tìm: "Hello, <username>." trong snapshot
```

---

## Các bước thực thi bằng `agent-browser`

### Bước 1: Điều hướng đến trang submissions

**⚠️ QUAN TRỌNG:** Có 3 cách để filter submissions của user

#### Option A: URL với username (TỐI ƯU NHẤT)

```bash
# Truy cập trực tiếp trang submissions của user cho problem đó
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submissions/USERNAME/" && agent-browser wait --load networkidle

# Ví dụ:
# agent-browser open "https://laptrinh.codemath.vn/problem/hsghanoi2425machdna/submissions/hnkhangdev/"
```

**Ưu điểm:**
- ✅ Chỉ hiện submissions của user đó
- ✅ Không cần filter thủ công
- ✅ Nếu không có submission → user chưa submit bài này

**Nhận biết kết quả:**
- Nếu trang rỗng hoặc redirect → User chưa submit
- Nếu có danh sách → Tiếp tục các bước sau

---

#### Option B: All submissions + Filter thủ công

```bash
# Mở trang tất cả submissions
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submissions/" && agent-browser wait --load networkidle
agent-browser snapshot -i

# Tìm username trong snapshot
# Look for: link "USERNAME" [ref=eX]
# Click vào "source" của submission đó
```

---

#### Option C: "Mine" filter (nếu đã login đúng user)

```bash
# Mở submissions page
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submissions/" && agent-browser wait --load networkidle
agent-browser snapshot -i

# Click "Mine" để filter chỉ hiện submission của mình
# Tìm link " Mine" [ref=eX] trong snapshot
agent-browser click @eX && agent-browser wait --load networkidle
agent-browser snapshot -i
```

### Bước 2: Tìm submission và click "source"

**⚠️ LƯU Ý:** Snapshot có thể KHÔNG hiển thị verdict (AC/WA/TLE).

**Cách làm:**
1. Từ snapshot, tìm username trong danh sách submissions
2. Tìm link "source" đi kèm với username đó
3. Click vào "source" để mở trang chi tiết submission

```bash
# Snapshot để tìm ref
agent-browser snapshot -i

# Tìm trong snapshot:
# - link "USERNAME" [ref=eX]
# - link "source" [ref=eY]  ← ref cần click

# Click source link
agent-browser click @eY && agent-browser wait --load networkidle
```

**Nếu muốn verify AC:**
- Sau khi click "source", snapshot trang detail
- Tìm verdict text (Accepted, AC, hoặc điểm số)

---

### Bước 3: Extract Source Code

**⚠️ QUAN TRỌNG:** KHÔNG dùng `jq` hoặc pipe (bị chặn bởi shell security).

**Cách đơn giản và reliable nhất:**

```bash
# Get current URL (contains submission ID)
agent-browser eval "window.location.href"
# Output: "https://laptrinh.codemath.vn/src/237644"

# Extract code directly from page
agent-browser eval "document.querySelector('pre code')?.innerText || document.querySelector('code')?.innerText || document.querySelector('textarea')?.value"
```

**Giải thích selectors:**
- `pre code` - Code trong preformatted block (phổ biến nhất)
- `code` - Fallback nếu không có pre
- `textarea` - Fallback nếu code trong editable area

**Kết quả trả về:**
- Plain text code (không cần decode JSON)
- Giữ nguyên indentation và newlines
- Sạch sẽ, dễ đọc

---

## 📋 Quick Commands Reference

```bash
# 1. Open user's submissions page (OPTIMAL)
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submissions/USERNAME/" && agent-browser wait --load networkidle

# 2. Get snapshot to find submissions
agent-browser snapshot -i
# Look for: link "source" [ref=eX]

# 3. Click source link
agent-browser click @eX && agent-browser wait --load networkidle

# 4. Extract code
agent-browser eval "document.querySelector('pre code')?.innerText"

# Alternative: Get submission ID from URL
agent-browser eval "window.location.href"
# Then open directly:
agent-browser open "https://laptrinh.codemath.vn/src/SUBMISSION_ID"
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Submissions page empty | User chưa submit bài này → Offer Flow A |
| Can't find "source" link | Check snapshot carefully, may need to scroll |
| No AC verdict visible | Snapshot doesn't always show verdict. Click "source" anyway if it's user's submission. |
| Code extraction returns null | Try different selectors: `pre code` → `code` → `textarea` |
| Pipe/jq errors | **Don't use pipes**. Use direct eval extraction. |

---

## 🔄 Fallback: Problem Statement Retrieval

**Nếu defuddle.md không lấy được đề bài đầy đủ:**

```bash
# Fallback 1: Thử defuddle.md với timeout
curl -s --max-time 10 "https://defuddle.md/https://laptrinh.codemath.vn/problem/<slug>" > /tmp/problem.md

# Check if complete
if ! grep -q "Input" /tmp/problem.md || ! grep -q "Output" /tmp/problem.md; then
    echo "⚠️  defuddle.md incomplete, falling back to agent-browser..."
    
    # Fallback 2: Dùng agent-browser extract
    npx agent-browser open "https://laptrinh.codemath.vn/problem/<slug>"
    npx agent-browser wait --load networkidle
    
    # Extract problem statement
    npx agent-browser eval "document.querySelector('.problem-statement')?.textContent || document.body.textContent" > /tmp/problem.md
fi
```

---

## ✅ Quality Checklist

Trước khi export lesson, check:

- [ ] Username tự động phát hiện
- [ ] Problem statement đầy đủ (Input/Output)
- [ ] Code AC retrieved thành công
- [ ] Lesson có 300+ dòng
- [ ] Có manual walkthrough
- [ ] Có code explanation line-by-line
- [ ] Có edge cases
- [ ] Có common mistakes

## Xử lý Ngoại lệ
- Tiêu chí báo lỗi: Nếu page submissions trống hoặc không có dòng nào đạt `AC`, trả về phản hồi cho user: `"Không tìm thấy submission AC nào trong lịch sử cho bài tập này. Bạn có muốn sử dụng Flow A để tôi tự giải luôn bài này không?"`
