# CMOJ Problem Filtering & Search Reference

## URL-Based API

Trang danh sách bài CMOJ hỗ trợ filter và sort qua URL query parameters.

### Base URL
```
https://laptrinh.codemath.vn/problems/
```

### Query Parameters

| Parameter | Values | Description | Ví dụ |
|-----------|--------|-------------|-------|
| `page` | 1, 2, 3... | Phân trang (mỗi trang ~50 bài) | `?page=2` |
| `order` | Xem bảng dưới | Sắp xếp theo cột | `?order=-points` |
| `category` | Tên category (URL-encoded) | Lọc theo nhóm bài | `?category=HSG+Thái+Bình` |
| `search` | Text tìm kiếm | Tìm kiếm bài theo tên/ID | `?search=số+đặc+biệt` |

### Order Values (Sắp xếp)

| Column | Ascending (↑) | Descending (↓) | Description |
|--------|---------------|-----------------|-------------|
| **ID** | `order=code` | `order=-code` | Mã bài (slug) |
| **Bài** (Name) | `order=name` | `order=-name` | Tên bài tập |
| **Nhóm** (Group) | `order=group` | `order=-group` | Nhóm/Category |
| **Điểm** (Points) | `order=points` | `order=-points` | Điểm của bài |
| **% AC** | `order=ac_rate` | `order=-ac_rate` | Tỉ lệ AC (dễ → khó) |
| **# AC** | `order=user_count` | `order=-user_count` | Số người đã AC |

> **Mặc định**: Prefix `-` = giảm dần (descending). Không prefix = tăng dần (ascending).
> Ví dụ: `?order=-points` = sắp theo điểm giảm dần (bài có điểm cao nhất trước).

### Kết hợp nhiều parameters

Các parameters có thể kết hợp với nhau bằng `&`:

```
# Lọc bài HSG Thái Bình, sắp xếp theo điểm giảm dần
?category=HSG+Thái+Bình&order=-points

# Tìm bài có từ "số", sắp xếp theo %AC giảm dần
?search=số&order=-ac_rate

# Lọc category + phân trang
?category=HSG+Hà+Nội&page=2

# Tìm kiếm + sắp xếp + phân trang
?search=dãy&order=-user_count&page=1
```

## Table Structure (Bảng danh sách bài)

Mỗi row trong bảng chứa các cột:

| Cột | Nội dung | Element thường gặp |
|-----|----------|--------------------|
| **ID** | Slug/mã bài (link tới `/problem/<slug>`) | `<a href="/problem/slug">slug</a>` |
| **Bài** | Tên bài tập (link tới `/problem/<slug>`) | `<a href="/problem/slug">Tên bài</a>` |
| **Nhóm** | Category/group name | Text hoặc link |
| **Điểm** | Số điểm (number) | Text |
| **% AC** | Tỉ lệ accepted (percentage) | Text |
| **# AC** | Số người đã AC (link tới `/problem/<slug>/rank/`) | `<a href="/problem/slug/rank/">number</a>` |
| **Solved** ✓ | Indicator đã giải (chỉ hiện khi login) | Icon/checkmark hoặc class CSS |

### Solved Indicator (Bài đã giải)

**⚠️ Quan trọng**: Indicator "đã giải" chỉ hiển thị khi user **đã login**. Thường biểu hiện bằng:
- ✅ Icon checkmark (tick xanh) bên cạnh tên bài
- CSS class như `.solved`, `.ac-icon` trên row hoặc cell
- Hoặc cột ẩn hiển thị trạng thái solve

Cách detect trong snapshot:
```bash
# Sau khi login, navigate tới problem list
agent-browser open "https://laptrinh.codemath.vn/problems/" && agent-browser wait --load networkidle
agent-browser snapshot -i

# Tìm visual indicators trong snapshot
# Bài đã solved thường có: tick icon, green color, hoặc class "solved"
```

Cách detect bằng JavaScript:
```bash
agent-browser eval --stdin <<'EVALEOF'
(function() {
    // Tìm tất cả rows trong bảng problem
    const rows = document.querySelectorAll('table tbody tr, .problem-list tr, #problem-table tr');
    const problems = [];
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 2) {
            const link = row.querySelector('a[href*="/problem/"]');
            const slug = link ? link.getAttribute('href').match(/\/problem\/([^/]+)/)?.[1] : null;
            const name = cells[1] ? cells[1].textContent.trim() : '';
            // Detect solved: tìm icon, class, hoặc element indicator
            const isSolved = row.classList.contains('solved') || 
                           row.querySelector('.solved-icon, .ac-icon, .tick, i.fa-check') !== null ||
                           row.querySelector('[title*="Solved"], [title*="AC"]') !== null;
            if (slug) {
                problems.push({ slug, name, solved: isSolved });
            }
        }
    });
    return JSON.stringify(problems, null, 2);
})()
EVALEOF
```

## Search Form Structure

Trang problems có form tìm kiếm gồm:
- **Text input**: Ô nhập từ khóa tìm kiếm
- **Category dropdown/select**: Dropdown chọn nhóm bài (nếu có)
- **Button "Tìm"**: Nút submit tìm kiếm
- **Button "Ngẫu nhiên"**: Chọn bài ngẫu nhiên

### Tương tác với Search Form qua agent-browser

