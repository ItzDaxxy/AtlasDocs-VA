# Transmission Runtime Parameters

## Overview

Runtime parameters for transmission control, gear detection, and vehicle speed calculation. These parameters are used for shift scheduling, speed limiting, and gear-dependent calibration.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Vehicle Speed Scalar A** | `scalar` | - | Primary vehicle speed scaling factor |
| **Vehicle Speed Scalar B** | `scalar` | - | Secondary vehicle speed scaling factor |
| **Current Gear** | `ubyte` | - | Currently engaged transmission gear |
| **Gear Speed** | `ushort` | rev/mi | Gear rotational speed in revolutions per mile |
| **Vehicle Speed** (kmh, ubyte) | `ubyte` | km/h | Vehicle speed (8-bit, limited range) |
| **Vehicle Speed** (kmh, ushort) | `ushort` | km/h | Vehicle speed (16-bit, full range) |
| **Vehicle Speed A** | `ushort` | - | Vehicle speed calculation A |
| **Vehicle Speed B** | `ushort` | - | Vehicle speed calculation B |
| **Vehicle Speed C** | `ushort` | - | Vehicle speed calculation C |
| **Vehicle Speed Canbus** | `ushort` | - | Vehicle speed transmitted over CAN bus |
| **Vehicle Speed D** | `ushort` | - | Vehicle speed calculation D |

## Parameter Details

### Vehicle Speed Scalars

**Type:** Scalar (fixed calibration values)
**Unit:** Dimensionless scaling factors

**Description:**
Calibration scalars used to convert transmission output shaft speed (or wheel speed sensor) to vehicle speed in km/h or mph.

**Purpose:**
- Accounts for tire diameter
- Accounts for final drive ratio
- Accounts for transmission output shaft ratio
- Converts sensor frequency to speed units

**Calculation:**
```
Vehicle Speed = (Transmission Output RPM × 60 min/hr) ÷ (Tire Revolutions per Mile × Scalar A × Scalar B)

Or simplified:
Vehicle Speed = Sensor Frequency × Scalar A × Scalar B
```

**When to Recalibrate:**
- **Tire Size Change:** Larger/smaller tires change revolutions per mile
- **Final Drive Change:** Different differential ratio
- **Speedometer Correction:** If speedometer reads incorrectly

**Example:**

Stock tire: 225/45R17
- Diameter: 24.97 inches
- Circumference: 78.4 inches
- Revolutions per mile: 5280 × 12 ÷ 78.4 = 808 rev/mile

Larger tire: 245/40R18
- Diameter: 25.67 inches
- Circumference: 80.6 inches
- Revolutions per mile: 787 rev/mile

**Speed error:** 787 ÷ 808 = 0.974 (2.6% slow reading)

**Correction:** Multiply Scalar A or B by 0.974 to correct speedometer

### Current Gear

**Type:** `ubyte` (unsigned 8-bit integer / enumeration)
**Unit:** Gear number (0-6)

**Description:**
Currently engaged transmission gear, detected by the ECU based on vehicle speed, RPM, and transmission sensors.

**Gear Values:**
- **0:** Neutral or Park
- **1:** First gear
- **2:** Second gear
- **3:** Third gear
- **4:** Fourth gear
- **5:** Fifth gear
- **6:** Sixth gear (6-speed manual) or Reverse

**Detection Methods:**

**Manual Transmission:**
- Calculate gear from: Gear = RPM ÷ (Vehicle Speed × Final Drive × Gear Ratio)
- Compare to known gear ratios
- Select closest match
- May have dedicated gear position sensor (some models)

**Automatic Transmission (CVT):**
- Transmission control module reports gear over CAN bus
- CVT has simulated "gears" for driver feedback
- Actual ratio is continuously variable

**Confidence:**
- High confidence during steady-state driving
- Low confidence during shifts or clutch engagement
- May show "0" (unknown) during rapid speed changes

**Uses:**
- **Shift Scheduling:** When to trigger rev-match, shift light
- **Speed Limiting:** Different limits per gear
- **Torque Limiting:** Reduce torque in lower gears (transmission protection)
- **Boost Control:** Gear-dependent boost targets
- **Launch Control:** Detect 1st gear launch
- **Datalogging:** Shift point analysis

### Gear Speed

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** rev/mi (revolutions per mile) or rev/km

**Description:**
Rotational speed of the current gear in revolutions per unit distance. Represents how fast the transmission output shaft (or wheels) rotate per mile traveled.

