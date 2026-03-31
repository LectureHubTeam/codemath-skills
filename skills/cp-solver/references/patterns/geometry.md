# Geometry Patterns

## 1. Basic Geometry Primitives

### Point and Vector

```cpp
struct Point {
    long long x, y;
    Point() : x(0), y(0) {}
    Point(long long x, long long y) : x(x), y(y) {}
    
    Point operator+(const Point& other) const { return Point(x + other.x, y + other.y); }
    Point operator-(const Point& other) const { return Point(x - other.x, y - other.y); }
    Point operator*(long long k) const { return Point(x * k, y * k); }
    Point operator/(long long k) const { return Point(x / k, y / k); }
    
    bool operator==(const Point& other) const { return x == other.x && y == other.y; }
    bool operator<(const Point& other) const { return x < other.x || (x == other.x && y < other.y); }
};

long long dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
long long cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
long long dist_sq(Point a, Point b) { return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y); }
double dist(Point a, Point b) { return sqrt(dist_sq(a, b)); }
```

---

## 2. Line and Segment

### Line Representation

```cpp
struct Line {
    long long a, b, c;  // ax + by + c = 0
    
    Line(Point p1, Point p2) {
        a = p1.y - p2.y;
        b = p2.x - p1.x;
        c = -a * p1.x - b * p1.y;
    }
    
    bool contains(Point p) const { return a * p.x + b * p.y + c == 0; }
};

// Intersection of two lines
Point intersect(Line l1, Line l2) {
    long long det = l1.a * l2.b - l2.a * l1.b;
    if (det == 0) return Point(LLONG_MAX, LLONG_MAX);  // Parallel
    return Point(
        (l1.b * l2.c - l2.b * l1.c) / det,
        (l2.a * l1.c - l1.a * l2.c) / det
    );
}
```

### Segment Intersection

```cpp
int orientation(Point p, Point q, Point r) {
    long long val = cross(q - p, r - p);
    if (val == 0) return 0;  // Collinear
    return (val > 0) ? 1 : 2;  // Clockwise or Counterclockwise
}

bool on_segment(Point p, Point q, Point r) {
    return q.x >= min(p.x, r.x) && q.x <= max(p.x, r.x) &&
           q.y >= min(p.y, r.y) && q.y <= max(p.y, r.y);
}

bool segments_intersect(Point p1, Point q1, Point p2, Point q2) {
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);
    
    if (o1 != o2 && o3 != o4) return true;
    
    // Special cases (collinear)
    if (o1 == 0 && on_segment(p1, p2, q1)) return true;
    if (o2 == 0 && on_segment(p1, q2, q1)) return true;
    if (o3 == 0 && on_segment(p2, p1, q2)) return true;
    if (o4 == 0 && on_segment(p2, q1, q2)) return true;
    
    return false;
}
```

---

## 3. Polygon

### Convex Hull (Monotone Chain)

```cpp
vector<Point> convex_hull(vector<Point>& points) {
    int n = points.size();
    if (n <= 1) return points;
    
    sort(points.begin(), points.end());
    
    vector<Point> hull;
    
    // Lower hull
    for (int i = 0; i < n; i++) {
        while (hull.size() >= 2 && cross(hull.back() - hull[hull.size()-2], 
                                          points[i] - hull.back()) <= 0)
            hull.pop_back();
        hull.push_back(points[i]);
    }
    
    // Upper hull
    int lower_size = hull.size();
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() > lower_size && cross(hull.back() - hull[hull.size()-2], 
                                                  points[i] - hull.back()) <= 0)
            hull.pop_back();
        hull.push_back(points[i]);
    }
    
    if (hull.size() > 1) hull.pop_back();  // Remove duplicate
    return hull;
}
```

### Polygon Area

```cpp
// Shoelace formula
long long polygon_area(vector<Point>& poly) {
    long long area = 0;
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        area += cross(poly[i], poly[(i + 1) % n]);
    }
    return abs(area) / 2;
}
```

### Point in Convex Polygon

```cpp
// O(log N) - Binary search
bool point_in_convex(vector<Point>& poly, Point p) {
    int n = poly.size();
    if (n < 3) return false;
    
    // Check if p is outside the angle formed by poly[0], poly[1], poly[n-1]
    if (cross(poly[1] - poly[0], p - poly[0]) < 0 || 
        cross(poly[n-1] - poly[0], p - poly[0]) > 0)
        return false;
    
    // Binary search
    int lo = 1, hi = n - 1;
    while (hi - lo > 1) {
        int mid = (lo + hi) / 2;
        if (cross(poly[mid] - poly[0], p - poly[0]) >= 0)
            lo = mid;
        else
            hi = mid;
    }
    
    return cross(poly[lo+1] - poly[lo], p - poly[lo]) >= 0;
}
```

---

## 4. Circle

### Circle from Three Points

