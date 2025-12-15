#!/usr/bin/env python3
"""
Atlas ECU Documentation Converter
Converts Markdown table documentation to JSON and HTML formats.

Usage:
    python convert.py                    # Convert all tables
    python convert.py tables/ignition    # Convert specific category
    python convert.py tables/ignition/primary-tgvs-closed.md  # Single file
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Try to import markdown library, provide fallback
try:
    import markdown
    from markdown.extensions.tables import TableExtension
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Note: 'markdown' library not installed. HTML output will be basic.")
    print("Install with: pip install markdown")


def parse_markdown_table(md_content: str) -> dict:
    """Parse a markdown table documentation file into structured data."""
    data = {
        "name": "",
        "category": "",
        "platform": "",
        "table_type": "",
        "data_type": "",
        "address": "",
        "description": "",
        "x_axis": {},
        "y_axis": {},
        "cell_values": {},
        "functional_behavior": "",
        "related_tables": [],
        "related_parameters": [],
        "tuning_notes": "",
        "warnings": "",
        "last_updated": ""
    }

    lines = md_content.split('\n')
    current_section = None
    current_subsection = None
    buffer = []

    # Extract title
    for line in lines:
        if line.startswith('# ') and not line.startswith('## '):
            data["name"] = line[2:].strip()
            break

    # Parse sections
    for i, line in enumerate(lines):
        # Main sections
        if line.startswith('## '):
            # Save previous section
            if current_section and buffer:
                save_section(data, current_section, current_subsection, buffer)
            current_section = line[3:].strip().lower()
            current_subsection = None
            buffer = []
        # Subsections
        elif line.startswith('### '):
            if current_section and buffer:
                save_section(data, current_section, current_subsection, buffer)
            current_subsection = line[4:].strip().lower()
            buffer = []
        else:
            buffer.append(line)

    # Save last section
    if current_section and buffer:
        save_section(data, current_section, current_subsection, buffer)

    return data


def save_section(data: dict, section: str, subsection: str, buffer: list):
    """Save parsed section content to data dict."""
    content = '\n'.join(buffer).strip()

    if section == "overview":
        # Parse overview table
        for match in re.finditer(r'\*\*([^*]+)\*\*\s*\|\s*([^\n|]+)', content):
            key = match.group(1).strip().lower().replace(' ', '_')
            value = match.group(2).strip()
            if key in data:
                data[key] = value

    elif section == "description":
        data["description"] = content

    elif section == "axes":
        axis_data = parse_property_table(content)
        if subsection == "x-axis":
            data["x_axis"] = axis_data
        elif subsection == "y-axis":
            data["y_axis"] = axis_data

    elif section == "cell values":
        data["cell_values"] = parse_property_table(content)

    elif section == "functional behavior":
        data["functional_behavior"] = content

    elif section == "related tables":
        # Extract markdown links
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
            data["related_tables"].append({
                "name": match.group(1),
                "link": match.group(2)
            })

    elif section == "related parameters (datalog)":
        # Parse parameter table
        for match in re.finditer(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', content):
            name = match.group(1).strip()
            desc = match.group(2).strip()
            if name and not name.startswith('-') and name != "Parameter Name":
                data["related_parameters"].append({
                    "name": name,
                    "description": desc
                })

    elif section == "tuning notes":
        data["tuning_notes"] = content

    elif section == "warnings":
        data["warnings"] = content


def parse_property_table(content: str) -> dict:
    """Parse a property/value markdown table."""
    result = {}
    for match in re.finditer(r'\*\*([^*]+)\*\*\s*\|\s*([^\n|]+)', content):
        key = match.group(1).strip().lower().replace(' ', '_')
        value = match.group(2).strip()
        result[key] = value
    return result


def to_json(data: dict) -> str:
    """Convert parsed data to JSON."""
    return json.dumps(data, indent=2)


def to_html(md_content: str, data: dict) -> str:
    """Convert markdown to HTML."""
    if HAS_MARKDOWN:
        html_body = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
    else:
        # Basic fallback - just wrap in pre tags
        html_body = f"<pre>{md_content}</pre>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Atlas Table Documentation')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ color: #1a1a2e; border-bottom: 2px solid #4a4e69; padding-bottom: 10px; }}
        h2 {{ color: #4a4e69; margin-top: 30px; }}
        h3 {{ color: #666; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #4a4e69;
            color: white;
        }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        a {{ color: #4a4e69; }}
        a:hover {{ color: #1a1a2e; }}
    </style>
</head>
<body>
    <nav><a href="../index.html">&larr; Back to Index</a></nav>
    {html_body}
</body>
</html>"""
    return html


