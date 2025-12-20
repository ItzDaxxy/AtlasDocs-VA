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
        Binding("enter", "select", "Select"),
    ]
    
    def __init__(self, start_path: str = "."):
        super().__init__()
        self.start_path = Path(start_path).expanduser()
        self.selected_file = None
    
    def compose(self) -> ComposeResult:
        with Container(id="file-picker-container"):
            yield Static("Select Datalog CSV", id="picker-title")
            yield Static("", id="selected-file-label")
            yield DirectoryTree(str(self.start_path), id="file-tree")
            with Horizontal(id="picker-buttons"):
                yield Button("Open", id="select-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn", variant="default")
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        """Handle file selection (double-click or enter on file)."""
        if str(event.path).endswith('.csv'):
            self.selected_file = event.path
            self.query_one("#selected-file-label", Static).update(f"Selected: {event.path.name}")
            # Auto-dismiss on double-click/enter
            self.dismiss(self.selected_file)
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "select-btn" and self.selected_file:
            self.dismiss(self.selected_file)
        elif event.button.id == "cancel-btn":
            self.dismiss(None)
    
    def action_cancel(self):
        self.dismiss(None)
    
    def action_select(self):
        if self.selected_file:
            self.dismiss(self.selected_file)


class DAMGoodApp(App):
    """DAMGood - FA20 Datalog Analyzer TUI."""
    
    CSS = """
    /* DAMGood Theme - Racing Inspired */
    $accent: #ff6b35;
    $accent-dim: #cc5529;
    $success: #00d26a;
    $warning: #ffd23f;
    $danger: #ff3366;
    $surface-dark: #0d1117;
    $surface: #161b22;
    $surface-light: #21262d;
    $border-color: #30363d;
    $text-dim: #8b949e;
    
    Screen {
        background: $surface-dark;
    }
    
    Header {
        background: $accent;
        color: #000;
    }
    
    Footer {
        background: $surface-light;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
    }
    
    #sidebar {
        width: 26;
        background: $surface;
        border-right: solid $border-color;
        padding: 0 1;
    }
    
    #content {
        width: 100%;
        padding: 0 1;
    }
    
    .section-title {
        background: $surface-light;
        color: $accent;
        padding: 0 1;
        margin: 1 0 0 0;
        text-style: bold;
        height: 1;
    }
    
    #summary-panel {
        height: auto;
        max-height: 10;
        border: solid $border-color;
        margin: 0 0 1 0;
    }
    
    DataTable {
        height: auto;
        max-height: 12;
        margin: 0;
        background: $surface;
    }
    
    DataTable > .datatable--header {
        background: $surface-light;
        color: $accent;
        text-style: bold;
    }
    
    DataTable > .datatable--cursor {
        background: $accent-dim;
        color: #fff;
    }
    
    #file-info {
        height: 1;
        background: $surface-light;
        color: $text-dim;
        padding: 0 1;
    }
    
    /* Compact Buttons */
    Button {
        min-width: 20;
        height: 1;
        margin: 0;
        padding: 0 1;
        border: none;
        background: $surface-light;
        color: $text-dim;
    }
    
    Button:hover {
        background: $accent-dim;
        color: #fff;
    }
    
    Button:focus {
        text-style: bold;
    }
    
    #load-datalog-btn {
        background: $accent;
        color: #000;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #load-datalog-btn:hover {
        background: $accent-dim;
        color: #fff;
    }
    
    #add-datalog-btn {
        background: $surface-light;
        margin-bottom: 1;
    }
    
    #generate-btn {
        background: $success;
        color: #000;
        margin-bottom: 1;
    }
    
    #generate-btn:hover {
        background: #00b359;
    }
    
    #export-btn {
        margin-bottom: 1;
    }
    
    #loaded-files-label {
        color: $success;
        height: auto;
    }
    
    #log-type-label {
        color: $warning;
        height: 1;
        margin-bottom: 1;
    }
    
    #status-label {
        color: $text-dim;
        height: auto;
    }
    
    /* File picker modal */
    #file-picker-container {
        width: 70%;
        height: 70%;
        background: $surface;
        border: solid $accent;
        padding: 1;
    }
    
    #picker-title {
        text-align: center;
        text-style: bold;
        background: $accent;
        color: #000;
        padding: 0 1;
        height: 1;
        margin-bottom: 1;
    }
    
    #selected-file-label {
        color: $success;
        height: 1;
        margin-bottom: 1;
    }
    
    #file-tree {
        height: 100%;
        background: $surface-dark;
        border: solid $border-color;
    }
    
    #picker-buttons {
        height: 1;
        align: center middle;
        margin-top: 1;
    }
    
    #picker-buttons Button {
        min-width: 12;
        margin: 0 1;
    }
    
    #select-btn {
        background: $accent;
        color: #000;
    }
    
    /* Tabs */
    TabbedContent {
        height: 100%;
    }
    
    TabbedContent ContentSwitcher {
        background: $surface-dark;
    }
    
    TabPane {
        padding: 0;
    }
    
    Tabs {
        background: $surface;
        border-bottom: solid $border-color;
    }
    
    Tab {
        background: $surface;
        color: $text-dim;
        padding: 0 2;
    }
    
    Tab:hover {
        background: $surface-light;
        color: #fff;
    }
    
    Tab.-active {
        background: $accent;
        color: #000;
        text-style: bold;
    }
    
    /* Scrollable containers */
    ScrollableContainer {
        background: $surface-dark;
    }
    """
    
    TITLE = "DAMGood"
    SUB_TITLE = "FA20 Datalog Analyzer"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "load_datalog", "Load Datalog"),
        Binding("g", "generate_tables", "Generate Tables"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    def __init__(self):
        super().__init__()
        self.datalogs = []  # List of loaded datalog paths
        self.df_all = None
        self.df_wot = None  # Auto-detected WOT portions
        self.config = load_config(None)
        self.log_type = "Unknown"  # Will be auto-detected
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="main-container"):
            # Sidebar
            with Vertical(id="sidebar"):
                yield Static("📁 Datalogs", classes="section-title")
                yield Button("Load Datalog", id="load-datalog-btn", variant="success")
                yield Button("Add Another", id="add-datalog-btn", variant="default")
                yield Static("", id="loaded-files-label")
                yield Static("", id="log-type-label")
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
        self.update_status("Ready - Press 'L' to load datalog")
    
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
    
    def action_load_datalog(self):
        """Load a datalog file."""
        start_path = self.datalogs[-1].parent if self.datalogs else Path.home()
        
        def handle_result(result):
            if result:
                path = Path(result)
                try:
                    df = load_datalog(str(path))
                    self.datalogs = [path]  # Reset to single file
                    self._process_datalog(df, path)
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(FilePickerScreen(str(start_path)), handle_result)
    
    def action_add_datalog(self):
        """Add another datalog file to the analysis."""
        start_path = self.datalogs[-1].parent if self.datalogs else Path.home()
        
        def handle_result(result):
            if result:
                path = Path(result)
                try:
                    df = load_datalog(str(path))
                    self.datalogs.append(path)
                    # Merge with existing data
                    if self.df_all is not None:
                        combined = pd.concat([self.df_all, df], ignore_index=True)
                        self._process_datalog(combined, path, append=True)
                    else:
                        self._process_datalog(df, path)
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(FilePickerScreen(str(start_path)), handle_result)
    
    def _detect_log_type(self, df: pd.DataFrame) -> tuple:
        """Auto-detect log type based on throttle and load data."""
        throttle_col = 'Throttle - Requested Torque - Main Accelerator Position'
        load_col = 'Engine - Calculated Load'
        
        if throttle_col not in df.columns or load_col not in df.columns:
            return "Mixed", df, df
        
        # WOT: throttle > 80% and load > 0.8
        wot_mask = (df[throttle_col] > 80) & (df[load_col] > 0.8)
        cruise_mask = (df[throttle_col] < 50) & (df[load_col] < 0.5)
        
        wot_count = wot_mask.sum()
        cruise_count = cruise_mask.sum()
        total = len(df)
        
        wot_pct = (wot_count / total) * 100 if total > 0 else 0
        cruise_pct = (cruise_count / total) * 100 if total > 0 else 0
        
        # Determine primary type
        if wot_pct > 30:
            log_type = f"WOT ({wot_pct:.0f}%)"
        elif cruise_pct > 50:
            log_type = f"Cruise ({cruise_pct:.0f}%)"
        else:
            log_type = f"Mixed (WOT:{wot_pct:.0f}% Cruise:{cruise_pct:.0f}%)"
        
        # Extract WOT portion for PE analysis
        df_wot = df[wot_mask] if wot_count > 10 else df
        
        return log_type, df, df_wot
    
    def _process_datalog(self, df: pd.DataFrame, path: Path, append: bool = False):
        """Process loaded datalog and update UI."""
        # Auto-detect log type
        self.log_type, self.df_all, self.df_wot = self._detect_log_type(df)
        
        # Update file labels
        if append:
            files_text = "\n".join([f"✓ {p.name}" for p in self.datalogs])
        else:
            files_text = f"✓ {path.name}"
        self.query_one("#loaded-files-label", Static).update(files_text)
        self.query_one("#log-type-label", Static).update(f"Type: {self.log_type}")
        
        # Run analysis
        self._analyze()
        self.update_status(f"Loaded: {len(self.df_all)} samples | {self.log_type}")
    
    def _analyze(self):
        """Run analysis on loaded data and update all panels."""
        if self.df_all is None:
            return
        
        # Update all panels
        self.query_one("#summary-panel", SummaryPanel).update_data(self.df_all, self.config)
        self.query_one("#fuel-panel", FuelTrimPanel).update_data(self.df_all)
        self.query_one("#boost-panel", BoostPanel).update_data(self.df_wot)
        self.query_one("#pe-panel", PowerEnrichmentPanel).update_data(self.df_wot)
        self.query_one("#actions-panel", ActionItemsPanel).update_data(self.df_all, self.df_wot)
        
        self.update_file_info()
    
    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "load-datalog-btn":
            self.action_load_datalog()
        elif event.button.id == "add-datalog-btn":
            self.action_add_datalog()
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
            self._analyze()
            self.update_status("Refreshed analysis")


def main():
    app = DAMGoodApp()
    app.run()


if __name__ == "__main__":
    main()
