#!/usr/bin/env python3
"""
DAMGood Web Server - Serve the TUI in a browser.

Run with: python scripts/serve_web.py
Then visit: http://localhost:8000

Requires: pip install textual-serve
"""

from textual_serve.server import Server
import sys
from pathlib import Path

def main():
    # Get the path to the TUI script
    tui_script = Path(__file__).parent / "tui.py"
    
    # Create server
    server = Server(
        command=f"python3 {tui_script}",
        host="localhost",
        port=8000,
        title="DAMGood - FA20 Datalog Analyzer"
    )
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     DAMGood Web Server                                        ║
║                     FA20 Datalog Analyzer                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Starting web server...

Open your browser to: http://localhost:8000

Press Ctrl+C to stop the server.
""")
    
    # Start serving
    server.serve()


if __name__ == "__main__":
    main()
