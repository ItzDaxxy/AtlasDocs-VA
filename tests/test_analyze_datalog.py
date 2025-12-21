"""
Tests for analyze_datalog.py

Run with: pytest tests/test_analyze_datalog.py -v
"""
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_datalog import (
    load_config,
    generate_executive_summary,
    generate_stft_histogram,
    generate_maf_analysis,
    generate_boost_analysis,
    generate_pe_analysis,
    generate_knock_reference,
    generate_action_items,
    DEFAULT_CONFIG,
)


class TestLoadConfig:
    """Tests for configuration loading."""
    
    def test_returns_default_config_when_no_file(self):
        config = load_config(None)
        assert 'vehicle' in config
        assert 'thresholds' in config
        assert config['thresholds']['dam_warning'] == 0.95
    
    def test_default_config_has_required_keys(self):
        assert 'vehicle' in DEFAULT_CONFIG
        assert 'targets' in DEFAULT_CONFIG
        assert 'safety_margins' in DEFAULT_CONFIG
        assert 'thresholds' in DEFAULT_CONFIG
    
    def test_default_thresholds_are_sensible(self):
        thresholds = DEFAULT_CONFIG['thresholds']
        assert thresholds['dam_warning'] >= thresholds['dam_critical']
        assert thresholds['stft_warning'] <= thresholds['stft_critical']
        assert thresholds['fbk_warning'] >= thresholds['fbk_critical']


class TestExecutiveSummary:
    """Tests for executive summary generation."""
    
    def test_healthy_datalog_shows_green_status(self, healthy_datalog, default_config):
        summary = generate_executive_summary(healthy_datalog, default_config)
        
        # Should have multiple rows now (comprehensive summary)
        assert len(summary) >= 10
        assert 'DAM (min)' in summary['Parameter'].values
        dam_row = summary[summary['Parameter'] == 'DAM (min)']
        assert '✅' in dam_row['Status'].values[0]
    
    def test_problematic_datalog_shows_warnings(self, problematic_datalog, default_config):
        summary = generate_executive_summary(problematic_datalog, default_config)
        
        # DAM dropped to 0.85, should be yellow/warning
        dam_row = summary[summary['Parameter'] == 'DAM (min)']
        assert '⚠️' in dam_row['Status'].values[0] or '❌' in dam_row['Status'].values[0]
        
        # Feedback knock is -4.5, should be red/critical
        fbk_row = summary[summary['Parameter'] == 'Feedback Knock']
        assert '❌' in fbk_row['Status'].values[0]
    
    def test_summary_includes_all_key_parameters(self, sample_datalog, default_config):
        summary = generate_executive_summary(sample_datalog, default_config)
        
        params = summary['Parameter'].tolist()
        assert 'DAM (min)' in params
        assert 'Feedback Knock' in params
        assert 'Fine Knock Learn' in params
        assert 'LTFT (avg)' in params
        assert 'STFT (avg)' in params
        assert 'Combined Trim' in params


class TestSTFTHistogram:
    """Tests for STFT histogram generation."""
    
    def test_histogram_has_expected_bins(self, sample_datalog):
        hist = generate_stft_histogram(sample_datalog)
        
        assert 'Range' in hist.columns
        assert 'Count' in hist.columns
        assert 'Pct' in hist.columns
        assert 'Histogram' in hist.columns
    
    def test_percentages_sum_to_100(self, sample_datalog):
        hist = generate_stft_histogram(sample_datalog)
        total_pct = hist['Pct'].sum()
        assert 99 <= total_pct <= 101  # Allow for rounding
    
    def test_histogram_column_exists(self, sample_datalog):
        hist = generate_stft_histogram(sample_datalog)
        # Histogram column should exist (may be empty if counts are low)
        assert 'Histogram' in hist.columns


class TestMAFAnalysis:
    """Tests for MAF range fuel trim analysis."""
    
    def test_maf_analysis_structure(self, sample_datalog):
        maf_df = generate_maf_analysis(sample_datalog)
        
        expected_cols = ['MAF Range', 'STFT', 'LTFT', 'Combined', 'Status', 'Samples']
        for col in expected_cols:
            assert col in maf_df.columns
    
    def test_maf_analysis_has_status_indicators(self, sample_datalog):
        maf_df = generate_maf_analysis(sample_datalog)
        
        # Should have at least one status
        statuses = maf_df['Status'].tolist()
        assert len(statuses) > 0
        assert any('✅' in s or '⚠️' in s or '❌' in s for s in statuses)
    
    def test_combined_trim_is_sum(self, sample_datalog):
        maf_df = generate_maf_analysis(sample_datalog)
        
        for _, row in maf_df.iterrows():
            stft = float(row['STFT'].replace('%', '').replace('+', ''))
            ltft = float(row['LTFT'].replace('%', '').replace('+', ''))
            combined = float(row['Combined'].replace('%', '').replace('+', ''))
            assert abs((stft + ltft) - combined) < 0.1


