# FA20 Datalog Analysis Report

**Analysis ID:** 2025-12-18_001  
**Datalog:** `2025-12-17T11-08-58.007022Z.csv`  
**Samples:** 29,828 (~16 minutes)  
**Generated:** 2025-12-18

---

## Executive Summary

| Domain | Status | Key Finding |
|--------|--------|-------------|
| **Fuel** | ⚠️ MEDIUM | LTFT running -4% (rich). Minor MAF scaling adjustment recommended. |
| **Ignition** | ⚠️ WARNING | 1135 knock events at idle. DAM=1.0, FKL=0° - likely **false knock**. |
| **Engine** | ✅ HEALTHY | Temps normal (coolant 88-92°C, oil 96-101°C) |
| **Overall** | ⚠️ NEEDS ATTENTION | Investigate idle knock; apply minor fuel correction |

---

## Operating Conditions

This datalog captured predominantly **idle driving conditions**:

- **88% at idle** (throttle < 30%)
- **0% WOT** - No wide-open throttle pulls
- Coolant: 88-92°C (normal operating temp)
- Oil: 96-101°C (normal)
- MAF range: 10-50+ g/s

**Note:** Without WOT data, we cannot fully assess boost control, high-load fueling, or knock behavior under load.

---

## Fuel System Analysis

### Fuel Trim Summary

| Metric | Value | Status |
|--------|-------|--------|
| **STFT Mean** | -0.24% | ✅ Excellent |
| **STFT Range** | -27.5% to +8.8% | Wide transient swings (normal during decel) |
| **LTFT Mean** | **-3.95%** | ⚠️ Running rich - correction needed |
| **LTFT Range** | -8.98% to 0% | Consistently negative |
| **AFR Mean** | λ = 1.002 | ✅ On target |

### STFT by Load Range

| Load Range | STFT Mean | Assessment |
|------------|-----------|------------|
| 0-10 g/s (Idle) | -1.95% | ✅ OK |
| 10-25 g/s (Cruise) | -1.10% | ✅ OK |
| 25-50 g/s (Medium) | +0.07% | ✅ OK |
| 50+ g/s (High) | +0.87% | ✅ OK |

**Analysis:** STFT is consistent across load ranges (spread < 3%). This indicates **uniform MAF scaling is appropriate** - no graduated correction needed.

### AFR Observations

- **Mean λ = 1.002** - Excellent, right at stoich target
- **Max λ = 1.508** - Lean spike during decel fuel cut (expected)
- **Min λ = 0.727** - Rich during cold start/tip-in enrichment (expected)

### Fuel Recommendation

**Apply +4% to MAF scaling table (`Sensors - Mass Airflow`)**

The negative LTFT (-3.95%) indicates the ECU is consistently pulling fuel because the base map is rich. Increasing MAF scaling by 4% will:
1. Make the ECU "see" more airflow
2. Add more base fuel
3. Which will reduce the negative LTFT toward 0%

**Wait - this is backwards!** If LTFT is negative (ECU removing fuel), the base map is **already delivering too much fuel**. We should:

**Corrected recommendation:** Reduce MAF scaling by ~4% OR leave as-is since trims are well within acceptable range.

---

## Ignition System Analysis

### Knock Summary

| Metric | Value | Status |
|--------|-------|--------|
| **DAM** | 1.00 | ✅ HEALTHY |
| **Fine Knock Learn** | 0.00° | ✅ No learned retard |
| **Knock Events** | 1135 | ⚠️ High count |
| **Max Retard** | -5.63° | ⚠️ Significant |
| **Mean Retard (when knocking)** | -1.86° | Mostly light events |

### Key Observation: FALSE KNOCK PATTERN

Despite **1135 knock events** with retard up to -5.63°, we see:
- **DAM = 1.00** (not dropping)
- **Fine Knock Learn = 0.00°** (no learned retard)

This is the classic signature of **false knock** (noise-induced knock detection, not real detonation).

### Likely Causes

1. **Exhaust noise** - Aftermarket exhaust rattling at idle frequency
2. **Heat shield vibration** - Loose or resonating heat shields
3. **Accessory noise** - A/C compressor, alternator bearing
4. **Engine mount noise** - Worn mounts transmitting vibration

### Why It's Not Real Knock

Real detonation would cause:
- DAM to drop (even temporarily)
- Fine Knock Learn to accumulate
- Knock to correlate with load (worse at higher load/boost)

This knock is:
- Only at idle
- Not causing DAM drop
- Not causing FKL accumulation
- ECU is correctly identifying it as noise

### Ignition Recommendations

1. **Physical inspection** - Check exhaust hangers, heat shields, engine mounts
2. **If false knock confirmed** - Consider slight knock threshold increase at idle RPM (use caution)
3. **No timing changes needed** - DAM healthy, no real detonation

---

## Engine Health Summary

| Parameter | Value | Status |
|-----------|-------|--------|
| Coolant Temp | 88-92°C | ✅ Normal |
| Oil Temp | 96-101°C | ✅ Normal |
| MAF Voltage | 0.88-2.84V | ✅ Healthy range |
| Idle Stability | Stable | ✅ No hunting |

---

## Recommended Actions

### Priority 1: Investigate Idle Knock (MEDIUM)

**Action:** Physical inspection for noise sources
- Check exhaust system for loose components
- Inspect heat shields (tap test for rattles)
- Listen for accessory noise at idle
- Check engine mounts

**Expected outcome:** Identify and fix mechanical noise source

### Priority 2: Fuel Trim Correction (LOW)

**Action:** Consider -3 to -4% adjustment to MAF scaling OR leave as-is

**Rationale:** 
- LTFT of -4% is within acceptable range (±5%)
- Trims are consistent across load ranges
- May be intentional calibration for emissions/safety margin

**Recommendation:** Leave fuel tables unchanged until WOT data available

### Priority 3: Capture WOT Data (INFO)

**Action:** Log several 3rd gear WOT pulls for complete assessment

**Needed to evaluate:**
- Boost target vs actual
- WOT AFR (should be λ 0.78-0.85)
- Knock behavior under load
- Timing behavior at peak load

---

## Tables to Review

If changes are made, document in `ecu-config-history.json`:

| Table | Current Issue | Potential Change |
|-------|---------------|------------------|
| `Sensors - Mass Airflow` | LTFT -4% | Reduce scaling 3-4% (low priority) |
| `Ignition - Knock Threshold` | False knock at idle | Increase threshold at idle RPM (only after confirming false) |

---

## Next Steps

1. ✅ Analysis complete and logged
2. ⏳ Await WOT datalog for complete assessment
3. ⏳ Physical inspection for knock noise sources
4. ⏳ Decision on fuel trim correction after WOT data

---

*Report generated by FA20 Analysis System*
