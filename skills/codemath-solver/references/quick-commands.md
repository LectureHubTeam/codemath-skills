# Quick Commands Reference

Quick reference card cho các lệnh thường dùng khi giải bài trên CMOJ.

---

## 📋 Submit Flow (Copy-Paste Ready)

### Full workflow (từ A-Z)

```bash
# 1. Open submit page
agent-browser open "https://laptrinh.codemath.vn/problem/SLUG/submit" && agent-browser wait --load networkidle

# 2. Snapshot to get refs
agent-browser snapshot -i

# 3. Fill code (cách reliable nhất - eval với template literal)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value = `YOUR_CODE_HERE`'

# 4. Verify code đã fill
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'

# 5. Submit
agent-browser click @eSUBMIT && agent-browser wait --load networkidle

# 6. Check result
curl "defuddle.md/<current_url>"
```

---

## 🔧 Debug Commands

### Check code trong editor

```bash
# Check độ dài code (should be > 0)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length'

# Check dòng đầu tiên (verify không bị corrupt)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.split("\n")[0]'

# Check toàn bộ code (first 200 chars)
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.substring(0, 200)'
```

### Force trigger input event

Nếu editor không update sau khi set value:

```bash
agent-browser eval 'const ta = document.querySelector("textarea[name=\"source\"]"); ta.value = ta.value; ta.dispatchEvent(new Event("input", {bubbles: true}))'
```

### Check login status

```bash
agent-browser open https://laptrinh.codemath.vn/ && agent-browser wait --load networkidle
agent-browser snapshot -i
# Tìm: "Hello, username" hoặc link "Đăng xuất"
```

### Verify refs sau navigation

```bash
# LUÔN chạy sau: open, click, wait --load
agent-browser snapshot -i
# Dùng refs MỚI từ snapshot này
```

---

## 📝 Code Injection Templates

### Template 1: Python solution (eval với template literal)

```bash
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value = `import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    # ... your logic here
    print(answer)

if __name__ == "__main__":
    solve()`'
```

### Template 2: C++ solution (eval với template literal)

```bash
agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value = `#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    // ... your logic here
    return 0;
}`'
```

### Template 3: Load từ file (bash script)

```bash
#!/bin/bash
# submit.sh - Submit solution từ file

SLUG=$1
FILE=$2

if [ -z "$SLUG" ] || [ -z "$FILE" ]; then
    echo "Usage: ./submit.sh <problem-slug> <solution-file>"
    exit 1
fi

# Read code from file
CODE=$(cat "$FILE")

# Open submit page
agent-browser open "https://laptrinh.codemath.vn/problem/$SLUG/submit" && agent-browser wait --load networkidle

# Snapshot to get refs
agent-browser snapshot -i

# Inject code
agent-browser eval "document.querySelector('textarea[name=\"source\"]').value = \`$CODE\`"

# Verify
LENGTH=$(agent-browser eval 'document.querySelector("textarea[name=\"source\"]').value.length')
echo "Code length: $LENGTH"

if [ "$LENGTH" -gt 0 ]; then
    echo "✅ Code injected successfully!"
    echo "Click submit manually or run:"
    echo "  agent-browser click @eSUBMIT"
else
    echo "❌ Code injection failed!"
fi
```

---

## 🎯 Quick Navigation URLs

| Action | URL Pattern |
|--------|-------------|
| Problem | `https://laptrinh.codemath.vn/problem/SLUG` |
| Submit | `https://laptrinh.codemath.vn/problem/SLUG/submit` |
| Submissions | `https://laptrinh.codemath.vn/problem/SLUG/submissions` |
| Rank | `https://laptrinh.codemath.vn/problem/SLUG/rank` |
| All submissions | `https://laptrinh.codemath.vn/submissions/?problem=SLUG` |

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| `SyntaxError: invalid syntax` | Dùng `eval` thay vì `fill` |
| Element blocked | `agent-browser snapshot -i` tìm modal close |
| Code length = 0 | Check selector: `textarea[name="source"]` |
| Overlay che | Scroll page: `agent-browser scroll down 100` |
| Need to re-snapshot | Always run `snapshot -i` after navigation |

---

## 💡 Pro Tips

1. **LUÔN re-snapshot** sau `click`, `open`, hoặc bất kỳ action nào làm thay đổi DOM
2. **Verify code length** trước khi submit - nếu = 0 thì code chưa được inject
3. **Dùng eval với template literal** () thay vì `fill` cho code nhiều dòng
4. **Test local trước** - tiết kiệm submissions và tránh rate limit
5. **Lưu session** sau login: `agent-browser state save codemath-auth.json`

---

## 📞 Emergency Commands

Khi mọi thứ bị lỗi:

```bash
# Close browser và restart
agent-browser close

# Clear session và login lại
agent-browser open https://laptrinh.codemath.vn/accounts/logout/
agent-browser open https://laptrinh.codemath.vn/accounts/login/

# Check browser status
agent-browser get title
```
