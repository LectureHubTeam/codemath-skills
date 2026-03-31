# CP Teacher - Lesson Generator

## 🎯 Overview

Bộ skill biến một bài toán Competitive Programming đã AC thành **bài giảng chi tiết** nhằm mục đích giảng dạy và học tập.

**Khác biệt so với codemath-solver và cp-solver:**
- codemath-solver → Submit AC
- cp-solver → Phân tích algorithm
- **cp-teacher** → **Biến solution thành bài giảng để DẠY HỌC**

---

## 📁 Structure

```
cp-teacher/
├── SKILL.md                          # Main skill description
├── README.md                         # This file
├── references/
│   ├── 01-manual-walkthrough.md      # Hướng dẫn Manual Walkthrough
│   ├── 02-code-explanation.md        # Hướng dẫn Code Explanation
│   ├── 03-theory-extension-decision.md # Khi nào sinh Theory
│   └── templates/
│       └── lesson-template.md        # Template markdown
├── examples/
│   └── sap-xep-chieu-lesson.md       # Example lesson
├── outputs/                          # Generated lessons
└── scripts/                          # Automation scripts
    └── export_lesson.py              # Convert MD to PDF/Word/LaTeX
```

---

## 🚀 Quick Start

### Input
```
User: Biến bài này thành bài giảng
URL: https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
```

### Output Structure
```markdown
# Bài giảng: [Tên bài]

## 1. Phân tích bài toán
...

## 2. Solution Breakdown ⭐ (TRỌNG TÂM)
   2.1. Mô phỏng thủ công (KHÔNG DÙNG CODE)
   2.2. Giải thích code (mapping với manual)
   2.3. Tại sao AC?

## 3. Bài học tổng quát
...

## 4. Chuyên đề: [Tên] (OPTIONAL)
...

## 5. Bài tập tương tự
...
```

---

## 📋 Chi tiết từng Module

### Module 1: Problem Analysis
- Tóm tắt đề
- Input/Output/Constraints
- Nhận diện dạng bài

### Module 2: Solution Breakdown ⭐
**QUAN TRỌNG NHẤT - Chiếm 40% độ dài lesson**

#### 2.1. Manual Walkthrough
- Giải thủ công, KHÔNG DÙNG CODE
- Chọn test case cụ thể
- Thể hiện từng bước suy nghĩ
- Rút ra pattern

#### 2.2. Code Explanation
- Map code với manual walkthrough
- Giải thích từng dòng/khối
- Nói "TẠI SAO" chứ không chỉ "CÁI GÌ"

#### 2.3. Why AC?
- Complexity analysis
- Edge cases
- Correctness proof sketch

### Module 3: Key Takeaways
- Kinh nghiệm nhận diện
- Pattern cần nhớ
- Sai lầm thường gặp
- Tips

### Module 4: Theory Extension (OPTIONAL)
**Agent tự quyết định có sinh hay không**

SINH khi:
- Bài thuộc dạng kinh điển
- Có nhiều bài tương tự
- Pattern generalize được

SKIP khi:
- Bài quá đơn giản
- Pattern quá cụ thể
- Lý thuyết quá phức tạp

### Module 5: Practice Problems
- 3-5 bài từ dễ → khó
- Có gợi ý
- Có lời giải chi tiết (trong <details>)

---

## 💡 Best Practices

### Manual Walkthrough
- ✅ LUÔN làm trước khi code
- ✅ Dùng ASCII art / formatting
- ✅ Giải thích "tại sao" cho mỗi bước
- ✅ Rút ra pattern tổng quát

### Code Explanation
- ✅ Reference đến Manual Walkthrough
- ✅ Group code thành khối logic
- ✅ Comment giải thích "tại sao"
- ✅ Include test case trong comment

### Theory Extension
- ✅ Chỉ sinh khi thực sự hữu ích
- ✅ Đừng forced theory vào mọi bài
- ✅ Link đến resources bên ngoài

### Practice Problems
- ✅ Từ dễ → khó
- ✅ Có gợi ý cụ thể
- ✅ Lời giải trong <details>

---

## 📊 Example Output

Xem [examples/sap-xep-chieu-lesson.md](examples/sap-xep-chieu-lesson.md)

---

## 🔧 Usage Examples

### Example 1: Basic Lesson
```
User: Biến bài này thành bài giảng
URL: https://laptrinh.codemath.vn/problem/hsgnamdinh2223sapxepchieu
```

### Example 2: Lesson với focus
```
User: Giảng chi tiết phần solution cho bài này
URL: https://laptrinh.codemath.vn/problem/...
Focus: Manual walkthrough
```

### Example 3: Lesson + Practice
```
User: Tạo lesson và cho em bài tập luyện tập
URL: https://laptrinh.codemath.vn/problem/...
```

---

## 📝 Templates

### Markdown Template
Xem [references/templates/lesson-template.md](references/templates/lesson-template.md)

### Checklist
- [ ] Manual walkthrough trước code
- [ ] Mapping rõ ràng giữa manual và code
- [ ] Giải thích tại sao AC
- [ ] Pattern tổng quát
- [ ] Practice problems từ dễ → khó
- [ ] Theory chỉ khi thực sự cần

---

## 🎓 Learning Path

### Cho người dạy
1. Đọc [01-manual-walkthrough.md](references/01-manual-walkthrough.md)
2. Đọc [02-code-explanation.md](references/02-code-explanation.md)
3. Đọc [03-theory-extension-decision.md](references/03-theory-extension-decision.md)
4. Xem example lesson

### Cho người học
1. Đọc Module 1 để hiểu đề
2. Đọc Module 2.1 để hiểu cách suy nghĩ
3. Đọc Module 2.2 để hiểu code
4. Đọc Module 3 để rút kinh nghiệm
5. Làm Module 5 để luyện tập

---

## 🔗 Related Skills

| Skill | Mục đích |
|-------|----------|
| [codemath-solver](../codemath-solver/SKILL.md) | Submit bài AC |
| [cp-solver](../cp-solver/SKILL.md) | Phân tích algorithm khó |
| **cp-teacher** | **Biến solution thành bài giảng** |

---

## 📊 Metrics

| Metric | Target |
|--------|--------|
| Manual walkthrough quality | 100% lessons có |
| Code explanation clarity | 4.5/5+ rating |
| Theory extension relevance | 80%+ useful |
| Practice problems quality | 3-5 problems per lesson |

---

## 🚀 Roadmap

### Phase 1: Core ✅
- [x] SKILL.md
- [x] Manual Walkthrough guide
- [x] Code Explanation guide
- [x] Theory Extension decision guide
- [x] Example lesson

### Phase 2: Templates (Next)
- [ ] HTML template
- [ ] PDF template
- [ ] Interactive quiz template

### Phase 3: Examples (Next)
- [ ] DP lesson example
- [ ] Graph lesson example
- [ ] String lesson example

---

**Happy Teaching! 🎓**
