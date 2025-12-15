# Ignition - Compensation - Tip-In - 4th Gear

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - Tip-In - 4th Gear - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation during tip-in events in 4th gear, indexed by TPS delta rate. It provides temporary timing adjustment to improve throttle response and reduce knock risk during rapid acceleration in 4th gear.

**Purpose:**
- Compensates timing during rapid throttle opening in 4th gear
- Typically retards timing to prevent knock during boost build
- Gear-specific calibration for highway cruising range
- 4th gear is commonly used for highway passing and sustained acceleration

**Value Interpretation:**
- Values in degrees of timing adjustment
- Positive = advance, Negative = retard
- Higher TPS delta = faster throttle movement
- Compensation active during transient throttle events

**4th Gear Context:**
Fourth gear is a tall gear often used for highway cruising and passing. Lower torque multiplication means tip-in events are typically less aggressive than lower gears, but boost can still build rapidly requiring knock protection.

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
- **X-Axis (TPS Delta)**: Rate of throttle position change

**4th Gear Context:**
Fourth gear is typically used for highway cruising speeds. Tip-in events in 4th gear are common during highway passing maneuvers where moderate but sustained acceleration is needed.

**Gear-Specific Compensation:**
Each gear has its own tip-in table because:
- Torque multiplication varies by gear
- Load increase rate differs
- RPM range during tip-in varies
- 4th gear has lower torque multiplication than lower gears

**Update Rate:** Calculated every ignition event during tip-in.

## Related Tables

- **[Ignition - Compensation - Tip-In - 1st Gear](./ignition-compensation-tip-in-1st-gear.md)**: 1st gear tip-in
- **[Ignition - Compensation - Tip-In - 2nd Gear](./ignition-compensation-tip-in-2nd-gear.md)**: 2nd gear tip-in
- **[Ignition - Compensation - Tip-In - 3rd Gear](./ignition-compensation-tip-in-3rd-gear.md)**: 3rd gear tip-in
- **[Ignition - Compensation - Tip-In - 5th Gear](./ignition-compensation-tip-in-5th-gear.md)**: 5th gear tip-in
- **[Ignition - Compensation - Tip-In - 6th Gear](./ignition-compensation-tip-in-6th-gear.md)**: 6th gear tip-in

## Related Datalog Parameters

- **Throttle Position (%)**: Used to calculate delta
- **TPS Delta**: Rate of throttle change
- **Gear Position**: Determines table selection
- **Ignition Timing**: Final timing with compensation
- **Vehicle Speed**: Used for gear calculation

## Tuning Notes

**Stock Behavior:** Stock provides appropriate tip-in compensation for 4th gear scenarios, which typically involve sustained highway acceleration and passing.

**4th Gear Characteristics:**
- Lower torque multiplication than 1st-3rd gears
- Common for highway cruising speeds (60-80 mph)
- Used for extended passing maneuvers
- Less aggressive load increase than lower gears

**Common Modifications:**
- Usually left at stock unless specific tip-in issues
- May adjust if experiencing knock during highway passing
- Consider if heat soak affects sustained acceleration

**Testing Tip-In:**
To verify proper tip-in compensation:
- Datalog during highway passing maneuvers
- Monitor knock and timing values
- Test at typical highway cruise speeds
- Verify compensation during sustained acceleration

## Warnings

**Transient Knock Risk**: Tip-in is knock-prone. Test carefully.

**Gear-Specific**: Only affects 4th gear operation.

**Safe Practices:**
- Test tip-in response at various temperatures
- Monitor knock during highway passing
- Test specifically in 4th gear scenarios
- Pay attention to sustained acceleration situations
