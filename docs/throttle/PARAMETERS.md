# Throttle System Runtime Parameters

## Overview

Runtime parameters for electronic throttle control (drive-by-wire). These parameters control throttle position, torque management, and pedal response in the electronic throttle system.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Cruise Control Requested Torque** | `ubyte` | - | Torque request from cruise control system |
| **Main Accelerator Position** | `ushort` | % | Position of accelerator pedal |
| **Requested Torque Final** | `ushort` | Nm | Final calculated torque request |

## Parameter Details

### Main Accelerator Position

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** % (percentage, 0-100%)

**Description:**
Position of the accelerator pedal as measured by the accelerator pedal position sensor (APPS). This is the driver's direct input for power request.

**Sensor Configuration:**
- Dual redundant sensors (APPS1 and APPS2)
- Different voltage ranges for safety validation
- ECU compares both sensors - must agree within tolerance

**Typical Values:**
- 0% = Pedal fully released (idle)
- 10-20% = Light acceleration, cruise
- 30-50% = Moderate acceleration
- 70-90% = Hard acceleration
- 100% = Wide-open pedal (full power request)

**Pedal Calibration:**
- 0% calibrated at full pedal release
- 100% calibrated at full pedal depression
- Dead zones at 0% and 100% (typically 2-5%)

**Safety Features:**

**Sensor Disagreement:**
- If APPS1 and APPS2 differ by >10%:
  - Limp mode activated
  - Throttle limited to ~20% maximum
  - Check engine light (DTC P0120-P0124)

**Stuck Throttle Detection:**
- If pedal >90% for extended time:
  - ECU monitors for brake application
  - Brake + pedal = reduce throttle to idle

**Pedal vs Throttle Relationship:**
- NOT 1:1 mapping
- Drive-by-wire allows tunable response curve
- More aggressive mapping = "sporty" feel
- Less aggressive = "smooth/comfort" feel

### Requested Torque Final

**Type:** `ushort` (unsigned 16-bit integer)
**Unit:** Nm (Newton-meters)

**Description:**
Final calculated engine torque request after all modifiers and limits are applied. This is what the ECU attempts to deliver via throttle position, boost control, and ignition timing.

**Calculation:**
```
Base Torque Request = f(Accelerator Position, RPM, Gear)
Modified Torque = Base × Cruise Control × Traction Control × VDC × Launch Control
Requested Torque Final = min(Modified Torque, Torque Limits)
```

**Torque Sources:**

**Driver Request:**
- Primary input from accelerator pedal
- Pedal position → torque request table lookup
- Non-linear: more sensitive at low pedal positions

**Cruise Control:**
- Overrides driver request when active
- PI controller maintains set speed
- Smooth torque changes for comfort

**Traction Control:**
- Reduces torque during wheelspin
- Fast response (within 1 engine cycle)
- Calculated from wheel speed difference

**VDC (Stability Control):**
- Reduces torque during oversteer/understeer
- Works with selective braking
- Helps maintain vehicle stability

**Launch Control:**
- Limits torque during launch to prevent wheelspin
- RPM-based torque reduction
- Gradually increases allowed torque as vehicle accelerates

**Torque Limits:**

**Engine Protection:**
- Maximum torque at given RPM (rod/bearing limits)
- Reduced torque when coolant temp excessive
- Torque limit during warmup

**Transmission Protection:**
- Lower torque limits in lower gears (1st/2nd)
- Prevents transmission damage from excessive shock loads

**Emissions/Drivability:**
- Torque smoothing during shifts
- Gradient limits (maximum torque rate of change)
- Prevents harsh throttle response

**Typical Values:**
- Idle: 0-20 Nm
- Light cruise: 50-80 Nm
- Moderate acceleration: 150-200 Nm
- Hard acceleration: 250-300 Nm
- WOT peak torque: 350-400 Nm (stock), 450-550 Nm (modified)

**Uses:**
- Electronic throttle position calculation
- Boost control target
- Ignition timing optimization
- Transmission shift scheduling
- Traction/stability control

### Cruise Control Requested Torque

**Type:** `ubyte` (unsigned 8-bit integer)
**Unit:** Dimensionless (0-255 scale, or percentage)

**Description:**
Torque request from the cruise control system when active. Overrides or blends with driver accelerator input.

**Cruise Control Operation:**

**Set Speed:**
- Driver activates cruise at current speed
- ECU stores set speed as target
- PI controller maintains speed

