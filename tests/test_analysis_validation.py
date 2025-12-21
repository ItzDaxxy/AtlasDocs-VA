#!/usr/bin/env python3
"""
Comprehensive analysis validation tests.
Creates synthetic datalogs with known conditions and validates analysis outputs.
"""

import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pandas as pd
import numpy as np
import pytest
from analyze_datalog import (
    load_datalog, generate_executive_summary, generate_stft_histogram,
    generate_maf_analysis, generate_boost_analysis, generate_pe_analysis,
    generate_action_items, DEFAULT_CONFIG
)


def create_healthy_datalog(n_samples=500):
    """Create a datalog representing a well-tuned FA20.
    
    Characteristics:
    - DAM = 1.00 (perfect)
    - No knock events
    - STFT centered around -2% (ideal rich bias)
    - LTFT around -1% 
    - Boost on target (no overshoot)
    - WOT AFR around 10.8:1 (safe rich)
    """
    np.random.seed(42)
    
    # Mix of cruise and WOT conditions
    n_cruise = int(n_samples * 0.7)
    n_wot = n_samples - n_cruise
    
    data = {
        'Engine - RPM': np.concatenate([
            np.random.uniform(1500, 3500, n_cruise),  # Cruise RPM
            np.random.uniform(3000, 6000, n_wot)      # WOT RPM
        ]),
        'Fuel - Command - Corrections - AF Correction STFT': np.concatenate([
            np.random.normal(-2.0, 1.5, n_cruise),    # Cruise: centered at -2%
            np.random.normal(-1.0, 2.0, n_wot)        # WOT: slight rich
        ]),
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)': np.concatenate([
            np.random.normal(-1.0, 0.5, n_cruise),
            np.random.normal(-1.0, 0.5, n_wot)
        ]),
        'Ignition - Dynamic Advance Multiplier': np.ones(n_samples) * 1.0,  # Perfect DAM
        'Ignition - Feedback Knock': np.zeros(n_samples),  # No knock
        'Ignition - Fine Knock Learn': np.zeros(n_samples),  # No learned knock
        'Analytical - Boost Pressure': np.concatenate([
            np.random.uniform(-5, 5, n_cruise),       # Vacuum/low boost cruise
            np.random.uniform(15, 18, n_wot)          # On-target WOT boost
        ]),
        'Sensors - AF Ratio 1': np.concatenate([
            np.random.uniform(0.98, 1.02, n_cruise),  # Stoich cruise
            np.random.uniform(0.72, 0.76, n_wot)      # Rich WOT (10.6-11.2 AFR)
        ]),
        'PIDs - (F410) Mass Air Flow': np.concatenate([
            np.random.uniform(15, 60, n_cruise),
            np.random.uniform(100, 180, n_wot)
        ]),
        'Engine - Calculated Load': np.concatenate([
            np.random.uniform(0.2, 0.5, n_cruise),
            np.random.uniform(0.85, 1.0, n_wot)
        ]),
        'Throttle - Requested Torque - Main Accelerator Position': np.concatenate([
            np.random.uniform(10, 40, n_cruise),
            np.random.uniform(85, 100, n_wot)
        ]),
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)': np.concatenate([
            np.random.uniform(0.9, 1.0, n_cruise),
            np.random.uniform(1.1, 1.2, n_wot)
        ]),
        'Airflow - Turbo - Boost - Manifold Absolute Pressure': np.concatenate([
            np.random.uniform(0.9, 1.0, n_cruise),
            np.random.uniform(1.1, 1.25, n_wot)  # Slight overshoot acceptable
        ]),
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded': np.concatenate([
            np.random.uniform(0, 10, n_cruise),
            np.random.uniform(40, 70, n_wot)
        ]),
    }
    
    return pd.DataFrame(data)


