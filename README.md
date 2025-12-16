# Atlas ECU Table Documentation

Comprehensive table-by-table documentation for the Atlas ECU tuning software.

## Structure

```
atlas-docs/
├── tables/              # Markdown source files organized by category
│   ├── avcs/            # AVCS - Variable valve timing control
│   ├── airflow/         # Airflow - MAF/airflow calculations
│   ├── analytical/      # Analytical - Diagnostic/analysis tables
│   ├── engine/          # Engine - Core engine parameters
│   ├── fuel/            # Fuel - Fuel injection/delivery
│   ├── ignition/        # Ignition - Spark timing tables
│   ├── patches/         # Patches - ROM patches/modifications
│   ├── pids/            # PIDs - OBD-II Parameter IDs
│   ├── sensors/         # Sensors - Sensor scaling/calibration
│   ├── throttle/        # Throttle - Electronic throttle control
│   ├── transmission/    # Transmission - Gearbox tables
│   └── vdc/             # VDC - Vehicle Dynamics Control
├── templates/           # Documentation templates
├── scripts/             # Conversion utilities
├── screenshots/         # Source screenshots from Atlas
└── output/              # Generated documentation
    ├── html/            # HTML format
    └── json/            # JSON format (machine-readable)
```


### Converting to HTML/JSON

```bash
# Convert all tables
python scripts/convert.py

# Convert specific category
python scripts/convert.py tables/ignition

# Convert single file
python scripts/convert.py tables/ignition/primary-tgvs-closed.md
```

### Viewing Documentation

After conversion, open `output/html/index.html` in a browser.

## Table Documentation Format

Each table document includes:

- **Overview**: Category, platform, data type, ROM address
- **Description**: What the table does
- **Axes**: X and Y axis parameters, units, ranges
- **Cell Values**: Units, data type, valid ranges
- **Functional Behavior**: How the ECU uses this table
- **Related Tables**: Tables that interact with this one
- **Related Parameters**: Datalog parameters to monitor
- **Tuning Notes**: Practical tuning guidance
- **Warnings**: Safety considerations

## Platform

Currently documenting: **VA WRX (2015-2021)** with FA20DIT engine

## Contributing

When documenting a table:

1. Verify the table name matches Atlas exactly
2. Include accurate axis information
3. Document safe operating ranges
4. Note any table dependencies
5. Add relevant datalog parameters
