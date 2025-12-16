# Airflow - Turbo - PI Control - Integral Negative Limit

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | PERCENT |
| **Source File** | `Airflow - Turbo - PI Control - Integral Negative Limit - 2018 - LF9C102P.csv` |

## Value

**-90.0000 PERCENT**

## Description

Sets the maximum negative value the integral term can accumulate when correcting over-boost conditions. At -90%, this allows substantial wastegate duty reduction to combat over-boost - nearly eliminating duty if needed.

This large negative limit reflects the safety-critical nature of over-boost protection. The I-term can accumulate to -90%, essentially commanding the wastegate to fully open if persistent over-boost is detected. This is intentionally much larger than the positive limit (+10%) because over-boost is more dangerous than under-boost.

**Asymmetric Safety Design:**
- Positive limit: +10% (modest authority for under-boost)
- Negative limit: -90% (substantial authority for over-boost)
- Prioritizes engine protection over boost performance

## Related Tables

- **Airflow - Turbo - PI Control - Integral Negative**: I-term constrained by this limit
- **Airflow - Turbo - PI Control - Integral Positive Limit**: Positive side limit (+10%)
- **Airflow - Turbo - PI Control - Proportional**: P-term (not limited by this)
- **Airflow - Turbo - Boost - Limit**: Boost ceiling protection

## Related Datalog Parameters

- **PI Integral Sum**: Can go as negative as this limit
- **Wastegate Duty (%)**: Reduced by negative I-term
- **Actual Boost**: Over-boost condition
- **Boost Error (Pa)**: Negative error accumulates I-term

## Tuning Notes

**Common Modifications:**
- Generally should not be reduced (safety-critical)
- May need adjustment for external wastegate setups
- Coordinate with overall boost protection strategy

**Considerations:**
- Large negative limit ensures over-boost can be corrected
- Even with bad feedforward duty, I-term can compensate
- Acts as backup to other boost control failures

**Safety Implications:**
- -90% allows nearly complete duty reduction
- Critical for preventing sustained over-boost
- Do not restrict without understanding consequences
