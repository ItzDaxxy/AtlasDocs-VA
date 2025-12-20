# 🏎️ DAMGood

**Because DAM=1.00 is the only acceptable answer.**

AI-powered datalog analysis and tuning tools for the **2015-2021 Subaru WRX (VA chassis)** with FA20DIT engine, built for the [Atlas Open Source Tuning Suite](https://github.com/atlas-tuning).

### Features
- 🔧 Interactive mod-list setup with safety margin calculations
- 📊 Comprehensive pandas-formatted tuning reports
- ⛽ Fuel trim analysis, knock detection, boost control review
- 📋 Revised table generation for Atlas import

> ⚠️ **Unofficial Resource**: This project is not affiliated with, endorsed by, or supported by Atlas or Subaru. All documentation is community-sourced and provided as-is for educational purposes.

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **VA WRX (2015-2021)** | ✅ Fully Supported | FA20DIT - Primary development platform |
| VA STI (2015-2021) | ⚠️ Partial | EJ257 - Different engine, some concepts apply |
| VB WRX (2022+) | ❌ Not Supported | FA24 - Different ECU architecture |

**This tool is built on and validated against the VA WRX FA20DIT platform.** Default thresholds and safety margins are calibrated for the stock FA20 turbo configuration.

## Overview

This repository contains:

- **ECU Table Documentation** - Reference docs for Atlas tables organized by domain (fuel, ignition, AVCS, etc.)
- **Datalog Analyzer** - Comprehensive analysis tool generating pandas-formatted tuning reports
- **Tuning Workflow** - Complete dial-in process with table corrections and math
- **AI Tuning Agent** - AGENTS.md instructions for AI-assisted datalog analysis

## Three Ways to Use This Tool

### Option 1: 🖥️ Terminal UI (TUI)
Launch the interactive terminal interface for a visual analysis experience:

```bash
./bin/damgood          # Terminal
./bin/damgood-web      # Web browser (http://localhost:8000)
```

**Features:**
- **Tabbed interface** — Summary, Fuel Trims, Boost, Power Enrichment panels
- **Auto-detection** — Automatically identifies WOT vs Cruise vs Mixed logs
- **Clickable file management** — Add/remove datalogs, hover to see remove option
- **Save dialogs** — Browse and choose where to export files
- **AI Chat** — Built-in AI assistant for detailed analysis (press `A`)
- **Web accessible** — Run in browser via textual-serve

**Keyboard Shortcuts:**
| Key | Action |
|-----|--------|
| `L` | Load datalog |
| `A` | AI Chat (requires API key) |
| `G` | Generate revised tables |
| `R` | Refresh analysis |
| `X` | Reset to default state |
| `Q` | Quit |

**AI Chat Setup:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."  # or
export OPENAI_API_KEY="sk-..."
```

![TUI Screenshot](assets/tui-screenshot.png)

### Option 2: Static Scripts
Run the analyzer directly from the command line for quick, automated reports:

```bash
python scripts/analyze_datalog.py --wot wot.csv --cruise cruise.csv
```

No AI required — just Python and pandas. Great for batch processing or CI/CD pipelines.

### Option 3: 🤖 Interactive AI Assistant

This repo includes an `AGENTS.md` file that turns AI assistants into FA20 tuning experts. Clone this repo and open it in [Amp](https://ampcode.com) or add it to a Claude project, and you get an interactive tuning partner that can:

- **Analyze your datalogs conversationally** — just drop a CSV and ask questions
- **Explain what the data means** — "Why is my STFT negative at high MAF?"
- **Generate full tuning reports** — formatted tables, histograms, and action items
- **Calculate table corrections** — MAF scaling, PE targets, boost adjustments
- **Debug tuning issues** — "I'm getting knock at 4500 RPM, what should I check?"

#### Example Interaction

```
You: Here's my WOT datalog, what do you see?
AI:  [analyzes CSV] Your DAM is solid at 1.00, no knock events. 
     However, STFT is running +8% lean at 4500-5000 RPM during WOT.
     Your PE table needs enrichment in that range. Here's the correction...
```

Unlike static scripts, the AI can answer follow-up questions, explain its reasoning, and adapt recommendations to your specific build and situation.

## Installation

```bash
# Clone the repo
git clone https://github.com/ItzDaxxy/DAMGood.git
cd DAMGood

# Run the installer (creates venv, installs deps, adds 'damgood' command)
./install.sh
```

After installation, run DAMGood from anywhere:
```bash
damgood
```

**Requirements:** Python 3.9+

## Quick Start

```bash
# Initialize a new tuning project (interactive mod list intake)
./scripts/setup_tuning_project.sh ~/my-wrx-tune

# Launch the interactive TUI
damgood

# Or analyze from command line
python scripts/analyze_datalog.py --wot datalogs/wot.csv --cruise datalogs/cruise.csv
```

## New Project Setup Flow

When you run `setup_tuning_project.sh`, you'll go through an interactive setup that:

1. **Gathers your mod list** - Turbo, intercooler, downpipe, intake, EBCS, flex fuel, etc.
2. **Asks about fuel system** - Injectors, fuel pump, fuel grade (91/93/E85)
3. **Sets boost targets** - Peak boost PSI, redline RPM
4. **Evaluates conditions** - Street/track use, climate, altitude
5. **Calculates safety margins** - Based on YOUR specific build

### Example Setup Session

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     FA20 DIT TUNING PROJECT SETUP                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Vehicle Year: 2017
Model: WRX

Turbo (stock/upgraded) [stock]: stock
Intercooler (stock/TMIC/FMIC) [stock]: FMIC
Downpipe (stock/catted/catless) [stock]: catted
Intake (stock/aftermarket) [stock]: aftermarket
EBCS (stock/3-port) [stock]: 3-port
Flex Fuel kit installed? (Y/N) [N]: N

Fuel grade typically used (91/93/E85) [93]: 93
Target peak boost (psi) [20]: 21

CALCULATING SAFETY MARGINS...

  ✓  Catted downpipe: Better flow, monitor EGTs
  ✓  3-port EBCS: Tighter boost control, reduced margin needed

CALCULATED SAFETY MARGINS FOR YOUR BUILD:
──────────────────────────────────────────
  Timing Margin:    2° (pull this much from aggressive maps)
  WOT AFR Target:   10.8:1 (lambda ~0.735)
  Boost Margin:     +0 psi (keep this buffer from target)
  DAM Minimum:      1.00 (never accept less)
```

### Safety Margin Logic

The setup script calculates margins based on risk factors:

| Mod/Condition | Effect | Reason |
|---------------|--------|--------|
| Stock intercooler + mods | +1° timing margin | Heat soak risk |
| 91 octane fuel | +2° timing, richer AFR | Lower knock resistance |
| E85 fuel | -1° timing margin | Excellent knock resistance |
| Hot climate | +1° timing margin | Higher IATs |
| High altitude | +1 psi boost margin | Turbo works harder |
| Track use | +1° timing, richer AFR | Sustained WOT heat |
| Stock EBCS | +1 psi boost margin | Slower boost response |
| 3-port EBCS | No boost margin needed | Precise control |

The output `vehicle_config.yaml` contains all your settings and calculated thresholds for the analyzer to use.

## What the Analyzer Produces

The analyzer generates a comprehensive tuning report with:

### Executive Summary
```
   Parameter     Value Threshold   Status
             DAM  1.00    ≥0.95    ✅ Perfect
  Feedback Knock  0.00       0°   ✅ No knock
Fine Knock Learn  0.00       0°      ✅ Clean
            LTFT -0.39      ±5%         ✅ OK
```

### STFT Histogram with Visual Bars
```
  Range     Count  Pct                    Histogram
    < -10%    58   2.1                               █
 -5 to -3%   226   8.1                          ██████
  -3 to 0%  1664  59.9 ███████████████████████████████
  0 to +3%   438  15.8                    ████████████
```

### Fuel Trim Analysis by MAF Range
```
 MAF Range   STFT   LTFT  Combined  Status   Samples
   0-10 g/s -0.14% +0.39%  +0.25%      ✅ OK   1234
100-150 g/s -1.14% -3.54%  -4.68%  ⚠️ Minor    294
```

### Power Enrichment Analysis (WOT)
```
      RPM Lambda    AFR   STFT     Status
4000-4500  0.741 10.9:1  +3.0%  ⚠️ Monitor
4500-5000  0.742 10.9:1 +10.1%     ❌ Lean
```

### Math & Calculations
Shows the actual formulas and calculations:
- Fuel trim correction methodology
- PE (φ) enrichment calculations with examples
- Boost target conversions (psi ↔ bar)
- Knock threshold reference table

### Revised Tables for Atlas Import
Ready-to-import corrected tables:
- **Boost Target Main** - With psi reductions applied
- **MAF Scaling** - Conservative corrections preserving rich bias
- **PE Target** - Enriched high-RPM cells

### Action Items Checklist
```
Priority   Category                                      Item     Status
       1     Safety                        DAM stable at 1.00 ✅ Complete
       2      Boost Import revised Boost Target Main (-1 psi)  ☐ Pending
       3       Fuel  Import revised PE Target (4000-5500 RPM)  ☐ Pending
```

## Project Structure

```
atlas-docs/
├── docs/                  # ECU table documentation by category
│   ├── fuel/              # Fuel injection, AFR targets, trims
│   ├── ignition/          # Spark timing, knock thresholds
│   ├── avcs/              # Variable valve timing
│   ├── airflow/           # MAF, boost control, wastegate
│   ├── engine/            # Core engine parameters
│   ├── sensors/           # Sensor scaling/calibration
│   ├── throttle/          # Electronic throttle control
│   └── transmission/      # Gearbox tables
├── scripts/
│   ├── analyze_datalog.py # Main analysis script
│   └── setup_tuning_project.sh  # Project initializer
├── samples/               # Example datalogs
├── output/                # Generated reports
├── AGENTS.md              # AI tuning agent instructions
└── WORKFLOW.md            # Tuning workflow documentation
```

## Tuning Workflow

### 0. Import the DAMGood Gauge Set
Before logging, import the included gauge set into Atlas for consistent, analysis-ready datalogs:

1. In Atlas, go to **File → Import → Gauge Set**
2. Select `gauges/DAMGood.gaugeset` from this repo
3. The gauge set will appear in your gauge list

**Why use this gauge set?**
- **Pre-configured parameters** — All the PIDs needed for fuel, ignition, boost, and knock analysis
- **Consistent column names** — Matches what the analyzer script expects
- **No missing data** — Ensures you capture DAM, FBK, FKL, STFT, LTFT, MAF, boost, lambda, etc.
- **Optimized layout** — Organized for at-a-glance monitoring while driving

Using a different gauge set? The analyzer will still work, but column names may need adjustment.

### 1. Collect Datalogs
Export from Atlas. Your logging needs will vary based on what you're tuning, but a comprehensive analysis can include:

| Scenario | What to Log | Purpose |
|----------|-------------|---------|
| **Idle** | Warm idle, A/C on/off, electrical loads | Fuel trims at low airflow, idle stability |
| **Cruise** | Highway steady-state, light throttle, various RPM | MAF scaling across load ranges, LTFT learning |
| **WOT Pulls** | 3rd gear, 3000-6000+ RPM, full throttle | Power enrichment, knock behavior, boost control |
| **Boost Transients** | Partial throttle tip-in, gear changes | Wastegate response, boost spikes/dips |
| **Cold Start** | First 2-3 minutes from cold | Warm-up enrichment, open-loop behavior |
| **Hill Climbs** | Sustained load, varying throttle | Heat soak, extended high-load fuel trims |

You can always log less — a single WOT pull will still give useful data. But for dial-in, more scenarios = better visibility into how the ECU is compensating across conditions.

### 2. Run Analysis
```bash
python scripts/analyze_datalog.py --wot wot.csv --cruise cruise.csv
```

### 3. Review Report
Check the generated `FA20_Tuning_Report.txt` for:
- DAM/FBK/FKL status (must be green)
- STFT distribution (should center around 0%)
- MAF range fuel trims (identify scaling issues)
- WOT AFR by RPM (identify PE table issues)
- Boost overshoot (adjust targets if needed)

### 4. Apply Corrections
Import revised tables to Atlas:
- Conservative MAF scaling (preserves 2-3% rich bias for cylinder protection)
- Enriched PE targets for high-RPM WOT
- Reduced boost targets if overshooting

### 5. Validate
Log again and verify:
- STFT within ±5% across all ranges
- DAM stays at 1.00
- No knock events
- Boost hitting new targets

## Key Thresholds

| Parameter | Green | Yellow | Red |
|-----------|-------|--------|-----|
| DAM | ≥0.95 | 0.75-0.95 | <0.75 |
| Feedback Knock | 0° | -1° to -3° | <-3° |
| Fine Knock Learn | 0° | -1° to -2° | <-2° |
| STFT | ±5% | ±5-10% | >±10% |
| LTFT | ±5% | ±5-10% | >±10% |

## Key Formulas

| Calculation | Formula |
|-------------|---------|
| Actual Fuel | `Commanded × (1 + STFT/100) × (1 + LTFT/100)` |
| MAF Correction | `-1 × Combined Trim` |
| AFR from Lambda | `Lambda × 14.7` |
| AFR from φ | `14.7 / φ` |
| psi to bar | `psi × 0.0689476` |
| bar to psi | `bar × 14.5038` |
| PE Enrichment | `New φ = Current φ × (1 + STFT/100)` |

## Safety Guidelines

1. **Always preserve rich bias** (2-3% negative trims) for cylinder protection under boost
2. **Never zero out fuel trims completely** - some margin is intentional
3. **DAM must stay at 1.00** - any drop requires immediate investigation
4. **Log after every change** - verify corrections with new datalogs

## Stock Calibration Baseline

Default configuration is based on **stock FA20DIT calibration**:

| Parameter | Stock Default | Notes |
|-----------|---------------|-------|
| Peak Boost | 18 psi | Stock turbo safe limit |
| WOT AFR | 10.8:1 | Rich for cylinder protection |
| DAM Minimum | 1.00 | Non-negotiable |
| Timing Margin | 2° | Conservative starting point |
| STFT Warning | ±5% | Typical stock tolerance |
| LTFT Warning | ±5% | Indicates MAF scaling issues |

These defaults are intentionally conservative. The setup wizard will adjust margins based on your specific mod list.

## Disclaimer

This documentation is provided for educational purposes only. Improper ECU tuning can cause engine damage, void warranties, and create unsafe conditions. Always:

- Work with a qualified tuner
- Use appropriate safety margins
- Monitor datalogs for anomalies
- Never exceed safe mechanical limits

**Use at your own risk.** We are not responsible for blown engines. We've never seen one yet, but if you give bad inputs, you'll get bad outputs. You've been warned—use your head.

---

*Built with the WRX community in mind. Contributions welcome.*
