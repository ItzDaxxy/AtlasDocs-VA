# Fuel - Injectors - Start of Injection - Homogeneous

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 16x8 |
| **Data Unit** | DEGREES |
| **Source File** | `Fuel - Injectors - Start of Injection - Homogeneous - 2017 - RogueWRX.csv` |

## Description

This table defines the Start of Injection (SOI) timing for homogeneous combustion mode, indexed by calculated load and RPM. SOI timing determines when during the engine cycle fuel injection begins, which critically affects mixture formation and combustion efficiency.

**Purpose:**
- Controls injection timing for optimal air-fuel mixture preparation
- Optimizes fuel atomization and charge mixing
- Balances emissions, efficiency, and power across operating conditions

**Value Interpretation:**
- Values in crankshaft degrees (BTDC/ATDC convention varies)
- Values around 260-320° typically represent intake stroke injection
- Earlier (higher values) = more time for mixing before combustion
- Later (lower values) = less mixing time, potentially stratified charge

**Homogeneous Mode:**
In homogeneous combustion, fuel is injected early to allow thorough mixing with intake air, creating a uniform air-fuel mixture throughout the cylinder. This contrasts with stratified mode where fuel is concentrated near the spark plug.

## Axes

### X-Axis

- **Parameter**: Fueling - Closed Loop - Calculated Load
- **Unit**: G_PER_REV
- **Range**: 0.2588 to 2.0704
- **Points**: 8

### Y-Axis

- **Parameter**: RPM
- **Unit**: RPM
- **Range**: 800.0000 to 6400.0000
- **Points**: 16

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |     0.2588 |     0.5176 |     0.7764 |     1.0352 |     1.2940 |     1.5528 |     1.8116 |     2.0704 |
--------------------------------------------------------------------------------------------------------------------
  800.0000 |   290.0000 |   290.0000 |   290.0000 |   260.0000 |   260.0000 |   260.0000 |   260.0000 |   260.0000 |
  825.0000 |   300.0000 |   290.0000 |   290.0000 |   262.0000 |   261.0000 |   260.0000 |   260.0000 |   270.0000 |
  950.0000 |   300.0000 |   290.0000 |   290.0000 |   271.0000 |   266.0000 |   260.0000 |   260.0000 |   270.0000 |
 1200.0000 |   290.0000 |   290.0000 |   290.0000 |   290.0000 |   275.0000 |   260.0000 |   260.0000 |   270.0000 |
 1600.0000 |   276.0000 |   298.0000 |   300.0000 |   290.0000 |   290.0000 |   270.0000 |   270.0000 |   270.0000 |
 2000.0000 |   273.0000 |   299.0000 |   302.0000 |   290.0000 |   290.0000 |   300.0000 |   290.0000 |   290.0000 |
 2400.0000 |   274.0000 |   299.0000 |   305.0000 |   300.0000 |   300.0000 |   310.0000 |   310.0000 |   290.0000 |
 2800.0000 |   279.0000 |   300.0000 |   305.0000 |   310.0000 |   310.0000 |   310.0000 |   310.0000 |   290.0000 |
```

## Functional Behavior

The ECU performs 2D interpolation using:
- **X-Axis (Load)**: Calculated load in g/rev
- **Y-Axis (RPM)**: Current engine speed

**SOI Calculation:**
```
Final SOI = Base SOI (this table) + Compensation (if applicable)
```

**Injection Timing Reference:**
- Values represent crankshaft degrees
- Typical convention: 0° = TDC compression, 360° = TDC exhaust, 720° = complete cycle
- Values 260-320° typically target intake stroke for homogeneous operation

**Update Rate:** Calculated every engine cycle based on current load and RPM.

## Related Tables

- **[Fuel - Injectors - Start of Injection - Homogeneous (Aggressive)](./fuel-injectors-start-of-injection-homogeneous-aggressive.md)**: Aggressive SOI timing
- **[Fuel - Injectors - Start of Injection - Cranking](./fuel-injectors-start-of-injection-cranking.md)**: Cranking SOI timing
- **[Fuel - Injectors - Start of Injection - Compensation](./fuel-injectors-start-of-injection-compensation-compensation-homogeneous.md)**: SOI compensation adders

## Related Datalog Parameters

- **Calculated Load (g/rev)**: X-axis input for table lookup
- **RPM**: Y-axis input for table lookup
- **Injector Timing (deg)**: Actual commanded injection timing
- **Fuel Pressure (High) (kPa)**: Higher pressure enables shorter injection duration

## Tuning Notes

**Stock Behavior:** Stock timing is calibrated for OEM injectors and emissions compliance. Values progress from earlier injection at low load to later injection at higher loads.

**Common Modifications:**
- **Different Injectors**: May require SOI adjustment for optimal spray pattern
- **Higher Pressure Targets**: Shorter injection duration may allow later SOI
- Generally left at stock unless injector hardware changed

**SOI Effects:**
- **Too Early**: Fuel may hit cylinder walls (wall wetting), increased emissions, potential oil dilution
- **Too Late**: Insufficient mixing time, inconsistent combustion, potential misfires

**Load-Based Progression:**
Notice values vary significantly with load:
- Low load (~0.26 g/rev): SOI around 276-300°
- High load (~2.07 g/rev): SOI around 260-290°
This reflects different mixing requirements at various load conditions.

## Warnings

⚠️ **Injection Duration Interaction**: SOI must be coordinated with injection duration (IPW). Very long IPW may overlap with valve events if SOI is too late.

⚠️ **Injector-Specific**: Different injector spray patterns may require different SOI calibration.

⚠️ **Emissions Impact**: SOI significantly affects particulate emissions from direct injection. Stock calibration optimized for emissions compliance.

**Safe Practices:**
- Start with stock values unless injector hardware changed
- Make small adjustments (5-10° at a time)
- Verify no misfires or knock after changes
- Monitor long-term emission-related health if applicable
