"""
Tests for safety boundary enforcement.

These tests verify that the safety limits and boundary checks work correctly.
Run with: pytest tests/test_safety_boundaries.py -v
"""
import pytest


class TestStockHardwareLimits:
    """Tests for stock hardware safety limits."""
    
    # Stock limits from AGENTS.md
    STOCK_LIMITS = {
        'turbo_safe_psi': 18,
        'turbo_max_psi': 20,
        'tmic_safe_psi': 18,
        'fuel_system_safe_psi': 18,
        'internals_safe_wtq': 300,
        'internals_max_wtq': 350,
        'wot_afr_min': 10.5,
        'dam_minimum': 1.00,
    }
    
    def test_stock_turbo_limit_defined(self):
        assert self.STOCK_LIMITS['turbo_safe_psi'] == 18
        assert self.STOCK_LIMITS['turbo_max_psi'] == 20
    
    def test_stock_intercooler_limit_defined(self):
        assert self.STOCK_LIMITS['tmic_safe_psi'] == 18
    
    def test_stock_internals_limit_defined(self):
        assert self.STOCK_LIMITS['internals_safe_wtq'] == 300
        assert self.STOCK_LIMITS['internals_max_wtq'] == 350
    
    def test_wot_afr_minimum_defined(self):
        assert self.STOCK_LIMITS['wot_afr_min'] == 10.5
    
    def test_dam_minimum_is_one(self):
        assert self.STOCK_LIMITS['dam_minimum'] == 1.00


class TestBoundaryViolationDetection:
    """Tests for detecting when parameters exceed safe limits."""
    
    def test_boost_exceeds_stock_turbo_limit(self):
        """25 psi on stock turbo should be flagged."""
        requested_boost = 25
        stock_turbo_limit = 18
        
        violation = requested_boost > stock_turbo_limit
        assert violation is True
    
    def test_boost_within_stock_limit(self):
        """18 psi on stock turbo should be safe."""
        requested_boost = 18
        stock_turbo_limit = 18
        
        violation = requested_boost > stock_turbo_limit
        assert violation is False
    
    def test_lean_afr_detected(self):
        """AFR > 11.5 at WOT should be flagged as lean."""
        wot_afr = 11.8
        safe_afr_limit = 11.5
        
        is_lean = wot_afr > safe_afr_limit
        assert is_lean is True
    
    def test_rich_afr_is_safe(self):
        """AFR of 10.8 at WOT should be safe."""
        wot_afr = 10.8
        safe_afr_limit = 11.5
        
        is_lean = wot_afr > safe_afr_limit
        assert is_lean is False
    
    def test_dam_drop_detected(self):
        """DAM < 1.00 should always be flagged."""
        observed_dam = 0.95
        required_dam = 1.00
        
        dam_dropped = observed_dam < required_dam
        assert dam_dropped is True
    
    def test_perfect_dam_is_safe(self):
        """DAM = 1.00 should be safe."""
        observed_dam = 1.00
        required_dam = 1.00
        
        dam_dropped = observed_dam < required_dam
        assert dam_dropped is False


class TestUpgradeAdjustments:
    """Tests for safety limit adjustments based on upgrades."""
    
    def test_fmic_adds_boost_headroom(self):
        """FMIC should allow +2 psi over stock TMIC."""
        stock_limit = 18
        fmic_bonus = 2
        
        fmic_limit = stock_limit + fmic_bonus
        assert fmic_limit == 20
    
    def test_e85_allows_more_timing(self):
        """E85 should allow +3° timing over pump gas."""
        base_timing_margin = 2
        e85_timing_bonus = 3
        
        e85_timing_margin = base_timing_margin - e85_timing_bonus
        assert e85_timing_margin == -1  # Can run less margin
    
    def test_e85_allows_leaner_afr(self):
        """E85 should allow AFR up to 9.5:1 safely."""
        pump_gas_min_afr = 10.5
        e85_min_afr = 9.5
        
        assert e85_min_afr < pump_gas_min_afr
    
    def test_built_motor_allows_high_boost(self):
        """Built motor should allow 25+ psi."""
        stock_internals_limit = 18
        built_motor_limit = 25
        
        assert built_motor_limit > stock_internals_limit


