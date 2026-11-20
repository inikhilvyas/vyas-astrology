/**
 * VYAS ASTRA — Universal Mobile Swipe Navigation Engine
 * Enables native-feeling horizontal swipe gesture navigation across portal sub-pages.
 * Left Swipe ➔ Next Page in Sequence
 * Right Swipe ➔ Previous Page in Sequence
 */

(function () {
    if (typeof window === 'undefined') return;

    var PORTAL_PAGES = [
        { path: '/', name: 'जन्म कुण्डली' },
        { path: '/panchang/', name: 'वैदिक पंचांग' },
        { path: '/dasha/', name: 'दशा चक्र' },
        { path: '/kp-astrology/', name: 'KP पद्धति' },
        { path: '/jaimini-astrology/', name: 'जैमिनी ज्योतिष' },
        { path: '/nadi-astrology/', name: 'BNN नाड़ी' },
        { path: '/ashtakavarga/', name: 'अष्टकवर्ग चक्र' },
        { path: '/varshphal/', name: 'ताजिक वर्षफल' },
        { path: '/prashna-kundli/', name: 'प्रश्न कुण्डली' },
        { path: '/kundli-matching/', name: 'गुण मिलान' },
        { path: '/saved-kundli/', name: 'कुण्डली वॉल्ट' }
    ];

    function getCurrentPageIndex() {
        var curPath = window.location.pathname.replace(/\/+$/, '') + '/';
        if (curPath === '//' || curPath === '/') return 0;
        for (var i = 0; i < PORTAL_PAGES.length; i++) {
            var p = PORTAL_PAGES[i].path.replace(/\/+$/, '') + '/';
            if (curPath === p || curPath.indexOf(p) !== -1) {
                return i;
            }
        }
        return 0;
    }

    var touchStartX = 0;
    var touchStartY = 0;
    var touchStartTime = 0;

    window.addEventListener('touchstart', function (e) {
        if (!e.touches || e.touches.length !== 1) return;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        touchStartTime = Date.now();
    }, { passive: true });

    window.addEventListener('touchend', function (e) {
        if (!e.changedTouches || e.changedTouches.length !== 1) return;
        var deltaX = e.changedTouches[0].clientX - touchStartX;
        var deltaY = e.changedTouches[0].clientY - touchStartY;
        var deltaTime = Date.now() - touchStartTime;

        // Ensure swipe is deliberate, fast, and primarily horizontal
        // Minimum deltaX: 65px, Maximum time: 600ms, Horizontal dominant: |deltaX| > |deltaY| * 1.5
        if (Math.abs(deltaX) < 65 || deltaTime > 600) return;
        if (Math.abs(deltaX) < Math.abs(deltaY) * 1.4) return;

        // Ignore swipe if user was dragging a scrollable table, slider, or input
        var target = e.target;
        if (target && (target.tagName === 'INPUT' || target.tagName === 'SELECT' || target.tagName === 'TEXTAREA' || target.closest('.table-wrap') || target.closest('.no-swipe'))) {
            return;
        }

        var curIdx = getCurrentPageIndex();
        if (deltaX < 0) {
            // SWIPE LEFT ➔ NEXT PAGE
            if (curIdx < PORTAL_PAGES.length - 1) {
                var nextP = PORTAL_PAGES[curIdx + 1];
                showSwipeToast('◂ ' + nextP.name + ' लोड हो रहा है...');
                setTimeout(function () {
                    window.location.href = nextP.path;
                }, 160);
            }
        } else {
            // SWIPE RIGHT ➔ PREVIOUS PAGE
            if (curIdx > 0) {
                var prevP = PORTAL_PAGES[curIdx - 1];
                showSwipeToast(prevP.name + ' ▸ लोड हो रहा है...');
                setTimeout(function () {
                    window.location.href = prevP.path;
                }, 160);
            }
        }
    }, { passive: true });

    function showSwipeToast(msg) {
        var existing = document.getElementById('vyasSwipeToast');
        if (existing) existing.remove();

        var toast = document.createElement('div');
        toast.id = 'vyasSwipeToast';
        toast.style.position = 'fixed';
        toast.style.bottom = '75px';
        toast.style.left = '50%';
        toast.style.transform = 'translateX(-50%)';
        toast.style.background = 'rgba(12, 19, 36, 0.95)';
        toast.style.border = '1px solid #d4af37';
        toast.style.color = '#fcedaa';
        toast.style.padding = '8px 18px';
        toast.style.borderRadius = '24px';
        toast.style.fontSize = '0.82rem';
        toast.style.fontWeight = '700';
        toast.style.boxShadow = '0 8px 24px rgba(0,0,0,0.6)';
        toast.style.zIndex = '9999';
        toast.style.pointerEvents = 'none';
        toast.style.transition = 'opacity 0.2s ease';
        toast.textContent = msg;

        document.body.appendChild(toast);
    }
})();
