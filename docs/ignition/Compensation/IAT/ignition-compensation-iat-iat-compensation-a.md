# Ignition - Compensation - IAT - IAT Compensation A

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | DEGREES |
| **Source File** | `Ignition - Compensation - IAT - IAT Compensation A - 2017 - RogueWRX.csv` |

## Description

This 1D table defines ignition timing compensation based on intake air temperature (IAT), variant A. It adjusts timing to account for air density changes and knock risk variations with intake temperature.

**Purpose:**
- Adjusts timing based on intake air temperature
- Retards timing when air is hot (higher knock risk)
- May advance when air is cold (denser air, more efficient)
- Variant A likely used for normal/low-load conditions

**Value Interpretation:**
- Values in degrees of timing adjustment
- Negative values = timing retard (typical for hot air)
- Positive values = timing advance (typical for cold air)
- Zero = no compensation (at reference temperature)

**IAT and Knock:**
Hot intake air:
- Lower density = less oxygen per volume
- Higher combustion temperatures
- Increased knock tendency
Timing retard compensates for these conditions.

## Axes

### X-Axis

- **Parameter**: IAT (Intake Air Temperature)
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: None (1D table)
- **Unit**: N/A

## Cell Values

- **Unit**: DEGREES
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU performs 1D interpolation using:
- **X-Axis (IAT)**: Current intake air temperature

**Typical Compensation Pattern:**
- Very Cold (-40 to 0°C): May advance (denser air allows it)
- Cool (0 to 25°C): Little or no compensation (ideal conditions)
- Warm (25 to 50°C): Progressive retard begins
- Hot (50 to 110°C): Significant retard (knock protection)

**Variant A vs B:**
Two IAT compensation tables exist (A and B):
- Variant A: Likely for normal/light load conditions
- Variant B: Likely for high load/boost conditions
Selection between them may depend on load, RPM, or boost state.

**Application with Activation:**
IAT compensation may be scaled by an activation table:
```
Effective Compensation = Base IAT Compensation × Activation %
```
This allows the compensation to be RPM/load dependent.

**1D Table Format:**
The 0x16 dimension indicates 1D lookup with 16 temperature points.

**Update Rate:** Evaluated continuously based on IAT sensor reading.

## Related Tables

- **[Ignition - Compensation - IAT - Compensation B](./ignition-compensation-iat-iat-compensation-b.md)**: Alternate IAT compensation table
- **[Ignition - Compensation - IAT - Compensation A Activation](./ignition-compensation-iat-iat-compensation-a-activation.md)**: Scales this compensation by RPM/load
- **[Ignition - Compensation - IAT - Compensation B Activation](./ignition-compensation-iat-iat-compensation-b-activation.md)**: Scales variant B

## Related Datalog Parameters

- **IAT (Intake Air Temperature)**: X-axis input (°C)
- **Ignition Timing**: Shows final timing with compensations
- **Manifold Pressure**: May influence A/B selection
- **Calculated Load**: Input to activation table

## Tuning Notes

**Stock Behavior:** Stock retards timing as IAT increases to prevent knock from hot intake air. The reference temperature (zero compensation) is typically around 20-25°C.

**IAT Importance for Turbo:**
On turbocharged engines, IAT is critical:
- Turbo compresses air, adding heat
- Intercooler may not fully cool air under sustained boost
- Heat soak after hard runs elevates IAT significantly
Hot IAT = high knock risk = timing retard needed.

**Common Modifications:**
- May increase retard at high IAT for safety margin
- Intercooler upgrades may allow less retard
- Cold air intake may allow slightly less advance at cold temps

**Hot Day Performance:**
On hot days, IAT is elevated even at idle. Combined with heat soak from traffic or hard driving, significant timing retard may be needed. This is why hot-day performance often suffers.

**Sensor Location Matters:**
IAT sensor location affects compensation:
- Pre-turbo: Measures ambient, misses turbo heat
- Post-intercooler: Most accurate for knock prediction
- Manifold: Affected by heat soak and fuel cooling

## Warnings

⚠️ **Knock Prevention Critical**: IAT compensation is a primary knock protection mechanism.

⚠️ **Heat Soak**: After hard driving, IAT remains elevated even at idle. Allow cool-down before aggressive driving.

⚠️ **Sensor Failure**: Failed IAT sensor can cause knock or excessive retard depending on failure mode.

**Safe Practices:**
- Monitor IAT during datalogging sessions
- Allow cool-down time after spirited driving
- If upgrading intercooler, verify IAT compensation still provides adequate protection
- Don't reduce hot-IAT retard without careful knock testing
