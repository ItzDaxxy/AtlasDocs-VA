# Airflow - Turbo - PI Control - PI Activation (Target Boost Threshold Abs)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | BAR |
| **Source File** | `Airflow - Turbo - PI Control - PI Activation (Target Boost Threshold Abs) - 2018 - LF9C102P.csv` |

## Description

Defines the target boost threshold at which closed-loop PI control activates, based on RPM. Below this threshold, the wastegate operates in open-loop mode using only feedforward (Initial Duty). Above this threshold, the PI controller engages to actively correct boost toward the target.

Values are in BAR (absolute pressure). The table specifies at what target boost level PI control should become active at each RPM point. This prevents PI control from interfering during low-boost operation where precise control is unnecessary, and ensures the PI system only engages when meaningful boost correction is required.

## Axes

### X-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 400.0000 to 8000.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: BAR
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   400.0000 |   800.0000 |  1200.0000 |  1600.0000 |  2000.0000 |  2400.0000 |  2800.0000 |  3200.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU uses this as a switch point for PI activation:

1. **RPM Reading**: ECU monitors engine RPM
2. **Table Lookup**: Interpolate activation threshold
3. **Comparison**: If Target Boost > Threshold, enable PI
4. **Mode Selection**: PI active or feedforward only

**Control Mode Logic:**
```
If (Target_Boost > PI_Activation_Threshold):
    Wastegate_Duty = Initial + P-term + I-term + Compensations
Else:
    Wastegate_Duty = Initial + Compensations (open-loop)
```

**Threshold Purpose:**
- Low boost: Feedforward (Initial Duty) is sufficient
- High boost: Closed-loop PI provides precise control
- Prevents unnecessary PI activity at low loads

## Related Tables

- **Airflow - Turbo - PI Control - Proportional**: P-term when PI active
- **Airflow - Turbo - PI Control - Integral Positive/Negative**: I-terms when PI active
- **Airflow - Turbo - Wastegate - Duty Initial**: Feedforward duty
- **Airflow - Turbo - Boost - Target Main**: Current boost target

## Related Datalog Parameters

- **Engine RPM**: X-axis input
- **Target Boost (bar)**: Compared against threshold
- **PI Active (boolean)**: Whether PI control is engaged
- **Wastegate Duty (%)**: Changes when PI activates

## Tuning Notes

**Common Modifications:**
- Lower threshold to engage PI control earlier
- Higher threshold to rely more on feedforward
- Stock values typically engage PI around 1.0-1.2 bar absolute

**Considerations:**
- Earlier PI activation = more precise low-boost control
- Later PI activation = smoother transitions, less hunting
- Match to boost target table activation points

**Threshold Guidelines:**
- Set below minimum positive boost target
- Ensure PI is active before significant boost builds
- Leave margin to avoid PI cycling on/off

## Warnings

- Setting too high may delay PI correction for over-boost
- Setting too low may cause PI hunting at low loads
- I-term should reset when PI deactivates to prevent windup
- Verify PI activates before boost target is reached
- Test transitions around threshold RPM points
