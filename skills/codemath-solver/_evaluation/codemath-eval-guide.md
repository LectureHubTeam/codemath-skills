# 🧪 Codemath-Solver Eval Guide

**Skill:** codemath-solver v2.0  
**Date:** 2026-03-12  
**Status:** ✅ Ready to Run

---

## 📊 Overview

| Metric | Value |
|--------|-------|
| **Total Evals** | 5 |
| **Flows Covered** | A, B, C, D |
| **Total Assertions** | 26 |
| **Workspace** | `~/.qwen/skills/codemath-solver/workspace/iteration-1` |

---

## 🎯 Eval Prompts

### Eval #1: solve-specific-problem (Flow A)
```
Giải bài hsgthaibinh2425sodacbiet trên codemath bằng Python
```
**Assertions:** 6 | **Expected:** Code generated, tested, submit with approval

### Eval #2: find-unsolved-problems (Flow B)
```
Tìm 10 bài chưa giải trong HSG Thái Bình, sắp xếp theo độ khó tăng dần
```
**Assertions:** 5 | **Expected:** Filtered list with correct sorting

### Eval #3: retrieve-ac-code (Flow D)
```
Lấy lại code bài hsghanoi2024catinh đã AC trên codemath
```
**Assertions:** 5 | **Expected:** Complete AC source code returned

### Eval #4: solve-contest (Flow C)
```
Giải toàn bộ contest https://laptrinh.codemath.vn/contest/hsg2425quangtri
```
**Assertions:** 5 | **Expected:** All problems solved with progress tracking

### Eval #5: find-easiest-unsolved (Flow B)
```
Bài nào dễ nhất (nhiều người AC nhất) mà mình chưa giải trên codemath?
```
**Assertions:** 5 | **Expected:** Problem with highest AC rate

---

## 🚀 How to Run Evals

### Option 1: Manual Run (Recommended)

```bash
# 1. Open Claude Code
# 2. Trigger skill
/skill codemath-solver

# 3. Paste eval prompt (from above)
# 4. Follow skill execution
# 5. Save outputs to:
#    ~/.qwen/skills/codemath-solver/workspace/iteration-1/eval-X-{name}/with_skill/outputs/
```

### Option 2: Use Task Tool

```bash
task: "codemath-solver"
prompt: "Giải bài hsgthaibinh2425sodacbiet trên codemath bằng Python"
```

---

## 📝 How to Grade

### After Each Eval Run:

1. **Open grading.json:**
   ```
   ~/.qwen/skills/codemath-solver/workspace/iteration-1/eval-X-{name}/with_skill/grading.json
   ```

2. **Fill in assertions:**
   ```json
   {
     "assertions": [
       {"name": "skill_triggered", "text": "...", "passed": true, "evidence": "Skill activated on keywords"}
     ],
     "timing": {
       "duration_seconds": 180,
       "token_usage": 50000
     },
     "feedback": "Skill worked well, but could be faster"
   }
   ```

3. **Set status:**
   ```json
   "status": "graded"
   ```

4. **Save file**

---

## 📊 View Results

### HTML Viewer (Recommended)

Open in browser:
```
file:///Users/macbook_118/.qwen/skills/codemath-solver/workspace/iteration-1/eval-viewer.html
```

**Features:**
- ✅ Interactive grading UI
- ✅ Real-time progress bar
- ✅ Auto-calculate pass rates
- ✅ Save feedback per eval

### Markdown Report

View:
```
~/.qwen/skills/codemath-solver/workspace/iteration-1/benchmark.md
```

**Contains:**
- Summary statistics
- Per-eval breakdown
- Assertion details

---

## 📈 Benchmark Aggregation

After grading all evals:

```bash
python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/aggregate-benchmark.py
```

**Outputs:**
- `benchmark.json` - Machine-readable results
- `benchmark.md` - Human-readable report

---

## ✅ Grading Rubric

| Grade | Criteria |
|-------|----------|
| **PASS** | 100% assertions ✅ |
| **PARTIAL** | 50-99% assertions ✅ |
| **FAIL** | <50% assertions ✅ |

---

## 📋 Files Created

| File | Purpose |
|------|---------|
| `run-all-evals.py` | Setup eval infrastructure |
| `aggregate-benchmark.py` | Aggregate & generate report |
| `generate-eval-viewer.py` | Create HTML viewer |
| `eval-viewer.html` | Interactive grading UI |
| `benchmark.json` | Aggregated results |
| `benchmark.md` | Human-readable report |
| `run_summary.json` | Run metadata |

---

## 🎯 Next Steps

1. **Run eval #1** - Start with solve-specific-problem
2. **Grade immediately** - Fill grading.json after each run
3. **Continue with #2-5** - Run all evals
4. **Aggregate results** - Run aggregate-benchmark.py
5. **Review & iterate** - Improve skill based on failures

---

## 💡 Tips

- **Run in order** - Start with simpler evals (#1, #2) before complex ones (#4)
- **Grade immediately** - Don't wait until all runs are done
- **Save outputs** - Keep code samples, screenshots for reference
- **Note patterns** - Common failures indicate skill issues
- **Time yourself** - Track how long each flow takes

---

## 📞 Support

If issues arise:

1. Check `references/troubleshooting.md` in skill folder
2. Review `cmoj-structure.md` for DOM changes
3. Verify login credentials are valid
4. Check agent-browser is working correctly

---

*Generated: 2026-03-12*  
*Skill Version: 2.0*  
*Workspace: iteration-1*
