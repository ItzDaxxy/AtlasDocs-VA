# Engine Runtime Parameters

## Overview

Core engine runtime parameters used throughout the ECU for load calculations, speed sensing, operating mode detection, and engine protection. These fundamental parameters serve as inputs to nearly all calibration tables.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Displacement** | `scalar` | - | Engine displacement (not directly modifiable) |
| **Calculated Load (Scaled)** | `ubyte` | g/rev | Engine load scaled for specific table ranges |
| **Calculated Load** | `ushort` | g/rev | Primary engine load calculation |
| **Engine Run Time** | `ushort` | seconds | Time since engine start |
| **Idle Switch** | `ubyte` | boolean | Throttle closed/idle position switch state |
| **RPM** | `ushort` | RPM | Engine crankshaft speed |
| **Tachometer RPM** | `ushort` | RPM | RPM value sent to instrument cluster tachometer |
| **Target Engine Speed** | `ushort` | RPM | Target RPM for idle speed control |
| **TGV Map Ratio** | `ushort` | % | Tumble Generator Valve position ratio |
| **Warmup Mode** | `ubyte` | boolean | Engine warmup/cold start mode active |

## Parameter Details

### Calculated Load

**Standard:** `ushort` (unsigned 16-bit integer)
**Scaled:** `ubyte` (unsigned 8-bit integer)
**Unit:** g/rev (grams of air per engine revolution)

**Description:**
The primary engine load parameter used throughout the ECU calibration. Represents the mass of air inducted per engine cycle.

**Calculation:**
```
Calculated Load (g/rev) = Mass Airflow (g/sec) ÷ (RPM ÷ 60 seconds) × (60 sec ÷ 120 revolutions)
Simplified: Load = (MAF × 120) ÷ RPM
```

**Typical Values:**
- Idle: 0.2-0.4 g/rev
- Light cruise: 0.5-1.0 g/rev
- Moderate acceleration: 1.0-2.0 g/rev
- Wide-open throttle, high boost: 2.5-4.0+ g/rev

**Scaled Version:**
- Used in tables with limited resolution
- Typically scaled by factor (e.g., ÷ 16 or ÷ 32)
- Allows larger load range in 8-bit table axes

**Uses:**
- Primary X-axis parameter for most calibration tables
- Fuel injection pulse width calculation
- Ignition timing table lookup
- Boost control target lookup
- Engine protection limits

### RPM

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** RPM (revolutions per minute)
**Source:** Crankshaft position sensor

**Description:**
Fundamental engine speed measurement from crankshaft position sensor. Updated every engine revolution.

**Typical Values:**
- Idle: 650-750 RPM
- Cruise: 2000-3000 RPM
- Peak power: 5500-6500 RPM
- Redline: 6700-6800 RPM
- Rev limiter: 6800-7000 RPM

**Measurement:**
- Crankshaft has toothed wheel (typically 36-2 teeth)
- Missing teeth indicate TDC position for each cylinder
- ECU measures time between teeth to calculate RPM
- Very precise (±10 RPM accuracy)

**Uses:**
- Primary Y-axis parameter for most calibration tables
- Rev limiter threshold
- Idle speed control target
- AVCS enable/disable conditions
- Shift light activation
- Tachometer display

### Tachometer RPM

**Type:** `ushort`
**Unit:** RPM

**Description:**
RPM value transmitted to instrument cluster for tachometer display. Usually identical to actual RPM but may be filtered or adjusted.

**Differences from RPM:**
- May include smoothing filter to reduce needle bounce
- Could be adjusted for gear-specific display (some race applications)
- Typically lags actual RPM by 50-100ms due to CAN bus transmission

**Tuning:**
- Rarely modified
- Some tuners adjust for aesthetic reasons (needle position)
- Can be set to show different value than actual (not recommended)

### Target Engine Speed

**Type:** `ushort`
**Unit:** RPM

**Description:**
Target RPM for idle speed control system. ECU adjusts throttle position and ignition timing to maintain this target.

**Typical Values:**
- Cold idle (coolant <60°C): 1000-1200 RPM
- Warm idle, no load: 650-750 RPM
- Warm idle, A/C on: 750-850 RPM
- Warm idle, heavy electrical load: 700-800 RPM

