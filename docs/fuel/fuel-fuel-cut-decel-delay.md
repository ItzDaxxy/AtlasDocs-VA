# Fuel - Fuel Cut - Decel - Delay

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 8x8 |
| **Data Unit** | NONE |
| **Source File** | `Fuel - Fuel Cut - Decel - Delay - 2017 - RogueWRX.csv` |

## Description

This table defines the delay time before deceleration fuel cut (DFCO) activates during engine braking, indexed by RPM and coolant temperature. DFCO improves fuel economy by cutting fuel injection when coasting in gear with closed throttle.

**Purpose:**
- Controls timing of fuel cut during deceleration
- Delays fuel cut to prevent abrupt transitions
- Adjusts delay based on temperature (cold engine needs longer delay)
- Allows engine braking without fuel consumption

**Value Interpretation:**
- Values represent delay time (likely in milliseconds or engine cycles)
- Value of 0 at low RPM/cold temp = no delay (immediate behavior defined elsewhere)
- Value of 5 at higher RPM/warm temp = 5 units of delay before DFCO
- Longer delays = smoother transition but delayed fuel savings

**Temperature Relationship:**
- Cold temps (below 20°C): Delay of 0 (DFCO may be disabled during warm-up)
- Warm temps (20-100°C): Delay of 5 units at higher RPMs
- Cold engine needs stable fueling for warm-up, so DFCO is delayed or disabled

## Axes

### X-Axis

- **Parameter**: Engine - Idle Speed - RPM
- **Unit**: NONE
- **Range**: 0.0000 to 3500.0000
- **Points**: 8

### Y-Axis

- **Parameter**: Engine - Idle Speed - Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 100.0000
- **Points**: 8

## Cell Values

- **Unit**: NONE
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |   500.0000 |  1000.0000 |  1500.0000 |  2000.0000 |  2500.0000 |  3000.0000 |  3500.0000 |
--------------------------------------------------------------------------------------------------------------------
  -40.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
  -20.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
    0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |     0.0000 |
   20.0000 |     0.0000 |     0.0000 |     0.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |
   40.0000 |     0.0000 |     0.0000 |     0.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |
   60.0000 |     0.0000 |     0.0000 |     0.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |
   80.0000 |     0.0000 |     0.0000 |     0.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |
  100.0000 |     0.0000 |     0.0000 |     0.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |     5.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (RPM)**: Current engine speed during deceleration
- **Y-Axis (Coolant Temp)**: Engine temperature

**DFCO Activation Sequence:**
1. Throttle closes (driver lifts off accelerator)
2. ECU detects deceleration condition (closed throttle, engine driven by wheels)
3. Looks up delay value from this table
4. Waits for delay period
5. If conditions remain met, activates fuel cut
6. Monitors for exit conditions (throttle opening, RPM dropping)

**DFCO Exit Conditions:**
- Throttle opens (driver applies throttle)
- RPM drops to near-idle threshold
- Clutch disengaged (if equipped with clutch position sensor)

**The Table Pattern:**
- Low RPM (0-1000): Delay of 0 (DFCO likely controlled by other parameters)
- High RPM (1500-3500): Delay of 5 units when engine is warm
- Cold engine (below 20°C): No DFCO delay entries (DFCO may be disabled)

**Update Rate:** Evaluated continuously during closed-throttle deceleration.

## Related Tables

- Fuel Cut Decel RPM Threshold (controls minimum RPM for DFCO)
- Fuel Cut Decel Resume RPM (RPM to resume fueling)
- Idle Speed Target tables (DFCO exits before reaching idle)

## Related Datalog Parameters

- **Injector Duty Cycle (%)**: Drops to 0% when DFCO active
- **Throttle Position (%)**: Closed throttle triggers DFCO evaluation
- **RPM**: X-axis input, DFCO active at higher RPM
- **Coolant Temperature (°C)**: Y-axis input
- **Fuel Mode**: May indicate DFCO state

## Tuning Notes

**Stock Behavior:** Stock calibration provides smooth DFCO engagement with delays that prevent abrupt transitions. Cold engine delays/disables DFCO for warm-up stability.

**Common Modifications:**
- **Shorter Delays**: Quicker DFCO engagement, slightly better economy but may feel abrupt
- **Longer Delays**: Smoother transitions, delayed fuel savings
- **Cold Temp Adjustment**: May enable DFCO earlier during warm-up for efficiency

**Drivability Impact:**
DFCO behavior affects how the car feels during coasting:
- Aggressive DFCO: More engine braking feel, some "on/off" sensation
- Gentle DFCO: Smoother transitions, feels more natural

**Cold Engine Considerations:** The zero values at cold temps likely mean DFCO is disabled during warm-up to prevent rough running and ensure catalyst warm-up.

## Warnings

⚠️ **Cold Engine**: Don't enable aggressive DFCO during warm-up. Cold engine needs stable fueling and catalyst needs to reach operating temperature.

⚠️ **Lean Concerns**: DFCO is safe because the engine is motored by the wheels (no combustion occurring). However, re-entry to fueling must be smooth to prevent lean transients.

**Safe Practices:**
- Test DFCO behavior across temperature range
- Verify smooth fuel resumption when throttle opens
- Monitor for any stumble or hesitation during DFCO exit
