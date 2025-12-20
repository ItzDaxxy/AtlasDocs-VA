#!/usr/bin/env python3
"""
DAMGood TUI - Interactive FA20 Datalog Analyzer
A beautiful terminal interface for analyzing WRX datalogs.

Run with: python scripts/tui.py
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Static, DataTable, Button, 
    Label, ProgressBar, TabbedContent, TabPane,
    DirectoryTree, Input, RichLog
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual import events
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
import pandas as pd
import sys

# Add scripts directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from analyze_datalog import (
    load_datalog, load_config, generate_executive_summary,
    generate_stft_histogram, generate_maf_analysis,
    generate_boost_analysis, generate_pe_analysis,
    generate_action_items, DEFAULT_CONFIG
)


class StatusIndicator(Static):
    """A colored status indicator widget."""
    
    def __init__(self, status: str = "unknown", label: str = "", **kwargs):
        super().__init__(**kwargs)
        self.status = status
        self.label = label
    
    def compose(self) -> ComposeResult:
        yield Static(self._render())
    
    def _render(self) -> Text:
        colors = {
            "ok": "green",
            "warning": "yellow",
            "critical": "red",
            "unknown": "dim"
        }
        symbols = {
            "ok": "✓",
            "warning": "⚠",
            "critical": "✗",
            "unknown": "?"
        }
        color = colors.get(self.status, "dim")
        symbol = symbols.get(self.status, "?")
        return Text(f" {symbol} {self.label} ", style=f"bold {color}")
    
    def update_status(self, status: str, label: str = None):
        self.status = status
        if label:
            self.label = label
        self.refresh()


class SummaryPanel(Static):
    """Executive summary panel showing key health metrics."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
    
    def compose(self) -> ComposeResult:
        yield Static("Load a datalog to see analysis", id="summary-content")
    
    def update_data(self, df: pd.DataFrame, config: dict):
        """Update the summary with new datalog data."""
        self.data = generate_executive_summary(df, config)
        content = self.query_one("#summary-content", Static)
        
        # Build rich display
        table = Table(title="Executive Summary", expand=True)
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", justify="right")
        table.add_column("Threshold", justify="center")
        table.add_column("Status", justify="center")
        
        for _, row in self.data.iterrows():
            status = row['Status']
            if '✅' in status:
                style = "green"
            elif '⚠️' in status:
                style = "yellow"
            else:
                style = "red"
            table.add_row(
                row['Parameter'],
                str(row['Value']),
                row['Threshold'],
                Text(status, style=style)
            )
        
        content.update(table)


