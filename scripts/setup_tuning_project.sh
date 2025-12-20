#!/bin/bash
#
# FA20 Tuning Project Setup Script
# Creates directory structure and gathers mod info for safety margin calculation
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

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                     FA20 DIT TUNING PROJECT SETUP                            ║"
echo "║                         Powered by Amp AI Tuning                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Create directory structure
mkdir -p "$PROJECT_DIR"/{datalogs,export,output,tables/{original,revised}}

echo "We'll ask about your mod list to calculate appropriate safety margins."
echo "Answer Y/N or provide values where asked."
echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                              VEHICLE INFO"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Vehicle Year (e.g., 2017): " YEAR
read -p "Model (WRX/STI): " MODEL

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                              ENGINE MODS"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Turbo (stock/upgraded) [stock]: " TURBO
TURBO=${TURBO:-stock}

read -p "Intercooler (stock/TMIC/FMIC) [stock]: " INTERCOOLER
INTERCOOLER=${INTERCOOLER:-stock}

read -p "Downpipe (stock/catted/catless) [stock]: " DOWNPIPE
DOWNPIPE=${DOWNPIPE:-stock}

read -p "Intake (stock/aftermarket) [stock]: " INTAKE
INTAKE=${INTAKE:-stock}

read -p "EBCS (stock/3-port) [stock]: " EBCS
EBCS=${EBCS:-stock}

read -p "Flex Fuel kit installed? (Y/N) [N]: " FLEX
FLEX=${FLEX:-N}

read -p "AOS/Catch Can installed? (Y/N) [N]: " AOS
AOS=${AOS:-N}

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                              FUEL SYSTEM"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Injectors (stock/upgraded) [stock]: " INJECTORS
INJECTORS=${INJECTORS:-stock}

read -p "Fuel pump (stock/upgraded) [stock]: " FUEL_PUMP
FUEL_PUMP=${FUEL_PUMP:-stock}

read -p "Fuel grade typically used (91/93/E85) [93]: " FUEL_GRADE
FUEL_GRADE=${FUEL_GRADE:-93}

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                              BOOST TARGETS"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Target peak boost (psi) [20]: " TARGET_BOOST
TARGET_BOOST=${TARGET_BOOST:-20}

read -p "Redline RPM [6500]: " REDLINE
REDLINE=${REDLINE:-6500}

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                              DRIVING CONDITIONS"
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

read -p "Primary use (street/track/mixed) [street]: " USE_CASE
USE_CASE=${USE_CASE:-street}

read -p "Climate (hot/moderate/cold) [moderate]: " CLIMATE
CLIMATE=${CLIMATE:-moderate}

read -p "Altitude (low/high) [low]: " ALTITUDE
ALTITUDE=${ALTITUDE:-low}

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo "                         CALCULATING SAFETY MARGINS..."
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

# Write mod config
cat > "$PROJECT_DIR/vehicle_config.yaml" << EOF
# FA20 Tuning Project Configuration
# Generated: $(date -Iseconds)

vehicle:
  year: $YEAR
  model: $MODEL
  engine: FA20DIT

mods:
  turbo: $TURBO
  intercooler: $INTERCOOLER
  downpipe: $DOWNPIPE
  intake: $INTAKE
  ebcs: $EBCS
  flex_fuel: $FLEX
  aos_catch_can: $AOS

fuel_system:
  injectors: $INJECTORS
  fuel_pump: $FUEL_PUMP
  fuel_grade: $FUEL_GRADE

targets:
  peak_boost_psi: $TARGET_BOOST
  redline_rpm: $REDLINE

conditions:
  use_case: $USE_CASE
  climate: $CLIMATE
  altitude: $ALTITUDE

# SAFETY MARGINS - Calculated based on mod list
# These are RECOMMENDATIONS - adjust based on your tuner's advice
safety_margins:
EOF

# Calculate safety margins based on mods
echo "Analyzing mod list for safety recommendations..."
echo ""

# Initialize risk factors
TIMING_MARGIN=2
AFR_MARGIN="10.8"
BOOST_MARGIN=1
DAM_THRESHOLD="1.00"
KNOCK_THRESHOLD="0"

# Adjust based on mods
if [ "$TURBO" != "stock" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN + 1))
    echo "  ⚠️  Upgraded turbo: +1° timing margin"
fi

if [ "$INTERCOOLER" = "stock" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN + 1))
    echo "  ⚠️  Stock intercooler with mods: +1° timing margin (heat soak risk)"
fi

if [ "$DOWNPIPE" = "catless" ]; then
    echo "  ✓  Catless downpipe: Better flow, monitor EGTs"
fi

if [ "$EBCS" = "3-port" ]; then
    BOOST_MARGIN=0
    echo "  ✓  3-port EBCS: Tighter boost control, reduced margin needed"
else
    echo "  ⚠️  Stock EBCS: Keep +1 psi boost margin for spikes"
fi

if [ "$FUEL_GRADE" = "91" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN + 2))
    AFR_MARGIN="10.5"
    echo "  ⚠️  91 octane: +2° timing margin, richer AFR target"
elif [ "$FUEL_GRADE" = "E85" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN - 1))
    AFR_MARGIN="11.5"
    echo "  ✓  E85: Knock resistant, can run -1° timing margin"
fi

if [ "$CLIMATE" = "hot" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN + 1))
    echo "  ⚠️  Hot climate: +1° timing margin for IAT compensation"
