# Flow B: Tìm & Lọc bài chưa giải

### Tổng quan

Flow này cho phép user tìm kiếm, lọc, và sắp xếp danh sách bài tập trên CMOJ. Đặc biệt hữu ích để:
- Tìm bài **chưa giải** trong một category cụ thể
- Lọc bài theo **mức điểm** (dễ → khó)
- Tìm bài có **%AC cao** (bài dễ, phù hợp để luyện tập)
- Tìm bài có **#AC thấp** (bài khó, ít người giải)
- Tìm bài theo **ID/slug** cụ thể

### Yêu cầu tiên quyết

**⚠️ BẮT BUỘC phải login** để thấy indicator bài đã giải/chưa giải. Nếu chưa login → chỉ thấy danh sách bài nhưng không phân biệt được solved/unsolved.

---

### ⚠️ Lưu ý quan trọng từ thực tế

**1. defuddle.md KHÔNG respect filter URL parameters:**
```bash
# ❌ KHÔNG DÙNG - defuddle trả về TẤT CẢ bài, không filter solved=0
curl "https://defuddle.md/https://laptrinh.codemath.vn/problems/?solved=0"
```

**2. Cách ĐÚNG để filter bài chưa giải:**
- Dùng **browser automation** để click checkbox "Hide solved problems"
- Verify checkbox có `[checked]` trong snapshot
- Sort bằng cách click vào column header (Points, %AC, etc.)

**3. Icons trong snapshot:**
- `` = Đã giải (solved)
- `` = Chưa giải (unsolved)

---

### B.1. CMOJ URL Query Parameters

Trang `/problems/` hỗ trợ filter/sort qua URL query parameters:

| Parameter | Ý nghĩa | Ví dụ |
|-----------|----------|-------|
| `page` | Phân trang (mỗi trang ~50 bài) | `?page=2` |
| `order` | Sắp xếp (prefix `-` = giảm dần) | `?order=-points` |
| `category` | Lọc theo nhóm bài (URL-encoded) | `?category=HSG+Thái+Bình` |
| `search` | Tìm kiếm theo tên/ID bài | `?search=số+đặc+biệt` |

**Order values:**

| Cột | Tăng dần (↑) | Giảm dần (↓) | Mô tả |
|-----|--------------|---------------|-------|
| ID | `order=code` | `order=-code` | Mã bài (slug) |
| Bài | `order=name` | `order=-name` | Tên bài tập |
| Nhóm | `order=group` | `order=-group` | Nhóm/Category |
| Điểm | `order=points` | `order=-points` | Điểm bài |
| % AC | `order=ac_rate` | `order=-ac_rate` | Tỉ lệ Accepted |
| # AC | `order=user_count` | `order=-user_count` | Số người đã AC |

---

### B.2. Navigate & Filter bằng Browser (RECOMMENDED)

**⚠️ QUAN TRỌNG:** Dùng browser automation thay vì defuddle để filter chính xác.

#### Bước 1: Mở trang problems

```bash
agent-browser open "https://laptrinh.codemath.vn/problems/" && agent-browser wait --load networkidle
agent-browser snapshot -i
```

#### Bước 2: Click "Hide solved problems" checkbox

Từ snapshot, tìm ref của checkbox "Hide solved problems":

```bash
# Click checkbox (thường là ref nhỏ, ví dụ e18)
agent-browser click @eX && agent-browser wait --load networkidle

# Verify checkbox đã checked
agent-browser snapshot -i
# Tìm: checkbox "Hide solved problems" [ref=eX] [checked]
```

#### Bước 3: Sort theo column mong muốn

```bash
# Click vào column header để sort
# Click 1 lần = giảm dần (▾), click 2 lần = tăng dần (▴)
agent-browser click @eY && agent-browser wait --load networkidle

# Sort tăng dần (points thấp → cao)
agent-browser click @eY && agent-browser wait --load networkidle
agent-browser snapshot -i
# Tìm: link "Points ▴" [ref=eY]
```

#### Bước 4: Parse danh sách từ snapshot

Từ snapshot, extract các bài có icon `` (chưa giải):

```
- link "" [ref=e42]          ← unsolved indicator
- link "sapxep" [ref=e43]      ← slug
- link "Sắp xếp" [ref=e44]     ← name
- link "7" [ref=e45]           ← #AC count
```

**Danh sách 10 bài chưa giải đầu tiên** (sort theo points tăng dần):

| # | Slug | Tên bài | #AC |
|---|------|---------|-----|
| 1 | `sapxep` | Sắp xếp | 7 |
| 2 | `24hcm1` | robot | 0 |
| 3 | `nsochan` | N số chẵn | 199 |
| 4 | `xh_mtr22` | Xếp hàng | 35 |
| 5 | `demnet_tk23` | Đếm nét | 91 |
| 6 | `vt_ts24` | Vận tốc | 104 |
| 7 | `khoaso` | Khóa số | 12 |
| 8 | `xepdiem_str24` | Xếp diêm | 36 |
| 9 | `chiphi` | Chi phí | 21 |
| 10 | `kbb2` | Kéo búa bao 2 | 24 |

### B.3. Quick Commands Reference

```bash
# 1. Open problems page
agent-browser open "https://laptrinh.codemath.vn/problems/" && agent-browser wait --load networkidle

# 2. Check login status
agent-browser snapshot -i
# Look for: "Hello, <username>." = logged in

# 3. Click "Hide solved problems" checkbox
agent-browser snapshot -i  # Find checkbox ref (e.g., e18)
agent-browser click @e18 && agent-browser wait --load networkidle

# 4. Verify checkbox is checked
agent-browser snapshot -i
# Look for: checkbox "Hide solved problems" [ref=e18] [checked]

# 5. Sort by Points (ascending = easy first)
agent-browser snapshot -i  # Find Points column ref (e.g., e38)
agent-browser click @e38 && agent-browser wait --load networkidle  # First click = descending
agent-browser click @e38 && agent-browser wait --load networkidle  # Second click = ascending
agent-browser snapshot -i
# Look for: link "Points ▴" [ref=e38]

# 6. Extract unsolved problems from snapshot
# Look for entries with icon "" (unsolved)
# Format: link "" [ref=eX] followed by slug and name links
```

---

### B.4. Troubleshooting

| Issue | Solution |
|-------|----------|
| defuddle shows all problems | **Expected** - defuddle doesn't respect URL filters. Use browser automation instead. |
| Checkbox not clicking | Check ref from snapshot. May need to scroll or close overlays first. |
| Sort not working | Click twice: 1st = descending (▾), 2nd = ascending (▴). Verify with snapshot. |
| Can't tell solved/unsolved | Look for icons: `` = solved, `` = unsolved in snapshot. |
| Need specific category | Use browser filter dropdown OR check user's solved submissions list. |

---

### B.5. Chuyển từ Browse → Solve

Khi user chọn bài từ danh sách:
1. Lấy slug từ bài được chọn (từ snapshot hoặc user input)
2. Chuyển sang **Flow A** (Giải bài) với slug đó
3. Giữ nguyên các tham số khác (language, auto_submit)

**Ví dụ:**
```
User: "Giải bài số 1"
→ Agent: Lấy slug "sapxep" từ danh sách đã hiển thị
→ Agent: Chuyển sang Flow A với problem_slug="sapxep"
```

---