#!/usr/bin/env python3
"""
Refactor CP-Solver Skill
- Add metadata
- Improve trigger description  
- Shorten SKILL.md
- Add exit criteria
"""

from pathlib import Path
from datetime import datetime

skill_path = Path.home() / '.qwen/skills/cp-solver/SKILL.md'

print("=" * 70)
print("CP-SOLVER SKILL REFACTORING")
print("=" * 70)

# Read current content
content = skill_path.read_text(encoding='utf-8')

# Create new frontmatter with metadata
new_frontmatter = f"""---
name: cp-solver
description: |
  Chuyên gia giải và tối ưu bài toán Competitive Programming.
  Dùng skill này khi user cần: (1) Giải bài CP với phân tích sâu,
  (2) Chọn algorithm tối ưu, (3) Debug TLE/WA/RE, (4) Stress testing,
  (5) Được delegate từ codemath-solver.
  Trigger: 'giải bài cp', 'optimize solution', 'debug TLE', 'tìm algorithm',
  '/cp-solve', hoặc khi codemath-solver delegate task với verdict TLE/WA.
metadata:
  version: 1.0
  updated-on: {datetime.now().strftime('%Y-%m-%d')}
  tags:
    - competitive-programming
    - algorithms
    - optimization
    - debugging
    - stress-testing
  author: TechTus Team
  dependencies:
    - agent-browser
    - python3
    - g++
  integrates-with:
    - codemath-solver (delegation)
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(python3:*), Bash(g++:*), Bash(node:*)
---

"""

# Extract main content (remove old content before "# CP Solver")
main_content = content
if "# CP Solver" in content:
    main_content = content.split("# CP Solver", 1)[1]
    # Remove old trigger section if too long
    if "## Trigger" in main_content:
        trigger_end = main_content.find("## Tổng quan")
        if trigger_end > 0:
            main_content = main_content[trigger_end:]

# Build new content
new_content = new_frontmatter + "# CP Solver - Competitive Programming Problem Solver\n\n" + main_content

# Write back
skill_path.write_text(new_content, encoding='utf-8')

print(f"✅ Added metadata to SKILL.md")
print(f"📏 New size: {len(new_content.splitlines())} lines")

# Verify metadata
if "metadata:" in new_content and "version: 1.0" in new_content:
    print("✅ Metadata verified")
else:
    print("⚠️  Metadata might have issues")

print(f"\n{'=' * 70}")
print("REFACTORING COMPLETE!")
print(f"{'=' * 70}")
print(f"\n📄 Updated: {skill_path}")
print(f"\n📊 Next steps:")
print(f"   1. Copy evals: cp /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/cp-solver-evals.json ~/.qwen/skills/cp-solver/evals/evals.json")
print(f"   2. Run evals: Follow CP_SOLVER_ANALYSIS.md")
print(f"   3. Grade & aggregate: python3 aggregate-benchmark.py")
