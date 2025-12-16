# Throttle - Requested Torque - Limits - Oil Temperature

## Overview

| Property | Value |
|----------|-------|
| **Category** | Throttle |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | CELSIUS |
| **Source File** | `Throttle - Requested Torque - Limits - Oil Temperature - 2017 - RogueWRX.csv` |

## Value

**Temperature threshold for oil-temperature-based torque limiting**

## Description

Defines the oil temperature threshold above which the ECU may limit requested torque to protect the engine from excessive stress during high oil temperature conditions. When oil temperature exceeds this threshold, the ECU reduces available torque to prevent oil breakdown and bearing damage.

High oil temperatures reduce lubrication effectiveness and can lead to accelerated wear or engine failure. This parameter provides a protective limit that reduces engine load when oil temperature becomes excessive.

## Related Tables

- **Throttle - Requested Torque - Limits - Main**: Primary torque limiting tables
- **Engine - Oil Temperature - Warning Threshold**: Oil temp warning activation
- **Throttle - Requested Torque - Target**: Base torque request tables

## Related Datalog Parameters

- **Oil Temperature**: Monitored against this threshold
- **Requested Torque**: Reduced when threshold exceeded
- **Throttle Position**: May be limited to reduce torque
- **Coolant Temperature**: Related thermal protection parameter

## Tuning Notes

**Oil Temperature Protection:**
- This threshold provides engine protection during extreme conditions
- Track use, aggressive driving, or hot weather can trigger this limit
- Adequate oil cooling prevents this limit from activating

**Modification Considerations:**
- Raising threshold increases risk of oil-related damage
- Better oil cooling (cooler, larger capacity) is preferred over threshold increase
- High-quality synthetic oil handles higher temps but doesn't eliminate limits

## Warnings

- Disabling or raising oil temp limits risks engine damage
- Oil breakdown at high temps reduces bearing protection
- Track use should include oil temperature monitoring
- Consistent threshold activation indicates need for oil cooling upgrades
