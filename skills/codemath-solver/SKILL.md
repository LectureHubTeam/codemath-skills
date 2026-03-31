---
name: codemath-solver
description: Tự động giải và submit bài tập lập trình trên CMOJ (laptrinh.codemath.vn). Hỗ trợ 4 flow chính: (1) Giải bài cụ thể, (2) Tìm & lọc bài chưa giải, (3) Giải nguyên contest, (4) Lấy lại code đã AC. Dùng skill này khi user nhắc đến 'codemath', 'CMOJ', 'laptrinh.codemath.vn', hoặc muốn giải bài, tìm bài, lấy code từ CMOJ.
metadata:
  version: 3.0
  updated-on: 2026-03-12
  tags:
    - competitive-programming
    - codemath
    - cmoj
    - problem-solving
    - automation
  dependencies:
    - agent-browser
    - python3
    - g++
  compatible-with: cp-solver (escalation)
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(python3:*), Bash(g++:*), Bash(node:*)
---

# CodeMath Problem Solver (CMOJ)

Skill tự động giải bài tập trên **CMOJ - CodeMath Online Judge** (https://laptrinh.codemath.vn)

---

## 🏗 4 Flows Chính

### Flow A: Giải bài cụ thể (khi có slug)

> Chi tiết: [references/flow-a-solve.md](references/flow-a-solve.md)
```
Login → Đọc đề → Sinh code → Test local → Submit (cần approve)
```

### Flow B: Tìm & lọc bài chưa giải

> Chi tiết: [references/flow-b-browse.md](references/flow-b-browse.md)
```
Login → Filter/Search → Parse & Lọc unsolved → Trình bày → User chọn → Flow A
```

### Flow C: Giải nguyên Contest

> Chi tiết: [references/flow-c-contest.md](references/flow-c-contest.md)
```
Login → Mở Contest → Parse IDs → For each ID → Gọi Flow A
```

### Flow D: Lấy lại code đã AC

> Chi tiết: [references/flow-d-retrieve-ac.md](references/flow-d-retrieve-ac.md)
```
Login → Vào bài → My submissions → Lọc AC đầu tiên → Copy source
```

---

## 🚀 Cách Dùng

### Flow A - Giải bài
- **Hướng dẫn:** [references/flow-a-solve.md](references/flow-a-solve.md)
```
User: "Giải bài hsgthaibinh2425sodacbiet bằng Python"
→ Agent: Login → Đọc đề → Sinh code → Test → Submit → Check kết quả → Nếu chưa AC thì vào vòng lặp fix cho tới khi AC → Nếu AC thì kết thúc.
```

### Flow B - Tìm bài
- **Hướng dẫn:** [references/flow-b-browse.md](references/flow-b-browse.md)
```
User: "Tìm 10 bài chưa giải trong HSG Thái Bình"
→ Agent: Login → Filter → Parse → Show danh sách
```

### Flow C - Giải contest
- **Hướng dẫn:** [references/flow-c-contest.md](references/flow-c-contest.md)
```
User: "Giải contest https://laptrinh.codemath.vn/contest/hsg2425quangtri"
→ Agent: Login → Parse contests → Loop Flow A
```

### Flow D - Lấy code AC
- **Hướng dẫn:** [references/flow-d-retrieve-ac.md](references/flow-d-retrieve-ac.md)
```
User: "Lấy code bài hsghanoi2024catinh"
→ Agent: Login → Submissions → Filter AC → Copy source
```

---

## ⚠️ Escalation to CP-Solver

**Khi nào cần escalate sang [cp-solver](../cp-solver/SKILL.md):**

| Dấu hiệu | Action |
|----------|--------|
| TLE 2+ lần dù optimize | → `task: cp-solver` |
| Algorithm khó (Segment Tree, Mo's, DP optimization) | → `task: cp-solver` |
| User hỏi sâu ("Tại sao TLE?", "Có cách nào tối ưu?") | → `task: cp-solver` |

**Chi tiết escalation:** Xem [references/escalation.md](references/escalation.md)

---

## 📋 Tham Số

### Flow A
- **Refer:** [references/flow-a-solve.md](references/flow-a-solve.md)
- `problem_slug`: Slug bài (ví dụ: `hsgthaibinh2425sodacbiet`)
- `language`: `PY3` (default), `CPP17`, `CPP20`, `JAVA`, `C`


### Flow B
- **Refer:** [references/flow-b-browse.md](references/flow-b-browse.md)
- `category`: HSG Thái Bình, HSG Hà Nội...
- `order_by`: `code`, `name`, `-points`, `-ac_rate`
- `unsolved_only`: `true` (default)
- `limit`: `20` (default)

### Flow C
- **Refer:** [references/flow-c-contest.md](references/flow-c-contest.md)
- `contest_url`: URL contest
- `language`: Như Flow A
- `auto_submit`: Như Flow A

### Flow D
- **Refer:** [references/flow-d-retrieve-ac.md](references/flow-d-retrieve-ac.md)
- `problem_slug`: Slug bài cần lấy code

**Chi tiết:** Xem [references/parameters.md](references/parameters.md)

---

## 📚 References

Dưới đây là các tài liệu chi tiết. **LUÔN DÙNG công cụ `view_file` để đọc file tương ứng** trước khi thực hiện các yêu cầu của User:

### Core Flows
- [Flow A: Giải bài cụ thể](references/flow-a-solve.md) - Chi tiết từng bước giải bài (Navigate, Đọc đề, Sinh code, Test local và Submit).
- [Flow B: Tìm & Lọc bài](references/flow-b-browse.md) - Kỹ thuật parse table, dùng URL params để lọc category, %AC rate, check bài chưa solved.
- [Flow C: Giải Contest](references/flow-c-contest.md) - Cách lấy danh sách IDs và gọi vòng lặp Flow A.
- [Flow D: Lấy lại code AC](references/flow-d-retrieve-ac.md) - Cách tương tác giao diện Submissions để copy RAW code.

### Deep-Dive & Utilities
- [escalation.md](references/escalation.md) - Tiêu chí và cách delegate qua `cp-solver`.
- [parameters.md](references/parameters.md) - Đặc tả ý nghĩa các tham số cần khai thác từ User.
- [cmoj-structure.md](references/cmoj-structure.md) - Cấu trúc DOM, CSS selector, URL pattern của CMOJ.
- [cp-patterns.md](references/cp-patterns.md) - Mẫu thuật toán tương ứng theo Complexity/Constraints.
- [problem-filtering.md](references/problem-filtering.md) - Chuyên sâu về tìm kiếm, query URL, phân trang của CMOJ.
- [quick-commands.md](references/quick-commands.md) - Snippet lệnh `agent-browser` hay dùng cho Flow A.
- [quick-commands-contest.md](references/quick-commands-contest.md) - Snippet lệnh cho Contest.
- [troubleshooting.md](references/troubleshooting.md) - Cách tự sửa CE/RE/TLE, xử lý CodeMirror Editor, lỗi inject code.

---

## 💡 Tips

1. **Luôn login trước** - indicator solved/unsolved chỉ hiện khi login
2. **Test local trước submit** - tiết kiệm submissions
3. **Dùng URL params** - nhanh hơn interact form
4. **Snapshot sau mỗi action** - verify UI state
5. **Đọc constraints** - quyết định algorithm
6. **Check encoding** - CMOJ hiển thị tiếng Việt
7. **Đọc nội dung web nhanh** - Khi cần đọc nội dung từ trang web hãy sử dụng cách sau:
   ```
   curl defuddle.md/<URL>
   ```


---

## 📊 Exit Criteria

### Flow A ✅ ([flow-a-solve.md](references/flow-a-solve.md))
- [ ] Code test pass với sample input
- [ ] Submit thành công hoặc escalate nếu TLE/WA

### Flow B ✅ ([flow-b-browse.md](references/flow-b-browse.md))
- [ ] Danh sách unsolved problems hiển thị đúng
- [ ] Filter đúng category/sort
- [ ] User chọn được bài

### Flow C ✅ ([flow-c-contest.md](references/flow-c-contest.md))
- [ ] Parse đủ problems trong contest
- [ ] Submit từng bài (có confirm)
- [ ] Báo cáo progress rõ ràng

### Flow D ✅ ([flow-d-retrieve-ac.md](references/flow-d-retrieve-ac.md))
- [ ] Tìm được submission AC đầu tiên
- [ ] Copy được source code
- [ ] Return code cho user

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-03-11 | Refactor: lean SKILL.md, add metadata, evals |
| 1.0 | - | Initial version |

---

*Refactored: 2026-03-11 | Version: 2.0*