def process_file(md_path: Path, output_dir: Path):
    """Process a single markdown file."""
    print(f"Processing: {md_path}")

    with open(md_path, 'r') as f:
        md_content = f.read()

    data = parse_markdown_table(md_content)

    # Generate output filename from input
    stem = md_path.stem
    category = md_path.parent.name

    # JSON output
    json_dir = output_dir / 'json' / category
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir / f"{stem}.json"
    with open(json_path, 'w') as f:
        f.write(to_json(data))
    print(f"  -> {json_path}")

    # HTML output
    html_dir = output_dir / 'html' / category
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"{stem}.html"
    with open(html_path, 'w') as f:
        f.write(to_html(md_content, data))
    print(f"  -> {html_path}")


def generate_index(tables_dir: Path, output_dir: Path):
    """Generate index files for the documentation."""
    all_tables = []

    for md_file in tables_dir.rglob('*.md'):
        if md_file.name.startswith('_'):
            continue
        with open(md_file, 'r') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else md_file.stem

        category = md_file.parent.name
        all_tables.append({
            "name": title,
            "category": category,
            "file": str(md_file.relative_to(tables_dir)),
            "html_path": f"{category}/{md_file.stem}.html",
            "json_path": f"{category}/{md_file.stem}.json"
        })

    # Sort by category then name
    all_tables.sort(key=lambda x: (x['category'], x['name']))

    # Generate JSON index
    index_json = output_dir / 'json' / 'index.json'
    with open(index_json, 'w') as f:
        json.dump({"tables": all_tables, "generated": datetime.now().isoformat()}, f, indent=2)

    # Generate HTML index
    categories = {}
    for table in all_tables:
        cat = table['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(table)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atlas ECU Table Documentation - VA WRX</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #1a1a2e; }
        h2 { color: #4a4e69; margin-top: 30px; text-transform: capitalize; }
        ul { list-style-type: none; padding-left: 0; }
        li { padding: 8px 0; border-bottom: 1px solid #eee; }
        a { color: #4a4e69; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .category-count { color: #888; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Atlas ECU Table Documentation</h1>
    <p><strong>Platform:</strong> VA WRX (2015-2021) / FA20DIT</p>
    <p><strong>Generated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """</p>
"""

    for cat, tables in sorted(categories.items()):
        html_content += f"\n    <h2>{cat} <span class='category-count'>({len(tables)} tables)</span></h2>\n    <ul>\n"
        for table in tables:
            html_content += f'        <li><a href="{table["html_path"]}">{table["name"]}</a></li>\n'
        html_content += "    </ul>\n"

    html_content += "</body>\n</html>"

    index_html = output_dir / 'html' / 'index.html'
    with open(index_html, 'w') as f:
        f.write(html_content)

    print(f"\nGenerated index files:")
    print(f"  -> {index_json}")
    print(f"  -> {index_html}")


def main():
    base_dir = Path(__file__).parent.parent
    tables_dir = base_dir / 'tables'
    output_dir = base_dir / 'output'

    # Determine what to process
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if not target.is_absolute():
            target = base_dir / target

        if target.is_file() and target.suffix == '.md':
            process_file(target, output_dir)
        elif target.is_dir():
            for md_file in target.rglob('*.md'):
                process_file(md_file, output_dir)
        else:
            print(f"Error: {target} not found or not a .md file/directory")
            sys.exit(1)
    else:
        # Process all
        md_files = list(tables_dir.rglob('*.md'))
        if not md_files:
            print("No markdown files found in tables/ directory.")
            print("Create table documentation files and run again.")
        else:
            for md_file in md_files:
                process_file(md_file, output_dir)

    # Always regenerate index
    generate_index(tables_dir, output_dir)


if __name__ == '__main__':
    main()
