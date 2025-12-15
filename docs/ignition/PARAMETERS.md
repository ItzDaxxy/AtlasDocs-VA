# Ignition System Runtime Parameters

## Overview

Runtime parameters for ignition timing control, knock detection, and coil dwell management. These parameters control spark timing across all engine operating conditions and protect the engine from detonation.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Dynamic Advance Multiplier** | `ubyte` | - | Multiplier for dynamic timing corrections |
| **Feedback Knock** | `sbyte` | ° | Knock-based timing retard |
| **Fine Knock Learn** | `sbyte` | ° | Long-term knock learning value |

## Parameter Details

### Dynamic Advance Multiplier

**Type:** `ubyte` (unsigned 8-bit integer)
**Unit:** Dimensionless multiplier (typically 0-255, scaled to 0-2.0x)

**Description:**
A multiplier applied to dynamic ignition advance corrections. Scales the magnitude of timing adjustments from various sources.

**Typical Value:** 128 (representing 1.0x - no scaling)

**Uses:**
- Scales dynamic advance corrections before applying to base timing
- Can be used to globally adjust responsiveness of timing corrections
- Applied to corrections like:
  - Cold start advance
  - Idle stability advance
  - Transient throttle advance
  - Atmospheric corrections

**Calculation:**
```
Final Dynamic Advance = Base Dynamic Advance × (Multiplier ÷ 128)
```

**Tuning:**
- Rarely modified
- Increase (>128) to make corrections more aggressive
- Decrease (<128) to make corrections more conservative

### Feedback Knock

**Type:** `sbyte` (signed 8-bit integer)
**Unit:** ° (degrees of timing retard)

**Description:**
Real-time ignition timing retard applied in response to knock sensor detection. This is the immediate, short-term response to knock events.

**Typical Values:**
- 0° = No knock detected, no retard applied
- -1° to -3° = Light knock detected, minor retard
- -4° to -8° = Moderate knock, significant retard
- -9° to -15° = Heavy knock, maximum retard

**Negative Values:**
- All values are negative (retard)
- More negative = more retard = less timing advance
- Example: -5° means removing 5° of advance from base timing

**Response Characteristics:**
- **Fast Application:** Retard applied within 1-2 engine cycles of knock detection
- **Slow Recovery:** Timing gradually advances back toward base over 5-30 seconds
- **Cylinder-Specific:** Each cylinder can have independent feedback knock value
- **Cumulative:** Can combine with Fine Knock Learn for total retard

**Recovery Rate:**
- Typical: 0.5-1.0° per second recovery
- Conservative: 0.25° per second
- Aggressive: 1.5-2.0° per second

**Uses:**
- Immediate engine protection from detonation
- Prevents catastrophic knock damage
- Automatic timing adjustment for fuel quality variations
- Compensates for environmental changes (hot day, high altitude)

### Fine Knock Learn

**Type:** `sbyte` (signed 8-bit integer)
**Unit:** ° (degrees of learned timing retard)

**Description:**
Long-term learned ignition timing retard based on persistent knock history. If knock occurs repeatedly in specific operating regions, Fine Knock Learn stores permanent retard for those cells.

**Typical Values:**
- 0° = No learned retard (no knock history in this region)
- -1° to -3° = Occasional knock detected, minor learning
- -4° to -6° = Frequent knock, moderate learning
- -7° to -10° = Severe/persistent knock, maximum learning

**Learning Process:**
1. Knock detected in specific RPM/Load cell
2. Feedback Knock applied immediately
3. If knock repeats multiple times in same cell:
   - Transfer some retard from Feedback Knock to Fine Knock Learn
   - Fine Knock Learn becomes persistent correction
4. Feedback Knock gradually recovers
5. Fine Knock Learn remains until cleared or learned out

**Learning Regions:**
- ECU divides RPM/Load map into learning cells (e.g., 16x16 grid)
- Each cell has independent knock learn value
- Typically 256 learning cells total
- More knock in a specific cell = more learned retard for that cell

**Persistence:**
- Stored in ECU memory (KAM - Keep Alive Memory)
- Survives key cycles and engine restarts
- Only cleared by:
  - Battery disconnect
  - ECU reset
  - Manual clear via tuning software
  - "Learning out" over time with knock-free operation

**Learning Out:**
- If no knock detected in cell for extended period (10-50 engine starts):
  - Fine Knock Learn gradually reduces toward 0°
  - Slow process: typically 0.1-0.5° per hour of operation
  - Allows ECU to re-test timing if conditions improve

