# VDC (Vehicle Dynamics Control)

## Overview

The VDC system monitors vehicle acceleration and stability using accelerometer sensors. These parameters are used for traction control, stability control, and performance monitoring. VDC data is shared between the ECU and the VDC control module for integrated vehicle dynamics management.

## Runtime Parameters

Real-time vehicle dynamics measurements from the VDC accelerometer sensors.

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Lateral Acceleration** | `sbyte` | m/s² | Lateral (side-to-side) acceleration force |
| **Longitudinal Acceleration** | `sbyte` | m/s² | Longitudinal (forward/backward) acceleration force |

## Parameter Details

### Lateral Acceleration

**Type:** `sbyte` (signed 8-bit integer)
**Unit:** m/s² (meters per second squared)
**Range:** -127 to +127 m/s² (±12.9 g)

**Description:**
Measures side-to-side acceleration forces during cornering, lane changes, and lateral weight transfer events.

**Positive Values:** Acceleration to the right (right-hand turn)
**Negative Values:** Acceleration to the left (left-hand turn)
**Zero:** Straight-line travel or neutral lateral forces

**Typical Values:**
- Normal street cornering: ±3-5 m/s² (0.3-0.5g)
- Spirited driving: ±7-10 m/s² (0.7-1.0g)
- Track driving: ±10-15 m/s² (1.0-1.5g)
- Emergency maneuvers: ±15+ m/s² (1.5g+)

**Uses:**
- VDC stability control activation threshold
- Traction control side-to-side weight transfer compensation
- Performance data logging for handling analysis
- Torque vectoring control (AWD models)

### Longitudinal Acceleration

**Type:** `sbyte` (signed 8-bit integer)
**Unit:** m/s² (meters per second squared)
**Range:** -127 to +127 m/s² (±12.9 g)

**Description:**
Measures forward/backward acceleration forces during acceleration, braking, and grade changes.

**Positive Values:** Forward acceleration (throttle application)
**Negative Values:** Deceleration (braking or coasting)
**Zero:** Constant speed on level ground

**Typical Values:**
- Normal acceleration: 2-4 m/s² (0.2-0.4g)
- WOT acceleration: 4-8 m/s² (0.4-0.8g)
- Modified/high-performance: 8-12 m/s² (0.8-1.2g)
- Hard braking: -10 to -15 m/s² (-1.0 to -1.5g)
- Emergency braking: -15+ m/s² (-1.5g+)

**Uses:**
- Launch control traction management
- Hill start assist
- Brake force distribution
- Performance measurement (0-60 mph times)
- Fuel cut prevention during high-g braking

## VDC System Integration

### ECU Interaction

The ECU receives VDC accelerometer data and uses it for:

1. **Traction Control:**
   - Detects wheelspin during high longitudinal acceleration
   - Reduces engine torque via ignition retard and throttle cut
   - Monitors lateral acceleration for cornering traction events

2. **Stability Control:**
   - Compares lateral acceleration to steering angle
   - Detects oversteer/understeer conditions
   - Commands selective brake application and torque reduction

3. **Performance Management:**
   - Fuel cut delay during high-g braking (prevents lean condition)
   - Rev limiter adjustment during launch control
   - Boost control compensation for uphill/downhill acceleration

### VDC Module Functions

The dedicated VDC module uses accelerometer data for:
- ABS brake pressure modulation
- Yaw rate control
- Roll stability control
- Individual wheel brake force distribution
- VDC warning light activation

## Datalogging

VDC parameters are essential for:
- **Traction Analysis:** Identify wheelspin events and traction loss
- **Handling Tuning:** Measure cornering performance and balance
- **Acceleration Testing:** 0-60 mph, quarter-mile times
- **Brake Testing:** Stopping distances and brake balance
- **Track Analysis:** Compare acceleration data across laps

### Recommended Logging Setup

**High-Performance Driving:**
- Log both lateral and longitudinal at 4Hz (4 samples/second)
- Include: vehicle speed, throttle position, brake pressure, steering angle
- Overlay on GPS track map for corner-by-corner analysis

**Drag Racing:**
- Log longitudinal acceleration at 4Hz
- Include: RPM, boost, gear position, wheel speed
- Calculate 60-foot, 330-foot, 1/8-mile, 1/4-mile times

**Road Course:**
- Log both parameters at 4Hz with GPS
- Include: brake pressure, throttle, steering angle, yaw rate
- Analyze corner entry/exit acceleration profiles

## Disabling VDC

Some tuners disable VDC for dedicated track vehicles. Considerations:

**Advantages:**
- No ECU torque reduction during wheelspin
- No brake intervention during oversteer
- Improved lap times for skilled drivers

**Disadvantages:**
- Loss of safety net for traction/stability
- No ABS function in some configurations
- Potential for loss of control
- May affect insurance coverage

**Recommendation:**
Keep VDC enabled for street driving. Use VDC "Sport" mode or momentary disable button for track use. Full VDC delete only appropriate for dedicated race cars with experienced drivers.

## Related Tables

VDC parameters interact with:
- **Engine**: Rev limiters, torque reduction tables
- **Fuel**: Fuel cut delay during deceleration
- **Ignition**: Ignition retard for traction control
- **Transmission**: Launch control gear detection

## Technical Notes

- VDC accelerometer is typically mounted near vehicle center of gravity
- Sensor calibrated at vehicle assembly (zero-g calibration)
- Data transmitted over CAN bus at 50Hz (20ms intervals)
- ECU receives VDC data and subsamples to 10Hz for most control functions
- Accelerometer has built-in temperature compensation
- Sensor fault detection: values pegged at ±127 indicate sensor failure
- Negative temperature coefficient: sensitivity decreases slightly at high temperatures

## Troubleshooting

**Constant Zero Reading:**
- VDC module communication fault
- Check wiring harness and CAN bus termination
- Verify VDC module power and ground

**Pegged Values (±127):**
- Accelerometer sensor failure
- VDC module internal fault
- Requires VDC module replacement

**Erratic Readings:**
- Loose sensor mounting
- CAN bus electrical interference
- Corroded connectors

**Offset from Zero at Rest:**
- Sensor calibration drift
- Vehicle on incline (normal - reading includes gravity component)
- VDC module requires recalibration after mounting position change