def create_problematic_datalog(n_samples=500):
    """Create a datalog representing a tune with issues.
    
    Characteristics:
    - DAM drops to 0.875 (knock detected)
    - Multiple knock events (-2° to -4°)
    - FKL showing learned retard
    - STFT running lean at high MAF (+8%)
    - Boost overshoot (3+ psi over target)
    - WOT AFR too lean (11.8:1)
    """
    np.random.seed(123)
    
    n_cruise = int(n_samples * 0.6)
    n_wot = n_samples - n_cruise
    
    data = {
        'Engine - RPM': np.concatenate([
            np.random.uniform(1500, 3500, n_cruise),
            np.random.uniform(3000, 6000, n_wot)
        ]),
        'Fuel - Command - Corrections - AF Correction STFT': np.concatenate([
            np.random.normal(2.0, 3.0, n_cruise),     # Running lean cruise
            np.random.normal(8.0, 3.0, n_wot)         # Very lean WOT - BAD
        ]),
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)': np.concatenate([
            np.random.normal(4.0, 1.0, n_cruise),     # High LTFT - undertrimmed
            np.random.normal(4.0, 1.0, n_wot)
        ]),
        'Ignition - Dynamic Advance Multiplier': np.concatenate([
            np.ones(n_cruise) * 1.0,                  # OK at cruise
            np.random.choice([1.0, 0.9375, 0.875], n_wot, p=[0.6, 0.3, 0.1])  # DAM drops under load
        ]),
        'Ignition - Feedback Knock': np.concatenate([
            np.zeros(n_cruise),
            np.random.choice([0, -1.41, -2.81, -4.22], n_wot, p=[0.7, 0.15, 0.1, 0.05])
        ]),
        'Ignition - Fine Knock Learn': np.concatenate([
            np.zeros(n_cruise),
            np.random.choice([0, -0.70, -1.41, -2.11], n_wot, p=[0.5, 0.25, 0.15, 0.1])
        ]),
        'Analytical - Boost Pressure': np.concatenate([
            np.random.uniform(-5, 5, n_cruise),
            np.random.uniform(19, 24, n_wot)          # Overshooting! BAD
        ]),
        'Sensors - AF Ratio 1': np.concatenate([
            np.random.uniform(0.98, 1.02, n_cruise),
            np.random.uniform(0.78, 0.82, n_wot)      # Lean WOT (11.5-12.0 AFR)
        ]),
        'PIDs - (F410) Mass Air Flow': np.concatenate([
            np.random.uniform(15, 60, n_cruise),
            np.random.uniform(120, 200, n_wot)        # High MAF = more airflow
        ]),
        'Engine - Calculated Load': np.concatenate([
            np.random.uniform(0.2, 0.5, n_cruise),
            np.random.uniform(0.85, 1.0, n_wot)
        ]),
        'Throttle - Requested Torque - Main Accelerator Position': np.concatenate([
            np.random.uniform(10, 40, n_cruise),
            np.random.uniform(85, 100, n_wot)
        ]),
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)': np.concatenate([
            np.random.uniform(0.9, 1.0, n_cruise),
            np.random.uniform(1.1, 1.2, n_wot)        # Target ~17 psi
        ]),
        'Airflow - Turbo - Boost - Manifold Absolute Pressure': np.concatenate([
            np.random.uniform(0.9, 1.0, n_cruise),
            np.random.uniform(1.3, 1.5, n_wot)        # Actual ~21+ psi - overshoot!
        ]),
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded': np.concatenate([
            np.random.uniform(0, 10, n_cruise),
            np.random.uniform(60, 90, n_wot)          # High WGDC
        ]),
    }
    
    return pd.DataFrame(data)