**Uses:**
- Long-term adaptation to:
  - Fuel quality (low octane)
  - Altitude changes (less oxygen = hotter combustion)
  - Temperature extremes (hot days increase knock tendency)
  - Carbon buildup (increases compression ratio)
  - Turbo modifications (more boost = more knock risk)
  - Aggressive timing calibration

## Ignition Timing Calculation

### Total Ignition Timing

```
Total Timing = Base Timing + Dynamic Advance - Feedback Knock - Fine Knock Learn
```

**Components:**

1. **Base Timing:** From primary ignition table (RPM vs Load)
2. **Dynamic Advance:** Corrections for cold start, idle, transient, etc.
3. **Feedback Knock:** Immediate knock retard
4. **Fine Knock Learn:** Long-term learned retard

**Example:**
```
Base Timing: 20° BTDC (from table)
Dynamic Advance: +2° (cold start enrichment)
Feedback Knock: -3° (knock just detected)
Fine Knock Learn: -1° (occasional knock history in this cell)

Total Timing = 20 + 2 - 3 - 1 = 18° BTDC
```

### Per-Cylinder Timing

Modern ECUs can adjust timing individually for each cylinder:

- Cylinder 1: Base + Corrections - Knock₁
- Cylinder 2: Base + Corrections - Knock₂
- Cylinder 3: Base + Corrections - Knock₃
- Cylinder 4: Base + Corrections - Knock₄

