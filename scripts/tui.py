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
    DirectoryTree, Input, RichLog, TextArea
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen
from textual import events
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from pathlib import Path
import pandas as pd
import json
import os
import sys

# Add scripts directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from analyze_datalog import (
    load_datalog, load_config, generate_executive_summary,
    generate_stft_histogram, generate_maf_analysis,
    generate_boost_analysis, generate_pe_analysis,
    generate_action_items, DEFAULT_CONFIG
)


class LoadedFileLabel(Static):
    """A clickable label for loaded files - click to remove."""
    
    def __init__(self, filepath: Path, on_remove: callable, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        self.on_remove = on_remove
        self.update(f"✓ {filepath.name}")
    
    def on_enter(self) -> None:
        """Mouse entered - show remove hint."""
        self.update(f"✕ {self.filepath.name} (click to remove)")
        self.styles.color = "#ff6b35"
    
    def on_leave(self) -> None:
        """Mouse left - restore normal view."""
        self.update(f"✓ {self.filepath.name}")
        self.styles.color = "#00d26a"
    
    def on_click(self) -> None:
        """Remove this file from the analysis."""
        self.on_remove(self.filepath)


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
        
        # Build rich display with controlled column widths
        table = Table(title="Executive Summary", expand=False, box=None, padding=(0, 1))
        table.add_column("Parameter", style="cyan", width=18)
        table.add_column("Value", justify="right", width=10)
        table.add_column("Thresh", justify="center", width=8)
        table.add_column("Status", justify="left", width=14)
        
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


class AIChatScreen(ModalScreen):
    """Modal screen for AI-powered analysis chat."""
    
    BINDINGS = [
        Binding("escape", "close", "Close"),
    ]
    
    def __init__(self, context: str = "", api_key: str = None):
        super().__init__()
        self.context = context
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.messages = []
        self.provider = "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "openai"
    
    def compose(self) -> ComposeResult:
        with Container(id="chat-container"):
            yield Static("🤖 AI Tuning Assistant", id="chat-title")
            yield ScrollableContainer(Static("", id="chat-history"), id="chat-scroll")
            if not self.api_key:
                yield Static("⚠️ No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY env var.", id="api-warning")
                yield Input(placeholder="Or paste API key here...", id="api-key-input", password=True)
            yield Input(placeholder="Ask about your datalog analysis...", id="chat-input")
            with Horizontal(id="chat-buttons"):
                yield Button("Send", id="send-btn", variant="primary")
                yield Button("Close", id="close-btn", variant="default")
    
    def on_mount(self):
        if self.context:
            history = self.query_one("#chat-history", Static)
            history.update(Text("Analysis context loaded. Ask me anything about your datalog!", style="dim"))
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "send-btn":
            self._send_message()
        elif event.button.id == "close-btn":
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "chat-input":
            self._send_message()
        elif event.input.id == "api-key-input":
            self.api_key = event.value
            self.query_one("#api-warning", Static).update("✓ API key set")
    
    def _send_message(self):
        chat_input = self.query_one("#chat-input", Input)
        user_message = chat_input.value.strip()
        
        if not user_message:
            return
        
        chat_input.value = ""
        
        # Check for API key
        if not self.api_key:
            api_input = self.query("#api-key-input")
            if api_input:
                self.api_key = api_input[0].value
        
        if not self.api_key:
            history = self.query_one("#chat-history", Static)
            history.update(Text("Please set an API key first.", style="red"))
            return
        
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message})
        self._update_history()
        
        # Get AI response
        self._get_ai_response(user_message)
    
    def _update_history(self):
        history = self.query_one("#chat-history", Static)
        lines = []
        for msg in self.messages[-10:]:  # Show last 10 messages
            if msg["role"] == "user":
                lines.append(Text(f"You: {msg['content']}\n", style="cyan"))
            else:
                lines.append(Text(f"AI: {msg['content']}\n", style="green"))
        
        combined = Text()
        for line in lines:
            combined.append(line)
        history.update(combined)
    
    def _get_ai_response(self, user_message: str):
        """Get response from AI API."""
        history = self.query_one("#chat-history", Static)
        
        try:
            if "anthropic" in self.api_key.lower()[:10] or self.provider == "anthropic":
                response = self._call_anthropic(user_message)
            else:
                response = self._call_openai(user_message)
            
            self.messages.append({"role": "assistant", "content": response})
            self._update_history()
            
        except Exception as e:
            self.messages.append({"role": "assistant", "content": f"Error: {e}"})
            self._update_history()
    
    def _call_anthropic(self, user_message: str) -> str:
        """Call Anthropic Claude API."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            system_prompt = f"""You are an expert FA20 engine tuner analyzing datalog data. 
