package in.vyasastro.app;

import android.app.AlarmManager;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.util.Log;

import androidx.core.app.NotificationCompat;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Calendar;

/**
 * Native Android Background Receiver for VYAS ASTRA Daily Notifications.
 * Fires at 9:00 PM (tomorrow's preview) and 7:00 AM (today's morning alert),
 * fetching the live 24x7 Cloud Feed when online or falling back to local
 * personalized Panchang + Bhavishyaphal synced from the user's Kundli.
 */
public class DailyNotificationReceiver extends BroadcastReceiver {
    private static final String TAG = "VyasDailyNotif";
    public static final String CHANNEL_ID = "vyas_daily_panchang";
    public static final String ACTION_9PM = "in.vyasastro.app.ACTION_DAILY_9PM";
    public static final String ACTION_7AM = "in.vyasastro.app.ACTION_DAILY_7AM";
    private static final String PREFS_NAME = "vyas_daily_notif";
    private static final String CLOUD_FEED_URL =
        "https://raw.githubusercontent.com/vyasbilawas-ctrl/vyas-astrology/main/data/daily_notifications_feed.json";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (context == null || intent == null) return;
        String action = intent.getAction();
        if (Intent.ACTION_BOOT_COMPLETED.equals(action)) {
            scheduleDailyAlarms(context);
            return;
        }

        final String slot = ACTION_9PM.equals(action) ? "9pm" : "7am";
        final PendingResult pendingResult = goAsync();
        new Thread(() -> {
            try {
                SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
                String title = prefs.getString("title_" + slot,
                    "9pm".equals(slot)
                        ? "🕉️ कल का दैनिक पंचांग व भविष्यफल"
                        : "🕉️ आज का प्रातःकालीन पंचांग व भविष्यफल");
                String body = prefs.getString("body_" + slot,
                    "अपना लग्न, राशि, नक्षत्र, सूक्ष्म दशा, नवतारा व सर्वतोभद्र चक्र फल देखें।");

                // Attempt to fetch latest 24x7 Cloud Feed when online
                try {
                    URL url = new URL(CLOUD_FEED_URL);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setConnectTimeout(5000);
                    conn.setReadTimeout(5000);
                    conn.setRequestProperty("User-Agent", "VyasAstra-Android/1.0");
                    if (conn.getResponseCode() == 200) {
                        BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
                        StringBuilder sb = new StringBuilder();
                        String line;
                        while ((line = br.readLine()) != null) sb.append(line);
                        br.close();
                        JSONObject root = new JSONObject(sb.toString());
                        JSONObject slots = root.optJSONObject("slots");
                        JSONObject slotObj = (slots != null && slots.has(slot))
                            ? slots.optJSONObject(slot)
                            : root.optJSONObject("latest");
                        if (slotObj != null) {
                            String cloudTitle = slotObj.optString("title", "");
                            String cloudBody = slotObj.optString("short_body", "");
                            if (!cloudTitle.isEmpty()) title = cloudTitle;
                            if (!cloudBody.isEmpty()) body = cloudBody;
                        }
                    }
                    conn.disconnect();
                } catch (Throwable netErr) {
                    Log.d(TAG, "Offline or feed unavailable, using local personalized cache: " + netErr.getMessage());
                }

                showNotification(context, title, body, "9pm".equals(slot) ? 9001 : 7001);
            } catch (Throwable t) {
                Log.e(TAG, "Error firing daily notification", t);
            } finally {
                if (pendingResult != null) pendingResult.finish();
            }
        }).start();
    }

    public static void ensureChannel(Context context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm != null && nm.getNotificationChannel(CHANNEL_ID) == null) {
                NotificationChannel ch = new NotificationChannel(
                    CHANNEL_ID,
                    "दैनिक पंचांग एवं व्यक्तिगत भविष्यफल",
                    NotificationManager.IMPORTANCE_HIGH
                );
                ch.setDescription("रात्रि 9:00 बजे और प्रातः 7:00 बजे दैनिक पंचांग, त्योहार-व्रत एवं व्यक्तिगत राशिफल सूचनाएं");
                nm.createNotificationChannel(ch);
            }
        }
    }

    public static void showNotification(Context context, String title, String body, int notifId) {
        ensureChannel(context);
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm == null) return;

        Intent openIntent = new Intent(context, MainActivity.class);
        openIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? PendingIntent.FLAG_IMMUTABLE : 0);
        PendingIntent contentIntent = PendingIntent.getActivity(context, notifId, openIntent, flags);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(new NotificationCompat.BigTextStyle().bigText(body))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(contentIntent);

        nm.notify(notifId, builder.build());
    }

    public static void scheduleDailyAlarms(Context context) {
        try {
            ensureChannel(context);
            AlarmManager am = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
            if (am == null) return;

            scheduleSlot(context, am, ACTION_9PM, 21, 0, 9001);
            scheduleSlot(context, am, ACTION_7AM, 7, 0, 7001);
            Log.i(TAG, "Scheduled daily alarms for 21:00 (9 PM) and 07:00 (7 AM)");
        } catch (Throwable t) {
            Log.e(TAG, "Failed to schedule alarms", t);
        }
    }

    private static void scheduleSlot(Context context, AlarmManager am, String action, int hour, int minute, int reqCode) {
        Intent intent = new Intent(context, DailyNotificationReceiver.class);
        intent.setAction(action);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? PendingIntent.FLAG_IMMUTABLE : 0);
        PendingIntent pi = PendingIntent.getBroadcast(context, reqCode, intent, flags);

        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, hour);
        cal.set(Calendar.MINUTE, minute);
        cal.set(Calendar.SECOND, 0);
        if (cal.getTimeInMillis() <= System.currentTimeMillis()) {
            cal.add(Calendar.DAY_OF_YEAR, 1);
        }

        am.setInexactRepeating(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), AlarmManager.INTERVAL_DAY, pi);
    }

    public static void savePersonalizedSlots(Context context, String title9pm, String body9pm, String title7am, String body7am) {
        SharedPreferences.Editor ed = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE).edit();
        if (title9pm != null && !title9pm.isEmpty()) ed.putString("title_9pm", title9pm);
        if (body9pm != null && !body9pm.isEmpty()) ed.putString("body_9pm", body9pm);
        if (title7am != null && !title7am.isEmpty()) ed.putString("title_7am", title7am);
        if (body7am != null && !body7am.isEmpty()) ed.putString("body_7am", body7am);
        ed.apply();
    }
}

