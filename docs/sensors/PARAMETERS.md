# Sensor Runtime Parameters

## Overview

Runtime parameters for engine sensor calibration and monitoring. These parameters represent sensor readings and calibration values used throughout the ECU for engine management.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **AF Ratio 1** | `ushort` | λ | Air/fuel ratio sensor 1 reading |
| **Barometric Pressure** | `ushort` | psi | Atmospheric barometric pressure |
| **Delivery Mode OEM** | `ubyte` | - | OEM fuel delivery mode indicator |
| **Intake Manifold Temperature** | `ubyte` | °C | Temperature of air in intake manifold |

## Parameter Details

### AF Ratio 1

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** λ (lambda) - air/fuel equivalence ratio

**Description:**
Primary air/fuel ratio sensor (O2 sensor) reading. This is the measured AFR from sensor 1, typically the upstream sensor (before catalytic converter).

**Lambda Values:**
- **λ = 1.00:** Stoichiometric ratio (14.7:1 for gasoline)
- **λ < 1.00:** Rich mixture (more fuel)
- **λ > 1.00:** Lean mixture (less fuel)

**Sensor Types:**

**Narrowband O2 Sensor (Stock):**
- Switches voltage around stoichiometric (0.1-0.9V)
- Only accurate at λ = 1.00
- Cannot measure actual AFR when rich or lean
- Used for closed-loop cruise fuel control
- Not adequate for WOT tuning

**Wideband O2 Sensor (Aftermarket):**
- Linear output across λ = 0.65 to 1.30 (approx 9.5:1 to 19:1)
- Accurate AFR measurement at all conditions
- Essential for performance tuning
- Required for WOT fuel calibration

**Typical Values:**
- Idle (closed-loop): λ = 1.00 (14.7:1)
- Cruise (closed-loop): λ = 1.00-1.02 (14.7-15.0:1)
- Light accel (open-loop): λ = 0.95-1.00 (14.0-14.7:1)
- WOT (power enrichment): λ = 0.75-0.85 (11.0-12.5:1)

**Uses:**
- Closed-loop fuel control feedback
- Fuel trim calculation (STFT/LTFT)
- Catalyst monitoring
- Emissions compliance
- Performance tuning validation

**Conversion:**
```
AFR = λ × 14.7 (for gasoline)
λ = AFR ÷ 14.7

Examples:
λ = 0.80 → AFR = 11.76:1 (rich, WOT)
λ = 1.00 → AFR = 14.7:1 (stoich, cruise)
λ = 1.05 → AFR = 15.4:1 (lean, economy)
```

### Barometric Pressure

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** psi (pounds per square inch, absolute)

**Description:**
Atmospheric pressure measured by barometric pressure sensor (or calculated from MAP sensor at key-on). Used for altitude compensation throughout ECU calibration.

**Typical Values:**
- Sea level: 14.7 psi (101.3 kPa, 1.013 bar)
- 3000 ft elevation: 13.2 psi (91.0 kPa)
- 5000 ft elevation: 12.2 psi (84.1 kPa)
- 8000 ft elevation: 10.9 psi (75.1 kPa)

**Measurement Methods:**

**Dedicated Baro Sensor:**
- Some ECUs have standalone barometric pressure sensor
- Continuously updated atmospheric pressure
- Most accurate method

**MAP Sensor at Key-On:**
- More common implementation
- When engine is off, manifold pressure = atmospheric
- ECU samples MAP sensor at key-on before engine start
- Stores value as barometric pressure
- Used until next key cycle

**GPS-Based (Advanced Systems):**
- Calculate altitude from GPS
- Lookup atmospheric pressure from altitude
- Useful for rapidly changing altitude (mountain driving)

**Uses:**
- **Boost Control:** Corrects boost targets for altitude
- **Fuel Delivery:** Adjusts fuel for air density changes
- **Ignition Timing:** Altitude correction for timing
- **Load Calculation:** Corrects calculated load for atmospheric density
- **Turbo Control:** Prevents overboost at altitude
- **Power Estimation:** Accounts for altitude in dyno calculations

**Altitude Effects:**

**Lower Air Density:**
- Less oxygen available for combustion
- Naturally aspirated: Direct power loss (~3% per 1000 ft)
- Turbocharged: Compensates via higher boost, but turbo works harder

**Knock Tendency:**
- Thinner air = less knock tendency (good)
- Can run slightly more aggressive timing at altitude
- Opposite at sea level (more knock tendency)

**Boost Control:**
- Wastegate sees less exhaust pressure at altitude
- Turbo may struggle to reach target boost
- ECU may increase wastegate duty cycle to compensate