**Calculation:**
```
Gear Speed (rev/mi) = (Gear Ratio × Final Drive × Tire Rev/Mile)

Example (3rd gear):
Gear Ratio: 1.52:1
Final Drive: 4.11:1
Tire: 808 rev/mi

Gear Speed = 1.52 × 4.11 × 808 = 5049 rev/mi
```

**Uses:**
- Gear detection validation
- Speed sensor correlation
- Transmission diagnostics
- Expected RPM calculation at given speed

**Relationship to RPM and Speed:**
```
RPM = Vehicle Speed (mph) × Gear Speed (rev/mi) ÷ 60

Example:
Speed: 60 mph
Gear Speed: 5049 rev/mi

RPM = 60 × 5049 ÷ 60 = 5049 RPM (in 3rd gear)
```

### Vehicle Speed Parameters

**Multiple Speed Parameters:**
The ECU calculates and stores vehicle speed in multiple ways for redundancy, validation, and different subsystems.

**Vehicle Speed (km/h, ubyte):**
- 8-bit unsigned integer (0-255 km/h)
- Limited range for low-speed applications
- Lower resolution but faster processing

**Vehicle Speed (km/h, ushort):**
- 16-bit unsigned integer (0-65535 km/h)
- Full range for all speeds
- Higher resolution

**Vehicle Speed A/B/C/D:**
- Different speed calculations from different sensors
- **Speed A:** From transmission output shaft sensor
- **Speed B:** From wheel speed sensors (average)
- **Speed C:** From GPS (if equipped)
- **Speed D:** From calculated RPM and gear ratio

**Vehicle Speed Canbus:**
- Speed transmitted to other modules over CAN bus
- Typically matches primary speed calculation
- Used by:
  - Instrument cluster (speedometer)
  - ABS/VDC module
  - Cruise control
  - Navigation system

**Speed Source Selection:**
```
Priority:
1. Wheel speed sensors (most accurate, fastest response)
2. Transmission output sensor (backup if wheel sensors fail)
3. Calculated from RPM + gear (backup if both fail)
4. GPS (very low accuracy for ECU control, used for navigation only)
```

**Cross-Validation:**
- ECU compares multiple speed sources
- If sources disagree significantly (>10 mph):
  - Set diagnostic trouble code (DTC)
  - May enter limp mode
  - Speedometer may show error

## Gear Ratio Calibration

### Stock Gear Ratios

**VA WRX 6-Speed Manual:**
- 1st: 3.454:1
- 2nd: 2.062:1
- 3rd: 1.448:1
- 4th: 1.088:1
- 5th: 0.825:1
- 6th: 0.645:1
- Reverse: 3.583:1
- Final Drive: 4.111:1

### Gear Detection Table

**Calculated Ratio vs Gear:**
```
Calculated Ratio = RPM ÷ (Vehicle Speed × Final Drive)

Ratio Ranges:
- 3.20-3.70: 1st gear
- 1.90-2.25: 2nd gear
- 1.30-1.60: 3rd gear
- 0.95-1.20: 4th gear
- 0.70-0.90: 5th gear
- 0.55-0.75: 6th gear
```

**Overlap Zones:**
- Hysteresis prevents gear hunting
- Requires ratio to move past threshold before changing detected gear
- Example: In 3rd gear (1.448), won't detect 4th until ratio drops below 1.25

### Aftermarket Transmission

**Close-Ratio Transmission:**
- Closer gear spacing for better performance
- May require updated gear ratio tables
- Gear detection may fail if ratios not updated

**Sequential Transmission:**
- Different shift logic (sequential only)
- May not use standard gear detection
- Requires custom calibration

## Vehicle Speed Limiting

### Speed Limiter Types

**Fuel Cut Speed Limiter:**
- Cuts fuel when speed exceeds limit
- Engine runs rough at limit
- Aggressive but effective

**Ignition Retard Speed Limiter:**
- Retards timing to reduce power
- Smoother operation than fuel cut
- Gentler on engine

**Throttle Close Speed Limiter:**
- Closes electronic throttle
- Smoothest operation
- Driver can override (safety concern)

### Speed Limit Calibration

**Stock Limits:**
- North America: 145 mph (233 km/h)
- Japan: 112 mph (180 km/h)
- Europe: 155 mph (250 km/h) on performance models

**Raising/Removing Limit:**
- Common modification for track use
- Consider:
  - Tire speed rating (Z-rated for >149 mph)
  - Aerodynamic stability (lift at high speed)
  - Brake capability (stopping from high speed)
  - Legal implications

