# Fuel - Pressure - Maximum Pressure DTC Threshold

## Overview

| Property | Value |
|----------|-------|
| **Category** | Fuel |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | KPA |
| **Source File** | `Fuel - Pressure - Maximum Pressure DTC Threshold - 2017 - RogueWRX.csv` |

## Value

**14999.9004 KPA**

## Description

This scalar defines the maximum fuel rail pressure threshold that triggers a Diagnostic Trouble Code (DTC). When actual fuel pressure exceeds this value, the ECU sets a fault code indicating over-pressure condition, which may indicate HPFP or pressure regulation issues.

**Purpose:**
- Protects fuel system components from excessive pressure
- Triggers diagnostic fault when pressure exceeds safe limits
- Alerts to potential HPFP or regulator malfunction

**Value Interpretation:**
- Value of ~15,000 kPa = 15 MPa = ~2,175 psi
- This is near the upper limit of the HPFP system capability
- Pressures exceeding this indicate potential component failure

**DTC Behavior:**
When fuel pressure exceeds this threshold:
1. ECU logs a DTC (P-code)
2. May enter limp mode or derate operation
3. Check Engine Light illuminates
4. Stored in fault memory for diagnostic retrieval

## Related Tables

- **[Fuel - Pressure - Fuel Pressure Target Main](./fuel-pressure-fuel-pressure-target-main.md)**: Normal pressure targets (should be below DTC threshold)
- **[Fuel - Pressure - Fuel Pressure Target Cranking](./fuel-pressure-fuel-pressure-target-cranking.md)**: Cranking targets
- **[Fuel - Pressure - Fuel Pressure Target Idle](./fuel-pressure-fuel-pressure-target-idle.md)**: Idle targets

## Related Datalog Parameters

- **Fuel Pressure (High) (kPa)**: Monitor for approach to threshold
- **HPFP Duty Cycle (%)**: Pump control effort
- **DTC Status**: Check for fuel pressure related codes
- **MIL Status**: Check Engine Light state

## Tuning Notes

**Stock Behavior:** Stock threshold of ~15,000 kPa is near HPFP system maximum, providing margin above normal operating pressures while protecting components.

**Common Modifications:**
- **Generally not modified**: This is a safety threshold
- May need adjustment if running extremely high pressure targets (race applications)
- Raising threshold removes protection - not recommended for street use

**When Over-Pressure Occurs:**
Over-pressure typically indicates:
- HPFP regulator failure
- Stuck/malfunctioning relief valve
- ECU commanding excessive pressure (calibration error)
- Fuel system blockage

**Diagnostic Use:** If this DTC triggers intermittently, investigate:
1. HPFP regulator function
2. Fuel return line restrictions
3. Commanded vs actual pressure (ECU issue vs mechanical)

## Warnings

⚠️ **Do Not Disable**: This threshold protects expensive fuel system components. Over-pressure can damage injectors, fuel rails, and HPFP.

⚠️ **Physical Limits**: The HPFP system has physical pressure limits (~20 MPa). Exceeding these causes component failure.

**Safe Practices:**
- Monitor fuel pressure during tuning to ensure it stays well below this threshold
- Investigate any over-pressure DTCs immediately
- If raising pressure targets, ensure adequate margin below DTC threshold