fi

if [ "$ALTITUDE" = "high" ]; then
    BOOST_MARGIN=$((BOOST_MARGIN + 1))
    echo "  ⚠️  High altitude: Turbo works harder, +1 psi boost margin"
fi

if [ "$USE_CASE" = "track" ]; then
    TIMING_MARGIN=$((TIMING_MARGIN + 1))
    AFR_MARGIN="10.5"
    echo "  ⚠️  Track use: +1° timing margin, richer AFR for sustained WOT"
fi

# Write calculated margins
cat >> "$PROJECT_DIR/vehicle_config.yaml" << EOF
  timing_margin_degrees: $TIMING_MARGIN
  wot_afr_target: $AFR_MARGIN
  boost_margin_psi: $BOOST_MARGIN
  dam_minimum: $DAM_THRESHOLD
  max_knock_retard: $KNOCK_THRESHOLD

# Thresholds for analysis
thresholds:
  stft_warning: 5
  stft_critical: 10
  ltft_warning: 5
  ltft_critical: 10
  dam_warning: 0.95
  dam_critical: 0.75
  fbk_warning: -1
  fbk_critical: -3
  fkl_warning: -1
  fkl_critical: -2

notes: |
  Safety margins calculated based on your mod list.
  These are starting points - always verify with datalogs.
  
  Key recommendations for your setup:
EOF

# Add specific recommendations
if [ "$INTERCOOLER" = "stock" ] && [ "$TARGET_BOOST" -gt 18 ]; then
    echo "  - Consider FMIC upgrade before pushing past 18 psi" >> "$PROJECT_DIR/vehicle_config.yaml"
fi

if [ "$FUEL_PUMP" = "stock" ] && [ "$TARGET_BOOST" -gt 22 ]; then
    echo "  - Monitor fuel pressure at high boost - stock pump may limit" >> "$PROJECT_DIR/vehicle_config.yaml"
fi

if [ "$AOS" = "N" ]; then
    echo "  - Monitor oil consumption - consider AOS for track use" >> "$PROJECT_DIR/vehicle_config.yaml"
fi

echo "  - Always log and verify after any changes" >> "$PROJECT_DIR/vehicle_config.yaml"
echo "  - DAM must stay at 1.00 - investigate any drops immediately" >> "$PROJECT_DIR/vehicle_config.yaml"

# Create README
cat > "$PROJECT_DIR/README.md" << EOF
# FA20 Tuning Project - $YEAR $MODEL

## Mod List
- Turbo: $TURBO
- Intercooler: $INTERCOOLER
- Downpipe: $DOWNPIPE
- Intake: $INTAKE
- EBCS: $EBCS
- Flex Fuel: $FLEX
- Injectors: $INJECTORS
- Fuel Pump: $FUEL_PUMP
- Fuel Grade: $FUEL_GRADE

## Targets
- Peak Boost: $TARGET_BOOST psi
- Redline: $REDLINE RPM

## Calculated Safety Margins
| Parameter | Value | Reason |
|-----------|-------|--------|
| Timing Margin | $TIMING_MARGIN° | Based on mods + conditions |
| WOT AFR Target | $AFR_MARGIN:1 | Cylinder protection |
| Boost Margin | +$BOOST_MARGIN psi | Overshoot buffer |
| DAM Minimum | $DAM_THRESHOLD | Non-negotiable |

## Directory Structure
\`\`\`
$PROJECT_DIR/
├── datalogs/          # Raw Atlas CSV exports
├── export/            # Table exports from Atlas
├── output/            # Generated reports
├── tables/
│   ├── original/      # Backup of original tables
│   └── revised/       # Modified tables for import
├── vehicle_config.yaml
└── README.md
\`\`\`

## Workflow
1. Export datalogs to \`datalogs/\`
2. Run: \`python analyze_datalog.py --wot datalogs/wot.csv --cruise datalogs/cruise.csv\`
3. Review report in \`output/\`
4. Apply corrections, re-log, verify
EOF

# Create .gitignore
cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# Datalogs can be large
*.csv
!tables/**/*.csv

# OS files
.DS_Store
Thumbs.db
EOF

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                           SETUP COMPLETE                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Project created at: $PROJECT_DIR"
echo ""
echo "CALCULATED SAFETY MARGINS FOR YOUR BUILD:"
echo "──────────────────────────────────────────"
echo "  Timing Margin:    $TIMING_MARGIN° (pull this much from aggressive maps)"
echo "  WOT AFR Target:   $AFR_MARGIN:1 (lambda ~$(echo "scale=3; $AFR_MARGIN / 14.7" | bc))"
echo "  Boost Margin:     +$BOOST_MARGIN psi (keep this buffer from target)"
echo "  DAM Minimum:      $DAM_THRESHOLD (never accept less)"
echo ""
echo "Configuration saved to: $PROJECT_DIR/vehicle_config.yaml"
echo ""
echo "NEXT STEPS:"
echo "  1. Review vehicle_config.yaml and adjust if needed"
echo "  2. Export your current Atlas tables to tables/original/"
echo "  3. Copy datalogs to datalogs/"
echo "  4. Run analysis: python scripts/analyze_datalog.py --wot ... --cruise ..."
echo ""
echo "⚠️  These margins are RECOMMENDATIONS based on common setups."
echo "    Always verify with a qualified tuner for your specific build."
echo ""
