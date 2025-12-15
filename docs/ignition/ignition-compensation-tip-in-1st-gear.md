# Ignition - Compensation - Tip-In - 1st Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 1st Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in (rapid throttle opening) events in 1st gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid load increases.

**Purpose:**
- Compensates timing during rapid throttle opening in 1st gear
- May retard timing to prevent knock during sudden load increase
- Or advance timing for improved response (depends on calibration)
- Gear-specific for optimal low-speed/high-torque response

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive values = timing advance (more responsive)
- Negative values = timing retard (knock protection)
- Higher TPS delta = faster throttle movement

**1st Gear Context:**
First gear has highest wheel torque multiplication, meaning engine load changes rapidly with throttle input. This table compensates for the unique tip-in characteristics in 1st gear.

## Axes

### X-Axis

- **Parameter**: Timing - Compensation - Tip-In - TPS Delta Raw
- **Unit**: Raw counts (0-28672 scale)
- **Range**: 0.0000 to 28672.0000
- **Points**: 8

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.0000 |  4096.0000 |  8192.0000 | 12288.0000 | 16384.0000 | 20480.0000 | 24576.0000 | 28672.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (TPS Delta)**: Rate of throttle position change (raw counts)

**TPS Delta Interpretation:**
- 0 = No throttle movement (steady state)
- Higher values = Faster throttle opening
- 28672 = Maximum throttle opening rate

**Tip-In Detection:**
The ECU monitors throttle position rate of change:
```
TPS Delta = Current TPS - Previous TPS (per calculation cycle)
```
When delta exceeds threshold, tip-in compensation activates.

**Gear Detection:**
ECU determines current gear from:
- Vehicle speed vs engine RPM ratio
- Gear position sensor (if equipped)
- Calculated from transmission ratios

**1D Table Format:**
The 0x8 dimension indicates 1D lookup with 8 TPS delta points.

**Update Rate:** Calculated every ignition event during tip-in conditions.

## Related Tables

- **[Ignition - Compensation - Tip-In - 2nd Gear](./ignition-compensation-tip-in-2nd-gear.md)**: 2nd gear tip-in compensation
- **[Ignition - Compensation - Tip-In - 3rd Gear](./ignition-compensation-tip-in-3rd-gear.md)**: 3rd gear tip-in compensation
- **[Ignition - Compensation - Tip-In - 4th Gear](./ignition-compensation-tip-in-4th-gear.md)**: 4th gear tip-in compensation
- **[Ignition - Compensation - Tip-In - 5th Gear](./ignition-compensation-tip-in-5th-gear.md)**: 5th gear tip-in compensation
- **[Ignition - Compensation - Tip-In - 6th Gear](./ignition-compensation-tip-in-6th-gear.md)**: 6th gear tip-in compensation

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines which table is active
- **Ignition Timing**: Shows final timing with compensation
- **Vehicle Speed**: Used for gear calculation

## Tuning Notes

**Stock Behavior:** Stock calibration typically retards timing slightly during tip-in to prevent knock as boost builds rapidly. The compensation decays as throttle stabilizes.

**1st Gear Characteristics:**
- Highest torque multiplication
- Fastest load increase rate
- Most knock-prone during tip-in
- May need most retard of all gears

**Common Modifications:**
- May reduce retard if knock-free operation confirmed
- Can add advance for sharper throttle response (test carefully)
- Usually left at stock unless specific tip-in issues

**Tip-In Knock:**
Rapid throttle opening causes:
1. Sudden boost increase
2. Intake air temperature rise (heat soak)
3. High cylinder pressure before timing can adapt
This table pre-emptively adjusts timing for these conditions.

**Testing Tip-In:**
To verify proper tip-in compensation:
- Datalog while snapping throttle open
- Monitor knock and timing values
- Check across different gears and RPM

## Warnings

⚠️ **Transient Knock Risk**: Tip-in is high-risk for knock. Excessive advance causes damage.

⚠️ **Gear-Specific**: This only affects 1st gear - test in appropriate conditions.

⚠️ **Heat Soak**: Hot engine/intercooler increases tip-in knock risk.

**Safe Practices:**
- Test tip-in response at various engine temperatures
- Monitor knock carefully during aggressive tip-in
- Start conservative (more retard) if modifying
- Test 1st gear acceleration specifically
