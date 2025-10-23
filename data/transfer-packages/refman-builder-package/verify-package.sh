#!/bin/bash

# Package Verification Script
# Verifies all files are present in the transfer package

echo "========================================="
echo "Reference Manual Builder - Package Verification"
echo "========================================="
echo ""

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PACKAGE_DIR"

echo "Package Location: $PACKAGE_DIR"
echo ""

# File checklist
declare -a required_files=(
    "README.md"
    "SETUP_GUIDE.md"
    "MANIFEST.md"
    "verify-package.sh"
    "commands/HAL-refman.md"
    "agents/documentation-writer.md"
    "example/reference-manual-template.html"
)

echo "Checking required files..."
echo ""

missing_count=0
found_count=0

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "✅ $file ($size)"
        ((found_count++))
    else
        echo "❌ MISSING: $file"
        ((missing_count++))
    fi
done

echo ""
echo "========================================="
echo "Results:"
echo "  Found: $found_count"
echo "  Missing: $missing_count"
echo "  Total Expected: ${#required_files[@]}"
echo "========================================="
echo ""

if [ $missing_count -eq 0 ]; then
    echo "✅ Package verification PASSED"
    echo ""
    echo "Next steps:"
    echo "1. Read SETUP_GUIDE.md for installation instructions"
    echo "2. Copy files to your Claude Code project"
    echo "3. Run /HAL-refman status to verify installation"
    echo ""
    exit 0
else
    echo "❌ Package verification FAILED"
    echo ""
    echo "Missing $missing_count file(s). Package may be incomplete."
    echo "Please re-download or check extraction."
    echo ""
    exit 1
fi
