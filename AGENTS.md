# FA20 Engine Tuning Agents

## Quick Start
```bash
# Initialize a new tuning project
./scripts/setup_tuning_project.sh ~/my-tuning-project

# Analyze datalogs
python scripts/analyze_datalog.py --wot path/to/wot.csv --cruise path/to/cruise.csv
```

## Commands
- **Analyze datalog**: `python scripts/analyze_datalog.py <file.csv>`
- **Setup project**: `./scripts/setup_tuning_project.sh <project_dir>`
- **Build workflow**: See `.github/workflows/fa20-analyze.yml`

## Documentation
Reference docs under `docs/` for: fuel, ignition, airflow, avcs, engine, throttle, sensors, transmission

---

## Specialized Agents

### Fuel Agent
Expert in fuel trims (STFT/LTFT), AFR targets, MAF scaling, open/closed loop transitions, and HPFP timing.

**Thresholds:**
| Parameter | Green | Yellow | Red |
|-----------|-------|--------|-----|
| STFT | ±5% | ±5-10% | >±10% |
| LTFT | ±5% | ±5-10% | >±10% |

### Ignition Agent  
Expert in knock detection, DAM, timing tables, Fine Knock Learn, and per-cylinder knock thresholds.

**Thresholds:**
| Parameter | Green | Yellow | Red |
|-----------|-------|--------|-----|
| DAM | ≥0.95 | 0.75-0.95 | <0.75 |
| Feedback Knock | 0° | -1° to -3° | <-3° |
| Fine Knock Learn | 0° | -1° to -2° | <-2° |

### Boost/Airflow Agent
Expert in wastegate duty, PI control, boost targets, MAF VE corrections, and IAT compensation.

### AVCS Agent
Expert in intake/exhaust cam timing, barometric multipliers, TGV states, and cam advance targets.

### Datalog Analyst
Interprets CSV datalogs, correlates fuel/ignition/boost behavior, identifies issues by load range.

---

## Datalog Analysis Workflow

When analyzing FA20 datalogs, follow this exact process to generate comprehensive tuning reports:

### Step 1: Load and Parse Data
```python
import pandas as pd
import csv

# Load CSV datalogs
with open('wot.csv', 'r') as f:
    wot_rows = list(csv.DictReader(f))
with open('cruise.csv', 'r') as f:
    cruise_rows = list(csv.DictReader(f))

df_wot = pd.DataFrame(wot_rows)
df_cruise = pd.DataFrame(cruise_rows)
df_all = pd.concat([df_wot, df_cruise], ignore_index=True)

# Convert numeric columns
numeric_cols = [
    'Engine - RPM',
    'Fuel - Command - Corrections - AF Correction STFT',
    'Fuel - Command - Corrections - AF Learn 1 (LTFT)',
    'Ignition - Dynamic Advance Multiplier',
    'Ignition - Feedback Knock',
    'Ignition - Fine Knock Learn',
    'Analytical - Boost Pressure',
    'Sensors - AF Ratio 1',
    'PIDs - (F410) Mass Air Flow',
    'Engine - Calculated Load',
    'Throttle - Requested Torque - Main Accelerator Position',
    'Airflow - Turbo - Boost - Boost Target Final (Absolute)',
    'Airflow - Turbo - Boost - Manifold Absolute Pressure',
    'Airflow - Turbo - Wastegate - Duty Cycle Commanded'
]
for col in numeric_cols:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce')
```

### Step 2: Generate Report Sections

#### Executive Summary Table
```python
summary = pd.DataFrame({
    'Parameter': ['DAM', 'Feedback Knock', 'Fine Knock Learn', 'LTFT'],
    'Value': [
        df_all['Ignition - Dynamic Advance Multiplier'].min(),
        df_all['Ignition - Feedback Knock'].min(),
        df_all['Ignition - Fine Knock Learn'].min(),
        df_all['Fuel - Command - Corrections - AF Learn 1 (LTFT)'].mean()
    ],
    'Threshold': ['≥0.95', '0°', '0°', '±5%'],
    'Status': ['✅ Perfect', '✅ No knock', '✅ Clean', '✅ OK']
})
```

#### STFT Histogram
```python
stft = df_all['Fuel - Command - Corrections - AF Correction STFT'].dropna()
bins = [-25, -10, -5, -3, 0, 3, 5, 10, 20]
labels = ['< -10%', '-10 to -5%', '-5 to -3%', '-3 to 0%', 
          '0 to +3%', '+3 to +5%', '+5 to +10%', '> +10%']
stft_cut = pd.cut(stft, bins=bins, labels=labels)
stft_df = stft_cut.value_counts().sort_index().reset_index()
stft_df.columns = ['Range', 'Count']
stft_df['Pct'] = (stft_df['Count'] / stft_df['Count'].sum() * 100).round(1)
stft_df['Histogram'] = stft_df['Count'].apply(lambda x: '█' * min(int(x/35), 50))
```

