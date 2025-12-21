#!/usr/bin/env python3
"""
Test script to debug view switching in DAMGood TUI.
This simulates the view switching process programmatically.
"""

import asyncio
import sys
from pathlib import Path

# Add scripts directory
sys.path.insert(0, str(Path(__file__).parent))

from analyze_datalog import load_datalog
from tui import DAMGoodApp


async def test_view_switching():
    """Test loading files and switching views."""
    app = DAMGoodApp()
    
    async with app.run_test(size=(120, 40)) as pilot:
        # Give the app time to initialize
        await pilot.pause()
        
        print("App started. Initial state:")
        print(f"  datalogs: {app.datalogs}")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all: {app.df_all is not None}")
        
        # Simulate loading test files
        test_file_1 = Path("samples/test-log-1.csv").resolve()
        test_file_2 = Path("samples/test-log-2.csv").resolve()
        
        if not test_file_1.exists():
            print(f"Test file not found: {test_file_1}")
            return
        
        # Load first file using the actual datalog loading
        print("\n--- Loading first file ---")
        df1 = load_datalog(test_file_1)
        app.datalogs = [test_file_1]
        app.datalog_dfs = {}
        app._process_datalog(df1, test_file_1)
        await pilot.pause()
        
        print(f"After loading first file:")
        print(f"  datalogs: {[str(p) for p in app.datalogs]}")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all rows: {len(app.df_all) if app.df_all is not None else 'None'}")
        
        # Load second file (append)
        print("\n--- Loading second file (append) ---")
        df2 = load_datalog(test_file_2)
        app.datalogs.append(test_file_2)
        log_type, _, df_wot = app._detect_log_type(df2)
        app.datalog_dfs[test_file_2] = (df2, log_type, df_wot)
        app._rebuild_combined_view()
        app.active_view = test_file_2
        app.df_all = df2
        app.df_wot = df_wot
        app.log_type = log_type
        app._update_file_list()
        app._analyze()
        await pilot.pause()
        
        print(f"After loading second file:")
        print(f"  datalogs: {[str(p) for p in app.datalogs]}")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all rows: {len(app.df_all) if app.df_all is not None else 'None'}")
        
        # Switch to first file
        print("\n--- Switching to first file ---")
        app._select_view(test_file_1)
        await pilot.pause()
        
        print(f"After switching to first file:")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all rows: {len(app.df_all) if app.df_all is not None else 'None'}")
        
        # Switch to second file
        print("\n--- Switching to second file ---")
        app._select_view(test_file_2)
        await pilot.pause()
        
        print(f"After switching to second file:")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all rows: {len(app.df_all) if app.df_all is not None else 'None'}")
        
        # Switch back to first file (3rd switch - the one that might fail)
        print("\n--- Switching back to first file (3rd switch) ---")
        app._select_view(test_file_1)
        await pilot.pause()
        
        print(f"After switching back to first file:")
        print(f"  active_view: {app.active_view}")
        print(f"  df_all rows: {len(app.df_all) if app.df_all is not None else 'None'}")
        
        print("\n--- Test complete ---")
        
        # Print the debug log
        print("\n=== Debug Log ===")
        try:
            with open('/tmp/damgood_debug.log', 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print("No debug log found")


if __name__ == "__main__":
    asyncio.run(test_view_switching())