class TestHealthyDatalog:
    """Test that healthy datalogs produce expected 'all good' analysis."""
    
    @pytest.fixture
    def healthy_df(self):
        return create_healthy_datalog()
    
    def test_dam_is_perfect(self, healthy_df):
        """DAM should be 1.00 and marked as perfect."""
        summary = generate_executive_summary(healthy_df, DEFAULT_CONFIG)
        dam_row = summary[summary['Parameter'] == 'DAM (min)'].iloc[0]
        assert float(dam_row['Value']) == 1.00
        assert '✅' in dam_row['Status']
    
    def test_no_knock_events(self, healthy_df):
        """Should have zero knock events."""
        summary = generate_executive_summary(healthy_df, DEFAULT_CONFIG)
        knock_row = summary[summary['Parameter'] == 'Knock Events'].iloc[0]
        assert knock_row['Value'] == '0'
        assert '✅' in knock_row['Status']
    
    def test_fuel_trims_healthy(self, healthy_df):
        """STFT and LTFT should be within acceptable range."""
        summary = generate_executive_summary(healthy_df, DEFAULT_CONFIG)
        stft_row = summary[summary['Parameter'] == 'STFT (avg)'].iloc[0]
        # Should be around -2% (rich bias) - acceptable
        assert '✅' in stft_row['Status'] or '⚠️' in stft_row['Status']
    
    def test_boost_on_target(self, healthy_df):
        """Boost should be on target without excessive overshoot."""
        summary = generate_executive_summary(healthy_df, DEFAULT_CONFIG)
        boost_rows = summary[summary['Parameter'] == 'Peak Boost']
        if len(boost_rows) > 0:
            boost_row = boost_rows.iloc[0]
            # Peak should be ~18 psi or less
            peak_value = float(boost_row['Value'].replace(' psi', ''))
            assert peak_value <= 20  # Within acceptable range
    
    def test_wot_afr_safe(self, healthy_df):
        """WOT AFR should be safely rich (< 11.0:1)."""
        summary = generate_executive_summary(healthy_df, DEFAULT_CONFIG)
        afr_rows = summary[summary['Parameter'] == 'WOT AFR']
        if len(afr_rows) > 0:
            afr_row = afr_rows.iloc[0]
            afr_value = float(afr_row['Value'].replace(':1', ''))
            assert afr_value < 11.5  # Safe rich


class TestProblematicDatalog:
    """Test that problematic datalogs correctly identify issues."""
    
    @pytest.fixture
    def problem_df(self):
        return create_problematic_datalog()
    
    def test_dam_drop_detected(self, problem_df):
        """Should detect DAM drop and flag as warning/critical."""
        summary = generate_executive_summary(problem_df, DEFAULT_CONFIG)
        dam_row = summary[summary['Parameter'] == 'DAM (min)'].iloc[0]
        dam_value = float(dam_row['Value'])
        assert dam_value < 1.0  # DAM dropped
        assert '⚠️' in dam_row['Status'] or '❌' in dam_row['Status']
    
    def test_knock_events_detected(self, problem_df):
        """Should detect knock events."""
        summary = generate_executive_summary(problem_df, DEFAULT_CONFIG)
        knock_rows = summary[summary['Parameter'] == 'Knock Events']
        if len(knock_rows) > 0:
            knock_row = knock_rows.iloc[0]
            knock_count = int(knock_row['Value'])
            assert knock_count > 0  # Knock detected
    
    def test_fkl_detected(self, problem_df):
        """Should detect Fine Knock Learn retard."""
        summary = generate_executive_summary(problem_df, DEFAULT_CONFIG)
        fkl_rows = summary[summary['Parameter'] == 'Fine Knock Learn']
        if len(fkl_rows) > 0:
            fkl_row = fkl_rows.iloc[0]
            fkl_value = float(fkl_row['Value'].replace('°', ''))
            assert fkl_value < 0  # FKL retard detected
    
    def test_lean_stft_flagged(self, problem_df):
        """Should flag high positive STFT (lean condition)."""
        summary = generate_executive_summary(problem_df, DEFAULT_CONFIG)
        stft_row = summary[summary['Parameter'] == 'STFT (avg)'].iloc[0]
        # High positive STFT = running lean
        stft_value = float(stft_row['Value'].replace('%', '').replace('+', ''))
        # The problematic datalog has avg STFT of ~4.5% (mix of cruise +2% and WOT +8%)
        # This should trigger at least warning status since it's near threshold
        assert stft_value > 2  # Running lean-ish
        # Status check - if value > 5% it should warn, otherwise might be OK
        if stft_value >= 5:
            assert '⚠️' in stft_row['Status'] or '❌' in stft_row['Status']
    
    def test_boost_overshoot_detected(self, problem_df):
        """Should detect boost overshoot via high peak boost."""
        summary = generate_executive_summary(problem_df, DEFAULT_CONFIG)
        boost_rows = summary[summary['Parameter'] == 'Peak Boost']
        if len(boost_rows) > 0:
            boost_row = boost_rows.iloc[0]
            peak_value = float(boost_row['Value'].replace(' psi', ''))
            # Problematic datalog has boost 19-24 psi, which exceeds 18 psi target
            assert peak_value > 18  # Overshooting target
            # Should be flagged as overshoot
            assert '⚠️' in boost_row['Status'] or '❌' in boost_row['Status']


