#!/usr/bin/env python3
"""
Lesson Validator - Kiểm tra chất lượng lesson trước khi export

Usage:
    python3 validate_lesson.py lesson.md
    python3 validate_lesson.py --batch ~/Desktop/contest/
"""

import argparse
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Problem Analysis",
    "Phân tích bài toán",
    "Manual Walkthrough",
    "Mô phỏng thủ công",
    "Code Explanation",
    "Giải thích",
    "Why AC",
    "chứng minh",
    "Chứng minh",
    "Edge Cases",
    "Common mistakes",
    "Practice Problems",
    "Bài tập",
]

MIN_LINES = 300
MIN_CODE_EXPLANATIONS = 5  # Số lần xuất hiện "Line X:" hoặc "================================="

def validate_lesson(lesson_path: Path) -> tuple[bool, list[str]]:
    """
    Validate lesson quality
    
    Returns:
        (is_valid, list_of_issues)
    """
    issues = []
    
    # Check 1: File exists
    if not lesson_path.exists():
        return False, [f"File not found: {lesson_path}"]
    
    # Check 2: Minimum lines
    with open(lesson_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        line_count = len(lines)
    
    if line_count < MIN_LINES:
        issues.append(f"❌ Too short: {line_count} lines (minimum {MIN_LINES})")
    
    # Check 3: Required sections
    content_lower = content.lower()
    missing_sections = []
    
    for section in REQUIRED_SECTIONS:
        if section.lower() not in content_lower:
            missing_sections.append(section)
    
    if missing_sections:
        issues.append(f"❌ Missing sections: {', '.join(missing_sections)}")
    
    # Check 4: Code explanation markers
    explanation_markers = content.count("=================================")
    if explanation_markers < MIN_CODE_EXPLANATIONS:
        issues.append(f"❌ Not enough code explanations: {explanation_markers} (minimum {MIN_CODE_EXPLANATIONS})")
    
    # Check 5: Has AC code
    if "def solve()" not in content and "int main()" not in content:
        issues.append("❌ No AC code found (missing solve() or main())")
    
    # Check 6: Has examples
    if "Input:" not in content or "Output:" not in content:
        issues.append("❌ No Input/Output examples")
    
    # Check 7: Has edge cases table
    if "| Case |" not in content and "| Input |" not in content:
        issues.append("⚠️  No edge cases table found (recommended)")
    
    # Check 8: Has common mistakes
    if "❌" not in content or "✅" not in content:
        issues.append("⚠️  No common mistakes (❌ SAI / ✅ ĐÚNG)")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def print_validation_report(lesson_path: Path, is_valid: bool, issues: list[str]):
    """Print validation report"""
    print(f"\n{'='*70}")
    print(f"VALIDATION REPORT: {lesson_path.name}")
    print(f"{'='*70}")
    
    if is_valid:
        print(f"✅ VALID: Lesson meets all quality requirements")
        
        # Show stats
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = len(content.split('\n'))
            code_blocks = content.count('```')
            tables = content.count('|')
        
        print(f"📊 Statistics:")
        print(f"   - Lines: {lines}")
        print(f"   - Code blocks: {code_blocks // 2}")
        print(f"   - Tables: {tables // 6}")
    else:
        print(f"❌ INVALID: Lesson has {len(issues)} issue(s):")
        for issue in issues:
            print(f"   {issue}")
    
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="Validate lesson quality")
    parser.add_argument("lesson_path", nargs="?", help="Path to lesson.md")
    parser.add_argument("--batch", help="Batch validate all lessons in folder")
    parser.add_argument("--strict", action="store_true", help="Strict mode (warnings become errors)")
    
    args = parser.parse_args()
    
    if args.batch:
        # Batch mode
        folder = Path(args.batch)
        if not folder.exists():
            print(f"❌ Folder not found: {folder}")
            sys.exit(1)
        
        print(f"🔍 Validating all lessons in {folder}...")
        
        valid_count = 0
        total_count = 0
        
        for lesson_file in folder.rglob("lesson.md"):
            total_count += 1
            is_valid, issues = validate_lesson(lesson_file)
            
            if is_valid:
                valid_count += 1
                print(f"✅ {lesson_file.parent.name}: VALID")
            else:
                print(f"❌ {lesson_file.parent.name}: INVALID ({len(issues)} issues)")
                for issue in issues[:2]:  # Show first 2 issues
                    print(f"      {issue}")
        
        print(f"\n{'='*70}")
        print(f"BATCH VALIDATION SUMMARY")
        print(f"{'='*70}")
        print(f"Valid: {valid_count}/{total_count}")
        print(f"Invalid: {total_count - valid_count}/{total_count}")
        print(f"Pass rate: {valid_count/total_count*100:.1f}%")
        print(f"{'='*70}\n")
        
        sys.exit(0 if valid_count == total_count else 1)
    
    elif args.lesson_path:
        # Single file mode
        lesson_path = Path(args.lesson_path)
        is_valid, issues = validate_lesson(lesson_path)
        print_validation_report(lesson_path, is_valid, issues)
        sys.exit(0 if is_valid else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
