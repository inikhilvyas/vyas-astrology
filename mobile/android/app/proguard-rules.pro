# VYAS ASTRA Play Store R8 ProGuard Rules
-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-dontwarn okio.**
-dontwarn javax.annotation.**