### Delivery Mode OEM

**Type:** `ubyte` (unsigned 8-bit integer / enumeration)
**Unit:** Mode identifier

**Description:**
OEM fuel delivery mode indicator. Specifies which fuel injection system is active (port injection, direct injection, or both).

**FA20DIT Dual Injection:**
The FA20DIT engine has both port injection (PI) and direct injection (DI):

**Port Injection (PI):**
- Fuel injected into intake port
- Better fuel atomization and mixing
- Cools intake valves (prevents carbon buildup)
- Lower pressure system (~60 psi)

**Direct Injection (DI):**
- Fuel injected directly into combustion chamber
- Better volumetric efficiency (more air in cylinder)
- Improved anti-knock properties (cooling effect)
- Higher pressure system (~2000 psi)

**Delivery Modes:**

**Mode 0 - Port Injection Only:**
- All fuel from port injectors
- Used during cold start (better mixing)
- Low load conditions
- DI system priming

**Mode 1 - Direct Injection Only:**
- All fuel from direct injectors
- Used during high load (maximum power)
- Better anti-knock at WOT

**Mode 2 - Dual Injection:**
- Combination of PI and DI
- Typical split: 30-50% PI, 50-70% DI
- Varies with load, RPM, temperature
- Optimizes benefits of both systems

**Mode Selection Logic:**
```
IF coolant temp < 60°C THEN Port Injection Only
ELSE IF low load AND cruise THEN Port Injection Only
ELSE IF high load AND WOT THEN Direct Injection Only
ELSE Dual Injection (blended)
```

**Injection Ratio Tables:**
- ECU has tables for PI/DI split vs RPM and load
- More PI at low loads (intake valve cleaning)
- More DI at high loads (anti-knock benefit)

### Intake Manifold Temperature

**Type:** `ubyte` (unsigned 8-bit integer)
**Unit:** °C (degrees Celsius)

**Description:**
Temperature of air in the intake manifold, measured by IAT (Intake Air Temperature) sensor or MAT (Manifold Air Temperature) sensor.

**Sensor Location:**
- Mounted in intake manifold
- Measures post-intercooler air temperature
- Sometimes combined with MAP sensor (TMAP sensor)

**Typical Values:**
- Ambient temp (no boost, no heat soak): 20-30°C (68-86°F)
- After intercooler (moderate boost): 30-50°C (86-122°F)
- After intercooler (high boost): 50-70°C (122-158°F)
- Heat soaked (traffic, idling): 60-80°C (140-176°F)
- Extreme heat soak: 80-100°C+ (176-212°F+)

**Ideal Target:**
- As close to ambient as possible
- <40°C is excellent
- 40-60°C is acceptable
- >60°C indicates intercooler inefficiency or heat soak

**Effects on Engine:**

**Hotter Intake Air:**
- Lower air density (less oxygen per volume)
- Increased knock tendency (hotter combustion temps)
- Reduced power output (~1% per 5°C increase)
- ECU may reduce boost or retard timing

**Cooler Intake Air:**
- Higher air density (more oxygen)
- Reduced knock tendency
- More power potential
- Can run more aggressive timing/boost

**Uses:**
- **Fuel Correction:** Adjust fuel delivery for air density
- **Ignition Timing:** Retard timing if intake temps too high
- **Boost Control:** Reduce boost if temps excessive
- **Load Calculation:** Correct load for temperature effects
- **Knock Protection:** More conservative timing when hot

**Temperature Corrections:**

**Fuel Delivery:**
```
Fuel Correction = (Base Temp ÷ Actual Temp) ^ 0.5
Hotter air = less fuel needed (less dense)
Colder air = more fuel needed (more dense)
```

**Ignition Timing:**
```
Timing Retard = (Temp - Base Temp) × Correction Factor
Every 10°C above base: -1 to -2° timing
Prevents knock when intake temps elevated
```

**Boost Control:**
```
IF Intake Temp > 70°C THEN Reduce boost target by 2-4 psi
Protects engine from knock when heat soaked
```

## Sensor Calibration

### O2 Sensor Calibration

**Narrowband O2:**
- Factory calibrated
- No user adjustment needed
- Replacement sensors are pre-calibrated

**Wideband O2:**
- Requires calibration procedure (free-air calibration)
- Must be performed periodically (every 10,000-20,000 miles)
- Incorrect calibration causes AFR reading errors

