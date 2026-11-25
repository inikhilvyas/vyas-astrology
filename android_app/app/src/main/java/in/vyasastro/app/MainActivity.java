package in.vyasastro.app;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkCapabilities;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Message;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowInsetsController;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends AppCompatActivity {
    private static final String LIVE_URL = "https://vyasastro.in/mobile/";
    private static final String OFFLINE_URL = "file:///android_asset/mobile/index.html";
    private static final String TAG = "VyasAstraNative";

    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Thread.setDefaultUncaughtExceptionHandler((t, e) ->
            Log.e(TAG, "Uncaught exception on thread " + t.getName() + ": " + e.getMessage(), e)
        );

        setupWindowBars();

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
            settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
            webView.clearCache(true);
            settings.setUseWideViewPort(true);
            settings.setLoadWithOverviewMode(true);
            settings.setBuiltInZoomControls(false);
            settings.setDisplayZoomControls(false);

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
            }

            webView.setWebViewClient(new WebViewClient() {
                @Override
                public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                    if (request == null || request.getUrl() == null) return false;
                    return handleUrlNavigation(view, request.getUrl().toString());
                }

                @Override
                public boolean shouldOverrideUrlLoading(WebView view, String url) {
                    return handleUrlNavigation(view, url);
                }

                private boolean handleUrlNavigation(WebView view, String url) {
                    if (url == null) return false;
                    // Google OAuth or external auth MUST open in system browser to prevent 403 disallowed_useragent and black screens
                    if (url.contains("accounts.google.com") || url.contains("google.com/o/oauth2") || url.contains("oauth2.googleapis.com")) {
                        try {
                            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                            startActivity(intent);
                            return true;
                        } catch (Throwable t) {
                            Log.e(TAG, "Failed to launch external browser for OAuth", t);
                            return true; // Consume so WebView NEVER loads 403 disallowed_useragent black screen
                        }
                    }
                    if (url.startsWith("https://vyasastro.in") || url.startsWith("file://")) {
                        return false;
                    }
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(intent);
                        return true;
                    } catch (Throwable t) {
                        return false;
                    }
                }

                @Override
                public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                    Log.w(TAG, "WebView error: " + description + " (" + errorCode + ") on " + failingUrl);
                    if (failingUrl != null && failingUrl.startsWith("https://vyasastro.in")) {
                        Log.i(TAG, "Network failure. Switching seamlessly to offline bundled asset engine.");
                        view.loadUrl(OFFLINE_URL);
                    }
                }
            });

            webView.setWebChromeClient(new WebChromeClient() {
                @Override
                public boolean onCreateWindow(WebView view, boolean isDialog, boolean isUserGesture, Message resultMsg) {
                    WebView.HitTestResult result = view.getHitTestResult();
                    String data = result != null ? result.getExtra() : null;
                    if (data != null && (data.contains("accounts.google.com") || data.contains("google.com/o/oauth2"))) {
                        try {
                            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(data));
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                            startActivity(intent);
                            return false;
                        } catch (Throwable ignored) {}
                    }
                    return false;
                }

                @Override
                public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
                    if (message != null && !message.trim().isEmpty()) {
                        Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
                    }
                    result.confirm();
                    return true;
                }

                @Override
                public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                    Log.d(TAG + "_JS", consoleMessage.message() + " [L" + consoleMessage.lineNumber() + "]");
                    return true;
                }
            });

            // Register Native JavaScript Bridge under BOTH "Android" and "VyasNativeBridge" for 100% interoperability
            WebAppInterface bridge = new WebAppInterface(this);
            webView.addJavascriptInterface(bridge, "Android");
            webView.addJavascriptInterface(bridge, "VyasNativeBridge");

            setContentView(webView);

            // Modern Predictive Back Navigation Callback
            getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
                @Override
                public void handleOnBackPressed() {
                    if (webView != null && webView.canGoBack()) {
                        webView.goBack();
                    } else {
                        setEnabled(false);
                        getOnBackPressedDispatcher().onBackPressed();
                    }
                }
            });

            // Route: Always load High-Precision Bundled Native Engine for 100% Offline Integrity & Speed
            Log.i(TAG, "Native Engine: Loading high-precision bundled asset " + OFFLINE_URL);
            webView.loadUrl(OFFLINE_URL);

        } catch (Throwable t) {
            Log.e(TAG, "Fatal WebView init failure", t);
            Toast.makeText(this, "VyasAstra Native Error: " + t.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void setupWindowBars() {
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
        } catch (Throwable ignored) {}
    }

    private boolean isNetworkConnected() {
        try {
            ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm == null) return false;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                android.net.Network net = cm.getActiveNetwork();
                if (net == null) return false;
                NetworkCapabilities caps = cm.getNetworkCapabilities(net);
                return caps != null && (caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
                                       caps.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) ||
                                       caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET));
            } else {
                NetworkInfo ni = cm.getActiveNetworkInfo();
                return ni != null && ni.isConnected();
            }
        } catch (Throwable ignored) {
            return false;
        }
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

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        if (intent != null && intent.getData() != null) {
            String dataUrl = intent.getData().toString();
            Log.i(TAG, "Deep link return received: " + dataUrl);
            if (webView != null) {
                if (dataUrl.contains("access_token=") || dataUrl.contains("id_token=")) {
                    final String safeUrl = dataUrl.replace("'", "\\'");
                    webView.post(() -> webView.evaluateJavascript(
                        "if(window.VyasMobile && typeof window.VyasMobile.handleOAuthDeepLink === 'function'){ window.VyasMobile.handleOAuthDeepLink('" + safeUrl + "'); }",
                        null
                    ));
                } else {
                    webView.loadUrl(dataUrl);
                }
            }
        }
    }

    /**
     * Native Android JavaScript Bridge for VYAS ASTRA
     */
    public class WebAppInterface {
        private final Context context;

        public WebAppInterface(Context context) {
            this.context = context;
        }

        @JavascriptInterface
        public void openExternalUrl(String url) {
            try {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(intent);
            } catch (Throwable t) {
                Log.e(TAG, "Failed to open external url: " + t.getMessage());
            }
        }

        @JavascriptInterface
        public void showToast(String message) {
            if (message != null && !message.isEmpty()) {
                runOnUiThread(() -> Toast.makeText(context, message, Toast.LENGTH_SHORT).show());
            }
        }

        @JavascriptInterface
        public void shareKundli(String text, String title) {
            try {
                Intent sendIntent = new Intent(Intent.ACTION_SEND);
                sendIntent.putExtra(Intent.EXTRA_TEXT, text);
                sendIntent.putExtra(Intent.EXTRA_SUBJECT, title != null ? title : "VYAS ASTRA वैदिक कुण्डली");
                sendIntent.setType("text/plain");
                Intent shareIntent = Intent.createChooser(sendIntent, title != null ? title : "कुण्डली साझा करें");
                context.startActivity(shareIntent);
            } catch (Throwable t) {
                Log.e(TAG, "Share failed: " + t.getMessage());
            }
        }

        @JavascriptInterface
        public void triggerHaptic() {
            try {
                Vibrator v = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
                if (v != null) {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        v.vibrate(VibrationEffect.createOneShot(35, VibrationEffect.DEFAULT_AMPLITUDE));
                    } else {
                        v.vibrate(35);
                    }
                }
            } catch (Throwable ignored) {}
        }

        @JavascriptInterface
        public boolean isOnline() {
            return isNetworkConnected();
        }

        @JavascriptInterface
        public String getVersionName() {
            return "1.0.0";
        }

        @JavascriptInterface
        public int getVersionCode() {
            return 100;
        }
    }
}
