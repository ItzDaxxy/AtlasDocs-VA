# AVCS - Intake - Intake Cam Advance Target Adder Activation

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Dimensions** | 0x16 |
| **Data Unit** | PERCENT |
| **Source File** | `AVCS - Intake - Intake Cam Advance Target Adder Activation - 2018 - LF9C102P.csv` |

## Description

Defines a temperature-based activation scaling factor that controls how much of the intake cam advance compensation is applied based on engine coolant temperature. This table acts as a percentage multiplier (0-100%) that scales the compensation adder values before they are added to the base cam timing target.

The activation table allows the ECU to:
- Reduce or eliminate compensation when the engine is cold
- Gradually ramp in compensation as engine warms up
- Protect cold engine from aggressive cam timing
- Optimize cam behavior across temperature range

Values are in PERCENT, where:
- **0%** = No compensation applied (compensation adder ignored)
- **50%** = Half of compensation adder applied
- **100%** = Full compensation adder applied

This temperature-dependent scaling ensures cam timing strategy adapts appropriately during engine warm-up and protects against cold-engine issues that aggressive cam timing could cause.

## Axes

### X-Axis

- **Parameter**: Coolant Temperature
- **Unit**: CELSIUS
- **Range**: -40.0000 to 110.0000
- **Points**: 16

### Y-Axis

- **Parameter**: Y-Axis
- **Unit**: 

## Cell Values

- **Unit**: PERCENT
- **Data Type**: Float

## Data Preview

First 8x8 corner of the table:

```
       RPM |   -40.0000 |   -30.0000 |   -20.0000 |   -10.0000 |     0.0000 |    10.0000 |    20.0000 |    30.0000 |
--------------------------------------------------------------------------------------------------------------------
```

## Functional Behavior

The ECU uses this table to scale compensation values based on coolant temperature:

1. **Temperature Lookup:** ECU reads current coolant temperature
2. **Activation % Lookup:** ECU interpolates this table to get activation percentage (0-100%)
3. **Compensation Scaling:** Compensation adder is multiplied by activation percentage:
   ```
   Scaled_Compensation = Raw_Compensation × (Activation% / 100)
   ```
4. **Final Target Calculation:**
   ```
   Final_Target = Base_Target + Scaled_Compensation
   ```

This ensures that:
- Cold engine (low coolant temp) = low activation % = minimal compensation applied
- Warm engine (normal operating temp) = 100% activation = full compensation applied
- Gradual transition prevents harsh changes during warm-up

## Related Tables

- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-open.md) - Compensation values that this table scales
- [AVCS - Intake - Barometric Multiplier High - Intake Cam Advance Compensation (TGV Closed)](./avcs-intake-barometric-multiplier-high-intake-cam-advance-compensation-tgv-closed.md) - TGV closed compensation
- [AVCS - Intake - Barometric Multiplier Low - Intake Cam Advance Compensation (TGV Open)](./avcs-intake-barometric-multiplier-low-intake-cam-advance-compensation-tgv-open.md) - Low altitude compensation
- [AVCS - Exhaust - Exhaust Cam Retard Target Adder Activation](./avcs-exhaust-exhaust-cam-retard-target-adder-activation.md) - Exhaust cam equivalent

## Related Datalog Parameters

- **Engine Coolant Temperature** - X-axis lookup parameter (primary input)
- **AVCS Intake Cam Advance (Target)** - Shows final target after activation scaling
- **AVCS Intake Cam Advance (Actual)** - Measured cam position
- **Oil Temperature** - Related warm-up indicator
- **Time Since Engine Start** - Indirect warm-up indicator

## Tuning Notes

**Understanding Activation Scaling:**

This table protects the engine during warm-up by reducing compensation effects when cold. Stock calibration typically shows:
- 0% activation at very cold temperatures (-40°C to 0°C)
- Gradual ramp from 0% to 100% as engine warms (0°C to 80°C)
- 100% activation at normal operating temperature (80°C+)

**When to Modify:**

**Faster Activation (Higher % at Lower Temps):**
- If compensation provides beneficial cold-start behavior
- For dedicated race applications with pre-warming
- When using compensation for conservative timing (not aggressive)
- Climate with minimal cold-weather operation

**Slower Activation (Lower % at Higher Temps):**
- If compensation is aggressive and needs more thermal protection
- Cold climate operation requires extended warm-up protection
- Oil system takes longer to reach proper pressure/viscosity
- Conservative approach for engine longevity

**Keep Stock Activation When:**
- Compensation tables are all zeros (activation has no effect)
- Using base tables for all tuning (not using compensation)
- Unsure of compensation strategy
- Want OEM-level cold-start protection

**Coordination with Compensation:**

The effectiveness of this table depends entirely on whether compensation tables have non-zero values:
- If all compensation tables = 0, activation scaling has no effect
- If compensation is used, activation curve becomes critical for cold operation
- Test cold-start behavior thoroughly if modifying activation

**Typical Modifications:**
- Shift activation curve 10-20°C cooler for faster compensation engagement
- Reduce maximum activation to 80-90% for safety margin
- Add hysteresis-like behavior with slower ramp for conservative approach

## Warnings

**Cold Engine Protection:**
- This table is a safety mechanism for cold operation
- Removing activation too early (cold temps) risks cold-engine damage
- Oil viscosity, clearances, and combustion stability all affected by temperature
- Always test cold-start behavior after modifications

**Compensation Dependency:**
- Only matters if compensation tables have non-zero values
- Verify compensation tables before spending time on activation tuning
- Changes have no effect if compensation isn't being used

**Temperature Sensor Accuracy:**
- Activation depends on accurate coolant temperature reading
- Faulty coolant temp sensor will cause incorrect activation
- Verify sensor operation before diagnosing activation issues

**Warm-Up Behavior:**
- Aggressive activation (high % at low temps) can cause:
  - Rough idle during warm-up
  - Increased cold-start emissions
  - Potential cold-engine wear
  - Oil system stress before full pressure established

**Testing Requirements:**
- Always test modifications during cold-start conditions
- Verify behavior across full temperature range (-20°C to 100°C+)
- Monitor AVCS actual vs target during warm-up
- Check for hunting or instability as activation ramps in

**Best Practice:**
- Leave stock unless using compensation tables actively
- Make conservative changes (small shifts in temperature breakpoints)
- Document activation strategy clearly for future reference
- Consider that other systems (ignition, fuel) may have temperature dependencies too
