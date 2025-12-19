# Datalog Analysis Workflow

## Overview

This workflow enables automated analysis of FA20DIT datalogs from Atlas ECU software, either locally via CLI or through GitHub Actions.

## Local Analysis

### Prerequisites

```bash
pip install pandas
```

### Analyze a Datalog

```bash
python bin/fa20amp-analyze path/to/datalog.csv
```

### Output

1. **Terminal Report** - Color-coded summary with issues by severity
2. **JSON Report** - Machine-readable analysis saved as `*_analysis.json`

### Example Output

```
============================================================
FA20 DATALOG ANALYSIS
============================================================
File: 2025-12-17T11-08-58.csv
Loading... 29828 samples (~16.4 min)

ISSUES
----------------------------------------
[CRITICAL] [IGNITION] Significant knock: -5.6° retard, 1135 events
[HIGH] [FUEL] Lean AFR detected: max λ=1.508

FUEL TRIMS
----------------------------------------
STFT: -0.24% (range: -27.5% to +8.8%)
LTFT: -3.95% (range: -9.0% to 0.0%)

IGNITION
----------------------------------------
DAM: 1.00
Knock: 1135 events, max -5.6° retard
FKL: 0.0°

Report saved: 2025-12-17T11-08-58_analysis.json
```

## GitHub Actions Workflow

### Automatic Analysis on Push

Add datalogs to a `datalogs/` directory and push - the workflow triggers automatically.

### Manual Analysis

1. Go to **Actions** → **FA20 Datalog Analysis**
2. Click **Run workflow**
3. Enter the path to your datalog CSV
4. Optionally enable "Fail on critical issues"

### PR Integration

When datalogs are added via pull request, the analysis results are automatically posted as a PR comment.

## Tracking Results

### Analysis Log

Track all analyses in `docs/tuning-history/analysis-log.json`:

```json
{
  "analyses": [
    {
      "id": "2025-12-18_001",
      "datalog": "2025-12-17T11-08-58.csv",
      "critical_findings": [...],
      "fuel_summary": {...},
      "ignition_summary": {...},
      "recommendations": [...],
      "status": "reviewed"
    }
  ]
}
```

### ECU Config History

Track ECU changes and mechanical issues in `docs/tuning-history/ecu-config-history.json`:

```json
{
  "mechanical_issues": [
    {
      "id": "MECH-2025-12-18_001",
      "status": "investigating",
      "category": "exhaust",
      "symptoms": ["Rhythmic poof sound under acceleration"],
      "inspection_checklist": [...]
    }
  ],
  "changes": []
}
```

## Interpreting Results

### Severity Levels

| Severity | Action Required |
|----------|-----------------|
| **CRITICAL** | Immediate attention - potential engine damage |
| **HIGH** | Address soon - significant deviation from targets |
| **MEDIUM** | Monitor - minor corrections may help |
| **LOW/INFO** | Informational - no action needed |

### Common Issues

| Issue | Likely Cause | Action |
|-------|--------------|--------|
| STFT/LTFT >10% | MAF scaling off | Adjust MAF table |
| DAM <0.75 | Real knock | Check fuel, timing, boost |
| Knock with DAM=1.0, FKL=0° | False knock | Check exhaust, heat shields |
| Lean AFR at WOT | Insufficient fueling | Check injector scaling, fuel pressure |

## Converting Documentation

Generate browsable HTML or JSON from the markdown docs:

```bash
# Convert all docs
python scripts/convert.py

# Convert single category
python scripts/convert.py docs/fuel

# View
open output/html/index.html
```