```bash
# Bước 1: Mở trang problems
agent-browser open "https://laptrinh.codemath.vn/problems/" && agent-browser wait --load networkidle

# Bước 2: Snapshot để tìm form elements
agent-browser snapshot -i
# Sẽ thấy các refs: @eX cho input search, @eY cho category select, @eZ cho nút Tìm

# Bước 3a: Tìm theo keyword
agent-browser fill @eSEARCH "số đặc biệt"
agent-browser click @eTIM              # Click button "Tìm"
agent-browser wait --load networkidle
agent-browser snapshot -i              # Xem kết quả

# Bước 3b: Lọc theo category  
agent-browser select @eCATEGORY "HSG Thái Bình"    # Select category
agent-browser click @eTIM
agent-browser wait --load networkidle
agent-browser snapshot -i

# Bước 3c: Sắp xếp theo cột
agent-browser click @eDIEM            # Click header "Điểm" để sort
agent-browser wait --load networkidle
agent-browser snapshot -i
```

### Tương tác trực tiếp qua URL (nhanh hơn)

```bash
# Không cần interact với form, navigate trực tiếp
agent-browser open "https://laptrinh.codemath.vn/problems/?category=HSG+Thái+Bình&order=-points" && agent-browser wait --load networkidle
agent-browser snapshot -i
```

## Common Categories (Nhóm bài phổ biến)

> **Lưu ý**: Danh sách category có thể thay đổi. Luôn kiểm tra dropdown trên trang thực tế.

Các category thường gặp trên CMOJ:
- HSG Thái Bình
- HSG Hà Nội
- HSG Nghệ An
- HSG Nam Định
- HSG Quảng Ninh
- HSG Vĩnh Phúc
- HSG Quảng Trị
- HSG Kon Tum
- HSG Lào Cai
- HSG Ninh Bình
- HSG An Giang
- HSG Phú Yên
- ICT (các bài thi ICT)
- Cơ bản (Basic problems)

### Lấy danh sách Category đầy đủ

```bash
# Dùng JavaScript để extract tất cả options từ category dropdown
agent-browser eval --stdin <<'EVALEOF'
(function() {
    const select = document.querySelector('select[name="category"], #id_category, select.category-filter');
    if (!select) {
        // Thử tìm trong form
        const allSelects = document.querySelectorAll('select');
        for (const s of allSelects) {
            const options = Array.from(s.options).map(o => ({ value: o.value, text: o.text }));
            if (options.some(o => o.text.includes('HSG') || o.text.includes('Cơ bản'))) {
                return JSON.stringify(options, null, 2);
            }
        }
        return 'No category select found. Available selects: ' + allSelects.length;
    }
    const options = Array.from(select.options).map(o => ({ value: o.value, text: o.text }));
    return JSON.stringify(options, null, 2);
})()
EVALEOF
```

## Pagination

### Structure
- Mỗi trang hiển thị khoảng **50 bài**
- Navigation: « (first) | 1, 2, 3... | » (next)
- URL: `?page=N` (kết hợp được với các params khác)

### Duyệt nhiều trang

```bash
# Trang 1 (mặc định)
agent-browser open "https://laptrinh.codemath.vn/problems/?order=-ac_rate" && agent-browser wait --load networkidle

# Trang 2
agent-browser open "https://laptrinh.codemath.vn/problems/?order=-ac_rate&page=2" && agent-browser wait --load networkidle

# Hoặc click nút pagination trong snapshot
agent-browser snapshot -i
agent-browser click @ePAGE_NEXT    # Click "»" hoặc số trang
```

## Workflow: Tìm bài chưa giải

### Mục tiêu
Tìm bài chưa giải theo các tiêu chí: category, points, %AC, #AC, ID.

### Yêu cầu tiên quyết
- **PHẢI login** để thấy indicator bài đã giải/chưa giải
- Nếu chưa login → chỉ thấy danh sách bài nhưng không biết bài nào đã solved

### Flow chi tiết

```
1. Login (nếu chưa)
   ↓
2. Navigate tới /problems/ với filter mong muốn
   ↓
3. Snapshot → Parse bảng bài tập
   ↓
4. Identify bài chưa giải (không có solved indicator)
   ↓
5. Filter kết quả theo tiêu chí user yêu cầu
   ↓
6. Trình bày danh sách bài chưa giải cho user
   ↓
7. (Tuỳ chọn) User chọn bài → chuyển sang flow solve
```

### Script tham khảo: Extract bài chưa giải

```bash
# Sau khi đã login và navigate tới trang problems
agent-browser eval --stdin <<'EVALEOF'
(function() {
    const results = [];
    const rows = document.querySelectorAll('table tbody tr, .problem-row, tr[data-problem]');
    
    rows.forEach((row, index) => {
        const cells = row.querySelectorAll('td, th');
        if (cells.length < 2) return;
        
        // Extract data từ mỗi row
        const links = row.querySelectorAll('a[href*="/problem/"]');
        const slugLink = links[0];
        if (!slugLink) return;
        
        const slug = slugLink.getAttribute('href').match(/\/problem\/([^/]+)/)?.[1];
        const name = links.length > 1 ? links[1].textContent.trim() : slugLink.textContent.trim();
        
        // Detect solved status
        const isSolved = 
            row.classList.contains('solved') ||
            row.querySelector('.solved-icon, .ac-icon, .fa-check, .glyphicon-ok, [style*="color: green"]') !== null ||
            row.getAttribute('data-solved') === 'true';
        
        // Extract other columns (order may vary)
        const cellTexts = Array.from(cells).map(c => c.textContent.trim());
        
        results.push({
            index: index + 1,
            slug: slug || 'unknown',
            name: name,
            solved: isSolved,
            cells: cellTexts
        });
    });
    
    // Filter only unsolved
    const unsolved = results.filter(r => !r.solved);
    
    return JSON.stringify({
        total: results.length,
        solved: results.filter(r => r.solved).length,
        unsolved: unsolved.length,
        problems: unsolved
    }, null, 2);
})()
EVALEOF
```
