#!/usr/bin/env python3
"""
Codemath-Solver Eval Runner
Chạy tất cả 5 evals và capture kết quả
"""

import json
from pathlib import Path
from datetime import datetime

# Config
SKILL_NAME = "codemath-solver"
SKILL_VERSION = "2.0"
WORKSPACE = Path('~/.qwen/skills/codemath-solver/workspace/iteration-1').expanduser()
EVALS_FILE = Path('/Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/codemath-evals.json')

# Load evals
evals_data = json.loads(EVALS_FILE.read_text())

print("=" * 70)
print(f"CODEMATH-SOLVER SKILL EVALUATION")
print(f"Version: {SKILL_VERSION} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# Run summary
results = []

for eval_item in evals_data['evals']:
    eval_id = eval_item['id']
    eval_name = eval_item['eval_name']
    prompt = eval_item['prompt']
    expected = eval_item.get('expected_output', '')
    
    eval_dir = WORKSPACE / f'eval-{eval_id}-{eval_name}'
    outputs_dir = eval_dir / 'with_skill' / 'outputs'
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'=' * 70}")
    print(f"EVAL #{eval_id}: {eval_name}")
    print(f"{'=' * 70}")
    print(f"📝 Prompt: {prompt}")
    print(f"🎯 Expected: {expected[:80]}...")
    
    # Create run metadata
    run_metadata = {
        'eval_id': eval_id,
        'eval_name': eval_name,
        'skill_name': SKILL_NAME,
        'skill_version': SKILL_VERSION,
        'prompt': prompt,
        'expected_output': expected,
        'started_at': datetime.now().isoformat(),
        'status': 'ready_to_run',
        'instructions': f"""
Để chạy eval này:

1. Mở Claude Code
2. Chạy: /skill {SKILL_NAME}
3. Paste prompt: {prompt}
4. Follow skill execution
5. Lưu outputs vào: {outputs_dir}

Sau khi chạy xong, update grading.json với kết quả.
"""
    }
    
    # Save run metadata
    metadata_file = outputs_dir / 'run_metadata.json'
    metadata_file.write_text(json.dumps(run_metadata, indent=2, ensure_ascii=False))
    
    # Create grading template
    grading_template = {
        'eval_id': eval_id,
        'eval_name': eval_name,
        'graded_at': None,
        'status': 'pending',
        'assertions': [],
        'timing': {
            'duration_seconds': None,
            'token_usage': None
        },
        'feedback': '',
        'passed': None
    }
    
    # Define assertions based on eval type
    if 'solve-specific' in eval_name:
        grading_template['assertions'] = [
            {'name': 'skill_triggered', 'text': 'Skill triggered correctly on keywords', 'passed': None, 'evidence': ''},
            {'name': 'parameters_extracted', 'text': 'Extracted problem_slug and language correctly', 'passed': None, 'evidence': ''},
            {'name': 'flow_followed', 'text': 'Followed Flow A steps in order', 'passed': None, 'evidence': ''},
            {'name': 'code_generated', 'text': 'Generated valid Python/C++ code', 'passed': None, 'evidence': ''},
            {'name': 'local_tested', 'text': 'Tested code with sample input locally', 'passed': None, 'evidence': ''},
            {'name': 'approval_asked', 'text': 'Asked for user approval before submit', 'passed': None, 'evidence': ''}
        ]
    elif 'find-unsolved' in eval_name or 'easiest-unsolved' in eval_name:
        grading_template['assertions'] = [
            {'name': 'skill_triggered', 'text': 'Skill triggered correctly', 'passed': None, 'evidence': ''},
            {'name': 'filters_applied', 'text': 'Applied correct filters (category, sort)', 'passed': None, 'evidence': ''},
            {'name': 'parsed_correctly', 'text': 'Parsed problem table correctly', 'passed': None, 'evidence': ''},
            {'name': 'unsolved_filtered', 'text': 'Filtered unsolved problems accurately', 'passed': None, 'evidence': ''},
            {'name': 'results_displayed', 'text': 'Displayed results in correct format', 'passed': None, 'evidence': ''}
        ]
    elif 'retrieve-ac' in eval_name:
        grading_template['assertions'] = [
            {'name': 'skill_triggered', 'text': 'Skill triggered correctly', 'passed': None, 'evidence': ''},
            {'name': 'navigated_to_problem', 'text': 'Navigated to problem page', 'passed': None, 'evidence': ''},
            {'name': 'opened_submissions', 'text': 'Opened My submissions page', 'passed': None, 'evidence': ''},
            {'name': 'filtered_ac', 'text': 'Filtered AC submissions correctly', 'passed': None, 'evidence': ''},
            {'name': 'copied_source', 'text': 'Copied and returned complete source code', 'passed': None, 'evidence': ''}
        ]
    elif 'solve-contest' in eval_name:
        grading_template['assertions'] = [
            {'name': 'skill_triggered', 'text': 'Skill triggered correctly', 'passed': None, 'evidence': ''},
            {'name': 'contest_parsed', 'text': 'Parsed contest page and extracted problem IDs', 'passed': None, 'evidence': ''},
            {'name': 'loop_executed', 'text': 'Looped through all problems', 'passed': None, 'evidence': ''},
            {'name': 'flow_a_called', 'text': 'Called Flow A for each problem', 'passed': None, 'evidence': ''},
            {'name': 'progress_reported', 'text': 'Reported progress clearly', 'passed': None, 'evidence': ''}
        ]
    
    # Save grading template
    grading_file = eval_dir / 'with_skill' / 'grading.json'
    grading_file.write_text(json.dumps(grading_template, indent=2, ensure_ascii=False))
    
    results.append({
        'eval_id': eval_id,
        'eval_name': eval_name,
        'status': 'ready',
        'metadata_file': str(metadata_file),
        'grading_file': str(grading_file)
    })
    
    print(f"✅ Metadata: {metadata_file}")
    print(f"✅ Grading template: {grading_file}")

# Save run summary
summary = {
    'skill_name': SKILL_NAME,
    'skill_version': SKILL_VERSION,
    'run_date': datetime.now().isoformat(),
    'total_evals': len(results),
    'evals': results,
    'workspace': str(WORKSPACE)
}

summary_file = WORKSPACE / 'run_summary.json'
summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

print(f"\n{'=' * 70}")
print(f"✅ EVAL SETUP COMPLETE!")
print(f"{'=' * 70}")
print(f"📂 Workspace: {WORKSPACE}")
print(f"📄 Summary: {summary_file}")
print(f"\n📋 Next steps:")
print(f"1. Run each eval manually (see run_metadata.json in each eval folder)")
print(f"2. Fill grading.json after each run")
print(f"3. Run aggregation script when all evals are done")
print(f"\n🚀 To start: Open Claude Code and run '/skill {SKILL_NAME}'")
