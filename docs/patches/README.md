# Patches

ROM patches and code modifications.

## Overview

Patches modify ECU behavior at the code level:
- Feature enables/disables
- Algorithm modifications
- Limit removals
- Custom functionality

## Subcategories

- **Feature Toggles**: Enable/disable specific ECU features
- **Limit Modifications**: Speed limiter, rev limiter adjustments
- **Algorithm Patches**: Modifications to ECU calculation routines

## Tables

| Table Name | Type | Description |
|------------|------|-------------|
| Speed Limiter | Constant | Vehicle speed limiter enable/disable |
| Rev Limiter | Constant | Engine RPM hard limit |
| CEL Disable | Constant | Check Engine Light suppression for specific codes |
| Immobilizer | Constant | Anti-theft immobilizer enable/disable |
| Cold Start Enrichment | Constant | Cold start fueling strategy modifications |

## Key Concepts

### ROM Patches vs Table Edits
- **Table Edits**: Change values in existing calibration tables
- **ROM Patches**: Modify ECU code/logic at the binary level
- Patches are more powerful but require ROM-specific addresses

### Common Patches for VA WRX
1. **Speed Limiter Removal**: Disables factory 180 km/h (Japan) or 250 km/h limit
2. **Rev Limiter Adjustment**: Modify hard cut RPM limit
3. **Secondary Air Injection Disable**: For emissions delete builds
4. **EGR Disable**: Exhaust gas recirculation system bypass

### Safety Considerations
- Document all active patches in your tune file
- Some patches may trigger diagnostic trouble codes
- CEL suppression should be used carefully—codes exist for reasons

## Related Systems

- Potentially affects all other categories depending on patch

## Notes

- Patches are ROM-specific
- May require re-application after ROM updates
- Document any active patches in your tune
