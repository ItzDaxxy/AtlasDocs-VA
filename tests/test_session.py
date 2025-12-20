"""
Tests for session.py - TuningSession and PhaseAnalysis classes.

Run with: pytest tests/test_session.py -v
"""
import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from session import TuningSession, PhaseAnalysis


class TestPhaseAnalysis:
    """Tests for PhaseAnalysis dataclass."""
    
    def test_create_phase_analysis(self):
        phase = PhaseAnalysis(
            phase_number=1,
            timestamp=datetime.now().isoformat(),
            log_files=["log1.csv", "log2.csv"],
            log_type="WOT",
            samples=500
        )
        assert phase.phase_number == 1
        assert phase.log_type == "WOT"
        assert phase.samples == 500
        assert len(phase.log_files) == 2
    
    def test_default_values(self):
        phase = PhaseAnalysis(
            phase_number=1,
            timestamp="2024-01-01T00:00:00",
            log_files=[],
            log_type="Cruise",
            samples=100
        )
        assert phase.dam_min == 1.0
        assert phase.dam_avg == 1.0
        assert phase.fbk_min == 0.0
        assert phase.fkl_min == 0.0
        assert phase.stft_avg == 0.0
        assert phase.ltft_avg == 0.0
        assert phase.has_knock is False
        assert phase.has_dam_drop is False
    
    def test_to_dict(self):
        phase = PhaseAnalysis(
            phase_number=2,
            timestamp="2024-01-01T12:00:00",
            log_files=["wot.csv"],
            log_type="WOT",
            samples=250,
            dam_min=0.95,
            fbk_min=-2.5,
            has_knock=True
        )
        data = phase.to_dict()
        
        assert data["phase_number"] == 2
        assert data["dam_min"] == 0.95
        assert data["fbk_min"] == -2.5
        assert data["has_knock"] is True
    
    def test_from_dict(self):
        data = {
            "phase_number": 3,
            "timestamp": "2024-01-02T00:00:00",
            "log_files": ["cruise.csv"],
            "log_type": "Cruise",
            "samples": 1000,
            "dam_min": 1.0,
            "dam_avg": 1.0,
            "fbk_min": 0.0,
            "fkl_min": 0.0,
            "stft_avg": -2.5,
            "ltft_avg": -1.0,
            "boost_max": 18.5,
            "boost_avg": 15.0,
            "has_knock": False,
            "has_dam_drop": False,
            "has_fuel_issues": False,
            "has_boost_issues": False,
            "notes": "Good tune"
        }
        phase = PhaseAnalysis.from_dict(data)
        
        assert phase.phase_number == 3
        assert phase.stft_avg == -2.5
        assert phase.boost_max == 18.5
        assert phase.notes == "Good tune"
    
    def test_from_dataframe(self, sample_datalog):
        phase = PhaseAnalysis.from_dataframe(
            phase_num=1,
            df=sample_datalog,
            log_files=["test.csv"],
            log_type="Mixed"
        )
        
        assert phase.phase_number == 1
        assert phase.samples == len(sample_datalog)
        assert phase.log_type == "Mixed"
        assert isinstance(phase.dam_min, float)
        assert isinstance(phase.stft_avg, float)
    
    def test_from_dataframe_detects_knock(self, problematic_datalog):
        phase = PhaseAnalysis.from_dataframe(
            phase_num=1,
            df=problematic_datalog,
            log_files=["problem.csv"],
            log_type="WOT"
        )
        
        assert phase.has_knock == True
        assert phase.has_dam_drop == True
        assert phase.fbk_min < -1.0


