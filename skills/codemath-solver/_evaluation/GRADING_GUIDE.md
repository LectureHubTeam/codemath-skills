# 🎯 Hướng Dẫn Input Grading & Improve Skill

**Date:** 2026-03-12  
**Status:** Ready to Grade

---

## 📋 Tình Trạng Hiện Tại

- ✅ 5 evals đã được run
- ⏳ Grading results chưa được input
- ⏳ Skill chưa được update dựa trên feedback
- ⏳ Benchmark chưa được aggregate

---

## 🚀 3 Bước Hoàn Thiện

### **Bước 1: Input Grading Results** (5 phút)

#### Option A: Quick Grading (Khuyến nghị)

1. **Mở file:**
   ```
   /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/quick-grading.html
   ```

2. **Click vào file để mở trong browser**

3. **Input kết quả:**
   - ✅ Check assertions đã pass
   - ⏱ Nhập duration (giây)
   - 💾 Nhập token usage
   - 📝 Feedback (optional)

4. **Click "Save Eval"** cho mỗi eval
   - JSON sẽ tự động download
   - Copy vào grading.json tương ứng

5. **Copy grading files:**
   ```bash
   # Sau khi download các grading-*.json files
   cp ~/Downloads/grading-eval-*.json \
      ~/.qwen/skills/codemath-solver/workspace/iteration-1/eval-*/with_skill/grading.json
   ```

#### Option B: Interactive Script

```bash
python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/input-grading.py
```

Script sẽ hỏi:
- Eval nào PASSED/PARTIAL/FAILED
- Assertions nào pass/fail
- Timing & feedback

---

### **Bước 2: Analyze & Improve Skill** (10 phút)

```bash
python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/analyze-and-improve.py
```

Script sẽ:
1. **Phân tích failures** - Tìm patterns
2. **Đề xuất improvements** - Dựa trên failures
3. **Auto-update SKILL.md** - Apply fixes
4. **Show recommendations** - Next steps

---

### **Bước 3: Aggregate Benchmark** (2 phút)

```bash
python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/aggregate-benchmark.py
```

Output:
- `benchmark.json` - Machine-readable
- `benchmark.md` - Human-readable report

---

## 📊 Quick Grading Form

| Eval ID | Prompt | Assertions | Status |
|---------|--------|------------|--------|
| 1 | Giải bài cụ thể | 6 | ⏳ Pending |
| 2 | Tìm bài chưa giải | 5 | ⏳ Pending |
| 3 | Lấy code AC | 5 | ⏳ Pending |
| 4 | Giải contest | 5 | ⏳ Pending |
| 5 | Tìm bài dễ nhất | 5 | ⏳ Pending |

---

## ✅ Checklist

### Grading Input
- [ ] Mở quick-grading.html
- [ ] Input Eval #1 results
- [ ] Input Eval #2 results
- [ ] Input Eval #3 results
- [ ] Input Eval #4 results
- [ ] Input Eval #5 results
- [ ] Copy grading.json files vào workspace

### Skill Improvement
- [ ] Run analyze-and-improve.py
- [ ] Review recommendations
- [ ] Approve changes
- [ ] Update version metadata

### Benchmark
- [ ] Run aggregate-benchmark.py
- [ ] Review benchmark.md
- [ ] Share results với team

---

## 📁 Files Cần Dùng

| File | Purpose |
|------|---------|
| `quick-grading.html` | Interactive grading UI |
| `input-grading.py` | CLI grading input |
| `analyze-and-improve.py` | Skill analyzer |
| `aggregate-benchmark.py` | Benchmark aggregation |

---

## 🎯 Kết Quả Cuối Cùng

Sau khi hoàn thành 3 bước:

1. **Grading results** được lưu vào workspace
2. **Skill** được improve dựa trên eval feedback
3. **Benchmark report** được generate
4. **HTML viewer** hiển thị kết quả

---

## 💡 Tips

- **Grade ngay sau khi run** - Đừng để quên
- **Be honest** - Failures giúp improve skill tốt hơn
- **Detailed feedback** - Giúp phân tích patterns dễ hơn
- **Save timing** - Để measure performance improvements

---

## 📞 Need Help?

Nếu có vấn đề:

1. Check grading files format đúng JSON
2. Verify paths đúng workspace structure
3. Run scripts với Python 3.6+

---

*Ready to start? Open `quick-grading.html` và begin!*
