#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from pathlib import Path

# Import validator
try:
    from validate_lesson import validate_lesson, print_validation_report
except ImportError:
    validate_lesson = None

def check_pandoc():
    try:
        subprocess.run(["pandoc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Export CP Teacher Markdown lesson to other formats using Pandoc.")
    parser.add_argument("input_file", help="Đường dẫn đến file markdown (ví dụ: outputs/bai-giang-1.md)")
    parser.add_argument("--formats", nargs="+", choices=["pdf", "docx", "word", "html", "latex", "tex"], default=["pdf", "docx"], help="Các định dạng muốn xuất ra (mặc định: pdf docx)")
    parser.add_argument("--pdf-engine", default="tectonic", help="PDF engine để dùng (mặc định: tectonic để tải packages tự động)")
    parser.add_argument("--validate", action="store_true", help="Validate lesson before export")
    parser.add_argument("--skip-validation", action="store_true", help="Skip validation even if lesson is short")

    args = parser.parse_args()

    if not check_pandoc():
        print("❌ LỖI: Không tìm thấy 'pandoc' trên hệ thống.")
        print("ℹ️ Vui lòng cài đặt Pandoc để sử dụng tính năng này.")
        print("   - macOS: brew install pandoc")
        print("   - Linux: sudo apt install pandoc")
        print("   - Windows: winget install pandoc")
        sys.exit(1)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ LỖI: Không tìm thấy file {input_path}")
        sys.exit(1)

    # Validate before export if requested
    if args.validate and validate_lesson:
        print("\n🔍 Validating lesson before export...\n")
        is_valid, issues = validate_lesson(input_path)
        print_validation_report(input_path, is_valid, issues)
        
        if not is_valid and not args.skip_validation:
            print("⚠️  Lesson has quality issues. Continue export anyway? (y/n)")
            try:
                response = input().strip().lower()
                if response != 'y':
                    print("❌ Export cancelled")
                    sys.exit(0)
            except:
                print("❌ Export cancelled")
                sys.exit(0)
        elif not is_valid:
            print("⏭️  Skipping validation, proceeding with export...\n")
        else:
            print("✅ Lesson passed validation!\n")
    elif args.validate and not validate_lesson:
        print("⚠️  Warning: validate_lesson module not found, skipping validation")

    base_name = input_path.stem
    output_dir = input_path.parent

    print(f"Đang xử lý file: {input_path}")
    
    for fmt in args.formats:
        fmt = fmt.lower()
        if fmt == "word": fmt = "docx"
        if fmt == "tex": fmt = "latex"
        
        output_file = output_dir / f"{base_name}.{fmt if fmt != 'latex' else 'tex'}"
        
        cmd = ["pandoc", str(input_path), "--standalone"]
        
        print(f"⏳ Đang xuất ra {fmt.upper()}...")
        
        if fmt == "html":
            cmd.extend(["--mathjax", "-o", str(output_file)])
        elif fmt == "docx":
            cmd.extend(["-o", str(output_file)])
        elif fmt == "latex":
            cmd.extend(["-o", str(output_file)])
        elif fmt == "pdf":
            # PDF requires extra args for Vietnamese unicode support
            cmd.extend([
                f"--pdf-engine={args.pdf_engine}",
                "-V", "geometry:margin=1in",
                "-o", str(output_file)
            ])
            # Note for user if they don't have LaTeX
            print("   (Lưu ý: Xuất PDF yêu cầu máy có cài đặt LaTeX như MacTeX/BasicTeX/TeXLive)")
            
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(f"✅ Đã lưu thành công: {output_file}")
            else:
                print(f"❌ Lỗi khi xuất {fmt}:")
                # Xử lý lỗi phổ biến với PDF (thiếu engine)
                if fmt == "pdf" and "tectonic not found" in result.stderr:
                    print("   Không tìm thấy 'tectonic' (PDF Engine).")
                    print("   Vui lòng cài đặt Tectonic. Trên macOS: brew install tectonic")
                    print("   Hoặc thử engine khác: --pdf-engine=xelatex (nếu đã có TeXLive)")
                else:
                    print(result.stderr.strip())
        except Exception as e:
            print(f"❌ Lỗi hệ thống: {str(e)}")

if __name__ == "__main__":
    main()
