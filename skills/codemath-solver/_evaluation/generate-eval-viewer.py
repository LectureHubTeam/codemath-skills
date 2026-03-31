#!/usr/bin/env python3
"""
Generate HTML Eval Viewer for Codemath-Solver
"""

import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path('~/.qwen/skills/codemath-solver/workspace/iteration-1').expanduser()
EVALS_FILE = Path('/Users/macbook_118/Documents/TechTus/02_Projects/Sharing_Session/codemath-evals.json')

# Load evals
evals_data = json.loads(EVALS_FILE.read_text())

html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codemath-Solver Eval Viewer</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #1a1a1a; margin-bottom: 10px; }}
        .meta {{ color: #666; margin-bottom: 30px; }}
        .eval-card {{ background: white; border-radius: 8px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .eval-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #eee; }}
        .eval-title {{ font-size: 20px; font-weight: 600; color: #1a1a1a; }}
        .eval-status {{ padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: 500; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        .status-passed {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
        .prompt-box {{ background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 20px; font-family: 'Courier New', monospace; font-size: 14px; }}
        .expected-box {{ background: #e8f5e9; border-left: 4px solid #28a745; padding: 15px; margin-bottom: 20px; }}
        .assertions {{ margin-top: 20px; }}
        .assertion-item {{ display: flex; align-items: flex-start; padding: 12px; margin-bottom: 10px; border-radius: 6px; background: #fafafa; }}
        .assertion-checkbox {{ margin-right: 12px; margin-top: 4px; }}
        .assertion-text {{ flex: 1; font-size: 14px; }}
        .assertion-evidence {{ width: 100%; margin-top: 8px; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 13px; }}
        .grade-section {{ margin-top: 20px; padding-top: 20px; border-top: 2px solid #eee; }}
        .grade-input {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; min-height: 80px; }}
        .timing-inputs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }}
        .timing-input {{ padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }}
        .save-btn {{ background: #007bff; color: white; border: none; padding: 10px 24px; border-radius: 4px; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 15px; }}
        .save-btn:hover {{ background: #0056b3; }}
        .progress-bar {{ height: 8px; background: #eee; border-radius: 4px; overflow: hidden; margin-bottom: 30px; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s; }}
        .summary-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 32px; font-weight: 700; color: #007bff; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Codemath-Solver Eval Viewer</h1>
        <p class="meta">Skill Version: 2.0 | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <div class="progress-bar">
            <div class="progress-fill" id="progress" style="width: 0%"></div>
        </div>
        
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-value" id="total-evals">{len(evals_data['evals'])}</div>
                <div class="stat-label">Total Evals</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="completed">0</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="pass-rate">-%</div>
                <div class="stat-label">Pass Rate</div>
            </div>
        </div>
"""

for eval_item in evals_data['evals']:
    eval_id = eval_item['id']
    eval_name = eval_item['eval_name']
    prompt = eval_item['prompt']
    expected = eval_item.get('expected_output', '')
    
    html += f"""
        <div class="eval-card" id="eval-{eval_id}">
            <div class="eval-header">
                <div class="eval-title">Eval #{eval_id}: {eval_name}</div>
                <div class="eval-status status-pending" id="status-{eval_id}">⏳ Pending</div>
            </div>
            
            <div class="prompt-box">
                <strong>📝 Prompt:</strong><br>
                {prompt}
            </div>
            
            <div class="expected-box">
                <strong>🎯 Expected Output:</strong><br>
                {expected}
            </div>
            
            <div class="assertions">
                <strong>✅ Assertions:</strong>
                <div id="assertions-{eval_id}">
                    <!-- Assertions will be loaded from grading.json -->
                </div>
            </div>
            
            <div class="grade-section">
                <strong>📝 Timing & Feedback:</strong>
                <div class="timing-inputs">
                    <input type="number" class="timing-input" id="duration-{eval_id}" placeholder="Duration (seconds)">
                    <input type="number" class="timing-input" id="tokens-{eval_id}" placeholder="Token usage">
                </div>
                <textarea class="grade-input" id="feedback-{eval_id}" placeholder="Your feedback here..."></textarea>
                <button class="save-btn" onclick="saveEval({eval_id})">💾 Save Grade</button>
            </div>
        </div>
"""

html += """
    </div>
    
    <script>
        const evals = """ + json.dumps(evals_data['evals']) + """;
        const workspace = '""" + str(WORKSPACE) + """';
        
        // Load grading data for each eval
        async function loadGradingData() {
            for (const evalItem of evals) {
                try {
                    const response = await fetch(`eval-${evalItem.id}-${evalItem.eval_name}/with_skill/grading.json`);
                    if (response.ok) {
                        const grading = await response.json();
                        renderAssertions(evalItem.id, grading);
                        updateStatus(evalItem.id, grading);
                    }
                } catch (e) {
                    console.log(`No grading data for eval ${evalItem.id}`);
                }
            }
            updateProgress();
        }
        
        function renderAssertions(evalId, grading) {
            const container = document.getElementById(`assertions-${evalId}`);
            if (!grading.assertions) return;
            
            let html = '';
            grading.assertions.forEach((assertion, idx) => {
                const checked = assertion.passed ? 'checked' : '';
                const evidence = assertion.evidence || '';
                html += `
                    <div class="assertion-item">
                        <input type="checkbox" class="assertion-checkbox" 
                               id="assert-${evalId}-${idx}" ${checked}
                               onchange="toggleAssertion(${evalId}, ${idx})">
                        <div class="assertion-text">
                            <strong>${assertion.name}:</strong> ${assertion.text}
                            <input type="text" class="assertion-evidence" 
                                   id="evidence-${evalId}-${idx}" 
                                   placeholder="Evidence..."
                                   value="${evidence}"
                                   onchange="updateEvidence(${evalId}, ${idx})">
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }
        
        function updateStatus(evalId, grading) {
            const statusEl = document.getElementById(`status-${evalId}`);
            const passed = grading.assertions.filter(a => a.passed).length;
            const total = grading.assertions.length;
            const passRate = total > 0 ? (passed / total * 100) : 0;
            
            if (passRate >= 100) {
                statusEl.className = 'eval-status status-passed';
                statusEl.textContent = `✅ Passed (${passRate.toFixed(0)}%)`;
            } else if (passRate >= 50) {
                statusEl.className = 'eval-status status-pending';
                statusEl.textContent = `⚠️ Partial (${passRate.toFixed(0)}%)`;
            } else {
                statusEl.className = 'eval-status status-failed';
                statusEl.textContent = `❌ Failed (${passRate.toFixed(0)}%)`;
            }
        }
        
        function toggleAssertion(evalId, idx) {
            // This would update the grading.json - for now just visual
            console.log(`Toggled assertion ${idx} for eval ${evalId}`);
        }
        
        function updateEvidence(evalId, idx) {
            console.log(`Updated evidence ${idx} for eval ${evalId}`);
        }
        
        function saveEval(evalId) {
            const duration = document.getElementById(`duration-${evalId}`).value;
            const tokens = document.getElementById(`tokens-${evalId}`).value;
            const feedback = document.getElementById(`feedback-${evalId}`).value;
            
            // Collect assertion states
            const assertions = [];
            document.querySelectorAll(`#assertions-${evalId} .assertion-item`).forEach((item, idx) => {
                const checkbox = item.querySelector('.assertion-checkbox');
                const evidence = item.querySelector('.assertion-evidence');
                assertions.push({
                    name: `assertion-${idx}`,
                    text: checkbox.parentElement.textContent.trim(),
                    passed: checkbox.checked,
                    evidence: evidence.value
                });
            });
            
            const grading = {
                eval_id: evalId,
                graded_at: new Date().toISOString(),
                status: 'graded',
                assertions: assertions,
                timing: {
                    duration_seconds: duration ? parseFloat(duration) : null,
                    token_usage: tokens ? parseInt(tokens) : null
                },
                feedback: feedback
            };
            
            // In a real implementation, this would save to file
            // For now, just show success
            const statusEl = document.getElementById(`status-${evalId}`);
            const passed = assertions.filter(a => a.passed).length;
            const total = assertions.length;
            const passRate = (passed / total * 100);
            
            statusEl.className = 'eval-status status-passed';
            statusEl.textContent = `✅ Saved (${passRate.toFixed(0)}%)`;
            
            alert(`✅ Saved grading for eval #${evalId}`);
            updateProgress();
        }
        
        function updateProgress() {
            const completed = document.querySelectorAll('.status-passed, .status-failed').length;
            const total = evals.length;
            const percent = (completed / total * 100);
            
            document.getElementById('progress').style.width = `${percent}%`;
            document.getElementById('completed').textContent = completed;
            
            // Calculate pass rate
            let passed = 0;
            document.querySelectorAll('.status-passed').forEach(() => passed++);
            if (completed > 0) {
                document.getElementById('pass-rate').textContent = `${(passed / completed * 100).toFixed(0)}%`;
            }
        }
        
        // Load on init
        loadGradingData();
    </script>
</body>
</html>
"""

# Save HTML
output_file = WORKSPACE / 'eval-viewer.html'
output_file.write_text(html)

print(f"✅ Eval viewer saved to: {output_file}")
print(f"🌐 Open in browser: file://{output_file.absolute()}")
