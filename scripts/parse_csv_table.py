#!/usr/bin/env python3
"""
Atlas CSV Table Parser
Parses CSV exports from Atlas and generates markdown documentation.

Usage:
    python parse_csv_table.py <csv_file> [output_md_file]
"""

import csv
import sys
import os
import re
from pathlib import Path


def parse_atlas_csv(csv_path):
    """
    Parse an Atlas CSV export and extract table metadata.

    Returns dict with:
    - table_name: str
    - category: str (inferred from path or content)
    - axes: dict with x_axis and y_axis info
    - data: 2D array of values
    - metadata: any header comments or metadata
    """

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract metadata from comments (lines starting with #)
    metadata = []
    data_start = 0

    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            metadata.append(line.strip('# \n'))
        else:
            data_start = i
            break

    # Parse CSV data
    csv_reader = csv.reader(lines[data_start:])
    rows = list(csv_reader)

    if not rows:
        return None

    # Detect structure:
    # Typical Atlas CSV format:
    # Row 0: [empty], X-axis values...
    # Row 1+: Y-axis value, data cells...

    header_row = rows[0]
    data_rows = rows[1:]

    # Extract X-axis (first row, skip first cell)
    x_axis_values = [cell.strip() for cell in header_row[1:] if cell.strip()]

    # Extract Y-axis (first column, skip first cell) and data
    y_axis_values = []
    data_grid = []

    for row in data_rows:
        if not row:
            continue
        y_axis_values.append(row[0].strip())
        data_grid.append([cell.strip() for cell in row[1:]])

    # Infer table name from filename
    table_name = Path(csv_path).stem.replace('_', ' ').replace('-', ' ').title()

    # Try to detect category from filename or path
    csv_path_obj = Path(csv_path)
    category = "Unknown"

    # Check if file is in a category subdirectory
    for cat in ['ignition', 'fuel', 'airflow', 'engine', 'avcs', 'throttle',
                'sensors', 'transmission', 'vdc', 'analytical', 'patches', 'pids']:
        if cat in str(csv_path_obj).lower():
            category = cat.title()
            break

    return {
        'table_name': table_name,
        'category': category,
        'filename': csv_path_obj.name,
        'metadata': metadata,
        'x_axis': {
            'values': x_axis_values,
            'label': infer_axis_label(x_axis_values, 'x'),
            'unit': infer_axis_unit(x_axis_values)
        },
        'y_axis': {
            'values': y_axis_values,
            'label': infer_axis_label(y_axis_values, 'y'),
            'unit': infer_axis_unit(y_axis_values)
        },
        'data': data_grid,
        'dimensions': f"{len(y_axis_values)}x{len(x_axis_values)}"
    }


def infer_axis_label(values, axis_type):
    """Infer axis label from values (e.g., RPM, Load, etc.)"""
    if not values:
        return f"{axis_type.upper()}-Axis"

    # Check if values look like RPM (numbers in 1000s)
    try:
        first_val = float(values[0])
        last_val = float(values[-1])

        if 500 <= first_val <= 8000 and last_val > first_val:
            return "Engine Speed (RPM)"
        elif 0 <= first_val <= 500 and last_val > first_val:
            return "Engine Load"
        elif -40 <= first_val <= 150:
            return "Temperature"
    except (ValueError, IndexError):
        pass

    return f"{axis_type.upper()}-Axis"


def infer_axis_unit(values):
    """Infer axis unit from values"""
    if not values:
        return ""

    try:
        first_val = float(values[0])
        last_val = float(values[-1])

        if 500 <= first_val <= 8000:
            return "RPM"
        elif 0 <= first_val <= 500 and last_val > 20:
            return "Load (calculated)"
        elif -40 <= first_val <= 150:
            return "°C"
    except (ValueError, IndexError):
        pass

    return ""


def infer_data_unit(data_grid):
    """Infer data unit from cell values"""
    if not data_grid or not data_grid[0]:
        return ""

    try:
        # Sample some values
        sample_values = [float(data_grid[0][0]),
                        float(data_grid[-1][0]) if len(data_grid) > 1 else float(data_grid[0][-1])]

        avg = sum(sample_values) / len(sample_values)

        # Timing values (degrees BTDC)
        if -20 <= avg <= 50:
            return "degrees BTDC"
        # Fuel values (often 0-100 or multipliers)
        elif 0 <= avg <= 2:
            return "multiplier"
        # AFR lambda
        elif 0.5 <= avg <= 1.5:
            return "lambda"
    except (ValueError, IndexError, TypeError):
        pass

    return ""


def generate_markdown(table_info, output_path=None):
    """Generate markdown documentation from parsed table info"""

    md_lines = [
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
        f"- **Parameter**: {table_info['x_axis']['label']}",
        f"- **Unit**: {table_info['x_axis']['unit'] or 'TBD'}",
        f"- **Range**: {table_info['x_axis']['values'][0]} to {table_info['x_axis']['values'][-1]}",
        f"- **Points**: {len(table_info['x_axis']['values'])}",
        "",
        "### Y-Axis",
        "",
        f"- **Parameter**: {table_info['y_axis']['label']}",
        f"- **Unit**: {table_info['y_axis']['unit'] or 'TBD'}",
        f"- **Range**: {table_info['y_axis']['values'][0]} to {table_info['y_axis']['values'][-1]}",
        f"- **Points**: {len(table_info['y_axis']['values'])}",
        "",
        "## Cell Values",
        "",
        f"- **Unit**: {infer_data_unit(table_info['data']) or 'TBD'}",
        "- **Data Type**: TBD",
        "- **Typical Range**: TBD",
        "",
        "## Data Sample",
        "",
        "```",
    ]

    # Add a small sample of the data (first 5x5 cells)
    sample_rows = min(5, len(table_info['data']))
    sample_cols = min(5, len(table_info['data'][0])) if table_info['data'] else 0

    # Header
    md_lines.append(f"{'':>10} " + " ".join(f"{val:>10}" for val in table_info['x_axis']['values'][:sample_cols]))

    # Data rows
    for i in range(sample_rows):
        row_label = table_info['y_axis']['values'][i]
        row_data = table_info['data'][i][:sample_cols]
        md_lines.append(f"{row_label:>10} " + " ".join(f"{val:>10}" for val in row_data))

    md_lines.extend([
        "...",
        "```",
        "",
        "*(Full data exported from Atlas)*",
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
        "*Add practical tuning guidance.*",
        "",
        "## Warnings",
        "",
        "*Add safety considerations.*",
        ""
    ])

    markdown_content = '\n'.join(md_lines)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✓ Generated: {output_path}")

    return markdown_content


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_csv_table.py <csv_file> [output_md_file]")
        print("\nExample:")
        print("  python parse_csv_table.py screenshots/ignition-primary.csv tables/ignition/primary.md")
        sys.exit(1)

    csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    # Parse CSV
    print(f"Parsing: {csv_path}")
    table_info = parse_atlas_csv(csv_path)

    if not table_info:
        print("Error: Could not parse CSV file")
        sys.exit(1)

    print(f"  Table: {table_info['table_name']}")
    print(f"  Category: {table_info['category']}")
    print(f"  Dimensions: {table_info['dimensions']}")
    print(f"  X-Axis: {table_info['x_axis']['label']} ({len(table_info['x_axis']['values'])} points)")
    print(f"  Y-Axis: {table_info['y_axis']['label']} ({len(table_info['y_axis']['values'])} points)")

    # Determine output path
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # Auto-generate output path
        csv_filename = Path(csv_path).stem
        category = table_info['category'].lower()
        output_path = f"tables/{category}/{csv_filename}.md"

        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate markdown
    generate_markdown(table_info, output_path)
    print(f"\n✓ Documentation generated successfully!")
    print(f"\nNext steps:")
    print(f"1. Review and edit: {output_path}")
    print(f"2. Fill in TBD sections")
    print(f"3. Run: python scripts/convert.py")


if __name__ == '__main__':
    main()
