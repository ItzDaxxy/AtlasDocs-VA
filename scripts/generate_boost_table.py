#!/usr/bin/env python3
"""
FA20 Boost Control Table Generator
Generates revised boost control tables for any target PSI.

Usage:
    python generate_boost_table.py --target 21 --current 23.6
    python generate_boost_table.py --target 19 --reduction 2
    python generate_boost_table.py --help

This script generates:
- Boost Target Main (reduced to hit target actual boost)
- Boost Limit Base (safety ceiling)
- Wastegate Duty Maximum (reduced to give PI headroom)
- Wastegate Duty Initial (reduced to prevent spool overshoot)
- PI Integral Negative (softened to reduce spool aggression)
"""

import argparse
import csv
from pathlib import Path
from datetime import datetime

PSI_TO_BAR = 0.0689476
BAR_TO_PSI = 14.5038

# Default export directory - can be overridden with --export-dir
DEFAULT_EXPORT_DIR = Path.home() / "Atlas Projects" / "Export"


def load_atlas_table(filepath):
    """Parse Atlas CSV into header, data rows, and metadata."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    data_lines = []
    metadata_start = len(lines)
    
    for i, line in enumerate(lines):
        stripped = line.strip().strip('"').strip(',')
        if stripped == '' or stripped.startswith('Series'):
            metadata_start = i
            break
        data_lines.append(line)
    
    # Parse header (X-axis values)
    header = [p.strip('"') for p in data_lines[0].strip().rstrip(',').split(',')]
    
    # Parse data rows
    rows = []
    for line in data_lines[1:]:
        parts = line.strip().rstrip(',').split(',')
        row = [p.strip('"') for p in parts]
        rows.append(row)
    
    # Get metadata
    metadata = lines[metadata_start:] if metadata_start < len(lines) else []
    
    return header, rows, metadata


def write_atlas_table(filepath, header, rows, table_name, unit, x_axis, x_unit, y_axis=None, y_unit=None):
    """Write complete Atlas-format CSV."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        
        # Header row
        writer.writerow(header)
        
        # Data rows
        for row in rows:
            writer.writerow(row)
        
        # Empty row + metadata
        f.write('"",\n')
        f.write('"Series","Name","Unit",\n')
        f.write(f'"Table","{table_name}","{unit}",\n')
        f.write(f'"X Axis","{x_axis}","{x_unit}",\n')
        if y_axis:
            f.write(f'"Y Axis","{y_axis}","{y_unit}",\n')


def print_table(header, rows, title, y_label="RPM", max_rows=15):
    """Print formatted table preview."""
    print(f"\n{title}")
    print("=" * 140)
    
    # Print header
    print(f"{y_label:<12}", end='')
    for h in header[1:]:
        if h:
            try:
                print(f"{float(h):>8.0f}", end='')
            except:
                print(f"{h:>8}", end='')
    print()
    print("-" * 140)
    
    # Print rows
    for row in rows[:max_rows]:
        try:
            print(f"{float(row[0]):<12.0f}", end='')
        except:
            print(f"{row[0]:<12}", end='')
        for val in row[1:]:
            if val:
                try:
                    print(f"{float(val):>8.4f}", end='')
                except:
                    print(f"{val:>8}", end='')
        print()
    
    if len(rows) > max_rows:
        print(f"... ({len(rows) - max_rows} more rows)")


