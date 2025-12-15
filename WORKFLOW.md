# Atlas ECU Documentation Workflow

## Overview

This workflow allows you to export tables from Atlas as CSV and automatically generate comprehensive markdown documentation.

## Tools Created

### 1. Atlas Launcher (`launch-atlas.sh`)
Fixes the Java version issue to launch Atlas with the bundled JRE.

```bash
./launch-atlas.sh
```

### 2. CSV Parser (`scripts/parse_atlas_csv.py`)
Parses Atlas CSV exports and generates markdown documentation.

#### Parse a single CSV file:
```bash
python3 scripts/parse_atlas_csv.py path/to/table.csv
```

#### Parse an entire directory:
```bash
python3 scripts/parse_atlas_csv.py tables/avcs/
```

### 3. Documentation Converter (`scripts/convert.py`)
Converts markdown to HTML and JSON formats.

```bash
python3 scripts/convert.py
```

## Complete Workflow

### Step 1: Export Tables from Atlas

1. Launch Atlas: `./launch-atlas.sh`
2. Open your ROM/project
3. For each table:
   - Right-click → Export → CSV
   - Save to appropriate category folder in `tables/`
   - Example: `tables/avcs/Intake/table-name.csv`

### Step 2: Generate Documentation

```bash
# Parse all CSV files in a category
python3 scripts/parse_atlas_csv.py tables/avcs/

# Or parse entire tables directory
python3 scripts/parse_atlas_csv.py tables/
```

### Step 3: Convert to HTML/JSON

```bash
python3 scripts/convert.py
```

### Step 4: View Documentation

Open `output/html/index.html` in your browser to browse all documentation.

## Directory Structure

```
atlas-docs/
├── tables/              # Source markdown + CSV files
│   ├── avcs/            # 28 tables documented
│   ├── ignition/
│   ├── fuel/
│   └── ...
├── screenshots/         # Optional: table screenshots
├── output/
│   ├── html/            # Generated HTML docs
│   └── json/            # Generated JSON (API-ready)
└── scripts/
    ├── parse_atlas_csv.py
    └── convert.py
```

## What Gets Generated

For each table, the parser creates markdown with:

- **Overview**: Category, platform, dimensions, units
- **Description**: What the table controls (fill in manually)
- **Axes**: X/Y axis parameters, ranges, units
- **Cell Values**: Data type, units, typical ranges
- **Data Preview**: First 8x8 corner of the table
- **Functional Behavior**: How ECU uses it (fill in manually)
- **Related Tables**: Dependencies (fill in manually)
- **Related Datalog Parameters**: What to monitor (fill in manually)
- **Tuning Notes**: Practical guidance (fill in manually)
- **Warnings**: Safety considerations (fill in manually)

## Progress

### ✓ Completed
- **AVCS**: 28 tables (3 scalars + 25 3D maps)
  - Intake cam tables (TGV Open/Closed, High/Low baro)
  - Exhaust cam tables (TGV Open/Closed, High/Low baro)
  - Activation speed parameters

### 🔄 Next Categories
- Ignition (timing tables)
- Fuel (injection, AFR targets)
- Airflow (MAF, load calculation)
- Engine (limiters, operating parameters)
- Throttle (pedal mapping)
- Sensors (scaling tables)
- Transmission
- VDC
- Analytical
- Patches
- PIDs

## Tips

1. **Export systematically**: Work through one category at a time
2. **Organize folders**: Match Atlas's tree structure
3. **Fill in descriptions**: Parser creates templates - add technical details
4. **Cross-reference**: Link related tables together
5. **Add datalog params**: Specify what to monitor when tuning
