with open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

user_ledger_section = '''
    <!-- LOGGED-IN USERS AUDIT LEDGER (Zero Kundli Data - Privacy Sealed) -->
    <div style="background:var(--bg-card); border:1px solid rgba(212,175,55,0.3); border-radius:12px; padding:20px; margin-top:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
            <div>
                <h3 style="color:#fbbf24; font-size:1.15rem; margin-bottom:4px;">👥 पंजीकृत व लॉगिन यूज़र्स की सूची (Login Audit Ledger)</h3>
                <span style="font-size:0.80rem; color:var(--text-muted);">केवल वही यूज़र्स जिन्होंने Google से लॉगिन किया है • कोई व्यक्तिगत कुण्डली डेटा सर्वर पर नहीं रहता</span>
            </div>
            <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; padding:6px 14px; border-radius:20px; font-weight:700; color:#10b981; font-size:0.90rem;">
                कुल लॉगिन यूज़र्स: <span id="totalUsersCount">0</span>
            </div>
        </div>

        <div style="background:rgba(3,7,18,0.5); border:1px solid var(--border-subtle); border-radius:8px; overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:0.84rem; text-align:left;">
                <thead>
                    <tr style="border-bottom:1px solid var(--border-subtle); color:#9ca3af; background:rgba(255,255,255,0.02);">
                        <th style="padding:10px 14px;">क्र.</th>
                        <th style="padding:10px 14px;">यूज़र का नाम</th>
                        <th style="padding:10px 14px;">ईमेल (Email)</th>
                        <th style="padding:10px 14px;">प्रथम लॉगिन</th>
                        <th style="padding:10px 14px;">अंतिम सक्रियता</th>
                        <th style="padding:10px 14px;">लॉगिन आवृत्ति</th>
                    </tr>
                </thead>
                <tbody id="userLoginsTableBody">
                    <tr>
                        <td colspan="6" style="padding:16px; text-align:center; color:#9ca3af;">यूज़र्स सूची लोड हो रही है...</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div style="margin-top:12px; font-size:0.75rem; color:#64748b; display:flex; align-items:center; gap:6px;">
            <span>🔒</span> <b>प्राइवेसी सुरक्षा:</b> सर्वर पर किसी भी यूजर की जन्म कुण्डली, जन्म तारीख या जन्म समय का कोई डेटा संचित नहीं किया जाता। समस्त कुण्डलियाँ यूजर्स के निजी डिवाइस (ब्राउज़र / ऐप) पर ही एन्क्रिप्टेड रूप में सुरक्षित रहती हैं।
        </div>
    </div>
'''

js_fetch_users = '''
        async function fetchUserLogins() {
            var tbody = document.getElementById('userLoginsTableBody');
            var countEl = document.getElementById('totalUsersCount');
            try {
                var res = await fetch('/api/log_user_login.php');
                var d = await res.json();
                if (d.ok && Array.isArray(d.users)) {
                    if (countEl) countEl.innerText = d.total_unique_users;
                    if (d.users.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6" style="padding:16px; text-align:center; color:#9ca3af;">अभी तक किसी यूजर ने लॉगिन नहीं किया है।</td></tr>';
                        return;
                    }
                    var html = '';
                    d.users.forEach(function(u, idx) {
                        var first = u.first_login ? new Date(u.first_login).toLocaleString('hi-IN') : '-';
                        var last = u.last_login ? new Date(u.last_login).toLocaleString('hi-IN') : '-';
                        html += '<tr style="border-bottom:1px solid rgba(255,255,255,0.05);">' +
                            '<td style="padding:10px 14px; color:#9ca3af;">' + (idx + 1) + '</td>' +
                            '<td style="padding:10px 14px; font-weight:600; color:#f9fafb;">' + (u.name || 'जातक') + '</td>' +
                            '<td style="padding:10px 14px; color:#38bdf8; font-family:monospace;">' + (u.email || '-') + '</td>' +
                            '<td style="padding:10px 14px; color:#9ca3af;">' + first + '</td>' +
                            '<td style="padding:10px 14px; color:#10b981;">' + last + '</td>' +
                            '<td style="padding:10px 14px; color:#fbbf24; font-weight:700;">' + (u.login_count || 1) + ' बार</td>' +
                        '</tr>';
                    });
                    tbody.innerHTML = html;
                }
            } catch(e) {
                if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="padding:16px; text-align:center; color:#ef4444;">डेटा लोड करने में त्रुटि।</td></tr>';
            }
        }

        // Auto load on open
        fetchLiveStatus();
        fetchUserLogins();
'''

pos_grid_end = text.rfind('</div>', 0, text.find('<script>'))
# Insert before </script>
text = text.replace('        // Auto load on open\n        fetchLiveStatus();', js_fetch_users)
# Insert section before </script>
pos_script = text.find('<script>')
text = text[:pos_script] + user_ledger_section + '\n\n    ' + text[pos_script:]

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✓ Successfully updated admin.html with User Logins Ledger")

