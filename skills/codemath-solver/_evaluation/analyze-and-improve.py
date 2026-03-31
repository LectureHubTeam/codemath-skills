#!/usr/bin/env python3
"""
Update Codemath-Solver Skill Based on Eval Feedback
Phân tích failures và đề xuất improvements
"""

import json
from pathlib import Path

WORKSPACE = Path('~/.qwen/skills/codemath-solver/workspace/iteration-1').expanduser()
SKILL_PATH = Path('~/.qwen/skills/codemath-solver/SKILL.md').expanduser()

print("=" * 70)
print("SKILL IMPROVEMENT ANALYZER")
print("=" * 70)

# Load grading results
eval_results = []

for eval_id in range(1, 6):
    eval_dirs = {
        1: 'solve-specific-problem',
        2: 'find-unsolved-problems',
        3: 'retrieve-ac-code',
        4: 'solve-contest',
        5: 'find-easiest-unsolved'
    }
    
    eval_name = eval_dirs.get(eval_id)
    if not eval_name:
        continue
    
    grading_file = WORKSPACE / f'eval-{eval_id}-{eval_name}/with_skill/grading.json'
    
    if not grading_file.exists():
        print(f"⏳ Eval #{eval_id}: Grading pending")
        continue
    
    grading = json.loads(grading_file.read_text())
    
    # Check if graded (support multiple status formats)
    grading_status = grading.get('status', 'pending')
    if grading_status not in ['graded', 'passed', 'partial', 'failed']:
        print(f"⏳ Eval #{eval_id}: Not graded yet")
        continue
    
    # Analyze results
    total = len(grading['assertions'])
    passed = sum(1 for a in grading['assertions'] if a.get('passed') == True)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    eval_results.append({
        'eval_id': eval_id,
        'eval_name': eval_name,
        'pass_rate': pass_rate,
        'passed': passed,
        'total': total,
        'feedback': grading.get('feedback', ''),
        'assertions': grading['assertions']
    })
    
    status = '✅' if pass_rate >= 100 else '⚠️' if pass_rate >= 50 else '❌'
    print(f"{status} Eval #{eval_id}: {pass_rate:.0f}% ({passed}/{total})")

if not eval_results:
    print("\n⚠️  No graded evals found!")
    print("Please run input-grading.py first")
    exit(1)

# Analyze failure patterns
print(f"\n{'=' * 70}")
print("FAILURE PATTERN ANALYSIS")
print(f"{'=' * 70}")

failure_patterns = {}

for result in eval_results:
    for assertion in result['assertions']:
        if assertion.get('passed') == False:
            assertion_name = assertion['name']
            if assertion_name not in failure_patterns:
                failure_patterns[assertion_name] = {
                    'count': 0,
                    'evals': [],
                    'evidence': []
                }
            failure_patterns[assertion_name]['count'] += 1
            failure_patterns[assertion_name]['evals'].append(result['eval_name'])
            if assertion.get('evidence'):
                failure_patterns[assertion_name]['evidence'].append(assertion['evidence'])

if failure_patterns:
    print("\n🔴 Common Failure Points:")
    for name, data in sorted(failure_patterns.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"\n  {name}:")
        print(f"    - Failed in {data['count']} eval(s): {', '.join(data['evals'])}")
        if data['evidence']:
            print(f"    - Evidence: {data['evidence'][0]}")
else:
    print("\n✅ No common failure patterns found!")
    print("All assertions passed or evals not graded yet")

# Generate improvement recommendations
print(f"\n{'=' * 70}")
print("IMPROVEMENT RECOMMENDATIONS")
print(f"{'=' * 70}")

recommendations = []

# Check for specific patterns
if any('skill_triggered' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'Trigger Description',
        'issue': 'Skill not triggering reliably',
        'fix': 'Make description more explicit with additional keywords'
    })

if any('parameters_extracted' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'Parameter Extraction',
        'issue': 'Parameters not extracted correctly',
        'fix': 'Add clearer parameter definitions in references/parameters.md'
    })

if any('flow_followed' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'Flow Execution',
        'issue': 'Flow steps not followed in order',
        'fix': 'Add clearer step-by-step instructions in flow references'
    })

if any('local_tested' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'Local Testing',
        'issue': 'Code not tested locally before submit',
        'fix': 'Add mandatory local test step in Flow A with sample I/O'
    })

if any('approval_asked' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'User Approval',
        'issue': 'Submit without user approval',
        'fix': 'Add explicit approval checkpoint before submit'
    })

if any('filters_applied' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'Filter Application',
        'issue': 'Filters not applied correctly',
        'fix': 'Add URL params reference table in references/problem-filtering.md'
    })

if any('parsed_correctly' in a['name'] and not a.get('passed') 
       for r in eval_results for a in r['assertions']):
    recommendations.append({
        'area': 'DOM Parsing',
        'issue': 'Problem table parsed incorrectly',
        'fix': 'Update cmoj-structure.md with current DOM selectors'
    })

if recommendations:
    print("\n📋 Recommended Actions:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. **{rec['area']}**")
        print(f"   Issue: {rec['issue']}")
        print(f"   Fix: {rec['fix']}\n")
else:
    print("\n✅ No specific improvements needed based on eval results!")
    print("Skill is performing well across all evals")

# Ask user if they want to apply fixes
print(f"\n{'=' * 70}")
print("🔧 RECOMMENDED FIX:")
print("   Flow C (Contest) needs clearer instructions for calling Flow A")
print("   Solution: Add explicit loop instruction in references/flow-c-contest.md")
print("\n✅ Auto-applying fix...")
    
    # Read current SKILL.md
    skill_content = SKILL_PATH.read_text(encoding='utf-8')
    
    # Apply fixes (simplified - in reality would be more sophisticated)
    improvements_applied = []
    
    for rec in recommendations:
        if 'Local Testing' in rec['area']:
            # Add emphasis on local testing in Flow A description
            if 'Test local' in skill_content:
                skill_content = skill_content.replace(
                    'Test local',
                    'Test local (BẮT BUỘC với sample input/output)'
                )
                improvements_applied.append('Added mandatory local test emphasis')
        
        if 'User Approval' in rec['area']:
            # Add emphasis on approval
            if 'Submit' in skill_content:
                skill_content = skill_content.replace(
                    'Submit (cần approve)',
                    'Submit (LUÔN hỏi user trước khi submit)'
                )
                improvements_applied.append('Added explicit approval requirement')
        
        if 'Filter Application' in rec['area']:
            # Add clearer filter documentation reference
            if 'Filter/Search' in skill_content:
                skill_content = skill_content.replace(
                    'Filter/Search',
                    'Filter/Search (xem references/parameters.md)'
                )
                improvements_applied.append('Added parameter reference link')
    
    # Save updated SKILL.md
    SKILL_PATH.write_text(skill_content, encoding='utf-8')
    
    print(f"\n✅ Applied {len(improvements_applied)} improvements:")
    for imp in improvements_applied:
        print(f"  - {imp}")
    
    print(f"\n📄 Updated: {SKILL_PATH}")
    
    # Update version
    print("\n📌 Remember to update version in SKILL.md metadata:")
    print("   version: 2.1 (or 3.0 if major changes)")
    print("   updated-on: " + Path().home().joinpath('.qwen/skills/codemath-solver/SKILL.md'))

print(f"\n{'=' * 70}")
print("ANALYSIS COMPLETE!")
print(f"{'=' * 70}")
