# Transmission - Gear Ratios - 1st - High

## Overview

| Property | Value |
|----------|-------|
| **Category** | Transmission |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | REV_PER_MI |
| **Source File** | `Transmission - Gear Ratios - 1st - High - 2017 - RogueWRX.csv` |

## Value

**24637.2188 REV_PER_MI**

## Description

Defines the gear ratio for 1st gear expressed as engine revolutions per mile traveled. This value represents the combined effect of transmission gear ratio and final drive ratio, used by the ECU to calculate vehicle speed from engine RPM.

The value 24637.2188 rev/mi corresponds to the VA WRX 6-speed manual transmission first gear (~3.636:1) combined with the final drive ratio (~4.11:1). This is the lowest (highest numerical) gear for maximum acceleration from a standstill.

The ECU uses this value to:
- Calculate vehicle speed when in 1st gear (Vehicle Speed = RPM / Gear Ratio Value × conversion factor)
- Determine target RPM for rev-matched downshifts
- Validate gear position based on speed/RPM relationship

## Related Tables

- **Transmission - Gear Ratios (2nd-6th High/Low)**: Complete gear ratio set
- **Transmission - Vehicle Speed Scalar A/B**: Additional speed calculation factors
- **Throttle - Rev Matching**: Uses ratios for RPM blip calculations

## Related Datalog Parameters

- **Engine RPM**: Used with ratio to calculate speed
- **Vehicle Speed**: Calculated output
- **Gear Position**: Determines which ratio to use
- **Clutch Switch Status**: Indicates gear changes

## Tuning Notes

**When to Modify:**
- Changed final drive ratio (4.44, 3.90, etc.)
- Non-stock tire diameter (larger tires = lower effective ratio)
- Transmission swap with different gear ratios
- Correcting speedometer errors

**Calculation:**
New Value = Old Value × (New Final Drive / Old Final Drive) × (Old Tire Diameter / New Tire Diameter)

**Examples:**
- 4.44 final drive swap: Multiply all ratios by ~1.08
- 265/35R18 to 255/40R18: Adjust for rolling circumference change

## Warnings

- Incorrect ratios cause inaccurate vehicle speed calculations
- Speedometer will read incorrectly if ratios don't match hardware
- Rev matching will target wrong RPMs causing harsh downshifts
- Must modify ALL gear ratios proportionally when changing tire size or final drive
- Do not modify individual gears unless actual transmission ratios changed