def generate_boost_target_main(export_dir, boost_reduction_psi, target_psi):
    """Generate revised Boost Target Main with reduction."""
    print("\n" + "=" * 80)
    print(f"  BOOST TARGET MAIN - Reducing by {boost_reduction_psi} psi")
    print("=" * 80)
    
    # Find input file
    input_path = export_dir / "Airflow - Turbo - Boost - Boost Target Main - 2017 - NEWDGM.csv"
    if not input_path.exists():
        # Try alternate naming
        candidates = list(export_dir.glob("*Boost Target Main*.csv"))
        if candidates:
            input_path = candidates[0]
        else:
            print(f"ERROR: Cannot find Boost Target Main table in {export_dir}")
            return None
    
    header, rows, _ = load_atlas_table(input_path)
    
    reduction_bar = boost_reduction_psi * PSI_TO_BAR
    
    # Find original max
    orig_max = 0
    for row in rows:
        for val in row[1:]:
            if val:
                try:
                    v = float(val)
                    if v > orig_max:
                        orig_max = v
                except:
                    pass
    
    # Apply reduction to positive values only - store both BAR and PSI
    revised_rows_bar = []
    revised_rows_psi = []
    new_max = 0
    for row in rows:
        new_row_bar = [row[0]]
        new_row_psi = []
        for val in row[1:]:
            if val:
                try:
                    v = float(val)
                    if v > 0:
                        v = max(0, v - reduction_bar)
                    if v > new_max:
                        new_max = v
                    new_row_bar.append(f"{v:.4f}")
                    # Convert to PSI for paste
                    v_psi = v * BAR_TO_PSI
                    new_row_psi.append(f"{v_psi:.2f}")
                except:
                    new_row_bar.append(val)
                    new_row_psi.append(val)
            else:
                new_row_bar.append(val)
                new_row_psi.append("")
        revised_rows_bar.append(new_row_bar)
        revised_rows_psi.append(new_row_psi)
    
    # Save CSV in BAR format
    output_path = export_dir / f"REVISED - Boost Target Main - {target_psi}psi.csv"
    write_atlas_table(
        output_path, header, revised_rows_bar,
        "Airflow - Turbo - Boost - Boost Target Main", "BAR",
        "Boost Control - Boost Targets/Limits - Requested Torque", "NM",
        "Boost Control - Wastegate - RPM", "RPM"
    )
    
    # Save PSI format for paste
    output_path_psi = export_dir / f"Boost_Target_Main_{target_psi}psi_for_paste.txt"
    with open(output_path_psi, 'w') as f:
        for row in revised_rows_psi:
            f.write("\t".join(row) + "\n")
    
    print(f"\nOriginal max: {orig_max:.4f} bar = {orig_max * BAR_TO_PSI:.1f} psi target")
    print(f"Revised max:  {new_max:.4f} bar = {new_max * BAR_TO_PSI:.1f} psi target")
    print(f"Reduction:    {reduction_bar:.4f} bar = {boost_reduction_psi:.1f} psi")
    
    # Print PSI values for paste (first 10 rows)
    print("\nPSI VALUES (for Atlas paste):")
    print(f"{'RPM':<12}", end='')
    for h in header[1:]:
        if h:
            try:
                print(f"{float(h):>8.0f}", end='')
            except:
                print(f"{h:>8}", end='')
    print()
    print("-" * 140)
    for i, row in enumerate(revised_rows_psi[:10]):
        rpm = revised_rows_bar[i][0]
        print(f"{float(rpm):<12.0f}", end='')
        for val in row:
            if val:
                print(f"{float(val):>8.2f}", end='')
        print()
    if len(revised_rows_psi) > 10:
        print(f"... ({len(revised_rows_psi) - 10} more rows)")
    
    print(f"\n✓ Saved CSV (BAR): {output_path}")
    print(f"✓ Saved PSI (for paste): {output_path_psi}")
    
    return new_max


