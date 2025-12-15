#!/usr/bin/env python3
"""
Comprehensive FA20 Datalog Analysis Script
Analyzes fuel, ignition, airflow, and engine domains with detailed reporting.
"""

import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime

def analyze_fuel_domain(df):
    """Analyze fuel trims and AFR"""
    results = {"issues": [], "summary": {}}
    
    # STFT Analysis
    stft_cols = [c for c in df.columns if 'STFT' in c or 'AF Correction STFT' in c]
    if stft_cols:
        stft = df[stft_cols[0]].dropna()
        results["summary"]["stft"] = {
            "mean": float(stft.mean()),
            "min": float(stft.min()),
            "max": float(stft.max()),
            "std": float(stft.std())
        }
        
        if abs(stft.mean()) > 10:
            results["issues"].append(("CRITICAL", f"STFT mean {stft.mean():.2f}% - Base map significantly off"))
        elif abs(stft.mean()) > 5:
            results["issues"].append(("HIGH", f"STFT mean {stft.mean():.2f}% - Fuel trim outside target"))
        elif abs(stft.mean()) > 3:
            results["issues"].append(("MEDIUM", f"STFT mean {stft.mean():.2f}% - Minor trim correction needed"))
    
    # LTFT Analysis
    ltft_cols = [c for c in df.columns if 'Learn 1' in c or 'Long Term' in c]
    if ltft_cols:
        ltft = df[ltft_cols[0]].dropna()
        results["summary"]["ltft"] = {
            "mean": float(ltft.mean()),
            "min": float(ltft.min()),
            "max": float(ltft.max()),
            "trend": float(ltft.iloc[-100:].mean() - ltft.iloc[:100].mean()) if len(ltft) > 200 else 0
        }
        
        if abs(ltft.mean()) > 15:
            results["issues"].append(("CRITICAL", f"LTFT at {ltft.mean():.2f}% - Check mechanical/sensor issues"))
        elif abs(ltft.mean()) > 10:
            results["issues"].append(("HIGH", f"LTFT at {ltft.mean():.2f}% - Persistent fuel correction"))
        elif abs(ltft.mean()) > 5:
            results["issues"].append(("MEDIUM", f"LTFT at {ltft.mean():.2f}% - Base map needs adjustment"))
    
    # AFR Analysis
    afr_cols = [c for c in df.columns if 'AF Ratio' in c or 'AF Sensor' in c]
    if afr_cols:
        afr = df[afr_cols[0]].dropna()
        results["summary"]["afr"] = {
            "mean": float(afr.mean()),
            "min": float(afr.min()),
            "max": float(afr.max())
        }
        
        if afr.max() > 1.08:
            results["issues"].append(("HIGH", f"Lean AFR detected: max λ={afr.max():.3f}"))
        if afr.min() < 0.92:
            results["issues"].append(("MEDIUM", f"Rich AFR detected: min λ={afr.min():.3f}"))
    
    # MAF-binned fuel trim analysis
    maf_cols = [c for c in df.columns if 'Mass Airflow Corrected' in c]
    if maf_cols and stft_cols:
        maf = df[maf_cols[0]]
        stft = df[stft_cols[0]]
        
        bins = {
            "0-10 g/s (Idle/Light)": (0, 10),
            "10-25 g/s (Cruise)": (10, 25),
            "25-50 g/s (Medium)": (25, 50),
            "50+ g/s (High Load)": (50, 500)
        }
        
        stft_by_load = {}
        for name, (low, high) in bins.items():
            mask = (maf >= low) & (maf < high)
            if mask.sum() > 10:
                stft_by_load[name] = float(stft[mask].mean())
        
        results["summary"]["stft_by_load"] = stft_by_load
        
        if stft_by_load:
            values = list(stft_by_load.values())
            spread = max(values) - min(values)
            if spread > 10:
                results["issues"].append(("HIGH", f"STFT varies {spread:.1f}% across loads - Graduated MAF scaling needed"))
    
    return results