**Gear-Dependent Limits:**
- Some ECUs have lower limits in lower gears
- Prevents over-revving in low gears
- Example: 1st gear limited to 50 mph to prevent exceeding redline

## Datalogging Recommendations

**Essential Transmission Parameters:**
- Current Gear
- Vehicle Speed
- RPM
- Gear Speed

**Shift Analysis:**
- Plot RPM vs Time during shifts
- Identify shift points (RPM drop)
- Calculate shift time (time from lift to next gear engagement)
- Measure RPM drop per gear (should match gear ratios)

**Speed Calibration:**
- Vehicle Speed (from ECU)
- GPS Speed (from external GPS)
- Compare: should match within 1-2%
- Adjust Vehicle Speed Scalars if mismatch

**Gear Detection:**
- Current Gear (detected)
- Expected Gear (from RPM ÷ Speed)
- Mismatches indicate:
  - Incorrect gear ratio calibration
  - Gear detection logic issue
  - Speed sensor problem

## Related Tables

**Gear Ratios:**
- Transmission → Gear Ratios → Ratios for each gear
- Final Drive ratio

**Speed Scaling:**
- Transmission → Vehicle Speed → Scalars A and B
- Tire diameter calibration

**Speed Limiting:**
- Engine → Rev Limit → Speed limiter thresholds
- Fuel cut vs throttle close vs ignition retard

**Launch Control:**
- Engine → Launch Control → 1st gear detection
- Launch RPM limit

## Tuning Notes

### Speedometer Correction

**When Needed:**
- Changed tire size
- Changed wheel diameter
- Changed final drive ratio
- Speedometer reading incorrectly

**Correction Process:**
1. Measure actual speed (GPS or radar)
2. Compare to speedometer reading
3. Calculate error: Error = (Speedo - Actual) ÷ Actual
4. Adjust Scalar: New Scalar = Old Scalar × (1 + Error)

**Example:**
- Speedometer reads: 60 mph
- GPS reads: 58 mph
- Error: (60 - 58) ÷ 58 = 3.4% fast
- New Scalar = Old Scalar × (1 - 0.034) = Old Scalar × 0.966

### Tire Size Changes

**Larger Tires:**
- Speedometer reads slower than actual
- Odometer under-reports distance
- Lower effective gear ratios (engine revs lower at given speed)
- Slight power/torque loss (longer effective gearing)

**Smaller Tires:**
- Speedometer reads faster than actual
- Odometer over-reports distance
- Higher effective gear ratios (engine revs higher at given speed)
- Slight power/torque gain (shorter effective gearing)

**Recommended Calibration:**
- Always recalibrate speedometer for accuracy
- Affects:
  - Speed-based fuel/timing tables
  - AVCS activation speed
  - Speed limiter
  - Cruise control

### Gear Detection Issues

**Symptoms:**
- Incorrect gear displayed
- Shift light activates at wrong RPM
- Torque limiting in wrong gear

**Causes:**
- Incorrect gear ratio calibration
- Speed sensor error
- Clutch slip (calculated ratio doesn't match)

**Diagnosis:**
- Datalog: RPM, Speed, Detected Gear
- Calculate: Actual Ratio = RPM ÷ (Speed × Final Drive)
- Compare to gear ratio tables
- Update calibration if needed

### Final Drive Changes

**Shorter Final Drive (higher numerical ratio):**
- Example: 4.11 → 4.44
- Lower top speed per gear
- Better acceleration
- Higher RPM at given speed
- May hurt fuel economy

**Longer Final Drive (lower numerical ratio):**
- Example: 4.11 → 3.90
- Higher top speed per gear
- Slower acceleration
- Lower RPM at given speed
- Better fuel economy

**Recalibration Required:**
- Update Final Drive ratio in ECU
- Recalibrate speedometer scalars
- Update gear detection tables
- Verify speed limiter still functions correctly

### CVT Tuning

**Simulated Gears:**
- CVT has no fixed gears
- ECU simulates gear steps for driver feel
- Can adjust:
  - Number of simulated gears
  - Ratio steps between gears
  - Shift firmness/speed

**Continuous Ratio:**
- Actual CVT ratio changes smoothly
- Not constrained to simulated gear steps
- ECU can optimize ratio for:
  - Maximum acceleration
  - Best fuel economy
  - Target engine speed (performance/economy modes)

**Performance CVT Tuning:**
- Adjust simulated shift points (hold lower ratios longer)
- Increase line pressure (firmer shifts, less slip)
- Modify ratio maps (more aggressive acceleration)