class FuelTrimPanel(Static):
    """Fuel trim analysis panel with STFT histogram and MAF breakdown."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("STFT Distribution", classes="section-title")
            yield DataTable(id="stft-table", zebra_stripes=True)
            yield Static("Fuel Trim by MAF Range", classes="section-title")
            yield DataTable(id="maf-table", zebra_stripes=True)
    
    def update_data(self, df: pd.DataFrame):
        """Update fuel trim tables with datalog data."""
        # STFT Histogram
        stft_data = generate_stft_histogram(df)
        stft_table = self.query_one("#stft-table", DataTable)
        stft_table.clear(columns=True)
        stft_table.add_columns("Range", "Count", "Pct", "Distribution")
        for _, row in stft_data.iterrows():
            stft_table.add_row(
                row['Range'],
                str(row['Count']),
                f"{row['Pct']}%",
                row['Histogram']
            )
        
        # MAF Analysis
        maf_data = generate_maf_analysis(df)
        maf_table = self.query_one("#maf-table", DataTable)
        maf_table.clear(columns=True)
        if not maf_data.empty:
            maf_table.add_columns("MAF Range", "STFT", "LTFT", "Combined", "Status", "Samples")
            for _, row in maf_data.iterrows():
                maf_table.add_row(
                    row['MAF Range'],
                    row['STFT'],
                    row['LTFT'],
                    row['Combined'],
                    row['Status'],
                    str(row['Samples'])
                )


class BoostPanel(Static):
    """Boost control analysis panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Boost Distribution", classes="section-title")
            yield DataTable(id="boost-dist-table", zebra_stripes=True)
            yield Static("WOT Performance", classes="section-title")
            yield DataTable(id="wot-stats-table", zebra_stripes=True)
    
    def update_data(self, df_wot: pd.DataFrame):
        """Update boost tables with WOT datalog data."""
        boost_dist, wot_stats = generate_boost_analysis(df_wot)
        
        # Boost distribution
        dist_table = self.query_one("#boost-dist-table", DataTable)
        dist_table.clear(columns=True)
        if boost_dist is not None and not boost_dist.empty:
            dist_table.add_columns("Range", "Count", "Distribution")
            for _, row in boost_dist.iterrows():
                dist_table.add_row(
                    row['Range'],
                    str(row['Count']),
                    row['Histogram']
                )
        
        # WOT stats
        stats_table = self.query_one("#wot-stats-table", DataTable)
        stats_table.clear(columns=True)
        if wot_stats is not None and not wot_stats.empty:
            stats_table.add_columns("Metric", "Value")
            for _, row in wot_stats.iterrows():
                stats_table.add_row(row['Metric'], str(row['Value']))


class PowerEnrichmentPanel(Static):
    """Power enrichment (WOT fueling) analysis panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("AFR by RPM (WOT, Load > 80%)", classes="section-title")
            yield DataTable(id="pe-table", zebra_stripes=True)
    
    def update_data(self, df_wot: pd.DataFrame):
        """Update PE table with WOT datalog data."""
        pe_data = generate_pe_analysis(df_wot)
        
        pe_table = self.query_one("#pe-table", DataTable)
        pe_table.clear(columns=True)
        if pe_data is not None and not pe_data.empty:
            pe_table.add_columns("RPM", "Lambda", "AFR", "STFT", "Status")
            for _, row in pe_data.iterrows():
                status = row['Status']
                pe_table.add_row(
                    row['RPM'],
                    row['Lambda'],
                    row['AFR'],
                    row['STFT'],
                    status
                )


class ActionItemsPanel(Static):
    """Action items and recommendations panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Action Items", classes="section-title")
            yield DataTable(id="actions-table", zebra_stripes=True)
    
    def update_data(self, df_all: pd.DataFrame, df_wot: pd.DataFrame):
        """Update action items table."""
        actions = generate_action_items(df_all, df_wot)
        
        table = self.query_one("#actions-table", DataTable)
        table.clear(columns=True)
        table.add_columns("Priority", "Category", "Item", "Status")
        for _, row in actions.iterrows():
            table.add_row(
                str(row['Priority']),
                row['Category'],
                row['Item'],
                row['Status']
            )


