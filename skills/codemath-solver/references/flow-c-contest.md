# Flow C: Giải nguyên Contest

Flow này được sử dụng khi User cung cấp một URL Contest cụ thể cần làm trọn bộ. Mặc dù contest có chế độ submit riêng trong `/contest/xxxx/submit...`, ta vẫn có thể lợi dụng URL bài toán `/problem/slug` độc lập lấy từ contest page để giải qua hệ thống Public Judge (giống hệt Flow A).

---

## Pre-flight Checklist ✅

Trước khi bắt đầu flow, đảm bảo các yêu cầu sau:

- [ ] **Đã login**: Kiểm tra bằng `snapshot -i`, thấy username/avatar hiển thị
- [ ] **Contest URL đúng**: Verify trang load thành công, có tiêu đề contest
- [ ] **Đã extract đủ slugs + solved status**: Verify số lượng bài phát hiện được (> 0)
- [ ] **Check contest status**: Nếu "Contest is over" → vẫn submit được qua public judge

---

## C.1. Đọc danh sách bài từ Contest

### Bước 1: Mở trang contest

```bash
# Mở trang contest và wait load
agent-browser open "https://laptrinh.codemath.vn/contest/SLUG" && agent-browser wait --load networkidle

# Snapshot để verify
agent-browser snapshot -i
```