**PI Control:**
```
Error = Set Speed - Actual Speed
P_term = Error × P_gain
I_term = Integral(Error) × I_gain
Cruise Torque = P_term + I_term
```

**Proportional (P):**
- Immediate response to speed error
- Large error = large torque change
- Fast correction but can overshoot

**Integral (I):**
- Accumulated error over time
- Eliminates steady-state error (e.g., on hills)
- Prevents speed drift

**Torque Blending:**

**Cruise Active, Pedal Released:**
- Cruise torque = 100% of request
- Driver pedal = ignored

**Cruise Active, Pedal Pressed:**
- Driver override
- Cruise disables or blends
- Allows driver to accelerate past set speed

**Cruise Active, Brake Pressed:**
- Immediate cruise deactivation
- Torque request drops to zero
- Safety feature

**Typical Behavior:**
- Level ground: Moderate steady torque
- Uphill: Increasing torque to maintain speed
- Downhill: Reduced torque (may request negative torque/engine braking)
- Acceleration: Higher torque request to reach set speed

**Limitations:**
- Maximum torque limited (prevents aggressive acceleration)
- Maximum acceleration rate limited (smooth operation)
- Will not downshift unless speed error very large

## Electronic Throttle Control (Drive-by-Wire)

### System Components

**Accelerator Pedal:**
- Dual position sensors (APPS1, APPS2)
- No mechanical linkage to throttle
- Pure electrical signal to ECU

**Throttle Body:**
- Electronic motor-driven throttle plate
- Dual position sensors (TPS1, TPS2)
- Return spring (fail-safe to closed position)
- Motor controlled by ECU

**ECU:**
- Reads accelerator pedal position
- Calculates desired throttle position
- Commands throttle motor
- Monitors throttle position feedback
- Compares commanded vs actual position

### Throttle Position Calculation

**Torque-Based Control:**
Modern ECUs use torque-based throttle control:

1. **Driver Input:** Accelerator position → Torque request
2. **Torque Calculation:** Apply limits and modifiers → Requested Torque Final
3. **Throttle Position:** Torque request → Throttle position (via torque model)

**Torque Model:**
```
Throttle Position = f(Requested Torque, RPM, Boost, Cam Position, ...)

The ECU has internal model of:
- Airflow vs throttle position
- Airflow vs boost pressure
- Airflow vs cam timing
- Torque vs airflow

This model calculates throttle position needed to achieve torque target.
```

**Benefits:**
- Allows smooth integration of cruise control, traction control, VDC
- All systems request torque, not throttle position
- ECU arbitrates between conflicting requests
- Smoother coordination of throttle, boost, timing

### Pedal Response Mapping

**Stock Mapping:**
- Progressive response (non-linear)
- Sensitive at low pedal positions (0-30%)
- Less sensitive at high positions (70-100%)
- Designed for smooth, predictable behavior

**Sport Mode Mapping:**
- More aggressive response
- Higher torque request for given pedal position
- Quicker throttle opening
- "Sharper" feel

**Tuning Pedal Maps:**

**More Aggressive:**
- Increase torque request at low pedal positions
- Throttle opens faster for given pedal input
- "Sportier" feel, more immediate response
- Can feel jerky or unrefined if too aggressive

**Less Aggressive:**
- Reduce torque request at low pedal positions
- Throttle opens slower for given pedal input
- "Smoother" feel, more progressive
- Better for traction in low-grip conditions

**Example Mappings:**

Stock:
- 10% pedal → 50 Nm torque
- 50% pedal → 200 Nm torque
- 100% pedal → 400 Nm torque

Sport:
- 10% pedal → 80 Nm torque (+60%)
- 50% pedal → 250 Nm torque (+25%)
- 100% pedal → 400 Nm torque (same)

Comfort:
- 10% pedal → 30 Nm torque (-40%)
- 50% pedal → 170 Nm torque (-15%)
- 100% pedal → 400 Nm torque (same)

## Safety Systems

### Traction Control (TC)

**Operation:**
1. Compare wheel speeds (front vs rear, left vs right)
2. Detect wheelspin (driven wheels faster than non-driven)
3. Reduce Requested Torque to eliminate wheelspin
4. Restore torque as traction regained

**Torque Reduction:**
- Immediate (within 1-2 engine cycles)
- Can reduce torque to near zero if needed
- Gradually increases torque as wheelspin reduces

**Methods:**
- Throttle closure (primary)
- Ignition retard (fast response)
- Fuel cut (aggressive reduction)
- Brake application to spinning wheel (AWD)

