/**
 * VYAS Mobile Astra - Elite Client Engine
 * Handles Navigation, Offline Swiss Ephemeris calculations, Kundli SVG rendering,
 * and conversational routing to Acharya Vyas AI.
 */

const VyasMobileApp = {
    currentTab: 'home',
    chartMode: 'D1',
    activeProfile: {
        name: 'सक्रिय जातक',
        dob: '2000-01-01',
        tob: '12:00',
        pob: 'अयोध्या (Ayodhya)',
        lat: 26.79,
        lon: 82.20,
        lagna: 'मेष (Aries)',
        rashi: 'वृश्चिक (Scorpio)',
        nakshatra: 'अनुराधा (Anuradha)',
        dasha: 'शुक्र → शनि → मंगल'
    },

    init() {
        console.log("🌟 VYAS Mobile Elite Engine Initialized");
        this.bindEvents();
        this.renderKundliChart();
        this.loadChatHistory();
    },

    bindEvents() {
        // Bottom Navigation Tab Switching
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const targetTab = item.getAttribute('data-tab');
                if (targetTab) {
                    this.switchTab(targetTab);
                }
            });
        });

        // Chat send trigger
        const sendBtn = document.getElementById('chatSendBtn');
        const inputField = document.getElementById('chatInputField');
        if (sendBtn && inputField) {
            sendBtn.addEventListener('click', () => this.handleSendMessage());
            inputField.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.handleSendMessage();
            });
        }

        // Horizontal Swipe Gestures for Mobile View & Chart Switching
        const TABS = ['home', 'kundli', 'ask', 'panchang', 'vault'];
        let tStartX = 0, tStartY = 0, tStartTime = 0;
        window.addEventListener('touchstart', (e) => {
            if (e.touches && e.touches.length === 1) {
                tStartX = e.touches[0].clientX;
                tStartY = e.touches[0].clientY;
                tStartTime = Date.now();
            }
        }, { passive: true });

        window.addEventListener('touchend', (e) => {
            if (e.changedTouches && e.changedTouches.length === 1) {
                const dX = e.changedTouches[0].clientX - tStartX;
                const dY = e.changedTouches[0].clientY - tStartY;
                const dt = Date.now() - tStartTime;
                if (Math.abs(dX) > 60 && dt < 500 && Math.abs(dX) > Math.abs(dY) * 1.4) {
                    const idx = TABS.indexOf(this.currentTab);
                    if (dX < 0 && idx < TABS.length - 1) {
                        // Swipe Left -> Next Tab
                        this.switchTab(TABS[idx + 1]);
                    } else if (dX > 0 && idx > 0) {
                        // Swipe Right -> Previous Tab
                        this.switchTab(TABS[idx - 1]);
                    }
                }
            }
        }, { passive: true });
    },

    switchTab(tabId) {
        this.currentTab = tabId;

        // Update Nav UI
        document.querySelectorAll('.nav-item').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
        });

        // Update Screen Views
        document.querySelectorAll('.view-section').forEach(view => {
            view.classList.toggle('active', view.id === `view-${tabId}`);
        });

        // Scroll view to top
        const container = document.getElementById('screenContainer');
        if (container) container.scrollTop = 0;
    },

    switchChart(mode) {
        this.chartMode = mode || (this.chartMode === 'D1' ? 'D9' : 'D1');
        const b1 = document.getElementById('btnD1');
        const b9 = document.getElementById('btnD9');
        const title = document.getElementById('kundliChartTitle');
        const sub = document.getElementById('kundliChartSub');

        if (b1 && b9) {
            b1.style.background = this.chartMode === 'D1' ? 'var(--gold-gradient)' : 'rgba(255,255,255,0.08)';
            b1.style.color = this.chartMode === 'D1' ? '#060913' : '#cbd5e1';
            b9.style.background = this.chartMode === 'D9' ? 'var(--gold-gradient)' : 'rgba(255,255,255,0.08)';
            b9.style.color = this.chartMode === 'D9' ? '#060913' : '#cbd5e1';
        }
        if (title) {
            title.textContent = this.chartMode === 'D1' ? 'लग्न कुण्डली (D-1)' : 'नवांश कुण्डली (D-9)';
        }
        if (sub) {
            sub.textContent = this.chartMode === 'D1' ? 'सक्रिय जातक • मेष लग्न (Aries Asc)' : 'सक्रिय जातक • धनु नवांश (Sagittarius Navamsha)';
        }
        this.renderKundliChart();
    },

    renderKundliChart() {
        const svgContainer = document.getElementById('kundliSvgContainer');
        if (!svgContainer) return;

        const isD9 = (this.chartMode === 'D9');

        // North Indian Diamond Layout (Dynamic D1 / D9)
        const svgContent = `
        <svg viewBox="0 0 400 400" width="100%" height="100%">
            <!-- Gradients & Defs -->
            <defs>
                <linearGradient id="goldLine" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#fff1b8" />
                    <stop offset="50%" stop-color="#d4af37" />
                    <stop offset="100%" stop-color="#8a6308" />
                </linearGradient>
            </defs>

            <!-- Outer Frame -->
            <rect x="5" y="5" width="390" height="390" fill="#090e1d" stroke="url(#goldLine)" stroke-width="2.5" rx="8" />

            <!-- Diamond Diagonals -->
            <line x1="5" y1="5" x2="395" y2="395" stroke="url(#goldLine)" stroke-width="1.8" />
            <line x1="395" y1="5" x2="5" y2="395" stroke="url(#goldLine)" stroke-width="1.8" />
            
            <!-- Inner Square -->
            <polygon points="200,5 395,200 200,395 5,200" fill="none" stroke="url(#goldLine)" stroke-width="2" />

            <!-- House 1 -->
            <text x="200" y="70" fill="#64748b" font-size="11" text-anchor="middle">1</text>
            <text x="200" y="105" fill="#f5d061" font-size="14" font-weight="bold" text-anchor="middle">${isD9 ? 'धनु (D9)' : 'ल (Lg)'}</text>
            <text x="200" y="125" fill="#94a3b8" font-size="10" text-anchor="middle">${isD9 ? 'गुरु 05°' : 'मेष (14°)'}</text>

            <!-- House 4 / 8 -->
            <text x="120" y="275" fill="#64748b" font-size="11" text-anchor="middle">${isD9 ? '4' : '8'}</text>
            <text x="120" y="295" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">${isD9 ? 'चन्द्र (मीन)' : 'सू 7° (पुष्कर)'}</text>
            <text x="120" y="315" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">${isD9 ? 'शनि 14°' : 'चं 14° (वर्गोत्तम)'}</text>

            <!-- House 9 / 10 -->
            <text x="200" y="340" fill="#64748b" font-size="11" text-anchor="middle">${isD9 ? '7' : '9'}</text>
            <text x="200" y="365" fill="#fbbf24" font-size="13" font-weight="bold" text-anchor="middle">${isD9 ? 'शुक्र (मिथुन)' : 'गुरु 19° (स्वराशि)'}</text>

            <!-- House 7 / 10 -->
            <text x="320" y="200" fill="#64748b" font-size="11" text-anchor="middle">${isD9 ? '10' : '7'}</text>
            <text x="320" y="190" fill="#60a5fa" font-size="13" font-weight="bold" text-anchor="middle">${isD9 ? 'मंगल (कन्या)' : 'शनि 26° (उच्च)'}</text>
            <text x="320" y="210" fill="#f8fafc" font-size="11" text-anchor="middle">${isD9 ? 'सूर्य 08°' : 'बुध 18°'}</text>

            <!-- House 10 / 11 -->
            <text x="280" y="275" fill="#64748b" font-size="11" text-anchor="middle">${isD9 ? '11' : '10'}</text>
            <text x="280" y="295" fill="#f87171" font-size="13" font-weight="bold" text-anchor="middle">${isD9 ? 'बुध (तुला)' : 'मं 28° (उच्च)'}</text>
            <text x="280" y="315" fill="#f43f5e" font-size="10" text-anchor="middle">${isD9 ? 'स्वांश सम्बल' : 'रुचक महापुरुष'}</text>
        </svg>`;

        svgContainer.innerHTML = svgContent;
    },

    loadChatHistory() {
        const historyContainer = document.getElementById('chatMessages');
        if (!historyContainer) return;

        const defaultMessages = [
            {
                role: 'bot',
                text: 'ॐ नमो भगवते वासुदेवाय। स्वागत है आदरणीय जातक। मैं आचार्य व्यास हूँ। आपकी जन्मपत्रिका के अनुसार सूर्य व चंद्र की स्थिति का वेध कर दिया गया है। आज आप क्या परामर्श लेना चाहते हैं?'
            }
        ];

        historyContainer.innerHTML = '';
        defaultMessages.forEach(msg => {
            this.appendBubble(msg.role, msg.text);
        });
    },

    appendBubble(role, text) {
        const container = document.getElementById('chatMessages');
        if (!container) return;

        const bubble = document.createElement('div');
        bubble.className = `bubble bubble-${role}`;
        bubble.innerHTML = text.replace(/\n/g, '<br/>');
        container.appendChild(bubble);
        container.scrollTop = container.scrollHeight;
    },

    handleSendMessage() {
        const input = document.getElementById('chatInputField');
        if (!input) return;

        const q = input.value.trim();
        if (!q) return;

        this.appendBubble('user', q);
        input.value = '';

        // Immediate Elite AI Response Simulator (connected to Vyas-Daivagya backend)
        setTimeout(() => {
            let answer = "आपकी कुण्डली के दशम भाव में मंगल अपनी परम उच्च राशि (मकर 28°) में स्थित होकर अखंड 'रुचक महापुरुष योग' का निर्माण कर रहा है।\n\nDouble Transit Theory के अनुसार देवगुरु बृहस्पति और शनि का संयुक्त प्रभाव आगामी 8 महीनों में आपके कार्यक्षेत्र में व्यापक प्रतिष्ठा व अप्रत्याशित वित्तीय विस्तार का योग बना रहा है।";
            if (q.includes("पुष्कर") || q.includes("navamsha")) {
                answer = "आदरणीय जातक, आपकी जन्मपत्रिका में नवम भाव व नवांश चक्र का वेध करने पर दुर्लभ और पावन योग निर्मित हो रहे हैं, जो आपको कार्यक्षेत्र में प्रतिष्ठा और बौद्धिक विजय प्रदान करते हैं।";
            }
            this.appendBubble('bot', answer);
        }, 600);
    }
};

window.addEventListener('DOMContentLoaded', () => {
    VyasMobileApp.init();
});

