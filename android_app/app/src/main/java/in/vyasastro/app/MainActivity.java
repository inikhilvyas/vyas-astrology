package in.vyasastro.app;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowInsetsController;
import android.webkit.ConsoleMessage;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;

import android.widget.Toast;

public class MainActivity extends Activity {
    private static final String LIVE_URL = "https://vyasastro.in/mobile/";
    private static final String OFFLINE_URL = "file:///android_asset/mobile/index.html";

    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Thread.setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
            @Override
            public void uncaughtException(Thread t, Throwable e) {
                Log.e("VyasAstraCrash", "Uncaught exception: " + e.getMessage(), e);
            }
        });

        try {
            Window window = getWindow();
            if (window != null) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                    WindowInsetsController controller = window.getInsetsController();
                    if (controller != null) {
                        controller.setSystemBarsAppearance(0,
                            WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);
                    }
                } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                    window.getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    );
                    window.setStatusBarColor(Color.parseColor("#030712"));
                    window.setNavigationBarColor(Color.parseColor("#030712"));
                }
            }
        } catch (Throwable t) {
            Log.w("VyasAstra", "StatusBar config skipped: " + t.getMessage());
        }

        try {
            webView = new WebView(this);
            webView.setBackgroundColor(Color.parseColor("#030712"));
            WebSettings settings = webView.getSettings();
            settings.setJavaScriptEnabled(true);
            settings.setDomStorageEnabled(true);
            settings.setDatabaseEnabled(true);
            settings.setAllowFileAccess(true);
            settings.setAllowContentAccess(true);
            settings.setAllowFileAccessFromFileURLs(true);
            settings.setAllowUniversalAccessFromFileURLs(true);
            settings.setLoadsImagesAutomatically(true);
            settings.setCacheMode(WebSettings.LOAD_DEFAULT);
            settings.setUseWideViewPort(true);
            settings.setLoadWithOverviewMode(true);
            settings.setBuiltInZoomControls(false);
            settings.setDisplayZoomControls(false);

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
            }

            webView.setWebViewClient(new WebViewClient() {
                @Override
                public boolean shouldOverrideUrlLoading(WebView view, String url) {
                    return false;
                }
                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Log.e("VyasAstraWeb", "WebView Error (" + errorCode + "): " + description);
                    try {
                        if (failingUrl != null && failingUrl.startsWith("https://vyasastro.in")) {
                            Log.i("VyasAstraWeb", "Network error encountered on live site. Falling back to offline bundle.");
                            view.loadUrl(OFFLINE_URL);
                        }
                    } catch (Throwable ignored) {}
                }
            });

            webView.setWebChromeClient(new WebChromeClient() {
                @Override
                public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
                    // Replace intrusive "The page at file:// says:" dialog with sleek Android Toast
                    if (message != null && !message.trim().isEmpty()) {
                        Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
                    }
                    result.confirm();
                    return true;
                }
                @Override
                public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                    Log.d("VyasAstraConsole", consoleMessage.message() + " [" + consoleMessage.lineNumber() + "]");
                    return true;
                }
            });

            try {
                webView.addJavascriptInterface(new WebAppInterface(this), "VyasNativeBridge");
            } catch (Throwable t) {
                Log.w("VyasAstra", "Bridge init skipped: " + t.getMessage());
            }

            setContentView(webView);
                        boolean isConnected = false;
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
            }

        } catch (Throwable t) {
            Log.e("VyasAstra", "Fatal WebView init error: " + t.getMessage(), t);
            Toast.makeText(this, "VyasAstra Init Error: " + t.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    @Override
    public void onBackPressed() {
        try {
            if (webView != null && webView.canGoBack()) {
                webView.goBack();
                return;
            }
        } catch (Throwable ignored) {}
        super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        try {
            if (webView != null) {
                webView.destroy();
            }
        } catch (Throwable ignored) {}
        super.onDestroy();
    }
}
