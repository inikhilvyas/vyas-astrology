# -*- coding: utf-8 -*-
import sys

def remove_early_returns():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix renderKP early return
    kp_old = """        renderKP() {
            var kp = (this.activeChartData && this.activeChartData.kp) ? this.activeChartData.kp : null;
            var cBody = document.getElementById('kpCuspsTableBody');
            if (!kp) {
                if (cBody) cBody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 12 कस्प सब-लॉर्ड्स प्रदर्शित होंगे।</td></tr>';
                return;
            }
            if (cBody && kp.cusps) {"""

    kp_new = """        renderKP() {
            var kp = (this.activeChartData && this.activeChartData.kp) ? this.activeChartData.kp : null;
            var cBody = document.getElementById('kpCuspsTableBody');
            if (!kp) {
                if (cBody) cBody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 12 कस्प सब-लॉर्ड्स प्रदर्शित होंगे।</td></tr>';
            } else if (cBody && kp.cusps) {"""

    if kp_old in content:
        content = content.replace(kp_old, kp_new, 1)
        print("✓ Removed early return in renderKP()")
    else:
        print("Warning: kp_old pattern not found")

    # 2. Fix renderJaimini early return
    jm_old = """        renderJaimini() {
            var jm = (this.activeChartData && this.activeChartData.jaimini) ? this.activeChartData.jaimini : null;
            var tbody = document.getElementById('jaiminiKarakasTableBody');
            if (!jm) {
                if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 7 चर कारक प्रदर्शित होंगे।</td></tr>';
                return;
            }
            if (tbody && jm.karakas) {"""

    jm_new = """        renderJaimini() {
            var jm = (this.activeChartData && this.activeChartData.jaimini) ? this.activeChartData.jaimini : null;
            var tbody = document.getElementById('jaiminiKarakasTableBody');
            if (!jm) {
                if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 7 चर कारक प्रदर्शित होंगे।</td></tr>';
            } else if (tbody && jm.karakas) {"""

    if jm_old in content:
        content = content.replace(jm_old, jm_new, 1)
        print("✓ Removed early return in renderJaimini()")
    else:
        print("Warning: jm_old pattern not found")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done removing early returns.")

if __name__ == '__main__':
    remove_early_returns()

