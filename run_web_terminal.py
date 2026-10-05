"""VYAS Web Terminal & Cloud Server Launcher.

Launches the VYAS Vedic Astrology Platform configured for cloud/web terminal deployment:
- Binds to 0.0.0.0 (accessible over public IP / web terminal)
- Headless execution mode
- Port 8501 (or custom PORT environment variable)
- Automatic browser opening disabled for server environments
"""
import os
import sys
import subprocess

def launch_server():
    port = os.environ.get("PORT", "8501")
    host = os.environ.get("HOST", "0.0.0.0")

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        f"--server.port={port}",
        f"--server.address={host}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--theme.base=dark"
    ]

    print(f"🚀 Starting VYAS Web Terminal Server on http://{host}:{port} ...")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️ VYAS Server stopped.")

if __name__ == "__main__":
    launch_server()
