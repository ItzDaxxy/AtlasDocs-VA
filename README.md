# FA20DIT Atlas ECU Documentation & Datalog Analyzer

Documentation and analysis tools for Subaru FA20DIT engines (2015-2021 WRX) tuned with Atlas ECU software.

> ⚠️ **Unofficial Resource**: This project is not affiliated with, endorsed by, or supported by Atlas ECU or any official tuning organization. All documentation is community-sourced and provided as-is for educational purposes.

## Overview

This repository contains:

- **ECU Table Documentation** - Reference docs for Atlas ECU tables organized by domain (fuel, ignition, AVCS, etc.)
- **Datalog Analyzer** - CLI tool and GitHub Action for analyzing FA20 datalogs
- **Tuning History** - Templates for tracking ECU changes and analysis results

## Structure

```
atlas-docs/
├── docs/                # ECU table documentation by category
│   ├── fuel/            # Fuel injection, AFR targets, trims
│   ├── ignition/        # Spark timing, knock thresholds
│   ├── avcs/            # Variable valve timing
│   ├── airflow/         # MAF, load calculations
│   ├── engine/          # Core engine parameters
│   ├── sensors/         # Sensor scaling/calibration
│   ├── throttle/        # Electronic throttle control
│   ├── transmission/    # Gearbox tables
│   └── tuning-history/  # Analysis logs, ECU change history
├── bin/                 # CLI tools
│   └── fa20amp-analyze  # Datalog analyzer
├── templates/           # Documentation templates
├── scripts/             # Conversion utilities
└── output/              # Generated documentation (HTML/JSON)
```

## Datalog Analyzer

Analyzes Atlas datalog CSV exports for fuel trims, knock, DAM, AFR, and engine health.

### CLI Usage

```bash
# Analyze a single datalog
python bin/fa20amp-analyze path/to/datalog.csv

# Analyze multiple datalogs
python bin/fa20amp-analyze log1.csv log2.csv log3.csv
```

**Requirements:** Python 3.11+, pandas (`pip install pandas`)

**Output:**
- Color-coded terminal report with issues by severity
- JSON report saved alongside input file (`*_analysis.json`)

### Analysis Domains

| Domain | Parameters Analyzed |
|--------|---------------------|
| **Fuel** | STFT, LTFT, AFR (λ), MAF-binned trims |
| **Ignition** | Feedback Knock, Fine Knock Learn, DAM |
| **Engine** | Coolant temp, oil temp, throttle position |

### Thresholds

| Parameter | OK | Warning | Critical |
|-----------|-----|---------|----------|
| STFT/LTFT | ±5% | ±10% | >10% |
| DAM | ≥0.95 | 0.75-0.95 | <0.75 |
| Knock Retard | 0-2° | 2-5° | >5° |

## GitHub Action

Use the analyzer as a GitHub Action in your own workflows.

### Workflow Example

```yaml
name: Analyze Datalog

on:
  push:
    paths:
      - 'datalogs/**/*.csv'
  workflow_dispatch:
    inputs:
      datalog_path:
        description: 'Path to datalog CSV'
        required: true

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run FA20 Analysis
        uses: ItzDaxxy/AtlasDocs-VA@main
        with:
          datalog-path: ${{ github.event.inputs.datalog_path || 'datalogs/latest.csv' }}
          fail-on-critical: 'true'
```

### Action Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `datalog-path` | Yes | - | Path to datalog CSV file |
| `fail-on-critical` | No | `false` | Fail workflow on critical issues |
| `fail-on-high` | No | `false` | Fail workflow on high priority issues |

### Action Outputs

| Output | Description |
|--------|-------------|
| `exit-code` | 0=ok, 1=high issues, 2=critical issues |
| `report-path` | Path to generated JSON report |
| `issues-found` | Number of issues detected |

## Sample Datalog

Minimal CSV structure for testing:

```csv
Time,AF Correction STFT (%),AF Learning Long Term (%),AF Ratio,Feedback Knock (°),Fine Knock Learn (°),Dynamic Advance Multiplier,Coolant Temp (°C),Mass Airflow Corrected (g/s)
0.000,-1.2,-3.5,1.001,0.00,0.00,1.00,88,4.2
0.033,-0.8,-3.5,0.998,0.00,0.00,1.00,88,4.5
0.066,-1.5,-3.5,1.003,-1.41,0.00,1.00,89,5.1
0.099,-0.5,-3.5,0.997,0.00,0.00,1.00,89,4.8
```

## Converting Documentation

Generate HTML or JSON from markdown docs:

```bash
# Convert all documentation
python scripts/convert.py

# Convert specific category
python scripts/convert.py docs/ignition

# View in browser
open output/html/index.html
```

## Platform

**Supported:** VA WRX (2015-2021) with FA20DIT engine

## Disclaimer

This documentation is provided for educational purposes only. Improper ECU tuning can cause engine damage, void warranties, and create unsafe conditions. Always:

- Work with a qualified tuner
- Use appropriate safety margins
- Monitor datalogs for anomalies
- Never exceed safe mechanical limits

**Use at your own risk.**
