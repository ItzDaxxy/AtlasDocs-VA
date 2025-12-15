# Hooks (Runtime Parameters)

## Overview

Hooks are runtime parameters that serve as inputs and outputs for ECU calculations. These parameters are continuously updated during engine operation and are used throughout the calibration tables for control logic and calculations.

## Runtime Parameters

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **AVCS Exhaust Target Base** | - | ° | Base exhaust cam target before corrections |
| **AVCS Intake Target Base** | - | ° | Base intake cam target before corrections |
| **Boost Target** | - | - | Calculated boost pressure target |
| **Calculated Load** | - | - | ECU-calculated engine load |
| **Calculated Load Canbus Target** | - | - | Load target transmitted over CAN bus |
| **Dynamic Advance Final** | - | ° | Final dynamic ignition advance value |
| **DVAVCS Max Minus Final** | - | - | Maximum AVCS correction limit |
| **Fuel Cut Base Mode** | - | - | Base fuel cut operating mode |
| **Fuel Injector Maximum Final** | - | ms | Maximum injector pulse width limit |
| **Fuel Injector Offset** | - | ms | Injector dead time/offset compensation |
| **Fuel Target Maximum Final** | - | - | Maximum fuel target limit |
| **Ignition Dwell** | - | ms | Coil charging time |
| **Ignition Dwell Commanded Final** | - | ms | Final commanded dwell time |
| **Intake Manifold Pressure** | - | - | Manifold pressure measurement |
| **Knock Learning** | - | - | Knock learning/adaptation value |
| **Manifold Absolute Pressure** | - | - | Absolute manifold pressure (MAP) |
| **Manifold Absolute Pressure Offset** | - | - | MAP sensor offset calibration |
| **Manifold Absolute Pressure Voltage** | - | V | MAP sensor voltage reading |
| **Mass Airflow Corrected** | - | g/sec | MAF reading with corrections applied |
| **OE Boost** | - | - | Original equipment boost value |
| **Other IPRPM** | - | RPM | Intermediate RPM calculation |
| **Requested Torque Final** | - | Nm | Final requested torque output |
| **RPM Active Correction** | - | RPM | Active RPM correction value |
| **Target Throttle Angle** | - | ° | Calculated throttle angle target |
| **Turbo Dynamics Commanded** | - | - | Turbo dynamics control output |
| **Wastegate % Final** | - | % | Final wastegate duty cycle command |

## Parameter Categories

### AVCS (Variable Valve Timing)

**AVCS Intake/Exhaust Target Base:**
- Starting point for cam timing calculations
- Modified by corrections for temperature, load, RPM
- Base values come from AVCS target tables
- Final cam position = Base + Corrections + Adaptations

### Boost Control

**Boost Target:**
- Calculated from boost tables and corrections
- Used as reference for closed-loop boost control
- Modified by atmospheric pressure, temperature, gear

**Wastegate % Final:**
- Final output to wastegate solenoid
- Combines feedforward (base table) and feedback (PID control)
- Higher % = more boost (less exhaust bypass)

**OE Boost:**
- Original equipment boost pressure reading
- Used for comparison with aftermarket sensors

### Engine Load

**Calculated Load:**
- Primary load parameter used throughout calibration
- Based on MAF, RPM, and VE calculations
- Units: g/rev (grams of air per engine revolution)

**Calculated Load (Scaled):**
- Load value scaled for specific table ranges
- Different scaling for different table types

### Fuel System

**Fuel Cut Base Mode:**
- Determines fuel cut operating state
- Modes: Normal, Decel Fuel Cut, Rev Limit Cut, etc.

**Fuel Injector Maximum Final:**
- Upper limit for injector pulse width
- Prevents over-fueling and injector damage

**Fuel Injector Offset:**
- Compensates for injector opening/closing delay
- Varies with battery voltage and fuel pressure

**Fuel Target Maximum Final:**
- Maximum allowed fuel delivery
- Safety limit for extreme conditions

### Ignition System

**Dynamic Advance Final:**
- Total dynamic ignition advance correction
- Includes knock retard, cold start advance, etc.

**Ignition Dwell:**
- Coil primary charging time
- Too short = weak spark, too long = coil overheating

**Ignition Dwell Commanded Final:**
- Final dwell time sent to ignition drivers
- Includes corrections for battery voltage, RPM

### Sensors

**Manifold Absolute Pressure (MAP):**
- Primary load sensing for speed-density calculation
- Used as backup if MAF fails
- Critical for boost control

**Manifold Absolute Pressure Voltage:**
- Raw voltage from MAP sensor
- Used for sensor diagnostics

**Manifold Absolute Pressure Offset:**
- Zero-point calibration for MAP sensor
- Set at atmospheric pressure with engine off

**Mass Airflow Corrected:**
- MAF sensor reading with all corrections applied
- Includes temperature, atmospheric pressure, VE corrections

### Throttle Control

**Requested Torque Final:**
- Driver-requested torque from accelerator pedal
- Modified by cruise control, traction control, VDC

**Target Throttle Angle:**
- Calculated throttle position to achieve requested torque
- Electronic throttle control target

### RPM Parameters

**RPM Active Correction:**
- Real-time RPM correction/adjustment
- Used for idle speed control and rev limiting

**Other IPRPM:**
- Intermediate RPM value for calculations
- May be filtered or predicted RPM

## Usage in Calibration

### Table Inputs

Most calibration tables use these parameters as axis values:
- **X-Axis (Load):** Calculated Load, MAP, Mass Airflow Corrected
- **Y-Axis (Speed):** RPM, Vehicle Speed

### Control Outputs

Many parameters are final outputs of table lookups + corrections:
- Wastegate % Final = Base Table + PID Correction + Atmospheric Correction
- Ignition Dwell Commanded Final = Base Dwell + Voltage Correction
- AVCS Target = Base Target + Temperature Correction + Load Correction

### Feedback Loops

Parameters used in closed-loop control:
- Boost Target vs Actual → adjusts Wastegate %
- Target Throttle vs Actual → adjusts throttle motor
- AVCS Target vs Actual → adjusts AVCS solenoid duty

## Datalogging Recommendations

**Essential Parameters for General Tuning:**
- Calculated Load
- RPM
- Mass Airflow Corrected
- Boost Target vs Actual Boost
- Wastegate % Final
- Dynamic Advance Final
- Fuel Injector Maximum Final

**Boost Control Tuning:**
- Boost Target
- Wastegate % Final
- Turbo Dynamics Commanded
- Manifold Absolute Pressure
- Mass Airflow Corrected

**Ignition Tuning:**
- Dynamic Advance Final
- Ignition Dwell Commanded Final
- Knock Learning
- Feedback Knock

**AVCS Tuning:**
- AVCS Intake Target Base
- AVCS Exhaust Target Base
- Actual Intake Cam Position
- Actual Exhaust Cam Position

## Related Tables

Hook parameters are used throughout all table categories:
- **Ignition**: Uses RPM, Load, Dynamic Advance
- **Fuel**: Uses Load, RPM, Fuel Cut Mode
- **Airflow**: Uses MAF Corrected, Boost Target, Wastegate %
- **AVCS**: Uses AVCS Targets, RPM, Load
- **Engine**: Uses all parameters for protection limits

## Technical Notes

- Parameters update at different rates (10Hz to 100Hz)
- Some parameters are CAN bus values from other modules
- "Final" suffix indicates last calculation step before actuator output
- "Commanded" indicates output to hardware (solenoid, motor, etc.)
- Base values typically come from table lookups
- Corrections are additive or multiplicative depending on parameter type
