#!/usr/bin/env python3
"""
Codemath-Solver Benchmark Aggregator
Aggregate results from all evals and generate benchmark report
"""

import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path('~/.qwen/skills/codemath-solver/workspace/iteration-1').expanduser()

print("=" * 70)
print("CODEMATH-SOLVER BENCHMARK AGGREGATION")
print("=" * 70)

# Load run summary
summary_file = WORKSPACE / 'run_summary.json'
if not summary_file.exists():
    print(f"❌ Run summary not found: {summary_file}")
    print("Please run run-all-evals.py first")
    exit(1)

summary = json.loads(summary_file.read_text())
print(f"\n📊 Skill: {summary['skill_name']} v{summary['skill_version']}")
print(f"📂 Workspace: {summary['workspace']}")
print(f"📅 Run date: {summary['run_date']}")

# Aggregate results
benchmark = {
    'skill_name': summary['skill_name'],
    'skill_version': summary['skill_version'],
    'aggregated_at': datetime.now().isoformat(),
    'total_evals': summary['total_evals'],
    'evals': [],
    'summary': {
        'passed': 0,
        'failed': 0,
        'pending': 0,
        'pass_rate': 0.0,
        'total_assertions': 0,
        'passed_assertions': 0,
        'avg_duration': 0.0,
        'avg_tokens': 0
    }
}

print(f"\n{'=' * 70}")
print("AGGREGATING RESULTS...")
print(f"{'=' * 70}")

durations = []
tokens = []

for eval_item in summary['evals']:
    eval_id = eval_item['eval_id']
    eval_name = eval_item['eval_name']
    
    grading_file = WORKSPACE / f'eval-{eval_id}-{eval_name}/with_skill/grading.json'
    
    if not grading_file.exists():
        print(f"⏳ {eval_name}: Grading pending")
        benchmark['evals'].append({
            'eval_id': eval_id,
            'eval_name': eval_name,
            'status': 'pending',
            'pass_rate': None
        })
        benchmark['summary']['pending'] += 1
        continue
    
    grading = json.loads(grading_file.read_text())
    
    # Calculate pass rate for this eval
    assertions = grading.get('assertions', [])
    total_assertions = len(assertions)
    passed_assertions = sum(1 for a in assertions if a.get('passed') == True)
    
    if total_assertions > 0:
        eval_pass_rate = (passed_assertions / total_assertions) * 100
    else:
        eval_pass_rate = 0.0
    
    # Determine status from grading.json first, then calculate
    grading_status = grading.get('status', 'pending')
    
    if grading_status == 'graded':
        if eval_pass_rate >= 100:
            status = 'passed'
            benchmark['summary']['passed'] += 1
        elif eval_pass_rate >= 50:
            status = 'partial'
            benchmark['summary']['failed'] += 1
        else:
            status = 'failed'
            benchmark['summary']['failed'] += 1
    elif grading_status == 'passed':
        status = 'passed'
        benchmark['summary']['passed'] += 1
    elif grading_status == 'partial':
        status = 'partial'
        benchmark['summary']['failed'] += 1
    elif grading_status == 'failed':
        status = 'failed'
        benchmark['summary']['failed'] += 1
    else:
        status = 'pending'
        benchmark['summary']['pending'] += 1
    
    # Update summary stats
    benchmark['summary']['total_assertions'] += total_assertions
    benchmark['summary']['passed_assertions'] += passed_assertions
    
    if grading.get('timing', {}).get('duration_seconds'):
        durations.append(grading['timing']['duration_seconds'])
    
    if grading.get('timing', {}).get('token_usage'):
        tokens.append(grading['timing']['token_usage'])
    
    benchmark['evals'].append({
        'eval_id': eval_id,
        'eval_name': eval_name,
        'status': status,
        'pass_rate': eval_pass_rate,
        'total_assertions': total_assertions,
        'passed_assertions': passed_assertions,
        'duration': grading.get('timing', {}).get('duration_seconds'),
        'tokens': grading.get('timing', {}).get('token_usage')
    })
    
    status_icon = '✅' if status == 'passed' else '⚠️' if status == 'partial' else '❌' if status == 'failed' else '⏳'
    print(f"{status_icon} {eval_name}: {eval_pass_rate:.0f}% ({passed_assertions}/{total_assertions}) - {status}")

# Calculate averages
if durations:
    benchmark['summary']['avg_duration'] = sum(durations) / len(durations)

if tokens:
    benchmark['summary']['avg_tokens'] = sum(tokens) / len(tokens)

# Calculate overall pass rate
completed = benchmark['summary']['passed'] + benchmark['summary']['failed']
if completed > 0:
    benchmark['summary']['pass_rate'] = (benchmark['summary']['passed'] / completed) * 100