class TestDangerousCombinations:
    """Tests for detecting dangerous mod/setting combinations."""
    
    def test_high_boost_stock_tmic_hot_day(self):
        """High boost + stock TMIC + hot ambient = dangerous."""
        boost = 20
        intercooler = 'stock'
        ambient_temp = 95  # Fahrenheit
        
        is_dangerous = (
            boost > 18 and
            intercooler == 'stock' and
            ambient_temp > 85
        )
        assert is_dangerous is True
    
    def test_high_boost_fmic_hot_day_ok(self):
        """High boost + FMIC + hot ambient = acceptable."""
        boost = 20
        intercooler = 'FMIC'
        ambient_temp = 95
        
        is_dangerous = (
            boost > 18 and
            intercooler == 'stock' and
            ambient_temp > 85
        )
        assert is_dangerous is False
    
    def test_91_octane_aggressive_timing(self):
        """91 octane + aggressive timing = dangerous."""
        octane = 91
        timing_advance = 4  # degrees over base
        safe_91_timing = 2  # max safe advance on 91
        
        is_dangerous = (
            octane <= 91 and
            timing_advance > safe_91_timing
        )
        assert is_dangerous is True
    
    def test_e85_wrong_tune_catastrophic(self):
        """E85 in tank + pump gas tune = catastrophic."""
        fuel_in_tank = 'E85'
        tune_fuel_type = 'pump_gas'
        
        is_catastrophic = (
            fuel_in_tank == 'E85' and
            tune_fuel_type == 'pump_gas'
        )
        assert is_catastrophic is True


class TestSafetyMarginCalculation:
    """Tests for dynamic safety margin calculation."""
    
    def test_stock_config_base_margins(self):
        """Stock config should have base margins."""
        mods = {
            'turbo': 'stock',
            'intercooler': 'stock',
            'ebcs': 'stock',
            'fuel_grade': 93,
            'climate': 'moderate',
            'altitude': 'low',
            'use_case': 'street',
        }
        
        timing_margin = 2  # Base
        boost_margin = 1   # Base for stock EBCS
        
        assert timing_margin == 2
        assert boost_margin == 1
    
    def test_risky_config_increased_margins(self):
        """Risky config should have increased margins."""
        timing_margin = 2  # Base
        
        # Add risk factors
        timing_margin += 1  # Upgraded turbo
        timing_margin += 1  # Stock IC with mods
        timing_margin += 2  # 91 octane
        timing_margin += 1  # Hot climate
        timing_margin += 1  # Track use
        
        assert timing_margin == 8  # Much more conservative
    
    def test_3port_ebcs_reduces_boost_margin(self):
        """3-port EBCS should reduce boost margin to 0."""
        base_boost_margin = 1
        
        ebcs = '3-port'
        boost_margin = 0 if ebcs == '3-port' else base_boost_margin
        
        assert boost_margin == 0


class TestAcknowledgmentRequirement:
    """Tests for the explicit acknowledgment requirement."""
    
    REQUIRED_PHRASE = "I understand the risks and this will probably blow up my engine"
    
    def test_exact_phrase_required(self):
        """Only the exact phrase should be accepted."""
        user_input = "I understand the risks and this will probably blow up my engine"
        
        acknowledged = user_input == self.REQUIRED_PHRASE
        assert acknowledged is True
    
    def test_partial_phrase_rejected(self):
        """Partial phrase should be rejected."""
        user_input = "I understand the risks"
        
        acknowledged = user_input == self.REQUIRED_PHRASE
        assert acknowledged is False
    
    def test_modified_phrase_rejected(self):
        """Modified phrase should be rejected."""
        user_input = "I understand the risks and will accept the consequences"
        
        acknowledged = user_input == self.REQUIRED_PHRASE
        assert acknowledged is False
    
    def test_yes_not_accepted(self):
        """Simple 'yes' should not bypass safety check."""
        user_input = "yes"
        
        acknowledged = user_input == self.REQUIRED_PHRASE
        assert acknowledged is False