def analyze_ignition_domain(df):
    """Analyze knock and timing"""
    results = {"issues": [], "summary": {}}
    
    # Feedback Knock
    knock_cols = [c for c in df.columns if 'Feedback Knock' in c]
    if knock_cols:
        knock = df[knock_cols[0]].dropna()
        non_zero = knock[knock != 0]
        
        results["summary"]["knock"] = {
            "events": int(len(non_zero)),
            "max_retard": float(knock.min()) if len(knock) > 0 else 0,
            "mean_when_knocking": float(non_zero.mean()) if len(non_zero) > 0 else 0
        }
        
        if len(non_zero) > 0:
            max_retard = abs(knock.min())
            if max_retard > 5:
                results["issues"].append(("CRITICAL", f"Significant knock: {knock.min():.1f}° retard, {len(non_zero)} events"))
            elif max_retard > 2:
                results["issues"].append(("HIGH", f"Moderate knock: {knock.min():.1f}° retard, {len(non_zero)} events"))
            elif len(non_zero) > 20:
                results["issues"].append(("MEDIUM", f"Frequent light knock: {len(non_zero)} events"))
    
    # Fine Knock Learn
    fkl_cols = [c for c in df.columns if 'Fine Knock Learn' in c]
    if fkl_cols:
        fkl = df[fkl_cols[0]].dropna()
        results["summary"]["fine_knock_learn"] = {
            "max": float(fkl.max()),
            "min": float(fkl.min()),
            "mean": float(fkl.mean())
        }
        
        if abs(fkl.max()) > 3 or abs(fkl.min()) > 3:
            results["issues"].append(("HIGH", f"Accumulated knock learn: {fkl.min():.1f}° to {fkl.max():.1f}°"))
    
    # DAM
    dam_cols = [c for c in df.columns if 'Dynamic Advance Multiplier' in c]
    if dam_cols:
        dam = df[dam_cols[0]].dropna()
        results["summary"]["dam"] = {
            "min": float(dam.min()),
            "max": float(dam.max()),
            "mean": float(dam.mean())
        }
        
        if dam.min() < 0.69:
            results["issues"].append(("CRITICAL", f"DAM critically low: {dam.min():.2f}"))
        elif dam.min() < 0.75:
            results["issues"].append(("HIGH", f"DAM low: {dam.min():.2f}"))
        elif dam.min() < 0.90:
            results["issues"].append(("MEDIUM", f"DAM below optimal: {dam.min():.2f} (may be normal post-flash)"))
    
    return results

def analyze_engine_domain(df):
    """Analyze temps, idle, sensors"""
    results = {"issues": [], "summary": {}}
    
    # Coolant temp
    coolant_cols = [c for c in df.columns if 'Coolant' in c]
    if coolant_cols:
        coolant = df[coolant_cols[0]].dropna()
        results["summary"]["coolant"] = {
            "min": float(coolant.min()),
            "max": float(coolant.max()),
            "mean": float(coolant.mean())
        }
        
        if coolant.max() > 110:
            results["issues"].append(("CRITICAL", f"Coolant overheating: max {coolant.max():.0f}°C"))
        elif coolant.max() > 100:
            results["issues"].append(("MEDIUM", f"Coolant warm: max {coolant.max():.0f}°C"))
    
    # Oil temp
    oil_cols = [c for c in df.columns if 'Oil Temp' in c]
    if oil_cols:
        oil = df[oil_cols[0]].dropna()
        results["summary"]["oil_temp"] = {
            "min": float(oil.min()),
            "max": float(oil.max()),
            "mean": float(oil.mean())
        }
        
        if oil.max() > 120:
            results["issues"].append(("HIGH", f"Oil temp high: max {oil.max():.0f}°C"))
    
    # Throttle analysis (operating conditions)
    throttle_cols = [c for c in df.columns if 'Throttle' in c]
    if throttle_cols:
        throttle = df[throttle_cols[0]].dropna()
        results["summary"]["throttle"] = {
            "mean": float(throttle.mean()),
            "max": float(throttle.max()),
            "pct_wot": float((throttle > 80).sum() / len(throttle) * 100) if len(throttle) > 0 else 0,
            "pct_idle": float((throttle < 30).sum() / len(throttle) * 100) if len(throttle) > 0 else 0
        }
    
    # MAF health
    maf_v_cols = [c for c in df.columns if 'Air Flow Sensor Voltage' in c or 'Air Flow Voltage' in c]
    if maf_v_cols:
        maf_v = df[maf_v_cols[0]].dropna()
        results["summary"]["maf_voltage"] = {
            "min": float(maf_v.min()),
            "max": float(maf_v.max()),
            "range": float(maf_v.max() - maf_v.min())
        }
    
    return results

