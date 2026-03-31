#!/bin/bash
# Template: Login to CMOJ and save session OR run via Custom Profile
# Usage reference only - agent executes step by step

BASE_URL="https://laptrinh.codemath.vn"
AUTH_STATE="codemath-auth.json"

echo "=== CMOJ Login Flow ==="

# ----------------- CHROME DEBUG OPTION -----------------
# Uncomment to use Local Chrome via Debug Port (Better for avoiding CAPTCHA/Cookies sync):
# mkdir -p ~/chrome-debug-profile
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
#   --remote-debugging-port=9222 \
#   --user-data-dir=$HOME/chrome-debug-profile \
#   --no-first-run \
#   --no-default-browser-check &
# sleep 3
# agent-browser connect 9222
# -------------------------------------------------------

# Step 1: Try loading saved state first
echo "--- Attempting to load saved session ---"
agent-browser state load "$AUTH_STATE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Session loaded. Verifying..."
    agent-browser open "$BASE_URL/" && agent-browser wait --load networkidle
    # snapshot -i → Check if still logged in
    # If yes → done
    # If no → proceed to fresh login
fi

# Step 2: Fresh login
echo "--- Fresh login ---"
agent-browser open "$BASE_URL/accounts/login/" && agent-browser wait --load networkidle
agent-browser snapshot -i

# Step 3: Fill credentials
# Agent will find refs from snapshot and fill:
# agent-browser fill @eUSERNAME "$USERNAME"
# agent-browser fill @ePASSWORD "$PASSWORD"
# agent-browser click @eLOGIN_BUTTON

# Step 4: Wait and verify
agent-browser wait --load networkidle
agent-browser snapshot -i
# Check: "Đăng xuất" text present = login success

# Step 5: Save state for reuse
agent-browser state save "$AUTH_STATE"
echo "Session saved to $AUTH_STATE"
echo "=== Login Complete ==="
