# Fuel System Runtime Parameters

## Overview

Runtime parameters for fuel injection control, fuel system monitoring, and operating mode management. These parameters control fuel delivery across all engine operating conditions.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Command Fuel Final** | `ushort` | λ | Final commanded fuel equivalence ratio |
| **Fuel Mode** | `ubyte` | - | Current fuel operating mode |
| **Startup Fuel Mode** | `ubyte` | - | Fuel mode during engine start |
| **AF Correction 1** | `ushort` | % | Air/fuel ratio correction factor 1 |
| **AF Correction STFT** | `ushort` | % | Short-term fuel trim correction |
| **AF Learn 1** | `ubyte` | % | Long-term fuel trim learning value 1 |

## Parameter Details

### Command Fuel Final

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** λ (lambda) - fuel equivalence ratio

**Description:**
The final commanded air/fuel ratio expressed as lambda (λ). This is the target AFR that the ECU attempts to achieve through fuel injection control.

**Lambda Values:**
- **λ = 1.00:** Stoichiometric (14.7:1 for gasoline)
- **λ < 1.00:** Rich (more fuel than stoich)
- **λ > 1.00:** Lean (less fuel than stoich)

**Typical Values:**
- Idle: λ = 1.00 (14.7:1)
- Light cruise: λ = 1.00-1.02 (14.7-15.0:1)
- Moderate acceleration: λ = 0.90-0.95 (13.2-14.0:1)
- Wide-open throttle (high boost): λ = 0.75-0.85 (11.0-12.5:1)
- Decel fuel cut: λ = ∞ (no fuel)

**Conversion:**
- AFR = λ × 14.7 (for gasoline)
- λ = AFR ÷ 14.7

**Uses:**
- Primary target for fuel injection calculation
- Combined with airflow to determine fuel mass
- Closed-loop fuel control uses this as reference

### Fuel Mode

**Type:** `ubyte` (unsigned 8-bit integer / enumeration)
**Unit:** Mode identifier

**Description:**
Indicates current fuel system operating mode. Each mode has different fuel control strategies.

**Common Modes:**
- **0 - Open Loop:** No O2 sensor feedback, uses tables only
- **1 - Closed Loop:** Using O2 sensor feedback for fuel correction
- **2 - Decel Fuel Cut:** Fuel completely shut off during deceleration
- **3 - Cranking:** Fuel enrichment during engine cranking
- **4 - Warmup Enrichment:** Cold engine enrichment active
- **5 - Power Enrichment:** WOT enrichment for maximum power
- **6 - Idle:** Special idle fuel control mode

**Mode Selection Logic:**
```
IF engine cranking THEN Cranking Mode
ELSE IF coolant temp < threshold THEN Warmup Mode
ELSE IF decel conditions met THEN Decel Fuel Cut
ELSE IF WOT THEN Power Enrichment
ELSE IF closed-loop conditions met THEN Closed Loop
ELSE Open Loop
```

**Uses:**
- Determines which fuel tables and corrections are active
- Controls whether O2 sensor feedback is used
- Affects fuel cut behavior

### Startup Fuel Mode

**Type:** `ubyte`
**Unit:** Mode identifier

**Description:**
Specific fuel mode active during engine cranking and initial startup. Ensures proper fuel delivery for reliable starting.

**Features:**
- Heavy enrichment (λ = 0.70-0.85 depending on temperature)
- No O2 sensor feedback
- Cranking pulse width vs coolant temperature table
- Prime pulse on key-on (fuel system pressurization)

**Temperature Compensation:**
- Very cold (<-10°C): Maximum enrichment
- Cold (0-20°C): Moderate enrichment
- Warm (20-60°C): Light enrichment
- Hot (>60°C): Minimal enrichment

**Transition:**
- Startup mode → Warmup mode after engine starts
- Typically 1-3 seconds after RPM stabilizes

### AF Correction 1

**Type:** `ushort`
**Unit:** % (percentage correction)

**Description:**
Primary air/fuel ratio correction factor applied to base fuel calculation. Modifies fuel delivery to account for specific operating conditions.

**Application:**
```
Corrected Fuel = Base Fuel × (AF Correction 1 ÷ 100)
```

**Typical Values:**
- 100% = No correction (base fuel)
- >100% = Enrichment (more fuel)
- <100% = Enleanment (less fuel)

