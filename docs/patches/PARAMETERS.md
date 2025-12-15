# Patches

## Overview

Patches are ECU ROM modifications that enable advanced features not available in the stock calibration. These include enhanced datalogging capabilities and real-time table editing without reflashing the ECU.

## Patch Categories

### Advanced Datalogging

Enables extended parameter logging and increased logging rates beyond stock ECU limitations.

**Features:**
- Higher logging frequency (up to 4x faster than stock)
- Additional parameters not available in stock ROM
- Extended parameter resolution (16-bit vs 8-bit for select PIDs)
- Custom calculated parameters
- Extended memory buffer for longer log sessions

**Use Cases:**
- High-resolution knock detection analysis
- Transient boost response tuning
- Fuel pressure fluctuation diagnosis
- Rapid throttle response characterization

### Realtime Tables

Allows modification of calibration tables in real-time without reflashing the ECU. Changes take effect immediately during engine operation.

**Supported Tables:**
- Boost targets
- Ignition timing maps
- Fuel maps
- AVCS targets
- Wastegate duty cycle
- MAF scaling

**Safety Features:**
- Changes revert to base calibration on ECU reset
- Limited to safe parameter ranges
- Does not modify ROM permanently
- Requires active connection to tuning software

### Realtime Tables (2020 Only)

Extended realtime table functionality specific to 2020+ model year ECUs with updated hardware/software architecture.

**Additional Capabilities:**
- Support for newer ECU memory architecture
- Enhanced parameter range checking
- Additional safety interlocks
- Compatibility with updated sensor inputs

## Technical Details

### Implementation
Patches modify ECU ROM code to:
- Intercept table lookups and redirect to RAM-based tables
- Add hooks for real-time parameter injection
- Expand logging buffers in unused ECU memory
- Insert custom calculation routines

### Memory Usage
- Advanced Datalogging: ~4KB RAM, 8KB ROM
- Realtime Tables: ~16KB RAM for table storage
- Combined patches: ~20KB total memory footprint

### Performance Impact
- Minimal (<0.5%) CPU overhead
- No measurable impact on engine response time
- Logging may reduce available bandwidth for other diagnostic functions

## Usage Workflow

### Enabling Patches

1. **Verify ECU Compatibility**: Confirm ECU model and calibration ID support patches
2. **Flash Patched ROM**: Use Atlas to flash ROM with patch modifications enabled
3. **Connect to ECU**: Establish communication with patching software
4. **Activate Features**: Enable desired patch features (datalogging, realtime tables)

### Using Realtime Tables

1. **Load Base Calibration**: Start with proven safe calibration
2. **Enable Realtime Mode**: Activate realtime table editing in Atlas
3. **Make Incremental Changes**: Adjust tables in small steps during operation
4. **Monitor Results**: Watch datalog parameters for unexpected behavior
5. **Save Working Tables**: Export successful changes to base calibration
6. **Reflash ECU**: Burn final calibration to ROM permanently

## Safety Warnings

- **Realtime changes are volatile**: All modifications lost on ECU power cycle
- **No safety net**: Realtime tables bypass normal calibration validation
- **Engine damage possible**: Excessive timing advance or lean AFR can cause detonation
- **Always monitor knock**: Watch knock sensors continuously during realtime tuning
- **Use on dyno first**: Test realtime changes in controlled environment before street use
- **Have safe base calibration**: Ensure underlying ROM is safe if realtime connection drops

## Recommended Workflow

### Dyno Tuning with Realtime Tables

1. Flash conservative base calibration
2. Enable realtime table patches
3. Make pull on dyno with realtime adjustments
4. Review datalog for knock, AFR, boost deviation
5. If successful, save realtime table values
6. Repeat for next operating region
7. Build complete calibration from proven realtime values
8. Flash final ROM with all changes burned in
9. Validation pull without realtime mode to confirm

### Advanced Datalogging Setup

1. Flash ROM with advanced datalogging patch
2. Configure logging parameters in Atlas
3. Set logging rate (1Hz to 4Hz depending on parameters)
4. Select extended parameters not available in stock
5. Perform test drive or dyno pull
6. Export high-resolution log for analysis
7. Use data for calibration refinement

## Related Tables

Patches interact with all calibration categories:
- **Ignition**: Realtime timing adjustments
- **Fuel**: Realtime fueling changes
- **Airflow**: Realtime boost control
- **AVCS**: Realtime cam timing
- **All Categories**: Advanced datalogging coverage

## Tuning Notes

- Start with small changes (2-3° timing, 5% fuel, 2psi boost) in realtime mode
- Always watch knock sensors - back out immediately on any knock event
- Realtime mode is for **tuning development only**, not daily driving
- Save proven realtime values to permanent calibration before relying on them
- Advanced datalogging adds ~100ms latency to parameter updates
- Some parameters cannot be logged simultaneously due to ECU bus bandwidth limits
