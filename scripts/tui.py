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

import logging
from textual.logging import TextualHandler

# Set up debug logging to BOTH file and Textual console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/damgood_debug.log', mode='w'),
        TextualHandler(),  # This sends logs to `textual console`
    ]
)
logger = logging.getLogger('DAMGood')
from api_keys import get_api_key, save_api_key, detect_provider_from_key, is_keyring_available
from session import TuningSession, PhaseAnalysis


class PhaseLabel(Static):
    """Clickable label for a tuning phase."""
    
    def __init__(self, phase_num: int, on_select: callable, is_active: bool = False, summary: str = "", **kwargs):
        super().__init__(**kwargs)
        self.phase_num = phase_num
        self.on_select = on_select
        self.is_active = is_active
        self.summary = summary
        self._render_label()
    
    def _render_label(self):
        prefix = "▶" if self.is_active else " "
        label = f"{prefix} Phase {self.phase_num}"
        if self.summary:
            label += f" ({self.summary})"
        self.update(label)
        if self.is_active:
            self.styles.color = "#ffd700"
            self.styles.text_style = "bold"
        else:
            self.styles.color = "#8899aa"
            self.styles.text_style = "none"
    
    def set_active(self, active: bool):
        self.is_active = active
        self._render_label()
    
    def on_click(self) -> None:
        self.on_select(self.phase_num)