**Common Corrections:**
- Atmospheric pressure compensation: 95-105%
- Intake air temperature compensation: 95-105%
- Battery voltage compensation: 98-102%
- Ethanol content compensation: 100-130%

**Multiple Correction Factors:**
- AF Correction 1 (primary/atmospheric)
- AF Correction 2 (temperature)
- AF Correction 3 (voltage/pressure)
- All multiplied together for total correction

### AF Correction STFT (Short-Term Fuel Trim)

**Type:** `ushort`
**Unit:** % (percentage correction)

**Description:**
Real-time fuel correction based on O2 sensor feedback during closed-loop operation. Adjusts fuel delivery to maintain target lambda.

**Operation:**
1. Measure actual lambda (from wideband O2 sensor)
2. Compare to Command Fuel Final (target lambda)
3. Calculate error: Target - Actual
4. Adjust STFT to correct error

**Typical Range:**
- ±15% during normal operation
- 0% = No correction needed (perfect base fuel)
- +10% = Adding 10% fuel (base map is lean)
- -10% = Removing 10% fuel (base map is rich)

**Fast Response:**
- Updates at 10-50 Hz
- Responds to rapid changes in operating conditions
- Resets to 0% when conditions change significantly

**Uses:**
- Immediate correction for fuel delivery errors
- Compensates for:
  - Intake air temperature changes
  - Barometric pressure variations
  - Fuel quality differences
  - Minor vacuum leaks
  - Sensor drift

### AF Learn 1 (Long-Term Fuel Trim)

**Type:** `ubyte`
**Unit:** % (percentage correction)

**Description:**
Learned fuel correction that adapts over time based on persistent STFT values. Compensates for long-term changes in engine/fuel system.

**Learning Process:**
1. Monitor STFT over time in specific operating region
2. If STFT consistently non-zero (e.g., +8% for 2+ minutes)
3. Gradually transfer STFT correction to LTFT (AF Learn 1)
4. STFT returns toward 0% as LTFT takes over correction

**Typical Range:**
- ±20-25% total learning capability
- Well-tuned engine: ±5%
- Significant deviation indicates:
  - Base fuel calibration error
  - Mechanical problem (vacuum leak, injector issue)
  - Sensor drift (MAF, MAP)

**Learning Regions:**
- Multiple learned values for different RPM/load cells
- Idle learn, cruise learn, light load learn
- Separate learning for different operating conditions

**Persistence:**
- Stored in ECU memory (KAM - Keep Alive Memory)
- Survives key cycles
- Reset by ECU power loss or manual clear (battery disconnect)

**Uses:**
- Long-term adaptation to:
  - Injector wear/clogging
  - MAF sensor contamination
  - Fuel pump wear
  - Air filter restriction
  - Altitude/climate changes

## Fuel System Control Logic

### Base Fuel Calculation

```
Base Fuel (ms) = (Calculated Load × λ × Stoich Fuel Mass) ÷ (Injector Flow Rate)
```

Where:
- Calculated Load = Mass of air per engine cycle (g/rev)
- λ = Target lambda (Command Fuel Final)
- Stoich Fuel Mass = Air mass ÷ 14.7 (for λ=1.0)

### Total Corrections

```
Final Fuel = Base Fuel × AF Correction 1 × AF Correction 2 × ... × STFT × LTFT
```

### Injector Pulse Width

```
Pulse Width (ms) = Final Fuel + Injector Offset

Where Injector Offset accounts for:
- Injector opening delay
- Injector closing delay
- Voltage compensation
```

## Closed-Loop Fuel Control

### Enable Conditions

Closed-loop (O2 feedback) active when ALL conditions met:

- Engine coolant temperature > 60°C (140°F)
- O2 sensors at operating temperature (>300°C)
- Engine run time > 30-60 seconds
- Not in WOT (throttle < 90%)
- RPM stable (not rapidly changing)
- Load stable (not rapid acceleration/decel)
- No relevant DTCs (O2 sensor, MAF, MAP faults)

### Disable Conditions

Switches to open-loop when:
- Cold engine (coolant temp low)
- Wide-open throttle (WOT)
- Decel fuel cut active
- Rapid throttle changes (tip-in, tip-out)
- High load (boost above threshold)
- O2 sensor fault detected

### Proportional-Integral (PI) Control

**Proportional:**
- Immediate correction proportional to error
- Fast response to AFR deviations
- Can cause oscillation if too aggressive

**Integral:**
- Accumulated correction over time
- Eliminates steady-state error
- Slower response, more stable

