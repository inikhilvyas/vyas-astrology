import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets

PORT = 9444
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
TEMP_PROFILE = r'C:\temp_chrome_audit_local'
ARTIFACT_DIR = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2'

async def run_local_audit():
    # 1. Start Python HTTP Server
    http_proc = subprocess.Popen(['python', '-m', 'http.server', '8765'], cwd=r'G:\software\simpa\VYAS')
    await asyncio.sleep(1)

    # 2. Launch Chrome Headless
    import shutil
    if os.path.exists(TEMP_PROFILE):
        try: shutil.rmtree(TEMP_PROFILE)
        except Exception: pass

    cmd = [
        CHROME_PATH,
        '--headless=new',
        f'--remote-debugging-port={PORT}',
        f'--user-data-dir={TEMP_PROFILE}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-gpu',
        '--window-size=1440,900',
        'http://localhost:8765/index.html'
    ]
    chrome_proc = subprocess.Popen(cmd)
    await asyncio.sleep(2)

    try:
        with urllib.request.urlopen(f'http://localhost:{PORT}/json') as resp:
            tabs = json.loads(resp.read().decode())
            ws_url = None
            for t in tabs:
                if t.get('type') == 'page' and 'localhost:8765' in t.get('url', ''):
                    ws_url = t.get('webSocketDebuggerUrl')
                    break
            if not ws_url and tabs:
                ws_url = tabs[0].get('webSocketDebuggerUrl')

        print(f"Connecting to Local CDP: {ws_url}")
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            msg_id = 0
            console_logs = []
            network_errors = []

            async def send_cmd(method, params=None):
                nonlocal msg_id
                msg_id += 1
                curr_id = msg_id
                payload = {"id": curr_id, "method": method}
                if params: payload["params"] = params
                await ws.send(json.dumps(payload))
                return curr_id

            async def eval_js(expression):
                cid = await send_cmd("Runtime.evaluate", {
                    "expression": expression,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    handle_event(data)
                    if data.get("id") == cid:
                        res = data.get("result", {})
                        if "exceptionDetails" in res:
                            return {"error": res["exceptionDetails"]}
                        return res.get("result", {}).get("value")

            def handle_event(data):
                method = data.get("method")
                if method == "Runtime.consoleAPICalled":
                    params = data.get("params", {})
                    log_type = params.get("type")
                    args = [a.get("value") or a.get("description") or str(a) for a in params.get("args", [])]
                    console_logs.append(f"[{log_type.upper()}] {' '.join(str(x) for x in args)}")
                elif method == "Runtime.exceptionThrown":
                    exc = data.get("params", {}).get("exceptionDetails", {})
                    console_logs.append(f"[EXCEPTION] {exc.get('text')} {exc.get('exception', {}).get('description')}")
                elif method == "Network.responseReceived":
                    resp = data.get("params", {}).get("response", {})
                    status = resp.get("status")
                    if status >= 400:
                        network_errors.append(f"HTTP {status}: {resp.get('url')}")

            await send_cmd("Page.enable")
            await send_cmd("Runtime.enable")
            await send_cmd("Console.enable")
            await send_cmd("Network.enable")

            # Wait 4 seconds for scripts
            start = time.time()
            while time.time() - start < 4:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    handle_event(data)
                except asyncio.TimeoutError:
                    pass

            print("\n=== LOCAL AUDIT CONSOLE LOGS ===")
            for l in console_logs:
                print(l)

            # Check VyasDesktop definition
            has_desktop = await eval_js("typeof window.VyasDesktop")
            print(f"\n[LOCAL TEST 1] typeof window.VyasDesktop: {has_desktop}")

            # Check Degree badge
            badge_text = await eval_js("document.querySelector('.user-profile-badge, #nikhilBadge, .header-profile-badge, .pro-status-badge')?.innerText || document.body.innerText.match(/NIKHIL[^\\n]*/)?.[0]")
            print(f"[LOCAL TEST 2] Header Badge: {badge_text}")

            # Check Active Chart Data
            lagna_deg = await eval_js("window.VyasDesktop?.activeChartData?.lagna_dms || window.VyasDesktop?.activeChartData?.planets?.find(p => p.name === 'Lagna')?.dms || 'Not loaded'")
            print(f"[LOCAL TEST 3] Active Chart Lagna: {lagna_deg}")

            # Check Dasha
            dasha_active = await eval_js("document.getElementById('dashaRunningChain')?.innerText || 'None'")
            print(f"[LOCAL TEST 4] Active Dasha Chain: {dasha_active}")

            # Check Ashtakavarga
            sav_sum = await eval_js("""
            (function() {
                var b = Array.from(document.querySelectorAll('.sav-bindu-val, .sav-score')).map(e => parseInt(e.innerText) || 0);
                return { count: b.length, sum: b.reduce((x, y) => x + y, 0), values: b };
            })()
            """)
            print(f"[LOCAL TEST 5] SAV Sum: {sav_sum}")

            # Check Google Sign in Button
            click_res = await eval_js("""
            (function() {
                var btn = document.getElementById('googleSignInBtn');
                if (!btn) return 'NO_BTN';
                btn.click();
                return 'CLICKED_SUCCESS';
            })()
            """)
            print(f"[LOCAL TEST 6] Google Sign In Click: {click_res}")

            # Wait 1 sec
            await asyncio.sleep(1)
            modal_display = await eval_js("document.getElementById('modalGoogleAuth')?.style.display")
            print(f"[LOCAL TEST 7] modalGoogleAuth display after click: {modal_display}")

            # Take screenshot of local fixed page
            shot_id = await send_cmd("Page.captureScreenshot", {"format": "png"})
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == shot_id:
                    img_data = data.get("result", {}).get("data")
                    import base64
                    screenshot_path = os.path.join(ARTIFACT_DIR, "local_fixed_audit_screenshot.png")
                    with open(screenshot_path, "wb") as sf:
                        sf.write(base64.b64decode(img_data))
                    print(f"\n[SCREENSHOT] Saved local screenshot to: {screenshot_path}")
                    break

    finally:
        chrome_proc.terminate()
        http_proc.terminate()
        print("\nLocal audit finished.")

if __name__ == '__main__':
    asyncio.run(run_local_audit())

