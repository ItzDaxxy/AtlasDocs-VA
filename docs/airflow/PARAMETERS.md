# Airflow Runtime Parameters

## Overview

Runtime parameters for airflow measurement, boost control, and intake system monitoring. These parameters are continuously calculated and used throughout the fuel and ignition control systems.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Mass Airflow Corrected** | `float` | g/sec | MAF reading with all corrections applied |
| **Boost Target Table** | `ushort` | bar | Boost pressure target from tables |
| **Corrected VE** | - | % | Volumetric efficiency with corrections |
| **MAF Volumetric Efficiency Correction A** | `ushort` | % | MAF VE correction factor A |
| **MAF Volumetric Efficiency Correction B** | `ushort` | % | MAF VE correction factor B |
| **MAF Volumetric Efficiency Final** | `float` | % | Final calculated MAF volumetric efficiency |
| **Idle Airflow Minimum** | `ushort` | - | Minimum airflow during idle conditions |

## Parameter Details

### Mass Airflow Corrected

**Type:** `float` (floating-point)
**Unit:** g/sec (grams per second)

**Description:**
The final mass airflow value after all corrections have been applied. This is the primary airflow measurement used throughout the ECU for fuel calculations and load determination.

**Corrections Applied:**
- MAF sensor temperature compensation
- Atmospheric pressure correction
- Intake air temperature correction
- MAF scaling/calibration factor
- MAF volumetric efficiency corrections

**Typical Values:**
- Idle: 2-4 g/sec
- Light cruise: 8-15 g/sec
- Moderate acceleration: 20-40 g/sec
- Wide-open throttle: 100-200+ g/sec (depending on boost/modifications)

**Uses:**
- Primary input for fuel injection calculations
- Engine load calculation (g/rev = g/sec ÷ RPM × 120)
- Boost control feedback
- Analytical power estimation

### Boost Target Table

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** bar (absolute pressure)

**Description:**
Target boost pressure looked up from boost control tables based on RPM and load conditions.

**Typical Values:**
- Naturally aspirated: 1.0 bar (atmospheric)
- Stock turbo, low boost: 1.2-1.4 bar (3-6 psi gauge)
- Stock turbo, high boost: 1.5-1.7 bar (7-10 psi gauge)
- Modified turbo: 1.8-2.5+ bar (12-22+ psi gauge)

**Note:** Values are absolute pressure (includes atmospheric ~1 bar)
- Gauge pressure = Absolute pressure - Atmospheric pressure
- 1.5 bar absolute = ~0.5 bar gauge = ~7 psi gauge

**Uses:**
- Reference for closed-loop boost control
- PID control calculates error (Target - Actual)
- Wastegate duty cycle adjusted to achieve target

### MAF Volumetric Efficiency Corrections

**Correction A & B:** `ushort` (percentage)
**Final:** `float` (percentage)

**Description:**
Multi-stage corrections to MAF reading to account for:
- Intake modifications (aftermarket intakes, piping)
- Turbocharger efficiency variations
- Intercooler pressure drop
- Throttle body diameter changes
- Manifold design differences

**Correction A:**
- Primary correction factor
- Typically based on RPM and load
- Accounts for major airflow differences from stock

**Correction B:**
- Secondary correction factor
- May account for temperature or additional conditions
- Fine-tuning adjustment

**Final:**
- Combined result of A × B × base corrections
- Applied to raw MAF reading to get Mass Airflow Corrected

**Tuning:**
- Stock configuration: corrections near 100%
- Larger MAF housing: corrections >100% (e.g., 110-120%)
- Smaller MAF housing: corrections <100% (e.g., 80-90%)
- Incorrect corrections cause:
  - Rich/lean AFR errors
  - Inaccurate load calculations
  - Poor boost control
  - Power loss or engine damage

### Corrected VE

**Type:** Calculated value
**Unit:** % (percentage)

**Description:**
Volumetric efficiency of the engine with corrections for:
- Intake air temperature
- Barometric pressure
- Camshaft timing (AVCS position)
- Throttle position
- Engine wear/carbon buildup

**Typical Values:**
- Naturally aspirated, stock: 85-95%
- Turbocharged, low boost: 90-100%
- Turbocharged, high boost: 100-120%+
- Performance builds: 120-150%+

**Note:** VE >100% indicates forced induction (more air than displacement)

**Uses:**
- Speed-density load calculation (backup to MAF)
- MAF sensor validation (compare MAF-based load to VE-based load)
- Diagnostic tool for intake restrictions or leaks

### Idle Airflow Minimum

**Type:** `ushort`
**Unit:** Dimensionless (likely raw MAF sensor counts or g/sec scaled)

**Description:**
Minimum allowable airflow during idle conditions. Prevents idle airflow from dropping too low, which could cause:
- Rough idle or stalling
- Inability to meet idle speed target
- Excessive idle speed variation

**Typical Behavior:**
- ECU commands throttle to maintain airflow above this minimum
- Electronic throttle opens slightly if airflow drops below limit
- Works with idle speed control to stabilize idle

