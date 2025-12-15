# FA20 Tuning History & Analysis Tracking

Comprehensive historical records of all tuning activities, datalog analyses, and ECU configuration changes.

## Structure

```
tuning-history/
├── README.md                    # This file
├── analysis-log.json            # Master log of all datalog analyses
├── ecu-config-history.json      # Historical record of ECU table/parameter changes
├── analyses/                    # Individual analysis reports (timestamped)
└── configurations/              # ECU configuration snapshots
```

## Analysis Log

Each entry in `analysis-log.json` tracks:
- Datalog filename and timestamp
- Critical findings (fuel trims, knock, DAM, AFR)
- Recommended changes with priority
- Status: pending / applied / rejected

## ECU Config History

Each change in `ecu-config-history.json` documents:
- Table/parameter modified
- Previous → New values
- Reason for change (linked to analysis)
- Verification status

## Safety Protocol

1. Document baseline before any modifications
2. Cross-reference changes with datalog evidence
3. Track DAM, knock, and fuel trim trends over time
4. Never apply changes without understanding the modset context