You have deep knowledge of fuel trims, knock detection, boost control, and ECU tuning for the 2015-2021 Subaru WRX.

Current analysis context:
{self.context}

Provide specific, actionable tuning advice based on the data. Be concise but thorough."""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": m["role"], "content": m["content"]} for m in self.messages if m["role"] in ["user", "assistant"]]
            )
            return response.content[0].text
        except ImportError:
            return "anthropic package not installed. Run: pip install anthropic"
    
    def _call_openai(self, user_message: str) -> str:
        """Call OpenAI API."""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            system_prompt = f"""You are an expert FA20 engine tuner analyzing datalog data.
You have deep knowledge of fuel trims, knock detection, boost control, and ECU tuning for the 2015-2021 Subaru WRX.

Current analysis context:
{self.context}

Provide specific, actionable tuning advice based on the data. Be concise but thorough."""
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend([{"role": m["role"], "content": m["content"]} for m in self.messages if m["role"] in ["user", "assistant"]])
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except ImportError:
            return "openai package not installed. Run: pip install openai"
    
    def action_close(self):
        self.dismiss(None)


class SaveFileScreen(ModalScreen):
    """Modal screen for choosing save location and filename."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def __init__(self, default_name: str = "export.txt", title: str = "Save As", start_path: str = None):
        super().__init__()
        self.default_name = default_name
        self.title = title
        self.start_path = Path(start_path).expanduser() if start_path else Path.home() / "Documents"
        self.selected_dir = self.start_path
    
    def compose(self) -> ComposeResult:
        with Container(id="save-file-container"):
            yield Static(self.title, id="save-title")
            yield Static(f"📁 {self.start_path}", id="current-dir-label")
            yield DirectoryTree(str(self.start_path), id="save-dir-tree")
            with Horizontal(id="filename-row"):
                yield Static("Filename:", id="filename-label")
                yield Input(value=self.default_name, placeholder="filename", id="save-filename-input")
            with Horizontal(id="save-buttons"):
                yield Button("Save", id="save-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn", variant="default")
    
    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected):
        """Update selected directory."""
        self.selected_dir = event.path
        self.query_one("#current-dir-label", Static).update(f"📁 {event.path}")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "save-btn":
            filename = self.query_one("#save-filename-input", Input).value
            if filename:
                full_path = self.selected_dir / filename
                self.dismiss(full_path)
            else:
                self.dismiss(None)
        elif event.button.id == "cancel-btn":
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted):
        """Handle enter key in input."""
        if event.value:
            full_path = self.selected_dir / event.value
            self.dismiss(full_path)
    
    def action_cancel(self):
        self.dismiss(None)


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
        align: center top;
    }
    
    #sidebar Static {
        width: 100%;
        text-align: center;
    }
    
    #sidebar Button {
        width: 100%;
        text-align: center;
    }
    
    #content {
        width: 1fr;
        max-width: 100%;
        padding: 0 1;
        overflow-x: hidden;
    }
    
    .section-title {
        background: $surface-light;
        color: $accent;
        padding: 0 1;
        margin: 1 0 0 0;
        text-style: bold;
        height: 1;
        text-align: center;
        width: 100%;
    }
    
    #summary-panel {
        height: auto;
        max-height: 10;
        border: solid $border-color;
        margin: 0 0 1 0;
        width: 100%;
    }
    
    #actions-panel {
        height: auto;
        max-height: 10;
        border: solid $border-color;
        margin: 0 0 1 0;
        width: 100%;
    }
    
    DataTable {
        height: auto;
        max-height: 12;
        margin: 0;
        background: $surface;
        width: 100%;
        overflow-x: auto;
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
        width: 100%;
    }
    
    /* Panel containers */
    FuelTrimPanel, BoostPanel, PowerEnrichmentPanel, ActionItemsPanel {
        width: 100%;
        height: auto;
    }
    
    /* Tab content */
    TabPane > * {
        width: 100%;
    }
    
    /* Save file dialog */
    #save-file-container {
        width: 70%;
        height: 70%;
        background: $surface;
        border: solid $accent;
        padding: 1;
    }
    
    #save-title {
        text-align: center;
        text-style: bold;
        background: $accent;
        color: #000;
        padding: 0 1;
        height: 1;
        margin-bottom: 1;
    }
    
    #current-dir-label {
        color: $text-dim;
        height: 1;
        margin-bottom: 1;
    }
    
    #save-dir-tree {
        height: 1fr;
        background: $surface-dark;
        border: solid $border-color;
        margin-bottom: 1;
    }
    
    #filename-row {
        height: 1;
        margin-bottom: 1;
        align: left middle;
    }
    
    #filename-label {
        width: 10;
        color: $text-dim;
    }
    
    #save-filename-input {
        width: 1fr;
        background: $surface-dark;
        border: solid $border-color;
    }
    
    #save-buttons {
        height: 1;
        align: center middle;
    }
    
    #save-buttons Button {
        min-width: 12;
        margin: 0 1;
    }
    
    /* AI Chat dialog */
    #chat-container {
        width: 80%;
        height: 80%;
        background: $surface;
        border: solid $success;
        padding: 1;
    }
    
    #chat-title {
        text-align: center;
        text-style: bold;
        background: $success;
        color: #000;
        padding: 0 1;
        height: 1;
        margin-bottom: 1;
    }
    
    #chat-scroll {
        height: 1fr;
        background: $surface-dark;
        border: solid $border-color;
        margin-bottom: 1;
        padding: 1;
    }
    
    #chat-history {
        width: 100%;
    }
    
    #api-warning {
        color: $warning;
        height: 1;
        margin-bottom: 1;
        text-align: center;
    }
    
    #api-key-input {
        margin-bottom: 1;
    }
    
    #chat-input {
        margin-bottom: 1;
        background: $surface-dark;
        border: solid $border-color;
    }
    
    #chat-buttons {
        height: 1;
        align: center middle;
    }
    
    #chat-buttons Button {
        min-width: 12;
        margin: 0 1;
    }
    """
    
    TITLE = "DAMGood"
    SUB_TITLE = "FA20 Datalog Analyzer"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "load_datalog", "Load"),
        Binding("g", "generate_tables", "Generate"),
        Binding("r", "refresh", "Refresh"),
        Binding("x", "reset", "Reset"),
        Binding("a", "ai_chat", "AI Chat"),
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
                yield Static("")  # Spacer
                yield Button("Load Datalog", id="load-datalog-btn", variant="success")
                yield Button("Add Another", id="add-datalog-btn", variant="default")
                yield Vertical(id="loaded-files-container")
                yield Static("", id="log-type-label")
                yield Static("")  # Spacer
                yield Static("⚡ Actions", classes="section-title")
                yield Static("")  # Spacer
                yield Button("Generate Tables", id="generate-btn", variant="primary")
                yield Button("Export Report", id="export-btn")
                yield Static("")  # Spacer
                yield Static("📊 Status", classes="section-title")
                yield Static("")  # Spacer
                yield Static("Ready", id="status-label")
            
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
        if self.datalogs:
            parts.append(f"Files: {len(self.datalogs)}")
        if self.df_all is not None:
            parts.append(f"Samples: {len(self.df_all)}")
        if hasattr(self, 'log_type') and self.log_type:
            parts.append(f"Type: {self.log_type}")
        info.update(" | ".join(parts) if parts else "No datalogs loaded")
    
    def _validate_and_load(self, path: Path) -> pd.DataFrame:
        """Validate file is a readable CSV and load it."""
        if not path.suffix.lower() == '.csv':
            raise ValueError(f"Invalid format: {path.suffix}. Only CSV files are supported.")
        
        if not path.exists():
            raise ValueError(f"File not found: {path.name}")
        
        try:
            df = load_datalog(str(path))
        except pd.errors.EmptyDataError:
            raise ValueError(f"Empty file: {path.name}")
        except pd.errors.ParserError:
            raise ValueError(f"Invalid CSV format: {path.name}")
        
        if df.empty:
            raise ValueError(f"No data in file: {path.name}")
        
        # Check for required columns
        required_cols = ['Engine - RPM']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns. Is this an Atlas datalog?")
        
        return df
    
    def action_load_datalog(self):
        """Load a datalog file."""
        start_path = self.datalogs[-1].parent if self.datalogs else Path.home()
        
        def handle_result(result):
            if result:
                path = Path(result)
                try:
                    df = self._validate_and_load(path)
                    self.datalogs = [path]  # Reset to single file
                    self._process_datalog(df, path)
                except ValueError as e:
                    self.update_status(f"⚠️ {e}")
                except Exception as e:
                    self.update_status(f"Error loading file: {e}")
        
        self.push_screen(FilePickerScreen(str(start_path)), handle_result)
    
    def action_add_datalog(self):
        """Add another datalog file to the analysis."""
        start_path = self.datalogs[-1].parent if self.datalogs else Path.home()
        
        def handle_result(result):
            if result:
                path = Path(result)
                try:
                    df = self._validate_and_load(path)
                    self.datalogs.append(path)
                    # Merge with existing data
                    if self.df_all is not None:
                        combined = pd.concat([self.df_all, df], ignore_index=True)
                        self._process_datalog(combined, path, append=True)
                    else:
                        self._process_datalog(df, path)
                except ValueError as e:
                    self.update_status(f"⚠️ {e}")
                except Exception as e:
                    self.update_status(f"Error loading file: {e}")
        
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
        
        # Update file labels with clickable items
        self._update_file_list()
        self.query_one("#log-type-label", Static).update(f"Type: {self.log_type}")
        
        # Run analysis
        self._analyze()
        self.update_status(f"Loaded: {len(self.df_all)} samples | {self.log_type}")
    
    def _update_file_list(self):
        """Update the clickable file list in the sidebar."""
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        
        for filepath in self.datalogs:
            label = LoadedFileLabel(filepath, self._remove_datalog)
            container.mount(label)
    
    def _remove_datalog(self, filepath: Path):
        """Remove a datalog file from the analysis."""
        if filepath in self.datalogs:
            self.datalogs.remove(filepath)
            
            if self.datalogs:
                # Reload remaining files
                combined_df = None
                for path in self.datalogs:
                    df = load_datalog(str(path))
                    if combined_df is None:
                        combined_df = df
                    else:
                        combined_df = pd.concat([combined_df, df], ignore_index=True)
                
                self.log_type, self.df_all, self.df_wot = self._detect_log_type(combined_df)
                self._update_file_list()
                self.query_one("#log-type-label", Static).update(f"Type: {self.log_type}")
                self._analyze()
                self.update_status(f"Removed {filepath.name} | {len(self.df_all)} samples remaining")
            else:
                # No files left
                self.df_all = None
                self.df_wot = None
                self.log_type = "Unknown"
                self._update_file_list()
                self.query_one("#log-type-label", Static).update("")
                self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
                self.update_status("All datalogs removed")
    
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
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        default_folder = f"tables_{timestamp}"
        
        def handle_save(result):
            if result:
                save_dir = Path(result).parent / Path(result).stem  # Use as folder name
                try:
                    from analyze_datalog import generate_revised_tables
                    generate_revised_tables(self.df_all, self.df_wot, str(save_dir))
                    self.update_status(f"✓ Tables saved to {save_dir}")
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(
            SaveFileScreen(
                default_name=default_folder,
                title="Save Tables To",
                start_path=str(Path.home() / "Documents")
            ),
            handle_save
        )
    
    def action_export_report(self):
        """Export full text report."""
        if self.df_all is None:
            self.update_status("Load a datalog first!")
            return
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        default_name = f"FA20_Report_{timestamp}.txt"
        
        def handle_save(result):
            if result:
                output_path = Path(result)
                try:
                    from analyze_datalog import generate_report
                    generate_report(self.df_all, self.df_wot, output_path, self.config)
                    self.update_status(f"✓ Report saved to {output_path}")
                except Exception as e:
                    self.update_status(f"Error: {e}")
        
        self.push_screen(
            SaveFileScreen(
                default_name=default_name,
                title="Export Report",
                start_path=str(Path.home() / "Documents")
            ),
            handle_save
        )
    
    def action_refresh(self):
        """Refresh the analysis."""
        if self.df_all is not None:
            self._analyze()
            self.update_status("Refreshed analysis")
    
    def action_reset(self):
        """Reset everything back to default state."""
        self.datalogs = []
        self.df_all = None
        self.df_wot = None
        self.log_type = "Unknown"
        
        # Clear file list
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        
        # Reset labels
        self.query_one("#log-type-label", Static).update("")
        self.query_one("#file-info", Static).update("No datalogs loaded")
        self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
        
        self.update_status("Reset complete - Ready")
    
    def action_ai_chat(self):
        """Open AI chat for detailed analysis."""
        if self.df_all is None:
            self.update_status("Load a datalog first to chat with AI")
            return
        
        # Build context from current analysis
        context_parts = []
        context_parts.append(f"Log type: {self.log_type}")
        context_parts.append(f"Total samples: {len(self.df_all)}")
        
        # Add executive summary
        summary = generate_executive_summary(self.df_all, self.config)
        context_parts.append("\nExecutive Summary:")
        for _, row in summary.iterrows():
            context_parts.append(f"  {row['Parameter']}: {row['Value']} ({row['Status']})")
        
        # Add key stats
        if 'Ignition - Dynamic Advance Multiplier' in self.df_all.columns:
            dam_min = self.df_all['Ignition - Dynamic Advance Multiplier'].min()
            context_parts.append(f"\nDAM minimum: {dam_min:.2f}")
        
        if 'Ignition - Feedback Knock' in self.df_all.columns:
            fbk_min = self.df_all['Ignition - Feedback Knock'].min()
            context_parts.append(f"Feedback Knock minimum: {fbk_min:.2f}°")
        
        if 'Fuel - Command - Corrections - AF Correction STFT' in self.df_all.columns:
            stft_mean = self.df_all['Fuel - Command - Corrections - AF Correction STFT'].mean()
            stft_min = self.df_all['Fuel - Command - Corrections - AF Correction STFT'].min()
            stft_max = self.df_all['Fuel - Command - Corrections - AF Correction STFT'].max()
            context_parts.append(f"STFT: mean={stft_mean:.1f}%, range=[{stft_min:.1f}%, {stft_max:.1f}%]")
        
        if 'Analytical - Boost Pressure' in self.df_all.columns:
            boost_max = self.df_all['Analytical - Boost Pressure'].max()
            context_parts.append(f"Peak boost: {boost_max:.1f} psi")
        
        context = "\n".join(context_parts)
        
        self.push_screen(AIChatScreen(context=context))


def main():
    app = DAMGoodApp()
    app.run()


if __name__ == "__main__":
    main()
