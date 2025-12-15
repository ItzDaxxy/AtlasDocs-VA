# Analytical Parameters

## Overview

The Analytical subsystem provides calculated performance metrics and vehicle dynamics parameters used for tuning analysis, power estimation, and vehicle modeling. These parameters are computed in real-time using inputs from sensors, calibration tables, and physical vehicle properties.

## Calculated Performance Parameters

Runtime calculations for power, torque, and airflow analysis.

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Acceleration (Integration)** | - | m/s² | Calculated acceleration from integration |
| **Acceleration (Sensor)** | - | m/s² | Direct accelerometer sensor reading |
| **Air Temperature Delta (Intake to Manifold)** | - | Δ°C | Temperature rise from intake to manifold |
| **Boost Pressure** | - | psi | Turbocharger boost pressure |
| **Estimated Power (Old Method)** | - | HP | Legacy power estimation algorithm |
| **Estimated Torque (Old Method)** | - | ft-lb | Legacy torque estimation algorithm |
| **Estimated Tractive Power** | - | HP | Power at wheels accounting for drivetrain loss |
| **Estimated Tractive Torque** | - | Nm | Torque at wheels accounting for drivetrain loss |
| **Estimated Wheel Power** | - | HP | Power delivered to wheels |
| **Estimated Wheel Torque** | - | Nm | Torque delivered to wheels |
| **Mass Air Flow (Fuel Trim Corrected)** | - | g/sec | MAF reading with fuel trim corrections applied |
| **Total Fuel Trim** | - | % | Combined short-term and long-term fuel trim |

## Vehicle Input Parameters

Physical vehicle properties and environmental conditions used in analytical calculations.

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **Actual Gear Ratio** | - | - | Current transmission gear ratio (calculated) |
| **Ambient Air Density** | - | kg/m³ | Calculated air density from temp/pressure |
| **Ambient Air Temperature** | - | °F | Outside air temperature |
| **Expected Gear Ratio** | - | - | Expected gear ratio from vehicle speed/RPM |
| **Load Reduction Factor** | - | - | Correction factor for calculated load |
| **Relative Humidity** | - | % | Atmospheric relative humidity |
| **Rolling Resistance** | - | N | Calculated rolling resistance force |
| **Rolling Resistance Coefficient** | - | - | Tire rolling resistance coefficient (Crr) |
| **SAE J1349 Correction Factor** | - | - | SAE atmospheric correction for power testing |
| **Tire Aspect Ratio** | - | - | Tire sidewall aspect ratio (height/width) |
| **Tire Loaded Diameter** | - | in | Tire diameter under vehicle load |
| **Tire Revolution Rate** | - | rev/km | Tire revolutions per kilometer |
| **Tire Sidewall Height** | - | mm | Tire sidewall height in millimeters |
| **Tire Total Circumference** | - | in | Total circumference of loaded tire |
| **Tire Unloaded Diameter** | - | in | Tire diameter without vehicle weight |
| **Tire Width** | - | mm | Tire width in millimeters |
| **Tractive Acceleration Force** | - | N | Force available for acceleration |
| **Vehicle Drag** | - | N | Aerodynamic drag force |
| **Vehicle Drag Coefficient** | - | - | Coefficient of drag (Cd) |
| **Vehicle Frontal Area** | - | ft² | Frontal cross-sectional area |
| **Vehicle Gross Weight** | - | lb | Total vehicle weight with occupants/fuel |
| **Wheel Diameter** | - | in | Wheel rim diameter |
| **Wheel Slip** | - | % | Calculated wheel slip percentage |

## Gear Ratio Parameters

Transmission gear ratios used for speed/RPM calculations and gear detection.

| Parameter Name | Data Type | Unit | Description |
|----------------|-----------|------|-------------|
| **1st** | - | - | First gear ratio |
| **2nd** | - | - | Second gear ratio |
| **3rd** | - | - | Third gear ratio |
| **4th** | - | - | Fourth gear ratio |
| **5th** | - | - | Fifth gear ratio |
| **6th** | - | - | Sixth gear ratio |
| **Final Drive** | - | - | Final drive/differential ratio |

## Functional Description

### Power/Torque Estimation
The analytical system estimates engine power and torque using:
- Mass airflow rate
- Air/fuel ratio
- BSFC (Brake Specific Fuel Consumption) assumptions
- Atmospheric corrections (SAE J1349)

### Tractive Performance
Wheel power and torque calculations account for:
- Drivetrain losses (assumed ~15% for AWD)
- Current gear ratio
- Final drive ratio
- Rolling resistance
- Aerodynamic drag

### Vehicle Dynamics
Real-time calculations for:
- Acceleration (both sensor-based and calculated)
- Wheel slip detection
- Gear ratio verification
- Speed error detection

## Usage in Tuning

These parameters are essential for:
- **Dyno Validation**: Compare estimated HP/TQ to dyno results
- **Drivability Analysis**: Monitor tractive force and acceleration
- **Fuel Trim Analysis**: Track total fuel corrections
- **Boost Analysis**: Verify boost pressure vs targets
- **Gear Detection**: Confirm transmission is in expected gear

## Related Tables

Analytical parameters interact with:
- **Airflow**: MAF corrections feed into power calculations
- **Fuel**: Fuel trim affects corrected MAF values
- **Engine**: Load calculations use gear ratios
- **Transmission**: Gear ratios validate speed/RPM relationship

## Tuning Notes

- SAE J1349 correction factor normalizes power to standard atmospheric conditions (77°F, 29.23" Hg, 0% humidity)
- Estimated power is most accurate at steady-state WOT conditions
- Wheel slip >5% indicates traction loss
- Large differences between actual and expected gear ratio indicate calibration issues
- Fuel trim should stay within ±10% during normal operation
