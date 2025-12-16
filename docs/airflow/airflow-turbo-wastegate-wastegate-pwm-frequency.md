# Airflow - Turbo - Wastegate - Wastegate PWM Frequency

## Overview

| Property | Value |
|----------|-------|
| **Category** | Airflow |
| **Platform** | VA WRX (2015-2021) |
| **Table Type** | Scalar (Single Value) |
| **Unit** | HZ |
| **Source File** | `Airflow - Turbo - Wastegate - Wastegate PWM Frequency - 2018 - LF9C102P.csv` |

## Value

**10.0000 HZ**

## Description

Defines the PWM (Pulse Width Modulation) frequency for the wastegate boost control solenoid. At 10 Hz, the solenoid cycles on/off 10 times per second, with the duty cycle (0-100%) determining what percentage of each cycle the solenoid is energized.

Higher frequencies provide smoother control but may exceed solenoid response capability. Lower frequencies can cause audible clicking and less precise control. 10 Hz is a common balance point for OEM wastegate solenoids.

## Related Tables

- **Airflow - Turbo - Wastegate - Duty Initial**: Duty cycle commanded at this frequency
- **Airflow - Turbo - Wastegate - Duty Maximum**: Maximum duty allowed
- **Airflow - Turbo - PI Control**: Closed-loop duty adjustments

## Related Datalog Parameters

- **Wastegate Duty (%)**: Duty cycle at this PWM frequency
- **Wastegate Solenoid State**: Actual solenoid actuation

## Tuning Notes

**Common Modifications:**
- Generally not modified for stock solenoid
- Aftermarket boost controllers may prefer different frequencies
- Some upgraded solenoids support higher frequencies

**Typical Frequency Ranges:**
- Stock solenoid: 10-20 Hz
- Performance solenoids: 20-40 Hz
- MAC-type solenoids: 30-50 Hz

**Considerations:**
- Higher frequency = finer control resolution
- Lower frequency = better solenoid compatibility
- Match to solenoid specification for best results