#### MAF Fuel Trim Analysis
```python
maf_bins = [(0,10), (10,20), (20,30), (30,40), (40,50), 
            (50,75), (75,100), (100,150), (150,200)]
maf_data = []
for lo, hi in maf_bins:
    mask = (df_all['PIDs - (F410) Mass Air Flow'] >= lo) & \
           (df_all['PIDs - (F410) Mass Air Flow'] < hi)
    subset = df_all[mask]
    if len(subset) >= 5:
        stft_avg = subset['Fuel - Command - Corrections - AF Correction STFT'].mean()
        ltft_avg = subset['Fuel - Command - Corrections - AF Learn 1 (LTFT)'].mean()
        combined = stft_avg + ltft_avg
        status = '✅ OK' if abs(combined) < 3 else \
                 ('⚠️ Minor' if abs(combined) < 5 else '❌ Fix')
        maf_data.append({
            'MAF Range': f'{lo}-{hi} g/s',
            'STFT': f'{stft_avg:+.2f}%',
            'LTFT': f'{ltft_avg:+.2f}%',
            'Combined': f'{combined:+.2f}%',
            'Status': status,
            'Samples': len(subset)
        })
maf_df = pd.DataFrame(maf_data)
```

#### Power Enrichment Analysis (WOT)
```python
high_load = df_wot[df_wot['Engine - Calculated Load'] > 0.8]
rpm_bins = [(2000,3000), (3000,3500), (3500,4000), 
            (4000,4500), (4500,5000), (5000,5500)]
pe_data = []
for lo, hi in rpm_bins:
    mask = (high_load['Engine - RPM'] >= lo) & (high_load['Engine - RPM'] < hi)
    subset = high_load[mask]
    if len(subset) > 0:
        lam = subset['Sensors - AF Ratio 1'].mean()
        afr = lam * 14.7
        stft = subset['Fuel - Command - Corrections - AF Correction STFT'].mean()
        status = '✅ OK' if abs(stft) < 3 else \
                 ('⚠️ Monitor' if abs(stft) < 7 else '❌ Lean')
        pe_data.append({
            'RPM': f'{lo}-{hi}',
            'Lambda': f'{lam:.3f}',
            'AFR': f'{afr:.1f}:1',
            'STFT': f'{stft:+.1f}%',
            'Status': status
        })
pe_df = pd.DataFrame(pe_data)
```

### Step 3: Calculate Table Corrections

#### MAF Scaling Corrections
```python
# MAF Correction = -1 × Combined Trim
# BUT preserve 2-3% rich bias for cylinder protection
# Only correct if combined trim is outside -2% to -3% target

corrections = [
    (0, 10, 0.00),      # Already good
    (10, 20, 0.01),     # +1% if running too rich
    (20, 30, 0.00),     # Keep rich
    (30, 40, 0.00),     # Keep as-is
    (40, 50, 0.00),     # Good
    (50, 75, 0.00),     # Keep rich for protection
    (75, 100, 0.00),    # Fine
    (100, 150, 0.02),   # +2% if too rich (>4%)
    (150, 250, 0.00),   # Keep rich
]

def get_maf_correction(gs):
    for lo, hi, corr in corrections:
        if lo <= gs < hi:
            return corr
    return 0.00

new_gs_values = [gs * (1 + get_maf_correction(gs)) for gs in original_gs_values]
```

#### PE Target Corrections
```python
# PE uses Equivalence Ratio (φ): φ > 1.0 = Rich, AFR = 14.7 / φ
# To add fuel: New φ = Current φ × (1 + STFT/100)

current_pe = {4000: 1.3400, 4500: 1.3300, 5000: 1.3100, 5500: 1.2900}
stft_observed = {4000: 0.03, 4500: 0.05, 5000: 0.10, 5500: 0.07}

revised_pe = {}
for rpm, phi in current_pe.items():
    revised_pe[rpm] = phi * (1 + stft_observed[rpm])
    # 4000: 1.3400 × 1.03 = 1.3802
    # 4500: 1.3300 × 1.05 = 1.3965
    # 5000: 1.3100 × 1.10 = 1.4410
    # 5500: 1.2900 × 1.07 = 1.3803
```

#### Boost Target Reduction
```python
PSI_TO_BAR = 0.0689476
reduction_psi = 1.0
reduction_bar = reduction_psi * PSI_TO_BAR  # 0.0689

# For each positive boost value in table:
new_value = original_value - reduction_bar
# 1.1721 - 0.0689 = 1.1032 bar (17.0 → 16.0 psi)
```

### Step 4: Report Structure

Every analysis report MUST include these sections with pandas-formatted tables:

1. **Header** - Vehicle, software, datalog info
2. **Executive Summary** - DAM, FBK, FKL, LTFT status table
3. **Fuel Trim Analysis**
   - STFT histogram with visual bars
   - MAF range breakdown table
