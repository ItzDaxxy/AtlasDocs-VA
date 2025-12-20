#!/usr/bin/env python3
"""
Atlas CSV Table Parser
Parses CSV exports from Atlas software and generates markdown documentation.

Atlas CSV Format:
- Row 1: X-axis values (empty first cell)
- Rows 2-N: Y-axis value in first column, data in remaining columns
- Footer: Metadata rows with Series, Name, Unit information

Usage:
    python parse_atlas_csv.py <csv_file> [output_md_file]
    python parse_atlas_csv.py tables/avcs/  # Process directory
"""

import csv
import sys
import os
import re
from pathlib import Path


def parse_atlas_csv(csv_path):
    """
    Parse an Atlas CSV export and extract table metadata.

    Returns dict with table information or None if parsing fails.
    """

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return None

    # Find metadata at bottom of file
    metadata = {}
    data_end_row = len(rows)

    for i in range(len(rows) - 1, -1, -1):
        row = rows[i]
        if len(row) >= 2 and row[0] in ['Table', 'X Axis', 'Y Axis', 'Series']:
            if row[0] == 'Table':
                metadata['table_name'] = row[1]
                metadata['table_unit'] = row[2] if len(row) > 2 else ''
                data_end_row = min(data_end_row, i - 1)
            elif row[0] == 'X Axis':
                metadata['x_axis_name'] = row[1]
                metadata['x_axis_unit'] = row[2] if len(row) > 2 else ''
            elif row[0] == 'Y Axis':
                metadata['y_axis_name'] = row[1]
                metadata['y_axis_unit'] = row[2] if len(row) > 2 else ''

    # Check if this is a scalar (single value) table
    is_scalar = 'x_axis_name' not in metadata and 'y_axis_name' not in metadata

    if is_scalar:
        # Scalar table - just one value
        scalar_value = rows[1][1] if len(rows) > 1 and len(rows[1]) > 1 else None
        return {
            'type': 'scalar',
            'table_name': metadata.get('table_name', 'Unknown'),
            'value': scalar_value,
            'unit': metadata.get('table_unit', ''),
            'filename': Path(csv_path).name,
            'category': infer_category(csv_path)
        }

    # 2D/3D table
    # Row 0: X-axis values (skip first cell)
    x_axis_values = [cell.strip() for cell in rows[0][1:] if cell.strip()]

    # Find where empty rows start (data end)
    for i in range(1, data_end_row):
        if not rows[i] or not rows[i][0].strip():
            data_end_row = i
            break

    # Extract Y-axis values and data grid
    y_axis_values = []
    data_grid = []

    for i in range(1, data_end_row):
        row = rows[i]
        if not row or not row[0].strip():
            break
        y_axis_values.append(row[0].strip())
        data_grid.append([cell.strip() for cell in row[1:len(x_axis_values)+1]])

    return {
        'type': '3d',
        'table_name': metadata.get('table_name', Path(csv_path).stem),
        'category': infer_category(csv_path),
        'filename': Path(csv_path).name,
        'table_unit': metadata.get('table_unit', ''),
        'x_axis': {
            'name': metadata.get('x_axis_name', 'X-Axis'),
            'unit': metadata.get('x_axis_unit', ''),
            'values': x_axis_values
        },
        'y_axis': {
            'name': metadata.get('y_axis_name', 'Y-Axis'),
            'unit': metadata.get('y_axis_unit', ''),
            'values': y_axis_values
        },
        'data': data_grid,
        'dimensions': f"{len(y_axis_values)}x{len(x_axis_values)}"
    }


def infer_category(file_path):
    """Infer category from file path"""
    path_str = str(file_path).lower()
    categories = {
        'avcs': 'AVCS',
        'ignition': 'Ignition',
        'fuel': 'Fuel',
        'airflow': 'Airflow',
        'engine': 'Engine',
        'throttle': 'Throttle',
        'sensors': 'Sensors',
        'transmission': 'Transmission',
        'vdc': 'VDC',
        'analytical': 'Analytical',
        'patches': 'Patches',
        'pids': 'PIDs'
    }

    for key, value in categories.items():
        if key in path_str:
            return value
    return 'Unknown'


def generate_markdown_scalar(table_info):
    """Generate markdown for scalar (single value) table"""

    lines = [
        f"# {table_info['table_name']}",
        "",
        "## Overview",
        "",
        "| Property | Value |",
        "|----------|-------|",
        f"| **Category** | {table_info['category']} |",
        "| **Platform** | VA WRX (2015-2021) |",
        "| **Table Type** | Scalar (Single Value) |",
        f"| **Unit** | {table_info['unit']} |",
        f"| **Source File** | `{table_info['filename']}` |",
        "",
        "## Value",
        "",
        f"**{table_info['value']} {table_info['unit']}**",
        "",
        "## Description",
        "",
        "*Add description of what this parameter controls.*",
        "",
        "## Related Tables",
        "",
        "- TBD",
        "",
        "## Related Datalog Parameters",
        "",
        "- TBD",
        "",
        "## Tuning Notes",
        "",
        "*Add tuning guidance.*",
        ""
    ]

    return '\n'.join(lines)