**Combined:**
- P correction handles quick changes
- I correction handles steady-state offset
- Optimized gains prevent oscillation

## Fuel Trims Analysis

### Healthy Fuel System

**Short-Term Fuel Trim (STFT):**
- Oscillates around 0% (±2-3%)
- Quick response to throttle changes
- Returns to 0% in steady-state

**Long-Term Fuel Trim (LTFT):**
- Stable at 0-5% correction
- Minimal change over time
- Similar values across operating regions

### Problem Indicators

**Large Positive STFT (+10% or more):**
- Base fuel calibration too lean
- Vacuum leak (unmeasured air)
- MAF sensor reading low (dirty, failing)
- Low fuel pressure
- Clogged injectors

**Large Negative STFT (-10% or more):**
- Base fuel calibration too rich
- MAF sensor reading high (contaminated)
- High fuel pressure
- Leaking injectors
- Rich fuel pressure regulator setting

**Large LTFT (>±10%):**
- Persistent problem in that operating region
- Base fuel map needs correction
- Sensor calibration issue
- Mechanical problem

**LTFT at limit (±20-25%):**
- Severe fuel system problem
- ECU has reached maximum correction capability
- Check engine light likely (fuel system lean/rich DTC)

## Datalogging Recommendations

**Fuel System Health:**
- Command Fuel Final (target)
- Actual AFR (from wideband O2)
- AF Correction STFT
- AF Learn 1 (LTFT)
- Fuel Mode
- RPM
- Calculated Load

**Fuel Trim Analysis:**
- Plot STFT vs time (should oscillate around 0%)
- Plot LTFT vs RPM/Load (should be flat, near 0%)
- Large deviations indicate calibration or mechanical issues

**Cold Start:**
- Startup Fuel Mode
- Coolant Temperature
- Commanded AFR
- Actual AFR
- Cranking time to start

## Related Tables

**Base Fuel:**
- Fuel → Command → Target lambda tables (RPM vs Load)
- Fuel → Injector → Pulse width tables

**Corrections:**
- Fuel → Command → Corrections → Temperature
- Fuel → Command → Corrections → Atmospheric pressure
- Fuel → Command → Corrections → Battery voltage

**Closed-Loop:**
- Fuel → Closed Loop → PI gains
- Fuel → Closed Loop → Enable thresholds
- Fuel → Closed Loop → Lambda targets

**Cold Start:**
- Fuel → Startup → Cranking pulse width vs temperature
- Fuel → Startup → Prime pulse
- Fuel → Warmup → Enrichment decay

## Tuning Notes

### Wideband O2 Sensor Essential

**Stock narrowband O2:**
- Only indicates rich/lean (binary)
- Cannot measure actual AFR
- Sufficient for closed-loop correction
- Not adequate for WOT tuning

**Wideband O2:**
- Measures actual AFR (10:1 to 20:1 range)
- Essential for performance tuning
- Allows precise WOT fuel calibration
- Recommended for any modified vehicle

### WOT Fuel Targets

**Naturally Aspirated:**
- λ = 0.85-0.90 (12.5-13.2 AFR)
- Richer at peak torque, leaner at peak power

**Turbocharged:**
- λ = 0.75-0.85 (11.0-12.5 AFR)
- Richer with higher boost
- Cooling effect prevents detonation

**Too Lean (<11:1):**
- Risk of detonation (knock)
- Piston damage possible
- EGT too high

**Too Rich (>13:1 at high boost):**
- Power loss
- Wasted fuel
- Excessive EGT
- Catalyst damage

### Base Map Calibration

**Process:**
1. Disable closed-loop (force open-loop)
2. Tune base fuel tables to achieve target AFR
3. Verify across all RPM/load regions
4. Re-enable closed-loop
5. Monitor fuel trims - should be near 0%

**Goal:**
- STFT: ±5% or less
- LTFT: ±5% or less
- If trims are large, base map needs correction

### Fuel Pressure

**Stock fuel pressure:**
- Port injection: ~43 psi (3 bar) base
- Direct injection: ~2000 psi (140 bar)

**Increased fuel pressure:**
- Common modification with larger injectors
- Increases injector flow rate
- Requires recalibration of injector scaling
- Check fuel pump capacity

**Fuel Pressure Regulator:**
- Manifold-referenced (1:1 with boost)
- Maintains constant pressure differential across injectors
- Ensures consistent fueling across all boost levels