**Control Strategy:**
- Electronic throttle opens to increase airflow → raise RPM
- Throttle closes to decrease airflow → lower RPM
- Ignition timing advanced slightly for fine RPM control
- Idle valve (if equipped) bypasses throttle for additional air

**Tuning:**
- Increase for rough-running engines (aggressive cams)
- Decrease for fuel economy (if idle is stable)
- Typical adjustment range: ±50 RPM

### Engine Run Time

**Type:** `ushort`
**Unit:** seconds (or seconds ÷ 10 for extended range)

**Description:**
Counter that starts at 0 when engine starts and increments continuously while engine is running.

**Uses:**
- Cold start enrichment decay (reduces over time)
- Warmup mode disable threshold
- AVCS enable delay (wait 2-3 seconds after start)
- Diagnostic timers
- Catalyst warmup monitoring
- Post-start fuel/timing adjustments

**Behavior:**
- Resets to 0 on every engine start
- Maxes out at 65535 seconds (~18 hours) or rolls over
- Not related to total engine operating hours (odometer)

### Idle Switch

**Type:** `ubyte` (boolean: 0 or 1)
**Unit:** On/Off state

**Description:**
Indicates whether throttle is in closed/idle position. Modern drive-by-wire systems use calculated throttle position; older systems used physical switch.

**States:**
- **0 (Off):** Throttle is open (driver requesting power)
- **1 (On):** Throttle is closed (foot off accelerator)

**Uses:**
- Decel fuel cut enable (idle switch on + RPM above threshold)
- Idle speed control activation
- Closed-loop boost control disable
- Overrun condition detection
- Transmission downshift inhibit

**Drive-by-Wire Implementation:**
- No physical switch on electronic throttle
- "Idle switch on" = Accelerator pedal <2% AND Target throttle <5%
- Slight delay (100-200ms) to prevent false triggers

### Warmup Mode

**Type:** `ubyte` (boolean: 0 or 1)
**Unit:** Active/Inactive

**Description:**
Indicates engine is in cold start / warmup operating mode.

**Activation:**
- Engine start with coolant temperature below threshold (typically 60°C / 140°F)

**Deactivation:**
- Coolant temperature exceeds warmup threshold, AND
- Engine run time exceeds minimum (typically 30-60 seconds)

**Effects When Active:**
- Enriched fuel mixture (90-95% of stoich vs 98-100% warm)
- Higher idle speed target (1000-1200 RPM vs 650-750 RPM)
- Modified ignition timing (slightly retarded for catalyst warmup)
- AVCS disabled or limited
- Closed-loop fuel control disabled
- Higher rev limiter threshold (some applications)

**Uses:**
- Cold start emissions control
- Engine protection during warmup
- Improved cold drivability
- Catalyst heating

### TGV Map Ratio

**Type:** `ushort`
**Unit:** % (percentage, 0-100)

**Description:**
Position of Tumble Generator Valves (TGV) in intake manifold. TGVs are butterfly valves that create swirl in combustion chamber at low loads.

**TGV Position:**
- **0%:** Valves closed (maximum tumble/swirl)
- **100%:** Valves fully open (minimum restriction)

**Operating Logic:**
- **Closed (0%):** Low RPM, low load (idle, cruise)
  - Creates tumble for better combustion efficiency
  - Improves fuel economy and emissions
  - Increases intake restriction

- **Open (100%):** High RPM or high load (WOT)
  - Minimizes intake restriction
  - Maximizes airflow for power
  - Reduces pumping losses

**Tuning:**
- Stock calibration is well-optimized
- Some tuners delete TGVs entirely for max flow
- TGV delete requires recalibration (MAF scaling, load calc)
- May hurt low-end torque and fuel economy

### Displacement

**Type:** Scalar constant
**Unit:** Liters (L) or cubic centimeters (cc)

**Description:**
Engine displacement - the swept volume of all cylinders. For FA20DIT: 2.0L (1998 cc)

**Not User-Modifiable:**
- Hard-coded in ECU ROM
- Used for internal calculations (VE, displacement-based load)
- Changing this value would corrupt load calculations

**Theoretical Only:**
- Could be adjusted if engine is bored/stroked to different displacement
- Requires expert-level ECU calibration knowledge
- Incorrect value causes major fueling and load calculation errors

## Load Calculation Methods

### MAF-Based Load (Primary)

