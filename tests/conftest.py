"""
Pytest configuration and shared fixtures for DAMGood tests.
"""
import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="damgood_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_datalog():
    """Create a sample datalog DataFrame for testing with enough data points."""
    n = 100  # Enough samples for histogram and MAF bins
    
    return pd.DataFrame({
        'Engine - RPM': np.linspace(2500, 6000, n),
        'Fuel - Command - Corrections - AF Correction STFT': np.random.uniform(-8, 8, n),
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)': np.random.uniform(-3, 3, n),
        'Ignition - Dynamic Advance Multiplier': np.ones(n),
        'Ignition - Feedback Knock': np.zeros(n),
        'Ignition - Fine Knock Learn': np.zeros(n),
        'Analytical - Boost Pressure': np.linspace(5, 20, n),
        'Sensors - AF Ratio 1': np.random.uniform(0.70, 0.78, n),
        'PIDs - (F410) Mass Air Flow': np.linspace(10, 180, n),
        'Engine - Calculated Load': np.linspace(0.3, 0.98, n),
        'Throttle - Requested Torque - Main Accelerator Position': np.linspace(20, 100, n),
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)': np.linspace(5, 19, n),
        'Airflow - Turbo - Boost - Manifold Absolute Pressure': np.linspace(5.5, 20, n),
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded': np.linspace(20, 90, n),
    })


@pytest.fixture
def sample_wot_datalog(sample_datalog):
    """WOT datalog with high throttle positions."""
    df = sample_datalog.copy()
    n = len(df)
    df['Throttle - Requested Torque - Main Accelerator Position'] = np.linspace(80, 100, n)
    df['Engine - Calculated Load'] = np.linspace(0.82, 0.98, n)
    return df


@pytest.fixture
def healthy_datalog():
    """Datalog representing a healthy tune (DAM=1, no knock, centered trims)."""
    return pd.DataFrame({
        'Engine - RPM': [3000, 4000, 5000, 5500],
        'Fuel - Command - Corrections - AF Correction STFT': [0.5, -0.3, 0.2, -0.1],
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)': [-1.0, -1.2, -0.8, -0.9],
        'Ignition - Dynamic Advance Multiplier': [1.0, 1.0, 1.0, 1.0],
        'Ignition - Feedback Knock': [0.0, 0.0, 0.0, 0.0],
        'Ignition - Fine Knock Learn': [0.0, 0.0, 0.0, 0.0],
        'Analytical - Boost Pressure': [16.0, 17.5, 18.0, 17.5],
        'Sensors - AF Ratio 1': [0.735, 0.730, 0.728, 0.732],
        'PIDs - (F410) Mass Air Flow': [80, 110, 140, 135],
        'Engine - Calculated Load': [0.82, 0.88, 0.94, 0.91],
        'Throttle - Requested Torque - Main Accelerator Position': [90, 95, 100, 95],
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)': [16.0, 17.5, 18.0, 17.5],
        'Airflow - Turbo - Boost - Manifold Absolute Pressure': [16.2, 17.8, 18.3, 17.7],
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded': [55, 70, 80, 72],
    })


@pytest.fixture
def problematic_datalog():
    """Datalog with issues (DAM drop, knock, lean WOT)."""
    return pd.DataFrame({
        'Engine - RPM': [3000, 4000, 5000, 5500],
        'Fuel - Command - Corrections - AF Correction STFT': [2.0, 5.0, 12.0, 8.0],
        'Fuel - Command - Corrections - AF Learn 1 (LTFT)': [3.0, 4.0, 5.0, 4.5],
        'Ignition - Dynamic Advance Multiplier': [1.0, 0.95, 0.85, 0.90],
        'Ignition - Feedback Knock': [0.0, -2.0, -4.5, -3.0],
        'Ignition - Fine Knock Learn': [0.0, -1.0, -3.0, -2.0],
        'Analytical - Boost Pressure': [18.0, 21.0, 23.0, 22.0],
        'Sensors - AF Ratio 1': [0.78, 0.80, 0.82, 0.81],
        'PIDs - (F410) Mass Air Flow': [90, 130, 170, 160],
        'Engine - Calculated Load': [0.85, 0.92, 0.98, 0.95],
        'Throttle - Requested Torque - Main Accelerator Position': [90, 95, 100, 98],
        'Airflow - Turbo - Boost - Boost Target Final (Absolute)': [17.0, 19.0, 20.0, 19.5],
        'Airflow - Turbo - Boost - Manifold Absolute Pressure': [18.5, 21.5, 24.0, 22.5],
        'Airflow - Turbo - Wastegate - Duty Cycle Commanded': [65, 85, 95, 90],
    })


@pytest.fixture
def default_config():
    """Default configuration dictionary."""
    return {
        'vehicle': {
            'year': '2017',
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