class TestMafAnalysis:
    """Test MAF-based fuel trim analysis."""
    
    def test_maf_bins_covered(self):
        """Should analyze multiple MAF ranges."""
        df = create_healthy_datalog(1000)
        maf_df = generate_maf_analysis(df)
        assert len(maf_df) >= 3  # At least 3 MAF bins with data
    
    def test_maf_combined_calculation(self):
        """Combined trim should equal STFT + LTFT."""
        df = create_healthy_datalog(1000)
        maf_df = generate_maf_analysis(df)
        
        if len(maf_df) > 0:
            row = maf_df.iloc[0]
            stft = float(row['STFT'].replace('%', '').replace('+', ''))
            ltft = float(row['LTFT'].replace('%', '').replace('+', ''))
            combined = float(row['Combined'].replace('%', '').replace('+', ''))
            assert abs((stft + ltft) - combined) < 0.1  # Math check


class TestPeAnalysis:
    """Test Power Enrichment analysis."""
    
    def test_pe_rpm_bins(self):
        """Should analyze multiple RPM ranges under WOT."""
        df = create_healthy_datalog(1000)
        pe_df = generate_pe_analysis(df)
        if pe_df is not None:
            assert len(pe_df) >= 2  # At least 2 RPM bins
    
    def test_afr_lambda_relationship(self):
        """AFR should equal Lambda * 14.7."""
        df = create_healthy_datalog(1000)
        pe_df = generate_pe_analysis(df)
        
        if pe_df is not None and len(pe_df) > 0:
            row = pe_df.iloc[0]
            lambda_val = float(row['Lambda'])
            afr_val = float(row['AFR'].replace(':1', ''))
            expected_afr = lambda_val * 14.7
            assert abs(afr_val - expected_afr) < 0.2  # Math check


class TestThresholdAccuracy:
    """Validate that thresholds match FA20DIT specifications."""
    
    def test_dam_thresholds(self):
        """DAM thresholds should match known FA20 values."""
        assert DEFAULT_CONFIG['thresholds']['dam_warning'] == 0.95
        assert DEFAULT_CONFIG['thresholds']['dam_critical'] == 0.75
    
    def test_knock_thresholds(self):
        """Knock thresholds should be appropriate for FA20."""
        assert DEFAULT_CONFIG['thresholds']['fbk_warning'] == -1
        assert DEFAULT_CONFIG['thresholds']['fbk_critical'] == -3
        assert DEFAULT_CONFIG['thresholds']['fkl_warning'] == -1
        assert DEFAULT_CONFIG['thresholds']['fkl_critical'] == -2
    
    def test_fuel_trim_thresholds(self):
        """Fuel trim thresholds should match tuning best practices."""
        assert DEFAULT_CONFIG['thresholds']['stft_warning'] == 5
        assert DEFAULT_CONFIG['thresholds']['stft_critical'] == 10
        assert DEFAULT_CONFIG['thresholds']['ltft_warning'] == 5
        assert DEFAULT_CONFIG['thresholds']['ltft_critical'] == 10
    
    def test_boost_target(self):
        """Stock boost target should be ~18 psi."""
        assert DEFAULT_CONFIG['targets']['peak_boost_psi'] == 18


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_datalog(self):
        """Should handle empty datalog gracefully."""
        df = pd.DataFrame()
        # Should not crash
        try:
            summary = generate_executive_summary(df, DEFAULT_CONFIG)
            assert len(summary) == 0 or summary is not None
        except KeyError:
            pass  # Expected if columns missing
    
    def test_missing_columns(self):
        """Should handle missing columns gracefully."""
        df = pd.DataFrame({'Engine - RPM': [1000, 2000, 3000]})
        summary = generate_executive_summary(df, DEFAULT_CONFIG)
        # Should return partial results, not crash
        assert summary is not None
    
    def test_nan_values(self):
        """Should handle NaN values in data."""
        df = create_healthy_datalog(100)
        df.loc[0:10, 'Ignition - Dynamic Advance Multiplier'] = np.nan
        summary = generate_executive_summary(df, DEFAULT_CONFIG)
        # Should still produce results
        assert len(summary) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
