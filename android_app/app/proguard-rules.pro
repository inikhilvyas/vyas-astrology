# Optimization & Obfuscation rules for VYAS ASTRA Release Build
# Google Play Store R8 / ProGuard rules

-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keepattributes JavascriptInterface

# Keep WebKit and JavaScript interfaces
-keepclassmembers class in.vyasastro.app.MainActivity$WebAppInterface {
    <methods>;
}

-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# AndroidX Core & Material
-dontwarn androidx.**
-keep class androidx.appcompat.** { *; }
-keep class com.google.android.material.** { *; }

# Security Crypto
-keep class androidx.security.crypto.** { *; }
