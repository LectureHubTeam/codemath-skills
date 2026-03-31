#!/bin/bash
# Template: Parse và phân tích cấu trúc một Contest trên CMOJ
# Usage: Script tham khảo để extract các link constraints từ Contest url

CONTEST_URL="${1:-https://laptrinh.codemath.vn/contest/hsg2425quangtri}"

echo "=== CodeMath Contest Solver ==="
echo "Contest URL: $CONTEST_URL"
echo ""

# ============================================================
# STEP 1: Navigate tới Contest Home Page
# ============================================================
echo "--- Step 1: Navigating to Contest ---"
agent-browser open "$CONTEST_URL" && agent-browser wait --load networkidle
agent-browser snapshot -i

# ============================================================
# STEP 2: Extract danh sách bài và Slug
# ============================================================
echo "--- Step 2: Extracting Problems List ---"
# Chúng ta sẽ tìm toàn bộ các liên kết trong main article có chứa đoạn "/problem/slug..."

agent-browser eval --stdin <<'EVALEOF' > /tmp/cmoj_contest.json
(function() {
    const results = [];
    
    // Tìm trong thẻ h2 hoặc các link phổ thông trong main page
    const links = document.querySelectorAll('a[href*="/problem/"]');
    
    links.forEach(link => {
        const href = link.getAttribute('href');
        const match = href.match(/\/problem\/([^/]+)/);
        
        if (match && match[1]) {
            const slug = match[1];
            // Tránh duplicate slug
            if (!results.some(r => r.slug === slug)) {
                results.push({
                    slug: slug,
                    name: link.textContent.trim(),
                    url: "https://laptrinh.codemath.vn/problem/" + slug
                });
            }
        }
    });

    const contestTitle = document.querySelector('h2') ? document.querySelector('h2').textContent.trim() : "Unknown Contest";
    
    return JSON.stringify({
        contest: contestTitle,
        total: results.length,
        problems: results
    }, null, 2);
})()
EVALEOF

cat /tmp/cmoj_contest.json

echo ""
echo "=== Processing Guidelines ==="
echo "Agent sẽ nhận được mảng JSON các problems trong contest trên."
echo "Sau đó Agent thực hiện vòng lặp:"
echo "For each Problem in problems:"
echo "   Chạy toàn bộ Flow A (solve-and-submit) với: problem_slug=slug"
echo "---"
