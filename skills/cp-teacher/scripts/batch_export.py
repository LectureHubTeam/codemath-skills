#!/usr/bin/env python3
"""
Batch Export - Export tất cả lessons trong contest folder sang PDF/DOCX/HTML

Usage:
    python3 batch_export.py ~/Desktop/hsghanoi-2024-2025/ --formats pdf docx html
    python3 batch_export.py ~/Desktop/contest/ --validate-first
"""

import argparse
import subprocess
import sys
from pathlib import Path

EXPORT_SCRIPT = Path(__file__).parent / "export_lesson.py"

def export_lesson(lesson_md: Path, formats: list[str], pdf_engine: str = "tectonic") -> bool:
    """Export single lesson to multiple formats"""
    
    if not lesson_md.exists():
        print(f"❌ File not found: {lesson_md}")
        return False
    
    output_dir = lesson_md.parent
    base_name = lesson_md.stem
    
    print(f"\n📄 Exporting: {lesson_md.name}")
    print(f"   Output dir: {output_dir}")
    print(f"   Formats: {', '.join(formats)}")
    
    success_count = 0
    
    for fmt in formats:
        fmt = fmt.lower()
        if fmt == "word":
            fmt = "docx"
        if fmt == "tex":
            fmt = "latex"
        
        output_file = output_dir / f"{base_name}.{fmt}"
        
        cmd = [
            sys.executable, str(EXPORT_SCRIPT),
            str(lesson_md),
            "--formats", fmt,
            "--pdf-engine", pdf_engine
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes timeout per format
            )
            
            if result.returncode == 0:
                print(f"   ✅ {fmt.upper()}: {output_file}")
                success_count += 1
            else:
                print(f"   ❌ {fmt.upper()} failed: {result.stderr[:100]}")
        
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  {fmt.upper()} timeout (2 minutes)")
        except Exception as e:
            print(f"   ❌ {fmt.upper()} error: {e}")
    
    return success_count == len(formats)


def main():
    parser = argparse.ArgumentParser(description="Batch export lessons to PDF/DOCX/HTML")
    parser.add_argument("contest_folder", help="Path to contest folder containing problem subfolders")
    parser.add_argument("--formats", nargs="+", default=["pdf", "docx", "html"],
                       choices=["pdf", "docx", "html", "latex", "word"],
                       help="Output formats (default: pdf docx html)")
    parser.add_argument("--pdf-engine", default="tectonic",
                       help="PDF engine (default: tectonic)")
    parser.add_argument("--validate-first", action="store_true",
                       help="Validate lessons before export")
    parser.add_argument("--skip-invalid", action="store_true",
                       help="Skip invalid lessons (only if --validate-first)")
    
    args = parser.parse_args()
    
    contest_folder = Path(args.contest_folder)
    
    if not contest_folder.exists():
        print(f"❌ Contest folder not found: {contest_folder}")
        sys.exit(1)
    
    # Find all lesson.md files
    lesson_files = list(contest_folder.rglob("lesson.md"))
    
    if not lesson_files:
        print(f"❌ No lesson.md files found in {contest_folder}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"BATCH EXPORT")
    print(f"{'='*70}")
    print(f"Contest folder: {contest_folder}")
    print(f"Found {len(lesson_files)} lesson(s)")
    print(f"Formats: {', '.join(args.formats)}")
    print(f"PDF engine: {args.pdf_engine}")
    print(f"{'='*70}\n")
    
    # Validate first if requested
    if args.validate_first:
        print("🔍 Validating lessons before export...\n")
        
        from validate_lesson import validate_lesson
        
        valid_lessons = []
        invalid_lessons = []
        
        for lesson_file in lesson_files:
            is_valid, issues = validate_lesson(lesson_file)
            
            if is_valid:
                valid_lessons.append(lesson_file)
                print(f"✅ {lesson_file.parent.name}: VALID")
            else:
                invalid_lessons.append((lesson_file, issues))
                print(f"❌ {lesson_file.parent.name}: INVALID ({len(issues)} issues)")
        
        print(f"\nValidation summary: {len(valid_lessons)} valid, {len(invalid_lessons)} invalid\n")
        
        if args.skip_invalid:
            lesson_files = valid_lessons
            print(f"⏭️  Skipping {len(invalid_lessons)} invalid lesson(s)\n")
        elif invalid_lessons:
            print("⚠️  Some lessons are invalid. Continue anyway? (y/n)")
            try:
                response = input().strip().lower()
                if response != 'y':
                    print("❌ Export cancelled")
                    sys.exit(0)
            except:
                print("❌ Export cancelled")
                sys.exit(0)
    
    # Export lessons
    success_count = 0
    fail_count = 0
    
    for lesson_file in lesson_files:
        print(f"\n{'─'*70}")
        success = export_lesson(lesson_file, args.formats, args.pdf_engine)
        
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"EXPORT SUMMARY")
    print(f"{'='*70}")
    print(f"Total lessons: {len(lesson_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    
    if fail_count == 0:
        print(f"\n✅ All lessons exported successfully!")
    else:
        print(f"\n⚠️  {fail_count} lesson(s) failed to export")
    
    print(f"{'='*70}\n")
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