def generate_boost_limit_base(export_dir, new_target_max, target_psi):
    """Generate revised Boost Limit Base as safety ceiling."""
    print("\n" + "=" * 80)
    print("  BOOST LIMIT BASE - Safety ceiling")
    print("=" * 80)
    
    input_path = export_dir / "Airflow - Turbo - Boost - Boost Limit Base - 2017 - NEWDGM.csv"
    if not input_path.exists():
        candidates = list(export_dir.glob("*Boost Limit Base*.csv"))
        if candidates:
            input_path = candidates[0]
        else:
            print(f"WARNING: Cannot find Boost Limit Base table, skipping")
            return
    
    header, rows, _ = load_atlas_table(input_path)
    
    # Limit should be ~0.15 bar above max target for PI headroom
    target_limit = new_target_max + 0.15
    
    # Cap values at target_limit for mid-high RPM
    revised_row_bar = [rows[0][0]]
    revised_row_psi = []
    for i, val in enumerate(rows[0][1:]):
        if val:
            try:
                v = float(val)
                rpm = float(header[i + 1])
                if rpm >= 2000 and v > target_limit:
                    v = target_limit
                revised_row_bar.append(f"{v:.4f}")
                revised_row_psi.append(f"{v * BAR_TO_PSI:.2f}")
            except:
                revised_row_bar.append(val)
                revised_row_psi.append(val)
        else:
            revised_row_bar.append(val)
            revised_row_psi.append("")
    
    revised_rows_bar = [revised_row_bar]
    
    output_path = export_dir / f"REVISED - Boost Limit Base - {target_psi}psi.csv"
    write_atlas_table(
        output_path, header, revised_rows_bar,
        "Airflow - Turbo - Boost - Boost Limit Base", "BAR",
        "Boost Control - Wastegate - RPM", "RPM"
    )
    
    output_path_psi = export_dir / f"Boost_Limit_Base_{target_psi}psi_for_paste.txt"
    with open(output_path_psi, 'w') as f:
        f.write("\t".join(revised_row_psi) + "\n")
    
    print(f"\nTarget limit: {target_limit:.4f} bar = {target_limit * BAR_TO_PSI:.1f} psi")
    
    print(f"\n✓ Saved CSV (BAR): {output_path}")
    print(f"✓ Saved PSI (for paste): {output_path_psi}")


def generate_wastegate_duty_maximum(export_dir, wgdc_reduction, target_psi):
    """Generate revised Wastegate Duty Maximum with reduction."""
    print("\n" + "=" * 80)
    print(f"  WASTEGATE DUTY MAXIMUM - Reducing by {wgdc_reduction}%")
    print("=" * 80)
    
    input_path = export_dir / "Airflow - Turbo - Wastegate - Wastegate Duty Maximum - 2017 - NEWDGM.csv"
    if not input_path.exists():
        candidates = list(export_dir.glob("*Wastegate Duty Maximum*.csv"))
        if candidates:
            input_path = candidates[0]
        else:
            print(f"WARNING: Cannot find Wastegate Duty Maximum table, skipping")
            return
    
    header, rows, _ = load_atlas_table(input_path)
    
    revised_rows = []
    for row in rows:
        new_row = [row[0]]
        for val in row[1:]:
            if val:
                try:
                    v = float(val)
                    if v > 30:
                        v = max(10, v - wgdc_reduction)
                    new_row.append(f"{v:.4f}")
                except:
                    new_row.append(val)
            else:
                new_row.append(val)
        revised_rows.append(new_row)
    
    output_path = export_dir / f"REVISED - Wastegate Duty Maximum - {target_psi}psi.csv"
    write_atlas_table(
        output_path, header, revised_rows,
        "Airflow - Turbo - Wastegate - Wastegate Duty Maximum", "PERCENT",
        "Boost Control - Requested Torque", "NM",
        "RPM", "RPM"
    )
    
    print(f"\nReduced all cells >30% by {wgdc_reduction}%")
    print_table(header, revised_rows, "REVISED WASTEGATE DUTY MAXIMUM (%)")
    print(f"\n✓ Saved: {output_path}")


