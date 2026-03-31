#!/usr/bin/env python3
"""
Update Flow C reference to fix contest loop issue
"""

from pathlib import Path

flow_c_path = Path.home() / '.qwen/skills/codemath-solver/references/flow-c-contest.md'

print("=" * 70)
print("UPDATING FLOW C: CONTEST SOLVER")
print("=" * 70)

if not flow_c_path.exists():
    print(f"❌ File not found: {flow_c_path}")
    exit(1)

content = flow_c_path.read_text(encoding='utf-8')

# Add explicit loop instruction
if "For each problem" in content and "Flow A" not in content:
    # Add explicit Flow A call instruction
    old_text = "For each problem:"
    new_text = """For each problem:

**IMPORTANT: Call Flow A for each problem**
```
→ Navigate to problem page
→ Read problem statement  
→ Generate solution code
→ Test locally with sample I/O
→ Ask user for approval
→ Submit code
→ Wait for verdict
→ Move to next problem
```

**Progress Tracking:**
- Keep count of solved/pending problems
- Report progress after each submission
- Handle errors gracefully (don't stop entire contest on 1 failure)"""
    
    content = content.replace(old_text, new_text)
    
    flow_c_path.write_text(content, encoding='utf-8')
    print(f"✅ Updated: {flow_c_path}")
    print("\n📝 Changes:")
    print("  - Added explicit Flow A call instructions")
    print("  - Added progress tracking guidance")
    print("  - Added error handling for contest loop")
else:
    print("ℹ️  File already has Flow A instructions or structure changed")
    print("   Manual review recommended")

# Update SKILL.md version
skill_path = Path.home() / '.qwen/skills/codemath-solver/SKILL.md'
skill_content = skill_path.read_text(encoding='utf-8')

# Update version from 2.0 to 2.1
if 'version: 2.0' in skill_content:
    skill_content = skill_content.replace('version: 2.0', 'version: 2.1')
    skill_content = skill_content.replace('updated-on: 2026-03-11', 'updated-on: 2026-03-12')
    skill_path.write_text(skill_content, encoding='utf-8')
    print(f"\n✅ Updated SKILL.md version: 2.0 → 2.1")

print(f"\n{'=' * 70}")
print("IMPROVEMENT COMPLETE!")
print(f"{'=' * 70}")
print("\n📊 Next: Re-run eval #4 to verify fix")
print("   Then run: python3 aggregate-benchmark.py")