class TestTuningSession:
    """Tests for TuningSession class."""
    
    def test_create_session(self):
        session = TuningSession()
        
        assert session.session_id.startswith("session_")
        assert session.created != ""
        assert session.modified != ""
        assert len(session.phases) == 0
        assert session.active_phase == 1
    
    def test_create_session_with_values(self):
        session = TuningSession(
            session_id="my_session",
            vehicle_info="2018 WRX",
            notes="Initial tune"
        )
        
        assert session.session_id == "my_session"
        assert session.vehicle_info == "2018 WRX"
        assert session.notes == "Initial tune"
    
    def test_add_phase(self):
        session = TuningSession()
        phase = PhaseAnalysis(
            phase_number=1,
            timestamp=datetime.now().isoformat(),
            log_files=["log.csv"],
            log_type="WOT",
            samples=100
        )
        
        session.add_phase(phase)
        
        assert len(session.phases) == 1
        assert session.active_phase == 1
        assert session.is_dirty is True
    
    def test_add_multiple_phases(self):
        session = TuningSession()
        
        for i in range(1, 4):
            phase = PhaseAnalysis(
                phase_number=i,
                timestamp=datetime.now().isoformat(),
                log_files=[f"log{i}.csv"],
                log_type="WOT",
                samples=100 * i
            )
            session.add_phase(phase)
        
        assert len(session.phases) == 3
        assert session.active_phase == 3
        assert session.current_phase_number == 3
        assert session.next_phase_number == 4
    
    def test_get_phase(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        phase2 = PhaseAnalysis(phase_number=2, timestamp="", log_files=[], log_type="", samples=200)
        session.add_phase(phase1)
        session.add_phase(phase2)
        
        assert session.get_phase(1).samples == 100
        assert session.get_phase(2).samples == 200
        assert session.get_phase(3) is None
    
    def test_set_active_phase(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        phase2 = PhaseAnalysis(phase_number=2, timestamp="", log_files=[], log_type="", samples=200)
        session.add_phase(phase1)
        session.add_phase(phase2)
        
        session.set_active_phase(1)
        assert session.active_phase == 1
        assert session.get_active_phase().samples == 100
    
    def test_set_active_phase_invalid(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        session.add_phase(phase1)
        
        session.set_active_phase(99)  # Invalid phase
        assert session.active_phase == 1  # Should remain unchanged
    
    def test_compare_phases(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(
            phase_number=1, timestamp="", log_files=[], log_type="", samples=100,
            dam_min=0.85, fbk_min=-3.0, stft_avg=8.0
        )
        phase2 = PhaseAnalysis(
            phase_number=2, timestamp="", log_files=[], log_type="", samples=150,
            dam_min=1.0, fbk_min=-0.5, stft_avg=2.0
        )
        session.add_phase(phase1)
        session.add_phase(phase2)
        
        comparison = session.compare_phases(1, 2)
        
        assert comparison["dam_min"]["status"] == "improved"
        assert comparison["fbk_min"]["status"] == "improved"
        assert comparison["stft_avg"]["status"] == "improved"
        assert comparison["samples"]["before"] == 100
        assert comparison["samples"]["after"] == 150
    
    def test_compare_phases_invalid(self):
        session = TuningSession()
        comparison = session.compare_phases(1, 2)
        assert comparison == {}
    
    def test_progress_summary_single_phase(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        session.add_phase(phase1)
        
        summary = session.get_progress_summary()
        assert "Complete Phase 1" in summary
    
    def test_progress_summary_multiple_phases(self):
        session = TuningSession()
        phase1 = PhaseAnalysis(
            phase_number=1, timestamp="", log_files=[], log_type="", samples=100,
            dam_min=0.85, has_knock=True, stft_avg=8.0
        )
        phase2 = PhaseAnalysis(
            phase_number=2, timestamp="", log_files=[], log_type="", samples=150,
            dam_min=1.0, has_knock=False, stft_avg=2.0
        )
        session.add_phase(phase1)
        session.add_phase(phase2)
        
        summary = session.get_progress_summary()
        assert "DAM recovered" in summary
        assert "Knock events resolved" in summary
        assert "STFT improved" in summary
    
    def test_to_dict(self):
        session = TuningSession(session_id="test", vehicle_info="WRX")
        phase = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        session.add_phase(phase)
        
        data = session.to_dict()
        
        assert data["session_id"] == "test"
        assert data["vehicle_info"] == "WRX"
        assert len(data["phases"]) == 1
        assert data["active_phase"] == 1
    
    def test_from_dict(self):
        data = {
            "session_id": "loaded_session",
            "created": "2024-01-01T00:00:00",
            "modified": "2024-01-02T00:00:00",
            "vehicle_info": "2017 WRX Limited",
            "notes": "Test session",
            "phases": [
                {
                    "phase_number": 1,
                    "timestamp": "2024-01-01T00:00:00",
                    "log_files": ["log1.csv"],
                    "log_type": "WOT",
                    "samples": 500,
                    "dam_min": 1.0,
                    "dam_avg": 1.0,
                    "fbk_min": 0.0,
                    "fkl_min": 0.0,
                    "stft_avg": 0.0,
                    "ltft_avg": 0.0,
                    "boost_max": 18.0,
                    "boost_avg": 15.0,
                    "has_knock": False,
                    "has_dam_drop": False,
                    "has_fuel_issues": False,
                    "has_boost_issues": False,
                    "notes": ""
                }
            ],
            "active_phase": 1
        }
        
        session = TuningSession.from_dict(data)
        
        assert session.session_id == "loaded_session"
        assert session.vehicle_info == "2017 WRX Limited"
        assert len(session.phases) == 1
        assert session.phases[0].boost_max == 18.0


class TestSessionPersistence:
    """Tests for session save/load functionality."""
    
    def test_save_session(self, temp_project_dir):
        session = TuningSession(session_id="save_test", vehicle_info="2019 WRX")
        phase = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="WOT", samples=100)
        session.add_phase(phase)
        
        save_path = Path(temp_project_dir) / "sessions" / "test_session.json"
        session.save(save_path)
        
        assert save_path.exists()
        assert session.is_dirty is False
        
        with open(save_path) as f:
            data = json.load(f)
        assert data["session_id"] == "save_test"
    
    def test_load_session(self, temp_project_dir):
        # First save a session
        session = TuningSession(session_id="load_test", notes="Load test")
        phase1 = PhaseAnalysis(phase_number=1, timestamp="", log_files=["a.csv"], log_type="WOT", samples=100)
        phase2 = PhaseAnalysis(phase_number=2, timestamp="", log_files=["b.csv"], log_type="Cruise", samples=200)
        session.add_phase(phase1)
        session.add_phase(phase2)
        
        save_path = Path(temp_project_dir) / "session.json"
        session.save(save_path)
        
        # Now load it
        loaded = TuningSession.load(save_path)
        
        assert loaded.session_id == "load_test"
        assert loaded.notes == "Load test"
        assert len(loaded.phases) == 2
        assert loaded.phases[0].log_files == ["a.csv"]
        assert loaded.phases[1].samples == 200
        assert loaded.is_dirty is False
    
    def test_save_without_path_raises(self):
        session = TuningSession()
        with pytest.raises(ValueError, match="No save path"):
            session.save()
    
    def test_save_creates_parent_dirs(self, temp_project_dir):
        session = TuningSession(session_id="nested_test")
        save_path = Path(temp_project_dir) / "deep" / "nested" / "dir" / "session.json"
        
        session.save(save_path)
        
        assert save_path.exists()
    
    def test_dirty_flag_tracking(self):
        session = TuningSession()
        assert session.is_dirty is False
        
        phase = PhaseAnalysis(phase_number=1, timestamp="", log_files=[], log_type="", samples=100)
        session.add_phase(phase)
        assert session.is_dirty is True
    
    def test_round_trip_preserves_data(self, temp_project_dir):
        # Create a session with complex data
        session = TuningSession(
            session_id="roundtrip",
            vehicle_info="2020 WRX Series.White",
            notes="Full round trip test"
        )
        phase = PhaseAnalysis(
            phase_number=1,
            timestamp="2024-06-15T14:30:00",
            log_files=["wot_pull1.csv", "wot_pull2.csv"],
            log_type="WOT",
            samples=1500,
            dam_min=0.96,
            dam_avg=0.99,
            fbk_min=-1.5,
            fkl_min=-0.75,
            stft_avg=3.2,
            ltft_avg=-1.8,
            boost_max=19.5,
            boost_avg=17.2,
            has_knock=True,
            has_dam_drop=True,
            has_fuel_issues=False,
            has_boost_issues=False,
            notes="First pull showed some knock"
        )
        session.add_phase(phase)
        
        save_path = Path(temp_project_dir) / "roundtrip.json"
        session.save(save_path)
        
        loaded = TuningSession.load(save_path)
        
        assert loaded.session_id == session.session_id
        assert loaded.vehicle_info == session.vehicle_info
        assert loaded.notes == session.notes
        assert len(loaded.phases) == 1
        
        loaded_phase = loaded.phases[0]
        assert loaded_phase.dam_min == phase.dam_min
        assert loaded_phase.fbk_min == phase.fbk_min
        assert loaded_phase.boost_max == phase.boost_max
        assert loaded_phase.has_knock == phase.has_knock
        assert loaded_phase.notes == phase.notes
