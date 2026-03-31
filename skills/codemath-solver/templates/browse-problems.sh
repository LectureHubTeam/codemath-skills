#!/bin/bash
# Template: Browse và filter bài chưa giải trên CMOJ
# Usage: Tham khảo script này cho flow browse. Agent thực hiện từng bước riêng biệt.

CATEGORY="${1:-}"          # Ví dụ: "HSG Thái Bình"
ORDER="${2:--ac_rate}"      # Mặc định: sắp theo %AC giảm dần
SEARCH="${3:-}"             # Từ khóa tìm kiếm (theo tên bài)

# Client-side filters (optional)
MIN_POINTS="${4:-0}"
MAX_POINTS="${5:-9999}"
MIN_AC_RATE="${6:-0}"       # %
MAX_AC_RATE="${7:-100}"     # %
MIN_AC_COUNT="${8:-0}"
MAX_AC_COUNT="${9:-999999}"
SEARCH_ID="${10:-}"         # Tìm theo keyword trong ID/Slug

BASE_URL="https://laptrinh.codemath.vn"

echo "=== CodeMath Problem Browser ==="
echo "Category: ${CATEGORY:-Tất cả}"
echo "Order: $ORDER"
echo "Search: ${SEARCH:-Không}"
echo ""

# ============================================================
# STEP 1: Login (BẮT BUỘC để thấy solved/unsolved indicator)
# ============================================================
echo "--- Step 1: Login ---"
# Thử load saved state
# agent-browser state load codemath-auth.json
# Nếu fail → login flow (xem templates/login-flow.sh)

# ============================================================
# STEP 2: Build URL với filter params
# ============================================================
echo "--- Step 2: Building filter URL ---"

URL="$BASE_URL/problems/?"

# Thêm category nếu có
if [ -n "$CATEGORY" ]; then
    # URL-encode category
    ENCODED_CAT=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CATEGORY'))")
    URL="${URL}category=${ENCODED_CAT}&"
fi

# Thêm search nếu có
if [ -n "$SEARCH" ]; then
    ENCODED_SEARCH=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SEARCH'))")
    URL="${URL}search=${ENCODED_SEARCH}&"
fi

# Thêm order
URL="${URL}order=${ORDER}"

echo "URL: $URL"

# ============================================================
# STEP 3: Navigate và snapshot
# ============================================================
echo "--- Step 3: Navigating ---"
agent-browser open "$URL" && agent-browser wait --load networkidle
agent-browser snapshot -i

# ============================================================
# STEP 4: Extract dữ liệu bảng bài tập
# ============================================================
echo "--- Step 4: Extracting problem list ---"

agent-browser eval --stdin <<'EVALEOF' > /tmp/cmoj_results.json
(function() {
    const results = [];
    const rows = document.querySelectorAll('table tbody tr');
    
    rows.forEach((row, index) => {
        const cells = row.querySelectorAll('td');
        if (cells.length < 2) return;
        
        const links = row.querySelectorAll('a[href*="/problem/"]');
        if (links.length === 0) return;
        
        const slugMatch = links[0].getAttribute('href').match(/\/problem\/([^/]+)/);
        const slug = slugMatch ? slugMatch[1] : null;
        if (!slug) return;
        
        const name = links.length > 1 ? links[1].textContent.trim() : links[0].textContent.trim();
        
        // Detect solved
        const isSolved = 
            row.classList.contains('solved') ||
            row.querySelector('.solved-icon, .ac-icon, .fa-check, .glyphicon-ok') !== null ||
            row.querySelector('i[style*="color: green"]') !== null ||
            row.querySelector('td:first-child i') !== null;
        
        const cellTexts = Array.from(cells).map(c => c.textContent.trim());
        
        results.push({
            '#': index + 1,
            slug, name,
            group: cellTexts[2] || '',
            points: cellTexts[3] || '',
            acRate: cellTexts[4] || '',
            acCount: cellTexts[5] || '',
            solved: isSolved
        });
    });
    
    const unsolved = results.filter(r => !r.solved);
    const solved = results.filter(r => r.solved);
    
    return JSON.stringify({
        total: results.length,
        solvedCount: solved.length,
        unsolvedCount: unsolved.length,
        unsolved: unsolved
    }, null, 2);
})()
EVALEOF

