"""
Tuning Session Management for DAMGood.

Tracks multiple phases of the tuning process, allowing comparison
between initial analysis and subsequent iterations.
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
import pandas as pd


@dataclass
class PhaseAnalysis:
    """Analysis results for a single tuning phase."""
    phase_number: int
    timestamp: str
    log_files: list[str]
    log_type: str
    samples: int
    
    # Key metrics for comparison
    dam_min: float = 1.0
    dam_avg: float = 1.0
    fbk_min: float = 0.0
    fkl_min: float = 0.0
    stft_avg: float = 0.0
    ltft_avg: float = 0.0
    boost_max: float = 0.0
    boost_avg: float = 0.0
    
    # Status flags
    has_knock: bool = False
    has_dam_drop: bool = False
    has_fuel_issues: bool = False
    has_boost_issues: bool = False
    
    notes: str = ""
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PhaseAnalysis':
        return cls(**data)
    
    @classmethod
    def from_dataframe(cls, phase_num: int, df: pd.DataFrame, log_files: list[str], log_type: str) -> 'PhaseAnalysis':
        """Create PhaseAnalysis from analyzed dataframe."""
        dam_col = 'Ignition - Dynamic Advance Multiplier'
        fbk_col = 'Ignition - Feedback Knock'
        fkl_col = 'Ignition - Fine Knock Learn'
        stft_col = 'Fuel - Command - Corrections - AF Correction STFT'
        ltft_col = 'Fuel - Command - Corrections - AF Learn 1 (LTFT)'
        boost_col = 'Analytical - Boost Pressure'
        
        dam_min = df[dam_col].min() if dam_col in df.columns else 1.0
        dam_avg = df[dam_col].mean() if dam_col in df.columns else 1.0
        fbk_min = df[fbk_col].min() if fbk_col in df.columns else 0.0
        fkl_min = df[fkl_col].min() if fkl_col in df.columns else 0.0
        stft_avg = df[stft_col].mean() if stft_col in df.columns else 0.0
        ltft_avg = df[ltft_col].mean() if ltft_col in df.columns else 0.0
        boost_max = df[boost_col].max() if boost_col in df.columns else 0.0
        boost_avg = df[boost_col].mean() if boost_col in df.columns else 0.0
        
        return cls(
            phase_number=phase_num,
            timestamp=datetime.now().isoformat(),
            log_files=[str(f) for f in log_files],
            log_type=log_type,
            samples=len(df),
            dam_min=float(dam_min) if pd.notna(dam_min) else 1.0,
            dam_avg=float(dam_avg) if pd.notna(dam_avg) else 1.0,
            fbk_min=float(fbk_min) if pd.notna(fbk_min) else 0.0,
            fkl_min=float(fkl_min) if pd.notna(fkl_min) else 0.0,
            stft_avg=float(stft_avg) if pd.notna(stft_avg) else 0.0,
            ltft_avg=float(ltft_avg) if pd.notna(ltft_avg) else 0.0,
            boost_max=float(boost_max) if pd.notna(boost_max) else 0.0,
            boost_avg=float(boost_avg) if pd.notna(boost_avg) else 0.0,
            has_knock=(fbk_min < -1.0) if pd.notna(fbk_min) else False,
            has_dam_drop=(dam_min < 1.0) if pd.notna(dam_min) else False,
            has_fuel_issues=(abs(stft_avg) > 5 or abs(ltft_avg) > 5) if pd.notna(stft_avg) else False,
            has_boost_issues=False,  # Could add overshoot detection
        )


@dataclass 
class TuningSession:
    """Manages a complete tuning session across multiple phases."""
    
    session_id: str = ""
    created: str = ""
    modified: str = ""
    vehicle_info: str = ""
    notes: str = ""
    
    phases: list[PhaseAnalysis] = field(default_factory=list)
    active_phase: int = 1
    
    _dirty: bool = field(default=False, repr=False)
    _save_path: Optional[Path] = field(default=None, repr=False)
    
    def __post_init__(self):
        if not self.session_id:
            self.session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
        if not self.created:
            self.created = datetime.now().isoformat()
        self.modified = datetime.now().isoformat()
    
    @property
    def is_dirty(self) -> bool:
        return self._dirty
    
    @property
    def current_phase_number(self) -> int:
        return len(self.phases) + 1 if not self.phases else max(p.phase_number for p in self.phases)
    
    @property
    def next_phase_number(self) -> int:
        return self.current_phase_number + 1 if self.phases else 1
    
    def get_phase(self, phase_num: int) -> Optional[PhaseAnalysis]:
        for p in self.phases:
            if p.phase_number == phase_num:
                return p
        return None
    
    def get_active_phase(self) -> Optional[PhaseAnalysis]:
        return self.get_phase(self.active_phase)
    
    def add_phase(self, analysis: PhaseAnalysis):
        """Add a new phase analysis."""
        self.phases.append(analysis)
        self.active_phase = analysis.phase_number
        self.modified = datetime.now().isoformat()
        self._dirty = True
    
    def set_active_phase(self, phase_num: int):
        """Set the active phase for viewing."""
        if self.get_phase(phase_num):
            self.active_phase = phase_num
            self._dirty = True
    
    def compare_phases(self, phase1_num: int, phase2_num: int) -> dict:
        """Compare two phases and return differences."""
        p1 = self.get_phase(phase1_num)
        p2 = self.get_phase(phase2_num)
        
        if not p1 or not p2:
            return {}
        
        def delta(v1, v2, name, better_lower=True):
            diff = v2 - v1
            if better_lower:
                status = "improved" if diff < 0 else ("worse" if diff > 0 else "same")
            else:
                status = "improved" if diff > 0 else ("worse" if diff < 0 else "same")
            return {"before": v1, "after": v2, "delta": diff, "status": status}
        
        return {
            "dam_min": delta(p1.dam_min, p2.dam_min, "DAM", better_lower=False),
            "fbk_min": delta(p1.fbk_min, p2.fbk_min, "Feedback Knock", better_lower=False),  # Less negative is better
            "fkl_min": delta(p1.fkl_min, p2.fkl_min, "Fine Knock Learn", better_lower=False),  # Less negative is better
            "stft_avg": delta(abs(p1.stft_avg), abs(p2.stft_avg), "STFT"),
            "ltft_avg": delta(abs(p1.ltft_avg), abs(p2.ltft_avg), "LTFT"),
            "samples": {"before": p1.samples, "after": p2.samples},
        }
    
    def get_progress_summary(self) -> str:
        """Get a summary of tuning progress across all phases."""
        if len(self.phases) < 2:
            return "Complete Phase 1 analysis first"
        
        first = self.phases[0]
        last = self.phases[-1]
        
        lines = [f"Progress: Phase 1 → Phase {last.phase_number}"]
        
        # DAM status
        if first.dam_min < 1.0 and last.dam_min >= 1.0:
            lines.append("✅ DAM recovered to 1.00")
        elif last.dam_min < 1.0:
            lines.append("⚠️ DAM still below 1.00")
        else:
            lines.append("✅ DAM stable at 1.00")
        
        # Fuel trim progress
        stft_improvement = abs(first.stft_avg) - abs(last.stft_avg)
        if stft_improvement > 1:
            lines.append(f"✅ STFT improved by {stft_improvement:.1f}%")
        elif stft_improvement < -1:
            lines.append(f"⚠️ STFT worsened by {abs(stft_improvement):.1f}%")
        
        # Knock status
        if first.has_knock and not last.has_knock:
            lines.append("✅ Knock events resolved")
        elif last.has_knock:
            lines.append("⚠️ Still seeing knock events")
        
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "created": self.created,
            "modified": self.modified,
            "vehicle_info": self.vehicle_info,
            "notes": self.notes,
            "phases": [p.to_dict() for p in self.phases],
            "active_phase": self.active_phase,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TuningSession':
        phases = [PhaseAnalysis.from_dict(p) for p in data.get("phases", [])]
        return cls(
            session_id=data.get("session_id", ""),
            created=data.get("created", ""),
            modified=data.get("modified", ""),
            vehicle_info=data.get("vehicle_info", ""),
            notes=data.get("notes", ""),
            phases=phases,
            active_phase=data.get("active_phase", 1),
        )
    
    def save(self, path: Optional[Path] = None):
        """Save session to JSON file."""
        save_path = path or self._save_path
        if not save_path:
            raise ValueError("No save path specified")
        
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        self._save_path = save_path
        self._dirty = False
        self.modified = datetime.now().isoformat()
    
    @classmethod
    def load(cls, path: Path) -> 'TuningSession':
        """Load session from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        session = cls.from_dict(data)
        session._save_path = path
        session._dirty = False
        return session
