#!/bin/bash
# Template: Full flow giải bài CMOJ
# Usage: Tham khảo script này để hiểu flow, KHÔNG chạy trực tiếp
# Agent sẽ thực hiện từng bước riêng biệt để có thể inspect output

SLUG="${1:-hsgthaibinh2425sodacbiet}"
LANG="${2:-CPP17}"
BASE_URL="https://laptrinh.codemath.vn"

echo "=== CodeMath Solver ==="
echo "Problem: $SLUG"
echo "Language: $LANG"
echo ""

# ============================================================
# STEP 1: Check login status
# ============================================================
echo "--- Step 1: Checking login status ---"
agent-browser open "$BASE_URL/" && agent-browser wait --load networkidle
# agent-browser snapshot -i → Check for "Đăng nhập" vs username

# If not logged in:
# agent-browser open "$BASE_URL/accounts/login/" && agent-browser wait --load networkidle
# agent-browser snapshot -i
# agent-browser fill @eUSERNAME "your_username"
# agent-browser fill @ePASSWORD "your_password"
# agent-browser click @eLOGIN
# agent-browser wait --load networkidle
# agent-browser snapshot -i  → Verify login success
# agent-browser state save codemath-auth.json

# ============================================================
# STEP 2: Read problem
# ============================================================
echo "--- Step 2: Reading problem ---"
agent-browser open "$BASE_URL/problem/$SLUG" && agent-browser wait --load networkidle
agent-browser snapshot -i
# curl "defuddle.md/$BASE_URL/problem/$SLUG" → Extract full problem text
# Parse: title, statement, input format, output format, constraints, samples

# ============================================================
# STEP 3: Generate solution
# ============================================================
echo "--- Step 3: Generating solution ---"
# Agent uses LLM to generate code based on problem analysis
# Save to /tmp/codemath_solution.cpp (or .py, .java)

# ============================================================
# STEP 4: Test locally
# ============================================================
echo "--- Step 4: Testing locally ---"
# For C++:
# g++ -std=c++17 -O2 -o /tmp/codemath_solution /tmp/codemath_solution.cpp
# echo "SAMPLE_INPUT" | /tmp/codemath_solution
# Compare output with expected

# For Python:
# echo "SAMPLE_INPUT" | python3 /tmp/codemath_solution.py
# Compare output with expected

# ============================================================
# STEP 5: Submit (requires user approval)
# ============================================================
echo "--- Step 5: Submitting ---"
agent-browser open "$BASE_URL/problem/$SLUG/submit" && agent-browser wait --load networkidle
agent-browser snapshot -i
# agent-browser select @eLANG "$LANG"
# Inject code into editor (see SKILL.md for methods)
# agent-browser screenshot /tmp/submit_preview.png  → Show user
# ASK USER FOR APPROVAL
# agent-browser click @eSUBMIT
# agent-browser wait --load networkidle

# ============================================================
# STEP 6: Check result
# ============================================================
echo "--- Step 6: Checking result ---"
agent-browser snapshot -i
# Parse verdict: AC / WA / TLE / MLE / RE / CE
# Report to user

echo "=== Done ==="
