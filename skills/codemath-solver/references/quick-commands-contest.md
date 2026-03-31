# Quick Commands - Contest Flow

Quick reference card cho các lệnh thường dùng khi giải nguyên Contest trên CMOJ.

---

## 📋 Contest Flow (Copy-Paste Ready)

### Full workflow (từ A-Z)

```bash
# 1. Mở contest page
agent-browser open "https://laptrinh.codemath.vn/contest/SLUG" && agent-browser wait --load networkidle

# 2. Snapshot verify
agent-browser snapshot -i

# 3. Extract problem slugs (eval đơn giản)
agent-browser eval 'const links = document.querySelectorAll("a[href*=\"/problem/\"]"); const results = []; links.forEach(l => { const h = l.getAttribute("href"); if (h && h.includes("/problem/")) { const s = h.split("/problem/")[1].split("/")[0]; const n = l.textContent.trim(); if (s && !results.some(r => r.slug === s)) results.push({slug: s, name: n}); } }); JSON.stringify(results)'

# 4. Check AC status cho từng slug (optional)
curl "defuddle.md/https://laptrinh.codemath.vn/submissions/?problem=SLUG&user=USERNAME"

# 5. Loop qua từng bài (Flow A)
# Xem quick-commands.md cho Flow A commands
```

---

## 🔧 Debug Commands

### Check contest loaded

```bash
# Get contest title
agent-browser eval 'document.querySelector("h2")?.textContent || document.querySelector("h1")?.textContent'

# Get contest status (over/active)
agent-browser eval 'document.body.textContent.includes("Contest is over") ? "OVER" : "ACTIVE"'
```

### Verify slugs extracted

```bash
# Count problems
agent-browser eval 'document.querySelectorAll("a[href*=\"/problem/\"]').length'

# Get first problem name
agent-browser eval 'document.querySelector("a[href*=\"/problem/\"]")?.textContent'
```

### Check AC status

```bash
# Check if user has AC submission for problem
agent-browser eval 'document.body.textContent.includes("Accepted") ? "AC" : "NOT_AC"'
```

---

## 📊 Progress Tracking Templates

### Template 1: Start contest

```
🚀 Bắt đầu giải Contest: <contest-name>
📊 Phát hiện: <N> bài

Danh sách bài:
┌─────┬─────────────────────────────────────┬────────────┐
│  #  │  Tên bài                            │  Slug      │
├─────┼─────────────────────────────────────┼────────────┤
│  1  │  <name-1>                           │  <slug-1>  │
│  2  │  <name-2>                           │  <slug-2>  │
│ ... │  ...                                │  ...       │
└─────┴─────────────────────────────────────┴────────────┘

✅ Bài đã AC: <slugs> (sẽ skip)
⏳ Sẽ giải: <M> bài

Bạn có muốn bắt đầu không? (yes/no)
```

### Template 2: Processing

```
⏳ Đang xử lý: [<i>/<N>] <problem-name> (<slug>)
├─ 📝 Đọc đề: ✅
├─ 💻 Sinh code: ✅ (<language>, <lines> dòng)
├─ 🧪 Test local: ✅ (sample: <expected> → <actual>)
├─ 📤 Submit: ❔ Chờ user confirm...
│
└─ Kết quả: ⏳ Pending...
```

### Template 3: After each problem

```
✅ <slug>: <name> - AC (1.000/1.000) - <time>s
❌ <slug>: <name> - WA (0.500/1.000) - Cần retry
⏭️ <slug>: <name> - SKIPPED (đã AC từ trước)
⏳ <slug>: <name> - Đang xử lý...
```

### Template 4: Contest complete

```
┌─────────────────────────────────────────────────────────────┐
│  🏁 HOÀN THÀNH CONTEST!                                     │
├─────────────────────────────────────────────────────────────┤
│  📊 Tổng kết:                                               │
│  - Tổng số bài: <N>                                         │
│  - Đã AC: <X> ✅                                            │
│  - Thất bại: <Y> ❌                                         │
│  - Skip (đã AC): <Z> ⏭️                                     │
│  - Chưa giải: <W> ⏸️                                       │
│                                                             │
│  🏆 Điểm số: <total-points> / <max-points>                  │
│  ⏱️  Thời gian: <total-time>                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Code Injection cho Contest

### Inject code nhanh (dùng lại từ Flow A)

```bash
# Base64 encode solution
base64 -i /tmp/solution.py

# Inject via eval
agent-browser eval 'const code = atob("BASE64_HERE"); document.querySelector("textarea[name=\"source\"]').value = code; code.length'

# Verify
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'

# Submit
agent-browser click @eSUBMIT
```

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Không extract được slug | `agent-browser eval 'document.querySelectorAll("a").length'` → Check links |
| Contest is over | Vẫn submit được qua `/problem/SLUG/submit` |
| Rate limit | `agent-browser wait 60000` (wait 60s) |
| Element blocked | `agent-browser snapshot -i` → Find overlay |
| Code length = 0 | Re-inject via base64 |

---

## 💡 Pro Tips

1. **Check AC trước khi giải** - Tiết kiệm thời gian, skip bài đã AC
2. **Wait 5s giữa các submit** - Tránh rate limit
3. **Lưu progress** - Ghi chú bài nào AC/WA để retry sau
4. **Priority: Dễ → Khó** - Nếu contest cho phép chọn thứ tự
5. **Snapshot sau mỗi action** - Verify state liên tục

---

## 📞 Emergency Commands

```bash
# Stop current contest
# (Just stop sending commands)

# Restart from beginning
agent-browser open "https://laptrinh.codemath.vn/contest/SLUG"

# Check current progress
curl "defuddle.md/<current_url>"

# Close browser if stuck
agent-browser close
```

---

## 🔗 Related References

| Reference | Purpose |
|-----------|---------|
| [flow-c-contest.md](flow-c-contest.md) | Chi tiết Flow C workflow |
| [flow-a-solve.md](flow-a-solve.md) | Chi tiết Flow A (giải từng bài) |
| [quick-commands.md](quick-commands.md) | Quick commands cho Flow A |
| [troubleshooting.md](troubleshooting.md) | Xử lý lỗi thường gặp |
