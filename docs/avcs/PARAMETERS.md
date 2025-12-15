# AVCS Runtime Parameters

## Overview

These runtime parameters control and monitor the AVCS (Active Valve Control System) for variable intake and exhaust cam timing. Parameters are calculated continuously based on engine conditions and used to command the AVCS solenoid valves.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Minimum Activation Speed** | `scalar` | km/h | Minimum vehicle speed for AVCS activation |
| **AVCS Enable Ratio** | `ubyte` | - | Enable condition ratio/threshold |

## Parameter Details

### Minimum Activation Speed

**Type:** Scalar (single value)
**Unit:** km/h (kilometers per hour)
**Typical Value:** 1.17 km/h

**Description:**
Defines the minimum vehicle speed required before the ECU will activate AVCS control. Below this speed, cam timing is held at the default mechanical position (full retard).

**Purpose:**
- Prevents AVCS operation during engine start
- Ensures stable oil pressure before AVCS activation
- Avoids cam timing changes during launch/crawling
- Protects AVCS system during very low oil pressure conditions

**Tuning Considerations:**
- Stock value is very low (~1 km/h) to allow AVCS almost immediately
- Increase if experiencing AVCS instability during idle or launch
- Decrease only if you need AVCS active at complete standstill (e.g., dyno tuning)
- Setting too high will delay AVCS engagement during normal driving

### AVCS Enable Ratio

**Type:** `ubyte` (unsigned 8-bit integer)
**Unit:** Dimensionless ratio

**Description:**
An enable threshold or ratio used to determine when AVCS control is permitted. Likely related to oil pressure, engine temperature, or system readiness conditions.

**Purpose:**
- Additional safety check before enabling AVCS
- May compare actual vs target conditions
- Prevents AVCS operation when system is not ready

**Typical Behavior:**
- Value must exceed threshold for AVCS to activate
- Combined with other enable conditions (speed, temp, oil pressure)
- Part of multi-condition AVCS enable logic

## AVCS Enable Logic

The ECU enables AVCS control when ALL conditions are met:

1. **Vehicle Speed** ≥ Minimum Activation Speed
2. **Engine Coolant Temperature** > Minimum Temperature (typically 60°C)
3. **Engine Oil Pressure** > Minimum Pressure (typically 150 kPa)
4. **AVCS Enable Ratio** > Threshold
5. **No AVCS System DTCs** (Diagnostic Trouble Codes)
6. **Engine Running Time** > Minimum Time (typically 2-3 seconds)

If any condition fails, AVCS is disabled and cams return to mechanical default position.

## AVCS Disable Conditions

AVCS will be forcibly disabled if:
- Vehicle speed drops below activation speed
- Engine RPM exceeds maximum AVCS control limit (typically 6800 RPM)
- Coolant temperature exceeds maximum limit (overheat protection)
- Oil pressure drops below minimum threshold
- AVCS system fault detected (stuck cam, solenoid fault, position sensor error)

## Related Tables

These parameters work with AVCS calibration tables:

**Intake Cam Tables:**
- AVCS - Intake - Target tables (various operating conditions)
- AVCS - Intake - Limits (maximum advance/retard)
- AVCS - Intake - Compensation (corrections for temp, load, etc.)

**Exhaust Cam Tables:**
- AVCS - Exhaust - Target tables
- AVCS - Exhaust - Limits
- AVCS - Exhaust - Compensation

**Control Parameters:**
- AVCS PID control gains
- AVCS solenoid duty cycle limits
- AVCS ramp rates (how fast cams can move)

## Datalogging

**Essential AVCS Parameters:**
- AVCS Intake Target (from tables)
- AVCS Intake Actual (from position sensor)
- AVCS Intake Error (Target - Actual)
- AVCS Intake Duty Cycle (solenoid command)
- Same for Exhaust cam
- Engine Oil Pressure
- Engine Oil Temperature

**Monitoring:**
- Error should be < 3° during steady-state operation
- Larger errors indicate:
  - Low oil pressure
  - Worn AVCS components
  - Solenoid failure
  - Stuck cam gear
  - Position sensor fault

## Tuning Notes

### Minimum Activation Speed

**Stock Value Works Well:**
- Default ~1 km/h allows AVCS almost immediately
- Only modify if experiencing specific issues

**Increase Speed (to 5-10 km/h) if:**
- AVCS hunting/instability during idle
- Low oil pressure at idle with aftermarket oil system
- Launch control compatibility issues
- Wanting simpler behavior during parking lot maneuvers

**Decrease Speed (to 0 km/h) if:**
- Need AVCS active for stationary dyno tuning
- Want AVCS control during idle (not usually beneficial)
- Testing AVCS calibration without driving

### AVCS Enable Ratio

**Typically Not Modified:**
- Internal calculation used by ECU
- Exact function may vary by ECU calibration version
- Changing may disable AVCS entirely or cause unexpected behavior

**If Modifying:**
- Make small incremental changes
- Verify AVCS still activates properly
- Monitor for DTCs after changes
- Test across full range of engine temperatures and conditions

## Diagnostic Tips

**AVCS Not Activating:**
1. Check vehicle speed > Minimum Activation Speed
2. Verify coolant temperature > 60°C
3. Check engine oil pressure > 150 kPa
4. Scan for AVCS-related DTCs
5. Monitor AVCS Enable Ratio value in datalog
6. Check AVCS solenoid electrical connections

**AVCS Hunting/Unstable:**
1. May need to increase Minimum Activation Speed
2. Check oil pressure stability
3. Verify AVCS PID gains are appropriate
4. Check for mechanical issues (worn cam gear, solenoid)
5. Confirm oil viscosity is correct (5W-30 recommended)

**AVCS Stuck at Default Position:**
1. Verify enable conditions are met
2. Check for AVCS system DTCs
3. Test AVCS solenoid operation (bidirectional controls)
4. Inspect cam position sensors
5. Check oil control valve (OCV) for clogging

## Technical Details

**Oil Pressure Requirement:**
- AVCS uses engine oil pressure to move cam gears
- Minimum ~150 kPa (22 psi) required for reliable operation
- Low oil pressure = sluggish or non-functional AVCS
- High-performance oils (0W-20, 0W-30) may reduce AVCS response

**Temperature Effects:**
- Cold oil (high viscosity) = slower AVCS response
- Hot oil (low viscosity) = faster response but potential pressure drop
- AVCS disabled until coolant > ~60°C to ensure oil is fluid enough

**Response Time:**
- Full range cam movement (0° to max advance): ~1-2 seconds
- Faster at higher RPM (more oil flow)
- Slower when oil is cold or pressure is marginal

**Mechanical Default Position:**
- Springs in cam gear hold cams at full retard when AVCS is off
- This is the fail-safe position (most overlap, conservative timing)
- Engine will run safely even if AVCS completely fails
