#!/usr/bin/env python3
"""
Move grading files from Downloads to skill workspace
"""

import json
import shutil
from pathlib import Path

# Source: Downloads folder
downloads = Path.home() / 'Downloads'

# Destination: Skill workspace
workspace = Path.home() / '.qwen/skills/codemath-solver/workspace/iteration-1'

print("=" * 70)
print("MOVING GRADING FILES TO SKILL WORKSPACE")
print("=" * 70)

# Eval mapping
eval_mapping = {
    1: 'solve-specific-problem',
    2: 'find-unsolved-problems',
    3: 'retrieve-ac-code',
    4: 'solve-contest',
    5: 'find-easiest-unsolved'
}

# Move each file
for eval_id, eval_name in eval_mapping.items():
    source = downloads / f'grading-eval-{eval_id}.json'
    dest_dir = workspace / f'eval-{eval_id}-{eval_name}/with_skill'
    dest = dest_dir / 'grading.json'
    
    if not source.exists():
        print(f"❌ Not found: {source}")
        continue
    
    # Read source
    grading_data = json.loads(source.read_text())
    
    # Ensure correct structure
    grading_data['eval_id'] = eval_id
    grading_data['eval_name'] = eval_name
    
    # Create destination directory if needed
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to destination
    dest.write_text(json.dumps(grading_data, indent=2, ensure_ascii=False))
    
    # Show status
    status = grading_data.get('status', 'unknown')
    passed = sum(1 for a in grading_data.get('assertions', []) if a.get('passed'))
    total = len(grading_data.get('assertions', []))
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    status_icon = '✅' if status == 'passed' else '⚠️' if status == 'partial' else '❌'
    print(f"{status_icon} Eval #{eval_id}: {pass_rate:.0f}% ({passed}/{total}) → {dest}")
    
    # Delete source file after copy
    source.unlink()
    print(f"   🗑 Deleted: {source}")

print(f"\n{'=' * 70}")
print("DONE!")
print(f"{'=' * 70}")
print(f"📂 Files moved to: {workspace}")
print(f"\n📊 Next step: Run benchmark aggregation")
print(f"   python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/aggregate-benchmark.py")
