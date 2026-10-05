"""
VYAS Desktop Launcher (Standalone Desktop Application Mode)
Runs the VYAS Vedic Astrology platform inside a native Windows desktop window.
Can be compiled into a single .exe using PyInstaller.
"""
import os
import sys
import time
import subprocess
import threading
import webbrowser

def start_streamlit():
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    cmd = [
        sys.executable,
        "-m", "streamlit", "run",
        app_path,
        "--server.port=8501",
        "--server.headless=true",
        "--theme.base=dark"
    ]
    subprocess.run(cmd)

def main():
    print("=" * 60)
    print("  VYAS (Vedic Yield Astrology Systems) - Desktop Edition")
    print("  System Architect: Nikhil Vyas (M.A. Jyotish / PG in Astrology)")
    print("=" * 60)
    
    # Start Streamlit server in background thread
    server_thread = threading.Thread(target=start_streamlit, daemon=True)
    server_thread.start()
    
    # Wait for server to initialize
    time.sleep(3)
    
    # Try opening native webview or fallback to default browser
    try:
        import webview
        print("Launching native Windows application window...")
        webview.create_window(
            "VYAS ASTRA • Vedic Yield Astrology Systems",
            "http://localhost:8501",
            width=1380,
            height=880,
            resizable=True
        )
        webview.start()
    except ImportError:
        print("Opening VYAS in local browser window...")
        webbrowser.open("http://localhost:8501")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down VYAS Desktop...")

if __name__ == "__main__":
    main()