class TestBoostAnalysis:
    """Tests for boost control analysis."""
    
    def test_boost_analysis_with_wot_data(self, sample_wot_datalog):
        boost_df, wot_stats = generate_boost_analysis(sample_wot_datalog)
        
        assert boost_df is not None
        assert 'Range' in boost_df.columns
        assert 'Count' in boost_df.columns
    
    def test_wot_stats_includes_key_metrics(self, sample_wot_datalog):
        boost_df, wot_stats = generate_boost_analysis(sample_wot_datalog)
        
        if wot_stats is not None:
            metrics = wot_stats['Metric'].tolist()
            assert 'Peak Boost' in metrics


class TestPEAnalysis:
    """Tests for power enrichment analysis."""
    
    def test_pe_analysis_structure(self, sample_wot_datalog):
        pe_df = generate_pe_analysis(sample_wot_datalog)
        
        if pe_df is not None:
            expected_cols = ['RPM', 'Lambda', 'AFR', 'STFT', 'Status']
            for col in expected_cols:
                assert col in pe_df.columns
    
    def test_pe_analysis_flags_lean_condition(self, problematic_datalog):
        pe_df = generate_pe_analysis(problematic_datalog)
        
        if pe_df is not None:
            # High STFT at WOT should flag as lean
            statuses = pe_df['Status'].tolist()
            assert any('❌' in s or '⚠️' in s for s in statuses)


class TestKnockReference:
    """Tests for knock threshold reference table."""
    
    def test_knock_reference_structure(self):
        ref = generate_knock_reference()
        
        assert 'Parameter' in ref.columns
        assert 'Green' in ref.columns
        assert 'Yellow' in ref.columns
        assert 'Red' in ref.columns
    
    def test_knock_reference_includes_key_params(self):
        ref = generate_knock_reference()
        
        params = ref['Parameter'].tolist()
        assert 'DAM' in params
        assert 'Feedback Knock' in params
        assert 'Fine Knock Learn' in params


class TestActionItems:
    """Tests for action item generation."""
    
    def test_action_items_structure(self, sample_datalog, sample_wot_datalog):
        actions = generate_action_items(sample_datalog, sample_wot_datalog)
        
        assert 'Priority' in actions.columns
        assert 'Category' in actions.columns
        assert 'Item' in actions.columns
        assert 'Status' in actions.columns
    
    def test_healthy_log_has_complete_safety_items(self, healthy_datalog):
        actions = generate_action_items(healthy_datalog, healthy_datalog)
        
        # Safety items should be marked complete
        safety_items = actions[actions['Category'] == 'Safety']
        assert len(safety_items) > 0
        assert any('✅' in str(s) for s in safety_items['Status'].values)
    
    def test_problematic_log_flags_issues(self, problematic_datalog):
        actions = generate_action_items(problematic_datalog, problematic_datalog)
        
        # Should have pending or investigation items
        statuses = actions['Status'].tolist()
        assert any('⚠️' in s or '☐' in s for s in statuses)


class TestThresholdLogic:
    """Tests for threshold evaluation logic."""
    
    def test_dam_below_warning_triggers_alert(self, default_config):
        import pandas as pd
        
        df = pd.DataFrame({
            'Ignition - Dynamic Advance Multiplier': [0.92, 0.90, 0.88],
            'Ignition - Feedback Knock': [0.0, 0.0, 0.0],
            'Ignition - Fine Knock Learn': [0.0, 0.0, 0.0],
            'Fuel - Command - Corrections - AF Learn 1 (LTFT)': [0.0, 0.0, 0.0],
        })
        
        summary = generate_executive_summary(df, default_config)
        # Parameter is now 'DAM (min)' not 'DAM'
        dam_status = summary[summary['Parameter'] == 'DAM (min)']['Status'].values[0]
        
        # DAM at 0.88 should be below 0.95 warning threshold
        assert '⚠️' in dam_status or '❌' in dam_status
    
    def test_dam_critical_triggers_red(self, default_config):
        import pandas as pd
        
        df = pd.DataFrame({
            'Ignition - Dynamic Advance Multiplier': [0.70, 0.65, 0.60],
            'Ignition - Feedback Knock': [0.0, 0.0, 0.0],
            'Ignition - Fine Knock Learn': [0.0, 0.0, 0.0],
            'Fuel - Command - Corrections - AF Learn 1 (LTFT)': [0.0, 0.0, 0.0],
        })
        
        summary = generate_executive_summary(df, default_config)
        # Parameter is now 'DAM (min)' not 'DAM'
        dam_status = summary[summary['Parameter'] == 'DAM (min)']['Status'].values[0]
        
        # DAM at 0.60 should be below 0.75 critical threshold
        assert '❌' in dam_status