def generate_wastegate_duty_initial(export_dir, wgdc_reduction, target_psi):
    """Generate revised Wastegate Duty Initial."""
    print("\n" + "=" * 80)
    print(f"  WASTEGATE DUTY INITIAL - Reducing by {wgdc_reduction}%")
    print("=" * 80)
    
    input_path = export_dir / "Airflow - Turbo - Wastegate - Wastegate Duty Initial - 2017 - NEWDGM.csv"
    if not input_path.exists():
        candidates = list(export_dir.glob("*Wastegate Duty Initial*.csv"))
        if candidates:
            input_path = candidates[0]
        else:
            print(f"WARNING: Cannot find Wastegate Duty Initial table, skipping")
            return
    
    header, rows, _ = load_atlas_table(input_path)
    
    revised_rows = []
    for row in rows:
        new_row = [row[0]]
        for val in row[1:]:
            if val:
                try:
                    v = float(val)
                    if v > 20:
                        v = max(0, v - wgdc_reduction)
                    new_row.append(f"{v:.4f}")
                except:
                    new_row.append(val)
            else:
                new_row.append(val)
        revised_rows.append(new_row)
    
    output_path = export_dir / f"REVISED - Wastegate Duty Initial - {target_psi}psi.csv"
    write_atlas_table(
        output_path, header, revised_rows,
        "Airflow - Turbo - Wastegate - Wastegate Duty Initial", "PERCENT",
        "REQ TORQUE", "NM",
        "RPM", "RPM"
    )
    
    print(f"\nReduced all cells >20% by {wgdc_reduction}%")
    print_table(header, revised_rows, "REVISED WASTEGATE DUTY INITIAL (%)")
    print(f"\n✓ Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='FA20 Boost Control Table Generator',
        epilog='Example: python generate_boost_table.py --target 21 --current 23.6'
    )
    parser.add_argument('--target', type=float, required=True,
                        help='Target actual boost in PSI (e.g., 21)')
    parser.add_argument('--current', type=float, default=None,
                        help='Current actual boost in PSI (e.g., 23.6). Used to calculate reduction.')
    parser.add_argument('--reduction', type=float, default=None,
                        help='Direct boost reduction in PSI (alternative to --current)')
    parser.add_argument('--wgdc-reduction', type=float, default=8.0,
                        help='Wastegate duty cycle reduction percent (default: 8)')
    parser.add_argument('--export-dir', type=str, default=None,
                        help=f'Atlas export directory (default: {DEFAULT_EXPORT_DIR})')
    parser.add_argument('--boost-only', action='store_true',
                        help='Only generate Boost Target Main, skip wastegate tables')
    
    args = parser.parse_args()
    
    # Determine export directory
    export_dir = Path(args.export_dir) if args.export_dir else DEFAULT_EXPORT_DIR
    if not export_dir.exists():
        print(f"ERROR: Export directory does not exist: {export_dir}")
        print("Please specify --export-dir or ensure Atlas export folder exists.")
        return 1
    
    # Calculate boost reduction
    if args.reduction is not None:
        boost_reduction = args.reduction
    elif args.current is not None:
        boost_reduction = args.current - args.target
    else:
        print("ERROR: Must specify either --current or --reduction")
        return 1
    
    if boost_reduction <= 0:
        print(f"WARNING: Boost reduction is {boost_reduction} psi (no reduction needed?)")
    
    target_psi = int(args.target)
    
    print("\n")
    print("=" * 80)
    print(f"  FA20 BOOST CONTROL TABLE GENERATOR")
    print(f"  Target: {target_psi} psi max actual boost")
    print("=" * 80)
    print(f"\nExport directory: {export_dir}")
    print(f"\nParameters:")
    print(f"  Target boost:     {args.target} psi")
    if args.current:
        print(f"  Current boost:    {args.current} psi")
    print(f"  Boost reduction:  {boost_reduction:.1f} psi")
    print(f"  WGDC reduction:   {args.wgdc_reduction}%")
    
    # Generate tables
    new_boost_max = generate_boost_target_main(export_dir, boost_reduction, target_psi)
    
    if new_boost_max is None:
        return 1
    
    generate_boost_limit_base(export_dir, new_boost_max, target_psi)
    
    if not args.boost_only:
        generate_wastegate_duty_maximum(export_dir, args.wgdc_reduction, target_psi)
        generate_wastegate_duty_initial(export_dir, args.wgdc_reduction, target_psi)
    
    print("\n")
    print("=" * 80)
    print("  GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nFiles saved to: {export_dir}")
    print(f"\nNEXT STEPS:")
    print(f"  1. Import revised tables into Atlas")
    print(f"  2. Flash to ECU")
    print(f"  3. Perform WOT pulls and log")
    print(f"  4. Verify max boost ≤ {target_psi} psi, DAM = 1.00, no knock")
    print(f"  5. If still overshooting, run again with larger reduction")
    print("\n")
    
    return 0


if __name__ == "__main__":
    exit(main())
