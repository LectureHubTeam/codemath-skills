# Test Generation - Tự sinh Test Cases

## Tại sao cần Test Generation?

- ✅ Verify solution đúng trước khi submit
- ✅ Tìm edge cases mà chưa nghĩ tới
- ✅ Stress test so sánh brute force vs optimized
- ✅ Debug WA/TLE hiệu quả hơn

---

## Pattern 1: Random Test Generator

### Template Python

```python
import random

def generate_test(n_min, n_max, val_min, val_max):
    """Generate random test case"""
    n = random.randint(n_min, n_max)
    a = [random.randint(val_min, val_max) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))

# Generate 10 tests
for i in range(10):
    test = generate_test(1, 100, 1, 1000)
    with open(f"test_{i}.inp", "w") as f:
        f.write(test)
```

### Template C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <test_number>" << endl;
        return 1;
    }
    
    int test_num = stoi(argv[1]);
    
    // Seed với test number để reproduce được
    srand(test_num);
    
    int n = rand() % 100 + 1;  // N từ 1 đến 100
    
    cout << n << "\n";
    for (int i = 0; i < n; i++) {
        cout << (rand() % 1000 + 1) << " \n"[i == n-1];
    }
    
    return 0;
}
```

---

## Pattern 2: Stress Testing Framework

### Full Framework (Python)

```python
import random
import subprocess
import time

def generate_test(n_max, val_max):
    """Generate random test"""
    n = random.randint(1, n_max)
    a = [random.randint(1, val_max) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))