### VDC (Vehicle Dynamics Control)

**Stability Control:**
1. Monitor: Steering angle, yaw rate, lateral acceleration
2. Detect: Oversteer or understeer
3. Intervene: Reduce torque + selective braking
4. Result: Maintain vehicle stability

**Torque Reduction:**
- Moderate reduction (30-50%)
- Works with braking (more effective)
- Prevents power-on oversteer
- Helps maintain intended path

### Launch Control

**Purpose:**
- Limit wheelspin during hard launch
- Optimize acceleration from standstill
- Typically for performance/drag racing applications

**Operation:**
1. Detect launch conditions (RPM > threshold, vehicle speed = 0)
2. Limit torque to prevent wheelspin
3. Monitor wheel speed and traction
4. Gradually increase allowed torque as speed increases
5. Disengage when above speed threshold

**Torque Limiting:**
- Holds RPM at launch RPM (e.g., 4000-5000 RPM)
- Limits torque to traction-limited value
- Ramps up torque as vehicle accelerates
- Full torque available above ~30 mph

## Datalogging Recommendations

**Essential Throttle Parameters:**
- Main Accelerator Position (driver input)
- Throttle Position (actual throttle)
- Requested Torque Final (calculated request)
- Cruise Control Requested Torque (if active)

**Traction Control Analysis:**
- Requested Torque Final
- Wheel Speeds (all 4 wheels)
- Traction Control Active flag
- Torque reduction amount

**Throttle Response Analysis:**
- Main Accelerator Position
- Requested Torque Final
- Plot: Torque vs Pedal (should follow desired curve)
- Throttle Position

**Cruise Control Diagnostics:**
- Cruise Control Requested Torque
- Vehicle Speed (actual vs set speed)
- Throttle Position
- Cruise control status (on/off/coast/accel)

## Related Tables

**Pedal Mapping:**
- Throttle → Requested Torque → Pedal maps (pedal % → torque request)
- Different maps for different drive modes (normal/sport/eco)

**Throttle Position:**
- Throttle → Target Throttle → Torque model tables (torque → throttle %)
- RPM and boost dependent

**Cruise Control:**
- Throttle → Requested Torque → Cruise control PI gains
- Cruise → Torque limits and ramp rates

**Traction Control:**
- Engine → Traction Control → Torque reduction tables
- Intervention thresholds and recovery rates

## Tuning Notes

### Pedal Response

**Stock pedal mapping optimized for:**
- Smooth daily driving
- Predictable response
- Good low-speed drivability
- Acceptable for most drivers

**Increase response if:**
- Want "sportier" feel
- Track/autocross use
- Quick throttle response desired
- Willing to sacrifice some smoothness

**Decrease response if:**
- Smoother operation desired
- Low-traction conditions (snow, rain)
- Towing or heavy loads
- Turbo lag very noticeable

### Cruise Control

**Stock cruise control well-calibrated**

**Tuning cruise PI gains:**
- Increase P gain: Faster response, potential oscillation
- Decrease P gain: Slower response, more stable
- Increase I gain: Eliminates steady-state error faster
- Decrease I gain: Prevents overshoot, slower settling

**Common Issues:**
- Speed oscillation on hills: Reduce P gain or increase I gain
- Speed drift on grades: Increase I gain
- Harsh throttle changes: Reduce P gain, add torque rate limits

### Traction Control Tuning

**Stock TC very conservative (safety first)**

**Less Intrusive TC:**
- Increase wheelspin threshold (allow more slip)
- Reduce torque reduction amount
- Faster torque recovery
- Better for performance driving

**More Intrusive TC:**
- Decrease wheelspin threshold
- Increase torque reduction
- Slower torque recovery
- Better for low-traction conditions

**TC Disable:**
- Many drivers prefer TC off for track use
- Requires skilled throttle control
- Risk of wheelspin and loss of traction

### Launch Control

**Setting Launch RPM:**
- Too low: Slow launch, not utilizing full traction
- Too high: Excessive wheelspin, slower 60-ft time
- Optimal: Maximum torque without breaking traction

**Typical Launch RPM:**
- AWD, good traction: 4000-5000 RPM
- AWD, poor traction: 3000-4000 RPM
- RWD/FWD: 2500-3500 RPM (higher wheelspin risk)

**Torque Ramp Rate:**
- Fast ramp: Quicker acceleration, risk of wheelspin
- Slow ramp: Safer, may be slower overall
- Tune based on tire grip and surface conditions
