# Fuel - Open Loop - AVCS Enabled - Low DAM Threshold

## Overview

| Property | Value |
|----------|-------|
| **Category** | AVCS |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | NONE |
| **Source File** | `Fuel - Open Loop - AVCS Enabled - Low DAM Threshold - 2017 - RogueWRX.csv` |

## Value

**1.0000 NONE**

## Description

Defines the DAM (Dynamic Advance Multiplier) threshold below which the ECU switches to a more conservative "Low DAM" fuel target table when AVCS is enabled. DAM is a knock-based adaptation value that ranges from 0 to 1.

With a threshold of 1.0, the Low DAM fuel table is never used via this threshold (since DAM cannot exceed 1.0). This indicates the stock calibration always uses the standard fuel tables when AVCS is enabled, and the Low DAM fuel table may be activated by other conditions or not used at all.

DAM is reduced when the ECU detects knock, providing a safety margin. Lower DAM values indicate more detected knock activity and a need for protection.

## Related Tables

- **Fuel - Open Loop - AVCS Enabled - Target Base (TGV Open)**: Standard fuel targets
- **Fuel - Open Loop - AVCS Enabled - Target Base Low DAM**: Conservative fuel map
- **Ignition - Primary - AVCS Enabled**: Ignition timing tables

## Related Datalog Parameters

- **DAM (Dynamic Advance Multiplier)**: Compared against this threshold
- **Knock Count**: Causes DAM reduction
- **AVCS Status**: AVCS must be enabled for this table
- **Target AFR**: Output affected by table selection

## Tuning Notes

**DAM Threshold Understanding:**
- DAM = 1.0 means no knock detected
- DAM < 1.0 means knock was detected and adapted
- Threshold of 1.0 means Low DAM table never activates via this path

**Stock Calibration:**
- Threshold at 1.0 effectively disables Low DAM table switching
- May indicate reliance on other protection mechanisms
- Could be lowered to enable conservative fueling under knock

**Potential Modifications:**
- Lower threshold to enable Low DAM table during knock
- Provides additional safety margin with richer targets
- Typically 0.9 or 0.8 to enable with moderate DAM drop
