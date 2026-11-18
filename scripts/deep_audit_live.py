import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets

PORT = 9333
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
TEMP_PROFILE = r'C:\temp_chrome_audit_live'
ARTIFACT_DIR = r'C:\Users\Administrator\.gemini\antigravity\brain\bf41d1cd-300b-445c-bfd4-855f546b57c2'

async def run_audit():
    # 1. Launch Chrome Headless
    import shutil
    if os.path.exists(TEMP_PROFILE):
        try:
            shutil.rmtree(TEMP_PROFILE)
        except Exception:
            pass

    cmd = [
        CHROME_PATH,
        '--headless=new',
        f'--remote-debugging-port={PORT}',
        f'--user-data-dir={TEMP_PROFILE}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-gpu',
        '--window-size=1440,900',
        'about:blank'
    ]
    proc = subprocess.Popen(cmd)
    await asyncio.sleep(2)

    try:
        # Get target WebSocket
        with urllib.request.urlopen(f'http://localhost:{PORT}/json') as resp:
            tabs = json.loads(resp.read().decode())
            ws_url = None
            for t in tabs:
                if t.get('type') == 'page' and 'about:blank' in t.get('url', ''):
                    ws_url = t.get('webSocketDebuggerUrl')
                    break
            if not ws_url and tabs:
                ws_url = tabs[0].get('webSocketDebuggerUrl')

        print(f"Connecting to CDP: {ws_url}")
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            msg_id = 0
            pending_responses = {}
            events = []
            console_logs = []
            network_errors = []

            async def send_cmd(method, params=None):
                nonlocal msg_id
                msg_id += 1
                curr_id = msg_id
                payload = {"id": curr_id, "method": method}
                if params:
                    payload["params"] = params
                await ws.send(json.dumps(payload))
                return curr_id

            async def eval_js(expression):
                cid = await send_cmd("Runtime.evaluate", {
                    "expression": expression,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                # wait for response
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
                elif method == "Network.loadingFailed":
                    params = data.get("params", {})
                    network_errors.append(f"FAILED: {params.get('errorText')} - {params.get('requestId')}")

            # Enable domains
            await send_cmd("Page.enable")
            await send_cmd("Runtime.enable")
            await send_cmd("Console.enable")
            await send_cmd("Network.enable")

            # Navigate to target
            print("Navigating to https://vyasastro.in/ ...")
            nav_id = await send_cmd("Page.navigate", {"url": "https://vyasastro.in/"})

            # Listen for 6 seconds to let scripts run and settle
            start_time = time.time()
            while time.time() - start_time < 6:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    handle_event(data)
                except asyncio.TimeoutError:
                    pass

            print("\n=== INITIAL CONSOLE LOGS & WARNINGS ===")
            for l in console_logs:
                print(l)

            print("\n=== NETWORK ERRORS ===")
            for n in network_errors:
                print(n)

            # 1. Evaluate top badge degree & current profile
            badge_text = await eval_js("document.querySelector('.pro-status-badge, .header-profile-badge, #proBadge, #nikhilBadge, .user-badge')?.innerText || document.body.innerText.match(/NIKHIL[^\\n]*/)?.[0]")
            print(f"\n[AUDIT 1] Top Profile Badge: {badge_text}")

            active_profile = await eval_js("JSON.stringify(localStorage.getItem('vyas_active_profile'))")
            print(f"[AUDIT 1.1] vyas_active_profile in localStorage: {active_profile[:200] if active_profile else 'None'}")

            engine_version = await eval_js("localStorage.getItem('vyas_engine_version')")
            print(f"[AUDIT 1.2] vyas_engine_version: {engine_version}")

            # 2. Evaluate Google Login State
            gis_loaded = await eval_js("!!(window.google && window.google.accounts)")
            gis_id_loaded = await eval_js("!!(window.google && window.google.accounts && window.google.accounts.id)")
            gis_oauth2_loaded = await eval_js("!!(window.google && window.google.accounts && window.google.accounts.oauth2)")
            client_id = await eval_js("window.VyasDesktop?.GOOGLE_CLIENT_ID")
            google_user = await eval_js("JSON.stringify(window.VyasDesktop?.googleUser)")
            print(f"\n[AUDIT 2] Google Identity Services Loaded: {gis_loaded}")
            print(f"[AUDIT 2.1] GIS .id exists: {gis_id_loaded}")
            print(f"[AUDIT 2.2] GIS .oauth2 exists: {gis_oauth2_loaded}")
            print(f"[AUDIT 2.3] GOOGLE_CLIENT_ID: {client_id}")
            print(f"[AUDIT 2.4] VyasDesktop.googleUser: {google_user}")

            # Check Google Sign in Button DOM
            btn_exists = await eval_js("!!document.getElementById('googleSignInBtn')")
            btn_text = await eval_js("document.getElementById('googleSignInBtn')?.innerText")
            print(f"[AUDIT 2.5] googleSignInBtn in DOM: {btn_exists}, text: {btn_text}")

            # 3. Simulate Clicking Google Sign In Button
            print("\n[AUDIT 3] Clicking Google Sign-In Button...")
            click_res = await eval_js("""
            (function() {
                var btn = document.getElementById('googleSignInBtn');
                if (!btn) return 'NO_BTN';
                try {
                    btn.click();
                    return 'CLICKED';
                } catch(e) {
                    return 'CLICK_ERROR: ' + e.message;
                }
            })()
            """)
            print(f"[AUDIT 3.1] Button Click Result: {click_res}")

            # Wait 3 seconds to capture any errors from clicking
            await asyncio.sleep(3)
            while True:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    data = json.loads(msg)
                    handle_event(data)
                except asyncio.TimeoutError:
                    break

            # Check if modal or popup opened
            modal_display = await eval_js("document.getElementById('modalGoogleAuth')?.style.display")
            modal_class = await eval_js("document.getElementById('modalGoogleAuth')?.className")
            popover_display = await eval_js("document.getElementById('userProfilePopover')?.style.display")
            print(f"[AUDIT 3.2] modalGoogleAuth: display={modal_display}, class={modal_class}")
            print(f"[AUDIT 3.3] userProfilePopover: display={popover_display}")

            # 4. Check Dasha Tab
            print("\n[AUDIT 4] Checking Vimshottari Dasha Tab...")
            dasha_click = await eval_js("""
            (function() {
                var tab = Array.from(document.querySelectorAll('.nav-tab, .tab-btn, button')).find(b => b.innerText.includes('विंशोत्तरी दशा'));
                if (tab) {
                    tab.click();
                    return 'TAB_CLICKED';
                }
                return 'TAB_NOT_FOUND';
            })()
            """)
            print(f"[AUDIT 4.1] Dasha Tab Click: {dasha_click}")
            await asyncio.sleep(1.5)

            active_dasha_badge = await eval_js("document.querySelector('#dashaRunningChain, .running-dasha-badge, #currentDashaPath')?.innerText || 'Not found'")
            print(f"[AUDIT 4.2] Active Dasha Badge: {active_dasha_badge}")

            dasha_items = await eval_js("""
            Array.from(document.querySelectorAll('#dashaTreeRoot .dasha-level-1, .dasha-row, .dasha-card')).slice(0, 5).map(el => el.innerText.replace(/\\s+/g, ' '))
            """)
            print(f"[AUDIT 4.3] Top Dasha Rows: {dasha_items}")

            # 5. Check Ashtakavarga Tab
            print("\n[AUDIT 5] Checking Ashtakavarga Tab...")
            av_click = await eval_js("""
            (function() {
                var tab = Array.from(document.querySelectorAll('.nav-tab, .tab-btn, button')).find(b => b.innerText.includes('अष्टकवर्ग'));
                if (tab) {
                    tab.click();
                    return 'TAB_CLICKED';
                }
                return 'TAB_NOT_FOUND';
            })()
            """)
            print(f"[AUDIT 5.1] Ashtakavarga Tab Click: {av_click}")
            await asyncio.sleep(1.5)

            sav_sum = await eval_js("""
            (function() {
                var bindoos = Array.from(document.querySelectorAll('.sav-house-card .sav-bindu-val, .sav-score')).map(e => parseInt(e.innerText) || 0);
                var sum = bindoos.reduce((a, b) => a + b, 0);
                return { bindoos: bindoos, sum: sum };
            })()
            """)
            print(f"[AUDIT 5.2] SAV Sum: {sav_sum}")

            # 6. Take Screenshot of Current State
            shot_id = await send_cmd("Page.captureScreenshot", {"format": "png"})
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == shot_id:
                    img_data = data.get("result", {}).get("data")
                    import base64
                    screenshot_path = os.path.join(ARTIFACT_DIR, "live_audit_screenshot.png")
                    with open(screenshot_path, "wb") as sf:
                        sf.write(base64.b64decode(img_data))
                    print(f"\n[SCREENSHOT] Saved full page screenshot to: {screenshot_path}")
                    break

            print("\n=== LATE CONSOLE LOGS AFTER TAB SWITCHING ===")
            for l in console_logs[-15:]:
                print(l)

    finally:
        proc.terminate()
        print("\nAudit complete, Chrome process terminated.")

if __name__ == '__main__':
    asyncio.run(run_audit())