def generate_recommendations(fuel, ignition, engine):
    """Generate actionable recommendations"""
    recs = []
    priority = 1
    
    # Fuel recommendations
    fuel_summary = fuel.get("summary", {})
    if "ltft" in fuel_summary:
        ltft_mean = fuel_summary["ltft"]["mean"]
        if abs(ltft_mean) > 3:
            recs.append({
                "priority": priority,
                "category": "FUEL",
                "action": f"Apply {-ltft_mean:.1f}% MAF scaling correction to reduce LTFT",
                "table": "Sensors - Mass Airflow or MAF VE Correction",
                "details": f"Current LTFT mean: {ltft_mean:+.2f}%"
            })
            priority += 1
    
    if "stft_by_load" in fuel_summary:
        stft_by_load = fuel_summary["stft_by_load"]
        if stft_by_load:
            values = list(stft_by_load.values())
            if max(values) - min(values) > 8:
                recs.append({
                    "priority": priority,
                    "category": "FUEL",
                    "action": "Apply graduated MAF scaling by load range",
                    "table": "Sensors - Mass Airflow",
                    "details": stft_by_load
                })
                priority += 1
    
    # Ignition recommendations
    ign_summary = ignition.get("summary", {})
    if "knock" in ign_summary and ign_summary["knock"]["events"] > 10:
        recs.append({
            "priority": priority,
            "category": "IGNITION",
            "action": "Investigate knock source - check fuel quality, intake temps, timing",
            "details": f"{ign_summary['knock']['events']} knock events, max {ign_summary['knock']['max_retard']:.1f}° retard"
        })
        priority += 1
    
    return recs

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_datalog.py <datalog.csv>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    print(f"Loading {filepath}...")
    df = pd.read_csv(filepath)
    
    print(f"Analyzing {len(df)} samples (~{len(df) * 0.033:.0f} seconds of data)...\n")
    
    # Run domain analyses
    fuel = analyze_fuel_domain(df)
    ignition = analyze_ignition_domain(df)
    engine = analyze_engine_domain(df)
    
    # Generate recommendations
    recommendations = generate_recommendations(fuel, ignition, engine)
    
    # Compile all issues
    all_issues = []
    for domain, name in [(fuel, "FUEL"), (ignition, "IGNITION"), (engine, "ENGINE")]:
        for severity, msg in domain.get("issues", []):
            all_issues.append({"severity": severity, "domain": name, "message": msg})
    
    # Sort by severity
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    all_issues.sort(key=lambda x: priority_order.get(x["severity"], 5))
    
    # Print report
    print("=" * 60)
    print("FA20 DATALOG ANALYSIS REPORT")
    print("=" * 60)
    print(f"File: {filepath.name}")
    print(f"Samples: {len(df)}")
    print(f"Generated: {datetime.now().isoformat()}")
    print()
    
    print("ISSUES BY PRIORITY")
    print("-" * 40)
    for issue in all_issues:
        print(f"[{issue['severity']}] [{issue['domain']}] {issue['message']}")
    
    if not all_issues:
        print("No significant issues detected!")
    
    print()
    print("FUEL TRIM SUMMARY")
    print("-" * 40)
    if "stft" in fuel["summary"]:
        s = fuel["summary"]["stft"]
        print(f"STFT: mean={s['mean']:+.2f}%, min={s['min']:+.2f}%, max={s['max']:+.2f}%")
    if "ltft" in fuel["summary"]:
        s = fuel["summary"]["ltft"]
        print(f"LTFT: mean={s['mean']:+.2f}%, range=[{s['min']:+.2f}% to {s['max']:+.2f}%]")
    if "stft_by_load" in fuel["summary"]:
        print("\nSTFT by Load Range:")
        for load_range, stft in fuel["summary"]["stft_by_load"].items():
            status = "OK" if abs(stft) < 5 else "NEEDS WORK" if abs(stft) < 10 else "CRITICAL"
            print(f"  {load_range}: {stft:+.2f}% [{status}]")
    
    print()
    print("IGNITION SUMMARY")
    print("-" * 40)
    if "dam" in ignition["summary"]:
        d = ignition["summary"]["dam"]
        status = "HEALTHY" if d["min"] >= 0.95 else "WARNING" if d["min"] >= 0.75 else "CRITICAL"
        print(f"DAM: {d['min']:.2f} - {d['max']:.2f} [{status}]")
    if "knock" in ignition["summary"]:
        k = ignition["summary"]["knock"]
        print(f"Knock Events: {k['events']}, Max Retard: {k['max_retard']:.1f}°")
    if "fine_knock_learn" in ignition["summary"]:
        f = ignition["summary"]["fine_knock_learn"]
        print(f"Fine Knock Learn: {f['min']:.1f}° to {f['max']:.1f}°")
    
    print()
    print("ENGINE/TEMPS")
    print("-" * 40)
    if "coolant" in engine["summary"]:
        c = engine["summary"]["coolant"]
        print(f"Coolant: {c['min']:.0f}°C - {c['max']:.0f}°C")
    if "oil_temp" in engine["summary"]:
        o = engine["summary"]["oil_temp"]
        print(f"Oil: {o['min']:.0f}°C - {o['max']:.0f}°C")
    if "throttle" in engine["summary"]:
        t = engine["summary"]["throttle"]
        print(f"Throttle: {t['pct_idle']:.0f}% idle, {t['pct_wot']:.0f}% WOT")
    
    if recommendations:
        print()
        print("RECOMMENDATIONS")
        print("-" * 40)
        for rec in recommendations:
            print(f"{rec['priority']}. [{rec['category']}] {rec['action']}")
            if "table" in rec:
                print(f"   Table: {rec['table']}")
    
    # Build JSON report
    report = {
        "metadata": {
            "file": str(filepath),
            "samples": len(df),
            "timestamp": datetime.now().isoformat()
        },
        "issues": all_issues,
        "domains": {
            "fuel": fuel,
            "ignition": ignition,
            "engine": engine
        },
        "recommendations": recommendations
    }
    
    # Save JSON
    output_path = filepath.parent / f"{filepath.stem}_analysis.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report saved to: {output_path}")
    
    return report

if __name__ == "__main__":
    main()
