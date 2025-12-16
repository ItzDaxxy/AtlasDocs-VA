# Airflow - Turbo - PI Control - Integral Positive Limit

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Positive Limit - 2018 - LF9C102P.csv` |

## Value

**10.0000 PERCENT**

## Description

Sets the maximum positive value the integral term can accumulate when correcting under-boost conditions. At 10%, this limits how much additional wastegate duty the I-term can add beyond the initial feedforward duty.

This limit prevents integral windup - a condition where the I-term accumulates excessively during sustained error, causing massive overshoot when the error condition clears. Without this limit, prolonged under-boost (such as during part-throttle cruise) could cause the I-term to wind up to very high values.

**Asymmetric Limits:**
The positive limit (+10%) is much smaller than the negative limit (-90%), reflecting the safety priority of the boost control system. The system allows much more correction for over-boost than under-boost.

## Related Tables

- **Airflow - Turbo - PI Control - Integral Positive**: I-term constrained by this limit
- **Airflow - Turbo - PI Control - Integral Negative Limit**: Negative side limit (-90%)
- **Airflow - Turbo - PI Control - Proportional**: P-term (not limited by this)
- **Airflow - Turbo - Wastegate - Duty Maximum**: Overall duty limit

## Related Datalog Parameters

- **PI Integral Sum**: Constrained to this maximum
- **Wastegate Duty (%)**: Includes limited I-term
- **Boost Error (Pa)**: Causes I-term accumulation

## Tuning Notes

**Common Modifications:**
- May increase for larger turbos requiring more duty range
- Increase if boost consistently under-targets despite I-term at limit
- Coordinate with wastegate duty maximum

**Considerations:**
- Higher limit = more correction authority, more windup risk
- Lower limit = faster windup recovery, less correction range
- 10% provides reasonable balance for stock turbo

**Anti-Windup Strategy:**
- Limit prevents excessive accumulation
- I-term should not fight mechanical limits
- Helps system recover quickly from transient conditions
