# Flow Parameters Reference

## Flow A - Giải Bài Cụ Thể

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem_slug` | string | required | Slug của bài (ví dụ: `hsgthaibinh2425sodacbiet`) |
| `language` | string | `PY3` | Ngôn ngữ submit |
| `auto_submit` | boolean | `false` | Tự động submit hay hỏi user |

### Language Options
- `CPP17` - C++17
- `CPP20` - C++20
- `PY3` - Python 3 (default)
- `JAVA` - Java
- `C` - C

### Example
```
User: "Giải bài abc123 bằng C++"
→ problem_slug: "abc123", language: "CPP17", auto_submit: false
```

---

## Flow B - Tìm & Lọc Bài

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | string | all | Lọc theo nhóm (HSG Thái Bình, HSG Hà Nội...) |
| `order_by` | string | `code` | Sắp xếp theo cột |
| `unsolved_only` | boolean | `true` | Chỉ hiện bài chưa giải |
| `min_points` | number | 0 | Điểm tối thiểu |
| `max_points` | number | ∞ | Điểm tối đa |
| `min_ac_rate` | number | 0 | %AC tối thiểu |
| `max_ac_rate` | number | 100 | %AC tối đa |
| `limit` | number | 20 | Số bài tối đa |

### Order By Options
- `code` - Theo ID (default)
- `name` - Theo tên
- `group` - Theo nhóm
- `-points` - Điểm giảm dần
- `-ac_rate` - %AC giảm dần (bài dễ nhất)
- `-user_count` - Nhiều người giải nhất

### Example
```
User: "Tìm 10 bài dễ nhất chưa giải trong HSG Thái Bình"
→ category: "HSG Thái Bình", order_by: "-ac_rate", limit: 10, unsolved_only: true
```

---

## Flow C - Giải Contest

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `contest_url` | string | required | URL contest |
| `language` | string | `PY3` | Ngôn ngữ submit |
| `auto_submit` | boolean | `false` | Tự động submit |

### Example
```
User: "Giải contest https://laptrinh.codemath.vn/contest/hsg2425quangtri"
→ contest_url: "https://laptrinh.codemath.vn/contest/hsg2425quangtri"
```

---

## Flow D - Lấy Code AC

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `problem_slug` | string | required | Slug bài cần lấy code |

### Example
```
User: "Lấy code bài hsghanoi2024catinh"
→ problem_slug: "hsghanoi2024catinh"
```

---

## URL Patterns

### Problem Page
```
https://laptrinh.codemath.vn/problem/{slug}
```

### Submissions Page
```
https://laptrinh.codemath.vn/problem/{slug}/submissions
https://laptrinh.codemath.vn/problem/{slug}/submissions/{username}
```

### Contest Page
```
https://laptrinh.codemath.vn/contest/{contest_id}
```

### Filter URL Pattern
```
?category={category}
&order_by={order}
&unsolved_only={true|false}
&min_points={n}
&max_points={n}
&min_ac_rate={n}
&max_ac_rate={n}
&limit={n}
```

---

*Reference: parameters.md | Version: 2.0*