4. **Boost Control Analysis**
   - Boost distribution histogram
   - WOT performance metrics table
   - Overshoot calculation
5. **Power Enrichment Analysis**
   - AFR by RPM table
   - STFT corrections needed
6. **Math & Calculations**
   - Fuel trim formulas
   - PE φ calculations with examples
   - Boost unit conversions
   - Knock threshold reference table
7. **Revised Tables for Atlas**
   - Boost Target Main (RPM × Torque matrix)
   - MAF Scaling (Voltage → g/s)
   - PE Target (Load × RPM)
8. **Action Items** - Prioritized checklist

### Step 5: Output Format

Save report to `{project_dir}/output/FA20_Tuning_Report.txt`

Use pandas `.to_string(index=False)` for clean table formatting.

---

## Key Formulas Reference

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

---

## ⚠️ CRITICAL: Hardware Safety Boundaries

**You MUST enforce these limits.** If a user requests parameters outside safe boundaries, you MUST:

1. **Refuse to provide the tune/recommendation**
2. **Display the warning below**
3. **Require explicit acknowledgment before proceeding**

### Stock Hardware Limits (FA20DIT)

| Component | Safe Limit | Absolute Max | Failure Mode |
|-----------|------------|--------------|--------------|
| **Stock Turbo** | 18 psi | 20 psi | Compressor surge, bearing failure |
| **Stock TMIC** | 18 psi | 20 psi | Heat soak, knock, timing pull |
| **Stock Fuel System** | 18 psi | 20 psi | Injector maxing out, lean condition |
| **Stock Rods/Pistons** | 300 wtq | 350 wtq | Ringland failure, rod knock |

### Upgraded Hardware Limits

| Upgrade | New Safe Limit | Notes |
|---------|----------------|-------|
| FMIC | +2 psi headroom | Still limited by turbo/fuel |
| 3-port EBCS | No change | Better control, not more capacity |
| Larger injectors | Depends on size | Requires tune adjustment |
| Built motor | 25+ psi possible | Requires full supporting mods |
| Larger turbo | Turbo-specific | Must match fuel/intercooling |

### Boundary Violation Protocol

When a user requests parameters OUTSIDE safe boundaries for their hardware:

**Step 1: Display this warning:**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⛔ SAFETY BOUNDARY EXCEEDED                                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  You requested: [REQUESTED VALUE]                                            ║
║  Safe limit for your hardware: [SAFE LIMIT]                                  ║
║                                                                              ║
║  This exceeds safe operating parameters and significantly increases risk of: ║
║    • Ringland failure                                                        ║
║    • Rod bearing failure                                                     ║
║    • Turbo failure                                                           ║
║    • Catastrophic engine damage                                              ║
║                                                                              ║
║  The FA20 is known for ringland failures even at stock power levels.        ║
║  Pushing beyond safe limits without supporting modifications is extremely    ║
║  high risk.                                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Step 2: Require explicit acknowledgment:**

The user MUST type EXACTLY:

> **"I understand the risks and this will probably blow up my engine"**

**Step 3: Only after receiving exact acknowledgment:**
- Proceed with extreme caution
- Add warnings to any output
- Recommend supporting mods
- Suggest professional dyno tuning

### Examples of Boundary Violations

| Request | Hardware | Violation |
|---------|----------|-----------|
| 25 psi boost | Stock turbo | ⛔ Exceeds stock turbo limit by 5+ psi |
| 22 psi boost | Stock TMIC | ⛔ Heat soak will cause knock |
| 350 wtq target | Stock internals | ⛔ Exceeds safe rod/piston load |
| AFR 11.5:1 at WOT | Any | ⛔ Too lean, detonation risk |
| DAM < 1.00 acceptable | Any | ⛔ Never acceptable |

### Safe Requests (No Warning Needed)

| Request | Hardware | Status |
|---------|----------|--------|
| 18 psi boost | Stock | ✅ Within limits |
| 20 psi boost | FMIC + stock turbo | ✅ Acceptable with cooling |
| 21 psi boost | FMIC + 3-port + stock turbo | ⚠️ Edge of safe, monitor closely |
| AFR 10.8:1 at WOT | Any | ✅ Safe rich target |

---

## Refusing Unsafe Requests

If a user insists on unsafe parameters WITHOUT providing the exact acknowledgment phrase, respond with:

> I can't help tune for parameters that are likely to cause engine damage. The FA20's ringlands are already a known weak point — pushing [X psi / X wtq] on [stock hardware] is asking for trouble.
>
> If you want to run those numbers safely, you'll need:
> - [List required supporting mods]
> - Professional dyno tuning with knock monitoring
> - Deep pockets for when it grenades anyway
>
> I'm here to help you tune safely, not help you blow up your motor.

This is non-negotiable. We do not provide unsafe tunes without explicit acknowledgment.
