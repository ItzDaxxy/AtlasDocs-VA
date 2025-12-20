#!/usr/bin/env python3
"""
FA20 DIT Comprehensive Datalog Analysis Script
Generates detailed tuning reports with pandas-formatted tables.

Usage:
    python analyze_datalog.py --wot wot.csv --cruise cruise.csv
    python analyze_datalog.py datalog.csv
    python analyze_datalog.py --config vehicle_config.yaml --wot wot.csv --cruise cruise.csv
"""

import pandas as pd
import numpy as np
import argparse
import sys
import yaml
from pathlib import Path
from datetime import datetime

pd.set_option('display.width', 120)
pd.set_option('display.max_columns', 20)

# Default thresholds (overridden by vehicle_config.yaml if provided)
DEFAULT_CONFIG = {
    'vehicle': {
        'year': 'Unknown',
        'model': 'WRX',
        'engine': 'FA20DIT'
    },
    'targets': {
        'peak_boost_psi': 18,
        'redline_rpm': 6500
    },
    'safety_margins': {
        'timing_margin_degrees': 2,
        'wot_afr_target': 10.8,
        'boost_margin_psi': 1,
        'dam_minimum': 1.00,
        'max_knock_retard': 0
    },
    'thresholds': {
        'stft_warning': 5,
        'stft_critical': 10,
        'ltft_warning': 5,
        'ltft_critical': 10,
        'dam_warning': 0.95,
        'dam_critical': 0.75,
        'fbk_warning': -1,
        'fbk_critical': -3,
        'fkl_warning': -1,
        'fkl_critical': -2
    }
}