class FilePickerScreen(ModalScreen):
    """Modal screen for picking datalog files."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def __init__(self, start_path: str = ".", file_type: str = "wot"):
        super().__init__()
        self.start_path = Path(start_path).expanduser()
        self.file_type = file_type
        self.selected_file = None
    
    def compose(self) -> ComposeResult:
        with Container(id="file-picker-container"):
            yield Static(f"Select {self.file_type.upper()} Datalog", id="picker-title")
            yield DirectoryTree(str(self.start_path), id="file-tree")
            with Horizontal(id="picker-buttons"):
                yield Button("Select", id="select-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn", variant="default")
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        """Handle file selection."""
        if str(event.path).endswith('.csv'):
            self.selected_file = event.path
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "select-btn" and self.selected_file:
            self.dismiss(self.selected_file)
        elif event.button.id == "cancel-btn":
            self.dismiss(None)
    
    def action_cancel(self):
        self.dismiss(None)


class DAMGoodApp(App):
    """DAMGood - FA20 Datalog Analyzer TUI."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
    }
    
    #sidebar {
        width: 30;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }
    
    #content {
        width: 100%;
        padding: 1;
    }
    
    .section-title {
        background: $primary;
        color: $text;
        padding: 0 1;
        margin: 1 0 0 0;
        text-style: bold;
    }
    
    #summary-panel {
        height: auto;
        max-height: 12;
        border: solid $primary;
        margin: 0 0 1 0;
    }
    
    DataTable {
        height: auto;
        max-height: 15;
        margin: 0 0 1 0;
    }
    
    #file-info {
        height: 3;
        background: $boost;
        padding: 0 1;
    }
    
    #status-bar {
        height: 1;
        background: $primary-darken-2;
        color: $text;
        padding: 0 1;
    }
    
    Button {
        margin: 0 1;
    }
    
    #load-wot-btn {
        background: $success;
    }
    
    #load-cruise-btn {
        background: $warning;
    }
    
    #generate-btn {
        background: $primary;
    }
    
    /* File picker modal */
    #file-picker-container {
        width: 80%;
        height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }
    
    #picker-title {
        text-align: center;
        text-style: bold;
        background: $primary;
        padding: 1;
        margin-bottom: 1;
    }
    
    #file-tree {
        height: 100%;
        margin-bottom: 1;
    }
    
    #picker-buttons {
        height: 3;
        align: center middle;
    }
    
    TabbedContent {
        height: 100%;
    }
    
    TabPane {
        padding: 1;
    }
    """
    
    TITLE = "DAMGood"
    SUB_TITLE = "FA20 Datalog Analyzer"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("w", "load_wot", "Load WOT"),
        Binding("c", "load_cruise", "Load Cruise"),
        Binding("g", "generate_tables", "Generate Tables"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    def __init__(self):
        super().__init__()
        self.df_wot = None
        self.df_cruise = None
        self.df_all = None
        self.config = load_config(None)
        self.wot_path = None
        self.cruise_path = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="main-container"):
            # Sidebar
            with Vertical(id="sidebar"):
                yield Static("📁 Datalogs", classes="section-title")
                yield Button("Load WOT", id="load-wot-btn", variant="success")
                yield Button("Load Cruise", id="load-cruise-btn", variant="warning")
                yield Static("", id="wot-file-label")
                yield Static("", id="cruise-file-label")
                yield Static("─" * 28)
                yield Static("⚡ Actions", classes="section-title")
                yield Button("Generate Tables", id="generate-btn", variant="primary")
                yield Button("Export Report", id="export-btn")
                yield Static("─" * 28)
                yield Static("📊 Status", classes="section-title")
                yield Static("No data loaded", id="status-label")
            
            # Main content with tabs
            with Vertical(id="content"):
                yield Static("", id="file-info")
                
                with TabbedContent():
                    with TabPane("Summary", id="tab-summary"):
                        yield SummaryPanel(id="summary-panel")
                        yield ActionItemsPanel(id="actions-panel")
                    
                    with TabPane("Fuel Trims", id="tab-fuel"):
                        with ScrollableContainer():
                            yield FuelTrimPanel(id="fuel-panel")
                    
                    with TabPane("Boost", id="tab-boost"):
                        with ScrollableContainer():
                            yield BoostPanel(id="boost-panel")
                    
                    with TabPane("Power Enrichment", id="tab-pe"):
                        with ScrollableContainer():
                            yield PowerEnrichmentPanel(id="pe-panel")
        
        yield Footer()
    
    def on_mount(self):
        """Called when app is mounted."""
        self.update_status("Ready - Press 'W' to load WOT datalog")
    
    def update_status(self, message: str):
        """Update the status label."""
        status = self.query_one("#status-label", Static)
        status.update(message)
    
    def update_file_info(self):
        """Update the file info bar."""
        info = self.query_one("#file-info", Static)
        parts = []
        if self.wot_path:
            parts.append(f"WOT: {self.wot_path.name}")
        if self.cruise_path:
            parts.append(f"Cruise: {self.cruise_path.name}")
        if self.df_all is not None:
            parts.append(f"Samples: {len(self.df_all)}")
        info.update(" | ".join(parts) if parts else "No datalogs loaded")
    
    def action_load_wot(self):
        """Load WOT datalog file."""
        start_path = self.wot_path.parent if self.wot_path else Path.home()
        
        def handle_wot_result(result):
            if result:
                self.wot_path = Path(result)
                try:
                    self.df_wot = load_datalog(str(self.wot_path))
                    self.query_one("#wot-file-label", Static).update(f"✓ {self.wot_path.name}")
                    self._merge_and_analyze()
                    self.update_status(f"Loaded WOT: {len(self.df_wot)} samples")
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(FilePickerScreen(str(start_path), "wot"), handle_wot_result)
    
    def action_load_cruise(self):
        """Load cruise datalog file."""
        start_path = self.cruise_path.parent if self.cruise_path else Path.home()
        
        def handle_cruise_result(result):
            if result:
                self.cruise_path = Path(result)
                try:
                    self.df_cruise = load_datalog(str(self.cruise_path))
                    self.query_one("#cruise-file-label", Static).update(f"✓ {self.cruise_path.name}")
                    self._merge_and_analyze()
                    self.update_status(f"Loaded Cruise: {len(self.df_cruise)} samples")
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(FilePickerScreen(str(start_path), "cruise"), handle_cruise_result)
    
    def _merge_and_analyze(self):
        """Merge datalogs and run analysis."""
        if self.df_wot is not None:
            if self.df_cruise is not None:
                self.df_all = pd.concat([self.df_wot, self.df_cruise], ignore_index=True)
            else:
                self.df_all = self.df_wot
            
            # Update all panels
            self.query_one("#summary-panel", SummaryPanel).update_data(self.df_all, self.config)
            self.query_one("#fuel-panel", FuelTrimPanel).update_data(self.df_all)
            self.query_one("#boost-panel", BoostPanel).update_data(self.df_wot)
            self.query_one("#pe-panel", PowerEnrichmentPanel).update_data(self.df_wot)
            self.query_one("#actions-panel", ActionItemsPanel).update_data(self.df_all, self.df_wot)
            
            self.update_file_info()
    
    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "load-wot-btn":
            self.action_load_wot()
        elif event.button.id == "load-cruise-btn":
            self.action_load_cruise()
        elif event.button.id == "generate-btn":
            self.action_generate_tables()
        elif event.button.id == "export-btn":
            self.action_export_report()
    
    def action_generate_tables(self):
        """Generate revised tables."""
        if self.df_all is None:
            self.update_status("Load a datalog first!")
            return
        
        # Import the table generation function
        from analyze_datalog import generate_revised_tables
        
        save_dir = Path.home() / "Documents" / "Atlas Tables"
        try:
            generate_revised_tables(self.df_all, self.df_wot, str(save_dir))
            self.update_status(f"Tables saved to {save_dir}")
        except Exception as e:
            self.update_status(f"Error generating tables: {e}")
    
    def action_export_report(self):
        """Export full text report."""
        if self.df_all is None:
            self.update_status("Load a datalog first!")
            return
        
        from analyze_datalog import generate_report
        
        output_path = Path.home() / "Documents" / "FA20_Tuning_Report.txt"
        try:
            generate_report(self.df_all, self.df_wot, output_path, self.config)
            self.update_status(f"Report saved to {output_path}")
        except Exception as e:
            self.update_status(f"Error: {e}")
    
    def action_refresh(self):
        """Refresh the analysis."""
        if self.df_all is not None:
            self._merge_and_analyze()
            self.update_status("Refreshed analysis")


def main():
    app = DAMGoodApp()
    app.run()


if __name__ == "__main__":
    main()