def generate_markdown_3d(table_info):
    """Generate markdown for 3D table"""

    lines = [
        f"# {table_info['table_name']}",
        "",
        "## Overview",
        "",
        "| Property | Value |",
        "|----------|-------|",
        f"| **Category** | {table_info['category']} |",
        "| **Platform** | VA WRX (2015-2021) |",
        "| **Table Type** | 3D Map |",
        f"| **Dimensions** | {table_info['dimensions']} |",
        f"| **Data Unit** | {table_info['table_unit']} |",
        f"| **Source File** | `{table_info['filename']}` |",
        "",
        "## Description",
        "",
        "*Add description of what this table controls and when it's used.*",
        "",
        "## Axes",
        "",
        "### X-Axis",
        "",
        f"- **Parameter**: {table_info['x_axis']['name']}",
        f"- **Unit**: {table_info['x_axis']['unit']}",
    ]

    if table_info['x_axis']['values']:
        lines.extend([
            f"- **Range**: {table_info['x_axis']['values'][0]} to {table_info['x_axis']['values'][-1]}",
            f"- **Points**: {len(table_info['x_axis']['values'])}"
        ])

    lines.extend([
        "",
        "### Y-Axis",
        "",
        f"- **Parameter**: {table_info['y_axis']['name']}",
        f"- **Unit**: {table_info['y_axis']['unit']}",
    ])

    if table_info['y_axis']['values']:
        lines.extend([
            f"- **Range**: {table_info['y_axis']['values'][0]} to {table_info['y_axis']['values'][-1]}",
            f"- **Points**: {len(table_info['y_axis']['values'])}"
        ])

    lines.extend([
        "",
        "## Cell Values",
        "",
        f"- **Unit**: {table_info['table_unit']}",
        "- **Data Type**: Float",
        "",
        "## Data Preview",
        "",
        "First 8x8 corner of the table:",
        "",
        "```",
    ])

    # Add data preview (first 8x8)
    sample_rows = min(8, len(table_info['data']))
    sample_cols = min(8, len(table_info['x_axis']['values']))

    # Header with X values
    header = f"{'RPM':>10} |"
    for i in range(sample_cols):
        header += f" {table_info['x_axis']['values'][i]:>10} |"
    lines.append(header)
    lines.append("-" * len(header))

    # Data rows
    for i in range(sample_rows):
        row_label = table_info['y_axis']['values'][i]
        row_data = table_info['data'][i][:sample_cols]
        row_str = f"{row_label:>10} |"
        for val in row_data:
            row_str += f" {val:>10} |"
        lines.append(row_str)

    lines.extend([
        "```",
        "",
        "## Functional Behavior",
        "",
        "*Add description of how the ECU interpolates and uses this table.*",
        "",
        "## Related Tables",
        "",
        "- TBD",
        "",
        "## Related Datalog Parameters",
        "",
        "- TBD",
        "",
        "## Tuning Notes",
        "",
        "*Add practical tuning guidance and typical modification patterns.*",
        "",
        "## Warnings",
        "",
        "*Add safety considerations and potential risks.*",
        ""
    ])

    return '\n'.join(lines)


def generate_markdown(table_info, output_path=None):
    """Generate markdown documentation from parsed table info"""

    if table_info['type'] == 'scalar':
        markdown = generate_markdown_scalar(table_info)
    else:
        markdown = generate_markdown_3d(table_info)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"  ✓ Generated: {output_path}")

    return markdown


def process_csv_file(csv_path, output_dir=None):
    """Process a single CSV file"""

    print(f"\nProcessing: {csv_path}")

    try:
        table_info = parse_atlas_csv(csv_path)

        if not table_info:
            print(f"  ✗ Failed to parse")
            return False

        print(f"  Table: {table_info['table_name']}")
        print(f"  Type: {table_info['type'].upper()}")
        print(f"  Category: {table_info['category']}")

        if table_info['type'] == '3d':
            print(f"  Dimensions: {table_info['dimensions']}")

        # Determine output path
        if output_dir:
            # Create sanitized filename
            safe_name = re.sub(r'[^\w\s-]', '', table_info['table_name'])
            safe_name = re.sub(r'[-\s]+', '-', safe_name).strip('-').lower()
            output_path = os.path.join(output_dir, f"{safe_name}.md")
        else:
            # Auto-generate based on category
            csv_path_obj = Path(csv_path)
            safe_name = re.sub(r'[^\w\s-]', '', table_info['table_name'])
            safe_name = re.sub(r'[-\s]+', '-', safe_name).strip('-').lower()

            category = table_info['category'].lower()
            output_path = f"tables/{category}/{safe_name}.md"

        generate_markdown(table_info, output_path)
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def process_directory(dir_path):
    """Process all CSV files in a directory recursively"""

    csv_files = list(Path(dir_path).rglob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {dir_path}")
        return

    print(f"\nFound {len(csv_files)} CSV files")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for csv_file in csv_files:
        if process_csv_file(csv_file):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Successfully processed: {success_count}")
    if fail_count > 0:
        print(f"✗ Failed: {fail_count}")
    print(f"\nNext steps:")
    print(f"1. Review generated markdown files")
    print(f"2. Fill in descriptions and tuning notes")
    print(f"3. Run: python scripts/convert.py")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python parse_atlas_csv.py <csv_file|directory> [output_file]")
        print("\nExamples:")
        print("  python parse_atlas_csv.py tables/avcs/intake.csv")
        print("  python parse_atlas_csv.py tables/avcs/  # Process entire directory")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print(f"Error: Path not found: {input_path}")
        sys.exit(1)

    if os.path.isdir(input_path):
        process_directory(input_path)
    else:
        output_path = sys.argv[2] if len(sys.argv) >= 3 else None
        if process_csv_file(input_path, output_path):
            print(f"\n✓ Documentation generated successfully!")
        else:
            print(f"\n✗ Failed to generate documentation")
            sys.exit(1)


if __name__ == '__main__':
    main()