**Verify contest loaded:**
- ✅ Có tiêu đề contest (h2 hoặc heading lớn)
- ✅ Có table danh sách bài (thường có cột: #, Problem, Points)
- ✅ Có link đến các problem (href chứa `/problem/`)

---

### Bước 2: Extract problem slugs + solved status (IMPROVED - Gộp bước 2 & 3)

**⚠️ QUAN TRỌNG:** Bước này gộp việc extract slugs và check solved status để bỏ qua Bước 3.

```bash
# Extract slugs + solved status từ contest page
agent-browser eval 'const rows = document.querySelectorAll("table tbody tr, .contest-problems tr"); const results = []; rows.forEach(r => { const links = r.querySelectorAll("a[href*=\"/problem/\"]"); const solvedIcon = r.querySelector(".solved, .ac-icon, .fa-check, i[style*=\"color: green\"]"); const cells = r.querySelectorAll("td"); let slug = "", name = ""; links.forEach(l => { const h = l.getAttribute("href"); if (h && h.includes("/problem/")) { const s = h.split("/problem/")[1].split("/")[0]; if (s && !slug) { slug = s; name = l.textContent.trim(); } } }); if (slug) { const isSolved = solvedIcon !== null || r.classList.contains("solved"); results.push({slug: slug, name: name, solved: isSolved, link: "https://laptrinh.codemath.vn/problem/" + slug}); } }); JSON.stringify(results)'
```

**Output example:**
```json
[
  {"slug": "24thtbhn1", "name": "MAXAA (THTB Hà Nội Sơ khảo 2024)", "solved": true, "link": "https://laptrinh.codemath.vn/problem/24thtbhn1"},
  {"slug": "24thtbhn2", "name": "Tổng chéo (THTB Sơ khảo HN 2024)", "solved": false, "link": "https://laptrinh.codemath.vn/problem/24thtbhn2"},
  {"slug": "24thtbhn3", "name": "Đoạn con 3 (THTB Sơ khảo HN 2024)", "solved": false, "link": "https://laptrinh.codemath.vn/problem/24thtbhn3"}
]
```

**Giải thích:**
- `solved: true` → Bài đã AC (có icon check màu xanh hoặc class "solved")
- `solved: false` → Bài chưa AC (cần giải)
- `link` → URL trực tiếp đến problem

---

### Bước 3: ~~Check bài đã AC (Optional)~~

**⚠️ BỎ QUA BƯỚC NÀY** - Đã gộp vào Bước 2.

---

### Bước 4: Show danh sách và AUTO-START (KHÔNG CẦN CONFIRM)

```
🚀 Contest: <contest-name>
📊 Phát hiện: <N> bài

Danh sách bài:
┌─────┬──────────────────────────────────────────────────────┬───────────────────────────────────────────────────────┬────────────┐
│  #  │  Tên bài                                             │  Link                                                 │  Status    │
├─────┼──────────────────────────────────────────────────────┼───────────────────────────────────────────────────────┼────────────┤
│  1  │  MAXAA (THTB Hà Nội Sơ khảo 2024)                    │  https://laptrinh.codemath.vn/problem/24thtbhn1       │  ✅ AC     │
│  2  │  Tổng chéo (THTB Sơ khảo HN 2024)                    │  https://laptrinh.codemath.vn/problem/24thtbhn2       │  ⏳ Pending│
│  3  │  Đoạn con 3 (THTB Sơ khảo HN 2024)                   │  https://laptrinh.codemath.vn/problem/24thtbhn3       │  ⏳ Pending│
└─────┴──────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┴────────────┘

✅ Bài đã AC: 1 (24thtbhn1) - Skip
⏳ Sẽ tự động giải: 2 bài (24thtbhn2, 24thtbhn3)

🚀 Bắt đầu giải contest...
```

**⚠️ LƯU Ý:** Flow tự động bắt đầu giải, KHÔNG cần user confirm.

---

## C.2. Giải tuần tự (Vòng lặp)

### Loop Structure

```
┌─────────────────────────────────────────────────────────────┐
│  FOR each problem in problems (thứ tự 1→N):                 │
│                                                             │
│  1. Check solved status (từ Bước 2):                        │
│     - Nếu solved=true → SKIP (đã AC từ trước)               │
│     - Nếu solved=false → Tiếp tục giải                      │
│  2. Gọi Flow A (AUTO-SUBMIT, không confirm):                │
│     - Bước 2: Đọc đề                                        │
│     - Bước 3: Sinh code                                     │
│     - Bước 4: Test local                                    │
│     - Bước 5: Submit (TỰ ĐỘNG)                              │
│  3. Update progress                                         │
│  4. Wait 3s (rate limit)                                    │
│                                                             │
│  END FOR                                                    │
└─────────────────────────────────────────────────────────────┘
```

### Progress Tracking Template

```
🚀 Contest: <contest-name>
📊 Tổng: <N> bài | ✅ AC: <X> | ❌ Fail: <Y> | ⏭️ Skip: <Z>

⏳ Đang xử lý: [<i>/<N>] <problem-name>
├─ 📝 Đọc đề: ✅
├─ 💻 Sinh code: ✅ (Python 3, <lines> dòng)
├─ 🧪 Test local: ✅ (sample: <expected> → <actual>)
├─ 📤 Submit: ✅ TỰ ĐỘNG
│
└─ Kết quả: ⏳ Pending...

───────────────────────────────────────────────────────────────

✅ 24thtbhn1: MAXAA - AC (1.000/1.000) - 0.05s
   Link: https://laptrinh.codemath.vn/problem/24thtbhn1
❌ 24thtbhn2: Tổng chéo - WA (0.500/1.000) - Cần retry
   Link: https://laptrinh.codemath.vn/problem/24thtbhn2
⏭️ 24thtbhn3: Đoạn con 3 - SKIPPED (đã AC từ trước)
   Link: https://laptrinh.codemath.vn/problem/24thtbhn3
⏳ 24thtbhn4: NUM9 - Đang xử lý...
   Link: https://laptrinh.codemath.vn/problem/24thtbhn4
```

### Rate Limit Handling

```bash
# Wait 3 giây giữa các submit để tránh rate limit
agent-browser wait 3000
```

**Khuyến nghị:**
- Tối thiểu **3 giây** giữa các submit liên tiếp
- Nếu gặp rate limit error → wait 60 giây và retry

---

## C.3. Xử lý các trường hợp đặc biệt

### Contest đã kết thúc (Contest is over)

```
⚠️ Contest đã kết thúc!

Tuy nhiên, bạn vẫn có thể:
- Submit qua public judge: `/problem/SLUG/submit`
- Code sẽ được chấm bình thường
- Không tính vào ranking contest

Bạn có muốn tiếp tục không? (yes/no)
```

### Không extract được slug nào

```
❌ Không tìm thấy problem nào trong contest!

Nguyên nhân có thể:
- Contest chưa mở (chưa đến giờ start)
- Contest yêu cầu đăng ký tham gia
- URL contest không đúng

Vui lòng kiểm tra lại!
```

### Bài yêu cầu file I/O

Một số bài trong contest có thể yêu cầu đọc/ghi file:
- Phát hiện qua đề bài (tìm `.INP`, `.OUT`, `freopen`)
- Adjust code theo hướng dẫn trong Flow A (mục "Bài yêu cầu file I/O")

---

## C.4. Tổng kết Contest

Sau khi hoàn thành tất cả bài:

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

## Ví dụ sử dụng đầy đủ

### Ví dụ 1: Giải contest từ URL

```
User: Giải contest https://laptrinh.codemath.vn/contest/24thtbhn
```

**Agent thực hiện:**

1. **Pre-flight:**
   - Open contest page → Verify loaded ✅
   - Check login → Đã login (culi-bot) ✅

2. **Extract slugs:**
   - Eval → Get 4 slugs: `24thtbhn1`, `24thtbhn2`, `24thtbhn3`, `24thtbhn4`

3. **Check AC status:**
   - Check submissions → `24thtbhn1` đã AC → Skip

4. **Show danh sách:**
   ```
   🚀 Contest: Tin học trẻ B - Hà Nội 2023
   📊 Phát hiện: 4 bài
   ✅ Đã AC: 24thtbhn1 (skip)
   ⏳ Sẽ giải: 3 bài

   Bạn có muốn bắt đầu không? (yes/no)
   ```

5. **Loop giải:**
   ```
   ⏳ [1/4] 24thtbhn1: MAXAA → ⏭️ SKIP (đã AC)
   ⏳ [2/4] 24thtbhn2: Tổng chéo → Flow A → ✅ AC
   ⏳ [3/4] 24thtbhn3: Đoạn con 3 → Flow A → ❌ WA (retry...)
   ⏳ [4/4] 24thtbhn4: NUM9 → Flow A → ✅ AC
   ```

6. **Tổng kết:**
   ```
   🏁 HOÀN THÀNH CONTEST!
   📊 Tổng: 4 bài | ✅ AC: 3 | ❌ Fail: 0 | ⏭️ Skip: 1
   🏆 Điểm: 15/20
   ```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `open /contest/SLUG` | Mở trang contest |
| `eval 'querySelectorAll("a[href*=\"/problem/\"]")'` | Extract slugs |
| `open /submissions/?problem=SLUG&user=USERNAME` | Check AC status |
| `wait 5000` | Rate limit delay |
| `open /problem/SLUG/submit` | Submit (Flow A) |

---

## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Không extract được slug | Check selector, snapshot để verify DOM |
| Rate limit error | Wait 60s, retry với delay dài hơn |
| Contest yêu cầu đăng ký | Click "Participate" hoặc "Virtual join" trước |
| Bài đã AC nhưng không detect được | Check submission history thủ công |

---

**See also:**
- [Flow A: Giải bài cụ thể](flow-a-solve.md) - Chi tiết từng bước giải 1 bài
- [Quick Commands](quick-commands-contest.md) - Copy-paste templates cho submit
