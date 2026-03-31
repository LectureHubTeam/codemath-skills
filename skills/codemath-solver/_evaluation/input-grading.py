#!/usr/bin/env python3
"""
Interactive Grading Script for Codemath-Solver Evals
Giúp input grading results dễ dàng
"""

import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path('~/.qwen/skills/codemath-solver/workspace/iteration-1').expanduser()

print("=" * 70)
print("CODING-SOLVER EVAL GRADING")
print("=" * 70)
print("\nAnh đã run cả 5 evals đúng không?")
print("Giờ em sẽ giúp anh input grading results.\n")

# Eval summaries
evals = [
    {
        'id': 1,
        'name': 'solve-specific-problem',
        'prompt': 'Giải bài hsgthaibinh2425sodacbiet trên codemath bằng Python',
        'flow': 'A'
    },
    {
        'id': 2,
        'name': 'find-unsolved-problems',
        'prompt': 'Tìm 10 bài chưa giải trong HSG Thái Bình',
        'flow': 'B'
    },
    {
        'id': 3,
        'name': 'retrieve-ac-code',
        'prompt': 'Lấy lại code bài hsghanoi2024catinh đã AC',
        'flow': 'D'
    },
    {
        'id': 4,
        'name': 'solve-contest',
        'prompt': 'Giải toàn bộ contest',
        'flow': 'C'
    },
    {
        'id': 5,
        'name': 'find-easiest-unsolved',
        'prompt': 'Bài nào dễ nhất chưa giải',
        'flow': 'B'
    }
]

# Show eval summary
print("\n📋 EVAL SUMMARY:")
print("-" * 70)
for e in evals:
    print(f"  #{e['id']}: {e['name']} (Flow {e['flow']})")
print("-" * 70)

# Ask for overall results
print("\n❓ Kết quả tổng quan:")
print("  - Eval nào PASSED (100% assertions)?")
print("  - Eval nào PARTIAL (50-99%)?")
print("  - Eval nào FAILED (<50%)?")
print("\nAnh có thể liệt kê theo format:")
print("  PASSED: 1, 3")
print("  PARTIAL: 2, 5")
print("  FAILED: 4")

passed_input = input("\n✅ PASSED (eval IDs, comma-separated): ").strip()
partial_input = input("⚠️  PARTIAL (eval IDs, comma-separated): ").strip()
failed_input = input("❌ FAILED (eval IDs, comma-separated): ").strip()

passed_ids = [int(x.strip()) for x in passed_input.split(',') if x.strip()]
partial_ids = [int(x.strip()) for x in partial_input.split(',') if x.strip()]
failed_ids = [int(x.strip()) for x in failed_input.split(',') if x.strip()]

# Process each eval
for eval_item in evals:
    eval_id = eval_item['id']
    eval_name = eval_item['name']
    
    grading_file = WORKSPACE / f'eval-{eval_id}-{eval_name}/with_skill/grading.json'
    
    if not grading_file.exists():
        print(f"\n⚠️  Skipping #{eval_id}: Grading file not found")
        continue
    
    # Load current grading
    grading = json.loads(grading_file.read_text())
    
    # Determine status
    if eval_id in passed_ids:
        status = 'passed'
        pass_rate = 100
    elif eval_id in partial_ids:
        status = 'partial'
        pass_rate = 70  # Default for partial
    elif eval_id in failed_ids:
        status = 'failed'
        pass_rate = 30  # Default for failed
    else:
        status = 'pending'
        pass_rate = None
    
    print(f"\n{'=' * 70}")
    print(f"EVAL #{eval_id}: {eval_name}")
    print(f"{'=' * 70}")
    
    if status != 'pending':
        print(f"Status: {status.upper()}")
        
        # Update assertions based on status
        if status == 'passed':
            for assertion in grading['assertions']:
                assertion['passed'] = True
                if not assertion.get('evidence'):
                    assertion['evidence'] = 'Verified during eval run'
        elif status == 'partial':
            # Ask which assertions passed
            print("\nAssertions:")
            for i, assertion in enumerate(grading['assertions']):
                response = input(f"  {i+1}. {assertion['name']} - Pass? (y/n/skip): ").strip().lower()
                if response == 'y':
                    assertion['passed'] = True
                    assertion['evidence'] = input("      Evidence: ").strip() or 'Verified'
                elif response == 'n':
                    assertion['passed'] = False
                    assertion['evidence'] = input("      Why failed: ").strip() or 'Did not meet criteria'
                # skip keeps it null
        else:  # failed
            for assertion in grading['assertions']:
                assertion['passed'] = False
                if not assertion.get('evidence'):
                    assertion['evidence'] = 'Failed during eval run'
        
        # Calculate actual pass rate
        total = len(grading['assertions'])
        passed_count = sum(1 for a in grading['assertions'] if a.get('passed') == True)
        if total > 0:
            pass_rate = (passed_count / total) * 100
        
        # Timing
        print("\nTiming:")
        duration = input("  Duration (seconds): ").strip()
        tokens = input("  Token usage: ").strip()
        
        if duration:
            grading['timing']['duration_seconds'] = float(duration)
        if tokens:
            grading['timing']['token_usage'] = int(tokens)
        
        # Feedback
        feedback = input("\nFeedback (optional): ").strip()
        grading['feedback'] = feedback
        
        # Update metadata
        grading['graded_at'] = datetime.now().isoformat()
        grading['status'] = 'graded'
        grading['passed'] = pass_rate >= 100
        
        # Save
        grading_file.write_text(json.dumps(grading, indent=2, ensure_ascii=False))
        print(f"\n✅ Saved: {passed_count}/{total} assertions ({pass_rate:.0f}%)")
    else:
        print("Status: PENDING - No update")

print(f"\n{'=' * 70}")
print("GRADING COMPLETE!")
print(f"{'=' * 70}")
print(f"✅ Passed: {len(passed_ids)}")
print(f"⚠️  Partial: {len(partial_ids)}")
print(f"❌ Failed: {len(failed_ids)}")
print(f"⏳ Pending: {5 - len(passed_ids) - len(partial_ids) - len(failed_ids)}")

print("\n📊 Next step: Run benchmark aggregation")
print(f"   python3 /Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/aggregate-benchmark.py")