def run_solution(input_data, solution_file, timeout=5):
    """Run solution với input và timeout"""
    try:
        result = subprocess.run(
            ['python3', solution_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return None, -1  # TLE

def stress_test(brute_file, optimized_file, num_tests=1000):
    """Stress test: compare brute force vs optimized"""
    
    print(f"Starting stress test: {num_tests} tests")
    print(f"Brute force: {brute_file}")
    print(f"Optimized: {optimized_file}")
    print("-" * 50)
    
    for i in range(num_tests):
        # Generate test
        test_input = generate_test(n_max=100, val_max=1000)
        
        # Run brute force
        bf_output, bf_code = run_solution(test_input, brute_file)
        if bf_code != 0:
            print(f"Brute force crashed on test {i}")
            continue
        
        # Run optimized
        opt_output, opt_code = run_solution(test_input, optimized_file)
        if opt_code == -1:
            print(f"Test {i}: TLE!")
            with open('tle_test.inp', 'w') as f:
                f.write(test_input)
            break
        if opt_code != 0:
            print(f"Optimized crashed on test {i}")
            break
        
        # Compare
        if bf_output != opt_output:
            print(f"Test {i}: WA!")
            print(f"Input:\n{test_input}")
            print(f"Expected: {bf_output}")
            print(f"Got: {opt_output}")
            with open('wa_test.inp', 'w') as f:
                f.write(test_input)
            with open('wa_test.expected', 'w') as f:
                f.write(bf_output)
            with open('wa_test.got', 'w') as f:
                f.write(opt_output)
            break
        
        # Progress
        if (i + 1) % 100 == 0:
            print(f"Passed {i+1}/{num_tests} tests")
    else:
        print(f"All {num_tests} tests passed! ✅")

# Usage
if __name__ == "__main__":
    stress_test('brute_force.py', 'optimized.py', num_tests=1000)
```

---

## Pattern 3: Edge Case Generator

### Template

```python
def generate_edge_cases():
    """Generate specific edge cases"""
    
    test_cases = []
    
    # N = 0 (empty)
    test_cases.append(("0\n", "Test N=0"))
    
    # N = 1 (single element)
    test_cases.append(("1\n5", "Test N=1"))
    
    # All same
    test_cases.append(("5\n3 3 3 3 3", "Test all same"))
    
    # Sorted increasing
    test_cases.append(("5\n1 2 3 4 5", "Test sorted inc"))
    
    # Sorted decreasing
    test_cases.append(("5\n5 4 3 2 1", "Test sorted dec"))
    
    # Max values
    test_cases.append(("3\n1000000000 1000000000 1000000000", "Test max val"))
    
    # Min values
    test_cases.append(("3\n1 1 1", "Test min val"))
    
    # Prime numbers
    test_cases.append(("4\n2 3 5 7", "Test primes"))
    
    return test_cases

# Run edge cases
for test_input, description in generate_edge_cases():
    print(f"Running: {description}")
    output = run_solution(test_input, 'solution.py')
    print(f"Output: {output}")
    print("-" * 50)
```

---

## Pattern 4: Specific Case Generator

### Generate cases with specific properties

```python
def generate_specific_cases():
    """Generate cases with specific properties"""
    
    test_cases = []
    
    # Case 1: Array with all divisors of X
    x = 12
    divisors = [i for i in range(1, x+1) if x % i == 0]
    test_cases.append((f"{len(divisors)}\n" + " ".join(map(str, divisors)), 
                       f"Divisors of {x}"))
    
    # Case 2: Fibonacci sequence
    fib = [1, 1]
    for _ in range(8):
        fib.append(fib[-1] + fib[-2])
    test_cases.append((f"{len(fib)}\n" + " ".join(map(str, fib)),
                       "Fibonacci"))
    
    # Case 3: Perfect squares
    squares = [i*i for i in range(1, 11)]
    test_cases.append((f"{len(squares)}\n" + " ".join(map(str, squares)),
                       "Perfect squares"))
    
    # Case 4: Alternating high-low
    alt = [i if i % 2 == 0 else 1000-i for i in range(10)]
    test_cases.append((f"{len(alt)}\n" + " ".join(map(str, alt)),
                       "Alternating"))
    
    return test_cases
```

---

## Pattern 5: Fuzzer (Random + Mutate)

```python
import random

def mutate(test_input, mutation_rate=0.1):
    """Mutate existing test input"""
    lines = test_input.strip().split('\n')
    n = int(lines[0])
    a = list(map(int, lines[1].split()))
    
    # Mutate operations
    op = random.choice(['swap', 'change', 'add', 'remove'])
    
    if op == 'swap' and len(a) >= 2:
        i, j = random.sample(range(len(a)), 2)
        a[i], a[j] = a[j], a[i]
    
    elif op == 'change' and len(a) >= 1:
        i = random.randint(0, len(a)-1)
        a[i] = random.randint(1, 1000)
    
    elif op == 'add' and len(a) < 100:
        a.append(random.randint(1, 1000))
    
    elif op == 'remove' and len(a) > 1:
        a.pop(random.randint(0, len(a)-1))
    
    return f"{len(a)}\n" + " ".join(map(str, a))

def fuzzer(initial_tests, num_mutations=1000):
    """Fuzz testing với mutation"""
    
    test_pool = initial_tests.copy()
    
    for i in range(num_mutations):
        # Pick random test from pool
        parent = random.choice(test_pool)
        
        # Mutate
        mutated = mutate(parent)
        
        # Add to pool
        test_pool.append(mutated)
        
        # Run test
        bf = run_solution(mutated, 'brute_force.py')
        opt = run_solution(mutated, 'optimized.py')
        
        if bf != opt:
            print(f"Found bug at mutation {i}!")
            print(f"Input: {mutated}")
            with open('fuzz_bug.inp', 'w') as f:
                f.write(mutated)
            return False
    
    print(f"All {num_mutations} mutations passed!")
    return True
```

---

## Pattern 6: Compare Multiple Solutions

```python
def compare_solutions(solutions, test_generator, num_tests=100):
    """Compare multiple solutions"""
    
    print(f"Comparing {len(solutions)} solutions")
    print("-" * 50)
    
    for i in range(num_tests):
        test_input = test_generator()
        
        outputs = []
        for sol in solutions:
            output, code = run_solution(test_input, sol)
            outputs.append((sol, output, code))
        
        # Check if all outputs match
        first_output = outputs[0][1]
        for sol, output, code in outputs[1:]:
            if output != first_output:
                print(f"Test {i}: Mismatch!")
                print(f"Input: {test_input}")
                for sol, output, code in outputs:
                    print(f"  {sol}: {output} (code={code})")
                with open('mismatch.inp', 'w') as f:
                    f.write(test_input)
                return False
        
        if (i + 1) % 20 == 0:
            print(f"Passed {i+1}/{num_tests}")
    
    print(f"All {num_tests} tests matched! ✅")
    return True

# Usage
solutions = ['sol1.py', 'sol2.py', 'sol3.py']
compare_solutions(solutions, lambda: generate_test(100, 1000), num_tests=100)
```

---

## Pattern 7: Generate Large Test Cases

```python
def generate_large_test(n, val_max=10**9):
    """Generate large test case for stress testing"""
    
    a = [random.randint(1, val_max) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))

# Generate max constraints test
max_test = generate_large_test(10**5, 10**9)
with open('max_test.inp', 'w') as f:
    f.write(max_test)

# Time the solution
import time
start = time.time()
output = run_solution(max_test, 'optimized.py')
end = time.time()
print(f"Time for max test: {end-start:.3f}s")
```

---

## Pattern 8: Interactive Problem Tester

```python
def test_interactive(problem_input, expected_output, solution_file):
    """Test interactive problem"""
    
    # Run solution
    process = subprocess.Popen(
        ['python3', solution_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Feed input
    stdout, stderr = process.communicate(input=problem_input)
    
    # Check output
    if stdout.strip() == expected_output.strip():
        print("✅ Test passed!")
        return True
    else:
        print("❌ Test failed!")
        print(f"Expected: {expected_output}")
        print(f"Got: {stdout}")
        if stderr:
            print(f"Stderr: {stderr}")
        return False
```

---

## Best Practices

### 1. Reproducibility

```python
# Set seed để reproduce được
random.seed(42)
test = generate_test(100, 1000)
```

### 2. Incremental Testing

```python
# Test nhỏ trước, sau đó tăng dần
for n in [10, 100, 1000, 10000]:
    test = generate_test(n, 1000)
    output = run_solution(test, 'solution.py')
    print(f"N={n}: OK")
```

### 3. Save Failed Tests

```python
# Luôn save failed tests để debug sau
if bf != opt:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(f'failed_{timestamp}.inp', 'w') as f:
        f.write(test_input)
```

### 4. Parallel Testing

```python
from multiprocessing import Pool

def run_single_test(test_input):
    bf = run_solution(test_input, 'brute.py')
    opt = run_solution(test_input, 'opt.py')
    return (test_input, bf, opt, bf == opt)

# Run parallel
with Pool(4) as p:
    tests = [generate_test(100, 1000) for _ in range(1000)]
    results = p.map(run_single_test, tests)
    
    failed = [r for r in results if not r[3]]
    if failed:
        print(f"Found {len(failed)} failed tests")
```

---

## Quick Reference

| Pattern | Khi nào dùng |
|---------|-------------|
| Random Generator | Test general correctness |
| Stress Testing | Compare brute vs optimized |
| Edge Cases | Test boundaries |
| Specific Cases | Test special properties |
| Fuzzer | Find edge bugs |
| Compare Solutions | Verify multiple approaches |
| Large Tests | Stress test performance |

---

## Next Steps

Sau khi generate tests:
1. → Run stress test để verify solution
2. → Nếu tìm ra bug → Qua [05-debugging-strategies.md](05-debugging-strategies.md)
3. → Nếu tất cả pass → Submit!
