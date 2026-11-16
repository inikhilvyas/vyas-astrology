import os
import re

print("=== Starting Comprehensive Privacy, UI, and Direct Update Overhaul ===")

# -------------------------------------------------------------
# 1. Update sw.js: Force Cache Invalidation
# -------------------------------------------------------------
sw_path = "sw.js"
with open(sw_path, "r", encoding="utf-8") as f:
    sw_code = f.read()

# Replace cache name
sw_code = re.sub(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'vyas-astra-v2026-fresh-1';", sw_code)
with open(sw_path, "w", encoding="utf-8") as f:
    f.write(sw_code)
print("✓ sw.js updated with fresh cache name 'vyas-astra-v2026-fresh-1'")

# -------------------------------------------------------------
# 2. Update MainActivity.java: Direct Online Sync + Offline Fallback
# -------------------------------------------------------------
main_act_path = r"android_app\app\src\main\java\in\vyasastro\app\MainActivity.java"
with open(main_act_path, "r", encoding="utf-8") as f:
    main_act = f.read()

# We need imports for ConnectivityManager, NetworkInfo
imports_to_add = """import android.net.ConnectivityManager;
import android.net.NetworkInfo;
"""
if "import android.net.ConnectivityManager;" not in main_act:
    main_act = main_act.replace("import android.webkit.WebViewClient;", "import android.webkit.WebViewClient;\n" + imports_to_add)

# Constants for LIVE_URL and OFFLINE_URL
constants = """    private static final String LIVE_URL = "https://vyasastro.in/mobile/";
    private static final String OFFLINE_URL = "file:///android_asset/mobile/index.html";
"""
if "LIVE_URL" not in main_act:
    main_act = main_act.replace("public class MainActivity extends Activity {", "public class MainActivity extends Activity {\n" + constants)

# Update onReceivedError in WebViewClient to fallback to offline asset
old_error_handler = """                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Log.e("VyasAstraWeb", "WebView Error (" + errorCode + "): " + description);
                }"""

new_error_handler = """                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Log.e("VyasAstraWeb", "WebView Error (" + errorCode + "): " + description);
                    try {
                        if (failingUrl != null && failingUrl.startsWith("https://vyasastro.in")) {
                            Log.i("VyasAstraWeb", "Network error encountered on live site. Falling back to offline bundle.");
                            view.loadUrl(OFFLINE_URL);
                        }
                    } catch (Throwable ignored) {}
                }"""

if old_error_handler in main_act:
    main_act = main_act.replace(old_error_handler, new_error_handler)

# Update webView.loadUrl call in onCreate
old_load = 'webView.loadUrl("file:///android_asset/mobile/index.html");'
new_load = """            boolean isConnected = false;
            try {
                ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
                if (cm != null) {
                    NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
                    isConnected = (activeNetwork != null && activeNetwork.isConnected());
                }
            } catch (Throwable t) {
                Log.w("VyasAstra", "Connectivity check skipped: " + t.getMessage());
            }

            if (isConnected) {
                Log.i("VyasAstra", "Active internet detected. Loading live mobile platform: " + LIVE_URL);
                webView.loadUrl(LIVE_URL);
            } else {
                Log.i("VyasAstra", "No internet connection detected. Loading offline assets: " + OFFLINE_URL);
                webView.loadUrl(OFFLINE_URL);
            }"""

if old_load in main_act:
    main_act = main_act.replace(old_load, new_load)

with open(main_act_path, "w", encoding="utf-8") as f:
    f.write(main_act)
print("✓ MainActivity.java updated with intelligent online live update + offline fallback")

print("Step 1 and 2 complete.")