def load_config(config_path=None):
    """Load vehicle configuration from YAML file or use defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            # Deep merge user config into defaults
            for key in user_config:
                if key in config and isinstance(config[key], dict):
                    config[key].update(user_config[key])
                else:
                    config[key] = user_config[key]
        print(f"Loaded config from: {config_path}")
    else:
        # Try to find vehicle_config.yaml in common locations
        search_paths = [
            Path.cwd() / 'vehicle_config.yaml',
            Path.cwd().parent / 'vehicle_config.yaml',
        ]
        for path in search_paths:
            if path.exists():
                with open(path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    for key in user_config:
                        if key in config and isinstance(config[key], dict):
                            config[key].update(user_config[key])
                        else:
                            config[key] = user_config[key]
                print(f"Auto-detected config: {path}")
                break
    
    return config


def load_datalog(filepath):
    """Load and prepare a datalog CSV."""
    df = pd.read_csv(filepath)
    
    numeric_cols = [
        'Engine - RPM',
        'Fuel - Command - Corrections - AF Correction STFT',
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)',
        'Ignition - Dynamic Advance Multiplier',
        'Ignition - Feedback Knock',
        'Ignition - Fine Knock Learn',
        'Analytical - Boost Pressure',
        'Sensors - AF Ratio 1',
        'PIDs - (F410) Mass Air Flow',
        'Engine - Calculated Load',
        'Throttle - Requested Torque - Main Accelerator Position',
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)',
        'Airflow - Turbo - Boost - Manifold Absolute Pressure',
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded',
        'PIDs - (F405) Coolant Temperature',
        'PIDs - (F45C) Oil Temperature'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def generate_executive_summary(df, config):
    """Generate executive summary table using config thresholds."""
    thresholds = config['thresholds']
    
    dam_min = df['Ignition - Dynamic Advance Multiplier'].min()
    fbk_min = df['Ignition - Feedback Knock'].min()
    fkl_min = df['Ignition - Fine Knock Learn'].min()
    ltft_mean = df['Fuel - Command - Corrections - AF Learn 1 (LTFT)'].mean()
    
    dam_status = '✅ Perfect' if dam_min >= thresholds['dam_warning'] else \
                 ('⚠️ Warning' if dam_min >= thresholds['dam_critical'] else '❌ Critical')
    fbk_status = '✅ No knock' if fbk_min >= thresholds['fbk_warning'] else \
                 ('⚠️ Minor' if fbk_min >= thresholds['fbk_critical'] else '❌ Knock')
    fkl_status = '✅ Clean' if fkl_min >= thresholds['fkl_warning'] else \
                 ('⚠️ Learning' if fkl_min >= thresholds['fkl_critical'] else '❌ Retard')
    ltft_status = '✅ OK' if abs(ltft_mean) < thresholds['ltft_warning'] else \
                  ('⚠️ High' if abs(ltft_mean) < thresholds['ltft_critical'] else '❌ Critical')
    
    summary = pd.DataFrame({
        'Parameter': ['DAM', 'Feedback Knock', 'Fine Knock Learn', 'LTFT'],
        'Value': [f'{dam_min:.2f}', f'{fbk_min:.2f}°', f'{fkl_min:.2f}°', f'{ltft_mean:+.2f}%'],
        'Threshold': ['≥0.95', '0°', '0°', '±5%'],
        'Status': [dam_status, fbk_status, fkl_status, ltft_status]
    })
    
    return summary


def generate_stft_histogram(df):
    """Generate STFT distribution histogram."""
    stft = df['Fuel - Command - Corrections - AF Correction STFT'].dropna()
    bins = [-25, -10, -5, -3, 0, 3, 5, 10, 20]
    labels = ['< -10%', '-10 to -5%', '-5 to -3%', '-3 to 0%', 
              '0 to +3%', '+3 to +5%', '+5 to +10%', '> +10%']
    
    stft_cut = pd.cut(stft, bins=bins, labels=labels)
    stft_df = stft_cut.value_counts().sort_index().reset_index()
    stft_df.columns = ['Range', 'Count']
    stft_df['Pct'] = (stft_df['Count'] / stft_df['Count'].sum() * 100).round(1)
    stft_df['Histogram'] = stft_df['Count'].apply(lambda x: '█' * min(int(x/35), 50))
    
    return stft_df


def generate_maf_analysis(df):
    """Generate fuel trim analysis by MAF range."""
    maf_bins = [(0,10), (10,20), (20,30), (30,40), (40,50), 
                (50,75), (75,100), (100,150), (150,200)]
    maf_data = []
    
    for lo, hi in maf_bins:
        mask = (df['PIDs - (F410) Mass Air Flow'] >= lo) & \
               (df['PIDs - (F410) Mass Air Flow'] < hi)
        subset = df[mask]
        
        if len(subset) >= 5:
            stft_avg = subset['Fuel - Command - Corrections - AF Correction STFT'].mean()
            ltft_avg = subset['Fuel - Command - Corrections - AF Learn 1 (LTFT)'].mean()
            combined = stft_avg + ltft_avg
            status = '✅ OK' if abs(combined) < 3 else \
                     ('⚠️ Minor' if abs(combined) < 5 else '❌ Fix')
            maf_data.append({
                'MAF Range': f'{lo}-{hi} g/s',
                'STFT': f'{stft_avg:+.2f}%',
                'LTFT': f'{ltft_avg:+.2f}%',
                'Combined': f'{combined:+.2f}%',
                'Status': status,
                'Samples': len(subset)
            })
    
    return pd.DataFrame(maf_data)


def generate_boost_analysis(df_wot):
    """Generate boost distribution and WOT performance analysis."""
    boost = df_wot[df_wot['Analytical - Boost Pressure'] > 0]['Analytical - Boost Pressure']
    
    if len(boost) == 0:
        return None, None
    
    bins = [0, 5, 10, 15, 18, 20, 22, 24, 30]
    labels = ['0-5 psi', '5-10 psi', '10-15 psi', '15-18 psi', 
              '18-20 psi', '20-22 psi', '22-24 psi', '>24 psi']
    
    boost_cut = pd.cut(boost, bins=bins, labels=labels)
    boost_df = boost_cut.value_counts().sort_index().reset_index()
    boost_df.columns = ['Range', 'Count']
    boost_df['Histogram'] = boost_df['Count'].apply(lambda x: '█' * min(int(x/2), 40))
    
    # WOT performance
    wot_mask = df_wot['Throttle - Requested Torque - Main Accelerator Position'] > 80
    wot_df = df_wot[wot_mask]
    
    if len(wot_df) > 0:
        overshoot = wot_df['Airflow - Turbo - Boost - Manifold Absolute Pressure'] - \
                    wot_df['Airflow - Turbo - Boost - Boost Target Final (Absolute)']
        
        wot_stats = pd.DataFrame({
            'Metric': ['Peak Boost', 'Target (MAP absolute)', 'WGDC Range', 
                      'Avg Overshoot', 'Max Overshoot'],
            'Value': [
                f"{wot_df['Analytical - Boost Pressure'].max():.1f} psi",
                f"{wot_df['Airflow - Turbo - Boost - Boost Target Final (Absolute)'].max():.1f} psi",
                f"{wot_df['Airflow - Turbo - Wastegate - Duty Cycle Commanded'].min():.0f}% - {wot_df['Airflow - Turbo - Wastegate - Duty Cycle Commanded'].max():.0f}%",
                f"{overshoot.mean():+.2f} psi",
                f"{overshoot.max():+.2f} psi"
            ]
        })
    else:
        wot_stats = None
    
    return boost_df, wot_stats


def generate_pe_analysis(df_wot):
    """Generate power enrichment analysis by RPM."""
    high_load = df_wot[df_wot['Engine - Calculated Load'] > 0.8]
    
    if len(high_load) == 0:
        return None
    
    rpm_bins = [(2000,3000), (3000,3500), (3500,4000), 
                (4000,4500), (4500,5000), (5000,5500)]
    pe_data = []
    
    for lo, hi in rpm_bins:
        mask = (high_load['Engine - RPM'] >= lo) & (high_load['Engine - RPM'] < hi)
        subset = high_load[mask]
        
        if len(subset) > 0:
            lam = subset['Sensors - AF Ratio 1'].mean()
            afr = lam * 14.7
            stft = subset['Fuel - Command - Corrections - AF Correction STFT'].mean()
            status = '✅ OK' if abs(stft) < 3 else \
                     ('⚠️ Monitor' if abs(stft) < 7 else '❌ Lean')
            pe_data.append({
                'RPM': f'{lo}-{hi}',
                'Lambda': f'{lam:.3f}',
                'AFR': f'{afr:.1f}:1',
                'STFT': f'{stft:+.1f}%',
                'Status': status
            })
    
    return pd.DataFrame(pe_data)


def generate_knock_reference():
    """Generate knock threshold reference table."""
    return pd.DataFrame({
        'Parameter': ['DAM', 'Feedback Knock', 'Fine Knock Learn', 'STFT/LTFT'],
        'Green': ['≥ 0.95', '0°', '0°', '±5%'],
        'Yellow': ['0.75-0.95', '-1° to -3°', '-1° to -2°', '±5-10%'],
        'Red': ['< 0.75', '< -3°', '< -2°', '> ±10%']
    })


def generate_action_items(df, df_wot):
    """Generate prioritized action items."""
    items = []
    
    dam_min = df['Ignition - Dynamic Advance Multiplier'].min()
    fbk_min = df['Ignition - Feedback Knock'].min()
    
    items.append({'Priority': '1', 'Category': 'Safety', 
                  'Item': f'DAM at {dam_min:.2f}', 
                  'Status': '✅ Complete' if dam_min >= 0.95 else '⚠️ Monitor'})
    items.append({'Priority': '1', 'Category': 'Safety', 
                  'Item': f'FBK at {fbk_min:.2f}°', 
                  'Status': '✅ Complete' if fbk_min >= -1 else '⚠️ Investigate'})
    
    # Check boost overshoot
    wot_mask = df_wot['Throttle - Requested Torque - Main Accelerator Position'] > 80
    wot_df = df_wot[wot_mask]
    if len(wot_df) > 0:
        overshoot = (wot_df['Airflow - Turbo - Boost - Manifold Absolute Pressure'] - \
                    wot_df['Airflow - Turbo - Boost - Boost Target Final (Absolute)']).mean()
        if overshoot > 2:
            items.append({'Priority': '2', 'Category': 'Boost', 
                         'Item': 'Reduce Boost Target Main (overshoot detected)', 
                         'Status': '☐ Pending'})
    
    # Check high RPM STFT
    high_load = df_wot[df_wot['Engine - Calculated Load'] > 0.8]
    if len(high_load) > 0:
        high_rpm = high_load[high_load['Engine - RPM'] > 4000]
        if len(high_rpm) > 0:
            stft_high = high_rpm['Fuel - Command - Corrections - AF Correction STFT'].mean()
            if stft_high > 5:
                items.append({'Priority': '3', 'Category': 'Fuel', 
                             'Item': 'Enrich PE Target at 4000+ RPM', 
                             'Status': '☐ Pending'})
    
    items.append({'Priority': '4', 'Category': 'Validation', 
                  'Item': 'New datalogs after changes', 
                  'Status': '☐ Pending'})
    
    return pd.DataFrame(items)


def generate_report(df_all, df_wot, output_path, config):
    """Generate the full analysis report."""
    
    vehicle = config.get('vehicle', {})
    mods = config.get('mods', {})
    safety = config.get('safety_margins', {})
    
    report = f'''
================================================================================
                    FA20 DIT DATALOG ANALYSIS REPORT
                         Generated by Amp AI Tuning
                           {datetime.now().strftime('%Y-%m-%d %H:%M')}
================================================================================

Vehicle:   {vehicle.get('year', '')} Subaru {vehicle.get('model', 'WRX')} ({vehicle.get('engine', 'FA20DIT')})
Software:  Atlas
Samples:   {len(df_all)} total
'''
    
    # Add mod list if available
    if mods:
        report += f'''
Mods:      Turbo: {mods.get('turbo', 'stock')} | IC: {mods.get('intercooler', 'stock')} | DP: {mods.get('downpipe', 'stock')}
'''
    
    # Add safety margins from config
    if safety:
        report += f'''
Safety:    Timing margin: {safety.get('timing_margin_degrees', 2)}° | AFR target: {safety.get('wot_afr_target', 10.8)}:1 | Boost margin: +{safety.get('boost_margin_psi', 1)} psi
'''
    
    report += '''
================================================================================
                              EXECUTIVE SUMMARY
================================================================================
'''
    
    summary = generate_executive_summary(df_all, config)
    report += summary.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                           FUEL TRIM ANALYSIS
================================================================================

STFT Distribution (Short Term Fuel Trim):
'''
    
    stft_hist = generate_stft_histogram(df_all)
    report += stft_hist.to_string(index=False) + '\n'
    
    report += '''
Fuel Trim by MAF Airflow (g/s):
'''
    
    maf_df = generate_maf_analysis(df_all)
    report += maf_df.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                          BOOST CONTROL ANALYSIS
================================================================================

Boost Pressure Distribution (positive boost only):
'''
    
    boost_df, wot_stats = generate_boost_analysis(df_wot)
    if boost_df is not None:
        report += boost_df.to_string(index=False) + '\n'
    
    if wot_stats is not None:
        report += '\nWOT Performance Summary:\n'
        report += wot_stats.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                      POWER ENRICHMENT (WOT FUELING)
================================================================================

AFR by RPM under WOT (Load > 80%):
'''
    
    pe_df = generate_pe_analysis(df_wot)
    if pe_df is not None:
        report += pe_df.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                         MATH & CALCULATIONS
================================================================================

FUEL TRIM FORMULAS:
  Actual Fuel = Commanded × (1 + STFT/100) × (1 + LTFT/100)
  MAF Correction = -1 × Combined Trim (but preserve 2-3% rich bias)

POWER ENRICHMENT (φ):
  φ > 1.0 = Rich    |    AFR = 14.7 / φ
  New φ = Current φ × (1 + STFT/100)

BOOST CONVERSION:
  1 psi = 0.0689476 bar
  1 bar = 14.5038 psi

KNOCK THRESHOLD REFERENCE:
'''
    
    knock_ref = generate_knock_reference()
    report += knock_ref.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                           ACTION ITEMS
================================================================================
'''
    
    actions = generate_action_items(df_all, df_wot)
    report += actions.to_string(index=False) + '\n'
    
    report += '''
================================================================================
                              END OF REPORT
                         Generated by Amp AI Tuning
                              For Atlas Software
================================================================================
'''
    
    # Write report
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(report)
    print(f"\nReport saved to: {output_path}")
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='FA20 DIT Datalog Analysis - Built for VA WRX (2015-2021)',
        epilog='Defaults based on stock FA20DIT calibration. Use --config for custom thresholds.'
    )
    parser.add_argument('datalog', nargs='?', help='Single datalog CSV file')
    parser.add_argument('--wot', help='WOT datalog CSV file')
    parser.add_argument('--cruise', help='Cruise datalog CSV file')
    parser.add_argument('--config', '-c', help='Path to vehicle_config.yaml')
    parser.add_argument('-o', '--output', help='Output report path')
    
    args = parser.parse_args()
    
    # Load configuration (will auto-detect vehicle_config.yaml if present)
    config = load_config(args.config)
    
    vehicle = config.get('vehicle', {})
    print(f"\n{'='*60}")
    print(f"  FA20 DIT Datalog Analyzer - VA WRX (2015-2021)")
    print(f"  Vehicle: {vehicle.get('year', '')} {vehicle.get('model', 'WRX')}")
    print(f"  Baseline: Stock FA20DIT calibration (18 psi)")
    print(f"{'='*60}\n")
    
    # Determine input files
    if args.wot and args.cruise:
        print(f"Loading WOT log: {args.wot}")
        df_wot = load_datalog(args.wot)
        print(f"Loading cruise log: {args.cruise}")
        df_cruise = load_datalog(args.cruise)
        df_all = pd.concat([df_wot, df_cruise], ignore_index=True)
        base_path = Path(args.wot).parent
    elif args.datalog:
        print(f"Loading datalog: {args.datalog}")
        df_all = load_datalog(args.datalog)
        df_wot = df_all
        base_path = Path(args.datalog).parent
    else:
        parser.print_help()
        sys.exit(1)
    
    print(f"Total samples: {len(df_all)}")
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = base_path / 'FA20_Tuning_Report.txt'
    
    # Generate report with config
    generate_report(df_all, df_wot, output_path, config)


if __name__ == "__main__":
    main()