class LoadedFileLabel(Static):
    """A clickable label for loaded files - styled like a button."""
    
    DEFAULT_CSS = """
    LoadedFileLabel {
        width: 100%;
        height: 1;
        padding: 0 1;
        background: #21262d;
        color: #8899aa;
        text-align: left;
        margin-bottom: 0;
    }
    LoadedFileLabel.active {
        background: #003366;
        color: #ffd700;
        text-style: bold;
    }
    LoadedFileLabel:hover {
        background: #00d26a;
        color: #000;
    }
    """
    
    def __init__(self, filepath: Path, is_active: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.filepath = Path(filepath)  # Ensure it's a Path
        self.is_active = is_active
        self._render_label()
    
    def _render_label(self):
        """Render the label based on state."""
        name = self.filepath.name
        if len(name) > 20:
            name = name[:17] + "..."
        if self.is_active:
            self.update(f"▶ {name}")
            self.add_class("active")
        else:
            self.update(f"  {name}")
            self.remove_class("active")
    
    def set_active(self, active: bool):
        """Set the active state of this label."""
        self.is_active = active
        self._render_label()
    
    def on_click(self, event) -> None:
        """Handle click on this label."""
        # Let the app handle this - post to parent
        if event.shift:
            self.app._remove_datalog(self.filepath)
        else:
            self.app._select_view(self.filepath)
        event.stop()


class AllCombinedLabel(Static):
    """Clickable label for 'All Combined' view."""
    
    def __init__(self, on_click_callback: callable, **kwargs):
        super().__init__(**kwargs)
        self.on_click_callback = on_click_callback
        self.is_active = True
        self._render_label()
    
    def _render_label(self):
        if self.is_active:
            self.update("▶ All Combined")
            self.styles.color = "#ffd700"
            self.styles.text_style = "bold"
        else:
            self.update("  All Combined")
            self.styles.color = "#8899aa"
            self.styles.text_style = "none"
    
    def set_active(self, active: bool):
        self.is_active = active
        self._render_label()
    
    def on_click(self) -> None:
        self.on_click_callback()


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
    """Executive summary panel showing key health metrics in organized sections."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
    
    def compose(self) -> ComposeResult:
        yield Static("Load a datalog to see analysis", id="summary-content")
    
    def _get_status_style(self, status: str) -> str:
        """Get the style for a status value."""
        if '✅' in status:
            return "green"
        elif '⚠️' in status:
            return "yellow"
        elif '📊' in status:
            return "dim cyan"
        else:
            return "red"
    
    def _create_section_table(self, title: str, rows: list, show_header: bool = True) -> Table:
        """Create a formatted section table."""
        from rich.box import SIMPLE
        table = Table(
            title=f"[bold cyan]{title}[/]" if title else None,
            expand=True,
            box=SIMPLE,
            padding=(0, 1),
            show_header=show_header,
            header_style="bold dim"
        )
        table.add_column("Parameter", style="white", width=18)
        table.add_column("Value", justify="right", style="bright_white", width=16)
        table.add_column("Thresh", justify="center", style="dim", width=8)
        table.add_column("Status", justify="left", width=14)
        
        for row in rows:
            status = str(row['Status'])
            style = self._get_status_style(status)
            table.add_row(
                str(row['Parameter']),
                str(row['Value']),
                str(row['Threshold']),
                Text(status, style=style)
            )
        return table
    
    def update_data(self, df: pd.DataFrame, config: dict):
        """Update the summary with new datalog data organized by section."""
        from rich.console import Group
        from rich.rule import Rule
        
        logger.info(f"SummaryPanel.update_data called with df of {len(df)} rows")
        
        self.data = generate_executive_summary(df, config)
        logger.info(f"SummaryPanel: Generated {len(self.data)} summary rows")
        
        content = self.query_one("#summary-content", Static)
        logger.info(f"SummaryPanel: Found content widget: {content}")
        
        # Categorize rows by section
        safety_params = ['DAM (min)', 'DAM (avg)', 'Feedback Knock', 'Knock Events', 'Fine Knock Learn']
        fuel_params = ['STFT (avg)', 'STFT (range)', 'LTFT (avg)', 'Combined Trim']
        boost_params = ['Peak Boost', 'Avg Boost']
        afr_params = ['WOT AFR', 'WOT Lambda']
        info_params = ['MAF Max', 'Total Samples']
        
        safety_rows = []
        fuel_rows = []
        boost_rows = []
        afr_rows = []
        info_rows = []
        
        for _, row in self.data.iterrows():
            param = row['Parameter']
            row_dict = row.to_dict()
            if param in safety_params:
                safety_rows.append(row_dict)
            elif param in fuel_params:
                fuel_rows.append(row_dict)
            elif param in boost_params:
                boost_rows.append(row_dict)
            elif param in afr_params:
                afr_rows.append(row_dict)
            elif param in info_params:
                info_rows.append(row_dict)
        
        # Build grouped display with sections
        sections = []
        
        if safety_rows:
            sections.append(self._create_section_table("🔒 IGNITION / KNOCK", safety_rows))
        
        if fuel_rows:
            sections.append(self._create_section_table("⛽ FUEL TRIMS", fuel_rows, show_header=False))
        
        if boost_rows:
            sections.append(self._create_section_table("💨 BOOST", boost_rows, show_header=False))
        
        if afr_rows:
            sections.append(self._create_section_table("🔥 WOT FUELING", afr_rows, show_header=False))
        
        if info_rows:
            sections.append(self._create_section_table("📊 INFO", info_rows, show_header=False))
        
        # Combine all sections and force refresh
        logger.info(f"SummaryPanel: Built {len(sections)} sections, calling update()")
        content.update(Group(*sections))
        logger.info("SummaryPanel: Called content.update(), now calling refresh()")
        content.refresh()
        self.refresh()
        logger.info("SummaryPanel: update_data complete")


class FuelTrimPanel(Static):
    """Fuel trim analysis panel with STFT histogram and MAF breakdown."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("STFT Distribution", classes="section-title")
            yield DataTable(id="stft-table", zebra_stripes=True)
            yield Static("Fuel Trim by MAF Range", classes="section-title")
            yield DataTable(id="maf-table", zebra_stripes=True)
    
    def _repopulate_table(self, table: DataTable, columns: list, rows: list, table_name: str = ""):
        """Safely repopulate a DataTable - clear, add columns/rows, and force refresh."""
        logger.debug(f"FuelTrimPanel._repopulate_table({table_name}): clearing, cols={columns}, rows={len(rows)}")
        table.clear(columns=True)
        if columns:
            table.add_columns(*columns)
            logger.debug(f"FuelTrimPanel._repopulate_table({table_name}): added {len(columns)} columns")
        for row in rows:
            table.add_row(*row)
        logger.debug(f"FuelTrimPanel._repopulate_table({table_name}): added {len(rows)} rows, calling refresh")
        table.refresh(layout=True)
        logger.debug(f"FuelTrimPanel._repopulate_table({table_name}): refresh complete")
    
    def update_data(self, df: pd.DataFrame):
        """Update fuel trim tables with datalog data."""
        logger.info(f"FuelTrimPanel.update_data called with df of {len(df)} rows")
        
        # STFT Histogram
        stft_data = generate_stft_histogram(df)
        stft_rows = [
            (row['Range'], str(row['Count']), f"{row['Pct']}%", row['Histogram'])
            for _, row in stft_data.iterrows()
        ]
        logger.info(f"FuelTrimPanel: Generated {len(stft_rows)} STFT rows")
        self._repopulate_table(
            self.query_one("#stft-table", DataTable),
            ["Range", "Count", "Pct", "Distribution"],
            stft_rows,
            "stft-table"
        )
        
        # MAF Analysis
        maf_data = generate_maf_analysis(df)
        logger.info(f"FuelTrimPanel: Generated MAF data, empty={maf_data.empty}")
        if not maf_data.empty:
            maf_rows = [
                (row['MAF Range'], row['STFT'], row['LTFT'], row['Combined'], row['Status'], str(row['Samples']))
                for _, row in maf_data.iterrows()
            ]
            self._repopulate_table(
                self.query_one("#maf-table", DataTable),
                ["MAF Range", "STFT", "LTFT", "Combined", "Status", "Samples"],
                maf_rows,
                "maf-table"
            )
        else:
            self._repopulate_table(self.query_one("#maf-table", DataTable), [], [], "maf-table")
        
        logger.info("FuelTrimPanel.update_data complete")


class BoostPanel(Static):
    """Boost control analysis panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Boost Distribution", classes="section-title")
            yield DataTable(id="boost-dist-table", zebra_stripes=True)
            yield Static("WOT Performance", classes="section-title")
            yield DataTable(id="wot-stats-table", zebra_stripes=True)
    
    def _repopulate_table(self, table: DataTable, columns: list, rows: list):
        """Safely repopulate a DataTable - clear, add columns/rows, and force refresh."""
        table.clear(columns=True)
        if columns:
            table.add_columns(*columns)
        for row in rows:
            table.add_row(*row)
        table.refresh(layout=True)
    
    def update_data(self, df_wot: pd.DataFrame):
        """Update boost tables with WOT datalog data."""
        boost_dist, wot_stats = generate_boost_analysis(df_wot)
        
        # Boost distribution
        if boost_dist is not None and not boost_dist.empty:
            dist_rows = [
                (row['Range'], str(row['Count']), row['Histogram'])
                for _, row in boost_dist.iterrows()
            ]
            self._repopulate_table(
                self.query_one("#boost-dist-table", DataTable),
                ["Range", "Count", "Distribution"],
                dist_rows
            )
        else:
            self._repopulate_table(self.query_one("#boost-dist-table", DataTable), [], [])
        
        # WOT stats
        if wot_stats is not None and not wot_stats.empty:
            stats_rows = [
                (row['Metric'], str(row['Value']))
                for _, row in wot_stats.iterrows()
            ]
            self._repopulate_table(
                self.query_one("#wot-stats-table", DataTable),
                ["Metric", "Value"],
                stats_rows
            )
        else:
            self._repopulate_table(self.query_one("#wot-stats-table", DataTable), [], [])


class PowerEnrichmentPanel(Static):
    """Power enrichment (WOT fueling) analysis panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("AFR by RPM (WOT, Load > 80%)", classes="section-title")
            yield DataTable(id="pe-table", zebra_stripes=True)
    
    def _repopulate_table(self, table: DataTable, columns: list, rows: list):
        """Safely repopulate a DataTable - clear, add columns/rows, and force refresh."""
        table.clear(columns=True)
        if columns:
            table.add_columns(*columns)
        for row in rows:
            table.add_row(*row)
        table.refresh(layout=True)
    
    def update_data(self, df_wot: pd.DataFrame):
        """Update PE table with WOT datalog data."""
        pe_data = generate_pe_analysis(df_wot)
        
        if pe_data is not None and not pe_data.empty:
            pe_rows = [
                (row['RPM'], row['Lambda'], row['AFR'], row['STFT'], row['Status'])
                for _, row in pe_data.iterrows()
            ]
            self._repopulate_table(
                self.query_one("#pe-table", DataTable),
                ["RPM", "Lambda", "AFR", "STFT", "Status"],
                pe_rows
            )
        else:
            self._repopulate_table(self.query_one("#pe-table", DataTable), [], [])


class ActionItemsPanel(Static):
    """Action items and recommendations panel."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Action Items", classes="section-title")
            yield DataTable(id="actions-table", zebra_stripes=True)
    
    def _repopulate_table(self, table: DataTable, columns: list, rows: list):
        """Safely repopulate a DataTable - clear, add columns/rows, and force refresh."""
        table.clear(columns=True)
        if columns:
            table.add_columns(*columns)
        for row in rows:
            table.add_row(*row)
        table.refresh(layout=True)
    
    def update_data(self, df_all: pd.DataFrame, df_wot: pd.DataFrame):
        """Update action items table."""
        actions = generate_action_items(df_all, df_wot)
        
        action_rows = [
            (str(row['Priority']), row['Category'], row['Item'], row['Status'])
            for _, row in actions.iterrows()
        ]
        self._repopulate_table(
            self.query_one("#actions-table", DataTable),
            ["Priority", "Category", "Item", "Status"],
            action_rows
        )


class AIChatScreen(ModalScreen):
    """Modal screen for AI-powered analysis chat."""
    
    BINDINGS = [
        Binding("escape", "close", "Close"),
    ]
    
    def __init__(self, context: str = "", api_key: str = None):
        super().__init__()
        self.context = context
        self.messages = []
        self.key_was_manually_entered = False
        
        # Try to get API key from secure storage or env
        stored_key, stored_provider = get_api_key()
        self.api_key = api_key or stored_key
        self.provider = stored_provider or "anthropic"
    
    def compose(self) -> ComposeResult:
        with Container(id="chat-container"):
            yield Static("🤖 AI Tuning Assistant", id="chat-title")
            yield ScrollableContainer(Static("", id="chat-history"), id="chat-scroll")
            if not self.api_key:
                if is_keyring_available():
                    yield Static("⚠️ No API key found. Enter your key below (will be saved securely).", id="api-warning")
                else:
                    yield Static("⚠️ No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY env var.", id="api-warning")
                yield Input(placeholder="Paste API key here (sk-ant-... or sk-...)...", id="api-key-input", password=True)
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
            self.key_was_manually_entered = True
            
            # Detect provider from key format
            detected = detect_provider_from_key(event.value)
            if detected:
                self.provider = detected
            
            # Try to save to secure storage
            if is_keyring_available() and self.provider:
                if save_api_key(self.provider, event.value):
                    self.query_one("#api-warning", Static).update(f"✓ API key saved securely ({self.provider})")
                else:
                    self.query_one("#api-warning", Static).update(f"✓ API key set ({self.provider}) - could not save to keyring")
            else:
                self.query_one("#api-warning", Static).update(f"✓ API key set ({self.provider})")
    
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


class ConfirmScreen(ModalScreen):
    """Simple confirmation dialog."""
    
    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
    }
    #confirm-container {
        width: 50;
        height: auto;
        background: #1c2128;
        border: solid #003366;
        padding: 1 2;
    }
    #confirm-title {
        text-align: center;
        text-style: bold;
        color: #ffd700;
        margin-bottom: 1;
    }
    #confirm-message {
        text-align: center;
        margin-bottom: 1;
    }
    #confirm-hint {
        text-align: center;
        color: #666;
        text-style: italic;
        margin-bottom: 1;
    }
    #confirm-buttons {
        align: center middle;
        height: 3;
    }
    #confirm-buttons Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "confirm", "Confirm"),
    ]
    
    def __init__(self, title: str, message: str, hint: str = ""):
        super().__init__()
        self.title_text = title
        self.message_text = message
        self.hint_text = hint
    
    def compose(self) -> ComposeResult:
        with Container(id="confirm-container"):
            yield Static(self.title_text, id="confirm-title")
            yield Static(self.message_text, id="confirm-message")
            if self.hint_text:
                yield Static(self.hint_text, id="confirm-hint")
            with Horizontal(id="confirm-buttons"):
                yield Button("Yes", id="yes-btn", variant="error")
                yield Button("No", id="no-btn", variant="success")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "yes-btn":
            self.dismiss(True)
        else:
            self.dismiss(False)
    
    def action_cancel(self):
        self.dismiss(False)
    
    def action_confirm(self):
        self.dismiss(True)


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


class PhaseSelectScreen(ModalScreen):
    """Modal screen for selecting a saved phase to view."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def __init__(self, phases: list, on_select: callable):
        super().__init__()
        self.phases = phases
        self.on_select = on_select
    
    def compose(self) -> ComposeResult:
        with Container(id="phase-select-container"):
            yield Static("📋 Select Phase", id="phase-select-title")
            yield Static("")
            with Vertical(id="phase-list"):
                for phase in self.phases:
                    btn = Button(
                        f"Phase {phase.phase_number} - {phase.samples} samples ({phase.log_type})",
                        id=f"phase-{phase.phase_number}",
                        variant="default"
                    )
                    yield btn
            yield Static("")
            yield Button("Cancel", id="cancel-btn", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cancel-btn":
            self.dismiss(None)
        elif event.button.id.startswith("phase-"):
            phase_num = int(event.button.id.split("-")[1])
            self.dismiss(None)
            self.on_select(phase_num)
    
    def action_cancel(self):
        self.dismiss(None)


class DAMGoodApp(App):
    """DAMGood - FA20 Datalog Analyzer TUI."""
    
    CSS = """
    /* DAMGood Theme - World Rally Blue (Subaru) */
    $accent: #003366;
    $accent-dim: #002244;
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
        border-top: solid $accent;
        padding: 0 1;
    }
    
    #status-label {
        color: $text-dim;
        height: auto;
        margin-bottom: 1;
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
        max-height: 22;
        border: solid $border-color;
        margin: 0 0 1 0;
        width: 100%;
        overflow-y: auto;
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
        background: $success;
        color: #000;
    }
    
    Button:focus {
        text-style: bold;
    }
    
    #load-datalog-btn {
        margin-bottom: 1;
    }
    
    #add-datalog-btn {
        margin-bottom: 1;
    }
    
    #loaded-files-label {
        color: $success;
        height: auto;
    }
    
    #file-help-label {
        color: #555555;
        text-style: italic;
        height: 2;
        text-align: left;
        padding: 0 1;
        margin-top: 1;
    }
    
    #log-type-label {
        color: $warning;
        height: 1;
        margin-top: 1;
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
    FuelTrimPanel, BoostPanel, PowerEnrichmentPanel {
        width: 100%;
        height: auto;
    }
    
    #actions-panel {
        width: 100%;
        height: 10;
        min-height: 8;
        border-top: solid $border-color;
        padding: 0 1;
        background: $surface;
        dock: bottom;
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
        self.datalog_dfs = {}  # Dict mapping filepath -> (df, log_type)
        self.df_all = None  # Combined or single-file view
        self.df_wot = None  # Auto-detected WOT portions
        self.config = load_config(None)
        self.log_type = "Unknown"  # Will be auto-detected
        self.active_view = None  # Path to currently viewed file
        
        # Session/phase tracking
        self.session = TuningSession()
        self.current_phase_dfs = {}  # Dataframes for current phase being built
        self.phase_committed = False  # True once phase is finalized
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="main-container"):
            # Sidebar
            with Vertical(id="sidebar"):
                # Datalogs section
                yield Static("📁 Datalogs", classes="section-title")
                yield Static("", id="phase-info-label")
                yield Button("Load Datalog", id="load-datalog-btn", variant="success")
                yield Button("Add Another", id="add-datalog-btn", variant="default", disabled=True)
                yield Vertical(id="loaded-files-container")
                yield Static("click: view\nshift+click: remove", id="file-help-label")
                yield Static("", id="log-type-label")
                
                # Phase management
                yield Static("📋 Phases", classes="section-title")
                yield Static("")  # Spacer
                yield Button("Save → Phase 1", id="save-phase-btn", variant="default", disabled=True)
                yield Button("Select Phase", id="select-phase-btn", variant="default", disabled=True)
                yield Static("")  # Spacer
                
                # Table generation
                yield Static("📊 Output", classes="section-title")
                yield Static("")  # Spacer
                yield Button("Generate Tables", id="generate-btn", variant="default", disabled=True)
                yield Button("Export Report", id="export-btn", variant="default", disabled=True)
                yield Static("")  # Spacer
                
                # Session management
                yield Static("💾 Session", classes="section-title")
                yield Static("")  # Spacer
                yield Button("Save Session", id="save-session-btn", variant="default", disabled=True)
                yield Button("Load Session", id="load-session-btn", variant="default")
                yield Static("")  # Spacer
                
                # Status
                yield Static("📡 Status", classes="section-title")
                yield Static("")  # Spacer
                yield Static("Ready", id="status-label")
            
            # Main content with tabs
            with Vertical(id="content"):
                yield Static("", id="file-info")
                
                with TabbedContent():
                    with TabPane("Summary", id="tab-summary"):
                        yield SummaryPanel(id="summary-panel")
                    
                    with TabPane("Fuel Trims", id="tab-fuel"):
                        with ScrollableContainer():
                            yield FuelTrimPanel(id="fuel-panel")
                    
                    with TabPane("Boost", id="tab-boost"):
                        with ScrollableContainer():
                            yield BoostPanel(id="boost-panel")
                    
                    with TabPane("Power Enrichment", id="tab-pe"):
                        with ScrollableContainer():
                            yield PowerEnrichmentPanel(id="pe-panel")
                
                # Action items shown below all tabs
                yield ActionItemsPanel(id="actions-panel")
        
        yield Footer()
    
    def on_mount(self):
        """Called when app is mounted."""
        self.update_status("Ready - Press 'L' to load datalog")
        # Initialize phase display
        self._update_phase_display()
    
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
            parts.append(f"Active: {self.log_type}")
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
        # If files already loaded, confirm overwrite
        if self.datalogs:
            def handle_confirm(confirmed: bool):
                if confirmed:
                    self._do_load_datalog()
            
            self.push_screen(
                ConfirmScreen(
                    "⚠️ Replace existing logs?",
                    "This will clear all currently loaded datalogs.",
                    "Tip: Use 'Add Another' to keep existing logs."
                ),
                handle_confirm
            )
        else:
            self._do_load_datalog()
    
    def _do_load_datalog(self):
        """Actually load the datalog file."""
        start_path = self.datalogs[-1].parent if self.datalogs else Path.home()
        
        def handle_result(result):
            if result:
                path = Path(result)
                try:
                    df = self._validate_and_load(path)
                    self.datalogs = [path]  # Reset to single file
                    self.datalog_dfs = {}  # Clear stored dataframes
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
                    
                    # Store this file's individual dataframe
                    log_type, _, df_wot = self._detect_log_type(df)
                    self.datalog_dfs[path] = (df, log_type, df_wot)
                    
                    # Rebuild combined view but keep focus on individual file
                    self._rebuild_combined_view()
                    self.active_view = path  # Focus on the newly added file
                    self.df_all = df
                    self.df_wot = df_wot
                    self.log_type = log_type
                    
                    # Enable buttons
                    self.query_one("#add-datalog-btn", Button).disabled = False
                    self.query_one("#generate-btn", Button).disabled = False
                    self.query_one("#export-btn", Button).disabled = False
                    
                    self._update_file_list()
                    self.query_one("#log-type-label", Static).update(f"Active: {self.log_type}")
                    self._analyze()
                    self.update_status(f"Added: {path.name} | {len(self.df_all)} total samples")
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
        # Store individual dataframe with its detected type
        log_type, _, df_wot = self._detect_log_type(df)
        self.datalog_dfs[path] = (df, log_type, df_wot)
        
        # Always focus on the individual file just loaded
        self.active_view = path
        self.df_all = df
        self.df_wot = df_wot
        self.log_type = log_type
        
        # Enable buttons now that we have data
        # Swap button emphasis: Add Another is now primary action
        self.query_one("#load-datalog-btn", Button).variant = "default"
        add_btn = self.query_one("#add-datalog-btn", Button)
        add_btn.disabled = False
        add_btn.variant = "success"
        self.query_one("#generate-btn", Button).disabled = False
        self.query_one("#export-btn", Button).disabled = False
        
        # Update file labels with clickable items
        self._update_file_list()
        
        # Run analysis
        self._analyze()
        self.update_status(f"Loaded: {path.name} | {len(self.df_all)} samples | {self.log_type}")
    
    def _rebuild_combined_view(self):
        """Rebuild the combined dataframe from all loaded datalogs."""
        if not self.datalog_dfs:
            self.df_all = None
            self.df_wot = None
            self.log_type = "Unknown"
            return
        
        combined_df = pd.concat([df for df, _, _ in self.datalog_dfs.values()], ignore_index=True)
        self.log_type, self.df_all, self.df_wot = self._detect_log_type(combined_df)
    
    def _select_view(self, filepath):
        """Select a specific datalog to view."""
        logger.info(f"_select_view called with: {filepath}")
        
        # Ensure filepath is a Path object for consistent comparison
        filepath = Path(filepath) if not isinstance(filepath, Path) else filepath
        
        # Skip if already viewing this file (compare resolved paths)
        if self.active_view is not None and Path(self.active_view).resolve() == filepath.resolve():
            logger.info(f"_select_view: Already viewing this file, skipping")
            return
        
        # Find the matching key in datalog_dfs (Path comparison can be tricky)
        matching_key = None
        for key in self.datalog_dfs:
            if Path(key).resolve() == filepath.resolve():
                matching_key = key
                break
        
        logger.info(f"_select_view: matching_key={matching_key}")
        
        if matching_key is not None:
            self.active_view = matching_key
            df, log_type, df_wot = self.datalog_dfs[matching_key]
            self.df_all = df
            self.df_wot = df_wot
            self.log_type = log_type
            logger.info(f"_select_view: Loaded df with {len(df)} rows, log_type={log_type}")
            
            # Update UI without recreating all labels - just update active states
            try:
                container = self.query_one("#loaded-files-container", Vertical)
                for label in container.children:
                    if isinstance(label, LoadedFileLabel):
                        is_match = Path(label.filepath).resolve() == Path(matching_key).resolve()
                        label.set_active(is_match)
            except Exception as e:
                logger.error(f"_select_view: Error updating labels: {e}")
            
            self.query_one("#log-type-label", Static).update(f"Active: {self.log_type}")
            logger.info("_select_view: Calling _analyze()")
            self._analyze()
            self.update_status(f"Viewing: {filepath.name} | {len(self.df_all)} samples")
        else:
            logger.warning(f"_select_view: No matching key found for {filepath}")
    
    def _update_file_list(self):
        """Update the clickable file list in the sidebar."""
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        
        for filepath in self.datalogs:
            is_active = (self.active_view is not None and 
                        Path(self.active_view).resolve() == Path(filepath).resolve())
            label = LoadedFileLabel(filepath, is_active=is_active)
            container.mount(label)
    
    def _remove_datalog(self, filepath: Path):
        """Remove a datalog file from the analysis."""
        if filepath in self.datalogs:
            self.datalogs.remove(filepath)
            
            # Remove from stored dataframes
            if filepath in self.datalog_dfs:
                del self.datalog_dfs[filepath]
            
            if self.datalogs:
                # If we were viewing the removed file, switch to first remaining file
                if self.active_view == filepath:
                    self.active_view = self.datalogs[0]
                    df, log_type, df_wot = self.datalog_dfs[self.active_view]
                    self.df_all = df
                    self.df_wot = df_wot
                    self.log_type = log_type
                
                self._update_file_list()
                self.query_one("#log-type-label", Static).update(f"Active: {self.log_type}")
                self._analyze()
                self.update_status(f"Removed {filepath.name} | {len(self.df_all)} samples remaining")
            else:
                # No files left
                self.df_all = None
                self.df_wot = None
                self.log_type = "Unknown"
                self.active_view = None
                self._update_file_list()
                self.query_one("#log-type-label", Static).update("")
                self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
                self.update_status("All datalogs removed")
    
    def _analyze(self):
        """Run analysis on loaded data and update all panels."""
        logger.info(f"_analyze called. df_all is None: {self.df_all is None}")
        if self.df_all is None:
            logger.warning("_analyze: df_all is None, returning early")
            return
        
        logger.info(f"_analyze: df_all has {len(self.df_all)} rows, df_wot has {len(self.df_wot) if self.df_wot is not None else 0} rows")
        
        # Update all panels with try/except to catch errors
        try:
            logger.info("_analyze: Updating summary-panel")
            self.query_one("#summary-panel", SummaryPanel).update_data(self.df_all, self.config)
            logger.info("_analyze: summary-panel updated successfully")
        except Exception as e:
            logger.error(f"_analyze: Error updating summary-panel: {e}", exc_info=True)
        
        try:
            logger.info("_analyze: Updating fuel-panel")
            self.query_one("#fuel-panel", FuelTrimPanel).update_data(self.df_all)
            logger.info("_analyze: fuel-panel updated successfully")
        except Exception as e:
            logger.error(f"_analyze: Error updating fuel-panel: {e}", exc_info=True)
        
        try:
            logger.info("_analyze: Updating boost-panel")
            self.query_one("#boost-panel", BoostPanel).update_data(self.df_wot)
            logger.info("_analyze: boost-panel updated successfully")
        except Exception as e:
            logger.error(f"_analyze: Error updating boost-panel: {e}", exc_info=True)
        
        try:
            logger.info("_analyze: Updating pe-panel")
            self.query_one("#pe-panel", PowerEnrichmentPanel).update_data(self.df_wot)
            logger.info("_analyze: pe-panel updated successfully")
        except Exception as e:
            logger.error(f"_analyze: Error updating pe-panel: {e}", exc_info=True)
        
        try:
            logger.info("_analyze: Updating actions-panel")
            self.query_one("#actions-panel", ActionItemsPanel).update_data(self.df_all, self.df_wot)
            logger.info("_analyze: actions-panel updated successfully")
        except Exception as e:
            logger.error(f"_analyze: Error updating actions-panel: {e}", exc_info=True)
        
        self.update_file_info()
        self._update_phase_display()
        logger.info("_analyze: Complete")
    
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
        elif event.button.id == "save-phase-btn":
            self._save_phase_and_continue()
        elif event.button.id == "select-phase-btn":
            self._show_phase_selector()
        elif event.button.id == "save-session-btn":
            self.action_save_session()
        elif event.button.id == "load-session-btn":
            self.action_load_session()
    
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
        self.datalog_dfs = {}
        self.df_all = None
        self.df_wot = None
        self.log_type = "Unknown"
        self.active_view = None
        
        # Clear file list
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        
        # Disable buttons and reset variants
        self.query_one("#load-datalog-btn", Button).variant = "success"
        add_btn = self.query_one("#add-datalog-btn", Button)
        add_btn.disabled = True
        add_btn.variant = "default"
        self.query_one("#generate-btn", Button).disabled = True
        self.query_one("#export-btn", Button).disabled = True
        
        # Reset labels
        self.query_one("#log-type-label", Static).update("")
        self.query_one("#file-info", Static).update("")
        self.query_one("#phase-info-label", Static).update("")
        self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
        
        # Clear action items table
        actions_table = self.query_one("#actions-panel", ActionItemsPanel).query_one("#actions-table", DataTable)
        actions_table.clear(columns=True)
        
        # Reset session/phase state
        self.session = TuningSession()
        self.current_phase_dfs = {}
        self.phase_committed = False
        self._update_phase_display()
        
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
    
    # ========== Phase/Session Management ==========
    
    def _update_phase_display(self):
        """Update the phase info and button states."""
        next_phase = self.session.next_phase_number
        
        # Update phase info label
        info_label = self.query_one("#phase-info-label", Static)
        if self.session.phases:
            info_label.update(f"Phase {len(self.session.phases)} saved")
        else:
            info_label.update("")
        
        # Update button states and labels
        self._update_phase_buttons()
    
    def _update_phase_buttons(self):
        """Update phase-related button states."""
        has_data = self.df_all is not None
        has_phases = len(self.session.phases) > 0
        next_phase = self.session.next_phase_number
        
        # Save phase button: enabled when we have uncommitted data
        save_btn = self.query_one("#save-phase-btn", Button)
        save_btn.disabled = not has_data or self.phase_committed
        save_btn.label = f"Save → Phase {next_phase}"
        
        # Select phase button: enabled when we have saved phases
        select_btn = self.query_one("#select-phase-btn", Button)
        select_btn.disabled = not has_phases
        
        # Save session: enabled when we have any committed phases
        session_btn = self.query_one("#save-session-btn", Button)
        session_btn.disabled = not has_phases
    
    def _select_phase(self, phase_num: int):
        """Switch to viewing a specific phase."""
        phase = self.session.get_phase(phase_num)
        if phase:
            self.session.set_active_phase(phase_num)
            # Load the phase's dataframe if we have it cached
            # For now, show the stored metrics
            self._update_phase_display()
            self.update_status(f"Viewing Phase {phase_num} ({phase.samples} samples)")
    
    def _save_phase_and_continue(self):
        """Save current analysis as a phase and prepare for next."""
        if self.df_all is None:
            self.update_status("No data to save!")
            return
        
        phase_num = self.session.next_phase_number
        analysis = PhaseAnalysis.from_dataframe(
            phase_num=phase_num,
            df=self.df_all,
            log_files=self.datalogs,
            log_type=self.log_type
        )
        
        self.session.add_phase(analysis)
        
        # Show comparison if this is Phase 2+
        if phase_num > 1:
            self._show_phase_comparison(phase_num - 1, phase_num)
            self.update_status(f"✓ Phase {phase_num} saved | Load logs for Phase {phase_num + 1}")
        else:
            self.update_status(f"✓ Phase {phase_num} saved | Load logs for Phase {phase_num + 1}")
        
        # Clear for next phase
        self.datalogs = []
        self.datalog_dfs = {}
        self.df_all = None
        self.df_wot = None
        self.log_type = "Unknown"
        self.active_view = None
        self.phase_committed = False
        
        # Update UI
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        self.query_one("#log-type-label", Static).update("")
        self.query_one("#file-info", Static).update("")
        self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
        
        # Clear action items
        actions_table = self.query_one("#actions-panel", ActionItemsPanel).query_one("#actions-table", DataTable)
        actions_table.clear(columns=True)
        
        # Disable buttons until new data loaded
        self.query_one("#load-datalog-btn", Button).variant = "success"
        add_btn = self.query_one("#add-datalog-btn", Button)
        add_btn.disabled = True
        add_btn.variant = "default"
        self.query_one("#generate-btn", Button).disabled = True
        self.query_one("#export-btn", Button).disabled = True
        
        self._update_phase_display()
    
    def _show_phase_selector(self):
        """Show popup to select a previous phase."""
        if not self.session.phases:
            self.update_status("No saved phases yet")
            return
        
        self.push_screen(PhaseSelectScreen(self.session.phases, self._on_phase_selected))
    
    def _on_phase_selected(self, phase_num: int):
        """Handle phase selection from popup."""
        if phase_num:
            phase = self.session.get_phase(phase_num)
            if phase:
                self.session.set_active_phase(phase_num)
                self._update_phase_display()
                self.update_status(f"Viewing Phase {phase_num} ({phase.samples} samples)")
    
    def _start_next_phase(self):
        """Start collecting data for the next phase."""
        if not self.phase_committed:
            self.update_status("Commit current phase first!")
            return
        
        # Clear current data for new phase
        self.datalogs = []
        self.datalog_dfs = {}
        self.df_all = None
        self.df_wot = None
        self.log_type = "Unknown"
        self.active_view = None
        self.phase_committed = False
        
        # Update UI
        container = self.query_one("#loaded-files-container", Vertical)
        container.remove_children()
        self.query_one("#log-type-label", Static).update("")
        self.query_one("#file-info", Static).update("")
        self.query_one("#summary-panel", SummaryPanel).query_one("#summary-content", Static).update("Load a datalog to see analysis")
        
        # Clear action items
        actions_table = self.query_one("#actions-panel", ActionItemsPanel).query_one("#actions-table", DataTable)
        actions_table.clear(columns=True)
        
        # Disable buttons until new data loaded
        self.query_one("#load-datalog-btn", Button).variant = "success"
        add_btn = self.query_one("#add-datalog-btn", Button)
        add_btn.disabled = True
        add_btn.variant = "default"
        self.query_one("#generate-btn", Button).disabled = True
        self.query_one("#export-btn", Button).disabled = True
        
        self._update_phase_display()
        self.update_status(f"Ready for Phase {self.session.next_phase_number} - load new logs")
    
    def _show_phase_comparison(self, phase1_num: int, phase2_num: int):
        """Show comparison between two phases in the action items."""
        comparison = self.session.compare_phases(phase1_num, phase2_num)
        if not comparison:
            return
        
        # Build comparison summary for status
        improvements = []
        regressions = []
        
        for key, data in comparison.items():
            if isinstance(data, dict) and "status" in data:
                if data["status"] == "improved":
                    improvements.append(key)
                elif data["status"] == "worse":
                    regressions.append(key)
        
        if improvements and not regressions:
            self.update_status(f"✅ Phase {phase2_num}: All metrics improved!")
        elif regressions:
            self.update_status(f"⚠️ Phase {phase2_num}: {len(regressions)} metric(s) need attention")
        else:
            self.update_status(f"Phase {phase2_num} committed - no significant changes")
    
    def action_save_session(self):
        """Save the current session to a file."""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        default_name = f"tuning_session_{timestamp}.json"
        
        def handle_save(result):
            if result:
                try:
                    self.session.save(Path(result))
                    self.update_status(f"✓ Session saved to {result}")
                except Exception as e:
                    self.update_status(f"Error saving: {e}")
        
        self.push_screen(
            SaveFileScreen(
                default_name=default_name,
                title="Save Session",
                start_path=str(Path.home() / "Documents")
            ),
            handle_save
        )
    
    def action_load_session(self):
        """Load a session from a file."""
        def handle_load(result):
            if result:
                try:
                    self.session = TuningSession.load(Path(result))
                    self._update_phase_display()
                    
                    # If session has phases, show the active one
                    if self.session.phases:
                        active = self.session.get_active_phase()
                        if active:
                            self.update_status(f"✓ Loaded session with {len(self.session.phases)} phase(s)")
                    else:
                        self.update_status("✓ Session loaded (no phases yet)")
                except Exception as e:
                    self.update_status(f"Error loading: {e}")
        
        self.push_screen(
            FilePickerScreen(
                start_path=str(Path.home() / "Documents"),
                extensions=[".json"]
            ),
            handle_load
        )
    
    def action_quit(self) -> None:
        """Handle quit with save prompt if unsaved."""
        if self.session.is_dirty:
            self.push_screen(ConfirmScreen(
                "You have unsaved changes. Save before exiting?",
                on_yes=self._save_and_quit,
                on_no=self.exit,
                on_cancel=lambda: None
            ))
        else:
            self.exit()
    
    def _save_and_quit(self):
        """Save session then quit."""
        def after_save(result):
            if result:
                try:
                    self.session.save(Path(result))
                except Exception:
                    pass
            self.exit()
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        default_name = f"tuning_session_{timestamp}.json"
        
        self.push_screen(
            SaveFileScreen(
                default_name=default_name,
                title="Save Session Before Exit",
                start_path=str(Path.home() / "Documents")
            ),
            after_save
        )


def main():
    app = DAMGoodApp()
    app.run()


if __name__ == "__main__":
    main()