# ============================================================
# STEP 5: Check pagination
# ============================================================
echo "--- Step 5: Checking pagination ---"

agent-browser eval --stdin <<'EVALEOF' > /tmp/cmoj_pagination.json
(function() {
    const pageLinks = document.querySelectorAll('.pagination a, .page-link, nav[aria-label*="page"] a');
    const pages = [];
    pageLinks.forEach(a => {
        const num = parseInt(a.textContent.trim());
        if (!isNaN(num)) pages.push(num);
    });
    const current = document.querySelector('.pagination .active, .page-item.active');
    const currentPageStr = current ? current.textContent.trim() : '1';
    return JSON.stringify({
        totalPages: pages.length > 0 ? Math.max(...pages) : 1,
        currentPage: currentPageStr,
        hasMore: pages.length > 0 && Math.max(...pages) > parseInt(currentPageStr, 10)
    }, null, 2);
})()
EVALEOF
cat /tmp/cmoj_pagination.json

# ============================================================
# STEP 6: Client-side Filtering (Điểm, %AC, #AC, ID)
# ============================================================
echo "--- Step 6: Client-side Filtering ---"
# Sử dụng NodeJS script để filter các thuộc tính mà URL query không hỗ trợ

node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/tmp/cmoj_results.json', 'utf8'));

const minPoints = parseInt('$MIN_POINTS', 10);
const maxPoints = parseInt('$MAX_POINTS', 10);
const minAcRate = parseInt('$MIN_AC_RATE', 10);
const maxAcRate = parseInt('$MAX_AC_RATE', 10);
const minAcCount = parseInt('$MIN_AC_COUNT', 10);
const maxAcCount = parseInt('$MAX_AC_COUNT', 10);
const searchId = '$SEARCH_ID'.toLowerCase();

const filtered = data.unsolved.filter(p => {
    // Parse values from text
    const pointsStr = p.points ? p.points.replace(/[^0-9.]/g, '') : '0';
    const points = pointsStr ? parseFloat(pointsStr) : 0;
    
    const acRateStr = p.acRate ? p.acRate.replace(/[^0-9.]/g, '') : '0';
    const acRate = acRateStr ? parseFloat(acRateStr) : 0;
    
    const acCountStr = p.acCount ? p.acCount.replace(/[^0-9]/g, '') : '0';
    const acCount = acCountStr ? parseInt(acCountStr, 10) : 0;

    // Filter Logic
    if (points < minPoints || points > maxPoints) return false;
    if (acRate < minAcRate || acRate > maxAcRate) return false;
    if (acCount < minAcCount || acCount > maxAcCount) return false;
    if (searchId && !p.slug.toLowerCase().includes(searchId)) return false;

    return true;
});

console.log('=== Kết Quả Lọc ===');
console.log('Số bài thỏa mãn:', filtered.length);
filtered.forEach(p => {
    console.log('[ID: ' + p.slug + '] ' + p.name + ' | Điểm: ' + p.points + ' | %AC: ' + p.acRate + ' | #AC: ' + p.acCount);
});
" > /tmp/cmoj_filtered_results.txt

cat /tmp/cmoj_filtered_results.txt

echo ""
echo "=== Done ==="
echo "Dữ liệu JSON lưu tại: /tmp/cmoj_results.json"
echo "Kết quả lọc dạng text lưu tại: /tmp/cmoj_filtered_results.txt"
echo "Agent sẽ trình bày danh sách bài chưa giải (đã lọc) cho user."
echo "User chọn bài → chuyển sang flow solve-and-submit."