**Wideband Free-Air Calibration:**
1. Engine off, sensor at operating temperature
2. Expose sensor to ambient air (λ = 1.00 × atmospheric O2 ratio)
3. Sensor learns voltage offset for ambient air
4. Stores calibration in controller memory

### Barometric Pressure Calibration

**MAP-Based Baro:**
- Uses MAP sensor calibration (see MAP sensor)
- Sampled at key-on, engine off
- Accuracy depends on MAP sensor accuracy

**Dedicated Baro Sensor:**
- Factory calibrated
- Typically no drift over time
- Replacement sensors are pre-calibrated

**Validation:**
- Compare to known altitude
- Sea level should read ~14.7 psi
- 5000 ft should read ~12.2 psi

### Intake Air Temperature Calibration

**Thermistor-Based:**
- Resistance changes with temperature
- ECU has lookup table: Resistance → Temperature
- Factory calibrated, no user adjustment

**Accuracy:**
- Typically ±2°C
- Can drift with age or contamination
- Check against known temperature source

**Common Issues:**
- Heat soak from engine bay (sensor reads high)
- Poor sensor location (not representative of actual intake temp)
- Corroded connector (erratic readings)

## Datalogging Recommendations

**Essential Sensor Monitoring:**
- AF Ratio 1 (wideband O2)
- Barometric Pressure
- Intake Manifold Temperature
- Coolant Temperature
- Engine Oil Temperature

**AFR Tuning:**
- AF Ratio 1 (actual)
- Command Fuel Final (target)
- AFR Error (target - actual)
- Fuel trims (STFT/LTFT)
- RPM and Load

**Boost/Intercooler Efficiency:**
- Intake Manifold Temperature
- Ambient Air Temperature
- Boost Pressure
- Intercooler efficiency = (Ambient Temp - Manifold Temp) / (Ambient Temp - Compressed Air Temp)

**Altitude Compensation:**
- Barometric Pressure
- Calculated Load
- Boost Pressure (absolute)
- Compare sea level vs altitude datalogs

## Related Tables

**O2 Sensor:**
- Fuel → Closed Loop → Lambda targets
- Fuel → Closed Loop → PI control gains
- Fuel → Corrections → AFR vs temperature

**Barometric Pressure:**
- Airflow → Corrections → Altitude correction
- Ignition → Corrections → Altitude correction
- Fuel → Corrections → Density correction

**Intake Temperature:**
- Fuel → Corrections → IAT correction
- Ignition → Corrections → IAT timing retard
- Boost → Corrections → IAT boost reduction

## Tuning Notes

### AFR Monitoring

**Wideband O2 Essential:**
- Stock narrowband O2 inadequate for WOT tuning
- Install wideband O2 sensor for performance applications
- Mount in exhaust upstream of turbo or cat

**Target AFR:**
- Cruise: 14.7:1 (λ = 1.00)
- Part throttle: 13.5-14.7:1 (λ = 0.92-1.00)
- WOT, moderate boost: 11.5-12.5:1 (λ = 0.78-0.85)
- WOT, high boost: 11.0-11.5:1 (λ = 0.75-0.78)

**Danger Zones:**
- Lean cruise (>15:1): Poor drivability, potential misfire
- Lean WOT (>13:1): Detonation risk, engine damage
- Excessive rich (<10.5:1): Power loss, plug fouling

### Intercooler Efficiency

**Measuring Efficiency:**
```
Efficiency % = (T_ambient - T_manifold) / (T_ambient - T_compressor) × 100

Where:
T_compressor = Ambient × (Boost Pressure Ratio) ^ 0.283
```

**Example:**
- Ambient: 25°C
- Boost: 1.5 bar absolute (0.5 bar gauge)
- Manifold temp: 50°C
- Compressor outlet (calculated): 80°C

```
Efficiency = (25 - 50) / (25 - 80) × 100 = 45%
```

**Intercooler Efficiency Targets:**
- Excellent: 70-80%
- Good: 60-70%
- Acceptable: 50-60%
- Poor: <50% (upgrade needed)

**Improving Efficiency:**
- Larger intercooler
- Better airflow (remove restrictions)
- Water spray (track use)
- Front-mount vs top-mount design

### Altitude Tuning

**High Altitude Effects:**
- Less available oxygen
- Lower boost pressure (absolute)
- Reduced knock tendency
- Power loss (NA engines)

**Compensation Strategies:**
- Increase wastegate duty (reach target boost)
- Slightly more aggressive timing (less knock)
- Verify AFR still on target (may go slightly lean)

**Datalogging Comparison:**
- Log at sea level
- Log at altitude
- Compare: boost, timing, knock, AFR
- Adjust calibration if needed
