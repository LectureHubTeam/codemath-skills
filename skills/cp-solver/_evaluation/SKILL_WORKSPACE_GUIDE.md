# 🏠 Skill Workspaces - File Organization

**Date:** 2026-03-12  
**Status:** ✅ Complete

---

## 📁 Workspace Structure

### Codemath-Solver
```
~/.qwen/skills/codemath-solver/
├── SKILL.md (v2.1)
├── evals/
│   └── evals.json
├── references/ (12 files)
├── templates/
├── workspace/
│   └── iteration-1/
│       ├── eval-1-solve-specific-problem/
│       ├── eval-2-find-unsolved-problems/
│       ├── eval-3-retrieve-ac-code/
│       ├── eval-4-solve-contest/
│       ├── eval-5-find-easiest-unsolved/
│       ├── benchmark.json
│       ├── benchmark.md
│       └── eval-viewer.html
└── _evaluation/ ← All evaluation scripts & docs
    ├── README.md
    ├── codemath-evals.json
    ├── FINAL_EVAL_REPORT.md
    ├── GRADING_GUIDE.md
    ├── aggregate-benchmark.py
    ├── quick-grading.html
    └── [other scripts...]
```

### CP-Solver
```
~/.qwen/skills/cp-solver/
├── SKILL.md (v1.0)
├── evals/
│   └── evals.json
├── references/ (13 files)
├── templates/
├── examples/
├── workspace/
│   └── iteration-1/
└── _evaluation/ ← All evaluation scripts & docs
    ├── README.md
    ├── cp-solver-evals.json
    ├── CP_SOLVER_ANALYSIS.md
    ├── CP_SOLVER_COMPARISON.md
    ├── aggregate-benchmark.py
    ├── quick-grading.html
    └── [other scripts...]
```

---

## 📊 Files Moved

### To Codemath-Solver/_evaluation (17 files)

| File | Purpose |
|------|---------|
| `README.md` | Workspace overview |
| `codemath-evals.json` | 5 test cases |
| `FINAL_EVAL_REPORT.md` | Complete evaluation report |
| `EVAL_CAMPAIGN_SUMMARY.md` | Campaign overview |
| `GRADING_GUIDE.md` | Grading instructions |
| `codemath-refactor-summary.md` | Refactoring summary |
| `codemath-eval-guide.md` | Detailed eval guide |
| `eval-1-run.md` | Eval #1 documentation |
| `run-all-evals.py` | Eval setup script |
| `move-grading-files.py` | File management |
| `input-grading.py` | Interactive grading |
| `analyze-and-improve.py` | Skill analyzer |
| `aggregate-benchmark.py` | Benchmark aggregation |
| `generate-eval-viewer.py` | HTML viewer generator |
| `quick-grading.html` | Grading UI |
| `fix-flow-c.py` | Flow C improvement |

### To CP-Solver/_evaluation (6 files)

| File | Purpose |
|------|---------|
| `README.md` | Workspace overview |
| `cp-solver-evals.json` | 6 test cases |
| `CP_SOLVER_ANALYSIS.md` | Evaluation plan |
| `CP_SOLVER_COMPARISON.md` | vs codemath-solver |
| `refactor-cp-solver.py` | Refactoring script |
| `aggregate-benchmark.py` | Shared script |
| `generate-eval-viewer.py` | Shared script |

---

## 🎯 Workspace Organization Principles

### 1. **Skill Code in `~/.qwen/skills/{skill-name}/`**
- `SKILL.md` - Main skill definition
- `references/` - Detailed documentation
- `templates/` - Code templates
- `examples/` - Example solutions

### 2. **Eval Workspace in `~/.qwen/skills/{skill-name}/workspace/`**
- `iteration-1/` - Current eval run
- `iteration-2/` - Next iteration (if needed)
- Each iteration contains:
  - `eval-{id}-{name}/` - Individual eval folders
  - `benchmark.json` - Aggregated results
  - `benchmark.md` - Human-readable report

### 3. **Evaluation Docs in `~/.qwen/skills/{skill-name}/_evaluation/`**
- All scripts (`.py`)
- All documentation (`.md`)
- All HTML tools
- All eval JSON files

### 4. **Project Docs in `/Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/`**
- Only high-level summaries
- Meeting notes
- Planning documents
- **NO skill-specific files**

---

## ✅ Benefits

### Before ❌
```
Project folder:
- codemath-evals.json
- cp-solver-evals.json
- FINAL_EVAL_REPORT.md
- CP_SOLVER_ANALYSIS.md
- [20+ scripts...]
```
**Problems:**
- Files scattered
- Hard to find related files
- Mix of different skills
- Not portable

### After ✅
```
~/.qwen/skills/codemath-solver/_evaluation/
~/.qwen/skills/cp-solver/_evaluation/
```
**Benefits:**
- All related files together
- Easy to find
- Self-contained
- Portable (can copy entire skill)
- Clear separation of concerns

---

## 🚀 Quick Commands

### Codemath-Solver
```bash
# Navigate to workspace
cd ~/.qwen/skills/codemath-solver/_evaluation

# Run benchmark aggregation
python3 aggregate-benchmark.py

# View final report
open ../workspace/iteration-1/benchmark.md

# Open grading UI
open quick-grading.html
```

### CP-Solver
```bash
# Navigate to workspace
cd ~/.qwen/skills/cp-solver/_evaluation

# Run evals
/skill cp-solver

# Aggregate results
python3 aggregate-benchmark.py
```

---

## 📞 File Location Guide

| Need | Go To |
|------|-------|
| **Run codemath evals** | `~/.qwen/skills/codemath-solver/_evaluation/` |
| **View codemath results** | `~/.qwen/skills/codemath-solver/workspace/iteration-1/` |
| **Run cp-solver evals** | `~/.qwen/skills/cp-solver/_evaluation/` |
| **View cp-solver results** | `~/.qwen/skills/cp-solver/workspace/iteration-1/` |
| **Skill definitions** | `~/.qwen/skills/{skill}/SKILL.md` |
| **Reference docs** | `~/.qwen/skills/{skill}/references/` |

---

## 📝 Maintenance

### When Creating New Skill
1. Create `~/.qwen/skills/{skill-name}/`
2. Create `workspace/` folder
3. Create `_evaluation/` folder
4. Keep all eval files in `_evaluation/`
5. Keep all run results in `workspace/iteration-X/`

### When Archiving
1. Zip entire skill folder
2. Move to `~/Archives/skills/{skill-name}-{date}.zip`
3. All context preserved

---

**Status: ✅ All files properly organized**

---

*Generated: 2026-03-12*  
*Skills: codemath-solver v2.1, cp-solver v1.0*