**Benefits:**
- Compensates for cylinder-to-cylinder variations
- More aggressive timing on cylinders that tolerate it
- Better protection for knock-prone cylinders (typically #4 on FA20)

## Knock Detection System

### Knock Sensors

**Location:**
- Mounted on engine block
- Detect vibrations from detonation
- Typically one sensor per bank (2 sensors total)

**Operation:**
- Piezoelectric sensors generate voltage from vibration
- ECU filters for knock frequency (~6-8 kHz)
- Compares amplitude to threshold tables
- Cylinder-specific knock windows (timing based on crank position)

### Knock Thresholds

**Low Threshold:**
- Sensitive to light knock
- Used during normal operation
- Triggers minor timing retard (1-3°)

**High Threshold:**
- Detects severe knock only
- Used during WOT or high load
- Triggers aggressive retard (5-10°)

**Adaptive Thresholds:**
- ECU learns background noise level
- Adjusts thresholds to filter false knock
- Prevents over-retarding from engine noise

### False Knock

**Sources of False Knock:**
- Exhaust noise (aftermarket exhausts)
- Transmission noise
- Accessory drive noise (A/C compressor, alternator)
- Rod knock (mechanical failure, not detonation)

**ECU Filtering:**
- Frequency filtering (only 6-8 kHz band)
- Timing windows (only listen during compression/combustion)
- Amplitude thresholds
- Pattern recognition (real knock has specific signature)

## Datalogging Recommendations

**Essential Knock Monitoring:**
- Feedback Knock (all 4 cylinders)
- Fine Knock Learn (all 4 cylinders)
- Knock Sum (total retard = Feedback + Learn)
- Base Ignition Timing
- Total Ignition Timing
- Boost Pressure
- AFR
- Coolant Temperature
- Intake Air Temperature

**Advanced Knock Analysis:**
- Knock sensor voltage (raw signal)
- Knock threshold (current threshold level)
- Knock event count (number of knock events detected)
- Knock intensity (severity of knock)

**Critical Monitoring:**
- **Any knock at cruise:** Indicates base timing too aggressive or fuel quality issue
- **Continuous knock at WOT:** Dangerous - back off boost or timing immediately
- **>5° total retard:** Significant issue requiring investigation
- **>10° total retard:** Severe problem, stop driving and diagnose

## Knock Analysis

### Acceptable Knock Levels

**Cruise/Light Load:**
- Feedback Knock: 0°
- Fine Knock Learn: 0-1°
- **Any knock at cruise is unacceptable** - indicates calibration or fuel issue

**Moderate Acceleration:**
- Feedback Knock: 0-2° occasional
- Fine Knock Learn: 0-2°
- Brief knock acceptable, should not persist

**Wide-Open Throttle (WOT):**
- Feedback Knock: 0-3° transient
- Fine Knock Learn: 0-3°
- Occasional light knock acceptable
- Continuous knock indicates problem

**Unacceptable Knock:**
- >5° total retard sustained
- Knock on every WOT pull
- Knock at cruise or idle
- Increasing Fine Knock Learn over time

### Problem Diagnosis

**Consistent Knock in All Cylinders:**
- Base timing too aggressive
- Boost too high for fuel octane
- Lean AFR (check fuel system)
- Intake temps too high (heat soak)
- Low fuel quality (below required octane)

**Knock in Specific Cylinder (e.g., #4):**
- Uneven fuel distribution
- Hot spot in that cylinder
- Carbon buildup
- Leaking injector (rich or lean)
- Weak ignition coil

**Knock After Modifications:**
- Boost increased without timing reduction
- Lean AFR from inadequate fuel
- Intake restriction removed (more airflow = more power = more heat)
- Heat soak from poor intercooler efficiency

**Knock in Hot Weather:**
- Normal - hotter intake air increases knock tendency
- Reduce boost or timing for hot days
- Improve intercooler efficiency
- Consider water/methanol injection

## Related Tables

**Base Timing:**
- Ignition → Primary → Base timing tables (RPM vs Load)
- Ignition → Primary → Idle/Decel timing tables

**Knock Thresholds:**
- Ignition → Knock Thresholds → Low threshold tables
- Ignition → Knock Thresholds → High threshold tables
- Threshold levels per cylinder

**Dynamic Advance:**
- Ignition → Dynamic Advance → Cold start advance
- Ignition → Dynamic Advance → Idle stability advance
- Ignition → Dynamic Advance → Transient advance

**Knock Control:**
- Ignition → Knock Control → Feedback gain
- Ignition → Knock Control → Recovery rate
- Ignition → Knock Control → Learning rate

## Tuning Notes

### Aggressive Timing

**Benefits:**
- More power and torque
- Better throttle response
- Improved fuel economy (at light loads)

**Risks:**
- Increased knock tendency
- Engine damage if knock is severe/sustained
- Requires higher octane fuel
- Less margin for error (fuel quality, hot days)

**Safe Approach:**
1. Start conservative (stock timing or slightly less)
2. Add timing in small increments (1-2° at a time)
3. Monitor knock carefully (datalog every change)
4. Back off at first sign of knock
5. Leave safety margin (don't tune to the edge of knock)

### Timing vs Boost

**More Boost = Less Timing:**
- Higher cylinder pressure increases knock tendency
- Typical: Remove 1-2° timing per 2-3 psi boost increase
- Stock timing tables designed for stock boost
- Must reduce timing when increasing boost

**Safe Combinations (FA20DIT):**
- Stock boost (~15 psi): Stock timing
- +3 psi boost: -2° timing
- +6 psi boost: -4° timing
- +10 psi boost: -6 to -8° timing

### Fuel Octane Requirements

**Stock Calibration:**
- Designed for 91 octane (North America)
- Can run 87 octane with knock retard (not recommended)
- 93 octane provides small safety margin

**Modified Calibration:**
- +3-5 psi boost: 91 octane minimum
- +6-10 psi boost: 93 octane recommended
- +10+ psi boost: E85 or race gas (100+ octane)

**E85 Benefits:**
- Effective octane ~105
- Cooling effect from ethanol evaporation
- Allows more aggressive timing and boost
- Requires 30% more fuel (larger injectors/pump)

### Knock Learning Reset

**When to Clear Knock Learn:**
- After fixing knock problem (fuel, calibration, mechanical)
- After switching to higher octane fuel
- After reducing boost pressure
- After improving intercooler efficiency

**How to Clear:**
1. Disconnect battery for 10+ minutes, OR
2. Use tuning software to clear learned values, OR
3. ECU reset procedure (specific to vehicle)

**After Clearing:**
- ECU will re-learn timing over ~50-100 starts
- Monitor knock closely during re-learning period
- New learned values should be near 0° if problems resolved

### Cylinder 4 Knock

**Common Issue:**
- Cylinder 4 tends to knock more than others
- Farthest from intercooler (hottest intake charge)
- Leanest cylinder on port injection systems
- Most heat-soaked cylinder

**Solutions:**
- Verify AFR in all cylinders (check injectors)
- Improve intercooler efficiency (larger IC, better flow)
- Add per-cylinder timing trim (reduce cyl 4 timing 2-3°)
- Verify coolant flow is adequate
- Check for vacuum leaks affecting cylinder 4