```cpp
struct Circle {
    Point center;
    double radius;
};

Circle circle_from_three_points(Point p1, Point p2, Point p3) {
    double ax = p1.x, ay = p1.y;
    double bx = p2.x, by = p2.y;
    double cx = p3.x, cy = p3.y;
    
    double d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by));
    if (abs(d) < 1e-9) return {{0, 0}, 0};  // Collinear
    
    double ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d;
    double uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d;
    
    Point center(ux, uy);
    double radius = dist(center, p1);
    
    return {center, radius};
}
```

### Circle Intersection

```cpp
vector<Point> circle_intersect(Point c1, double r1, Point c2, double r2) {
    double d = dist(c1, c2);
    if (d > r1 + r2 || d < abs(r1 - r2)) return {};  // No intersection
    if (d == 0 && r1 == r2) return {};  // Same circle
    
    double a = (r1*r1 - r2*r2 + d*d) / (2*d);
    double h = sqrt(max(0.0, r1*r1 - a*a));
    
    Point p = c1 + (c2 - c1) * (a / d);
    
    return {
        Point(p.x + h * (c2.y - c1.y) / d, p.y - h * (c2.x - c1.x) / d),
        Point(p.x - h * (c2.y - c1.y) / d, p.y + h * (c2.x - c1.x) / d)
    };
}
```

---

## 5. Closest Pair of Points

### Divide and Conquer (O(N log N))

```cpp
double closest_pair(vector<Point>& points) {
    int n = points.size();
    if (n <= 1) return 1e18;
    
    sort(points.begin(), points.end());
    
    function<double(int, int)> solve = [&](int l, int r) -> double {
        if (r - l <= 3) {
            double min_dist = 1e18;
            for (int i = l; i <= r; i++)
                for (int j = i + 1; j <= r; j++)
                    min_dist = min(min_dist, dist(points[i], points[j]));
            return min_dist;
        }
        
        int mid = (l + r) / 2;
        double mid_x = points[mid].x;
        double d = min(solve(l, mid), solve(mid + 1, r));
        
        // Merge step
        vector<Point> strip;
        for (int i = l; i <= r; i++)
            if (abs(points[i].x - mid_x) < d)
                strip.push_back(points[i]);
        
        sort(strip.begin(), strip.end(), [](Point a, Point b) {
            return a.y < b.y;
        });
        
        for (int i = 0; i < strip.size(); i++)
            for (int j = i + 1; j < strip.size() && strip[j].y - strip[i].y < d; j++)
                d = min(d, dist(strip[i], strip[j]));
        
        return d;
    };
    
    return solve(0, n - 1);
}
```

---

## 6. Rotating Calipers

### Diameter of Convex Polygon

```cpp
double diameter(vector<Point>& poly) {
    int n = poly.size();
    if (n <= 1) return 0;
    if (n == 2) return dist(poly[0], poly[1]);
    
    double max_dist = 0;
    int j = 1;
    
    for (int i = 0; i < n; i++) {
        while (cross(poly[(i+1)%n] - poly[i], poly[(j+1)%n] - poly[j]) > 0)
            j = (j + 1) % n;
        
        max_dist = max(max_dist, dist(poly[i], poly[j]));
        max_dist = max(max_dist, dist(poly[(i+1)%n], poly[(j+1)%n]));
    }
    
    return max_dist;
}
```

---

## 7. Pick's Theorem

```cpp
// Area = I + B/2 - 1
// where I = interior lattice points, B = boundary lattice points

long long boundary_lattice_points(Point p1, Point p2) {
    return gcd(abs(p1.x - p2.x), abs(p1.y - p2.y)) + 1;
}

// For a polygon
pair<long long, long long> picks_theorem(vector<Point>& poly) {
    long long area2 = 0;  // 2 * area
    long long B = 0;
    
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        area2 += cross(poly[i], poly[(i+1)%n]);
        B += boundary_lattice_points(poly[i], poly[(i+1)%n]);
    }
    
    area2 = abs(area2);
    B -= n;  // Each vertex counted twice
    
    // I = Area - B/2 + 1
    long long I = (area2 - B + 2) / 2;
    
    return {I, B};
}
```

---

## Common Geometry Problems

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| Convex hull | Monotone chain | O(N log N) |
| Polygon area | Shoelace | O(N) |
| Point in polygon | Ray casting / Winding number | O(N) |
| Segment intersection | Orientation test | O(1) |
| Closest pair | Divide & conquer | O(N log N) |
| Circle from 3 points | Perpendicular bisectors | O(1) |
| Diameter of polygon | Rotating calipers | O(N) |

---

## Tips

1. **Use long long** for coordinates to avoid overflow
2. **Avoid floating point** when possible (use cross product instead of angles)
3. **Handle edge cases**: collinear points, empty polygons
4. **Use epsilon** for floating point comparisons: `abs(a - b) < 1e-9`

---

## Next Steps

- → Practice geometry problems on CMOJ
- → Learn computational geometry tricks
- → Use [06-test-generation.md](06-test-generation.md) to test with random points