**Tuning Considerations:**
- Set too high: elevated idle speed, rough idle
- Set too low: potential for stalling, unstable idle
- May need adjustment with:
  - Aggressive camshafts (need higher minimum)
  - Large throttle body (airflow more sensitive to position)
  - Intake restrictions removed (more airflow at given throttle position)

## Boost Control System

### Closed-Loop Boost Control

The ECU uses these parameters for PID-based boost control:

1. **Measure:** Actual boost (from MAP sensor)
2. **Compare:** Boost Target Table vs Actual
3. **Calculate Error:** Target - Actual
4. **PID Controller:** Calculates wastegate duty cycle adjustment
5. **Output:** Wastegate solenoid duty cycle
6. **Result:** Actual boost approaches target

### Feedforward + Feedback

**Feedforward (Open-Loop):**
- Base wastegate duty cycle from tables
- Predicts correct duty cycle for given RPM/load
- Fast response, no delay

**Feedback (Closed-Loop):**
- PID correction based on boost error
- Corrects for variations (temperature, altitude, turbo wear)
- Slower response but accurate

**Combined:**
Final Wastegate Duty = Base Table Value + PID Correction

## MAF Sensor Calibration

### Stock MAF Sensor

- Measures mass airflow directly
- Temperature-compensated hot-wire sensor
- Outputs voltage proportional to airflow
- ECU has lookup table: Voltage → g/sec

### Aftermarket MAF Sensors

When installing larger MAF sensor:

1. **Physical Installation:**
   - Larger diameter housing flows more air
   - Less restriction, improved response
   - Must recalibrate MAF scaling

2. **Calibration Required:**
   - Update MAF voltage→airflow transfer function
   - Adjust MAF VE Corrections A & B
   - May need to rescale Mass Airflow Corrected calculation

3. **Validation:**
   - Compare calculated load to actual engine behavior
   - Verify AFR targets are met across all conditions
   - Ensure boost control remains accurate

### MAF Failure Modes

**Symptoms:**
- Erratic idle, stalling
- Rich or lean AFR across all conditions
- Poor boost control
- Reduced power
- Check engine light (MAF sensor DTC)

**Backup Operation:**
- ECU switches to speed-density mode
- Uses MAP sensor + VE tables for load calculation
- Less accurate than MAF-based calculation
- May run rich or lean depending on calibration

## Related Tables

**Boost Control:**
- Turbo → Boost → Target tables (various conditions)
- Turbo → Wastegate → Duty cycle tables
- Turbo → PI Control → PID gain tables

**MAF Scaling:**
- MAF → Volumetric Efficiency Correction tables
- MAF → Temperature Compensation tables

**Load Calculation:**
- Uses Mass Airflow Corrected ÷ RPM

**Fuel Injection:**
- Uses Mass Airflow Corrected for fuel mass calculation

## Datalogging Recommendations

**Boost Control Tuning:**
- Boost Target Table
- Actual Boost (MAP sensor)
- Boost Error (Target - Actual)
- Wastegate Duty Cycle
- Mass Airflow Corrected
- RPM
- Throttle Position

**MAF Calibration:**
- Mass Airflow Corrected
- MAF Sensor Voltage
- MAF VE Final
- Calculated Load
- AFR (wideband O2 sensor)
- RPM
- Throttle Position

**Idle Stability:**
- Idle Airflow Minimum
- Mass Airflow Corrected
- Throttle Position
- RPM
- Idle Speed Error

## Tuning Notes

### Boost Control

**Stock Boost Target:**
- Conservative for reliability and fuel economy
- Typically 14-18 psi peak (varies by model year)

**Increased Boost:**
- Ensure adequate fuel supply (injectors, pump)
- Monitor AFR carefully (target ~11.5:1 under boost)
- Watch for knock (monitor knock sensors)
- Consider octane requirements (91+ octane recommended)

**Boost Creep:**
- If actual boost exceeds target at high RPM
- Indicates wastegate cannot bypass enough exhaust
- Requires larger wastegate or exhaust housing

### MAF Scaling

**Symptoms of Incorrect MAF Scaling:**
- AFR doesn't match target across load range
- Boost control oscillates or overshoots
- Power delivery feels inconsistent
- Calculated load seems wrong for engine output

**Correction Process:**
1. Log Mass Airflow Corrected and AFR during WOT
2. Compare actual AFR to target AFR
3. If lean: increase MAF VE corrections
4. If rich: decrease MAF VE corrections
5. Adjust in 2-5% increments
6. Retest and iterate

### Idle Airflow

**Symptoms of Incorrect Idle Airflow Minimum:**
- Idle speed hunts up and down
- Stalls when coming to stop
- Idle speed too high (won't drop to target)

**Tuning:**
- Start with stock value
- If idle unstable, increase minimum slightly (2-5%)
- If idle too high, decrease minimum slightly
- Test with A/C on and off (A/C increases idle load)
