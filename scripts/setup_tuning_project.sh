#!/bin/bash
#
# FA20 Tuning Project Setup Script
# Creates directory structure for a new tuning project
#
# Usage: ./setup_tuning_project.sh <project_directory>
#

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <project_directory>"
    echo "Example: $0 ~/my-wrx-tune"
    exit 1
fi

PROJECT_DIR="$1"

echo "=============================================="
echo "  FA20 Tuning Project Setup"
echo "=============================================="
echo ""
echo "Creating project at: $PROJECT_DIR"
echo ""

# Create directory structure
mkdir -p "$PROJECT_DIR"/{datalogs,export,output,tables/{original,revised}}

# Create .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# Datalogs can be large
*.csv
!tables/**/*.csv

# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~
EOF

# Create project config
cat > "$PROJECT_DIR/project.yaml" << 'EOF'
# FA20 Tuning Project Configuration
vehicle:
  year: 2017
  make: Subaru
  model: WRX
  engine: FA20DIT
  software: Atlas

targets:
  peak_boost_psi: 22
  wot_afr_min: 10.5
  wot_afr_max: 11.5
  dam_minimum: 1.00
  ltft_max_percent: 5

notes: |
  Add your tuning notes here.
  Document any modifications, fuel grade, conditions, etc.
EOF

# Create README
cat > "$PROJECT_DIR/README.md" << 'EOF'
# FA20 Tuning Project

## Directory Structure

```
project/
├── datalogs/          # Raw Atlas CSV exports
├── export/            # Table exports from Atlas
├── output/            # Generated reports
├── tables/
│   ├── original/      # Backup of original tables
│   └── revised/       # Modified tables for import
├── project.yaml       # Project configuration
└── README.md
```

## Workflow

1. Export datalogs from Atlas to `datalogs/`
2. Export current tables from Atlas to `export/`
3. Run analysis: `python analyze_datalog.py --wot datalogs/wot.csv --cruise datalogs/cruise.csv`
4. Review generated report in `output/`
5. Import revised tables from `tables/revised/` into Atlas
6. Log again and verify improvements

## Key Parameters to Monitor

| Parameter | Target | Action if out of range |
|-----------|--------|------------------------|
| DAM | 1.00 | Reduce timing or boost |
| FBK | 0° | Check for knock sources |
| FKL | 0° | Pull timing in affected cells |
| STFT | ±5% | Adjust MAF scaling |
| LTFT | ±5% | Adjust MAF scaling |
| Peak Boost | ±1 psi of target | Adjust boost tables |
EOF

echo "Created directories:"
echo "  - datalogs/     (put WOT and cruise logs here)"
echo "  - export/       (Atlas table exports)"
echo "  - output/       (generated reports)"
echo "  - tables/       (original and revised tables)"
echo ""
echo "Created files:"
echo "  - project.yaml  (edit with your vehicle info)"
echo "  - README.md     (workflow documentation)"
echo "  - .gitignore    (excludes large CSV files)"
echo ""
echo "=============================================="
echo "  Project ready at: $PROJECT_DIR"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Edit project.yaml with your vehicle details"
echo "  2. Copy WOT and cruise datalogs to datalogs/"
echo "  3. Copy Atlas table exports to export/"
echo "  4. Run: python scripts/analyze_datalog.py --help"
echo ""
