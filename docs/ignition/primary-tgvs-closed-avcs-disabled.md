# Ignition - Primary - TGVs Closed (AVCS Disabled)

## Overview

| Property | Value |
|----------|-------|
| **Category** | Ignition |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | 3D Map |
| **Data Type** | sbyte (signed byte) |
| **Address** | ROM-specific (see Atlas definition file) |

## Description

Primary ignition timing base table used when Tumble Generator Valves (TGVs) are closed and AVCS (Active Valve Control System) cam timing is disabled. This is one of four base ignition tables that blend together based on TGV position and AVCS state.

This table provides the foundational timing values before any dynamic advance, knock correction, or other compensations are applied.

## Axes

### X-Axis
| Property | Value |
|----------|-------|
| **Parameter** | Engine RPM |
| **Units** | RPM |
| **Range** | 0 - 7000+ |
| **Resolution** | Variable (typically 250-500 RPM increments) |

### Y-Axis
| Property | Value |
|----------|-------|
| **Parameter** | Engine Load |
| **Units** | g/rev (grams per revolution) |
| **Range** | 0 - 3.0+ |
| **Resolution** | Variable |

## Cell Values

| Property | Value |
|----------|-------|
| **Units** | Degrees BTDC (Before Top Dead Center) |
| **Data Type** | sbyte (signed byte) |
| **Range** | -20 to +50 |
| **Default Range** | Varies by cell (typically 5-35 degrees) |

## Functional Behavior

The ECU blends between the four primary ignition base tables using two ratio parameters:

1. **Engine - TGV Map Ratio (%, ubyte)** - Determines blend between TGVs Closed and TGVs Open tables
2. **Engine - AVCS Map Ratio (%, ubyte)** - Determines blend between AVCS Disabled and AVCS Enabled tables

The resulting base timing is then modified by:
- Dynamic Advance tables (scaled by DAM)
- Knock correction (KCA/KCLR)
- Temperature compensations
- Start-up enrichment timing

Final timing is monitored via "Ignition - Commanded Final (deg, sbyte)".

## Related Tables

- [Ignition - Primary - TGVs Closed (AVCS Enabled)](./primary-tgvs-closed-avcs-enabled.md)
- [Ignition - Primary - TGVs Open (AVCS Disabled)](./primary-tgvs-open-avcs-disabled.md)
- [Ignition - Primary - TGVs Open (AVCS Enabled)](./primary-tgvs-open-avcs-enabled.md)
- [Ignition - Primary - Advance - TGVs Closed (Base)](./advance-tgvs-closed-base.md)

## Related Parameters (Datalog)

| Parameter Name | Description |
|----------------|-------------|
| Ignition - Primary - Base Table (deg, sbyte) | Monitored base timing after table blending |
| Ignition - Commanded Final (deg, sbyte) | Final timing sent to coils |
| Engine - TGV Map Ratio (%, ubyte) | Current TGV blend ratio |
| Engine - AVCS Map Ratio (%, ubyte) | Current AVCS blend ratio |
| Knock Control - Dynamic Advance Multiplier (ubyte) | DAM value (0.00-1.00) |
| Knock - Feedback Correction (deg, sbyte) | Real-time knock correction |

## Tuning Notes

- This table is primarily active at lower RPM and during cold engine operation when TGVs remain closed
- TGVs typically open above ~3500-4000 RPM, shifting blend toward the "TGVs Open" tables
- Conservative timing in this table helps prevent knock during cold start conditions
- When tuning, focus first on the cells active during your typical operating conditions
- Use datalog to identify which load/RPM cells are most frequently accessed
- Always tune with knock monitoring enabled and DAM observed

## Warnings

- Excessive ignition advance can cause detonation (knock), leading to engine damage
- Monitor Feedback Knock Correction and Fine Knock Learn during tuning
- Any sustained knock correction indicates timing should be reduced
- DAM dropping below 1.0 indicates the ECU is reducing advance due to detected knock
- Always use quality fuel meeting minimum octane requirements (91+ AKI recommended)

---
*Last updated: 2024-12-14*
*Platform: VA WRX MT (FA20DIT)*