# Save benchmark.json
benchmark_file = WORKSPACE / 'benchmark.json'
benchmark_file.write_text(json.dumps(benchmark, indent=2, ensure_ascii=False))
print(f"\n✅ Benchmark saved to: {benchmark_file}")

# Generate human-readable report
report = f"""# Codemath-Solver Benchmark Report

**Skill:** {benchmark['skill_name']} v{benchmark['skill_version']}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status:** {'Complete' if benchmark['summary']['pending'] == 0 else 'In Progress'}

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| **Total Evals** | {benchmark['total_evals']} |
| **Passed** | {benchmark['summary']['passed']} |
| **Failed** | {benchmark['summary']['failed']} |
| **Pending** | {benchmark['summary']['pending']} |
| **Pass Rate** | {benchmark['summary']['pass_rate']:.1f}% |
| **Total Assertions** | {benchmark['summary']['total_assertions']} |
| **Passed Assertions** | {benchmark['summary']['passed_assertions']} |
| **Assertion Pass Rate** | {(benchmark['summary']['passed_assertions'] / benchmark['summary']['total_assertions'] * 100) if benchmark['summary']['total_assertions'] > 0 else 0:.1f}% |
| **Avg Duration** | {benchmark['summary']['avg_duration']:.1f}s |
| **Avg Tokens** | {benchmark['summary']['avg_tokens']:,.0f} |

---

## 📋 Eval Results

| # | Eval Name | Status | Pass Rate | Assertions | Duration | Tokens |
|---|-----------|--------|-----------|------------|----------|--------|
"""

for eval_item in benchmark['evals']:
    status_icon = '✅' if eval_item['status'] == 'passed' else '⚠️' if eval_item['status'] == 'partial' else '❌' if eval_item['status'] == 'failed' else '⏳'
    duration = f"{eval_item['duration']:.1f}s" if eval_item['duration'] else '-'
    tokens = f"{eval_item['tokens']:,}" if eval_item['tokens'] else '-'
    pass_rate = f"{eval_item['pass_rate']:.0f}%" if eval_item['pass_rate'] is not None else '-'
    
    report += f"| {eval_item['eval_id']} | {eval_item['eval_name']} | {status_icon} {eval_item['status']} | {pass_rate} | {eval_item['passed_assertions']}/{eval_item['total_assertions']} | {duration} | {tokens} |\n"

report += f"""
---

## 📈 Analysis

### Strengths
- [To be filled based on results]

### Areas for Improvement
- [To be filled based on results]

### Recommendations
- [To be filled based on results]

---

## 📝 Detailed Results

"""

for eval_item in benchmark['evals']:
    eval_id = eval_item['eval_id']
    eval_name = eval_item['eval_name']
    
    grading_file = WORKSPACE / f'eval-{eval_id}-{eval_name}/with_skill/grading.json'
    if grading_file.exists():
        grading = json.loads(grading_file.read_text())
        
        report += f"### Eval #{eval_id}: {eval_name}\n\n"
        report += f"**Status:** {eval_item['status']}\n"
        report += f"**Pass Rate:** {eval_item['pass_rate']:.0f}%\n\n"
        
        if grading.get('assertions'):
            report += "**Assertions:**\n\n"
            report += "| Assertion | Result | Evidence |\n"
            report += "|-----------|--------|----------|\n"
            for assertion in grading['assertions']:
                icon = '✅' if assertion.get('passed') else '❌' if assertion.get('passed') == False else '⏳'
                evidence = assertion.get('evidence', '')[:50] + '...' if len(assertion.get('evidence', '')) > 50 else assertion.get('evidence', '')
                report += f"| {icon} {assertion['text']} | {'Pass' if assertion.get('passed') else 'Fail' if assertion.get('passed') == False else 'Pending'} | {evidence} |\n"
        
        if grading.get('feedback'):
            report += f"\n**Feedback:** {grading['feedback']}\n"
        
        report += "\n---\n\n"

report += f"""
---

## 🎯 Next Steps

1. **Review failures** - Check evals with <100% pass rate
2. **Identify patterns** - Look for common failure modes
3. **Iterate skill** - Update SKILL.md or references based on findings
4. **Re-run evals** - Verify improvements

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

# Save report
report_file = WORKSPACE / 'benchmark.md'
report_file.write_text(report)
print(f"✅ Report saved to: {report_file}")

print(f"\n{'=' * 70}")
print("BENCHMARK COMPLETE!")
print(f"{'=' * 70}")
print(f"📊 Pass Rate: {benchmark['summary']['pass_rate']:.1f}%")
print(f"✅ Passed: {benchmark['summary']['passed']}/{completed} evals")
print(f"📄 Report: {report_file}")

if benchmark['summary']['pending'] > 0:
    print(f"\n⚠️  {benchmark['summary']['pending']} evals still pending grading")
    print("👉 Open each grading.json and fill in results after running evals")