```
Calculated Load = (Mass Airflow Corrected × 120) ÷ RPM
```

**Advantages:**
- Direct airflow measurement
- Accounts for boost, modifications automatically
- Accurate across wide range of conditions

**Disadvantages:**
- Relies on accurate MAF calibration
- MAF sensor can fail or become contaminated
- Intake leaks downstream of MAF cause lean condition

### Speed-Density Load (Backup)

```
Calculated Load = (MAP × Displacement × VE) ÷ (IAT × RPM)
```

Where:
- MAP = Manifold Absolute Pressure
- VE = Volumetric Efficiency (from tables)
- IAT = Intake Air Temperature

**Advantages:**
- No MAF sensor required
- More robust to intake leaks
- Can be more accurate with proper VE table calibration

**Disadvantages:**
- Requires extensive VE table calibration
- Less adaptive to modifications
- Sensitive to atmospheric pressure changes

**ECU Operation:**
- Primary: MAF-based load
- Backup: Speed-density if MAF fails or reads out of range
- Cross-check: Compares both methods for sensor validation

## Engine Protection

### Rev Limiter

Prevents engine damage from over-revving:

**Soft Limit (Fuel Cut):**
- Begins at ~6700 RPM
- Cuts fuel to some cylinders
- Allows quick recovery when RPM drops

**Hard Limit (Ignition + Fuel Cut):**
- Activates at ~6800 RPM
- Cuts fuel and retards ignition
- More aggressive limiting for safety

**Tuning:**
- Stock limit appropriate for stock internals
- Increase only with forged internals, upgraded valve springs
- Excessive RPM can cause:
  - Valve float (valves don't close fully)
  - Connecting rod failure
  - Bearing failure

### Speed Limiters

Vehicle speed limiters use RPM and gear calculations:

**Typical Limits:**
- North America: 145 mph (233 km/h) [stock]
- Japan: 112 mph (180 km/h) [stock]
- Germany: 155 mph (250 km/h) [performance models]

**Tuning:**
- Can be removed or raised
- Consider tire speed rating
- Legal implications vary by jurisdiction

## Datalogging Recommendations

**Essential Parameters:**
- RPM
- Calculated Load
- Mass Airflow Corrected
- Throttle Position
- Boost Pressure

**Cold Start Analysis:**
- Warmup Mode
- Engine Run Time
- Coolant Temperature
- Target Engine Speed (idle)
- Actual RPM

**Idle Stability:**
- RPM
- Target Engine Speed
- Idle Switch
- Calculated Load
- Throttle Position

## Related Tables

**All Tables Use:**
- RPM (Y-axis)
- Calculated Load (X-axis)

**Idle Control:**
- Target Engine Speed tables (vs coolant temp, A/C load, electrical load)
- Idle airflow tables

**Rev Limiter:**
- Fuel cut RPM thresholds
- Ignition cut RPM thresholds

**TGV Control:**
- TGV position tables (RPM vs Load)
- TGV transition hysteresis

## Tuning Notes

### Load Calibration

**MAF-Based Systems:**
- Ensure MAF sensor is clean and properly scaled
- Verify MAF VE corrections are accurate
- Compare MAF load to speed-density load for validation

**Speed-Density Systems:**
- Requires extensive VE table calibration
- Must account for altitude, temperature, modifications
- More complex than MAF-based tuning

### Idle Speed

**Stock idle speed is well-optimized for:**
- Fuel economy
- Noise/vibration levels
- A/C compressor load capability
- Alternator output at idle

**Increase idle if:**
- Aggressive camshafts cause rough idle
- Electrical load is high (audio system, lights)
- A/C struggles to maintain compressor speed

**Decrease idle if:**
- Fuel economy is priority
- Engine idles smoothly at lower RPM
- Noise reduction desired

### Warmup Mode

**Stock warmup calibration appropriate for most uses**

**Shorten warmup if:**
- Racing application (don't care about emissions)
- Want faster closed-loop operation
- Cold drivability is acceptable

**Extend warmup if:**
- Cold start drivability issues
- Need more aggressive catalyst heating
- Operating in extremely cold climates

**Caution:** Shortening warmup too much can cause:
- Increased emissions
- Catalyst damage (insufficient heating)
- Cold engine wear
- Poor drivability when cold
