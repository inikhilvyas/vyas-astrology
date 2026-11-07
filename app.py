import streamlit as st

def format_bold_clean(text: str) -> str:
    """Converts any markdown bold/italic asterisks into clean HTML <b> tags."""
    if not text or not isinstance(text, str):
        return str(text) if text is not None else ""
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    t = re.sub(r'(?<!\*)\*([A-Za-z\u0900-\u097F0-9_ -]+)\*(?!\*)', r'<b>\1</b>', t)
    return t

def render_modern_table(data_rows, title: str = "", badge_cols: dict = None) -> str:
    """Renders a list of dicts as an ultra-modern, responsive HTML glass table."""
    if not data_rows:
        return ""
    if isinstance(data_rows, pd.DataFrame):
        records = data_rows.to_dict(orient="records")
    else:
        records = list(data_rows)
    if not records:
        return ""
    headers = list(records[0].keys())
    th_cells = "".join([f'<th style="padding: 11px 14px; text-align: left; font-size: 0.90rem; font-weight: 800; color: #f0c05a; background: rgba(15, 23, 42, 0.95); border-bottom: 2px solid rgba(240, 192, 90, 0.35); white-space: nowrap;">{h}</th>' for h in headers])
    
    tr_rows = []
    for idx, row in enumerate(records):
        bg = "rgba(15, 23, 42, 0.55)" if idx % 2 == 0 else "rgba(15, 23, 42, 0.30)"
        td_cells = []
        for h in headers:
            val = str(row.get(h, ""))
            val_clean = format_bold_clean(val)
            # Apply color badge if matching
            if any(w in val for w in ["सर्वश्रेष्ठ", "प्रबल", "उच्च", "शुभ", "अति शुभ", "Exalted", "Own Sign"]):
                val_disp = f'<span style="background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.82rem;">{val_clean}</span>'
            elif any(w in val for w in ["सावधानी", "अल्प", "नीच", "अशुभ", "क्रूर", "Debilitated", "Enemy"]):
                val_disp = f'<span style="background: rgba(239, 68, 68, 0.18); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.82rem;">{val_clean}</span>'
            elif any(w in val for w in ["मध्यम", "सामान्य", "Neutral"]):
                val_disp = f'<span style="background: rgba(56, 189, 248, 0.18); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 0.82rem;">{val_clean}</span>'
            else:
                val_disp = val_clean
            td_cells.append(f'<td style="padding: 10px 14px; font-size: 0.88rem; color: #f1f5f9; border-bottom: 1px solid rgba(255,255,255,0.06); line-height: 1.5;">{val_disp}</td>')
        tr_rows.append(f'<tr style="background: {bg}; transition: background 0.2s;">{"".join(td_cells)}</tr>')

    title_html = f'<div style="font-weight: 800; color: #f0c05a; font-size: 1.05rem; margin-bottom: 8px;">{title}</div>' if title else ""
    return f"""<div style="width: 100%; max-width: 100%; margin: 12px 0 16px 0;">
{title_html}
<div style="width: 100%; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 16px rgba(0,0,0,0.25);">
<table style="width: 100%; min-width: 100%; max-width: 100%; border-collapse: collapse; text-align: left;">
<thead><tr>{th_cells}</tr></thead>
<tbody>{"".join(tr_rows)}</tbody>
</table>
</div>
</div>"""


# Backward/forward compatibility shims across Streamlit versions
if not hasattr(st, "dialog") and hasattr(st, "experimental_dialog"):
    st.dialog = st.experimental_dialog

if not hasattr(st, "iframe"):
    try:
        import streamlit.components.v1 as _comp
        st.iframe = _comp.html
    except Exception:
        pass
from datetime import datetime, timezone, timedelta, time as d_time
import sys
import os
import shutil
import platform
import re
import urllib.parse
import pandas as pd
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
except ImportError:
    Nominatim = None
    GeocoderTimedOut = Exception
import base64

# Ensure the vyas module is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from vyas.ephem import planet_positions, ascendant_sidereal
from vyas.chart import Chart, PlanetState
from vyas.varga import calculate_vargas_detailed, get_all_vargas_matrix, format_dms as format_varga_dms, SIGNS as VARGA_SIGNS
from vyas import constants
from vyas.svg_chart import get_north_indian_chart_svg, get_south_indian_chart_svg
from vyas.kp import (
    calculate_placidus_cusps_sidereal,
    calculate_sub_lords,
    compute_kp_significators,
    get_ruling_planets,
    KPCusp,
    calculate_planet_kp_lords,
    compute_kp_4fold_house_significators,
    evaluate_kp_house_promises,
    evaluate_active_houses_by_dasha
)
from vyas.dasha import VimshottariDasha
from vyas import ephem as vyas_ephem
from vyas import panchang as vyas_panchang
from vyas import gochar as vyas_gochar
from vyas.predictive_engine import synthesize_prediction
from vyas import chakras as vyas_chakras
from vyas import nadi as vyas_nadi
from vyas import sutra_bank as vyas_sutra_bank
from vyas import knowledge_engine as vyas_knowledge_engine
from vyas import ashtakavarga as vyas_ashtaka
from vyas import shadbala as vyas_shadbala
from vyas import chalit as vyas_chalit
from vyas import jaimini as vyas_jaimini
from vyas import forensic_predictor
from vyas import publication_engine
from vyas import auth_vault
from vyas import lalkitab as vyas_lalkitab
from vyas import daily_horoscope as vyas_daily
from vyas import btr as vyas_btr
from vyas import varga_predictions as vyas_vp
from vyas import match as vyas_match
from vyas import prashna as vyas_prashna
from vyas.chatbot import vyas_chatbot
try:
    from vyas import city_search
except Exception:
    city_search = None
from vyas import google_drive_sync

# ---------------- AUTH SESSION HELPERS ----------------
# A signed-in user must survive a full page reload, but Streamlit Cloud has no
# server-side session: the old get_last_active_user() restored the SAME account
# for every visitor (one shared row). Instead each browser gets an opaque token
# cookie that maps to exactly one account.
_SESSION_COOKIE = "vyas_sess"


def _read_session_cookie() -> str:
    try:
        return str((st.context.cookies or {}).get(_SESSION_COOKIE, "") or "")
    except Exception:
        return ""


def _write_session_cookie(token: str) -> None:
    """Sets/clears the browser token. SameSite=None so it also works when the
    app is embedded in Streamlit Cloud's sharing iframe."""
    try:
        if token:
            _js = (
                f"document.cookie='{_SESSION_COOKIE}={token}; path=/; "
                "max-age=2592000; SameSite=None; Secure';"
            )
        else:
            _js = (
                f"document.cookie='{_SESSION_COOKIE}=; path=/; "
                "max-age=0; SameSite=None; Secure';"
            )
        _snippet = f"<script>{_js}</script>"
        # st.iframe is the documented replacement for components.html, but it
        # drops <script>, which is exactly what is needed here — so keep using
        # components.html and fall back to st.iframe only if it is gone.
        try:
            import streamlit.components.v1 as _components
            _components.html(_snippet, height=0)
        except Exception:
            if hasattr(st, "iframe"):
                st.components.v1.html(_snippet, height=0)
    except Exception:
        pass


# ---------------- DURABLE BROWSER SESSION (localStorage bridge) ----------------
# Streamlit Community Cloud's proxy forwards only an allowlist of cookies to
# the app. A custom `vyas_sess` cookie is stored in the browser (document.cookie
# shows it) but arrives EMPTY in st.context.cookies on Cloud, so every reload
# fell back to the logged-out landing page. This zero-height bidirectional
# component runs in the app page itself (no sandboxed iframe), so it can read
# and write localStorage and hand the token back to Python through component
# state — a channel the proxy cannot strip.
_SESSION_STORE_KEY = "vyas_session_v1"
_SESSION_STORE_JS = r"""
export default function (component) {
    const { setStateValue, data } = component;
    const KEY = 'vyas_session_v1';
    const action = (data && data.action) || 'read';
    try {
        if (action === 'store' && data && data.token) {
            localStorage.setItem(KEY, data.token);
            setStateValue('token', data.token);
        } else if (action === 'clear') {
            localStorage.removeItem(KEY);
            setStateValue('token', '');
        } else {
            setStateValue('token', localStorage.getItem(KEY) || '');
        }
    } catch (err) {
        setStateValue('token', '');
    }
}
"""

try:
    _SESSION_COMPONENT = st.components.v2.component(
        "vyas_session_store", js=_SESSION_STORE_JS
    )
except Exception:
    _SESSION_COMPONENT = None


def _mount_session_bridge(action: str = "read", token: str = "") -> str:
    """Reads/stores/clears the browser session token (empty on any failure)."""
    if _SESSION_COMPONENT is None:
        return ""
    try:
        result = _SESSION_COMPONENT(
            data={"action": action, "token": token},
            default={"token": ""},
            key="vyas_session_bridge",
            on_token_change=lambda: None,
            height=0,
            width="stretch",
        )
        return str(getattr(result, "token", "") or "")
    except Exception:
        return ""


def _load_kundli_into_session(chosen_k, make_default=False, user_id=None):
    """Loads a saved kundli profile into active session and marks data ready without widget conflicts."""
    if not chosen_k:
        return
    st.session_state['loaded_profile'] = dict(chosen_k)
    st.session_state['lat'] = float(chosen_k.get('lat', 28.6139))
    st.session_state['lon'] = float(chosen_k.get('lon', 77.2090))
    c_name = chosen_k.get('city', 'New Delhi, India')
    st.session_state['city_name'] = c_name
    st.session_state['_last_chosen_city'] = c_name
    st.session_state['_pending_city_search_input'] = c_name
    try:
        st.session_state['city_search_input'] = c_name
    except Exception:
        pass
    st.session_state.pop('selected_city_dropdown', None)
    st.session_state.pop('_birth_input_sig', None)
    st.session_state['data_generated'] = True
    st.session_state['show_birth_form'] = False
    if make_default and user_id and chosen_k.get("id"):
        try:
            auth_vault.set_default_kundli(user_id, int(chosen_k["id"]))
        except Exception:
            pass


def _start_user_session(u_obj) -> None:
    """Marks the user signed in for this session and remembers this browser."""
    if not u_obj:
        return
    st.session_state["user"] = u_obj
    try:
        auth_vault.set_active_session_user(u_obj["id"])
    except Exception:
        pass
    try:
        token = auth_vault.create_session_token(u_obj["id"])
    except Exception:
        token = ""
    if token:
        st.session_state["_vyas_session_token"] = token
        # Both are written on the NEXT run: this call is followed by st.rerun(),
        # which discards any element (including the cookie script) created in
        # the current run.
        st.session_state["_vyas_store_pending"] = token
        st.session_state["_vyas_cookie_pending"] = True

    # Automatically load user's default/saved kundli
    try:
        _auto_k = auth_vault.get_default_or_latest_kundli(u_obj["id"])
        if _auto_k:
            _load_kundli_into_session(_auto_k, user_id=u_obj["id"])
        else:
            st.session_state.pop('loaded_profile', None)
            st.session_state['show_birth_form'] = True
            st.session_state['data_generated'] = False
    except Exception:
        pass


def _end_user_session() -> None:
    """Logs out: invalidates the token, clears the cookie and session flags."""
    token = st.session_state.pop("_vyas_session_token", "") or _read_session_cookie()
    try:
        auth_vault.delete_session_token(token)
    except Exception:
        pass
    try:
        auth_vault.clear_active_session()
    except Exception:
        pass
    st.session_state["_vyas_cookie_pending"] = True  # clears it on the next run
    st.session_state["_vyas_clear_pending"] = True
    st.session_state["user"] = {
        "id": 1,
        "name": "नया जातक (Seeker)",
        "email": "seeker@vyasastro.com",
        "tier": "VIP_TRIAL",
        "days_left": 30,
        "is_vip": True,
    }
    for _sk in ("loaded_profile", "google_access_token", "user_google_processed",
                "oauth_state", "gdrive_last_link", "saved_k_picker",
                "oauth_code_verifier", "data_generated", "show_birth_form",
                "_birth_input_sig", "chart", "birth", "kp_cusps", "dasha_engine",
                "vargas_matrix", "panchang", "gochar", "predictions"):
        st.session_state.pop(_sk, None)



def get_svg_vector(name: str, size: int = 18, color: str = "#f0c05a") -> str:
    """Returns crisp inline SVG vector graphics (replacing emojis with store-grade iconography)."""
    n = (name or "").lower().strip()
    s = size
    if n in ("career", "work", "job", "profession", "business"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>'
    elif n in ("wealth", "money", "finance", "dhana"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><circle cx="12" cy="12" r="9"></circle><path d="M12 6v12M15 9.5H9.5a2.5 2.5 0 0 1 0-5H14M10 19.5h4.5a2.5 2.5 0 0 0 0-5H9"></path></svg>'
    elif n in ("intellect", "brain", "mind", "buddhi"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04z"></path><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04z"></path></svg>'
    elif n in ("health", "ayurveda", "body", "leaf"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><path d="M11 20A7 7 0 0 1 4 13a8 8 0 0 1 12-7 8 8 0 0 1 7 12 7 7 0 0 1-7 7M2 21c0-5 3.5-9 9-9"></path></svg>'
    elif n in ("marriage", "spouse", "partner", "union"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><circle cx="8" cy="12" r="5"></circle><circle cx="16" cy="12" r="5"></circle></svg>'
    elif n in ("education", "learning", "knowledge", "vidya"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>'
    elif n in ("children", "family", "santana"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><circle cx="12" cy="7" r="4"></circle><path d="M5.5 21a6.5 6.5 0 0 1 13 0"></path></svg>'
    elif n in ("protection", "defense", "shield"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
    elif n in ("travel", "foreign", "globe"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    elif n in ("spirituality", "dharma", "moksha", "temple"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><circle cx="12" cy="12" r="9"></circle><path d="M12 3v18M3 12h18"></path><circle cx="12" cy="12" r="3"></circle></svg>'
    elif n in ("destiny", "luck", "fortune", "star"):
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
    else:
        return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; display: inline-block;"><polygon points="12 2 22 12 12 22 2 12 12 2"></polygon></svg>'

def render_kundli(svg_str: str):
    """Render astrological SVG cleanly via base64 data URI with crisp high-DPI scaling."""
    clean = re.sub(r'<!--.*?-->', '', svg_str, flags=re.DOTALL)
    clean = re.sub(r'\s+', ' ', clean).strip()
    b64 = base64.b64encode(clean.encode('utf-8')).decode('utf-8')
    st.markdown(f'<div class="kundli-container" style="text-align: center; margin: 8px auto;"><img src="data:image/svg+xml;base64,{b64}" style="width: 100%; max-width: 650px; height: auto; display: block; margin: 0 auto; filter: drop-shadow(0 10px 25px rgba(0,0,0,0.65)); border-radius: 12px;" /></div>', unsafe_allow_html=True)


def lazy_sections(labels, key: str):
    """A tab strip that renders ONLY the selected section's body.

    ``st.tabs`` runs every tab body on every rerun: with 8 tab groups (one nine
    tabs wide, plus nested four-tab sets) the app rebuilt the Panchang engine
    (~2.2s), the transit engine (~1.4s), 34 dataframes and 4 large SVG charts
    even while the user was reading the first tab.

    ``with tab:`` cannot skip work — Python always executes the body — so this
    returns a list of booleans instead, and call sites become::

        _lz = lazy_sections(["A", "B", "C"], key="forecast")
        if _lz[0]:
            ...expensive A...
        if _lz[1]:
            ...expensive B...

    Because the unselected bodies never execute, their engines, dataframes and
    charts are never built. Selection lives in session_state, so it survives
    reruns triggered by widgets elsewhere on the page.
    """
    active = st.radio(
        "",
        options=list(range(len(labels))),
        format_func=lambda i: labels[i],
        index=0,
        key=f"lazytab_{key}",
        horizontal=True,
        label_visibility="collapsed",
    )
    return [i == active for i in range(len(labels))]

_VYAS_LOGO_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_icon.png")
st.set_page_config(
    page_title="VYAS • Vedic Yield Astrology Systems",
    page_icon=_VYAS_LOGO_ICON if os.path.exists(_VYAS_LOGO_ICON) else "",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------- CACHED HEAVY ENGINES ----------------
# Measured on a real chart (Windows, cold pyephem/Skyfield):
#   panchang.compute  ~2.2s   gochar.transits ~1.4s   planet_positions ~1.5s
# Streamlit reruns the whole script on EVERY widget interaction, so without
# caching the user paid ~5s of astronomy for something as trivial as opening an
# expander. These wrappers memoise on the *inputs that actually matter*, so a
# rerun with unchanged birth data costs ~0ms.
#
# Dataclass results are converted to plain dicts because st.cache_data pickles
# its return value (and the index argument lets callers rehydrate cheaply).
@st.cache_data(show_spinner=False, max_entries=64)
def _cached_panchang(dt_local, lat: float, lon: float, tz_hours: float, asc_lon: float):
    """Full Panchang for a local datetime. Keyed on date+time+place+ayanamsa."""
    return vyas_panchang.compute(dt_local, lat, lon, tz_hours, asc_lon)


@st.cache_data(show_spinner=False, max_entries=64)
def _cached_gochar_transits(now_day: str, tz_hours: float, moon_lon: float, asc_lon: float):
    """Transit/ingress table for the given day. Keyed on the DAY, not the second,
    so moving between tabs on the same day never recomputes."""
    return vyas_gochar.transits(
        datetime.fromisoformat(now_day), tz_hours, moon_lon, asc_lon, with_ingress=True
    )


@st.cache_data(show_spinner=False, max_entries=64)
def _cached_transit_positions(now_day: str):
    """Current transit positions for the given day (planet -> object with
    longitude/speed/sign_index)."""
    return vyas_gochar.get_current_transit_positions()

# ---------------- FONT LOADING (non-blocking, exactly once) ----------------
# Preconnect warms the TLS handshake to both font hosts while the HTML is still
# parsing, so the stylesheet request starts ~200-400ms earlier than it otherwise
# would. `display=swap` means text paints immediately in the fallback stack and
# reflows once webfonts arrive — the page is never held hostage by fonts.google
# .com, which is the single biggest first-paint cost on a cold Streamlit load.
st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yatra+One&family=Cinzel:wght@600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Tiro+Devanagari+Sanskrit&family=Noto+Sans+Devanagari:wght@400;500;600;700;800;900&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap">
""")

# ---------------- GOOGLE OAUTH 2.0 CALLBACK HANDLING ----------------
# Rules:
#  1. Google errors (redirect_uri_mismatch, access_denied...) are surfaced, never ignored.
#  2. `state` must match the per-session nonce generated at login (CSRF protection).
#  3. A code is processed exactly once — success OR failure — so a consumed
#     single-use code is never re-sent to Google on every rerun (invalid_grant loop).
_oauth_code = st.query_params.get("code")
_oauth_state = st.query_params.get("state")
_oauth_error = st.query_params.get("error")
_oauth_err_desc = st.query_params.get("error_description")

if _oauth_error:
    # Google bounced back with an error — show it and clean the URL.
    st.session_state["user_google_processed"] = True
    _eff_ruri = google_drive_sync.resolve_redirect_uri(
        google_drive_sync.load_google_config().get("redirect_uri", "")
    )
    google_drive_sync.record_oauth_error(
        f"google_redirected_back error={_oauth_error} desc={_oauth_err_desc or '-'} redirect_uri={_eff_ruri}"
    )
    st.error(f"Google लॉगिन विफल: {_oauth_error} — {_oauth_err_desc or 'कृपया पुनः प्रयास करें।'}\n\n"
             f"**Redirect URI:** `{_eff_ruri}` — यह Google Cloud Console → Credentials → "
             f"OAuth client → **Authorized redirect URIs** में हूबहू होना चाहिए।")
    st.query_params.clear()

elif _oauth_code and not st.session_state.get("user_google_processed"):
    st.session_state["user_google_processed"] = True  # mark BEFORE any network call

    if not google_drive_sync.verify_oauth_state(_oauth_state):
        google_drive_sync.record_oauth_error(f"state_mismatch received={(_oauth_state or '')[:12]}")
        st.error("लॉगिन सुरक्षा जाँच विफल (state mismatch)। कृपया पेज रीफ़्रेश करके दोबारा लॉगिन करें।")
        st.query_params.clear()
    else:
        with st.spinner("Google से प्रमाणीकरण एवं Google Drive सिंक किया जा रहा है..."):
            ok_tok, msg_tok, tok_data = google_drive_sync.exchange_code_for_tokens(_oauth_code)
            _login_err = None
            if not ok_tok or not tok_data:
                _login_err = f"चरण 1 (टोकन प्राप्ति) विफल: {msg_tok}"
            else:
                acc_tok = tok_data.get("access_token")
                ref_tok = tok_data.get("refresh_token", "")
                ok_ui, msg_ui, u_info = google_drive_sync.get_user_info(acc_tok)
                if not ok_ui or not u_info:
                    _login_err = f"चरण 2 (प्रोफ़ाइल प्राप्ति) विफल: {msg_ui}"
                else:
                    ok_log, msg_log, u_obj = auth_vault.login_or_register_google(u_info["email"], u_info["name"])
                    if not ok_log or not u_obj:
                        _login_err = f"चरण 3 (खाता) विफल: {msg_log}"
                    elif not auth_vault.save_google_tokens(u_obj["id"], acc_tok, ref_tok):
                        _login_err = ("लॉगिन सफल हुआ, परंतु Drive टोकन सुरक्षित नहीं हो सका "
                                      "(डेटाबेस त्रुटि)। Drive सिंक काम नहीं करेगा।")
                    else:
                        st.session_state["google_access_token"] = acc_tok
                        _start_user_session(u_obj)
                        google_drive_sync.clear_oauth_error()

            if _login_err:
                google_drive_sync.record_oauth_error(_login_err)
                st.error(f"Google लॉगिन विफल — {_login_err}")
            else:
                st.toast(f"Google से सफल लॉगिन: {u_obj['name']}! Google Drive कनेक्ट हो गया।", icon="")
            st.query_params.clear()
            st.session_state.pop("oauth_state", None)
            st.rerun()

# PWA Manifest & Native Mobile Responsive Viewport Engine
st.markdown('''
<link rel="manifest" href="static/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
<meta name="theme-color" content="#e5a93c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="mobile-web-app-capable" content="yes">
<script>
(function() {
    try {
        var pDoc = window.parent.document;
        var meta = pDoc.querySelector('meta[name="viewport"]');
        if (!meta) {
            meta = pDoc.createElement('meta');
            meta.name = 'viewport';
            pDoc.head.appendChild(meta);
        }
        meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover';
    } catch(e) {}
})();
</script>
''', unsafe_allow_html=True)


# ---------------- EARLY THEME RESOLUTION ----------------
_active_theme_mode = st.session_state.get("_user_theme_mode", "डार्क थीम (Dark)")
_is_light = "लाइट" in str(_active_theme_mode) or "Light" in str(_active_theme_mode) or "कंट्रास्ट" in str(_active_theme_mode)

# High-contrast Theme Design Tokens for 100% Legibility in Light & Dark Mode
TH_GOLD = "#1e3a8a" if _is_light else "#f0c05a"
TH_GOLD_TITLE = "#1e3a8a" if _is_light else "#ffd700"
TH_GOLD_ACCENT = "#2563eb" if _is_light else "#fbbf24"
TH_MUTED = "#1e293b" if _is_light else "#cbd5e1"
TH_NAME = "#0f172a" if _is_light else "#ffffff"
TH_CARD_BG = "#ffffff" if _is_light else "linear-gradient(135deg, rgba(240,192,90,0.18) 0%, rgba(14,23,42,0.96) 100%)"
TH_CARD_BORDER = "1.5px solid rgba(37, 99, 235, 0.35)" if _is_light else "1.8px solid #f0c05a"
TH_BADGE_BG = "#eff6ff" if _is_light else "rgba(0,0,0,0.4)"
TH_BADGE_TEXT = "#1e3a8a" if _is_light else "#cbd5e1"
TH_BADGE_BORDER = "1.5px solid #93c5fd" if _is_light else "1px solid rgba(240,192,90,0.25)"

# Global Luxury Vedic Styling & Mobile-First Responsive Framework
_light_css_rules = """
        :root {
            --gold-primary: #1e3a8a !important;
            --gold-light: #1e40af !important;
            --gold-accent: #2563eb !important;
            --bg-deep: #f8fafc !important;
            --bg-surface: #ffffff !important;
            --card-bg: #ffffff !important;
            --card-border: rgba(15, 23, 42, 0.16) !important;
            --card-border-hover: rgba(37, 99, 235, 0.55) !important;
            --accent-ruby: #dc2626 !important;
            --accent-emerald: #15803d !important;
            --text-main: #0f172a !important;
            --text-muted: #334155 !important;
            --vyas-gold-1: #1e3a8a !important;
            --vyas-gold-2: #2563eb !important;
            --vyas-gold-3: #1d4ed8 !important;
            --vyas-line: rgba(37, 99, 235, 0.24) !important;
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container, section[data-testid="stSidebar"] {
            background: #f8fafc !important;
            background-image: none !important;
            color: #0f172a !important;
        }

        .glass-card, .predict-card, [data-testid="stExpander"] {
            background: #ffffff !important;
            background-image: none !important;
            border: 1.5px solid rgba(15, 23, 42, 0.16) !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05) !important;
            color: #0f172a !important;
        }

        .glass-card p, .predict-card p, .glass-card div, .predict-card div, [data-testid="stExpander"] p, [data-testid="stExpander"] div {
            color: #1e293b !important;
        }

        .vyas-hero-banner {
            background: #ffffff !important;
            background-image: none !important;
            border: 2px solid #2563eb !important;
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.08) !important;
        }
        .vyas-hero-kicker {
            color: #1e40af !important;
            font-size: 0.74rem !important;
        }
        .vyas-hero-title {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #1d4ed8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-shadow: none !important;
        }
        .vyas-hero-subtitle {
            color: #334155 !important;
        }
        .section-title, h1, h2, h3, h4, h5 {
            color: #1e3a8a !important;
            border-bottom-color: rgba(30, 58, 138, 0.25) !important;
        }

        /* Override ALL dark boxes and dark linear gradients to pure white cards in Light Mode */
        [style*="background: linear-gradient"],
        [style*="background:linear-gradient"],
        [style*="background: rgba(14, 23, 42"], [style*="background:rgba(14,23,42"],
        [style*="background: rgba(15, 23, 42"], [style*="background:rgba(15,23,42"],
        [style*="background: rgba(16, 26, 52"], [style*="background:rgba(16,26,52"],
        [style*="background: rgba(19, 27, 54"], [style*="background:rgba(19,27,54"],
        [style*="background: rgba(8, 12, 26"], [style*="background:rgba(8,12,26"],
        [style*="background: rgba(10, 16, 32"], [style*="background:rgba(10,16,32"],
        [style*="background: rgba(9, 14, 30"], [style*="background:rgba(9,14,30"],
        [style*="background: rgba(0, 0, 0"], [style*="background: rgba(0,0,0"],
        [style*="background: rgba(2, 6, 23"], [style*="background:rgba(2,6,23"],
        [style*="background: #060c18"], [style*="background:#060c18"],
        [style*="background: #0b1220"], [style*="background:#0b1220"],
        [style*="background: #07090d"], [style*="background:#07090d"] {
            background: #ffffff !important;
            background-image: none !important;
            border: 1.5px solid rgba(15, 23, 42, 0.15) !important;
            color: #0f172a !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        }

        /* Ensure ALL children of neutralized dark containers have deep navy/slate text */
        [style*="background: linear-gradient"] p, [style*="background: linear-gradient"] span, [style*="background: linear-gradient"] div,
        [style*="background:linear-gradient"] p, [style*="background:linear-gradient"] span, [style*="background:linear-gradient"] div,
        [style*="background: rgba(14, 23, 42"] p, [style*="background: rgba(14, 23, 42"] span, [style*="background: rgba(14, 23, 42"] div,
        [style*="background: rgba(15, 23, 42"] p, [style*="background: rgba(15, 23, 42"] span, [style*="background: rgba(15, 23, 42"] div,
        [style*="background: rgba(19, 27, 54"] p, [style*="background: rgba(19, 27, 54"] span, [style*="background: rgba(19, 27, 54"] div,
        [style*="background: rgba(0, 0, 0"] p, [style*="background: rgba(0, 0, 0"] span, [style*="background: rgba(0, 0, 0"] div,
        [style*="background: rgba(0,0,0"] p, [style*="background: rgba(0,0,0"] span, [style*="background: rgba(0,0,0"] div {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        /* Replace ALL golden/yellow text colors with Deep Royal Navy Blue in Light Mode */
        [style*="color: #f0c05a"], [style*="color:#f0c05a"],
        [style*="color: #ffd700"], [style*="color:#ffd700"],
        [style*="color: #fbbf24"], [style*="color:#fbbf24"],
        [style*="color: #facc15"], [style*="color:#facc15"],
        [style*="color: #eedc9a"], [style*="color:#eedc9a"],
        [style*="color: #fef3c7"], [style*="color:#fef3c7"],
        [style*="color: #ffd97d"], [style*="color:#ffd97d"],
        [style*="color: #e5a93c"], [style*="color:#e5a93c"],
        [style*="color: #f5d16e"], [style*="color:#f5d16e"],
        [style*="color: #b45309"], [style*="color:#b45309"],
        [style*="color: #92400e"], [style*="color:#92400e"] {
            color: #1e3a8a !important;
            font-weight: 800 !important;
        }

        /* Replace ALL white/light-grey text colors with Deep Slate in Light Mode */
        [style*="color: #f8fafc"], [style*="color:#f8fafc"],
        [style*="color: #f1f5f9"], [style*="color:#f1f5f9"],
        [style*="color: #cbd5e1"], [style*="color:#cbd5e1"],
        [style*="color: #94a3b8"], [style*="color:#94a3b8"],
        [style*="color: #e2e8f0"], [style*="color:#e2e8f0"],
        [style*="color: #ffffff"], [style*="color:#ffffff"],
        [style*="color: white"], [style*="color:white"] {
            color: #0f172a !important;
        }

        /* ALL Radio Buttons & Nav Pills in Light Mode (Main Content & Sidebar) */
        div[data-testid="stRadio"] [role="radiogroup"],
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
            background: #f1f5f9 !important;
            border: 1.5px solid #cbd5e1 !important;
            padding: 6px !important;
            border-radius: 999px !important;
        }
        div[data-testid="stRadio"] [role="radiogroup"] label,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 999px !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
            padding: 8px 18px !important;
        }
        div[data-testid="stRadio"] [role="radiogroup"] label *,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label * {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked),
        div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border-color: #1d4ed8 !important;
            box-shadow: 0 3px 12px rgba(37,99,235,0.35) !important;
        }
        div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) *,
        div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] *,
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) * {
            color: #ffffff !important;
            font-weight: 800 !important;
        }

        /* Complete 100% Selectbox, Input, Popover & Descendant Theme Fix in Light/Contrast Mode */
        div[data-testid="stSelectbox"],
        div[data-testid="stSelectbox"] div,
        div[data-testid="stSelectbox"] span,
        div[data-testid="stSelectbox"] p,
        div[data-baseweb="select"],
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input,
        div[data-baseweb="input"],
        div[data-baseweb="input"] div,
        div[data-baseweb="input"] input,
        div[data-testid="stTextInput"] div,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] div,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] div,
        div[data-testid="stDateInput"] input,
        div[data-testid="stTimeInput"] div,
        div[data-testid="stTimeInput"] input {
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        /* Distinct Border & Radius for Selectbox Container */
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border: 1.8px solid #94a3b8 !important;
            border-radius: 10px !important;
            background: #ffffff !important;
            background-color: #ffffff !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        }

        /* SVG arrows and icons inside Selectbox */
        div[data-testid="stSelectbox"] svg,
        div[data-baseweb="select"] svg {
            fill: #0f172a !important;
            color: #0f172a !important;
        }

        /* Dropdown Popover Menus (when clicked) */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] div,
        div[data-baseweb="menu"],
        div[data-baseweb="menu"] div,
        ul[data-baseweb="menu"],
        ul[data-baseweb="menu"] li,
        ul[role="listbox"],
        ul[role="listbox"] li,
        li[role="option"],
        li[role="option"] div,
        li[role="option"] span,
        li[data-baseweb="menu-item"],
        li[data-baseweb="menu-item"] div,
        li[data-baseweb="menu-item"] span {
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }
        li[data-baseweb="menu-item"]:hover,
        li[data-baseweb="menu-item"]:hover div,
        li[data-baseweb="menu-item"]:hover span,
        li[role="option"]:hover,
        li[role="option"]:hover div,
        li[role="option"]:hover span,
        li[aria-selected="true"],
        li[aria-selected="true"] div,
        li[aria-selected="true"] span {
            background: #dbeafe !important;
            background-color: #dbeafe !important;
            color: #1e3a8a !important;
            -webkit-text-fill-color: #1e3a8a !important;
            font-weight: 800 !important;
        }

        /* Sidebar in Light Mode */
        section[data-testid="stSidebar"] {
            background: #f8fafc !important;
            border-right: 1.5px solid rgba(15, 23, 42, 0.15) !important;
            color: #0f172a !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
            border-radius: 12px !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
            border-radius: 8px !important;
        }
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] p {
            color: #0f172a !important;
        }

        /* All Buttons in Light Mode: Vibrant Cobalt Blue with 100% white bold text */
        div.stButton > button,
        div[data-testid="stButton"] > button,
        button[kind="secondary"],
        button[kind="primary"],
        section[data-testid="stSidebar"] div.stButton > button {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: 2px solid #1e3a8a !important;
            box-shadow: 0 4px 14px rgba(37,99,235,0.25) !important;
            border-radius: 10px !important;
        }
        div.stButton > button *,
        div[data-testid="stButton"] > button *,
        button[kind="secondary"] *,
        button[kind="primary"] *,
        section[data-testid="stSidebar"] div.stButton > button * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800 !important;
        }

        /* Logo frame in Light Mode */
        .vyas-sidebar-logo {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1.5px solid rgba(37, 99, 235, 0.4) !important;
            filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.15)) !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.12) !important;
        }

        /* Modern Tables in Light Mode */
        table {
            background: #ffffff !important;
            border-color: #cbd5e1 !important;
        }
        th {
            background: #eff6ff !important;
            color: #1e3a8a !important;
            border-bottom: 2px solid #93c5fd !important;
            font-weight: 800 !important;
        }
        td {
            color: #0f172a !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        tr:nth-child(even) td {
            background: #f8fafc !important;
        }
        tr:nth-child(odd) td {
            background: #ffffff !important;
        }
"""

st.markdown("""
<style>
    @font-face {
        font-family: 'Material Symbols Rounded';
        font-style: normal;
        font-weight: 400;
        font-display: block;
        src: url(https://fonts.gstatic.com/s/materialsymbolsrounded/v376/syl0-zNym6YjUruM-QrEh7-nyTnjDwKNJ_190FjpZIvDmUSVOK7BDB_Qb9vUSzq3wzLK-P0J-V_Zs-QtQth3-jOcbTCVpeRL2w5rwZu2rIelXxI.ttf) format('truetype');
    }

    :root {
        --app-font-size: 19.5px;
        --gold-primary: #e5a93c;
        --gold-light: #fef3c7;
        --gold-accent: #f59e0b;
        --bg-deep: #07090d;
        --bg-surface: #0b1220;
        --card-bg: rgba(11, 18, 32, 0.88);
        --card-border: rgba(229, 169, 60, 0.22);
        --card-border-hover: rgba(229, 169, 60, 0.55);
        --accent-ruby: #ef4444;
        --accent-emerald: #10b981;
        --text-main: #f1f5f9;
        --text-muted: #94a3b8;
        --vyas-gold-1: #fff4cc;
        --vyas-gold-2: #f5d16e;
        --vyas-gold-3: #b99a3d;
        --vyas-line: rgba(245, 209, 110, 0.24);
        --vyas-ease: cubic-bezier(0.22, 1, 0.36, 1);
        --font-yatra: 'Yatra One', 'Noto Sans Devanagari', 'Cinzel', serif;
        --font-body: 'Noto Sans Devanagari', 'Plus Jakarta Sans', sans-serif;
    }

    /* Automatic System Light Mode Adaptation for PC & Mobile */
    @media (prefers-color-scheme: light) {
        :root {
            --gold-primary: #1e3a8a;
            --gold-light: #2563eb;
            --gold-accent: #1d4ed8;
            --bg-deep: #f8fafc;
            --bg-surface: #ffffff;
            --card-bg: rgba(255, 255, 255, 0.98);
            --card-border: rgba(37, 99, 235, 0.25);
            --card-border-hover: rgba(37, 99, 235, 0.65);
            --accent-ruby: #dc2626;
            --accent-emerald: #059669;
            --text-main: #0f172a;
            --text-muted: #1e293b;
            --vyas-gold-1: #1e3a8a;
            --vyas-gold-2: #2563eb;
            --vyas-gold-3: #1d4ed8;
            --vyas-line: rgba(37, 99, 235, 0.25);
        }

        html, body {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }

        .stApp, [data-testid="stAppViewContainer"], .main {
            background: #f8fafc !important;
            background-image: none !important;
            color: #0f172a !important;
        }

        p, span, li, label,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li {
            color: #0f172a !important;
        }

        .glass-card, .predict-card {
            background: #ffffff !important;
            border-color: rgba(37, 99, 235, 0.25) !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06) !important;
            color: #0f172a !important;
        }

        .glass-card p, .predict-card p, .predict-card div {
            color: #1e293b !important;
        }

        .vyas-hero-banner {
            background: #ffffff !important;
            border-color: rgba(37, 99, 235, 0.45) !important;
            box-shadow: 0 10px 30px rgba(37,99,235,0.08) !important;
        }

        .vyas-hero-kicker {
            color: #1e3a8a !important;
        }

        .vyas-hero-title {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #1d4ed8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-shadow: none !important;
        }

        .section-title {
            color: #1e3a8a !important;
            border-bottom-color: rgba(37, 99, 235, 0.35) !important;
        }

        section[data-testid="stSidebar"] {
            background: #f8fafc !important;
            border-right: 1.5px solid rgba(15, 23, 42, 0.15) !important;
        }

        [data-testid="stExpander"] {
            background: #ffffff !important;
            border-color: rgba(37, 99, 235, 0.25) !important;
        }

        [data-testid="stExpander"] summary {
            color: #0f172a !important;
        }
    }

    /* Base Page Styling with Fluid Typography */
    html, body {
        max-width: 100vw;
        overflow-x: hidden;
        -webkit-text-size-adjust: 100%;
        text-size-adjust: 100%;
        margin: 0;
        padding: 0;
        background-color: #07090d !important;
        font-size: var(--app-font-size, 20.5px) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], .main {
        background:
            radial-gradient(140% 140% at 50% 0%, rgba(245, 209, 110, 0.08) 0%, transparent 38%),
            radial-gradient(120% 120% at 50% 100%, rgba(76, 110, 245, 0.08) 0%, transparent 42%),
            radial-gradient(ellipse at top, #121a36 0%, #070b1a 48%, #04050d 100%) !important;
        background-attachment: fixed !important;
        font-family: var(--font-body) !important;
        color: #f1f5f9 !important;
        line-height: 1.75 !important;
    }

    /* Universal bold typography & high readability */
    p, span, li, label,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li {
        font-size: var(--app-font-size, 20.5px) !important;
        line-height: 1.75 !important;
        color: var(--text-main, #f1f5f9) !important;
        font-family: var(--font-body) !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
    }

    /* Force override any hardcoded inline micro-fonts (0.6rem - 0.88rem) */
    [style*="font-size: 0."],
    [style*="font-size:0."] {
        font-size: calc(var(--app-font-size, 20.5px) * 0.95) !important;
        line-height: 1.65 !important;
    }

    /* Responsive Block Container */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1380px !important;
        margin: 0 auto !important;
    }

    @media (min-width: 992px) {
        .block-container {
            padding-top: 1.8rem !important;
            padding-left: 2.2rem !important;
            padding-right: 2.2rem !important;
        }
    }

    /* -------------------------------------------------------------
       HERO BANNER (Majestic Yatra One Header)
       ------------------------------------------------------------- */
    .vyas-hero-banner {
        position: relative;
        background: radial-gradient(140% 140% at 50% 0%, rgba(245, 209, 110, 0.16) 0%, transparent 60%),
                    linear-gradient(180deg, rgba(16, 26, 52, 0.96) 0%, rgba(7, 12, 26, 0.98) 100%);
        border: 1.5px solid rgba(240, 192, 90, 0.45);
        border-radius: 20px;
        padding: 24px 30px;
        text-align: center;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(240, 192, 90, 0.35);
        margin-bottom: 20px;
    }
    .vyas-hero-banner::after {
        content: "";
        position: absolute;
        top: 0; left: 15%; right: 15%; height: 2px;
        background: radial-gradient(circle, rgba(255, 244, 204, 0.95) 0%, rgba(245, 209, 110, 0.6) 50%, transparent 100%);
    }
    .vyas-hero-kicker {
        font-family: var(--font-yatra);
        font-size: clamp(0.85rem, 2.5vw, 1.05rem);
        letter-spacing: 3px;
        color: #eedc9a;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .vyas-hero-title {
        font-family: var(--font-yatra);
        font-size: clamp(2.3rem, 7vw, 3.5rem);
        font-weight: 900;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #fff2cc 0%, #f0c05a 50%, #d49429 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        text-shadow: 0 0 28px rgba(240, 192, 90, 0.4);
        line-height: 1.25;
    }
    .vyas-hero-subtitle {
        font-family: var(--font-yatra);
        font-size: clamp(1.05rem, 3.2vw, 1.35rem);
        font-weight: 500;
        color: #eedc9a;
        letter-spacing: 0.8px;
        line-height: 1.45;
    }

    @media (max-width: 1024px) {
        .vyas-hero-banner {
            padding: 16px 16px !important;
            border-radius: 16px !important;
            margin-bottom: 14px !important;
        }
        .vyas-hero-kicker {
            letter-spacing: 2px !important;
        }
        .vyas-hero-title {
            letter-spacing: 2px !important;
        }
    }

    /* -------------------------------------------------------------
       SECTION TITLES & HEADINGS (Large, Bold Yatra One)
       ------------------------------------------------------------- */
    .section-title, h1, h2, h3 {
        font-family: var(--font-yatra) !important;
        font-size: clamp(1.4rem, 4.5vw, 1.9rem) !important;
        font-weight: 700 !important;
        letter-spacing: 0.6px !important;
        line-height: 1.45 !important;
        padding: 4px 0 10px 0 !important;
        margin-top: 16px !important;
        margin-bottom: 18px !important;
        color: #fff4cc !important;
        border-bottom: 2px solid rgba(245, 209, 110, 0.35) !important;
        display: block !important;
    }

    /* Form Field Labels (Large, Crisp, High Contrast) */
    label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        font-family: var(--font-body) !important;
        font-size: clamp(1.05rem, 3vw, 1.18rem) !important;
        font-weight: 700 !important;
        color: #fef3c7 !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 6px !important;
    }

    /* Input Fields (50px Height, 17px Text) */
    input, select, textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] input,
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input,
    .stSelectbox select {
        font-family: var(--font-body) !important;
        font-size: clamp(1.02rem, 3vw, 1.15rem) !important;
        min-height: 50px !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        background-color: rgba(14, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(240, 192, 90, 0.3) !important;
    }

    /* -------------------------------------------------------------
       DOMAIN SUITES & SUB-TABS (Pill Navigation with Yatra One)
       ------------------------------------------------------------- */
    div[data-testid="stRadio"] > label,
    div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
        background: rgba(9, 14, 30, 0.9) !important;
        padding: 10px !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(245, 209, 110, 0.3) !important;
        margin-bottom: 18px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px 20px !important;
        border-radius: 999px !important;
        border: 1px solid rgba(240, 192, 90, 0.28) !important;
        background: rgba(14, 23, 42, 0.88) !important;
        color: #cbd5e1 !important;
        font-family: var(--font-yatra) !important;
        font-size: clamp(0.98rem, 2.8vw, 1.12rem) !important;
        font-weight: 500 !important;
        letter-spacing: 0.4px !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        min-height: 44px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        background: rgba(240, 192, 90, 0.18) !important;
        color: #fff4cc !important;
        border-color: rgba(240, 192, 90, 0.6) !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked),
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #f5d16e 0%, #b99a3d 100%) !important;
        color: #1a1305 !important;
        font-weight: 800 !important;
        border-color: #ffd700 !important;
        box-shadow: 0 4px 18px rgba(240, 192, 90, 0.45) !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) *,
    div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"] * {
        color: #1a1305 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* Sidebar Suite Navigation vertical list */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
        flex-direction: column !important;
        background: rgba(10, 16, 32, 0.7) !important;
        padding: 8px !important;
        gap: 6px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(240, 192, 90, 0.2) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
        width: 100% !important;
        justify-content: flex-start !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 0.95rem !important;
        white-space: normal !important;
        line-height: 1.3 !important;
        min-height: 40px !important;
    }

    /* -------------------------------------------------------------
       ROYAL GOLD CTA BUTTON (Grand Yatra One Button)
       ------------------------------------------------------------- */
    div.stButton > button[kind="primary"],
    div.stButton > button,
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #e5a93c 0%, #fcd375 50%, #c98822 100%) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: var(--font-yatra) !important;
        font-weight: 900 !important;
        font-size: clamp(1.1rem, 3.5vw, 1.3rem) !important;
        letter-spacing: 0.6px !important;
        border: 2px solid #ffd97d !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 22px rgba(212, 148, 41, 0.45) !important;
        transition: all 0.25s ease !important;
        padding: 12px 24px !important;
        min-height: 52px !important;
        text-shadow: none !important;
    }
    div.stButton > button *,
    section[data-testid="stSidebar"] div.stButton > button * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }
    div.stButton > button:hover,
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #fcd375 0%, #fff2cc 50%, #e5a93c 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(247, 213, 132, 0.65) !important;
        color: #000000 !important;
    }

    /* -------------------------------------------------------------
       MODERN ADAPTIVE RESPONSIVE ENGINE (Mobile / Tablet / PC Auto-Reflow)
       ------------------------------------------------------------- */
    @media (max-width: 1024px) {
        /* 1. Prevent desktop zoom-out; force true 100vw mobile width */
        html, body, .stApp, [data-testid="stAppViewContainer"], .main {
            width: 100vw !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 2. On Mobile, sidebar is an animated overlay drawer that never sticks on screen when closed */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            bottom: 0 !important;
            height: 100vh !important;
            width: 86vw !important;
            max-width: 340px !important;
            z-index: 9999999 !important;
            box-shadow: 12px 0 45px rgba(0, 0, 0, 0.85) !important;
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }

        /* Sidebar CLOSED: completely hidden off-screen to the left so it NEVER covers content */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-110%) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* Sidebar OPEN: smoothly slides into view */
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            left: 0 !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }

        /* Large touch-friendly toggle buttons for finger tap */
        [data-testid="stSidebarCollapseButton"] button {
            min-width: 44px !important;
            min-height: 44px !important;
            border-radius: 8px !important;
        }
        [data-testid="stExpandSidebarButton"] button,
        [data-testid="collapsedControl"] button {
            min-width: 44px !important;
            min-height: 44px !important;
            border-radius: 8px !important;
            background: #2563eb !important;
            color: #ffffff !important;
        }

        /* 3. Main container takes full 100% screen with zero side-cramping */
        [data-testid="stAppViewContainer"] > .main,
        .main {
            width: 100vw !important;
            max-width: 100vw !important;
            min-width: 100vw !important;
            flex: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .block-container {
            width: 100vw !important;
            max-width: 100vw !important;
            padding-left: 14px !important;
            padding-right: 14px !important;
            padding-top: 20px !important;
            padding-bottom: 3.5rem !important;
            box-sizing: border-box !important;
        }

        /* 4. Column vertical stack on mobile: 1 column so elements are large and legible */
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 12px !important;
            width: 100% !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* 5. Mobile Fluid Typography & Touch-Friendly Dimensions */
        :root {
            --app-font-size: 20px !important;
        }
        p, span, li, label, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span {
            font-size: 1.15rem !important;
            line-height: 1.8 !important;
            text-align: left !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            word-break: normal !important;
        }
        .section-title {
            font-size: 1.42rem !important;
            padding: 4px 0 8px 0 !important;
            margin-top: 14px !important;
            margin-bottom: 12px !important;
            line-height: 1.4 !important;
        }
        .glass-card, .predict-card {
            padding: 16px 14px !important;
            border-radius: 14px !important;
            margin-bottom: 14px !important;
            font-size: 1.15rem !important;
            line-height: 1.8 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
        .glass-card p, .predict-card p, .predict-card div {
            font-size: 1.15rem !important;
            line-height: 1.8 !important;
            text-align: left !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
        [data-testid="stExpander"] {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            margin-bottom: 10px !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] div[role="button"] p {
            font-size: 1.18rem !important;
            font-weight: 700 !important;
            line-height: 1.5 !important;
            word-wrap: break-word !important;
        }
        div.stButton > button {
            min-height: 50px !important;
            font-size: 1.15rem !important;
            width: 100% !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
        }
        input, select, textarea, div[data-baseweb="input"] input, div[data-baseweb="select"] input {
            min-height: 48px !important;
            font-size: 1.05rem !important;
        }

        /* 6. Mobile Horizontal Scrollable Pills for Domain Suites */
        div[data-testid="stRadio"] [role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            gap: 8px !important;
            padding: 8px 6px !important;
            margin-bottom: 12px !important;
            border-radius: 12px !important;
            width: 100% !important;
        }
        div[data-testid="stRadio"] [role="radiogroup"] label {
            flex: 0 0 auto !important;
            white-space: nowrap !important;
            padding: 10px 18px !important;
            font-size: 1rem !important;
            min-height: 44px !important;
            border-radius: 999px !important;
        }

        /* 7. Action Button Pairs side-by-side on mobile */
        .mobile-button-row [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 8px !important;
            width: 100% !important;
        }
        .mobile-button-row [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 50% !important;
            width: 50% !important;
            min-width: 0 !important;
            max-width: 50% !important;
        }
        .mobile-button-row div.stButton > button {
            min-height: 44px !important;
            font-size: 0.98rem !important;
            padding: 6px 8px !important;
            white-space: nowrap !important;
        }

        /* 8. Unified Banner Cards with seamless bottom action buttons on mobile */
        .consultation-banner-card {
            border-bottom-left-radius: 0 !important;
            border-bottom-right-radius: 0 !important;
            border-bottom: none !important;
            margin-bottom: 0 !important;
        }
        .consultation-action-btn div.stButton > button {
            border-top-left-radius: 0 !important;
            border-top-right-radius: 0 !important;
            margin-top: 0 !important;
            box-shadow: none !important;
        }
    }

    /* -------------------------------------------------------------
       CARDS & PREDICTIONS (Generous Spacing & High Legibility)
       ------------------------------------------------------------- */
    .glass-card {
        position: relative;
        background:
            radial-gradient(160% 160% at 50% 0%, rgba(245, 209, 110, 0.09) 0%, transparent 48%),
            linear-gradient(180deg, rgba(19, 27, 54, 0.98) 0%, rgba(8, 12, 26, 0.98) 100%);
        border: 1px solid rgba(245, 209, 110, 0.32);
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 0 rgba(255, 246, 210, 0.08) inset,
                    0 24px 50px -24px rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        font-size: clamp(1.10rem, 2.8vw, 1.25rem) !important;
        line-height: 1.8 !important;
    }

    .predict-card {
        position: relative;
        background:
            radial-gradient(140% 140% at 50% 0%, rgba(245, 209, 110, 0.08) 0%, transparent 48%),
            linear-gradient(180deg, rgba(18, 26, 52, 0.98) 0%, rgba(9, 13, 28, 0.98) 100%);
        border-left: 5px solid var(--vyas-gold-2);
        border-top: 1px solid rgba(245, 209, 110, 0.24);
        border-right: 1px solid rgba(245, 209, 110, 0.18);
        border-bottom: 1px solid rgba(245, 209, 110, 0.18);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 20px 46px -24px rgba(0, 0, 0, 0.98);
        font-size: clamp(1.10rem, 2.8vw, 1.25rem) !important;
        line-height: 1.8 !important;
    }

    /* Kundli Diamond Chart */
    .kundli-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 14px 8px !important;
        background: radial-gradient(circle at 50% 40%, rgba(20, 32, 60, 0.75) 0%, rgba(7, 11, 22, 0.98) 100%) !important;
        border: 1px solid rgba(240, 192, 90, 0.35) !important;
        border-radius: 18px !important;
        box-shadow: 0 20px 50px -20px rgba(0, 0, 0, 0.9) !important;
        margin-bottom: 18px !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    .kundli-container img,
    .kundli-container svg {
        max-width: 440px !important;
        width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
    }

    @media (max-width: 768px) {
        .kundli-container {
            padding: 8px 2px !important;
            border-radius: 14px !important;
            margin-bottom: 14px !important;
        }
        .kundli-container img,
        .kundli-container svg {
            max-width: 100% !important;
        }
    }

    /* Consultation Dialog Bottom Sheet */
    @media (max-width: 1024px) {
        div[data-testid="stDialog"] > div {
            width: 100vw !important;
            max-width: 100vw !important;
            min-width: 100vw !important;
            height: 92vh !important;
            max-height: 92vh !important;
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            top: auto !important;
            border-radius: 20px 20px 0 0 !important;
            margin: 0 !important;
            padding: 16px 12px !important;
            overflow-y: auto !important;
            border: 1.5px solid rgba(240, 192, 90, 0.45) !important;
            border-bottom: none !important;
            box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.95) !important;
        }
        div[data-testid="stDialog"] [data-testid="stVerticalBlock"] {
            gap: 8px !important;
        }
    }

    /* Tables & Tabs */
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    .as-table-wrap {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        display: block !important;
        font-size: clamp(0.95rem, 2.5vw, 1.05rem) !important;
    }
    table {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        border-collapse: collapse !important;
        font-size: clamp(0.95rem, 2.5vw, 1.05rem) !important;
    }

    /* Timed Prediction Cards styling */
    .timed-pred-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .timed-pred-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.22);
    }

    .stTabs [data-baseweb="tab-list"], .stTabs [role="tablist"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        gap: 8px !important;
        padding: 6px 8px !important;
        background-color: rgba(9, 15, 30, 0.88) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(240, 192, 90, 0.25) !important;
        scrollbar-width: none !important;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar,
    .stTabs [role="tablist"]::-webkit-scrollbar {
        display: none !important;
    }
    .stTabs [data-baseweb="tab"], .stTabs button[role="tab"] {
        flex: 0 0 auto !important;
        white-space: nowrap !important;
        height: 44px !important;
        padding: 8px 16px !important;
        font-family: var(--font-yatra) !important;
        font-size: 1.02rem !important;
    }

    /* Material Icons Ligature Fix */
    span[data-testid="stIconMaterial"],
    span[data-testid*="stIcon"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stExpandSidebarButton"] *,
    [data-testid="stExpanderToggleIcon"] *,
    [data-testid="stExpanderStepChevron"] *,
    details summary *,
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-feature-settings: 'liga' 1 !important;
        -webkit-font-feature-settings: 'liga' 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
        font-style: normal !important;
    }
</style>
""", unsafe_allow_html=True)

if _is_light:
    st.markdown(f"<style>{_light_css_rules}</style>", unsafe_allow_html=True)

_is_hi_banner = "English" not in st.session_state.get('main_ui_lang_radio', 'हिन्दी')
_hero_kicker = "खगोलीय ग्रहीय गणितीय संरचना • HIGH-PRECISION ASTRONOMICAL INTELLIGENCE" if _is_hi_banner else "CELESTIAL PATTERN ARCHITECTURE • HIGH-PRECISION ASTRONOMICAL INTELLIGENCE"

st.markdown(f"""
<div class="vyas-hero-banner">
    <div class="vyas-hero-kicker" style="font-size: 0.72rem; letter-spacing: 1.8px; opacity: 0.9; margin-bottom: 2px; font-weight: 700; color: {TH_GOLD};">{_hero_kicker}</div>
    <div class="vyas-hero-title">VYAS ASTRA</div>
    <div class="vyas-hero-subtitle">Vedic Yield Astrology Systems &bull; High-Precision Astronomical Intelligence</div>
    <div style="font-family: var(--font-yatra); font-size: clamp(0.82rem, 2.4vw, 1.02rem); color: {TH_MUTED}; margin-top: 8px; line-height: 1.5;">
        वेबसाइट निर्माता एवं शोधकर्ता: <b style="color: {TH_GOLD};">निखिल व्यास (Nikhil Vyas)</b> &bull;  <a href="mailto:inikhilvyas@gmail.com" style="color: {TH_GOLD_ACCENT}; text-decoration:none;">inikhilvyas@gmail.com</a> &bull;  <a href="tel:+919414121172" style="color: {TH_GOLD_ACCENT}; text-decoration:none;">+91 94141 21172</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- SESSION RESOLUTION (before the sidebar) ----------------
# Resolved once, up-front: the logged-out landing page is rendered in the MAIN
# area and st.stop() ends the run before the sidebar is built. (It used to be
# built inside `with st.sidebar:`, so visitors saw a blank main page.)
if st.session_state.pop("_vyas_cookie_pending", False):
    # Deferred write from the run that just signed in/out (see
    # _start_user_session): doing it here means it survives st.rerun().
    _write_session_cookie(st.session_state.get("_vyas_session_token", "") or "")

# Mirror the token into localStorage (works where cookies are stripped) and
# read it back on the next run. The component is zero-height and invisible.
_store_pending = st.session_state.pop("_vyas_store_pending", "") or ""
_clear_pending = st.session_state.pop("_vyas_clear_pending", False)
_bridge_token = _mount_session_bridge(
    "store" if _store_pending else ("clear" if _clear_pending else "read"),
    _store_pending,
)
if _clear_pending:
    # The component still reports the old token on the logout run (JS clears it
    # in the browser only after this run). Never treat that as a restore.
    _bridge_token = ""

_current_email = (st.session_state.get("user") or {}).get("email", "")
if (not _current_email) or _current_email == "seeker@vyasastro.com":
    _restored = None
    # localStorage first: it survives reloads even when the Cloud proxy drops
    # custom cookies. The cookie remains a fallback for local/direct hosting.
    _token = _bridge_token or _read_session_cookie()
    if _token:
        try:
            _restored = auth_vault.get_user_by_session_token(_token)
        except Exception:
            _restored = None
    if _restored:
        st.session_state["user"] = _restored
        # Keep the token so Logout can invalidate exactly this browser's row.
        st.session_state["_vyas_session_token"] = _token
    else:
        st.session_state["user"] = {
            "id": 1,
            "name": "नया जातक (Seeker)",
            "email": "seeker@vyasastro.com",
            "tier": "VIP_TRIAL",
            "days_left": 30,
            "is_vip": True,
        }

# A stale `uid` param must never log anyone in; scrub it from the URL.
if st.query_params.get("uid"):
    st.query_params.clear()

u = st.session_state["user"]
is_logged_in_now = (u.get("email") != "seeker@vyasastro.com")

# Auto-load the default or last saved kundli into loaded_profile on fresh session
if is_logged_in_now:
    cur_lp = st.session_state.get('loaded_profile')
    if not cur_lp or cur_lp.get('user_id') != u["id"]:
        try:
            _auto_k = auth_vault.get_default_or_latest_kundli(u["id"])
            if _auto_k:
                _load_kundli_into_session(_auto_k, user_id=u["id"])
            else:
                st.session_state['show_birth_form'] = True
        except Exception:
            pass


# ---------------- LOGGED-OUT LANDING: EMAIL LOGIN / REGISTRATION ----------------
if not is_logged_in_now:
    # Mount the sidebar container on the very first run of every session, even
    # though visitors only see the landing page. Streamlit creates the sidebar
    # lazily, and when it was first used *after* login the deployed app rendered
    # the main page but never mounted the sidebar (birth details unreachable).
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-family: 'Cinzel', serif; font-size: 1.02rem; font-weight: 800; color: #fef3c7; letter-spacing: 2px;">VYAS ASTRA</div>
            <div style="font-size: 0.66rem; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase;">Vedic Astrology Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("जन्म विवरण, कुण्डली एवं विश्लेषण के लिए लॉगिन करें।")

    _hero_col, _auth_col = st.columns([1.12, 1], gap="large")

    with _hero_col:
        st.markdown("""
        <div style="text-align: center; padding: 34px 26px; background: radial-gradient(circle at 50% 0%, rgba(245, 209, 110, 0.14) 0%, transparent 62%), linear-gradient(180deg, rgba(19, 27, 54, 0.98) 0%, rgba(8, 12, 26, 0.98) 100%); border: 1px solid rgba(245, 209, 110, 0.32); border-radius: 18px; box-shadow: 0 28px 60px -26px rgba(0,0,0,0.98);">
            <div style="font-family: 'Cinzel', serif; font-size: 2.1rem; font-weight: 800; background: linear-gradient(90deg, #fff4cc 0%, #f5d16e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">VYAS ASTRA</div>
            <div style="font-size: 1.05rem; color: #f7d584; margin-bottom: 8px; font-weight: 600;">वैदिक ज्योतिष • के.पी. प्रणाली • शोध प्रबंध</div>
            <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">सटीक जन्मकुंडली विश्लेषण, विंशोत्तरी दशा,<br/>के.पी. फलादेश एवं विस्तृत PDF रिपोर्ट</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 16px; display: grid; gap: 10px;">
            <div style="background: rgba(19,27,54,0.72); border: 1px solid rgba(245,209,110,0.18); border-radius: 12px; padding: 12px 14px; color: #e2e8f0; font-size: 0.9rem;">
                 <b style="color:#f7d584;">पूर्ण कुण्डली</b> — लग्न, नवांश, ग्रह-दशा, योग एवं भाव विश्लेषण
            </div>
            <div style="background: rgba(19,27,54,0.72); border: 1px solid rgba(245,209,110,0.18); border-radius: 12px; padding: 12px 14px; color: #e2e8f0; font-size: 0.9rem;">
                <b style="color:#f7d584;">के.पी. सूट</b> — सब-लॉर्ड, रूलिंग प्लैनेट्स एवं 4-फोल्ड सिग्निफिकेटर
            </div>
            <div style="background: rgba(19,27,54,0.72); border: 1px solid rgba(245,209,110,0.18); border-radius: 12px; padding: 12px 14px; color: #e2e8f0; font-size: 0.9rem;">
                <b style="color:#f7d584;">56-पृष्ठ PDF</b> — प्रिंट-रेडी रिपोर्ट, Google Drive में सुरक्षित
            </div>
        </div>
        """, unsafe_allow_html=True)

    with _auth_col:
        st.markdown(
            '<div style="font-size:1.15rem;font-weight:800;color:#fef3c7;margin-bottom:2px;">'
            'खाते में प्रवेश करें</div>'
            '<div style="font-size:0.82rem;color:#94a3b8;margin-bottom:10px;">'
            'ईमेल से नया खाता बनाएं या लॉगिन करें</div>',
            unsafe_allow_html=True,
        )

        _tab_login, _tab_register = st.tabs(["लॉगिन", "नया खाता"])

        with _tab_login:
            with st.form("vyas_login_form", clear_on_submit=False):
                _in_email = st.text_input("ईमेल", key="login_email", placeholder="you@example.com")
                _in_pw = st.text_input("पासवर्ड", type="password", key="login_pw")
                _in_submit = st.form_submit_button("लॉगिन करें", type="primary", use_container_width=True)
            if _in_submit:
                _ok_in, _msg_in, _u_in = auth_vault.login_user(_in_email, _in_pw)
                if _ok_in and _u_in:
                    _start_user_session(_u_in)
                    st.rerun()
                else:
                    st.error(_msg_in)
            st.caption("पासवर्ड भूल गए? नीचे 'नया खाता' से नया खाता बना सकते हैं।")

        with _tab_register:
            with st.form("vyas_register_form", clear_on_submit=False):
                _up_name = st.text_input("पूरा नाम", key="reg_name", placeholder="जैसे: राहुल शर्मा")
                _up_email = st.text_input("ईमेल", key="reg_email", placeholder="you@example.com")
                _up_pw = st.text_input("पासवर्ड (कम से कम 6 अक्षर)", type="password", key="reg_pw")
                _up_pw2 = st.text_input("पासवर्ड दोबारा", type="password", key="reg_pw2")
                _up_submit = st.form_submit_button("निःशुल्क खाता बनाएं", type="primary", use_container_width=True)
            if _up_submit:
                if not (_up_name or "").strip():
                    st.error("कृपया अपना नाम भरें।")
                elif "@" not in (_up_email or ""):
                    st.error("कृपया सही ईमेल आईडी भरें।")
                elif len(_up_pw or "") < 6:
                    st.error("पासवर्ड कम से कम 6 अक्षरों का होना चाहिए।")
                elif _up_pw != _up_pw2:
                    st.error("दोनों पासवर्ड मेल नहीं खा रहे।")
                else:
                    _ok_up, _msg_up, _u_up = auth_vault.register_user(_up_email, _up_name, _up_pw)
                    if _ok_up and _u_up:
                        _start_user_session(_u_up)
                        st.rerun()
                    else:
                        st.error(_msg_up)
            st.caption("नए खाते पर **30 दिन का VIP Pro ट्रायल निःशुल्क**।")

        _google_login_url = google_drive_sync.get_google_auth_url(include_drive=False)
        if _google_login_url:
            st.markdown(
                "<div style='text-align:center;color:#64748b;font-size:0.78rem;margin:12px 0 6px;'>— या —</div>",
                unsafe_allow_html=True,
            )
            st.link_button("Google से साइन इन करें", _google_login_url, use_container_width=True)

    with st.expander("साइन-इन में समस्या? / Sign-in help", expanded=False):
        _diag = google_drive_sync.oauth_diagnostics()
        _bad = []
        if _diag["client_id_configured"] != "yes":
            _bad.append("Google Client ID सेट नहीं है — Streamlit **Secrets** में `GOOGLE_CLIENT_ID` जोड़ें।")
        if _diag["client_secret_configured"] != "yes":
            _bad.append("Google Client Secret सेट नहीं है — Secrets में `GOOGLE_CLIENT_SECRET` जोड़ें।")
        if _diag["redirect_uri_registered"] != "yes":
            _bad.append("यह Redirect URI Google Cloud Console में registered नहीं है (नीचे देखें)।")
        if _bad:
            st.warning(" • ".join(_bad))
        else:
            st.success("Google क्रेडेंशियल्स ठीक दिख रहे हैं।")
        st.markdown(
            f"**Redirect URI (यही Google Console में डालें):**\n\n"
            f"`{_diag['effective_redirect_uri']}`"
        )
        if _diag["last_oauth_error"]:
            st.error(f"अंतिम Google त्रुटि:\n\n{_diag['last_oauth_error']}")
        st.caption(
            "ईमेल/पासवर्ड से लॉगिन हमेशा काम करता है — Google वैकल्पिक है। "
            "Google के लिए OAuth client में redirect URI जोड़ें और Audience → Test users में Gmail डालें।"
        )

    st.stop()

# Sidebar Native Setup
with st.sidebar:
    # Use the compact logo variant (the sidebar renders it at max 110px, so the
    # 1 MB original only bloats every rerun's HTML payload).
    _here = os.path.dirname(__file__)
    if os.path.exists(os.path.join(_here, "logo_icon.png")):
        logo_file = "logo_icon.png"
    elif os.path.exists(os.path.join(_here, "logo.png")):
        logo_file = "logo.png"
    else:
        logo_file = "logo.jpg"
    try:
        _logo_b64 = base64.b64encode(open(os.path.join(_here, logo_file), 'rb').read()).decode()
    except Exception:
        _logo_b64 = ""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 8px;">
        <img src="data:image/png;base64,{_logo_b64}" 
             class="vyas-sidebar-logo"
             style="max-width: 105px; height: auto; border-radius: 14px; padding: 6px; background: rgba(255, 255, 255, 0.15); filter: drop-shadow(0 6px 18px rgba(0, 0, 0, 0.4)) drop-shadow(0 0 2px rgba(0, 0, 0, 0.6)); border: 1.5px solid rgba(240, 192, 90, 0.4);" />
        <div style="font-family: 'Cinzel', serif; font-size: 1.08rem; font-weight: 800; color: #fef3c7; letter-spacing: 2px; margin-top: 6px;">VYAS ASTRA</div>
        <div style="font-size: 0.68rem; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase;">Vedic Astrology Intelligence</div>
    </div>
    <hr style="border-color: rgba(229, 169, 60, 0.16); margin: 10px 0;">
    """, unsafe_allow_html=True)

    # ---------------- THEME & ACCESSIBILITY CONTROLS ----------------
    col_th_a, col_th_b = st.columns([1.3, 1.1])
    with col_th_a:
        def _on_theme_select_cb():
            st.session_state["_user_theme_mode"] = st.session_state["_user_theme_radio_widget"]

        _theme_choice = st.radio(
            "थीम स्वरूप (Display Theme):",
            options=["डार्क थीम (Dark)", "लाइट थीम (Light)", "हाई कंट्रास्ट (High Contrast)", "सिस्टम अनुसार (Auto System)"],
            index=0 if st.session_state.get("_user_theme_mode") is None or "डार्क" in str(st.session_state.get("_user_theme_mode", "")) else (
                1 if "लाइट" in str(st.session_state.get("_user_theme_mode", "")) else (
                    2 if "कंट्रास्ट" in str(st.session_state.get("_user_theme_mode", "")) else 0
                )
            ),
            horizontal=False,
            key="_user_theme_radio_widget",
            on_change=_on_theme_select_cb,
            help="डिवाइस सिस्टम के अनुसार अथवा मनपसंद डार्क/लाइट/कंट्रास्ट थीम चुनें"
        )
    with col_th_b:
        _contrast_font = st.toggle(
            "कंट्रास्ट फ़ॉन्ट (Crisp Contrast)",
            value=st.session_state.get("_user_contrast_font", True),
            key="_user_contrast_font",
            help="अक्षरों को गहरा, स्पष्ट व 100% सुपाठ्य बनाएं ताकि लाइट थीम में कोई टेक्स्ट अदृश्य या धुंधला न रहे"
        )
    # Unified theme styling is handled at the root level for 100% consistency

    _font_scale_choice = st.select_slider(
        "अक्षर आकार (Text Size):",
        options=["सामान्य (17px)", "बड़ा (19.5px - डिफ़ॉल्ट)", "अति विशाल (22px)"],
        value=st.session_state.get("_user_font_scale", "बड़ा (19.5px - डिफ़ॉल्ट)"),
        key="_user_font_scale",
        help="वेबसाइट पर अक्षरों का आकार छोटा या बड़ा करें"
    )
    if "विशाल" in _font_scale_choice:
        st.markdown("<style>:root { --app-font-size: 22px !important; } html, body, p, div, span, label, .stMarkdown, .glass-card, .predict-card { font-size: 22px !important; }</style>", unsafe_allow_html=True)
    elif "सामान्य" in _font_scale_choice:
        st.markdown("<style>:root { --app-font-size: 17px !important; } html, body, p, div, span, label, .stMarkdown, .glass-card, .predict-card { font-size: 17px !important; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>:root { --app-font-size: 19.5px !important; } html, body, p, div, span, label, .stMarkdown, .glass-card, .predict-card { font-size: 19.5px !important; }</style>", unsafe_allow_html=True)

    # ---------------- 7:00 AM DAILY HOROSCOPE NOTIFICATION WIDGET ----------------
    with st.expander(" 7:00 AM दैनिक राशिफल अलर्ट", expanded=False):
        st.markdown("""
        <div style="font-size: 0.8rem; color: #eedc9a; line-height: 1.5; margin-bottom: 8px;">
            <b>प्रातःकालीन व्यक्तिगत राशिफल:</b><br/>
            रोज़ाना सुबह 7:00 बजे आपके ब्राउज़र/फ़ोन पर नवतारा चक्र, गोचरस्थ चन्द्रमा व चालू विंशोत्तरी दशा का दैनिक फलादेश अलर्ट प्राप्त करें।
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html("""
        <div style="text-align: center; font-family: sans-serif;">
            <button id="notif-btn" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: 800; border: none; border-radius: 8px; padding: 10px 14px; font-size: 0.85rem; cursor: pointer; width: 100%; box-shadow: 0 4px 14px rgba(245,158,11,0.35);">
                 7:00 AM अलर्ट चालू करें
            </button>
            <div id="notif-status" style="font-size: 0.74rem; color: #94a3b8; margin-top: 6px;"></div>
        </div>
        <script>
            const btn = document.getElementById('notif-btn');
            const status = document.getElementById('notif-status');

            function updateStatus() {
                if (!("Notification" in window)) {
                    status.innerHTML = "ब्राउज़र नोटिफिकेशन समर्थित नहीं है।";
                    btn.disabled = true;
                    return;
                }
                if (Notification.permission === "granted") {
                    status.innerHTML = " 7:00 AM दैनिक राशिफल अलर्ट सक्रिय है!";
                    status.style.color = "#34d399";
                    btn.innerText = " अलर्ट सक्रिय है (7:00 AM Daily)";
                    checkMorningAlert();
                } else if (Notification.permission === "denied") {
                    status.innerHTML = " नोटिफिकेशन ब्लॉक है। ब्राउज़र सेटिंग्स में अनुमति दें।";
                    status.style.color = "#f87171";
                } else {
                    status.innerHTML = "सुबह 7 बजे दैनिक फलादेश पाने हेतु बटन दबाएं।";
                }
            }

            function checkMorningAlert() {
                const today = new Date().toISOString().slice(0, 10);
                const lastNotif = localStorage.getItem('vyas_last_7am_notif');
                const now = new Date();
                if (now.getHours() >= 7 && lastNotif !== today) {
                    new Notification("VYAS • आज का दैनिक पंचांग, शुभ मुहूर्त व राशिफल", {
                        body: "नमस्ते! आज का पंचांग, शुभ अभिजीत मुहूर्त, राहुकाल एवं आपकी चालू दशा का व्यक्तिगत राशिफल तैयार है।",
                        icon: "https://raw.githubusercontent.com/nikhilvyas007/VYAS/master/logo_icon.png"
                    });
                    localStorage.setItem('vyas_last_7am_notif', today);
                }
            }

            btn.addEventListener('click', async () => {
                if ("Notification" in window) {
                    const perm = await Notification.requestPermission();
                    if (perm === "granted") {
                        localStorage.setItem('vyas_daily_notif_enabled', 'true');
                        new Notification("VYAS • 7:00 AM अलर्ट चालू", {
                            body: "दैनिक पंचांग, मुहूर्त व राशिफल अलर्ट सक्रिय हो गया है। हर सुबह 7:00 बजे आपको दिन फल प्राप्त होगा।",
                            icon: "https://raw.githubusercontent.com/nikhilvyas007/VYAS/master/logo_icon.png"
                        });
                    }
                    updateStatus();
                }
            });
            updateStatus();
        </script>
        """, height=105)

    # ---------------- USER AUTH & 30-DAY VIP TRIAL VAULT ----------------
    # `u` and `is_logged_in_now` are resolved once, above the sidebar.
    
    # ---------------- MOBILE 1-CLICK PWA APP INSTALLATION (NATIVE PROMPT) ----------------
    if is_logged_in_now:
        st.components.v1.html("""
        <div id="pwa-install-container" style="display: none; background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(14, 23, 47, 0.95) 100%);
                    border: 1px solid rgba(96, 165, 250, 0.5); border-radius: 12px; padding: 12px 14px; margin-bottom: 12px; text-align: center;">
            <div style="font-size: 0.9rem; font-weight: 800; color: #93c5fd; font-family: sans-serif;"> VYAS ASTRA ऐप इंस्टॉल करें</div>
            <div style="font-size: 0.76rem; color: #cbd5e1; margin: 4px 0 10px 0; font-family: sans-serif;">अपने फोन की होम स्क्रीन पर सीधे 1-क्लिक में ऐप जोड़ें।</div>
            <button id="pwa-install-btn" style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: 1px solid #60a5fa; border-radius: 8px; padding: 8px 18px; font-weight: 700; font-size: 0.85rem; cursor: pointer; width: 100%; box-shadow: 0 4px 12px rgba(37,99,235,0.4);">
                 अभी इंस्टॉल करें (Install Now)
            </button>
        </div>

        <script>
            let deferredPrompt;
            const container = document.getElementById('pwa-install-container');
            const installBtn = document.getElementById('pwa-install-btn');

            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                deferredPrompt = e;
                container.style.display = 'block';
            });

            if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
                container.style.display = 'block';
            }

            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    if (outcome === 'accepted') {
                        container.style.display = 'none';
                    }
                    deferredPrompt = null;
                } else {
                    alert("मोबाइल पर इंस्टॉल करने के लिए ब्राउज़र के शीर्ष मेनू (⋮ या शेयर आइकन) पर टैप करके 'Add to Home screen' चुनें।");
                }
            });
        </script>
        """, height=125)
    
    if is_logged_in_now:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(240, 192, 90, 0.18) 0%, rgba(14, 23, 47, 0.95) 100%);
                    border: 1px solid rgba(240, 192, 90, 0.5); border-radius: 10px; padding: 8px 12px; text-align: center; margin-bottom: 8px;">
            <div style="color: #f7d584; font-weight: 800; font-size: 0.88rem;">VIP PRO TRIAL ACTIVE</div>
            <div style="color: #eedc9a; font-size: 0.76rem; margin-top: 2px;">{u['name']} • <b>{u.get('days_left', 30)} Days Left</b></div>
        </div>
        """, unsafe_allow_html=True)

    # Hybrid Payment & Upgrade VIP Modal
    if is_logged_in_now:
        with st.expander(" Upgrade VIP / प्रीमियम सदस्यता लें", expanded=False):
            st.markdown("""
            <div style="font-size: 0.82rem; color: #eedc9a; margin-bottom: 8px;">
                <b>VIP Pro प्लान्स:</b> असीमित कुंडलियां, विस्तृत रिपोर्ट्स, लाल किताब व BTR का पूर्ण एक्सेस।
            </div>
            """, unsafe_allow_html=True)
            plan_sel = st.selectbox("चुनें प्लान (Select Plan)", [
                " वार्षिक प्रो (Annual VIP Pro) - ₹999 / वर्ष",
                " मासिक (Monthly Starter) - ₹199 / माह",
                " लाइफटाइम एलीट (Lifetime Elite) - ₹2,499"
            ])
            
            plan_key = "annual"
            amount = 999
            if "मासिक" in plan_sel:
                plan_key = "monthly"
                amount = 199
            elif "लाइफटाइम" in plan_sel:
                plan_key = "lifetime"
                amount = 2499

            upi_id = "inikhilvyas@ybl"
            payee_name = "Nikhil Vyas"
            import urllib.parse
            upi_uri = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am={amount}.00&cu=INR&tn={urllib.parse.quote('VYAS VIP Subscription')}"
            encoded_uri = urllib.parse.quote(upi_uri)
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_uri}"

            st.markdown(f"""
            <div style="text-align: center; background: rgba(10, 16, 32, 0.9); border: 1px solid #f0c05a; border-radius: 12px; padding: 12px; margin-top: 8px;">
                <div style="color: #f0c05a; font-weight: 800; font-size: 0.9rem;"> Scan & Pay ₹{amount}</div>
                <div style="color: #eedc9a; font-size: 0.76rem;">(PhonePe, GPay, Paytm, BHIM)</div>
                <div style="margin: 10px 0;">
                    <img src="{qr_url}" width="160" height="160" style="border-radius: 10px; border: 2px solid #eedc9a; background: white; padding: 6px;"/>
                </div>
                <div style="font-size: 0.8rem; color: #f7d584;"><b>UPI ID:</b> <code>{upi_id}</code></div>
                <div style="font-size: 0.9rem; color: #48cae4; font-weight: 800; margin-top: 4px;">कुल देय राशि: ₹{amount}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<small style='color: #eedc9a;'><b>भुगतान के बाद पुष्टि करें:</b></small>", unsafe_allow_html=True)
            txn_input = st.text_input("UPI Reference / UTR No.", placeholder="e.g. 428192849120", key="txn_field")
            
            col_pay1, col_pay2 = st.columns(2)
            with col_pay1:
                if st.button(" Confirm Payment", use_container_width=True):
                    if txn_input and len(txn_input) >= 6:
                        ok, up_msg = auth_vault.upgrade_vip(u["id"], plan_key, txn_input)
                        if ok:
                            st.session_state["user"]["tier"] = "VIP_PAID"
                            st.session_state["user"]["is_vip"] = True
                            st.success(up_msg)
                            st.rerun()
                        else:
                            st.error(up_msg)
                    else:
                        st.warning("कृपया मान्य UTR दर्ज करें।")
            with col_pay2:
                wa_text = f"Namaste Nikhil Ji, I have paid INR {amount} for VYAS VIP ({plan_key}). UTR: {txn_input}"
                wa_url = f"https://wa.me/919414121172?text={wa_text.replace(' ', '%20')}"
                st.markdown(f"""
                <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                    <button style="width: 100%; background: #25D366; color: white; border: none; border-radius: 6px; padding: 7px; font-weight: 700; font-size: 0.82rem; cursor: pointer;">
                         WhatsApp Help
                    </button>
                </a>
                """, unsafe_allow_html=True)

    # ---------------- USER AUTHENTICATION & SESSION ----------------
    is_logged_in = (u["email"] != "seeker@vyasastro.com")
    
    if is_logged_in:
        u_tokens = auth_vault.get_google_tokens(u["id"])
        has_gdrive = bool(u_tokens and u_tokens.get("access_token"))
        gdrive_status_html = """
        <div style="font-size: 0.8rem; color: #6ee7b7; margin-top: 6px; display: flex; align-items: center; gap: 6px;">
            <span style="display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%;"></span>
            <b>Google Drive:</b> सक्रिय (PDF रिपोर्ट सिंक)
        </div>
        """ if has_gdrive else """
        <div style="font-size: 0.8rem; color: #facc15; margin-top: 6px;">
            Google Drive कनेक्ट नहीं है
        </div>
        """

        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.5); border-radius: 10px; padding: 10px 12px; margin-bottom: 10px;">
            <div style="font-weight: 700; color: #34d399; font-size: 0.92rem;">लॉगिन: {u['name']}</div>
            <div style="font-size: 0.78rem; color: #cbd5e1;">{u['email']}</div>
            {gdrive_status_html}
        </div>
        """, unsafe_allow_html=True)

        col_gdr1, col_gdr2 = st.columns([1.2, 1])
        with col_gdr1:
            if not has_gdrive:
                auth_url = google_drive_sync.get_google_auth_url(include_drive=True)
                if auth_url:
                    st.link_button(
                        "Drive कनेक्ट करें",
                        auth_url,
                        use_container_width=True,
                        help="Drive में PDF सुरक्षित करने के लिए अनुमति दें।",
                    )
        with col_gdr2:
            if st.button("Logout", key="sidebar_logout_btn", use_container_width=True):
                _end_user_session()
                st.query_params.clear()
                for _dk in ("oauth_state", "oauth_code_verifier"):
                    try:
                        auth_vault.pop_app_state(_dk)
                    except Exception:
                        pass
                st.success("लॉगआउट हुआ।")
                st.rerun()

        # ---------------- PROMINENT SIDEBAR KUNDLI VAULT (OPEN KUNDLI) ----------------
        saved_list_sb = auth_vault.get_saved_kundlis(u["id"])
        cur_lp_sb = st.session_state.get('loaded_profile')
        
        st.markdown("""
        <div style="font-size: 0.78rem; color: #eedc9a; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; margin: 12px 0 6px 0;">
            सुरक्षित कुण्डलियाँ (Saved Kundlis)
        </div>
        """, unsafe_allow_html=True)
        
        if cur_lp_sb:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.9); border: 1.2px solid #f0c05a; border-radius: 8px; padding: 6px 10px; margin-bottom: 8px;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #f0c05a;">सक्रिय कुण्डली: {cur_lp_sb.get('name', 'जातक')}</div>
                <div style="font-size: 0.72rem; color: #cbd5e1;">{cur_lp_sb.get('dob')} • {cur_lp_sb.get('city', '')[:16]}</div>
            </div>
            """, unsafe_allow_html=True)

        if saved_list_sb:
            sb_k_map = {f"{k['name']} ({k.get('dob')} - {k.get('city', '')[:12]})": k for k in saved_list_sb}
            cur_k_id = cur_lp_sb.get('id') if cur_lp_sb else None
            cur_k_idx = 0
            for idx, k in enumerate(saved_list_sb):
                if k.get('id') == cur_k_id:
                    cur_k_idx = idx
                    break
            sb_sel_lbl = st.selectbox("कुण्डली चुनें:", list(sb_k_map.keys()), index=cur_k_idx, key="sb_vault_kundli_select", label_visibility="collapsed")
            sb_sel_k = sb_k_map[sb_sel_lbl]
            
            c_sb1, c_sb2 = st.columns(2)
            with c_sb1:
                if st.button("कुण्डली खोलें", key="sb_open_k_btn", use_container_width=True, type="primary", help="चयनित कुण्डली तुरंत लोड करें"):
                    _load_kundli_into_session(sb_sel_k, user_id=u["id"])
                    st.rerun()
            with c_sb2:
                if st.button("नई कुण्डली", key="sb_new_k_btn", use_container_width=True, help="नये जातक का जन्म विवरण भरें"):
                    st.session_state['show_birth_form'] = True
                    st.session_state.pop('loaded_profile', None)
                    st.rerun()
        else:
            if st.button("नई कुण्डली बनाएं (Enter Details)", key="sb_new_k_empty_btn", use_container_width=True, type="primary"):
                st.session_state['show_birth_form'] = True
                st.session_state.pop('loaded_profile', None)
                st.rerun()
    else:
        auth_url = google_drive_sync.get_google_auth_url(include_drive=False)
        if auth_url:
            st.link_button(
                "Google से साइन इन करें",
                auth_url,
                use_container_width=True,
                type="primary",
                help="सुरक्षित OAuth 2.0 — Google लॉगिन नई विंडो में खुलेगा।",
            )
            st.caption(" साइन-इन नई विंडो में पूरा करें, फिर यह पेज रीफ़्रेश करें।")

    # Admin/debug panels - ONLY visible when ?admin=1 query param is explicitly passed
    is_admin_mode = bool(st.query_params.get("admin") in ("1", "true") or os.environ.get("VYAS_ADMIN") == "1")
    if is_logged_in and is_admin_mode:
        with st.expander("Google Cloud API Credentials (Admin Only)", expanded=False):
            g_cfg = google_drive_sync.load_google_config()
            # Never render stored OAuth secrets in the browser.
            cfg_cid = st.text_input("Google Client ID", value="", key="cfg_cid_in", placeholder="Leave blank to keep current Client ID")
            cfg_csec = st.text_input("Google Client Secret", value="", type="password", key="cfg_csec_in", placeholder="Leave blank to keep current secret")
            st.caption("Stored credentials remain server-side. Enter new values only when rotating them.")
            cfg_ruri = st.text_input("Redirect URI", value=g_cfg.get("redirect_uri", "http://localhost:8501"), key="cfg_ruri_in")
            if st.button(" Save Credentials", key="save_g_cfg_btn", use_container_width=True):
                if google_drive_sync.save_google_config(cfg_cid, cfg_csec, cfg_ruri):
                    st.success("Google OAuth सेटिंग्स सुरक्षित हुईं!")
                    st.rerun()
                else:
                    st.error("सेव करने में त्रुटि।")
            st.markdown("""
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; line-height: 1.45;">
                <b>क्रेडेंशियल्स प्राप्त करने का तरीका:</b><br/>
                1. <a href="https://console.cloud.google.com/auth/clients" target="_blank" style="color: #60a5fa;">Google Cloud Console → Google Auth Platform → Clients</a> में जाएं।<br/>
                2. <b>Google Drive API</b> को Enable करें।<br/>
                3. OAuth 2.0 Web Client बनाएं और <b>Authorized redirect URIs</b> में ये दोनों जोड़ें
                (अंत में स्लैश नहीं — Google में byte-exact मैच होना चाहिए):<br/>
                <code>http://localhost:8501</code> (local के लिए)<br/>
                <code>https://vyas-astrology-111.streamlit.app</code> (live app के लिए)<br/>
                4. जिस Gmail से लॉगिन करना है उसे <b>Audience → Test users</b> में जोड़ें (या app Publish करें)।
            </div>
            """, unsafe_allow_html=True)

            # ---- Account storage (persistence) ----
            with st.container():
                if auth_vault.BACKEND == "postgres":
                    st.success("Neon Postgres — खाते redeploy/reboot के बाद भी सुरक्षित रहेंगे।")
                else:
                    st.warning(
                        "Local SQLite — Streamlit Cloud redeploy पर खाते मिट सकते हैं। "
                        "Settings → Secrets में DATABASE_URL जोड़ें।"
                    )
                if auth_vault.LAST_DB_ERROR:
                    st.caption(f"Last DB error: {auth_vault.LAST_DB_ERROR}")

            # ---- OAuth diagnostics ----
            st.markdown("---")
            st.markdown("** OAuth Debug (redirect URI जाँचें)**")
            with st.container():
                _eff_redirect = google_drive_sync.resolve_redirect_uri(
                    google_drive_sync.load_google_config().get("redirect_uri", "")
                )
                _auth_url = google_drive_sync.get_google_auth_url()
                _sent_redirect = ""
                try:
                    _qs = urllib.parse.parse_qs(urllib.parse.urlparse(_auth_url).query)
                    _sent_redirect = (_qs.get("redirect_uri") or [""])[0]
                except Exception:
                    pass

                _ctx = getattr(st, "context", None)
                _ctx_headers = getattr(_ctx, "headers", {}) if _ctx else {}
                _ctx_url = str(getattr(_ctx, "url", "") or "") if _ctx else ""
                st.code(
                    "Effective redirect_uri : " + repr(_eff_redirect) + "\n"
                    + "Sent in auth URL     : " + repr(_sent_redirect) + "\n"
                    + "Match (code side)    : "
                    + ("OK" if _eff_redirect == _sent_redirect else "MISMATCH!") + "\n"
                    + "Registered in code   : " + repr(sorted(google_drive_sync.REGISTERED_REDIRECT_URIS)) + "\n"
                    + "st.context.url       : " + repr(_ctx_url) + "\n"
                    + "X-Forwarded-Host     : " + repr(_ctx_headers.get("X-Forwarded-Host")) + "\n"
                    + "X-Forwarded-Proto    : " + repr(_ctx_headers.get("X-Forwarded-Proto")) + "\n"
                    + "Host                 : " + repr(_ctx_headers.get("Host")),
                    language="text",
                )
                st.caption(
                    "Google Console → Clients → VYAS Astra → Authorized redirect URIs में "
                    "ऊपर की 'Sent in auth URL' वाली value बिल्कुल वैसी ही होनी चाहिए "
                    "(trailing slash, http vs https, www — कुछ भी अलग नहीं)।"
                )

                if st.button(" Google क्रेडेंशियल्स जाँचें", key="test_g_creds_btn", use_container_width=True):
                    _ok_gc, _msg_gc = google_drive_sync.test_google_credentials()
                    if _ok_gc:
                        st.success(_msg_gc)
                    else:
                        st.error(_msg_gc)

# ---------------- SAVED KUNDLIS VAULT & ACTIVE KUNDLI BAR ----------------
saved_list = auth_vault.get_saved_kundlis(u["id"]) if is_logged_in_now else []
active_lp = st.session_state.get('loaded_profile')

col_top_lang, col_top_font = st.columns([1.1, 1.4])
with col_top_lang:
    ui_lang = st.radio(" भाषा / Language", ["हिन्दी (Hindi)", "English"], horizontal=True, key="main_ui_lang_radio")
    is_hi = "हिन्दी" in ui_lang
with col_top_font:
    _font_scale_choice = st.radio(
        " फ़ॉन्ट आकार (Text Size):",
        ["मध्यम (18.5px)", "बड़ा (20.5px)", "अति विशाल (24px)"],
        index=1,
        horizontal=True,
        key="main_font_scale_choice_radio",
        help="अक्षरों का आकार छोटा या बड़ा करें"
    )

if "विशाल" in _font_scale_choice:
    chosen_font_px = "24px"
elif "मध्यम" in _font_scale_choice:
    chosen_font_px = "18.5px"
else:
    chosen_font_px = "20.5px"

st.markdown(f"""
<style>
:root {{
    --app-font-size: {chosen_font_px} !important;
}}
html, body {{
    font-size: {chosen_font_px} !important;
}}
p, span, li, label, .stMarkdown, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span {{
    font-size: {chosen_font_px} !important;
    line-height: 1.75 !important;
}}
.glass-card, .predict-card {{
    font-size: calc({chosen_font_px} * 1.02) !important;
    line-height: 1.75 !important;
}}
[style*="font-size: 0."], [style*="font-size:0."] {{
    font-size: calc({chosen_font_px} * 0.95) !important;
    line-height: 1.65 !important;
}}
.section-title, h1, h2, h3 {{
    font-size: calc({chosen_font_px} * 1.35) !important;
}}
</style>
""", unsafe_allow_html=True)

# If user has an active loaded profile, show active status bar & quick action controls
if is_logged_in_now and active_lp:
    col_act1, col_act2 = st.columns([2.4, 1.4])
    with col_act1:
        st.markdown(f"""
        <div style="background: {TH_CARD_BG}; border: {TH_CARD_BORDER}; border-radius: 12px; padding: 12px 18px; margin-bottom: 12px; box-shadow: 0 4px 18px rgba(0,0,0,0.06);">
            <div style="font-size: 0.74rem; color: {TH_GOLD_TITLE}; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">
                 आपकी सक्रिय प्राथमिक कुण्डली (Active Default Kundli)
            </div>
            <div style="font-family: var(--font-yatra); font-size: 1.42rem; color: {TH_NAME}; font-weight: 800; margin-top: 2px;">
                {active_lp.get('name', 'जातक')}
            </div>
            <div style="font-size: 0.86rem; color: {TH_MUTED}; margin-top: 3px; font-weight: 600;">
                 <b>जन्म:</b> {active_lp.get('dob')} ({active_lp.get('tob')}) &nbsp;|&nbsp; 
                <b>स्थान:</b> {active_lp.get('city', 'स्थान')} &nbsp;|&nbsp; 
                 <b>निर्देशांक:</b> {float(active_lp.get('lat', 28.61)):.2f}°N, {float(active_lp.get('lon', 77.20)):.2f}°E
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_act2:
        st.markdown('<div class="mobile-button-row">', unsafe_allow_html=True)
        c_btn_a, c_btn_b = st.columns(2)
        with c_btn_a:
            if st.button(" नई कुण्डली", key="new_k_top_btn", use_container_width=True, help="नये जातक का जन्म विवरण भरें"):
                st.session_state['show_birth_form'] = True
                st.session_state.pop('loaded_profile', None)
                st.rerun()
        with c_btn_b:
            toggle_btn_txt = " फॉर्म बंद करें" if st.session_state.get('show_birth_form') else " विवरण बदलें"
            if st.button(toggle_btn_txt, key="toggle_edit_k_btn", use_container_width=True, help="समय/स्थान संशोधित करें"):
                st.session_state['show_birth_form'] = not st.session_state.get('show_birth_form', False)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # If user has multiple saved kundlis, show a quick switch drawer
    if len(saved_list) >= 1:
        with st.expander(f" कुण्डली बदलें / सुरक्षित कुण्डलियाँ ({len(saved_list)})", expanded=False):
            k_disp_map = {f"{k['name']} ({k.get('dob')} - {k.get('city', '')})": k for k in saved_list}
            cur_id = active_lp.get('id')
            def_idx = 0
            for idx, k in enumerate(saved_list):
                if k.get('id') == cur_id:
                    def_idx = idx
                    break
            chosen_label = st.selectbox("सुरक्षित कुण्डली चुनें:", list(k_disp_map.keys()), index=def_idx, key="active_k_selector")
            chosen_k = k_disp_map[chosen_label]

            col_k1, col_k2, col_k3 = st.columns([1.2, 1, 1.2])
            with col_k1:
                if chosen_k.get('id') != active_lp.get('id'):
                    if st.button(" यह कुण्डली खोलें", key="switch_k_btn", use_container_width=True):
                        _load_kundli_into_session(chosen_k, user_id=u["id"])
                        st.rerun()
                else:
                    st.caption(" यह कुण्डली अभी सक्रिय है")
            with col_k2:
                if st.button(" हटाएं", key="del_k_btn", use_container_width=True):
                    ok_del, del_msg = auth_vault.delete_kundli(u["id"], chosen_k["id"])
                    if ok_del:
                        st.success(del_msg)
                        if active_lp.get('id') == chosen_k["id"]:
                            st.session_state.pop('loaded_profile', None)
                            st.session_state['data_generated'] = False
                        st.rerun()
                    else:
                        st.error(del_msg)
            with col_k3:
                if st.button(" इसे डिफ़ॉल्ट बनाएं", key="set_def_k_btn", use_container_width=True, help="हर बार ऐप खोलने पर यह कुण्डली स्वतः खुली मिलेगी"):
                    auth_vault.set_default_kundli(u["id"], chosen_k["id"])
                    st.success(f"'{chosen_k['name']}' को प्राथमिक डिफ़ॉल्ट कुण्डली सेट किया गया!")
                    st.rerun()

# If no active profile is loaded but user has saved kundlis, show a 1-click open prompt
if is_logged_in_now and not active_lp and saved_list:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(240,192,90,0.15) 0%, rgba(14,23,42,0.95) 100%);
                border: 1.5px solid #f0c05a; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px;">
        <div style="font-size: 1.05rem; font-weight: 800; color: #f0c05a; margin-bottom: 6px;">
            आपकी सुरक्षित कुण्डलियाँ उपलब्ध हैं (Saved Kundlis Ready)
        </div>
        <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 10px;">
            हर बार विवरण भरने की आवश्यकता नहीं है। नीचे से अपनी पूर्व सुरक्षित कुण्डली चुनें और 'कुण्डली खोलें' दबाएं:
        </div>
    </div>
    """, unsafe_allow_html=True)
    c_wel_1, c_wel_2 = st.columns([2.5, 1.2])
    with c_wel_1:
        welcome_map = {f"{k['name']} ({k.get('dob')} - {k.get('city', '')})": k for k in saved_list}
        w_sel_lbl = st.selectbox("सुरक्षित कुण्डली चुनें:", list(welcome_map.keys()), key="welcome_k_selector")
        w_sel_k = welcome_map[w_sel_lbl]
    with c_wel_2:
        st.write("") # spacing
        if st.button("कुण्डली खोलें (Open)", key="welcome_open_btn", type="primary", use_container_width=True):
            _load_kundli_into_session(w_sel_k, make_default=True, user_id=u["id"])
            st.rerun()

# Determine whether to show birth input form:
# Only show if user has no loaded profile OR clicked ' नई कुण्डली' / ' विवरण बदलें'
show_form = st.session_state.get('show_birth_form', False) or (active_lp is None)

lp = st.session_state.get('loaded_profile', {})
default_name = lp.get('name', 'जातक / Seeker' if not is_logged_in_now else u.get('name', 'जातक'))
default_city = lp.get('city', 'New Delhi, India')
default_lat = float(lp.get('lat', 28.6139))
default_lon = float(lp.get('lon', 77.2090))
default_tz = float(lp.get('tz', 5.5))

default_dob = datetime(1995, 1, 1).date()
if lp.get('dob'):
    try:
        default_dob = datetime.strptime(lp['dob'], "%Y-%m-%d").date()
    except Exception:
        pass

def_h, def_m, def_s = 12, 0, 0
if lp.get('tob'):
    try:
        parts = [int(p) for p in lp['tob'].split(':')]
        if len(parts) >= 1: def_h = parts[0]
        if len(parts) >= 2: def_m = parts[1]
        if len(parts) >= 3: def_s = parts[2]
    except Exception:
        pass

mode = "Natal Kundli (जन्म कुण्डली)"
generate = False
if show_form:
    st.markdown("""
    <div style="margin: 4px 0 16px; padding: 18px 22px; border-radius: 14px;
                background: radial-gradient(circle at 8% 0%, rgba(229,169,60,0.20) 0%, transparent 55%),
                            linear-gradient(135deg, rgba(19,27,54,0.96) 0%, rgba(8,12,26,0.96) 100%);
                border: 1px solid rgba(229,169,60,0.38); box-shadow: 0 18px 40px -24px #000;">
        <div style="font-family: 'Cinzel', serif; font-size: 1.45rem; font-weight: 800; color: #fef3c7; letter-spacing: 0.5px;">
             अपनी कुण्डली बनाएं / विवरण भरें
        </div>
        <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 5px;">
            जन्म विवरण भरें, फिर नीचे <b style="color:#f7d584;">“कुण्डली एवं ज्योतिषीय विश्लेषण बनाएं”</b> दबाएं।
            चाहें तो <b style="color:#f7d584;">“कुण्डली सुरक्षित करें”</b> से प्रोफ़ाइल वॉल्ट में भी रख सकते हैं।
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Mode / प्रकार" if is_hi else "Mode", ["Natal Kundli (जन्म कुण्डली)", "Prashna (प्रश्न कुण्डली)"] if is_hi else ["Natal Kundli", "Prashna (Horary)"], horizontal=True)

    if "Natal" in mode:
        name = st.text_input("Name / नाम" if is_hi else "Name", default_name)
        date_val = st.date_input("Date of Birth / जन्म तिथि" if is_hi else "Date of Birth", value=default_dob, min_value=datetime(1900, 1, 1).date(), max_value=datetime(2100, 12, 31).date(), format="DD/MM/YYYY")
        
        # Exact HH:MM:SS input for ultra micro-precision
        st.markdown("<small style='color: #f0c05a;'><b>Time of Birth (Hours : Mins : Secs) / जन्म समय</b></small>", unsafe_allow_html=True)
        t_col1, t_col2, t_col3 = st.columns(3)
        tob_hour = t_col1.number_input("Hour (घंटा)", min_value=0, max_value=23, value=def_h)
        tob_min = t_col2.number_input("Min (मिनट)", min_value=0, max_value=59, value=def_m)
        tob_sec = t_col3.number_input("Sec (सेकंड)", min_value=0, max_value=59, value=def_s)
        time_val = d_time(int(tob_hour), int(tob_min), int(tob_sec))
    else:
        name = st.text_input("Querent Name / प्रच्छक का नाम" if is_hi else "Querent Name", "Querent")
        prashna_category = st.selectbox(
            "प्रश्न विषय (Prashna Subject / Category)",
            [
                " नौकरी / कार्य सफलता (Career & Job)",
                "विवाह एवं प्रेम संबंध (Marriage & Romance)",
                " रोग मुक्ति व स्वास्थ्य (Health & Recovery)",
                "कोर्ट केस / वाद-विवाद (Court Case & Dispute)",
                " धन लाभ / फंसा हुआ धन (Wealth & Recovery of Dues)",
                "विदेश यात्रा / स्थानांतरण (Travel & Relocation)",
                " खोई हुई वस्तु / गुमशुदा (Lost Article / Missing Person)"
            ]
        )
        prashna_text = st.text_input("विशेष प्रश्न (Specific Question)", "क्या मेरा कार्य सिद्ध होगा?")
        st.session_state['prashna_meta'] = {"category": prashna_category, "text": prashna_text}
        st.info("प्रश्न कुण्डली में तात्कालिक सटीक समय व स्थान प्रयुक्त होगा (Prashna uses exact horary moment).")
        now = datetime.now()
        date_val = now.date()
        time_val = now.time()

    st.subheader("Birth Place / जन्म स्थान" if is_hi else "Birth Place")

    if '_pending_city_search_input' in st.session_state:
        st.session_state['city_search_input'] = st.session_state.pop('_pending_city_search_input')

    city_query = st.text_input("नगर/कस्बा खोजें (Type City / Town / Tehsil to search):", value=default_city, key="city_search_input")

    matched_cities = city_search.search_cities(city_query, limit=40) if city_search else []
    city_options = {}
    if matched_cities:
        for c in matched_cities:
            city_options[c["label"]] = c
    else:
        fallback_label = f"{city_query or default_city} (स्थान)"
        city_options[fallback_label] = {
            "label": fallback_label,
            "name": city_query or default_city,
            "lat": float(st.session_state.get('lat', default_lat)),
            "lon": float(st.session_state.get('lon', default_lon))
        }

    selected_city_label = st.selectbox(
        "नगर चुनें (Select Town / City from List):",
        options=list(city_options.keys()),
        index=0,
        key="selected_city_dropdown"
    )

    sel_city_data = city_options.get(selected_city_label)
    if sel_city_data and ('lat' in sel_city_data) and ('lon' in sel_city_data):
        if st.session_state.get('_last_chosen_city') != selected_city_label:
            st.session_state['lat'] = sel_city_data['lat']
            st.session_state['lon'] = sel_city_data['lon']
            st.session_state['city_name'] = sel_city_data['name']
            st.session_state['_last_chosen_city'] = selected_city_label

    city_name = st.session_state.get('city_name', sel_city_data.get('name', default_city) if sel_city_data else default_city)
            
    coord_col1, coord_col2 = st.columns(2)
    lat = coord_col1.number_input("Latitude (°N) / अक्षांश" if is_hi else "Latitude (°N)", value=float(st.session_state.get('lat', default_lat)), format="%.4f", step=0.01)
    lon = coord_col2.number_input("Longitude (°E) / रेखांश" if is_hi else "Longitude (°E)", value=float(st.session_state.get('lon', default_lon)), format="%.4f", step=0.01)
    st.session_state['lat'] = lat
    st.session_state['lon'] = lon

    tz_offset = st.number_input("Timezone Offset (Hours) / समय क्षेत्र", value=default_tz, step=0.5)

    col_ay1, col_ay2 = st.columns(2)
    with col_ay1:
        ayan_choice = st.selectbox("Ayanamsa (अयनांश)", ["Lahiri", "KP", "Raman"], index=0)
    with col_ay2:
        node_choice = st.selectbox("राहु-केतु नोड (Rahu Node)", ["Mean (औसत)", "True (स्पष्ट)"], index=0)

    # Save to vault and Generate buttons
    col_sv1, col_sv2 = st.columns([1, 1.2])
    with col_sv1:
        if st.button(" कुण्डली सुरक्षित करें", use_container_width=True, help="प्रोफ़ाइल वॉल्ट में सेव करें व डिफ़ॉल्ट बनाएं"):
            k_payload = {
                "name": name,
                "dob": date_val.strftime("%Y-%m-%d"),
                "tob": time_val.strftime("%H:%M:%S"),
                "city": city_name,
                "lat": lat,
                "lon": lon,
                "tz": tz_offset,
                "ayanamsa": ayan_choice
            }
            ok, s_msg = auth_vault.save_kundli(u["id"], k_payload)
            if ok:
                _latest = auth_vault.get_default_or_latest_kundli(u["id"]) or k_payload
                _load_kundli_into_session(_latest, make_default=True, user_id=u["id"])
                st.success(f"'{name}' की कुण्डली सुरक्षित व डिफ़ॉल्ट सेट हो गई! अगली बार ऐप खोलने पर यह स्वतः खुली मिलेगी।")
                st.rerun()
            else:
                st.warning(s_msg)

    with col_sv2:
        btn_lbl = "Generate Analysis & Birth Chart →" if not is_hi else "कुण्डली एवं ज्योतिषीय विश्लेषण बनाएं →"
        generate = st.button(btn_lbl, type="primary", use_container_width=True)
        if generate:
            st.session_state['show_birth_form'] = False
            st.session_state['data_generated'] = True
            st.session_state['loaded_profile'] = {
                "name": name,
                "dob": date_val.strftime("%Y-%m-%d"),
                "tob": time_val.strftime("%H:%M:%S"),
                "city": city_name,
                "lat": lat,
                "lon": lon,
                "tz": tz_offset,
                "ayanamsa": ayan_choice
            }
else:
    # Form is collapsed: use active profile data directly
    mode = "Natal Kundli (जन्म कुण्डली)"
    name = lp.get('name', 'जातक')
    city_name = default_city
    lat = default_lat
    lon = default_lon
    tz_offset = default_tz
    date_val = default_dob
    time_val = d_time(def_h, def_m, def_s)
    ayan_choice = lp.get('ayanamsa', 'Lahiri')
    node_choice = lp.get('node', 'Mean (औसत)')
    generate = False

# Calculate Core Structures
# Input signature: the cached chart must be invalidated whenever ANY birth-input
# changes. Previously only the Generate button could refresh it, so users who
# edited dob/tob/place and re-rendered kept seeing the OLD chart silently.
_birth_input_sig = (
    date_val.isoformat(), time_val.isoformat(), round(float(lat), 6),
    round(float(lon), 6), round(float(tz_offset), 4), ayan_choice, node_choice,
)
if (generate or 'data_generated' not in st.session_state
        or st.session_state.get('_birth_input_sig') != _birth_input_sig
        or 'chart' not in st.session_state):
    dt = datetime.combine(date_val, time_val)
    dt_utc = dt - timedelta(hours=tz_offset)
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    vyas_ephem.set_ayanamsa(ayan_choice)
    vyas_ephem.set_node_model("true" if "True" in node_choice else "mean")
    with st.spinner("Executing Micro-Degree Ephemeris, D60 & KP Cuspal Mathematics..."):
        try:
            raw_pos = planet_positions(dt_utc)
            asc_lon = ascendant_sidereal(dt_utc, lat, lon)
            
            planets = {n: PlanetState(n, p.longitude, p.speed) for n, p in raw_pos.items()}
            chart = Chart(asc_lon, planets)
            
            # Placidus cusps
            kp_cusps = calculate_placidus_cusps_sidereal(dt_utc, lat, lon)
            
            # Vimshottari Dasha Engine
            dasha_eng = VimshottariDasha(chart.planets["Moon"].longitude, dt)
            vargas_matrix = get_all_vargas_matrix(chart)
            
            st.session_state['birth'] = {'local': dt, 'lat': lat, 'lon': lon, 'tz': tz_offset, 'name': name, 'city': city_name}
            st.session_state['chart'] = chart
            st.session_state['kp_cusps'] = kp_cusps
            st.session_state['dasha_engine'] = dasha_eng
            st.session_state['vargas_matrix'] = vargas_matrix
            st.session_state['data_generated'] = True
            st.session_state['_birth_input_sig'] = _birth_input_sig
            for k in ('panchang', 'gochar', 'predictions'):
                st.session_state.pop(k, None)
        except Exception as e:
            st.error(f"Error calculating: {e}")

if st.session_state.get('data_generated'):
    chart = st.session_state['chart']
    birth = st.session_state['birth']
    kp_cusps = st.session_state['kp_cusps']
    dasha_engine = st.session_state['dasha_engine']
    vargas_matrix = st.session_state['vargas_matrix']
    asc_sign_idx = chart.ascendant_sign

    # Global predictive and astrological precomputations (MEMOIZED in session_state to prevent lag)
    if 'dignities' not in st.session_state or st.session_state.get('_calc_sig') != _birth_input_sig:
        st.session_state['dignities'] = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_matrix)
        st.session_state['bhavas'] = forensic_predictor.analyze_all_12_bhavas(chart, st.session_state['dignities'])
        p_signs_map = {n: p.sign_index for n, p in chart.planets.items()}
        st.session_state['av_res'] = vyas_ashtaka.compute_ashtakavarga(p_signs_map, asc_sign_idx)
        st.session_state['_calc_sig'] = _birth_input_sig

    dignities = st.session_state['dignities']
    bhavas = st.session_state['bhavas']
    av_res = st.session_state['av_res']
    sav = av_res["sav"]
    cur_dasha = dasha_engine.get_running_dasha(datetime.now()) if hasattr(dasha_engine, 'get_running_dasha') else dasha_engine.get_dasha_at(datetime.now())

    d1_houses = {h: [] for h in range(1, 13)}
    for h in range(1, 13):
        sign = (asc_sign_idx + h - 1) % 12
        d1_houses[h].append(str(sign + 1))
        
    for p_name, p in chart.planets.items():
        house_num = (p.sign_index - asc_sign_idx + 12) % 12 + 1
        p_hi_abbr = constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]
        abbr = f"{p_hi_abbr} {int(p.longitude % 30)}°{int((p.longitude % 1)*60):02d}'"
        if p.is_retrograde:
            abbr += " (R)" if not is_hi else " (व)"
        d1_houses[house_num].append(abbr)

    # -------------------------------------------------------------------------
    # ACHARYA VYAS LIVE VEDIC CONSULTATION TRIGGER BAR
    # -------------------------------------------------------------------------
    col_bot_bar1, col_bot_bar2 = st.columns([3.5, 1.5])
    with col_bot_bar1:
        st.markdown(f"""
        <div class="consultation-banner-card" style="background: {TH_CARD_BG};
                    border: {TH_CARD_BORDER}; border-radius: 14px; padding: 14px 18px; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 18px rgba(0,0,0,0.06);">
            <div style="font-family: 'Yatra One', serif; font-size: 2.2rem; line-height: 1; color: {TH_GOLD}; font-weight: 900; border: 2px solid {TH_GOLD}; border-radius: 50%; width: 52px; height: 52px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 0 14px rgba(37,99,235,0.2);">ॐ</div>
            <div>
                <div style="font-family: 'Yatra One', serif; font-weight: 700; color: {TH_GOLD}; font-size: clamp(1.15rem, 3.8vw, 1.4rem); letter-spacing: 0.4px;">
                    आचार्य व्यास • प्रत्यक्ष वैदिक संवाद (Live Consultation)
                </div>
                <div style="color: {TH_MUTED}; font-size: clamp(0.92rem, 2.8vw, 1.05rem); margin-top: 4px; line-height: 1.5; font-weight: 600;">
                    आपकी कुण्डली, चालू विंशोत्तरी दशा व तात्कालिक गोचर पर आधारित सीधा समाधान
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_bot_bar2:
        st.markdown('<div class="consultation-action-btn">', unsafe_allow_html=True)
        if st.button("परामर्श प्रारंभ करें (Chat Now)", key="open_acharya_bot_bar_btn", use_container_width=True):
            st.session_state["show_acharya_dialog"] = True
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # DOMAIN SUITE NAVIGATION (Moved to Sidebar to keep interface clean and compact)
    # -------------------------------------------------------------------------
    suite_options = [
        "व्यक्तिगत दैनिक राशिफल" if is_hi else "Daily Horoscope & Timing",
        "दिव्य प्रश्न कुण्डली (Horary & Mook Prashna)" if is_hi else "Horary & Mook Prashna",
        "कुण्डली एवं षोडशवर्ग" if is_hi else "Birth Charts & 16 Vargas",
        "वैदिक फलित एवं शास्त्रीय सूत्र" if is_hi else "Vedic Forecast & Classical Sutras",
        "अष्टकूट मिलान एवं परिहार" if is_hi else "Compatibility & Dosha Parihara",
        "लाल किताब सम्पूर्ण" if is_hi else "Lal Kitab System & Remedies",
        "दशा, गोचर एवं वर्षफल" if is_hi else "Dasha, Transits & Varshphal",
        "जन्म समय शुद्धि (BTR)" if is_hi else "Birth Time Rectification",
        "अष्टकवर्ग, षड्बल एवं मैत्री" if is_hi else "Ashtakavarga & Strengths",
        "केपी, जैमिनी, नाड़ी एवं चक्र" if is_hi else "KP, Jaimini, Nadi & Chakras",
        "शोध प्रबंध PDF" if is_hi else "Publication PDF"
    ]

    # Pre-select Daily Horoscope if triggered
    if st.session_state.pop("_jump_to_daily_suite", False):
        st.session_state["domain_suite_sidebar_radio"] = "व्यक्तिगत दैनिक राशिफल" if is_hi else "Daily Horoscope & Timing"

    with st.sidebar:
        st.markdown("""
        <div style="margin: 16px 0 6px; padding: 10px 14px; background: linear-gradient(135deg, rgba(240,192,90,0.2) 0%, rgba(14,23,42,0.92) 100%); border-left: 4px solid #f0c05a; border-radius: 8px;">
            <div style="font-family: var(--font-yatra); font-size: 1.05rem; font-weight: 700; color: #f0c05a;">
                ज्योतिष अनुसंधान प्रभाग (Domain Suites)
            </div>
            <div style="font-size: 0.74rem; color: #cbd5e1;">(यहाँ से मुख्य प्रभाग / टैब चुनें)</div>
        </div>
        """, unsafe_allow_html=True)
        selected_suite = st.radio(
            "चयनित ज्योतिषीय अनुसंधान प्रभाग (Select Domain Suite):",
            suite_options,
            key="domain_suite_sidebar_radio",
            label_visibility="collapsed"
        )

        if is_logged_in_now and len(saved_list) > 1:
            with st.expander(f"कुण्डली बदलें ({len(saved_list)})", expanded=False):
                sb_k_map = {f"{k['name']} ({k.get('dob')})": k for k in saved_list}
                cur_k_id = active_lp.get('id') if active_lp else None
                cur_k_idx = 0
                for idx, k in enumerate(saved_list):
                    if k.get('id') == cur_k_id:
                        cur_k_idx = idx
                        break
                sb_sel_lbl = st.selectbox("कुण्डली चुनें:", list(sb_k_map.keys()), index=cur_k_idx, key="sb_kundli_switcher")
                sb_sel_k = sb_k_map[sb_sel_lbl]
                if sb_sel_k.get('id') != cur_k_id:
                    if st.button("खोलें", key="sb_switch_btn", use_container_width=True):
                        _load_kundli_into_session(sb_sel_k, user_id=u["id"])
                        st.rerun()

        # Creator Info in Sidebar Footer (subtle & dignified)
        st.markdown("""
        <div style="margin-top: 25px; padding: 12px 14px; background: rgba(14, 23, 42, 0.85); border: 1px solid rgba(240, 192, 90, 0.28); border-radius: 10px; text-align: center;">
            <div style="font-size: 0.72rem; color: #eedc9a; letter-spacing: 0.8px; text-transform: uppercase; font-weight: 600;">शोध एवं निर्माण (Creator):</div>
            <div style="font-family: var(--font-yatra); font-size: 1.05rem; font-weight: 700; color: #f0c05a; margin-top: 2px;">निखिल व्यास (Nikhil Vyas)</div>
            <div style="font-size: 0.76rem; color: #cbd5e1; margin-top: 4px; line-height: 1.5;">
                 <a href="mailto:inikhilvyas@gmail.com" style="color: #93c5fd; text-decoration: none;">inikhilvyas@gmail.com</a><br/>
                 <a href="tel:+919414121172" style="color: #93c5fd; text-decoration: none;">+91 94141 21172</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MORNING 7:00 AM DAILY HOROSCOPE BANNER
    # (Only shown on other tabs so it doesn't clutter the daily horoscope tab itself)
    # -------------------------------------------------------------------------
    if selected_suite not in ["व्यक्तिगत दैनिक राशिफल", "Daily Horoscope & Timing"]:
        col_m_banner1, col_m_banner2 = st.columns([3.5, 1.5])
        with col_m_banner1:
            st.markdown(f"""
            <div class="consultation-banner-card" style="background: {TH_CARD_BG};
                        border: {TH_CARD_BORDER}; border-radius: 12px; padding: 12px 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 18px rgba(0,0,0,0.06);">
                <div>
                    <div style="font-family: var(--font-yatra); font-weight: 700; color: {TH_GOLD_TITLE}; font-size: clamp(1.05rem, 3.2vw, 1.25rem);">
                        प्रातः 7:00 AM दैनिक राशिफल अलर्ट • {birth.get('name', 'जातक')}
                    </div>
                    <div style="font-size: clamp(0.85rem, 2.5vw, 0.95rem); color: {TH_MUTED}; margin-top: 2px; font-weight: 600;">
                        नवतारा चक्र, गोचरस्थ चन्द्रमा एवं चालू विंशोत्तरी दशा के आधार पर आज का दिन फल उपलब्ध है।
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_m_banner2:
            st.markdown('<div class="consultation-action-btn">', unsafe_allow_html=True)
            def _jump_to_daily_suite_cb():
                st.session_state["domain_suite_sidebar_radio"] = "व्यक्तिगत दैनिक राशिफल" if is_hi else "Daily Horoscope & Timing"

            st.button(" आज का राशिफल देखें", key="jump_daily_horo_top_btn", on_click=_jump_to_daily_suite_cb, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN SCREEN DOMAIN SUITE SELECTOR (Native Mobile Nav & Desktop Quick Nav)
    # -------------------------------------------------------------------------
    cur_suite_idx = 0
    if selected_suite in suite_options:
        cur_suite_idx = suite_options.index(selected_suite)

    def _sync_suite_from_main():
        st.session_state["domain_suite_sidebar_radio"] = st.session_state["main_screen_suite_select"]

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin: 12px 2px 6px 2px;">
        <span style="font-size: 0.86rem; color: {TH_GOLD}; letter-spacing: 1px; text-transform: uppercase; font-weight: 800;">
            ज्योतिष अनुसंधान प्रभाग (Domain Suite)
        </span>
        <span style="font-size: 0.80rem; color: {TH_MUTED}; font-weight: 700;">
            (यहाँ से प्रभाग बदलें)
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.selectbox(
        "मुख्य अनुसंधान प्रभाग चुनें (Select Domain Suite):",
        suite_options,
        index=cur_suite_idx,
        key="main_screen_suite_select",
        on_change=_sync_suite_from_main,
        label_visibility="collapsed"
    )

    # -------------------------------------------------------------------------
    # PRASHNA KUNDLI HORARY JUDGEMENT (तात्कालिक प्रश्न विचार व फलित)
    # -------------------------------------------------------------------------
    if "Prashna" in mode or "प्रश्न" in selected_suite or "Prashna" in selected_suite:
        st.markdown(f'<div class="section-title">{"दिव्य प्रश्न कुण्डली एवं मूक प्रश्न विचार (Horary & Thought Detection)" if is_hi else "Horary & Thought Detection"}</div>', unsafe_allow_html=True)
        
        # Method selection (Dual Mode: KP 1-249 Horary Seed + Real-Time Prana Lagna)
        col_pr1, col_pr2, col_pr3 = st.columns([1.2, 1.2, 1.6])
        with col_pr1:
            horary_method = st.radio(
                "प्रश्न निर्धारण पद्धति (Horary Method):",
                ["के.पी. होरारी (1-249 अंक)", "तात्कालिक प्राण लग्न (24-Sec Clock)", "संयुक्त महा-संगम (Dual Synthesis)"],
                index=2,
                key="horary_method_choice"
            )
        with col_pr2:
            seed_input = st.number_input(
                "के.पी. होरारी सीड अंक (1-249):",
                min_value=1,
                max_value=249,
                value=int(st.session_state.get('prashna_kp_seed', 108)),
                step=1,
                key="kp_seed_num_input"
            )
            st.session_state['prashna_kp_seed'] = seed_input
            if st.button("अंतर्ज्ञान से अंक रोल करें (Roll Random Seed)", use_container_width=True):
                import random
                new_seed = random.randint(1, 249)
                st.session_state['prashna_kp_seed'] = new_seed
                st.session_state['prashna_active_domain_id'] = None
                st.rerun()
        with col_pr3:
            s_seed_data = vyas_prashna.get_kp_seed_data(seed_input)
            seed_card_html = f"""<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(229,169,60,0.25); border-radius: 8px; padding: 10px; font-size: 0.85rem; color: #cbd5e1;"><b>के.पी. अंक {seed_input} विवरण:</b><br/>राशि: <b>{s_seed_data.sign_name}</b> ({constants.PLANETS_HI.get(s_seed_data.sign_lord, s_seed_data.sign_lord)}) | नक्षत्र: <b>{s_seed_data.star_name}</b> ({constants.PLANETS_HI.get(s_seed_data.star_lord, s_seed_data.star_lord)})<br/>उप-स्वामी (SL): <b style='color: #facc15;'>{constants.PLANETS_HI.get(s_seed_data.sub_lord, s_seed_data.sub_lord)}</b><br/>विस्तार: <code>{s_seed_data.span_str}</code></div>"""
            st.markdown(seed_card_html, unsafe_allow_html=True)

        # Detect Mook Prashna Intent
        target_seed = seed_input if ("249" in horary_method or "संयुक्त" in horary_method) else None
        mook_res = vyas_prashna.detect_mook_prashna_intent(chart, kp_seed_num=target_seed, dt_local=birth.get('local', datetime.now()))
        
        # Mook Prashna Display Card
        top_domain = mook_res["top_domain"]
        active_domain_id = st.session_state.get("prashna_active_domain_id", top_domain["id"])
        active_domain = next((d for d in vyas_prashna.QUESTION_DOMAINS if d["id"] == active_domain_id), top_domain)
        
        mook_card_html = f"""<div class="glass-card" style="border: 2px solid #f59e0b; background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(15, 23, 42, 0.95) 100%); margin-top: 15px; margin-bottom: 15px;">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
<div style="font-size: 1.18rem; font-weight: 800; color: #fbbf24;">मूक प्रश्न: मनोगत विचार संसूचक (Mook Prashna Thought Detector)</div>
<span style="background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); padding: 4px 10px; border-radius: 20px; font-weight: 800; font-size: 0.85rem;">{mook_res['confidence_pct']}% खगोलीय सामंजस्य</span>
</div>
<div style="font-size: 1.05rem; color: #fef3c7; margin-top: 10px; line-height: 1.6;">हमारी खगोलीय व के.पी. गणना के अनुसार, इस क्षण आपका मन मुख्यतः <b style="color: #38bdf8; font-size: 1.15rem;">'{top_domain['title_hi']}'</b> से सम्बद्ध प्रतीत होता है।</div>
<div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 8px; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #f59e0b;"><b>शास्त्रीय प्रमाण:</b> {mook_res['reasoning_hi']}</div>
</div>"""
        st.markdown(mook_card_html, unsafe_allow_html=True)
        
        # Interactive Question Chips / Selection
        st.markdown("<b>क्या यही आपका प्रश्न है, अथवा कोई अन्य विषय चुनना चाहते हैं?</b>", unsafe_allow_html=True)
        chip_cols = st.columns(3)
        for idx, dom in enumerate(vyas_prashna.QUESTION_DOMAINS):
            col_target = chip_cols[idx % 3]
            is_active = (dom["id"] == active_domain_id)
            btn_label = f"{'' if is_active else ''}{dom['title_hi'].split('(')[0].strip()}"
            if col_target.button(btn_label, key=f"chip_dom_{dom['id']}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state["prashna_active_domain_id"] = dom["id"]
                st.rerun()

        # Custom Question Text
        custom_q = st.text_input(
            "अपना विशिष्ट प्रश्न दर्ज करें (या डिफ़ॉल्ट रहने दें):",
            value=active_domain.get("default_question", "क्या मेरा कार्य सिद्ध होगा?"),
            key=f"prashna_custom_q_{active_domain_id}"
        )

        # Evaluate Horary Decision for Active Domain
        tajik_res = vyas_prashna.evaluate_tajik_horary_judgement(chart, target_house=active_domain["prime_house"], kp_seed_num=target_seed)

        # Horary Verdict Card
        verdict_card_html = f"""<div class="glass-card" style="border: 2px solid {tajik_res['verdict_color']}; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%); margin-top: 15px;">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
<div>
<span style="font-size: 1.25rem; font-weight: 800; color: #f0c05a;">ताजिक एवं के.पी. प्रश्न निर्णय (Final Horary Judgement)</span>
<div style="font-size: 0.92rem; color: #fef3c7; margin-top: 4px;"><b>विषय:</b> {active_domain['title_hi']} | <b>प्रश्न:</b> "{custom_q}"</div>
</div>
<span style="background: {tajik_res['verdict_color']}; color: black; font-weight: 800; padding: 6px 16px; border-radius: 20px; font-size: 0.92rem;">{tajik_res['verdict_hi']}</span>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; font-size: 0.88rem; color: #cbd5e1; margin-top: 14px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px;">
<div><b>प्रच्छक (लग्न):</b> {tajik_res['lagna_sign_hi']} (स्वामी: {tajik_res['lagnesh_hi']})</div>
<div><b>कार्य भाव:</b> भाव {tajik_res['target_house']} ({tajik_res['target_sign_hi']})</div>
<div><b>कार्येश ग्रह:</b> {tajik_res['karyesh_hi']}</div>
<div><b>चन्द्रमा (कार्यवाहक):</b> {tajik_res['moon_sign_hi']} ({tajik_res['moon_hi']})</div>
</div>
<div style="background: rgba(0,0,0,0.35); padding: 12px 14px; border-radius: 8px; border-left: 4px solid {tajik_res['verdict_color']}; margin-top: 14px;">
<div style="font-weight: 700; color: #facc15; font-size: 1.02rem; margin-bottom: 4px;">{tajik_res['yoga_name']}</div>
<div style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc;">{tajik_res['yoga_desc']}</div>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 14px; font-size: 0.92rem;">
<div style="background: rgba(15, 23, 42, 0.7); padding: 10px 14px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.78rem; color: #94a3b8; text-transform: uppercase;">कार्य सिद्धि की समय सीमा (Timeline)</div>
<div style="font-size: 1.02rem; font-weight: 700; color: #38bdf8; margin-top: 2px;">{tajik_res['timeline_str']}</div>
</div>
<div style="background: rgba(15, 23, 42, 0.7); padding: 10px 14px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
<div style="font-size: 0.78rem; color: #94a3b8; text-transform: uppercase;">अनुकूल दिशा सूचक (Direction)</div>
<div style="font-size: 1.02rem; font-weight: 700; color: #4ade80; margin-top: 2px;">{tajik_res['direction_info']}</div>
<div style="font-size: 0.75rem; color: #94a3b8;">{tajik_res['direction_desc']}</div>
</div>
</div>
</div>"""
        st.markdown(verdict_card_html, unsafe_allow_html=True)

        col_pr_btn1, col_pr_btn2 = st.columns([1.5, 1])
        with col_pr_btn1:
            if st.button("आचार्य व्यास से इस प्रश्न पर सीधे संवाद करें (Chat Now)", type="primary", use_container_width=True, key="prashna_live_chat_btn"):
                st.session_state['prashna_meta'] = {"category": active_domain['title_hi'], "text": custom_q}
                st.session_state["show_acharya_dialog"] = True
                st.rerun()

    # =========================================================================
    # SUITE 0:  HYPER-PERSONALISED DAILY HOROSCOPE
    # =========================================================================
    if "दैनिक" in selected_suite or "Daily" in selected_suite:
        st.markdown(f'<div class="section-title">{" जातक का व्यक्तिगत दैनिक राशिफल (नवतारा चक्र + गोचर + चालू दशा)" if is_hi else " Personalised Daily Horoscope (Navatara + Transit + Active Dasha)"}</div>', unsafe_allow_html=True)
        
        # Calculate daily horoscope using native location timezone
        target_tz = timezone(timedelta(hours=birth.get('tz', 5.5)))
        now_dt = datetime.now(timezone.utc).astimezone(target_tz)
        # Transit moon longitude using current time
        try:
            cur_raw_pos = planet_positions(now_dt)
            transit_moon_lon = cur_raw_pos["Moon"].longitude
        except Exception:
            transit_moon_lon = (chart.planets["Moon"].longitude + 13.2) % 360.0
        
        cur_dasha_str = cur_dasha.get("full_path", "Jupiter-Saturn") if isinstance(cur_dasha, dict) else str(cur_dasha)
        _today_str = now_dt.strftime("%Y-%m-%d")
        if (st.session_state.get('_daily_cache_day') != _today_str 
                or st.session_state.get('_daily_cache_sig') != _birth_input_sig
                or 'daily_res' not in st.session_state):
            daily_res = vyas_daily.generate_daily_horoscope(
                chart.planets["Moon"].longitude,
                chart.ascendant_longitude,
                cur_dasha_str,
                transit_moon_lon,
                now_dt,
                lat=birth.get('lat', 28.6139),
                lon=birth.get('lon', 77.2090),
                tz_hours=birth.get('tz', 5.5)
            )
            st.session_state['daily_res'] = daily_res
            st.session_state['_daily_cache_day'] = _today_str
            st.session_state['_daily_cache_sig'] = _birth_input_sig
        else:
            daily_res = st.session_state['daily_res']

        # Render Top Score Cards with High Contrast Calibration
        score = daily_res["overall_score"]
        if score >= 75:
            score_color = "#34d399" if not _is_light else "#059669"
            dial_border = "3.5px solid #10b981"
            dial_bg = "rgba(16, 185, 129, 0.14)" if not _is_light else "#ecfdf5"
            dial_glow = "0 0 18px rgba(52, 211, 153, 0.45)"
            status_txt = "अनुकूल (Favourable)" if is_hi else "Favourable"
        elif score >= 55:
            score_color = "#fbbf24" if not _is_light else "#d97706"
            dial_border = "3.5px solid #f59e0b"
            dial_bg = "rgba(245, 158, 11, 0.14)" if not _is_light else "#fffbeb"
            dial_glow = "0 0 18px rgba(251, 191, 36, 0.45)"
            status_txt = "सामान्य (Moderate)" if is_hi else "Moderate"
        else:
            score_color = "#f87171" if not _is_light else "#dc2626"
            dial_border = "3.5px solid #ef4444"
            dial_bg = "rgba(239, 68, 68, 0.14)" if not _is_light else "#fef2f2"
            dial_glow = "0 0 18px rgba(248, 113, 113, 0.45)"
            status_txt = "सतर्क (Cautious)" if is_hi else "Cautious"
        
        # 4-PANEL DASHBOARD (Matching Reference Figma/UI Mockup)
        col_d1, col_d2, col_d3, col_d4 = st.columns([1.1, 1.3, 1.2, 1.4])
        
        with col_d1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="font-size: 0.88rem; letter-spacing: 1.2px; color: {TH_GOLD}; font-weight: 800; text-transform: uppercase;">VYAS DAY INDEX</div>
                <div style="margin: 12px auto; position: relative; width: 104px; height: 104px; border-radius: 50%; border: {dial_border}; background: {dial_bg}; display: flex; align-items: center; justify-content: center; box-shadow: {dial_glow};">
                    <div style="font-family: 'Cinzel', serif; font-size: 2.6rem; font-weight: 900; color: {score_color}; line-height: 1;">{score}</div>
                </div>
                <div style="font-size: 1.08rem; font-weight: 800; color: {score_color};">{status_txt}</div>
                <div style="margin-top: 10px; font-size: 0.94rem; color: {TH_MUTED}; text-align: left; font-weight: 600;">
                    <div>ऊर्जा (Energy): <b style="color: {TH_GOLD_ACCENT};">{daily_res['scores']['health']}%</b></div>
                    <div>एकाग्रता (Focus): <b style="color: {TH_GOLD_ACCENT};">{daily_res['scores']['career']}%</b></div>
                    <div>वृद्धि (Growth): <b style="color: {TH_GOLD_ACCENT};">{daily_res['scores']['wealth']}%</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_d2:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.88rem; letter-spacing: 1.2px; color: #94a3b8; font-weight: 700; text-transform: uppercase;">TODAY'S INSIGHT</div>
                    <div style="font-size: 1.18rem; font-weight: 800; color: #e5a93c; margin: 10px 0 6px 0;">{daily_res['tara_name']}</div>
                    <div style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.6;">{daily_res['tara_desc']}</div>
                </div>
                <div style="border-top: 1px solid rgba(229, 169, 60, 0.15); padding-top: 8px; margin-top: 12px; font-size: 0.92rem; color: #cbd5e1;">
                    <b>सक्रिय दशा:</b> <span style="color: #fef3c7;">{daily_res['running_dasha']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_d3:
            sun_p = chart.planets.get("Sun")
            moon_p = chart.planets.get("Moon")
            jup_p = chart.planets.get("Jupiter")
            sat_p = chart.planets.get("Saturn")
            st.markdown(f"""
            <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="font-size: 0.88rem; letter-spacing: 1.2px; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">CELESTIAL STATE</div>
                <div style="font-size: 0.95rem; color: #e2e8f0; display: flex; flex-direction: column; gap: 7px;">
                    <div style="display: flex; justify-content: space-between;"><span> सूर्य:</span> <b>{constants.SIGNS_HI[sun_p.sign_index]} {int(sun_p.longitude%30)}°</b></div>
                    <div style="display: flex; justify-content: space-between;"><span> चन्द्र:</span> <b>{constants.SIGNS_HI[moon_p.sign_index]} {int(moon_p.longitude%30)}°</b></div>
                    <div style="display: flex; justify-content: space-between;"><span> गुरु:</span> <b>{constants.SIGNS_HI[jup_p.sign_index]} {int(jup_p.longitude%30)}°</b></div>
                    <div style="display: flex; justify-content: space-between;"><span>शनि:</span> <b>{constants.SIGNS_HI[sat_p.sign_index]} {int(sat_p.longitude%30)}°</b></div>
                </div>
                <div style="border-top: 1px solid rgba(229, 169, 60, 0.15); padding-top: 6px; margin-top: 8px; font-size: 0.92rem; color: #f0c05a; font-weight: 600;">
                    नक्षत्र: {daily_res['natal_nakshatra']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_d4:
            amrit_v = daily_res.get('amrit_vela', '-')
            if "कोई नहीं" in amrit_v or "वर्जित" in amrit_v or "Prohibited" in amrit_v or "बुधवार" in amrit_v:
                abhijit_ui = '<span style="color: #ef4444; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 6px; border-radius: 4px; display: inline-block;"> कोई नहीं (बुधवार को नहीं होता)</span>'
            else:
                abhijit_ui = f'<span style="color: #38bdf8; font-weight: 600;">{amrit_v}</span>'

            st.markdown(f"""
            <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="font-size: 0.88rem; letter-spacing: 1.2px; color: #94a3b8; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">IMPORTANT TIMINGS</div>
                <div style="font-size: 0.95rem; display: flex; flex-direction: column; gap: 7px;">
                    <div><b>अभिजीत मुहूर्त:</b> <br>{abhijit_ui}</div>
                    <div><b>राहुकाल (सावधानी):</b> <br><span style="color: #f87171; font-weight: 600;">{daily_res['rahu_kalam']}</span></div>
                </div>
                <div style="border-top: 1px solid rgba(229, 169, 60, 0.15); padding-top: 6px; margin-top: 6px; font-size: 0.92rem; color: #cbd5e1;">
                    <b>शुभ रंग:</b> <span style="color: #fef3c7;">{daily_res['lucky_color']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # TODAY'S COMPLETE VEDIC PANCHANG & AUSPICIOUS MUHURTAS
        # ---------------------------------------------------------------------
        try:
            from vyas import panchang as vyas_panchang
            daily_panchang = vyas_panchang.compute(now_dt, birth.get('lat', 28.6139), birth.get('lon', 77.2090), birth.get('tz', 5.5))
        except Exception:
            daily_panchang = None

        wd = now_dt.weekday()
        disha_map = {
            0: ("पूर्व (East)", "दर्पण देखकर अथवा थोड़ा दूध पीकर प्रस्थान करें"),
            1: ("उत्तर (North)", "गुड़ अथवा धनिया खाकर प्रस्थान करें"),
            2: ("उत्तर (North)", "तिल अथवा गुड़ खाकर प्रस्थान करें"),
            3: ("दक्षिण (South)", "दही अथवा जीरा खाकर प्रस्थान करें"),
            4: ("पश्चिम (West)", "जौ अथवा राई खाकर प्रस्थान करें"),
            5: ("पूर्व (East)", "अदरक अथवा उड़द खाकर प्रस्थान करें"),
            6: ("पश्चिम (West)", "घी अथवा दलिया खाकर प्रस्थान करें"),
        }
        shool_dir, shool_rem = disha_map.get(wd, ("पूर्व", "ईश्वर स्मरण कर प्रस्थान करें"))

        def _safe_panchang_time_fmt(val):
            if not val:
                return ""
            if isinstance(val, str):
                parts = val.split()
                if len(parts) == 2:
                    try:
                        return datetime.strptime(parts[1], "%H:%M:%S").strftime("%I:%M %p")
                    except Exception:
                        return parts[1]
                elif len(parts) == 1:
                    try:
                        return datetime.strptime(parts[0], "%H:%M:%S").strftime("%I:%M %p")
                    except Exception:
                        return parts[0]
                return val
            if hasattr(val, 'strftime'):
                return val.strftime("%I:%M %p")
            return str(val)

        if daily_panchang:
            if getattr(daily_panchang, 'has_dual_tithi', False):
                tithi_html = f"""<div style="font-size: 0.88rem; font-weight: 700; color: #f8fafc; line-height: 1.45; margin-top: 2px;"><div><b>उदयातिथि:</b> {daily_panchang.udaya_tithi_hi} <span style="color: #94a3b8; font-weight: 400; font-size: 0.82rem;">({daily_panchang.udaya_tithi_end_rel} तक)</span></div><div style="color: #38bdf8; margin-top: 2px;"><b>तत्पश्चात:</b> {daily_panchang.next_tithi_hi} <span style="color: #93c5fd; font-weight: 400; font-size: 0.82rem;">({daily_panchang.next_tithi_end_rel} तक)</span></div></div>"""
            else:
                tithi_end_disp = daily_panchang.udaya_tithi_end_rel or _safe_panchang_time_fmt(daily_panchang.tithi_end)
                tithi_html = f"""<div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 2px;">{daily_panchang.udaya_tithi_hi or daily_panchang.tithi_hi} <span style="color: #cbd5e1; font-weight: 400; font-size: 0.85rem;">({tithi_end_disp} तक)</span></div>"""

            nak_timeline = getattr(daily_panchang, 'nakshatra_timeline_hi', None)
            if not nak_timeline:
                nak_str = f"{daily_panchang.nakshatra_hi} पद {daily_panchang.nakshatra_pada} (स्वामी: {constants.PLANETS_HI.get(daily_panchang.nakshatra_lord, daily_panchang.nakshatra_lord)})"
            else:
                nak_str = f"{nak_timeline} (स्वामी: {constants.PLANETS_HI.get(daily_panchang.nakshatra_lord, daily_panchang.nakshatra_lord)})"

            yoga_timeline = getattr(daily_panchang, 'yoga_timeline_hi', None)
            yoga_str = yoga_timeline if yoga_timeline else f"{daily_panchang.yoga}"

            karana_timeline = getattr(daily_panchang, 'karana_timeline_hi', None)
            karana_str = karana_timeline if karana_timeline else f"{getattr(daily_panchang, 'karana', 'बव')}"

            sunrise_str = _safe_panchang_time_fmt(daily_panchang.sunrise) or "06:30 AM"
            sunset_str = _safe_panchang_time_fmt(daily_panchang.sunset) or "05:45 PM"
            vara_str = f"{daily_panchang.vara} (स्वामी: {constants.PLANETS_HI.get(daily_panchang.vara_lord, daily_panchang.vara_lord)})"
            vikram_str = f"विक्रम संवत {daily_panchang.vikram_samvat} | शक संवत {daily_panchang.shaka_samvat}"
        else:
            tithi_html = '<div style="font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 2px;">शुक्ल/कृष्ण पक्ष तिथि</div>'
            nak_str = daily_res.get('transit_nakshatra', '-')
            yoga_str = "शुभ योग"
            karana_str = "बव"
            sunrise_str = "06:30 AM"
            sunset_str = "05:45 PM"
            vara_str = now_dt.strftime("%A")
            vikram_str = "विक्रम संवत 2083"

        # Collect daytime Shubh Horas for the panchang card
        shubh_horas_summary = []
        for h in daily_res.get('horas_day', []):
            if h.get('color') == '#10b981':
                shubh_horas_summary.append(f"<b>{h['lord_hi']}</b> ({h['start']}-{h['end']})")
        shubh_horas_summary_str = " | ".join(shubh_horas_summary) if shubh_horas_summary else "गुरु, शुक्र, बुध, चन्द्र होरा"

        _pch_box_bg = "#f1f5f9" if _is_light else "rgba(15, 23, 42, 0.65)"
        _pch_box_border = "1px solid #cbd5e1" if _is_light else "1px solid rgba(255,255,255,0.06)"
        _pch_lbl_col = "#475569" if _is_light else "#94a3b8"
        _pch_val_col = "#0f172a" if _is_light else "#f8fafc"
        _pch_title_col = TH_GOLD
        _pch_divider = "1px solid #cbd5e1" if _is_light else "1px solid rgba(255,255,255,0.08)"

        panchang_card_html = f"""<div class="glass-card" style="margin-top: 15px; margin-bottom: 15px; border-left: 4px solid {TH_GOLD_ACCENT};">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
<div style="font-weight: 800; color: {_pch_title_col}; font-size: 1.15rem;">आज का सम्पूर्ण दैनिक पंचांग एवं विशिष्ट मुहूर्त ({birth.get('city', 'New Delhi')})</div>
<span style="font-size: 0.85rem; color: {TH_MUTED}; background: {TH_BADGE_BG}; border: {TH_BADGE_BORDER}; padding: 3px 8px; border-radius: 6px; font-weight: 700;">{vikram_str}</span>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-top: 14px;">
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">तिथि (Tithi)</div>{tithi_html}</div>
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">वार (Vara)</div><div style="font-size: 0.95rem; font-weight: 700; color: {_pch_val_col}; margin-top: 2px;">{vara_str}</div></div>
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">नक्षत्र (Nakshatra)</div><div style="font-size: 0.90rem; font-weight: 700; color: {_pch_val_col}; margin-top: 2px;">{nak_str}</div></div>
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">योग एवं करण (Yoga & Karana)</div><div style="font-size: 0.88rem; font-weight: 600; color: {_pch_val_col}; margin-top: 2px;"><b>योग:</b> {yoga_str}<br/><b>करण:</b> {karana_str}</div></div>
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">सूर्योदय व सूर्यास्त (Sunrise / Sunset)</div><div style="font-size: 0.92rem; font-weight: 600; color: {TH_GOLD_TITLE}; margin-top: 2px;">{sunrise_str} — {sunset_str}</div></div>
<div style="background: {_pch_box_bg}; padding: 8px 12px; border-radius: 6px; border: {_pch_box_border};"><div style="font-size: 0.78rem; color: {_pch_lbl_col}; text-transform: uppercase; font-weight: 700;">दिशा शूल व परिहार (Travel Rule)</div><div style="font-size: 0.9rem; font-weight: 600; color: #ef4444; margin-top: 2px;">दिशा: <b>{shool_dir}</b> | <span style="color: {TH_MUTED}; font-size: 0.82rem;">{shool_rem}</span></div></div>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; margin-top: 12px; border-top: {_pch_divider}; padding-top: 10px;">
<div><b>अभिजीत मुहूर्त:</b> <span style="color: #2563eb if _is_light else #38bdf8;">{daily_res.get('amrit_vela', '-')}</span></div>
<div><b>ब्रह्म मुहूर्त:</b> <span style="color: #16a34a if _is_light else #4ade80;">{daily_res.get('brahma_muhurta', '-')}</span></div>
<div><b>अमृत काल:</b> <span style="color: #059669 if _is_light else #34d399;">{daily_res.get('amrit_kalam', '-')}</span></div>
<div><b>राहुकाल (सावधानी):</b> <span style="color: #dc2626 if _is_light else #f87171; font-weight: 700;">{daily_res.get('rahu_kalam', '-')}</span></div>
<div><b>यमगण्ड:</b> <span style="color: {TH_GOLD_ACCENT}; font-weight: 700;">{daily_res.get('yamaganda', '-')}</span></div>
<div><b>गुलिक काल:</b> <span style="color: {_pch_val_col}; font-weight: 700;">{daily_res.get('gulika_kalam', '-')}</span></div>
</div>
<div style="margin-top: 10px; border-top: {_pch_divider}; padding-top: 8px; font-size: 0.88rem; color: {TH_MUTED}; font-weight: 600;">
<b>दिन की प्रमुख शुभ होरा (Auspicious Horas):</b> <span style="color: #16a34a if _is_light else #4ade80;">{shubh_horas_summary_str}</span>
</div>
</div>"""
        st.markdown(panchang_card_html, unsafe_allow_html=True)

        # Location-specific Chaughadiya, Horas & Muhurtas (Directly rendered from daily_res)
        with st.expander("जातक के स्थान अनुसार आज का चौघड़िया, 24 होरा चक्र एवं शुभ-अशुभ मुहूर्त", expanded=True):
            col_m1, col_m2 = st.columns([1, 1.4])
            with col_m1:
                amrit_v_exp = daily_res.get('amrit_vela', '-')
                if "कोई नहीं" in amrit_v_exp or "वर्जित" in amrit_v_exp or "Prohibited" in amrit_v_exp or "बुधवार" in amrit_v_exp:
                    abhijit_exp_ui = '<span style="color: #ef4444; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 6px; border-radius: 4px;"> कोई नहीं (बुधवार को अभिजीत मुहूर्त नहीं होता)</span>'
                else:
                    abhijit_exp_ui = f"<span style='color: #38bdf8; font-weight: 700;'>{amrit_v_exp}</span>"

                st.markdown(f"<div><b>स्थान (Location):</b> <code>{birth.get('city', 'New Delhi')}</code></div>", unsafe_allow_html=True)
                st.markdown(f"<div><b>अभिजीत मुहूर्त:</b> {abhijit_exp_ui}</div>", unsafe_allow_html=True)
                st.markdown(f"<div><b>राहु काल:</b> <span style='color: #ef4444; font-weight: 700;'>{daily_res.get('rahu_kalam', '-')}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div><b>यमगण्ड:</b> <span style='color: #f59e0b; font-weight: 700;'>{daily_res.get('yamaganda', '-')}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div><b>गुलिक काल:</b> <span style='color: #e2e8f0; font-weight: 700;'>{daily_res.get('gulika_kalam', '-')}</span></div>", unsafe_allow_html=True)
            with col_m2:
                st.markdown("""
                <div style="font-size: 0.82rem; color: #cbd5e1; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(229, 169, 60, 0.2); border-radius: 8px; padding: 10px;">
                    <b> चौघड़िया नियम:</b> 
                    <span style="color: #10b981; font-weight: 700;">शुभ, लाभ, अमृत, चर = हरा (शुभ/कार्य सिद्धि)</span> | 
                    <span style="color: #ef4444; font-weight: 700;">उद्वेग, काल, रोग = लाल (वर्जित/सावधानी)</span>
                </div>
                """, unsafe_allow_html=True)

            _lz_tab_ch = lazy_sections([
                "जातक-विशिष्ट मुहूर्त (Personal Muhurta)",
                "दिन का चौघड़िया",
                "रात्रि का चौघड़िया",
                "24 कालहोरा चक्र (Horas)",
                "शुभ-अशुभ मुहूर्त (Muhurtas)",
            ], key="tab_ch")
            def _is_time_window_active(s_str, e_str):
                try:
                    t_now = now_dt.time()
                    s_t = datetime.strptime(s_str.strip(), "%I:%M %p").time()
                    e_t = datetime.strptime(e_str.strip(), "%I:%M %p").time()
                    if s_t <= e_t:
                        return s_t <= t_now <= e_t
                    else:
                        return t_now >= s_t or t_now <= e_t
                except Exception:
                    return False

            if _lz_tab_ch[0]:
                asc_idx = getattr(chart, 'ascendant_sign', int(chart.ascendant_longitude // 30.0) % 12)
                l_sign = constants.SIGNS_HI[asc_idx]
                l_lord = constants.SIGN_LORD[asc_idx]
                l_lord_hi = constants.PLANETS_HI.get(l_lord, l_lord)
                
                b_lord = constants.SIGN_LORD[(asc_idx + 8) % 12]
                b_lord_hi = constants.PLANETS_HI.get(b_lord, b_lord)
                
                p_lord = constants.SIGN_LORD[(asc_idx + 4) % 12]
                p_lord_hi = constants.PLANETS_HI.get(p_lord, p_lord)
                
                a_lord = constants.SIGN_LORD[(asc_idx + 7) % 12]
                a_lord_hi = constants.PLANETS_HI.get(a_lord, a_lord)
                
                sh_lord = constants.SIGN_LORD[(asc_idx + 5) % 12]
                sh_lord_hi = constants.PLANETS_HI.get(sh_lord, sh_lord)
                
                natal_m_p = chart.planets.get("Moon")
                natal_m_sign = natal_m_p.sign_index
                natal_m_sign_hi = constants.SIGNS_HI[natal_m_sign]
                
                transit_m_sign = int(transit_moon_lon // 30)
                h_from_m = ((transit_m_sign - natal_m_sign) % 12) + 1
                
                if h_from_m == 8:
                    ch_status_color = "#ef4444"
                    ch_badge = "चन्द्राष्टम दोष (अति सावधान)"
                    ch_desc = "गोचर चन्द्र आपकी जन्म राशि से 8वें भाव में संचरण कर रहे हैं। आज कोई भी नवीन अनुबंध, जोखिमपूर्ण निवेश, बड़ी खरीदारी या लंबी यात्रा टालें।"
                elif h_from_m in [1, 3, 6, 7, 10, 11]:
                    ch_status_color = "#10b981"
                    ch_badge = f"अनुकूल चन्द्रबल ({h_from_m}वाँ भाव)"
                    ch_desc = f"गोचर चन्द्र जन्म राशि से {h_from_m}वें भाव में हैं। कार्य सिद्धि, मानसिक एकाग्रता, वार्ता व प्रतिष्ठा संवर्धन हेतु उत्तम समय।"
                elif h_from_m in [4, 12]:
                    ch_status_color = "#f59e0b"
                    ch_badge = f"मध्यम चन्द्रबल ({h_from_m}वाँ भाव)"
                    ch_desc = f"गोचर चन्द्र {h_from_m}वें भाव में हैं। अनावश्यक व्यय व मानसिक उद्वेग से बचें, शांत रहकर नियमित कार्य निपटाएं।"
                else:
                    ch_status_color = "#38bdf8"
                    ch_badge = f"सामान्य चन्द्रबल ({h_from_m}वाँ भाव)"
                    ch_desc = f"गोचर चन्द्र जन्म राशि से {h_from_m}वें भाव में स्थित हैं।"

                p_overview_html = f"""<div class="glass-card" style="border-left: 4px solid #f59e0b; margin-bottom: 14px;">
<div style="font-weight: 800; font-size: 1.05rem; color: #fbbf24; margin-bottom: 6px;">जातक कुण्डली खगोलीय सामंजस्य (Native Muhurta Alignment) — {birth.get('name', 'जातक')}</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; font-size: 0.88rem; color: #cbd5e1;">
<div><b>लग्न:</b> {l_sign} (लग्नेश: <b style="color: #38bdf8;">{l_lord_hi}</b>)</div>
<div><b>जन्म राशि:</b> {natal_m_sign_hi} (राशि स्वामी: <b style="color: #38bdf8;">{constants.PLANETS_HI.get(constants.SIGN_LORD[natal_m_sign], '')}</b>)</div>
<div><b>भाग्येश:</b> <b style="color: #facc15;">{b_lord_hi}</b> | <b>पंचमेश:</b> <b style="color: #4ade80;">{p_lord_hi}</b></div>
<div><b>अष्टमेश (सावधानी):</b> <b style="color: #f87171;">{a_lord_hi}</b></div>
</div>
<div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 0.88rem;">
<span style="color: #fbbf24; font-weight: 700;">दैनिक ताराबल:</span> {daily_res['tara_name']} ({daily_res['tara_desc']})<br/>
<span style="color: {ch_status_color}; font-weight: 700;">दैनिक चन्द्रबल:</span> <span style="background: {ch_status_color}22; color: {ch_status_color}; border: 1px solid {ch_status_color}44; padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 0.78rem;">{ch_badge}</span> — <span style="color: #cbd5e1;">{ch_desc}</span>
</div>
</div>"""
                st.markdown(p_overview_html, unsafe_allow_html=True)

                col_pj1, col_pj2 = st.columns(2)
                with col_pj1:
                    st.markdown("##### जातक के लिए आज के सर्वश्रेष्ठ शुभ मुहूर्त (Peak Lucky Windows)")
                    p_shubh_items = []
                    am_v = daily_res.get('amrit_vela', '-')
                    if not ("कोई नहीं" in am_v or "वर्जित" in am_v or "Prohibited" in am_v or "बुधवार" in am_v):
                        p_shubh_items.append({
                            "title": "अभिजीत मुहूर्त (Universal Victory Window)",
                            "time": am_v,
                            "desc": "दिन का मध्याह्न काल — किसी भी नवीन कार्य, खरीद व महत्वपूर्ण निर्णय हेतु अचूक सिद्धि योग।"
                        })
                    ak_v = daily_res.get('amrit_kalam', '-')
                    if ak_v and ak_v != '-':
                        p_shubh_items.append({
                            "title": "अमृत कालम् (Amrit Kalam)",
                            "time": ak_v,
                            "desc": "चिरस्थायी मांगलिक व आर्थिक अनुबंधों हेतु अत्यंत शुभ समय।"
                        })
                    
                    b_planets = {l_lord: f"लग्नेश {l_lord_hi} की सिद्धि होरा", b_lord: f"भाग्येश {b_lord_hi} की महा-शुभ होरा", p_lord: f"पंचमेश {p_lord_hi} की होरा"}
                    for h in daily_res.get('horas_day', []):
                        if h['lord'] in b_planets:
                            p_shubh_items.append({
                                "title": f"#{h['num']} {b_planets[h['lord']]}",
                                "time": f"{h['start']} - {h['end']}",
                                "desc": f"{h['nature']} | जातक की कुण्डली अनुसार आत्मबल, आर्थिक लाभ व नए शुभारंभ हेतु सर्वश्रेष्ठ।"
                            })
                    
                    sh_cards = []
                    for item in p_shubh_items:
                        act = False
                        if " - " in item["time"]:
                            parts = item["time"].split(" - ")
                            if len(parts) == 2:
                                act = _is_time_window_active(parts[0], parts[1])
                        act_border = "border: 2px solid #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);" if act else "border: 1px solid rgba(16, 185, 129, 0.25);"
                        act_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 6px;">● सक्रिय</span>' if act else ''
                        sh_cards.append(f"""<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; {act_border}">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px;">
<div style="font-weight: 800; font-size: 0.95rem; color: #4ade80;">{item['title']}{act_pill}</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #38bdf8; background: rgba(15,23,42,0.85); padding: 2px 8px; border-radius: 4px;">{item['time']}</span>
</div>
<div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 4px;">{item['desc']}</div>
</div>""")
                    st.markdown("".join(sh_cards) if sh_cards else "<p style='color: #94a3b8;'>आज का दिन सामान्य है।</p>", unsafe_allow_html=True)

                with col_pj2:
                    st.markdown("##### जातक के लिए आज के टालने योग्य काल (Windows to Avoid)")
                    p_avoid_items = []
                    p_avoid_items.append({
                        "title": "राहु काल (Rahu Kaal)",
                        "time": daily_res.get('rahu_kalam', '-'),
                        "desc": "महत्वपूर्ण अनुबंध, नवीन वाहन क्रय, बड़ी खरीदारी व यात्रा सर्वथा टालें।"
                    })
                    p_avoid_items.append({
                        "title": "यमगण्ड काल (Yamaganda)",
                        "time": daily_res.get('yamaganda', '-'),
                        "desc": "अप्रिय परिणाम की आशंका, जोखिमपूर्ण निर्णय न लें।"
                    })
                    m_planets = {a_lord: f"अष्टमेश {a_lord_hi} की होरा", sh_lord: f"षष्ठेश {sh_lord_hi} की होरा"}
                    for h in daily_res.get('horas_day', []):
                        if h['lord'] in m_planets and h['lord'] != l_lord and h['lord'] != b_lord:
                            p_avoid_items.append({
                                "title": f"#{h['num']} {m_planets[h['lord']]} (सावधानी)",
                                "time": f"{h['start']} - {h['end']}",
                                "desc": f"{h['nature']} | इस समय विवाद, बहस, कानूनी वार्ता या जोखिमपूर्ण लेन-देन टालें।"
                            })
                    
                    av_cards = []
                    for item in p_avoid_items:
                        act = False
                        if " - " in item["time"]:
                            parts = item["time"].split(" - ")
                            if len(parts) == 2:
                                act = _is_time_window_active(parts[0], parts[1])
                        act_border = "border: 2px solid #ef4444; box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);" if act else "border: 1px solid rgba(239, 68, 68, 0.25);"
                        act_pill = '<span style="background: #ef4444; color: #ffffff; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 6px;">चालू (सावधान)</span>' if act else ''
                        av_cards.append(f"""<div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; {act_border}">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px;">
<div style="font-weight: 800; font-size: 0.95rem; color: #f87171;">{item['title']}{act_pill}</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #fca5a5; background: rgba(15,23,42,0.85); padding: 2px 8px; border-radius: 4px;">{item['time']}</span>
</div>
<div style="font-size: 0.78rem; color: #fecaca; margin-top: 4px;">{item['desc']}</div>
</div>""")
                    st.markdown("".join(av_cards), unsafe_allow_html=True)

            if _lz_tab_ch[1]:
                day_chs = daily_res.get('chaughadiya_day', [])
                if day_chs:
                    ch_cards = []
                    for c in day_chs:
                        act = _is_time_window_active(c.get('start', ''), c.get('end', ''))
                        color = c.get('color', '#10b981')
                        is_good = c.get('is_good', True)
                        badge_bg = "rgba(16, 185, 129, 0.2)" if is_good else "rgba(239, 68, 68, 0.2)"
                        badge_color = "#4ade80" if is_good else "#f87171"
                        badge_label = "शुभ" if is_good else "अशुभ"
                        active_style = "border: 2px solid #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);" if act else "border-top: 1px solid rgba(255,255,255,0.06); border-right: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06);"
                        active_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 4px;">● सक्रिय</span>' if act else ''
                        ch_cards.append(f"""<div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid {color}; border-radius: 8px; padding: 8px 10px; {active_style}">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 800; font-size: 0.95rem; color: {color};">{c.get('name_hi')} ({c.get('name')}){active_pill}</div>
<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_color}44; padding: 1px 5px; border-radius: 4px; font-weight: 700; font-size: 0.70rem;">{badge_label}</span>
</div>
<div style="font-size: 0.75rem; color: #94a3b8; margin: 2px 0;">{c.get('nature')}</div>
<div style="font-size: 0.78rem; font-weight: 600; color: #f8fafc;">{c.get('start')} - {c.get('end')}</div>
</div>""")
                    st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-top: 8px;">' + "".join(ch_cards) + '</div>', unsafe_allow_html=True)

            if _lz_tab_ch[2]:
                night_chs = daily_res.get('chaughadiya_night', [])
                if night_chs:
                    ch_cards = []
                    for c in night_chs:
                        act = _is_time_window_active(c.get('start', ''), c.get('end', ''))
                        color = c.get('color', '#10b981')
                        is_good = c.get('is_good', True)
                        badge_bg = "rgba(16, 185, 129, 0.2)" if is_good else "rgba(239, 68, 68, 0.2)"
                        badge_color = "#4ade80" if is_good else "#f87171"
                        badge_label = "शुभ" if is_good else "अशुभ"
                        active_style = "border: 2px solid #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);" if act else "border-top: 1px solid rgba(255,255,255,0.06); border-right: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06);"
                        active_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 4px;">● सक्रिय</span>' if act else ''
                        ch_cards.append(f"""<div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid {color}; border-radius: 8px; padding: 8px 10px; {active_style}">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 800; font-size: 0.95rem; color: {color};">{c.get('name_hi')} ({c.get('name')}){active_pill}</div>
<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_color}44; padding: 1px 5px; border-radius: 4px; font-weight: 700; font-size: 0.70rem;">{badge_label}</span>
</div>
<div style="font-size: 0.75rem; color: #94a3b8; margin: 2px 0;">{c.get('nature')}</div>
<div style="font-size: 0.78rem; font-weight: 600; color: #f8fafc;">{c.get('start')} - {c.get('end')}</div>
</div>""")
                    st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-top: 8px;">' + "".join(ch_cards) + '</div>', unsafe_allow_html=True)

            if _lz_tab_ch[3]:
                h_day = daily_res.get('horas_day', [])
                h_night = daily_res.get('horas_night', [])

                def _render_hora_grid(horas_list):
                    cards = []
                    for h in horas_list:
                        act = _is_time_window_active(h.get('start', ''), h.get('end', ''))
                        color = h.get('color', '#10b981')
                        if color == '#10b981':
                            badge_bg = "rgba(16, 185, 129, 0.2)"
                            badge_color = "#4ade80"
                            badge_label = "शुभ"
                        elif color == '#ef4444':
                            badge_bg = "rgba(239, 68, 68, 0.2)"
                            badge_color = "#f87171"
                            badge_label = "अशुभ / क्रूर"
                        else:
                            badge_bg = "rgba(245, 158, 11, 0.2)"
                            badge_color = "#fbbf24"
                            badge_label = "मध्यम"
                        
                        active_style = "border: 2px solid #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);" if act else "border-top: 1px solid rgba(255,255,255,0.06); border-right: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06);"
                        active_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 4px;">● सक्रिय</span>' if act else ''
                        cards.append(f"""<div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid {color}; border-radius: 8px; padding: 8px 10px; {active_style}">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 800; font-size: 0.90rem; color: {color};">#{h['num']} {h['lord_hi']} ({h['lord']}){active_pill}</div>
<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_color}44; padding: 1px 5px; border-radius: 4px; font-weight: 700; font-size: 0.70rem;">{badge_label}</span>
</div>
<div style="font-size: 0.74rem; color: #94a3b8; margin: 2px 0;">{h['nature']}</div>
<div style="font-size: 0.78rem; font-weight: 600; color: #f8fafc;">{h['start']} - {h['end']}</div>
</div>""")
                    return '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 8px; margin-top: 8px;">' + "".join(cards) + '</div>'

                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.markdown("<b>दिन की 12 होरा (Day Horas):</b>", unsafe_allow_html=True)
                    if h_day:
                        st.markdown(_render_hora_grid(h_day), unsafe_allow_html=True)
                with col_h2:
                    st.markdown("<b>रात्रि की 12 होरा (Night Horas):</b>", unsafe_allow_html=True)
                    if h_night:
                        st.markdown(_render_hora_grid(h_night), unsafe_allow_html=True)

            if _lz_tab_ch[4]:
                col_m_shubh, col_m_ashubh = st.columns(2)
                with col_m_shubh:
                    st.markdown("#####  शास्त्रोक्त शुभ मुहूर्त (Auspicious Timings)")
                    m_shubh_data = [
                        {"name": "ब्रह्म मुहूर्त (Brahma Muhurta)", "time": daily_res.get("brahma_muhurta", "-"), "desc": "ध्यान, योग, अध्ययन एवं ईश-स्मरण हेतु सर्वश्रेष्ठ"},
                        {"name": "प्रातः संध्या (Pratah Sandhya)", "time": daily_res.get("pratah_sandhya", "-"), "desc": "गायत्री जप एवं सूर्योपासना का मुख्य काल"},
                        {"name": "अभिजीत मुहूर्त (Abhijit)", "time": daily_res.get("amrit_vela", "-"), "desc": "सर्वकार्य सिद्धिदायक (बुधवार को शास्त्रानुसार वर्जित)"},
                        {"name": "विजय मुहूर्त (Vijaya)", "time": daily_res.get("vijaya_muhurta", "-"), "desc": "मुकदमे, प्रतिस्पर्धा व यात्रा में विजय कारक"},
                        {"name": "गोधूलि मुहूर्त (Godhuli)", "time": daily_res.get("godhuli_muhurta", "-"), "desc": "गृह प्रवेश व मांगलिक वार्तालाप हेतु शुभ"},
                        {"name": "अमृत कालम् (Amrit Kalam)", "time": daily_res.get("amrit_kalam", "-"), "desc": "विशेष अनुबंध, क्रय-विक्रय व नवीन कार्य"},
                        {"name": "निशिता मुहूर्त (Nishita)", "time": daily_res.get("nishita_muhurta", "-"), "desc": "मध्यरात्रि शिव-पूजा एवं तांत्रिक साधना"}
                    ]
                    shubh_cards = []
                    for m in m_shubh_data:
                        t_span = m["time"]
                        act = False
                        if " - " in t_span and not ("कोई नहीं" in t_span or "वर्जित" in t_span):
                            parts = t_span.split(" - ")
                            if len(parts) == 2:
                                act = _is_time_window_active(parts[0], parts[1])
                        active_style = "border: 2px solid #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.35);" if act else "border: 1px solid rgba(16, 185, 129, 0.25);"
                        active_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 6px;">● सक्रिय</span>' if act else ''
                        shubh_cards.append(f"""<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; {active_style}">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px;">
<div style="font-weight: 800; font-size: 0.95rem; color: #4ade80;">{m['name']}{active_pill}</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #38bdf8; background: rgba(15,23,42,0.85); padding: 2px 8px; border-radius: 4px;">{m['time']}</span>
</div>
<div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 4px;">{m['desc']}</div>
</div>""")
                    st.markdown("".join(shubh_cards), unsafe_allow_html=True)

                with col_m_ashubh:
                    st.markdown("#####  शास्त्रोक्त अशुभ/वर्जित काल (Inauspicious Windows)")
                    m_ashubh_data = [
                        {"name": "राहु काल (Rahu Kaal)", "time": daily_res.get("rahu_kalam", "-"), "rule": "नया व्यापार, क्रय एवं यात्रा सर्वथा वर्जित"},
                        {"name": "यमगण्ड (Yamaganda)", "time": daily_res.get("yamaganda", "-"), "rule": "अप्रिय परिणाम सूचक, महत्वपूर्ण निर्णय टालें"},
                        {"name": "गुलिक काल (Gulika Kalam)", "time": daily_res.get("gulika_kalam", "-"), "rule": "शनि-पुत्र गुलिक का समय, बाधा कारक"}
                    ]
                    ashubh_cards = []
                    for m in m_ashubh_data:
                        t_span = m["time"]
                        act = False
                        if " - " in t_span and not ("कोई नहीं" in t_span or "वर्जित" in t_span):
                            parts = t_span.split(" - ")
                            if len(parts) == 2:
                                act = _is_time_window_active(parts[0], parts[1])
                        active_style = "border: 2px solid #ef4444; box-shadow: 0 0 10px rgba(239,68,68,0.35);" if act else "border: 1px solid rgba(239, 68, 68, 0.25);"
                        active_pill = '<span style="background: #ef4444; color: #ffffff; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 6px;">चालू (सावधान)</span>' if act else ''
                        ashubh_cards.append(f"""<div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; {active_style}">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 4px;">
<div style="font-weight: 800; font-size: 0.95rem; color: #f87171;">{m['name']}{active_pill}</div>
<span style="font-size: 0.88rem; font-weight: 700; color: #fca5a5; background: rgba(15,23,42,0.85); padding: 2px 8px; border-radius: 4px;">{m['time']}</span>
</div>
<div style="font-size: 0.78rem; color: #fecaca; margin-top: 4px;"><b>नियम:</b> {m['rule']}</div>
</div>""")
                    st.markdown("".join(ashubh_cards), unsafe_allow_html=True)

                st.markdown("<div style='margin-top: 14px; font-weight: 800; font-size: 1.05rem; color: #fbbf24;'>दिन की सर्वमान्य शुभ कालहोरा (Universal Auspicious Planetary Horas)</div>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 0.85rem; color: #94a3b8; margin-top: 2px;'>शास्त्रानुसार गुरु, शुक्र, बुध एवं चन्द्रमा की होरा में किए गए कार्य सर्वकार्य सिद्धिदायक व सफल होते हैं:</p>", unsafe_allow_html=True)
                sh_uni_cards = []
                for h in daily_res.get('horas_day', []):
                    if h.get('color') == '#10b981':
                        act = _is_time_window_active(h['start'], h['end'])
                        act_border = "border: 2px solid #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.35);" if act else "border: 1px solid rgba(16, 185, 129, 0.25);"
                        act_pill = '<span style="background: #38bdf8; color: #020617; font-weight: 800; font-size: 0.68rem; padding: 1px 6px; border-radius: 10px; margin-left: 6px;">● चालू</span>' if act else ''
                        sh_uni_cards.append(f"""<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 8px; padding: 8px 12px; {act_border}">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 800; font-size: 0.95rem; color: #4ade80;">#{h['num']} {h['lord_hi']} ({h['lord']}){act_pill}</div>
<span style="font-size: 0.85rem; font-weight: 700; color: #38bdf8; background: rgba(15,23,42,0.85); padding: 2px 8px; border-radius: 4px;">{h['start']} - {h['end']}</span>
</div>
<div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 4px;">{h['nature']}</div>
</div>""")
                if sh_uni_cards:
                    st.markdown("<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin-top: 8px;'>" + "".join(sh_uni_cards) + "</div>", unsafe_allow_html=True)

        # In-depth Comprehensive Daily Forecast (4 Life Pillars & Gochar Synthesis)
        narrs = daily_res.get("narratives", {})
        if narrs:
            st.markdown(f'<div class="section-title">{"आज का विस्तृत 4-स्तंभ फलादेश एवं गोचर मीमांसा" if is_hi else "Comprehensive 4-Pillar Daily Forecast"}</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f0c05a; margin-bottom: 16px;">
                <div style="font-size: 1.1rem; font-weight: 800; color: #f0c05a; margin-bottom: 6px;">
                    {narrs.get('chandra_gochar_title', 'दैनिक गोचर सारांश')} (जन्म राशि से {narrs.get('chandra_gochar_house')}वाँ भाव)
                </div>
                <p style="font-size: 0.95rem; color: #f8fafc; line-height: 1.7; margin: 0;">
                    {narrs.get('synthesis', '')}
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_narr1, col_narr2 = st.columns(2)
            with col_narr1:
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom: 12px; border-left: 4px solid #3b82f6;">
                    <div style="font-weight: 700; color: #60a5fa; font-size: 1rem; margin-bottom: 4px;"> आजीविका एवं कार्यक्षेत्र (Career & Profession) • {daily_res['scores']['career']}%</div>
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">{narrs.get('career', '')}</div>
                </div>
                <div class="glass-card" style="margin-bottom: 12px; border-left: 4px solid #10b981;">
                    <div style="font-weight: 700; color: #34d399; font-size: 1rem; margin-bottom: 4px;"> धन, व्यापार एवं निवेश (Wealth & Finance) • {daily_res['scores']['wealth']}%</div>
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">{narrs.get('wealth', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_narr2:
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom: 12px; border-left: 4px solid #ec4899;">
                    <div style="font-weight: 700; color: #f472b6; font-size: 1rem; margin-bottom: 4px;">संबंध, प्रेम व दांपत्य (Relationships & Family) • {daily_res['scores']['love']}%</div>
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">{narrs.get('love', '')}</div>
                </div>
                <div class="glass-card" style="margin-bottom: 12px; border-left: 4px solid #f59e0b;">
                    <div style="font-weight: 700; color: #fbbf24; font-size: 1rem; margin-bottom: 4px;"> स्वास्थ्य, ऊर्जा व मनोबल (Health & Vitality) • {daily_res['scores']['health']}%</div>
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">{narrs.get('health', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10b981; border-radius: 10px; padding: 12px 16px; margin-top: 8px;">
                <div style="color: #34d399; font-weight: 700; font-size: 0.92rem;">आज का अचूक सात्विक उपाय (Target Daily Remedy):</div>
                <div style="color: #f0fdf4; font-size: 0.9rem; margin-top: 4px;">{daily_res['remedy']}</div>
            </div>
            """, unsafe_allow_html=True)

    # (Chatbot is now integrated as a Floating Popup Dialog with Acharya Vyas)

    # =========================================================================
    # SUITE: LAL KITAB SYSTEM & REMEDIES
    # =========================================================================
    if "लाल किताब" in selected_suite or "Lal Kitab" in selected_suite:
        st.markdown(f'<div class="section-title">{"लाल किताब संपूर्ण विश्लेषण एवं अचूक घरेलू उपाय (पं. रूपचंद जोशी व जी.डी. वशिष्ठ)" if is_hi else "Lal Kitab System & Authentic Remedies"}</div>', unsafe_allow_html=True)
        
        planets_dict = {n: {"sign_index": p.sign_index, "longitude": p.longitude} for n, p in chart.planets.items()}
        lk_res = vyas_lalkitab.analyze_lalkitab(planets_dict, asc_sign_idx)

        # Badges for Dharmi and Andhi Kundli
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown(f"""
            <div class="glass-card" style="padding: 14px 18px; border-left: 4px solid #f0c05a;">
                <div style="font-weight: 700; color: #f0c05a;">तेवा प्रकृति (Tewa Type):</div>
                <div style="color: #fef0cd; font-size: 0.95rem;">{lk_res['summary']['dharmi_status']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_l2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 14px 18px; border-left: 4px solid #e63946;">
                <div style="font-weight: 700; color: #e63946;">दृष्टि स्थिति (Sight Status):</div>
                <div style="color: #fef0cd; font-size: 0.95rem;">{lk_res['summary']['andhi_status']}</div>
            </div>
            """, unsafe_allow_html=True)

        if lk_res['sleeping_houses']:
            st.info(f" **सोए हुए घर (Sleeping Houses):** भाव {', '.join(str(h) for h in lk_res['sleeping_houses'])} — इन भावों के फलों को जाग्रत करने हेतु संबंधित उपायों की आवश्यकता है।")
        if lk_res['sleeping_planets']:
            st.warning(f" **सोए हुए ग्रह (Sleeping Planets):** {', '.join(lk_res['sleeping_planets'])} — यह ग्रह अपनी पूर्ण क्षमता से फल देने में असमर्थ हैं।")

        st.markdown("#### 9 ग्रहों की भाव स्थिति एवं अचूक लाल किताब उपाय")
        st.dataframe(pd.DataFrame(lk_res["planet_details"]), use_container_width=True, hide_index=True)

        lk_script_res = vyas_knowledge_engine.synthesize_lal_kitab_scripts(chart, lk_res)
        st.markdown(lk_script_res["lal_kitab_script"], unsafe_allow_html=True)

    # =========================================================================
    # SUITE: BIRTH TIME RECTIFICATION (BTR)
    # =========================================================================
    if ("जन्म समय शुद्धि" in selected_suite or "BTR" in selected_suite
            or "Rectification" in selected_suite):
        st.markdown(f'<div class="section-title">{"जन्म समय शुद्धि (Birth Time Rectification - कुन्द व तत्व शोधन)" if is_hi else "Birth Time Rectification (BTR Engine)"}</div>', unsafe_allow_html=True)
        st.info("ऋषि पराशर एवं आधुनिक KP अनुसंधान के अनुसार जन्म समय में 1-2 मिनट का भी अंतर लग्न कस्प, D60 और सब-लॉर्ड्स को बदल देता है। नीचे दिए गए शास्त्रीय परीक्षणों से अपने समय की प्रामाणिकता जांचें:")

        k_ok, k_nak, k_msg = vyas_btr.kunda_shodhana(chart.ascendant_longitude, chart.planets["Moon"].longitude)
        t_ok, t_name, t_msg = vyas_btr.tattva_shodhana(birth['local'], gender="Male")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {'#2a9d8f' if k_ok else '#e63946'};">
                <div style="font-weight: 700; color: #f0c05a;">1. कुन्द शुद्धि (Kunda Shodhana - 81x गुणनफल)</div>
                <div style="color: #eedc9a; margin-top: 4px;">कुन्द नक्षत्र: <b>{k_nak}</b></div>
                <div style="color: #fdf5e6; font-size: 0.9rem; margin-top: 4px;">{k_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b2:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {'#2a9d8f' if t_ok else '#e63946'};">
                <div style="font-weight: 700; color: #f0c05a;">2. तत्व शुद्धि (Tattva Shodhana - पंचतत्व लिंग परीक्षण)</div>
                <div style="color: #eedc9a; margin-top: 4px;">सक्रिय तत्व: <b>{t_name}</b></div>
                <div style="color: #fdf5e6; font-size: 0.9rem; margin-top: 4px;">{t_msg}</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("जन्म समय शुद्धि (BTR) पद्धति कैसे कार्य करती है? (Methodology Guide)", expanded=False):
            st.markdown("""
            <div style="font-size: 0.95rem; line-height: 1.7; color: var(--text-main);">
                <b>वैदिक महर्षियों एवं आधुनिक के.पी. शोधकर्ताओं द्वारा प्रतिपादित 4 प्रमुख शोधन स्तंभ:</b><br/>
                <ol style="margin-top: 6px; padding-left: 20px;">
                    <li><b>पाराशरी कुन्द शुद्धि (Kunda Shodhana - BPHS):</b>
                        लग्न के स्पष्ट अंशों को 81 से गुणा करके 27 नक्षत्रों से भाग दिया जाता है। प्राप्त 'कुन्द नक्षत्र' जातक के जन्म चन्द्र नक्षत्र से त्रिकोण (1, 10, या 19वें नक्षत्र) में होना अनिवार्य है। यदि समय में 15 सेकंड का भी अंतर हो तो कुन्द नक्षत्र बदल जाता है।
                    </li>
                    <li><b>पंचतत्त्व शोधन (Pancha Tattva Shodhana):</b>
                        सूर्योदय से जन्म समय तक 24-24 मिनट के पंचतत्त्व (अग्नि, पृथ्वी, वायु, जल, आकाश) चक्र संचलित होते हैं। पुरुष जातक के लिए विषम तत्त्व (अग्नि, वायु, आकाश) और स्त्री जातक के लिए सम तत्त्व (पृथ्वी, जल) प्राकृतिक रूप से अनुकूल व फलदायी होते हैं।
                    </li>
                    <li><b>के.पी. कस्पल सब-लॉर्ड संगति (KP Ruling Planets):</b>
                        लग्न का उप-स्वामी (Cuspal Sub-Lord) चन्द्रमा के नक्षत्र स्वामी या दिन के स्वामी से प्रत्यक्ष संबंध रखता है।
                    </li>
                    <li><b>वर्ग कुण्डली संधि परीक्षण (Divisional Cuspal Stability):</b>
                        लग्न किसी राशि के अंतिम (29°) या प्रारंभिक (0°) संधि अंश में न होकर नवांश (D-9) व दशमांश (D-10) में स्थिर होना चाहिए।
                    </li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### ±10 मिनट विंडो ऑटोमैटिक सेकंड्स स्कैनर (Automated Time Rectifier)")
        
        col_scan1, col_scan2 = st.columns([2.5, 1])
        with col_scan1:
            st.caption("यह स्कैनर आपके दर्ज समय के ±10 मिनट में प्रत्येक 20 सेकंड के अंतराल पर कुन्द शोधन, तत्व शुद्धि एवं वर्ग स्थिरता की सूक्ष्म गणना करता है।")
        with col_scan2:
            run_btr = st.button("Run Multi-Factor BTR Scanner", key="run_btr_scan_btn", type="primary", use_container_width=True)

        if run_btr:
            with st.spinner("Scanning micro-time variations across Kunda & Tattva matrices..."):
                candidates = vyas_btr.scan_rectification_window(
                    birth['local'], birth['lat'], birth['lon'], birth['tz'],
                    chart.planets['Moon'].longitude, gender="Male", window_minutes=10
                )
                st.session_state['btr_candidates'] = candidates

        btr_candidates = st.session_state.get('btr_candidates', [])
        if btr_candidates:
            top_c = btr_candidates[0]
            
            # 1. TOP RECOMMENDED CANDIDATE CARD
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(240, 192, 90, 0.18) 0%, rgba(14, 23, 42, 0.98) 100%);
                        border: 2px solid #f0c05a; border-radius: 14px; padding: 18px 20px; margin: 16px 0; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div style="font-size: 0.85rem; color: #ffd700; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;">
                        [प्रमाणित] सर्वाधिक अनुशंसित एवं गणितीय रूप से प्रमाणित शुद्ध जन्म समय
                    </div>
                    <div style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 800; font-size: 0.82rem;">
                        {top_c['confidence_pct']}% शुद्धता स्कोर
                    </div>
                </div>
                <div style="display: flex; align-items: baseline; gap: 14px; margin-top: 8px;">
                    <div style="font-family: var(--font-yatra); font-size: 2.2rem; color: #ffffff; font-weight: 800; letter-spacing: 1px;">
                        {top_c['time_str']}
                    </div>
                    <div style="font-size: 1.05rem; color: #f7d584; font-weight: 600;">
                        ({top_c['offset_desc']})
                    </div>
                </div>
                <hr style="border-color: rgba(240, 192, 90, 0.3); margin: 12px 0;"/>
                <div style="font-size: 0.92rem; color: #f1f5f9; line-height: 1.7;">
                    <div style="margin-bottom: 8px;">
                        <b style="color: #f0c05a;">• पाराशरी कुन्द शोधन (81x):</b> {top_c['reason_kunda']}
                    </div>
                    <div style="margin-bottom: 8px;">
                        <b style="color: #f0c05a;">• पंचतत्त्व लिंग शुद्धि:</b> {top_c['reason_tattva']}
                    </div>
                    <div style="margin-bottom: 4px;">
                        <b style="color: #f0c05a;">• सूक्ष्म वर्ग स्थिरता:</b> {top_c['reason_varga']}
                    </div>
                    <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 8px; background: rgba(0,0,0,0.35); padding: 6px 12px; border-radius: 8px;">
                        <b>लग्न स्पष्ट:</b> {top_c['asc_deg']} &nbsp;|&nbsp; <b>कुन्द नक्षत्र:</b> {top_c['kunda_nak']} &nbsp;|&nbsp; <b>नवमांश लग्न:</b> {top_c['navamsha_lagna']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_apply1, col_apply2 = st.columns([1.5, 1])
            with col_apply1:
                if st.button(f"इस शुद्ध समय ({top_c['time_str']}) को अपनी कुण्डली में लागू करें", key="apply_btr_top_btn", type="primary", use_container_width=True):
                    cur_p = st.session_state.get('loaded_profile', dict(birth))
                    cur_p['tob'] = top_c['time_str']
                    if is_logged_in_now:
                        auth_vault.save_kundli(u["id"], cur_p)
                    _load_kundli_into_session(cur_p, user_id=u["id"] if is_logged_in_now else None)
                    st.success(f"जन्म समय को शुद्ध कर '{top_c['time_str']}' पर सेट कर दिया गया! सम्पूर्ण कुण्डली नए समय से अपडेट हो गई है।")
                    st.rerun()

            # 2. ALTERNATIVE CANDIDATES (If hospital birth time had a 3-5 min variation)
            other_candidates = btr_candidates[1:]
            if other_candidates:
                with st.expander(f"वैकल्पिक शुद्ध समय विकल्प ({len(other_candidates)} अन्य संभावित समय)", expanded=False):
                    st.caption("यदि आपको संदेह है कि घड़ी या अस्पताल रिकॉर्ड 3 से 5 मिनट आगे-पीछे दर्ज हुआ था, तो नीचे दिए गए वैकल्पिक समय भी कुन्द व तत्व दोनों की कसौटी पर शत-प्रतिशत शुद्ध हैं:")
                    for idx, alt_c in enumerate(other_candidates):
                        st.markdown(f"""
                        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(240,192,90,0.3); border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="font-weight: 800; color: #f0c05a; font-size: 1.1rem;">विकल्प {idx+2}: {alt_c['time_str']} ({alt_c['offset_desc']})</div>
                                <div style="color: #34d399; font-weight: 700; font-size: 0.85rem;">स्कोर: {alt_c['score']}%</div>
                            </div>
                            <div style="font-size: 0.86rem; color: #cbd5e1; margin-top: 6px; line-height: 1.6;">
                                {alt_c['full_reasoning']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"यह वैकल्पिक समय ({alt_c['time_str']}) लागू करें", key=f"apply_alt_btr_{idx}"):
                            cur_p = st.session_state.get('loaded_profile', dict(birth))
                            cur_p['tob'] = alt_c['time_str']
                            if is_logged_in_now:
                                auth_vault.save_kundli(u["id"], cur_p)
                            _load_kundli_into_session(cur_p, user_id=u["id"] if is_logged_in_now else None)
                            st.success(f"जन्म समय को शुद्ध कर '{alt_c['time_str']}' पर सेट कर दिया गया!")
                            st.rerun()

        # -------------------------------------------------------------
        # LIFE EVENTS CORRELATION & VERIFICATION (जीवन की प्रमुख घटनाओं से समय शुद्धि)
        # -------------------------------------------------------------
        st.markdown("---")
        st.markdown("#### जीवन की वास्तविक घटनाओं द्वारा जन्म समय सत्यापन (Life Events Cross-Verification)")
        st.markdown("""
        <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 12px;">
            <b>वैदिक एवं केपी शोधन सिद्धांत:</b> यदि जन्म समय 1-2 मिनट भी आगे-पीछे हो, तो विंशोत्तरी दशा व वर्ग कुंडलियों (D9, D10, D7) 
            का सटीक फलित जीवन की वास्तविक घटनाओं (विवाह, नौकरी, संतान, दुर्घटना) से मेल नहीं खाता। 
            नीचे अपने जीवन की 1 या अधिक प्रमुख घटनाएं दर्ज करें और कुंडली के दशा चक्र से मिलान जांचें:
        </div>
        """, unsafe_allow_html=True)

        col_ev1, col_ev2 = st.columns([1.5, 1])
        with col_ev1:
            ev_type_input = st.selectbox("घटना का प्रकार (Event Type)", [
                "विवाह (Marriage)",
                "करियर / नौकरी (Job / Promotion)",
                "संतान जन्म (Childbirth)",
                "वाहन / गृह क्रय (Property / Vehicle)",
                "विदेश गमन (Foreign Travel / Relocation)",
                "स्वास्थ्य कष्ट / दुर्घटना (Surgery / Health Event)"
            ])
        with col_ev2:
            ev_date_input = st.date_input("घटना दिनांक (Event Date)", value=datetime(2020, 1, 1).date(),
                                         min_value=datetime(1950, 1, 1).date(), max_value=datetime.now().date())

        if st.button("घटना मिलान सत्यापित करें (Verify Event) (दशा व वर्ग कुण्डली से घटना का मिलान करें)", use_container_width=True):
            test_events = [{"type": ev_type_input, "date": ev_date_input.strftime("%Y-%m-%d")}]
            ev_res = vyas_btr.verify_life_events(
                birth['local'], chart.planets['Moon'].longitude, chart.ascendant_longitude, test_events
            )
            if ev_res:
                st.markdown("#####  घटना एवं दशा समन्वय परिणाम (Event Alignment Report)")
                for r in ev_res:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid #2a9d8f; padding: 14px 18px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #f0c05a; font-size: 1rem;">{r['event_type']} ({r['event_date']})</span>
                            <span style="background: rgba(42, 157, 143, 0.25); border: 1px solid #2a9d8f; color: #a7f3d0; padding: 3px 10px; border-radius: 12px; font-weight: 700; font-size: 0.82rem;">सटीकता: {r['alignment_score']}</span>
                        </div>
                        <div style="font-size: 0.88rem; color: #e2e8f0; margin-top: 6px;"><b>सक्रिय विंशोत्तरी दशा:</b> {r['running_dasha']} &nbsp;|&nbsp; <b>संबंधित वर्ग चक्र:</b> {r['relevant_varga']}</div>
                        <div style="font-size: 0.85rem; color: #eedc9a; margin-top: 6px; line-height: 1.4;">{r['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)



    # =========================================================================
    # SUITE 1: CHARTS & 16 VARGAS
    # =========================================================================
    if "कुण्डली" in selected_suite or "Charts" in selected_suite:
        _lz_sub_tab = lazy_sections([
            "लग्न एवं नवमांश (D1 & D9)" if is_hi else "D1 & D9 Charts",
            "षोडशवर्ग 16 चक्र" if is_hi else "16 Divisional Charts",
            "षष्ट्यंश देवता (D60)" if is_hi else "D60 Deities",
            "वर्ग कुण्डली शास्त्रीय सूत्र फलित" if is_hi else "Divisional Vargas Script",
        ], key="sub_tab")

        if _lz_sub_tab[0]:
            st.markdown(f'<div class="section-title">{"वैदिक ग्रह स्थिति एवं जन्म कुण्डली" if is_hi else "Vedic Planetary Positions & Natal Charts"}</div>', unsafe_allow_html=True)
            
            # Overview metric cards (Reference Style)
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 20px;">
                <div class="glass-card" style="text-align: center; padding: 14px 18px;">
                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">{'जातक का नाम' if is_hi else 'NATIVE NAME'}</div>
                    <div style="color: #fef3c7; font-size: 1.15rem; font-weight: 700; font-family: 'Cinzel', serif; margin-top: 4px;">{birth.get('name', 'Nikhil Vyas')}</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 14px 18px;">
                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">{'जन्म लग्न' if is_hi else 'LAGNA (ASCENDANT)'}</div>
                    <div style="color: #e5a93c; font-size: 1.15rem; font-weight: 700; margin-top: 4px;">{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]} ({format_varga_dms(chart.ascendant_longitude)})</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 14px 18px;">
                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">{'चन्द्र राशि एवं नक्षत्र' if is_hi else 'MOON RASHI & NAKSHATRA'}</div>
                    <div style="color: #fef3c7; font-size: 1.05rem; font-weight: 700; margin-top: 4px;">{constants.SIGNS_HI[chart.planets['Moon'].sign_index] if is_hi else chart.planets['Moon'].sign_name} • {constants.NAKSHATRAS_HI[int(chart.planets['Moon'].longitude // constants.NAKSHATRA_SPAN) % 27] if is_hi else constants.NAKSHATRAS[int(chart.planets['Moon'].longitude // constants.NAKSHATRA_SPAN) % 27]}</div>
                </div>
                <div class="glass-card" style="text-align: center; padding: 14px 18px;">
                    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;">{'अयनांश व नोड' if is_hi else 'AYANAMSA & NODE'}</div>
                    <div style="color: #e5a93c; font-size: 1.05rem; font-weight: 700; margin-top: 4px;">{vyas_ephem.AYANAMSA_NAME} ({vyas_ephem.NODE_MODEL.title()})</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            chart_style = st.radio("Kundli Style (कुंडली प्रारूप)", ["North Indian (उत्तर भारतीय हीरा शैली)", "South Indian (दक्षिण भारतीय चौकोर शैली)"], horizontal=True)

            col1, col2 = st.columns([1.35, 1.0])
            with col1:
                title_txt = f"{'लग्न चक्र: ' if is_hi else 'D1 Lagna: '}{constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx]} {format_varga_dms(chart.ascendant_longitude)}"
                if "South" in chart_style:
                    si_data = {r: [] for r in range(12)}
                    for p_name, p in chart.planets.items():
                        abbr = f"{constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]} {int(p.longitude % 30)}°{int((p.longitude % 1)*60):02d}'"
                        if p.is_retrograde:
                            abbr += " (व)" if is_hi else " (R)"
                        si_data[p.sign_index].append(abbr)
                    svg_d1 = get_south_indian_chart_svg(si_data, asc_sign_idx, size=560, chart_title=title_txt)
                else:
                    svg_d1 = get_north_indian_chart_svg(d1_houses, size=560, chart_title=title_txt)
                render_kundli(svg_d1)
                
                with st.expander("विशाल कुण्डली चार्ट (Zoom In / 650px Ultra HD View)", expanded=False):
                    if "South" in chart_style:
                        svg_d1_large = get_south_indian_chart_svg(si_data, asc_sign_idx, size=650, chart_title=title_txt)
                    else:
                        svg_d1_large = get_north_indian_chart_svg(d1_houses, size=650, chart_title=title_txt)
                    render_kundli(svg_d1_large)
                
            with col2:
                st.markdown(f"#### {' ग्रह स्पष्ट एवं अधिपति तालिका' if is_hi else ' Planetary Degrees & Dispositor Matrix'}")
                p_data = []
                asc_nak = int(chart.ascendant_longitude // constants.NAKSHATRA_SPAN) % 27
                asc_pada = int((chart.ascendant_longitude % constants.NAKSHATRA_SPAN) // constants.PADA_SPAN) + 1
                asc_subs = calculate_sub_lords(chart.ascendant_longitude, depth=4)
                
                p_data.append({
                    "ग्रह" if is_hi else "Graha": "लग्न (Ascendant)" if is_hi else "Lagna (Asc)",
                    "राशि" if is_hi else "Rashi": constants.SIGNS_HI[asc_sign_idx] if is_hi else constants.SIGNS[asc_sign_idx],
                    "स्पष्ट अंश" if is_hi else "Degree (DMS)": format_varga_dms(chart.ascendant_longitude),
                    "नक्षत्र" if is_hi else "Nakshatra": constants.NAKSHATRAS_HI[asc_nak] if is_hi else constants.NAKSHATRAS[asc_nak],
                    "पद" if is_hi else "Pada": asc_pada,
                    "राशि स्वामी" if is_hi else "Rashi Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[asc_sign_idx], constants.SIGN_LORD[asc_sign_idx]) if is_hi else constants.SIGN_LORD[asc_sign_idx],
                    "नक्षत्र स्वामी" if is_hi else "Star Lord (NL)": constants.PLANETS_HI.get(asc_subs["NL"], asc_subs["NL"]) if is_hi else asc_subs["NL"],
                    "उप-स्वामी" if is_hi else "Sub Lord (SL)": constants.PLANETS_HI.get(asc_subs["SL"], asc_subs["SL"]) if is_hi else asc_subs["SL"],
                    "गति" if is_hi else "Speed": "-"
                })
                for p_name, p in chart.planets.items():
                    subs = calculate_sub_lords(p.longitude, depth=4)
                    nak_idx = int(p.longitude // constants.NAKSHATRA_SPAN) % 27
                    p_label = constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name
                    if p.is_retrograde:
                        p_label += " (वक्री)" if is_hi else " (R)"
                    p_data.append({
                        "ग्रह" if is_hi else "Graha": p_label,
                        "राशि" if is_hi else "Rashi": constants.SIGNS_HI[p.sign_index] if is_hi else p.sign_name,
                        "स्पष्ट अंश" if is_hi else "Degree (DMS)": format_varga_dms(p.longitude),
                        "नक्षत्र" if is_hi else "Nakshatra": constants.NAKSHATRAS_HI[nak_idx] if is_hi else constants.NAKSHATRAS[nak_idx],
                        "पद" if is_hi else "Pada": p.pada,
                        "राशि स्वामी" if is_hi else "Rashi Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[p.sign_index], constants.SIGN_LORD[p.sign_index]) if is_hi else constants.SIGN_LORD[p.sign_index],
                        "नक्षत्र स्वामी" if is_hi else "Star Lord (NL)": constants.PLANETS_HI.get(subs["NL"], subs["NL"]) if is_hi else subs["NL"],
                        "उप-स्वामी" if is_hi else "Sub Lord (SL)": constants.PLANETS_HI.get(subs["SL"], subs["SL"]) if is_hi else subs["SL"],
                        "गति" if is_hi else "Speed": f"{p.speed:.3f}°/d"
                    })
                st.dataframe(pd.DataFrame(p_data), use_container_width=True, hide_index=True)

        if _lz_sub_tab[1]:
            st.markdown(f'<div class="section-title">{"षोडशवर्ग 16 कुण्डलियाँ (Shodashvarga 16 Divisional Charts)" if is_hi else "Shodashvarga 16 Divisional Charts"}</div>', unsafe_allow_html=True)
            varga_list = ["D9", "D10", "D60", "D2", "D3", "D4", "D7", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45"]
            varga_sel = st.selectbox("जाँच हेतु वर्ग कुण्डली का चयन करें (Select Divisional Chart):", varga_list, index=0)
            
            asc_v_pos = vargas_matrix[varga_sel]["Ascendant"]
            v_houses = {h: [] for h in range(1, 13)}
            for h in range(1, 13):
                sign = (asc_v_pos.sign_index + h - 1) % 12
                v_houses[h].append(str(sign + 1))
                
            for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                pv_pos = vargas_matrix[varga_sel][p_name]
                house_num = (pv_pos.sign_index - asc_v_pos.sign_index + 12) % 12 + 1
                p_abbr = constants.PLANETS_HI.get(p_name, p_name)[:2] if is_hi else p_name[:2]
                v_houses[house_num].append(f"{p_abbr} {pv_pos.dms_str}")
                
            vcol1, vcol2 = st.columns([1, 1.2])
            with vcol1:
                st.markdown(f"<h4 style='text-align: center; color: #f0c05a;'>{varga_sel} {'कुण्डली' if is_hi else 'Kundli'}</h4>", unsafe_allow_html=True)
                svg_v = get_north_indian_chart_svg(v_houses, size=500, chart_title=f"{varga_sel} Lagna: {asc_v_pos.sign_name} {asc_v_pos.dms_str}")
                render_kundli(svg_v)
                
            with vcol2:
                st.markdown(f"#### {varga_sel} {'सूक्ष्म ग्रह स्थिति' if is_hi else 'Micro-Positions'}")
                v_rows = []
                v_rows.append({
                    "बिंदु" if is_hi else "Point": "लग्न (Lagna)" if is_hi else "Lagna",
                    "राशि" if is_hi else "Divisional Sign": constants.SIGNS_HI[asc_v_pos.sign_index] if is_hi else asc_v_pos.sign_name,
                    "वर्ग में अंश" if is_hi else "Degree in Varga": asc_v_pos.dms_str,
                    "राशि स्वामी" if is_hi else "Sign Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[asc_v_pos.sign_index], constants.SIGN_LORD[asc_v_pos.sign_index]) if is_hi else constants.SIGN_LORD[asc_v_pos.sign_index],
                    "षष्ट्यंश देवता" if is_hi else "D60 Deity": asc_v_pos.deity if varga_sel == "D60" else "-",
                    "प्रकृति" if is_hi else "Disposition": ("शुभ (Benefic)" if asc_v_pos.is_benefic else "अशुभ (Malefic)") if varga_sel == "D60" else "-"
                })
                for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                    p_v_res = vargas_matrix[varga_sel][p_name]
                    v_rows.append({
                        "बिंदु" if is_hi else "Point": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                        "राशि" if is_hi else "Divisional Sign": constants.SIGNS_HI[p_v_res.sign_index] if is_hi else p_v_res.sign_name,
                        "वर्ग में अंश" if is_hi else "Degree in Varga": p_v_res.dms_str,
                        "राशि स्वामी" if is_hi else "Sign Lord": constants.PLANETS_HI.get(constants.SIGN_LORD[p_v_res.sign_index], constants.SIGN_LORD[p_v_res.sign_index]) if is_hi else constants.SIGN_LORD[p_v_res.sign_index],
                        "षष्ट्यंश देवता" if is_hi else "D60 Deity": p_v_res.deity if varga_sel == "D60" else "-",
                        "प्रकृति" if is_hi else "Disposition": ("शुभ (Benefic)" if p_v_res.is_benefic else "अशुभ (Malefic)") if varga_sel == "D60" else "-"
                    })
                st.dataframe(pd.DataFrame(v_rows), use_container_width=True, hide_index=True)

            # Automated Varga Prediction Card (Relative to D1 Lagna)
            vp_planets = {p: {"sign_index": vargas_matrix[varga_sel][p].sign_index, "sign_name": vargas_matrix[varga_sel][p].sign_name}
                          for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]}
            v_pred = vyas_vp.predict_varga(varga_sel, asc_v_pos.sign_index, vp_planets, asc_sign_idx)
            st.markdown(f"""
            <div class="glass-card" style="margin-top: 15px; border-left: 4px solid #f0c05a;">
                <div style="font-weight: 800; font-size: 1.1rem; color: #f0c05a; margin-bottom: 6px;">
                    {varga_sel} वर्ग फलित एवं लग्न सापेक्ष विश्लेषण (Automated Synthesis)
                </div>
                <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">
                    {v_pred['narrative']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if _lz_sub_tab[2]:
            st.markdown(f'<div class="section-title">{"D60 षष्ट्यंश विश्लेषण एवं अधिष्ठाता देवता (Prarabdha Karma Alignment)" if is_hi else "D60 Shashtyamsha & Deities"}</div>', unsafe_allow_html=True)
            st.info("पाराशरी सिद्धांत: षष्ट्यंश कुण्डली में पूर्वजन्म संचित प्रारब्ध एवं कर्म संस्कारों का अंतिम निर्णय होता है। प्रत्येक 30 कला (0°30') पर विशिष्ट अधिष्ठाता देवता का आधिपत्य होता है।")
            d60_table = []
            for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                pv = vargas_matrix["D60"][p_name]
                d60_table.append({
                    "ग्रह" if is_hi else "Planet": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                    "D60 राशि" if is_hi else "D60 Sign": constants.SIGNS_HI[pv.sign_index] if is_hi else pv.sign_name,
                    "अंश": pv.dms_str,
                    "अधिष्ठाता देवता": pv.deity,
                    "प्रकृति / स्वभाव": "शुभ (Benefic)" if pv.is_benefic else "अशुभ / शोधन योग्य"
                })
            st.markdown(render_modern_table(d60_table, title="D-60 षष्ट्यंश देवता एवं प्रारब्ध तालिका"), unsafe_allow_html=True)

        if _lz_sub_tab[3]:
            st.markdown(f'<div class="section-title">{"वर्ग कुण्डली शास्त्रीय सूत्र फलित (D1, D9, D10 व D60 महा-विश्लेषण)" if is_hi else "Divisional Vargas Script Synthesis"}</div>', unsafe_allow_html=True)
            v_scripts = vyas_knowledge_engine.synthesize_varga_scripts(chart, vargas_matrix)
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 16px; border-left: 4px solid var(--gold-accent);">
                <div style="font-weight: 700; color: var(--gold-primary); font-size: 1.1rem;">
                    13,000+ आंतरिक शास्त्रीय ज्ञानकोष से आपकी कुण्डली के वर्ग-चक्रों पर सक्रिय सूत्र
                </div>
                <div style="color: var(--text-main); font-size: 0.95rem; margin-top: 4px;">
                    वर्ग कुण्डलियों (षोडशवर्ग) के आधार पर लग्न-नवमांश संतुलन, दशमांश कर्म रेखा एवं षष्ट्यंश प्रारब्ध का सम्पूर्ण एकीकृत शास्त्रीय विश्लेषण:
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(v_scripts["d1_d9_script"], unsafe_allow_html=True)
            st.markdown(v_scripts["d10_script"], unsafe_allow_html=True)
            st.markdown(v_scripts["d60_script"], unsafe_allow_html=True)

            # Classical treatises direct search # Classical treatises direct search
            with st.expander(" समस्त शास्त्रीय ग्रंथ एवं पुस्तकें प्रत्यक्ष खोज (Search Classical Astrological Library)", expanded=False):
                try:
                    import vyas.book_reader as vyas_books
                    all_bks = vyas_books.list_available_books()
                    st.markdown(f"**पुस्तकालय स्थिति:** कुल **{len(all_bks)} शास्त्रीय ग्रंथ व पुस्तकें** (PDF, Markdown, JSONL) `books/` फोल्डर में उपलब्ध हैं।")
                    col_bk1, col_bk2 = st.columns([1.5, 1])
                    with col_bk1:
                        bk_query = st.text_input("ग्रंथों में श्लोक / शब्द खोजें (Search Shloka or Topic across Books):", placeholder="उदा. गजकेसरी, भृगु, मांगलिक, सूर्य...", key="bk_lib_search_q")
                    with col_bk2:
                        bk_options = ["समस्त ग्रंथ (All Treatises)"] + [b["filename"] for b in all_bks]
                        sel_bk = st.selectbox("विशिष्ट पुस्तक चुनें:", bk_options, index=0, key="bk_lib_sel_file")

                    if bk_query:
                        target_file_param = None if sel_bk == "समस्त ग्रंथ (All Treatises)" else sel_bk
                        search_res = vyas_books.search_books(bk_query, target_file_param, max_results=12)
                        if search_res:
                            st.success(f"कुल {len(search_res)} संदर्भ प्राप्त हुए:")
                            for sr in search_res:
                                st.markdown(f"""
                                <div style="background: rgba(15, 23, 42, 0.7); border-left: 3px solid #38bdf8; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                                    <div style="font-weight: 700; color: #38bdf8; font-size: 0.92rem;"> {sr['book']} &nbsp;<span style="color: #94a3b8; font-size: 0.82rem;">({sr['page']})</span></div>
                                    <div style="color: #f1f5f9; font-size: 0.88rem; margin-top: 4px; font-family: monospace;">{sr['snippet']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("इस शब्द पर कोई संदर्भ नहीं मिला। कृपया भिन्न शब्द खोजें।")
                except Exception as e:
                    st.warning(f"पुस्तक खोज में त्रुटि: {e}")

    # =========================================================================
    # SUITE: ASHTAKOOTA MILAN & DOSHA CANCELLATIONS
    # =========================================================================
    elif ("अष्टकूट" in selected_suite or "Ashtakoota" in selected_suite
          or "Compatibility" in selected_suite):
        st.markdown(f'<div class="section-title">{"अष्टकूट गुण मिलान (36 गुण) एवं शास्त्रीय दोष परिहार विश्लेषण" if is_hi else "Ashtakoota 36 Gunas Match & Classical Dosha Cancellation"}</div>', unsafe_allow_html=True)
        st.info("विवाह मिलान केवल 36 में से 18 गुण मिलाने तक सीमित नहीं है। ऋषि पराशर एवं मुहुर्त चिंतामणि के अनुसार यदि नाड़ी या भकूट में शास्त्रीय परिहार (Exceptions) लागू हो जाएं, तो शून्य अंक भी दोषमुक्त होकर शुभ फल प्रदान करते हैं।")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("<h4 style='color: #48cae4;'> वर विवरण (Boy Details)</h4>", unsafe_allow_html=True)
            boy_name = st.text_input("वर का नाम (Boy Name)", birth.get('name', 'वर (Groom)'), key="match_boy_name")
            boy_m_lon = chart.planets["Moon"].longitude
            boy_mars_h = (chart.planets["Mars"].sign_index - asc_sign_idx + 12) % 12 + 1
            st.markdown(f"<b>चन्द्र राशि:</b> {constants.SIGNS_HI[int(boy_m_lon // 30) % 12]} | <b>नक्षत्र:</b> {constants.NAKSHATRAS_HI[int(boy_m_lon // constants.NAKSHATRA_SPAN) % 27]} | <b>मंगल भाव:</b> भाव {boy_mars_h}", unsafe_allow_html=True)

        with col_m2:
            st.markdown("<h4 style='color: #ff858d;'> कन्या विवरण (Girl Details)</h4>", unsafe_allow_html=True)
            girl_name = st.text_input("कन्या का नाम (Girl Name)", "कन्या (Bride)", key="match_girl_name")
            girl_sign_choice = st.selectbox("कन्या की चन्द्र राशि (Girl Moon Sign)", constants.SIGNS_HI, index=(int(boy_m_lon // 30) + 4) % 12, key="match_girl_sign")
            girl_sign_idx = constants.SIGNS_HI.index(girl_sign_choice)
            girl_deg_in_sign = st.slider("कन्या चन्द्र अंश (Degrees in Sign)", min_value=0.0, max_value=29.9, value=15.0, step=0.5, key="match_girl_deg")
            girl_m_lon = girl_sign_idx * 30.0 + girl_deg_in_sign
            girl_mars_h = st.number_input("कन्या की कुण्डली में मंगल का भाव (Girl Mars House 1-12)", min_value=1, max_value=12, value=1, key="match_girl_mars")

        match_res = vyas_match.calculate_ashtakoota(boy_m_lon, girl_m_lon, boy_mars_h, girl_mars_h)

        # Overview score card
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; border: 2px solid #f0c05a; margin-top: 15px; margin-bottom: 20px;">
            <div style="font-size: 0.95rem; color: #eedc9a; font-weight: 700;">अष्टकूट कुल प्राप्तांक (TOTAL ASHTAKOOTA SCORE)</div>
            <div style="font-size: 3rem; font-weight: 900; color: #ffd97d; font-family: 'Cinzel', serif; margin: 4px 0;">
                {match_res['total_score']} / {match_res['max_score']} <span style="font-size: 1.2rem; color: #cbd5e1;">गुण</span>
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: {'#4ade80' if match_res['total_score'] >= 18 else '#f87171'};">
                {match_res['verdict']}
            </div>
            <div style="font-size: 0.95rem; color: #93c5fd; margin-top: 8px;">
                <b>मांगलिक (कुज) दोष स्थिति:</b> {match_res['manglik_status']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"#### 8 कूटों का विस्तृत परीक्षण एवं दोष परिहार सारणी")
        st.dataframe(pd.DataFrame(match_res["kootas"]), use_container_width=True, hide_index=True)
    elif "दशा" in selected_suite or "Dasha" in selected_suite:
        _lz_d_tab = lazy_sections([
            "विंशोत्तरी 5-स्तरीय दशा (Vimshottari 5-Levels)" if is_hi else "Vimshottari 5-Levels",
            "योगिनी दशा चक्र (Yogini Dasha 36-Year)" if is_hi else "Yogini Dasha",
            "ताजिक वर्षफल एवं मुन्था (Tajik Varshphal)" if is_hi else "Tajik Varshphal",
            "गोचर संचरण (Realtime Gochar Transits)" if is_hi else "Gochar Transits",
        ], key="d_tab")

        if _lz_d_tab[0]:
            st.markdown(f'<div class="section-title">{"विंशोत्तरी दशा: 5-स्तरीय सूक्ष्म समय कालक्रम" if is_hi else "Vimshottari 5-Fold Micro-Dasha"}</div>', unsafe_allow_html=True)
            cur_dasha = dasha_engine.get_running_dasha(datetime.now()) if hasattr(dasha_engine, 'get_running_dasha') else dasha_engine.get_dasha_at(datetime.now())
            st.markdown(f"""
            <div class="glass-card">
                <span style="color: #eedc9a; font-weight: bold;">{'वर्तमान सक्रिय 5-स्तरीय दशा: ' if is_hi else 'Current Active 5-Level Dasha: '}</span>
                <span style="color: #f0c05a; font-size: 1.15rem; font-weight: bold;">
                    {constants.PLANETS_HI.get(cur_dasha['MD']['lord'], cur_dasha['MD']['lord'])} MD | 
                    {constants.PLANETS_HI.get(cur_dasha['AD']['lord'], cur_dasha['AD']['lord'])} AD | 
                    {constants.PLANETS_HI.get(cur_dasha['PD']['lord'], cur_dasha['PD']['lord'])} PD | 
                    {constants.PLANETS_HI.get(cur_dasha['SD']['lord'], cur_dasha['SD']['lord'])} SD | 
                    {constants.PLANETS_HI.get(cur_dasha['PrD']['lord'], cur_dasha['PrD']['lord'])} PrD
                </span>
                <div style="color: #a0aec0; font-size: 0.85rem; margin-top: 4px;">
                    {'प्रत्यन्तर्दशा समाप्ति:' if is_hi else 'Pratyantar Ends:'} {cur_dasha['PD']['end']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Active Dasha Phala Synthesis (दशा फल)
            active_dasha_synth = forensic_predictor.compute_active_dasha_synthesis(chart, cur_dasha, dignities, bhavas)
            st.markdown(f"""
            <div class="predict-card" style="border-left-color: #ffd97d; margin-top: 15px; margin-bottom: 20px;">
                <div class="predict-header" style="color: #ffd97d; font-size: 1.15rem;">
                    वर्तमान सक्रिय विंशोत्तरी दशा महा-फलित (Active MD-AD-PD Synthesis)
                </div>
                <div style="font-size: 1.02rem; line-height: 1.7; color: #f8fafc; white-space: pre-line; margin-top: 8px;">
                    {active_dasha_synth['synthesis_hi']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'120-वर्षीय महादशा चक्र' if is_hi else '120-Year Mahadasha Trajectory'}")
            mds = dasha_engine.calculate_mahadashas(num_cycles=1)
            md_table = []
            for md in mds:
                md_table.append({
                    "महादशा स्वामी" if is_hi else "MD Lord": constants.PLANETS_HI.get(md.lord, md.lord) if is_hi else md.lord,
                    "आरम्भ तिथि" if is_hi else "Start Date": md.start_date.strftime("%d/%m/%Y"),
                    "समाप्ति तिथि" if is_hi else "End Date": md.end_date.strftime("%d/%m/%Y"),
                    "पूर्ण अवधि" if is_hi else "Duration": f"{constants.VIMSHOTTARI_YEARS.get(md.lord, 0)} {'वर्ष' if is_hi else 'Years'}"
                })
            st.dataframe(pd.DataFrame(md_table), use_container_width=True, hide_index=True)

        if _lz_d_tab[1]:
            st.markdown(f'<div class="section-title">{"योगिनी दशा: 36-वर्षीय जीवन चक्र एवं अन्तर्दशाएँ" if is_hi else "Yogini Dasha 36-Year Lifecycle"}</div>', unsafe_allow_html=True)
            y_cycles = forensic_predictor.compute_yogini_dasha(chart.planets["Moon"].longitude, birth["local"])
            y_table = []
            for yc in y_cycles[:16]:
                y_table.append({
                    "योगिनी नाम" if is_hi else "Yogini": yc["name_hi"] if is_hi else yc["name"],
                    "स्वामी ग्रह" if is_hi else "Lord": yc["lord_hi"] if is_hi else yc["lord"],
                    "अवधि" if is_hi else "Years": f"{yc['years']} {'वर्ष' if is_hi else 'Years'}",
                    "आरम्भ" if is_hi else "Start": yc["start"],
                    "समाप्ति" if is_hi else "End": yc["end"]
                })
            st.dataframe(pd.DataFrame(y_table), use_container_width=True, hide_index=True)

        if _lz_d_tab[2]:
            st.markdown(f'<div class="section-title">{"ताजिक वर्षफल एवं मुन्था विचार (Annual Solar Return)" if is_hi else "Tajik Varshphal & Muntha"}</div>', unsafe_allow_html=True)
            col_v1, col_v2 = st.columns([1, 2])
            with col_v1:
                varsh_choice = st.number_input(
                    "वर्षफल वर्ष का चयन करें (Target Varshphal Year):" if is_hi else "Target Varshphal Year:",
                    min_value=birth['local'].year,
                    max_value=birth['local'].year + 100,
                    value=2026,
                    step=1,
                    key="interactive_varsh_year_choice"
                )
            v_data = forensic_predictor.compute_tajik_varshphal(birth["local"], chart.planets["Sun"].longitude, int(varsh_choice), asc_sign_idx)
            
            with col_v2:
                st.markdown(f"""
                <div class="glass-card" style="margin-top: 10px;">
                    <div style="font-weight: bold; color: #f0c05a; font-size: 1.05rem;">
                         वर्ष चक्र: {v_data.get('target_year', varsh_choice)}-{int(v_data.get('target_year', varsh_choice))+1} (आयु {v_data.get('age', 0)} वर्ष)
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.92rem; margin-top: 4px;">
                        अवधि: {v_data.get('varsha_start', '')} से {v_data.get('varsha_end', '')} | वर्ष लग्न: <b>{v_data.get('varsha_lagna_hi', 'लग्न')}</b> | वर्षेश: <b>{v_data.get('varshesh_hi', 'वर्षेश')}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="predict-card">
                <div class="predict-header"> मुन्था स्थिति एवं वार्षिक महा-फलादेश:</div>
                <div style="font-size: 1.15rem; font-weight: bold; color: #4ade80;">{v_data.get('annual_summary_hi', '')}</div>
                <p style="margin-top: 8px; color: #e2e8f0; line-height: 1.6;">
                    मुन्था जन्म लग्न से <b>{v_data.get('muntha_house', 1)}वें भाव ({v_data.get('muntha_sign_hi', '')} राशि)</b> में संचरण कर रही है। {v_data.get('muntha_phal_hi', '')}
                </p>
                <div style="background: rgba(240, 192, 90, 0.1); border-left: 3px solid #f0c05a; padding: 8px 12px; border-radius: 4px; margin-top: 6px; color: #ffd97d; font-size: 0.9rem;">
                     <b>ताजिक नीलकण्ठी सूत्र:</b> यदि मुन्था 1, 2, 3, 5, 9, 10, 11 भावों में हो तो वर्ष अत्यंत शुभ, पदोन्नति, धन लाभ एवं यश प्रदायक होता है। त्रिक भावों (6, 8, 12) में स्वास्थ्य व विवादों से सतर्कता अपेक्षित है।
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'वार्षिक मुद्धा दशा तालिका (1-Year Patyayini Dasha)' if is_hi else 'Annual Mudda Dasha'}")
            mudda_df = []
            for md in v_data["mudda_periods"]:
                mudda_df.append({
                    "दशा स्वामी": md["planet_hi"] if is_hi else md["planet"],
                    "आरम्भ तिथि": md["start"],
                    "समाप्ति तिथि": md["end"],
                    "अवधि": f"{md['days']} दिन",
                    "प्रभाव फलित": f"{md['planet_hi']} के प्रभाव से वर्ष में इस अवधि में कर्म, स्वास्थ्य व वित्त पर विशेष प्रभाव रहता है।"
                })
            st.dataframe(pd.DataFrame(mudda_df), use_container_width=True, hide_index=True)

        if _lz_d_tab[3]:
            st.markdown(f'<div class="section-title">{"तात्कालिक गोचर संचरण एवं शास्त्रीय वेध विश्लेषण" if is_hi else "Gochar Transits & Vedha Analysis"}</div>', unsafe_allow_html=True)
            if hasattr(vyas_gochar, "get_current_transit_positions"):
                gochar_pos = _cached_transit_positions(datetime.now().strftime("%Y-%m-%d"))
            else:
                pos_now = vyas_ephem.planet_positions(datetime.now(timezone.utc))
                gochar_pos = {name: PlanetState(name=name, longitude=p.longitude, speed=p.speed) for name, p in pos_now.items()}
            
            g_table = []
            for p_name in ["Jupiter", "Saturn", "Rahu", "Ketu", "Mars", "Sun", "Mercury", "Venus", "Moon"]:
                if p_name in gochar_pos:
                    gp = gochar_pos[p_name]
                    g_house = (gp.sign_index - asc_sign_idx + 12) % 12 + 1
                    g_from_moon = (gp.sign_index - chart.planets["Moon"].sign_index + 12) % 12 + 1
                    g_table.append({
                        "ग्रह" if is_hi else "Planet": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                        "गोचर राशि" if is_hi else "Transit Sign": constants.SIGNS_HI[gp.sign_index] if is_hi else constants.SIGNS[gp.sign_index],
                        "लग्न से भाव" if is_hi else "House from Lagna": f"भाव {g_house}",
                        "चन्द्र से भाव" if is_hi else "House from Moon": f"भाव {g_from_moon}",
                        "स्थिति": "वक्री (R)" if gp.speed < 0 else "मार्गी (Direct)"
                    })
            st.markdown(render_modern_table(g_table, title="फलदीपिका शास्त्रीय गोचर एवं वेध तालिका"), unsafe_allow_html=True)

            st.markdown(f"#### {'फलदीपिका शास्त्रीय गोचर, तारा बल एवं वेध तालिका' if is_hi else 'Phaladeepika Transit, Tara & Vedha'}")
            try:
                transit_rows = _cached_gochar_transits(datetime.now().strftime("%Y-%m-%d"), 5.5, chart.planets["Moon"].longitude, chart.ascendant_longitude)
                t_table = []
                for tr in transit_rows:
                    t_table.append({
                        "ग्रह": constants.PLANETS_HI.get(tr.planet, tr.planet) if is_hi else tr.planet,
                        "गोचर राशि": constants.SIGNS_HI[tr.sign] if is_hi and tr.sign < 12 else tr.sign,
                        "अंश": f"{tr.degree:.2f}°",
                        "नक्षत्र": tr.nakshatra,
                        "तारा बल": tr.tara,
                        "वेध स्थिति": tr.vedha_by or "वेध-मुक्त (अबाधित)",
                        "गोचर प्रभाव": "शुभ फलदायी" if tr.favourable else "सावधानी अपेक्षित",
                        "आगामी राशि परिवर्तन": tr.next_ingress or "-"
                    })
                st.markdown(render_modern_table(t_table, title="दैनिक नवतारा चक्र एवं ताराबल"), unsafe_allow_html=True)
            except Exception as e:
                st.caption(f"Classical transit table: {e}")


    # =========================================================================
    # SUITE 3: ASHTAKAVARGA, SHADBALA & MAITRI
    # =========================================================================
    elif "अष्टकवर्ग" in selected_suite or "Ashtakavarga" in selected_suite:
        _lz_b_tab = lazy_sections([
            "अष्टकवर्ग चक्र एवं शोधन (SAV & BAV)" if is_hi else "Ashtakavarga Matrix",
            "षड्बल एवं भावबल (Shadbala & Bhavabala)" if is_hi else "Shadbala & Bhavabala",
            "भाव चलित एवं पञ्चधा मैत्री (Chalit & Maitri)" if is_hi else "Chalit & Maitri",
            "अष्टकवर्ग शास्त्रीय सूत्र महा-विश्लेषण" if is_hi else "Ashtakavarga Sutras Script",
        ], key="b_tab")

        p_signs = {n: p.sign_index for n, p in chart.planets.items()}
        av_res = vyas_ashtaka.compute_ashtakavarga(p_signs, asc_sign_idx)

        if _lz_b_tab[0]:
            st.markdown(f'<div class="section-title">{"समुदाय अष्टकवर्ग (SAV: 337 बिंदु) एवं शोधन" if is_hi else "Samudaya Ashtakavarga"}</div>', unsafe_allow_html=True)
            sav_pred = forensic_predictor.compute_ashtakavarga_predictions(av_res["sav"], asc_sign_idx)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-weight: bold; color: #f0c05a; font-size: 1.1rem;">अष्टकवर्ग शास्त्रीय निष्कर्ष:</div>
                <p style="color: #eedc9a; margin-top: 4px;">{sav_pred['wealth_flow_hi']}</p>
            </div>
            """, unsafe_allow_html=True)

            sav_cards_html = []
            for he in sav_pred["house_evals"]:
                pts = he["bindus"]
                if pts >= 30:
                    badge_border = "#10b981"
                    badge_bg = "rgba(16, 185, 129, 0.16)"
                    badge_color = "#34d399"
                    status_lbl = "अत्यंत प्रबल (सर्वश्रेष्ठ फल)" if pts >= 32 else "प्रबल (सकारात्मक फल)"
                elif pts >= 28:
                    badge_border = "#38bdf8"
                    badge_bg = "rgba(56, 189, 248, 0.16)"
                    badge_color = "#38bdf8"
                    status_lbl = "मध्यम (संतुलित फल)"
                else:
                    badge_border = "#ef4444"
                    badge_bg = "rgba(239, 68, 68, 0.16)"
                    badge_color = "#f87171"
                    status_lbl = "अल्प बली (सावधानी अपेक्षित)"

                sign_name = he["sign_hi"] if is_hi else constants.SIGNS[(asc_sign_idx + he['house'] - 1) % 12]
                sav_cards_html.append(f"""<div style="background: rgba(15, 23, 42, 0.72); border: 1px solid rgba(255,255,255,0.08); border-left: 4px solid {badge_border}; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.08rem; font-weight: 800; color: #f0c05a;">भाव {he['house']}</span>
<span style="font-size: 0.88rem; color: #cbd5e1; background: rgba(255,255,255,0.06); padding: 2px 10px; border-radius: 4px;">{sign_name} राशि</span>
</div>
<div style="display: flex; align-items: center; gap: 8px;">
<span style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; font-weight: 800; font-size: 0.82rem; padding: 2px 10px; border-radius: 12px;">{status_lbl}</span>
<span style="font-weight: 800; font-size: 1.05rem; color: #fbbf24; background: rgba(0,0,0,0.35); padding: 2px 12px; border-radius: 6px; border: 1px solid rgba(251, 191, 36, 0.35);">{pts} बिंदु</span>
</div>
</div>
<div style="font-size: 0.94rem; line-height: 1.65; color: var(--text-main, #f1f5f9);">{he['analysis_hi']}</div>
</div>""")
            st.markdown("".join(sav_cards_html), unsafe_allow_html=True)

        if _lz_b_tab[1]:
            st.markdown(f'<div class="section-title">{"षड्बल एवं भावबल विश्लेषण (Six-Fold Planetary Strengths)" if is_hi else "Shadbala Six-Fold Strengths"}</div>', unsafe_allow_html=True)
            # 2nd param is is_day_birth:bool (Sun in houses 1-6 = above horizon);
            # 3rd is paksha. The old call passed asc_sign_idx here.
            _sun_h = (chart.planets['Sun'].sign_index - asc_sign_idx + 12) % 12 + 1
            _is_day_birth = 1 <= _sun_h <= 6
            _pk = "Shukla" if ((chart.planets['Moon'].longitude - chart.planets['Sun'].longitude) % 360.0) < 180.0 else "Krishna"
            shad_res, bhava_res = vyas_shadbala.compute_shadbala(chart, _is_day_birth, _pk,
                                                                birth_utc=birth['local'], tz_hours=birth['tz'])
            shad_table = []
            for p, s in shad_res.items():
                shad_table.append({
                    "ग्रह": constants.PLANETS_HI.get(p, p) if is_hi else p,
                    "स्थान बल": f"{s.sthana_bala:.1f}",
                    "दिग् बल": f"{s.dig_bala:.1f}",
                    "काल बल": f"{s.kala_bala:.1f}",
                    "चेष्टा बल": f"{s.chesta_bala:.1f}",
                    "नैसर्गिक": f"{s.naisargika_bala:.1f}",
                    "दृग् बल": f"{s.drik_bala:.1f}",
                    "कुल विरूप": f"{s.total_virupas:.1f}",
                    "रूप में": f"{s.total_rupas:.2f}",
                    "श्रेणी": f"#{s.rank}",
                    "परिणाम": "प्रबल (बली)" if s.strength_ratio >= 1.0 else "निर्बल (दुर्बल)"
                })
            st.markdown(render_modern_table(shad_table, title="षड्बल एवं भावबल विस्तृत तालिका"), unsafe_allow_html=True)

        if _lz_b_tab[2]:
            st.markdown(f'<div class="section-title">{"श्रीपति भाव चलित चक्र एवं पञ्चधा मैत्री" if is_hi else "Sripati Chalit Chart & Maitri"}</div>', unsafe_allow_html=True)
            pl_lons = {n: p.longitude for n, p in chart.planets.items()}
            mc_lon = kp_cusps[9].longitude
            chalit_data = vyas_chalit.compute_sripati_chalit(chart.ascendant_longitude, mc_lon, pl_lons)
            
            # Construct Bhava Chalit Houses for Chart SVG
            chalit_houses = {h: [] for h in range(1, 13)}
            for cd in chalit_data:
                # Sign index of Bhava Madhya
                m_sign_idx = int(cd.madhya_deg // 30.0) % 12
                chalit_houses[cd.bhava_num].append(str(m_sign_idx + 1))
                for p in cd.planets_in_bhava:
                    p_obj = chart.planets[p]
                    p_hi_abbr = constants.PLANETS_HI.get(p, p)[:2] if is_hi else p[:2]
                    abbr = f"{p_hi_abbr} {int(p_obj.longitude % 30)}°{int((p_obj.longitude % 1)*60):02d}'"
                    if p_obj.is_retrograde:
                        abbr += " (व)" if is_hi else " (R)"
                    chalit_houses[cd.bhava_num].append(abbr)
                    
            ch_col1, ch_col2 = st.columns([1, 1.2])
            with ch_col1:
                st.markdown(f"<h4 style='text-align: center; color: #f0c05a;'>{'श्रीपति भाव-चलित चक्र' if is_hi else 'Sripati Bhava Chalit Chart'}</h4>", unsafe_allow_html=True)
                svg_chalit = get_north_indian_chart_svg(chalit_houses, size=500, chart_title="श्रीपति भाव चलित चक्र" if is_hi else "Sripati Bhava Chalit")
                render_kundli(svg_chalit)
            with ch_col2:
                st.markdown(f"#### {' भाव आरम्भ, मध्य (संधि) एवं अन्त सारणी' if is_hi else 'Bhava Sandhi & Cuspal Table'}")
                chalit_table = []
                for cd in chalit_data:
                    chalit_table.append({
                        "भाव": f"भाव {cd.bhava_num}",
                        "आरम्भ": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.arambha_sign)] if is_hi and cd.arambha_sign in constants.SIGNS else cd.arambha_sign} {cd.arambha_dms}",
                        "मध्य (शिखर)": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.madhya_sign)] if is_hi and cd.madhya_sign in constants.SIGNS else cd.madhya_sign} {cd.madhya_dms}",
                        "अन्त (संधि)": f"{constants.SIGNS_HI[constants.SIGNS.index(cd.anta_sign)] if is_hi and cd.anta_sign in constants.SIGNS else cd.anta_sign} {cd.anta_dms}",
                        "चलित भावस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in cd.planets_in_bhava]) if cd.planets_in_bhava else "-"
                    })
                st.markdown(render_modern_table(chalit_table, title="भाव चलित चक्र तालिका"), unsafe_allow_html=True)

            # Panchadha Maitri Matrix
            st.markdown(f"#### {' सप्तग्रह पञ्चधा मैत्री चक्र (Compound 5-Fold Friendship Matrix)' if is_hi else 'Panchadha Maitri Matrix'}")
            pm_matrix = vyas_chalit.compute_panchadha_maitri(p_signs)
            pm_rows = []
            for p1, rels in pm_matrix.items():
                row = {"ग्रह": constants.PLANETS_HI.get(p1, p1) if is_hi else p1}
                for p2, relation in rels.items():
                    p2_lbl = constants.PLANETS_HI.get(p2, p2) if is_hi else p2
                    row[p2_lbl] = relation
                pm_rows.append(row)
            st.markdown(render_modern_table(pm_rows, title="पंचधा मैत्री चक्र"), unsafe_allow_html=True)

        if _lz_b_tab[3]:
            st.markdown(f'<div class="section-title">{"अष्टकवर्ग शास्त्रीय सूत्र एवं काक्ष्य फलित" if is_hi else "Ashtakavarga Sutras Script"}</div>', unsafe_allow_html=True)
            av_script_res = vyas_knowledge_engine.synthesize_ashtakavarga_scripts(chart, av_res)
            st.markdown(av_script_res["ashtakavarga_script"], unsafe_allow_html=True)

    # =========================================================================
    # SUITE 4: KP, JAIMINI, NADI & CHAKRAS
    # =========================================================================
    elif "केपी" in selected_suite or "KP" in selected_suite:
        _lz_k_tab = lazy_sections([
            "केपी सूक्ष्म प्रणाली (KP System)" if is_hi else "KP System",
            "जैमिनी चर कारक" if is_hi else "Jaimini Karakas",
            "भृगु नन्दी नाड़ी" if is_hi else "Bhrigu Nandi Nadi",
            "वैदिक चक्र (Sudarshan & SBC)" if is_hi else "Classical Chakras",
            "पंचांग एवं अवकहड़ा" if is_hi else "Panchang & Avakhada",
        ], key="k_tab")

        if _lz_k_tab[0]:
            st.markdown(f'<div class="section-title">{" कृष्णमूर्ति पद्धति (KP System) • SSSSSL गणना, 4-Step कार्येश एवं जीवन प्रॉमिस" if is_hi else "Krishnamurti Paddhati (KP System) Master Engine"}</div>', unsafe_allow_html=True)
            
            # Precompute KP 4-fold significators and planet lords
            kp_sigs = compute_kp_4fold_house_significators(chart.planets, kp_cusps)
            house_significators = kp_sigs["house_significators"]
            planet_significators = kp_sigs["planet_significators"]
            planet_kp_lords = calculate_planet_kp_lords(chart.planets, kp_cusps)
            kp_promises = evaluate_kp_house_promises(kp_cusps, planet_significators, chart.planets)
            dasha_active = evaluate_active_houses_by_dasha(cur_dasha, planet_significators, kp_cusps)

            # --- SUB-SECTION 1: KAB KAUNSA BHAV ACTIVE HO RAHA HAI ---
            st.markdown(f"#### {'वर्तमान सक्रिय भाव एवं घटना कालक्रम (Active Houses by Dasha)' if is_hi else 'Active Houses by Running Dasha'}")
            
            md_hi = dasha_active['mahadasha_lord_hi']
            ad_hi = dasha_active['antardasha_lord_hi']
            pd_hi = dasha_active['pratyantardasha_lord_hi']
            co_active_str = ", ".join([f"भाव {h}" for h in dasha_active['co_active_houses']]) if dasha_active['co_active_houses'] else "समानुपातिक प्रभाव"
            all_active_str = ", ".join([f"भाव {h}" for h in dasha_active['all_active_houses']])

            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #38bdf8; margin-bottom: 18px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: #38bdf8;">
                    वर्तमान सक्रिय दशा चक्र: महादशा [{md_hi}] -> अन्तर्दशा [{ad_hi}] -> प्रत्यन्तर्दशा [{pd_hi}]
                </div>
                <div style="margin-top: 8px; font-size: 0.98rem; line-height: 1.7; color: #f8fafc;">
                    <b> अत्यंत तीव्र सक्रिय भाव (MD + AD सह-कार्येश):</b> <span style="color: #4ade80; font-weight: bold; font-size: 1.05rem;">{co_active_str}</span><br>
                    <b> समस्त सक्रिय भाव स्पेक्ट्रम (Total Active Spectrum):</b> <span style="color: #93c5fd;">{all_active_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Render event triggers
            for trg in dasha_active['event_triggers']:
                st.markdown(f"""
                <div class="predict-card" style="border-left-color: #06b6d4; margin-bottom: 8px; padding: 10px 14px;">
                    <div style="font-size: 0.98rem; color: #e2e8f0; line-height: 1.6;">{trg}</div>
                </div>
                """, unsafe_allow_html=True)

            # Active houses breakdown grid
            with st.expander(" सक्रिय भावों का विस्तृत कार्येश प्रभाव (Active Houses Influence Details)"):
                col_act1, col_act2 = st.columns(2)
                for i, ad_item in enumerate(dasha_active['active_details']):
                    target_c = col_act1 if i % 2 == 0 else col_act2
                    with target_c:
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 3px solid {ad_item['color']}; margin-bottom: 8px; padding: 8px 12px;">
                            <b style="color: {ad_item['color']};">भाव {ad_item['house']}: {ad_item['title']}</b> 
                            <span style="font-size: 0.8rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; margin-left: 6px;">{ad_item['intensity']}</span>
                            <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">{ad_item['meaning']}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- SUB-SECTION 2: KIS BAAT KA KYA PROMISE HAI KUNDLI MEIN ---
            st.markdown(f"#### {'कुण्डली में किस बात का प्रॉमिस है और क्या नहीं (KP Life Promises Verification)' if is_hi else 'KP Life Promises Verification'}")
            st.markdown("""
            <p style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 15px;">
                कृष्णमूर्ति पद्धति का अकाट्य नियम: किसी भी जीवन प्रसंग की सिद्धि या निषेध उस भाव के <b>कस्प उप-स्वामी (Cusp Sub-Lord)</b> तथा उसके <b>नक्षत्र स्वामी</b> द्वारा सिग्निफाई किए जाने वाले भावों पर निर्भर करती है।
            </p>
            """, unsafe_allow_html=True)

            col_p1, col_p2 = st.columns(2)
            for i, p_item in enumerate(kp_promises):
                t_col = col_p1 if i % 2 == 0 else col_p2
                with t_col:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {p_item['status_color']}; margin-bottom: 14px; min-height: 220px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: bold; font-size: 1.05rem; color: #f8fafc;">{p_item['icon']} {p_item['title_hi']}</span>
                            <span style="background: {p_item['status_color']}22; color: {p_item['status_color']}; border: 1px solid {p_item['status_color']}; font-size: 0.82rem; font-weight: bold; padding: 2px 8px; border-radius: 4px;">
                                {p_item['status_hi']}
                            </span>
                        </div>
                        <div style="font-size: 0.88rem; color: #eedc9a; margin-bottom: 6px;">
                            प्राथमिक कस्प: <b>भाव {p_item['primary_cusp']}</b> | उप-स्वामी (SL): <b>{p_item['sub_lord_hi']}</b> (नक्षत्र स्वामी: <b>{p_item['star_lord_hi']}</b>)
                        </div>
                        <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 8px;">
                            अनुकूल भाव: <b style="color: #4ade80;">{p_item['favorable_houses']}</b> (सक्रिय: {p_item['favorable_active'] or 'कोई नहीं'}) | 
                            विरोधी भाव: <b style="color: #f87171;">{p_item['detrimental_houses']}</b> (सक्रिय: {p_item['detrimental_active'] or 'कोई नहीं'})
                        </div>
                        <div style="font-size: 1.05rem; line-height: 1.75; color: #f1f5f9; text-align: left; margin: 0; word-wrap: break-word; overflow-wrap: break-word;">
                            {p_item['verdict_text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)

            # --- SUB-SECTION 3: KP PLACIDUS 12 CUSPS TABLE (DOWN TO SSSSSL) ---
            st.markdown(f"#### {' केपी 12 भाव कस्प स्पष्ट तालिका (Placidus Cusps down to SSSSSL)' if is_hi else 'KP Placidus Cusps (down to SSSSSL)'}")
            kp_table = []
            for c in kp_cusps:
                kp_table.append({
                    "भाव कस्प": f"भाव {c.cusp_num}",
                    "स्पष्ट अंश": c.dms_str,
                    "राशि": constants.SIGNS_HI[c.sign_index] if is_hi else c.sign_name,
                    "राशि स्वामी (RL)": constants.PLANETS_HI.get(c.sign_lord, c.sign_lord) if is_hi else c.sign_lord,
                    "नक्षत्र स्वामी (NL)": constants.PLANETS_HI.get(c.star_lord, c.star_lord) if is_hi else c.star_lord,
                    "उप-स्वामी (SL)": constants.PLANETS_HI.get(c.sub_lord, c.sub_lord) if is_hi else c.sub_lord,
                    "SSL": constants.PLANETS_HI.get(c.sub_sub_lord, c.sub_sub_lord) if is_hi else c.sub_sub_lord,
                    "SSSL": constants.PLANETS_HI.get(c.sub_sub_sub_lord, c.sub_sub_sub_lord) if is_hi else c.sub_sub_sub_lord,
                    "SSSSL": constants.PLANETS_HI.get(c.sub_sub_sub_sub_lord, c.sub_sub_sub_sub_lord) if is_hi else c.sub_sub_sub_sub_lord,
                    "SSSSSL": constants.PLANETS_HI.get(c.sub_sub_sub_sub_sub_lord, c.sub_sub_sub_sub_sub_lord) if is_hi else c.sub_sub_sub_sub_sub_lord
                })
            st.markdown(render_modern_table(kp_table, title="केपी कस्प उप-स्वामी तालिका"), unsafe_allow_html=True)

            # --- SUB-SECTION 4: 9 PLANETARY KP TABLE (DOWN TO SSSSSL) ---
            st.markdown(f"#### {'नवग्रह केपी स्पष्ट एवं SSSSSL तालिका (Planetary KP Table down to SSSSSL)' if is_hi else 'Planetary KP Table (down to SSSSSL)'}")
            kp_pl_table = []
            for pl in planet_kp_lords:
                kp_pl_table.append({
                    "ग्रह": pl.planet_hi if is_hi else pl.planet,
                    "स्पष्ट अंश": pl.dms_str,
                    "राशि": constants.SIGNS_HI[pl.sign_index] if is_hi else pl.sign_name,
                    "चलित भाव": f"भाव {pl.house_occupied}",
                    "राशि स्वामी (RL)": constants.PLANETS_HI.get(pl.sign_lord, pl.sign_lord) if is_hi else pl.sign_lord,
                    "नक्षत्र स्वामी (NL)": constants.PLANETS_HI.get(pl.star_lord, pl.star_lord) if is_hi else pl.star_lord,
                    "उप-स्वामी (SL)": constants.PLANETS_HI.get(pl.sub_lord, pl.sub_lord) if is_hi else pl.sub_lord,
                    "SSL": constants.PLANETS_HI.get(pl.sub_sub_lord, pl.sub_sub_lord) if is_hi else pl.sub_sub_lord,
                    "SSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_lord, pl.sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_lord,
                    "SSSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_sub_lord, pl.sub_sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_sub_lord,
                    "SSSSSL": constants.PLANETS_HI.get(pl.sub_sub_sub_sub_sub_lord, pl.sub_sub_sub_sub_sub_lord) if is_hi else pl.sub_sub_sub_sub_sub_lord
                })
            st.markdown(render_modern_table(kp_pl_table, title="केपी ग्रह स्थिति एवं उप-स्वामी तालिका"), unsafe_allow_html=True)

            # --- SUB-SECTION 5: 4-FOLD SIGNIFICATORS (चतुर्विध कार्येश) ---
            st.markdown(f"#### {'केपी 4-Step कार्येश तालिका (KP 4-Fold Significators Matrix)' if is_hi else 'KP 4-Fold Significators Matrix'}")
            
            _lz_sig_tab = lazy_sections([
                "ग्रह अनुसार कार्येश (Planet-wise Significators)" if is_hi else "Planet-wise Significators",
                "भाव अनुसार कार्येश (House-wise Significators)" if is_hi else "House-wise Significators",
            ], key="sig_tab")
            
            if _lz_sig_tab[0]:
                pl_sig_rows = []
                for p_name in constants.PLANETS:
                    if p_name in planet_significators:
                        s_info = planet_significators[p_name]
                        pl_sig_rows.append({
                            "ग्रह": constants.PLANETS_HI.get(p_name, p_name) if is_hi else p_name,
                            "स्थित भाव": f"भाव {s_info.get('house_occupied', '-')}",
                            "नक्षत्र स्वामी": constants.PLANETS_HI.get(s_info.get('star_lord', ''), s_info.get('star_lord', '')) if is_hi else s_info.get('star_lord', ''),
                            "कक्षा A (Star of Occ.)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_A', [])]) or "-",
                            "कक्षा B (Occ. House)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_B', [])]) or "-",
                            "कक्षा C (Star of Lord)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_C', [])]) or "-",
                            "कक्षा D (Lord of House)": ", ".join([f"भाव {h}" for h in s_info.get('lvl_D', [])]) or "-",
                            "समस्त कार्येश भाव": ", ".join([f"भाव {h}" for h in s_info.get('all_signified', [])]) or "-"
                        })
                st.dataframe(pd.DataFrame(pl_sig_rows), use_container_width=True, hide_index=True)

            if _lz_sig_tab[1]:
                h_sig_rows = []
                for h in range(1, 13):
                    hs = house_significators[h]
                    h_sig_rows.append({
                        "भाव": f"भाव {h}",
                        "भाव स्वामी": constants.PLANETS_HI.get(hs['house_lord'], hs['house_lord']) if is_hi else hs['house_lord'],
                        "भावस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['occupants']]) or "-",
                        "कक्षा A ग्रह (परम बलवान)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_a']]) or "-",
                        "कक्षा B ग्रह (बलवान)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_b']]) or "-",
                        "कक्षा C ग्रह (मध्यम)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_c']]) or "-",
                        "कक्षा D ग्रह (सामान्य)": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['level_d']]) or "-",
                        "समस्त कार्येश ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) if is_hi else p for p in hs['all_significators']]) or "-"
                    })
                st.dataframe(pd.DataFrame(h_sig_rows), use_container_width=True, hide_index=True)

            # KP Synthesized Script from 13,000 Sutras
            kp_script_res = vyas_knowledge_engine.synthesize_kp_scripts(chart, kp_cusps)
            st.markdown(kp_script_res["kp_script"], unsafe_allow_html=True)

            # KP 10 Core Life Event Promises via Cuspal Sub-Lords & Dasha Manifestation Timing
            st.markdown(f"#### {'केपी 10 प्रमुख जीवन घटना प्रॉमिस एवं दशा फलित काल' if is_hi else 'KP 10 Core Life Event Promises & Dasha Timing'}")
            kp_promises = vyas_kp.get_kp_house_promises(kp_cusps, planet_significators)
            col_p1, col_p2 = st.columns(2)
            for i, p_item in enumerate(kp_promises):
                target_col = col_p1 if i % 2 == 0 else col_p2
                with target_col:
                    with st.expander(f"{p_item['title_hi']} — {p_item['status_hi']}", expanded=(i in [0, 1])):
                        fav_str = ", ".join([str(h) for h in p_item['favorable_houses']])
                        fav_act_str = ", ".join([str(h) for h in p_item['favorable_active']]) or "कोई नहीं"
                        det_str = ", ".join([str(h) for h in p_item['detrimental_houses']])
                        det_act_str = ", ".join([str(h) for h in p_item['detrimental_active']]) or "कोई नहीं"
                        
                        st.markdown(f"""
                        <div style="font-size: 0.88rem; color: #eedc9a; margin-bottom: 6px;">
                            कस्प: <b>भाव {p_item['primary_cusp']}</b> | उप-स्वामी (SL): <b>{p_item['sub_lord_hi']}</b> | नक्षत्र स्वामी (NL): <b>{p_item['star_lord_hi']}</b>
                        </div>
                        <div style="font-size: 0.82rem; margin-bottom: 8px;">
                            <span style="background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); padding: 2px 6px; border-radius: 4px;">
                                अनुकूल भाव: {fav_str} (सक्रिय: {fav_act_str})
                            </span>
                            <span style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 2px 6px; border-radius: 4px; margin-left: 6px;">
                                विरोधी भाव: {det_str} (सक्रिय: {det_act_str})
                            </span>
                        </div>
                        <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-bottom: 8px;">
                            {p_item['verdict_text']}
                        </p>
                        <div style="border-top: 1px solid rgba(229, 169, 60, 0.2); padding-top: 6px; font-size: 0.88rem; color: #38bdf8;">
                            <b>फलित काल (Dasha Timing):</b> {p_item.get('timing_text', '')}
                        </div>
                        """, unsafe_allow_html=True)

            # KP Predictions & Dasha Event Timing Synthesis
            kp_preds = forensic_predictor.compute_kp_predictions_and_dasha_phala(chart, kp_cusps, cur_dasha)
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #38bdf8; margin-top: 15px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #7dd3fc; font-size: 1.05rem;">
                    केपी विंशोत्तरी दशा समन्वय (KP Dasha Synthesis)
                </div>
                <p style="font-size: 0.98rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">
                    {kp_preds['active_dasha_summary_hi']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'केपी कस्प उप-स्वामी सूक्ष्म फलकथन (Cusp Sub-Lord Predictions)' if is_hi else 'KP Cusp Sub-Lord Predictions'}")
            col_k1, col_k2 = st.columns(2)
            for i, ce in enumerate(kp_preds['cusp_evaluations']):
                target_col = col_k1 if i % 2 == 0 else col_k2
                with target_col:
                    with st.expander(f"{ce['title_hi']} [SL: {ce['sub_lord_hi']}]", expanded=(ce['cusp_num'] in [1, 2, 10])):
                        st.markdown(f"""
                        <div style="font-size: 0.85rem; color: #eedc9a; margin-bottom: 4px;">
                            राशि स्वामी: <b>{ce['sign_lord_hi']}</b> | नक्षत्र स्वामी: <b>{ce['star_lord_hi']}</b> | उप-स्वामी: <b>{ce['sub_lord_hi']}</b>
                        </div>
                        <p style="font-size: 0.98rem; line-height: 1.6; color: #f8fafc;">
                            {ce['prediction_hi']}
                        </p>
                        """, unsafe_allow_html=True)

        if _lz_k_tab[1]:
            st.markdown(f'<div class="section-title">{"जैमिनी सप्त चर कारक एवं आत्मकारक" if is_hi else "Jaimini Chara Karakas"}</div>', unsafe_allow_html=True)
            j_karakas, ak_p, km_sign = vyas_jaimini.compute_chara_karakas(chart.planets)
            jk_table = []
            for k in j_karakas:
                jk_table.append({
                    "चर कारक": f"{k.karaka_name} ({k.abbreviation})",
                    "ग्रह": constants.PLANETS_HI.get(k.planet, k.planet) if is_hi else k.planet,
                    "राशि में अंश": k.dms_str,
                    "राशि": constants.SIGNS_HI[constants.SIGNS.index(k.sign_name)] if is_hi and k.sign_name in constants.SIGNS else k.sign_name,
                    "शास्त्रीय कारकत्व": k.signification
                })
            st.markdown(render_modern_table(jk_table, title="जैमिनी चर कारक तालिका (7-Karaka Scheme)"), unsafe_allow_html=True)

            # Jaimini Predictions & Chara Dasha Phala Synthesis
            chara_dashas = forensic_predictor.compute_chara_dasha(chart.ascendant_sign, birth['local'], chart)
            j_preds = forensic_predictor.compute_jaimini_predictions_and_chara_dasha_phala(chart, j_karakas, ak_p, chara_dashas, birth['local'])

            j_script_res = vyas_knowledge_engine.synthesize_jaimini_scripts(chart)
            st.markdown(j_script_res["jaimini_script"], unsafe_allow_html=True)

            st.markdown(f"""
            <div class="predict-card" style="border-left-color: var(--gold-accent); margin-top: 15px;">
                <div class="predict-header" style="color: var(--gold-primary); font-size: 1.15rem;">
                    आत्मकारक (AK) एवं अमात्यकारक (AmK) जैमिनी राजयोग
                </div>
                <p style="font-size: 1.02rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                    {j_preds['ak_synthesis_hi']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            cd_info = j_preds['active_chara_dasha']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #a855f7; margin-top: 12px; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #c084fc; font-size: 1.1rem;">
                    वर्तमान सक्रिय चर महादशा फलित: {cd_info['sign_hi']} राशि ({cd_info['start']} से {cd_info['end']})
                </div>
                <p style="font-size: 1.02rem; line-height: 1.7; color: #e2e8f0; margin-top: 6px;">
                    {cd_info['prediction_hi']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'जैमिनी चर महादशा कालक्रम चक्र' if is_hi else 'Jaimini Chara Dasha Trajectory'}")
            cd_table = []
            for cd in chara_dashas:
                cd_table.append({
                    "राशि": cd.get("sign_hi", cd.get("sign", "")),
                    "अवधि": f"{cd.get('years', 0)} वर्ष",
                    "आरम्भ तिथि": cd.get("start", ""),
                    "समाप्ति तिथि": cd.get("end", "")
                })
            st.markdown(render_modern_table(cd_table, title="जैमिनी चर दशा कालखंड तालिका"), unsafe_allow_html=True)

        if _lz_k_tab[2]:
            st.markdown(f'<div class="section-title">{"भृगु नन्दी नाड़ी: गहन जीवन फलादेश एवं ग्रह संयोजन" if is_hi else "Bhrigu Nandi Nadi"}</div>', unsafe_allow_html=True)
            
            # BNN Deep Dynamic 4-Pillar Life Predictions & 12-Year Progression
            bnn_life = forensic_predictor.compute_bnn_detailed_life_predictions(chart, birth.get('local'))
            bnn_prog = bnn_life.get('bhrigu_progression', {})
            
            # 1. Bhrigu 12-Year Progression Cycle (भृगु 12 वर्षीय चक्र भ्रमण)
            if bnn_prog:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #f59e0b; margin-top: 15px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                        <div style="font-weight: 800; color: #fbbf24; font-size: 1.15rem;">
                            भृगु नन्दी नाड़ी 12 वर्षीय चक्र भ्रमण — {bnn_prog.get('cycle_title_hi', '')}
                        </div>
                        <span style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">
                            आयु: {bnn_prog.get('current_age_years', 0)} वर्ष (चक्र {bnn_prog.get('cycle_index', 1)})
                        </span>
                    </div>
                    <div style="font-size: 0.95rem; color: #e2e8f0; margin-top: 10px; line-height: 1.7;">
                        • <b>सक्रिय भ्रमण राशि:</b> <span style="color: #38bdf8; font-weight: 700;">{bnn_prog.get('progressed_sign_hi', '')} ({bnn_prog.get('progressed_sign', '')})</span><br/>
                        • <b>जीवन का केंद्रीय लक्ष्य:</b> {bnn_prog.get('cycle_focus_hi', '')}<br/>
                        • <b>कार्मिक निर्देश व सिद्धि:</b> <span style="color: #4ade80;">{bnn_prog.get('cycle_mandate_hi', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px; margin-top: 10px; margin-bottom: 20px;">
                <div class="glass-card" style="border-left: 4px solid #eab308;">
                    <div style="font-weight: bold; color: #facc15; font-size: 1.05rem;">जीव कारक (Jeeva Karaka - देवगुरु)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['jeeva_karaka_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #3b82f6;">
                    <div style="font-weight: bold; color: #60a5fa; font-size: 1.05rem;">कर्म कारक (Karma Karaka - शनिदेव)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['karma_karaka_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #10b981;">
                    <div style="font-weight: bold; color: #34d399; font-size: 1.05rem;">धन व बुद्धि कारक (Venus & Mercury)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['occult_mercury_hi']}</p>
                </div>
                <div class="glass-card" style="border-left: 4px solid #ec4899;">
                    <div style="font-weight: bold; color: #f472b6; font-size: 1.05rem;">नाड़ी दिशा संयोजन (Directional Trines)</div>
                    <p style="font-size: 0.95rem; line-height: 1.6; color: #f8fafc; margin-top: 6px;">{bnn_life['directional_trines_hi']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"#### {'पारस्परिक नाड़ी ग्रह संयोजन (Nadi Planetary Conjunctions)' if is_hi else 'Nadi Conjunctions'}")
            if hasattr(vyas_nadi, 'analyze_nadi_combinations'):
                nadi_res = vyas_nadi.analyze_nadi_combinations(chart.planets)
            elif hasattr(vyas_nadi, 'analyze_bhrigu_nandi_nadi'):
                res = vyas_nadi.analyze_bhrigu_nandi_nadi({p: st.sign for p, st in chart.planets.items()})
                combs = [{"name": c.title, "result": f"<b>{c.relationship}</b> ({c.auspiciousness})<br>{c.life_impact}"} for c in res.get("nadi_combinations", [])]
                nadi_res = {"combinations": combs}
            else:
                nadi_res = {"combinations": []}
            for comb in nadi_res.get("combinations", [])[:6]:
                st.markdown(f"""
                <div class="predict-card">
                    <div class="predict-header"> नाड़ी संयोजन: {comb.get('name', 'ग्रह युति')}</div>
                    <p>{comb.get('result', 'नाड़ी प्रभाव')}</p>
                </div>
                """, unsafe_allow_html=True)


        if _lz_k_tab[3]:
            st.markdown(f'<div class="section-title">{"वैदिक चक्र अनुसंधान: सुदर्शन चक्र, कोटा, सर्वतोभद्र एवं 27 नवतारा" if is_hi else "Classical Vedic Chakras Engine"}</div>', unsafe_allow_html=True)
            
            pl_lons = {n: p.longitude for n, p in chart.planets.items()}
            sudarshan_analysis = vyas_chakras.compute_sudarshan_chakra(chart)
            sbc_points = vyas_chakras.compute_sbc_special_points(chart.planets['Moon'].longitude, pl_lons)
            kota_res = vyas_chakras.compute_kota_chakra(chart.planets['Moon'].longitude, chart.ascendant_longitude, pl_lons)
            navatara_items = vyas_chakras.compute_navatara_chakra(chart.planets['Moon'].longitude, pl_lons)

            _lz_ch_sub = lazy_sections([
                "सुदर्शन चक्र" if is_hi else "Sudarshan Chakra",
                "कोटा चक्र" if is_hi else "Kota Chakra",
                "सर्वतोभद्र चक्र" if is_hi else "Sarvatobhadra Chakra",
                "27 नवतारा चक्र" if is_hi else "27 Navatara Chakra",
            ], key="ch_sub")

            if _lz_ch_sub[0]:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #f59e0b; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #fbbf24;">
                        महर्षि पाराशर प्रणीत सुदर्शन चक्र • त्रिविध संगम विश्लेषण
                    </div>
                    <p style="font-size: 0.98rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                        {sudarshan_analysis.sudarshan_verdict_hi}
                    </p>
                    <div style="font-size: 0.88rem; color: #eedc9a; margin-top: 6px;">
                        देह केंद्र (लग्न): <b>{sudarshan_analysis.lagna_sign_hi}</b> | 
                        मन केंद्र (चन्द्र): <b>{sudarshan_analysis.chandra_sign_hi}</b> | 
                        आत्मा केंद्र (सूर्य): <b>{sudarshan_analysis.surya_sign_hi}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                sd_table = []
                for sh in sudarshan_analysis.houses:
                    sd_table.append({
                        "भाव": f"भाव {sh.house_num}",
                        "शास्त्रीय नाम": sh.name_hi.split(" (")[1].replace(")", "") if " (" in sh.name_hi else sh.name_hi,
                        "लग्न से राशि (देह)": f"{sh.lagna_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.lagna_planets]) or 'रिक्त'})",
                        "चन्द्र से राशि (मन)": f"{sh.chandra_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.chandra_planets]) or 'रिक्त'})",
                        "सूर्य से राशि (आत्मा)": f"{sh.surya_sign_hi} ({', '.join([constants.PLANETS_HI.get(p, p) for p in sh.surya_planets]) or 'रिक्त'})",
                        "त्रिविध प्रभाव स्थिति": sh.status
                    })
                st.dataframe(pd.DataFrame(sd_table), use_container_width=True, hide_index=True)

                with st.expander(" सुदर्शन चक्र द्वादश भाव विस्तृत फलादेश"):
                    for sh in sudarshan_analysis.houses:
                        st.markdown(f"""
                        <div style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px;">
                            <b style="color: #f0c05a;">{sh.name_hi}:</b> 
                            <span style="color: #cbd5e1; font-size: 0.95rem;">{sh.summary_hi}</span>
                        </div>
                        """, unsafe_allow_html=True)

            if _lz_ch_sub[1]:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid {'#ef4444' if kota_res.is_fort_under_siege else '#22c55e'}; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: {'#f87171' if kota_res.is_fort_under_siege else '#4ade80'};">
                         कोटा चक्र (दुर्ग सुरक्षा व आक्रमण परीक्षण)
                    </div>
                    <p style="font-size: 0.98rem; line-height: 1.7; color: #f8fafc; margin-top: 8px;">
                        {kota_res.summary}
                    </p>
                    <div style="font-size: 0.88rem; color: #eedc9a; margin-top: 6px;">
                        कोटा स्वामी (दुर्ग अधिपति): <b>{constants.PLANETS_HI.get(kota_res.kota_swami, kota_res.kota_swami)}</b> | 
                        कोटा पाल (दुर्ग रक्षक): <b>{constants.PLANETS_HI.get(kota_res.kota_pala, kota_res.kota_pala)}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                kota_table = []
                for s_name, seg in kota_res.segments.items():
                    kota_table.append({
                        "दुर्ग प्राचीर खंड": seg.segment_name,
                        "समाहित नक्षत्र": ", ".join(seg.nakshatras[:4]) + ("..." if len(seg.nakshatras) > 4 else ""),
                        "उपस्थित ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in seg.planets_present]) if seg.planets_present else "कोई ग्रह नहीं",
                        "सामरिक प्रभाव": seg.nature
                    })
                st.dataframe(pd.DataFrame(kota_table), use_container_width=True, hide_index=True)

            if _lz_ch_sub[2]:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #8b5cf6; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #a78bfa;">
                        सर्वतोभद्र चक्र (28 नक्षत्र एवं 7 संवेदी मर्म बिंदु)
                    </div>
                    <p style="font-size: 0.95rem; color: #cbd5e1; margin-top: 6px;">
                        सर्वतोभद्र चक्र में अभिजित सहित 28 नक्षत्रों का प्रयोग होता है। जन्म नक्षत्र से 1, 10, 16, 18, 23, 25 एवं 26वें नक्षत्र विशेष संवेदी बिंदु होते हैं जिन पर क्रूर ग्रहों का गोचर अथवा वेध संकटकारक और शुभ ग्रहों का वेध कल्याणकारी होता है।
                    </p>
                </div>
                """, unsafe_allow_html=True)

                sbc_table = []
                for sp in sbc_points:
                    sbc_table.append({
                        "संवेदी मर्म बिंदु": sp.name,
                        "28-नक्षत्र": sp.nakshatra_28,
                        "जन्मनक्षत्र से दूरी": f"{sp.index_from_janma}वाँ नक्षत्र",
                        "कारकत्व एवं प्रभाव क्षेत्र": sp.significance,
                        "वर्तमान गोचरस्थ ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in sp.transiting_planets]) if sp.transiting_planets else "शुद्ध (वेध रहित)"
                    })
                st.dataframe(pd.DataFrame(sbc_table), use_container_width=True, hide_index=True)

            if _lz_ch_sub[3]:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #06b6d4; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: bold; color: #22d3ee;">
                        27 नवतारा चक्र (3 पर्य्याय: शारीरिक, कर्मिक एवं पारलौकिक)
                    </div>
                    <p style="font-size: 0.95rem; color: #cbd5e1; margin-top: 6px;">
                        जन्मनक्षत्र से 9 ताराओं का तीन आवृत्तियों में विभाजन: प्रथम पर्य्याय (व्यक्तिगत), द्वितीय पर्य्याय (कर्म व समाज), तृतीय पर्य्याय (आंतरिक व प्रारब्ध)।
                    </p>
                </div>
                """, unsafe_allow_html=True)

                nt_table = []
                for item in navatara_items:
                    nt_table.append({
                        "पर्य्याय": f"पर्य्याय {item.paryaya_num}",
                        "तारा नाम": item.tara_name,
                        "नक्षत्र": item.nakshatra_name,
                        "नक्षत्र स्वामी": constants.PLANETS_HI.get(item.nakshatra_lord, item.nakshatra_lord),
                        "गुणवत्ता": item.quality,
                        "उपस्थित ग्रह": ", ".join([constants.PLANETS_HI.get(p, p) for p in item.planets_present]) if item.planets_present else "-"
                    })
                st.dataframe(pd.DataFrame(nt_table), use_container_width=True, hide_index=True)

        if _lz_k_tab[4]:
            st.markdown(f'<div class="section-title">{"दैनिक पंचांग, अवकहड़ा चक्र एवं शुद्ध स्थानीय मुहूर्त" if is_hi else "Panchang, Avakhada & Local Muhurta"}</div>', unsafe_allow_html=True)
            panch_obj = _cached_panchang(birth['local'], birth['lat'], birth['lon'], birth['tz'], chart.ascendant_longitude)
            col_p1, col_p2, col_p3 = st.columns([1.1, 1.1, 1.2])
            with col_p1:
                st.markdown(f"""
                <div class="glass-card" style="height: 100%;">
                    <div style="font-weight: bold; color: #f0c05a; font-size: 1.05rem; margin-bottom: 6px;">पंचांग मुख्य अंग:</div>
                    <div style="font-size: 0.88rem; line-height: 1.8; color: #e2e8f0;">
                        <b>वार:</b> {panch_obj.vara} ({panch_obj.vara_lord})<br>
                        <b>तिथि:</b> {panch_obj.tithi} ({panch_obj.tithi_hi})<br>
                        <small style="color: #94a3b8;">समाप्ति: {panch_obj.tithi_end}</small><br>
                        <b>नक्षत्र:</b> {panch_obj.nakshatra} ({panch_obj.nakshatra_hi}) पद {panch_obj.nakshatra_pada}<br>
                        <small style="color: #94a3b8;">समाप्ति: {panch_obj.nakshatra_end}</small><br>
                        <b>योग:</b> {panch_obj.yoga} (समाप्ति: {panch_obj.yoga_end})<br>
                        <b>करण:</b> {panch_obj.karana} (समाप्ति: {panch_obj.karana_end})
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_p2:
                av = panch_obj.avakhada
                st.markdown(f"""
                <div class="glass-card" style="height: 100%;">
                    <div style="font-weight: bold; color: #f0c05a; font-size: 1.05rem; margin-bottom: 6px;">अवकहड़ा चक्र (Avakhada):</div>
                    <div style="font-size: 0.88rem; line-height: 1.8; color: #e2e8f0;">
                        <b>वर्ण:</b> {av.get('Varna', 'Brahmin')}<br>
                        <b>वश्य:</b> {av.get('Vashya', 'Keet')}<br>
                        <b>योनि:</b> {av.get('Yoni', 'Mrig')}<br>
                        <b>गण:</b> {av.get('Gana', 'Deva')}<br>
                        <b>नाड़ी:</b> {av.get('Nadi', 'Madhya')}<br>
                        <b>नाम अक्षर:</b> <span style="font-size: 1.1rem; color: #facc15; font-weight: bold;">{av.get('Naam Akshar', 'न')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_p3:
                st.markdown(f"""
                <div class="glass-card" style="height: 100%;">
                    <div style="font-weight: bold; color: #f0c05a; font-size: 1.05rem; margin-bottom: 6px;"> स्थानीय खगोलीय काल ({birth.get('city', 'New Delhi')}):</div>
                    <div style="font-size: 0.88rem; line-height: 1.8; color: #e2e8f0;">
                        <b>सूर्योदय:</b> <span style="color: #fde047;">{panch_obj.sunrise}</span> | <b>सूर्यास्त:</b> <span style="color: #fde047;">{panch_obj.sunset}</span><br>
                        <b>दिनमान:</b> {panch_obj.day_length}<br>
                        <b>अभिजीत मुहूर्त:</b> {'<span style="color: #ef4444; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 6px; border-radius: 4px;"> कोई नहीं (बुधवार को अभिजीत मुहूर्त नहीं होता)</span>' if ('कोई नहीं' in panch_obj.abhijit_muhurta or 'वर्जित' in panch_obj.abhijit_muhurta or 'Prohibited' in panch_obj.abhijit_muhurta or 'बुधवार' in panch_obj.abhijit_muhurta) else f'<span style="color: #38bdf8; font-weight: 700;">{panch_obj.abhijit_muhurta}</span>'}<br>
                        <b>ब्रह्म मुहूर्त:</b> <span style="color: #4ade80; font-weight: 600;">{panch_obj.brahma_muhurta}</span><br>
                        <b>विजय मुहूर्त:</b> <span style="color: #4ade80; font-weight: 600;">{panch_obj.vijaya_muhurta}</span> | <b>गोधूलि:</b> <span style="color: #4ade80; font-weight: 600;">{panch_obj.godhuli_muhurta}</span><br>
                        <b>राहु काल:</b> <span style="color: #ef4444; font-weight: 700;">{panch_obj.rahu_kalam}</span><br>
                        <b>यमगण्ड:</b> <span style="color: #f59e0b; font-weight: 700;">{panch_obj.yamaganda}</span> | <b>गुलिक काल:</b> {panch_obj.gulika_kalam}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Chaughadiya Grid inside Panchang tab
            if panch_obj.chaughadiya_day:
                with st.expander(" शुद्ध अक्षांशीय चौघड़िया चक्र (Day & Night Chaughadiya Grid)", expanded=False):
                    def _render_ch_mini(ch_list):
                        cards = []
                        for c in ch_list:
                            color = c.get('color', '#10b981')
                            is_good = c.get('is_good', True)
                            b_bg = "rgba(16, 185, 129, 0.2)" if is_good else "rgba(239, 68, 68, 0.2)"
                            b_col = "#4ade80" if is_good else "#f87171"
                            b_lbl = "शुभ" if is_good else "अशुभ"
                            cards.append(f"""<div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid {color}; border-radius: 8px; padding: 8px 10px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 6px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-weight: 800; font-size: 0.92rem; color: {color};">{c.get('name_hi')} ({c.get('name')})</div>
<span style="background: {b_bg}; color: {b_col}; border: 1px solid {b_col}44; padding: 1px 5px; border-radius: 4px; font-weight: 700; font-size: 0.70rem;">{b_lbl}</span>
</div>
<div style="font-size: 0.75rem; color: #94a3b8; margin: 2px 0;">{c.get('nature')}</div>
<div style="font-size: 0.78rem; font-weight: 600; color: #f8fafc;">{c.get('start')} - {c.get('end')}</div>
</div>""")
                        return '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px;">' + "".join(cards) + '</div>'

                    ch_col1, ch_col2 = st.columns(2)
                    with ch_col1:
                        st.markdown("<b>दिन का चौघड़िया (Day):</b>", unsafe_allow_html=True)
                        st.markdown(_render_ch_mini(panch_obj.chaughadiya_day), unsafe_allow_html=True)
                    with ch_col2:
                        st.markdown("<b>रात्रि का चौघड़िया (Night):</b>", unsafe_allow_html=True)
                        st.markdown(_render_ch_mini(panch_obj.chaughadiya_night), unsafe_allow_html=True)

    # =========================================================================
    # SUITE 5:  DEEP FORENSIC PREDICTIONS (Extensive Classical Analysis)
    # =========================================================================
    elif ("फलित" in selected_suite or "Predictions" in selected_suite
          or "Forecast" in selected_suite):
        p_signs = {n: p.sign_index for n, p in chart.planets.items()}
        av_res = vyas_ashtaka.compute_ashtakavarga(p_signs, asc_sign_idx)
        sav = av_res["sav"]
        dignities = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_matrix)
        bhavas = forensic_predictor.analyze_all_12_bhavas(chart, dignities)
        overall_forecast = forensic_predictor.compute_overall_life_forecast(
            chart, dignities, bhavas, sav, vargas_matrix,
            dasha_engine=st.session_state.get('dasha_engine'),
            birth=st.session_state.get('birth'),
        )

        _lz_p_tab = lazy_sections([
            "समग्र जीवन महा-फलादेश (13 जीवन अध्याय)" if is_hi else "Master Overall Life Forecast",
            "द्वादश भाव विस्तृत फलादेश (12 Bhavas)" if is_hi else "12 Bhavas In-Depth",
            "भावत् भावम् सूक्ष्म विश्लेषण (Bhavat Bhavam)" if is_hi else "Bhavat Bhavam Matrix",
            "ग्रह अवस्था एवं दृष्टि बल (Dignities & Aspects)" if is_hi else "Dignities & Aspects",
            "मंगल दोष सम्पूर्ण विवेचन एवं परिहार (Mangal Dosha)" if is_hi else "Mangal Dosha Analysis",
            "शनि साढ़े साती एवं ढैय्या 46-चरणीय चक्र (Sade Sati)" if is_hi else "Sade Sati Report",
            "कालसर्प दोष 12 भेदों की सूक्ष्म जाँच (Kalsarp Dosha)" if is_hi else "Kalsarp Dosha",
            "विशिष्ट शास्त्रीय योग एवं दुर्लभ फलित (Classical Yogas)" if is_hi else "Classical Rare Yogas",
        ], key="p_tab")

        if _lz_p_tab[0]:
            st.markdown(f'<div class="section-title">{"महर्षि पाराशर व कल्याणवर्मा परंपरा: समग्र जीवन महा-फलादेश (13 जीवन अध्याय)" if is_hi else "Comprehensive Classical Life Horoscope Synthesis"}</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid var(--gold-accent); margin-bottom: 20px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: var(--gold-primary);">फलित ज्योतिष शोध प्रबन्ध • वरिष्ठ ज्योतिषी दृष्टिकोण</div>
                <p style="color: var(--text-main); margin-top: 6px; font-size: 0.98rem; line-height: 1.6;">
                    यह फलादेश केवल सतही ग्रह स्थिति नहीं, अपितु बृहत्पाराशर होराशास्त्र, फलदीपिका, सारावली, जातक पारिजात एवं सर्वार्थचिंतामणि के संयुक्त शास्त्रीय नियमों पर आधारित 13 विस्तृत अध्यायों का महा-संश्लेषण है।
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            for _chap in overall_forecast:
                ch_num = _chap.get('chapter_num', 1)
                ch_title = _chap.get('title_hi', _chap.get('title', 'जीवन अध्याय'))
                ch_icon = _chap.get('icon', 'destiny')
                with st.expander(f"अध्याय {ch_num}: {ch_title}", expanded=(ch_num in [1, 4, 5, 8])):
                    st.markdown(f"""
                    <div class="predict-card" style="border-left-color: var(--gold-accent);">
                        <div class="predict-header" style="font-size: 1.18rem; color: var(--gold-primary); display: flex; align-items: center; gap: 8px;">
                            {get_svg_vector(ch_icon, 20)} <span>{ch_title}</span>
                        </div>
                        <div style="font-size: 1.15rem; line-height: 1.85; color: var(--text-main); text-align: left; margin-top: 12px; word-wrap: break-word; overflow-wrap: break-word;">
                            {_chap.get('content_hi', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        if _lz_p_tab[1]:
            st.markdown(f'<div class="section-title">{"द्वादश भाव गहन ज्योतिषीय फलित (12 Houses Forensic Interpretation)" if is_hi else "12 Houses Forensic Interpretation"}</div>', unsafe_allow_html=True)
            bhava_scripts_data = vyas_knowledge_engine.synthesize_bhava_and_yogas_scripts(chart)
            bhava_map = bhava_scripts_data.get("bhava_map", {})
            for bh in bhavas:
                with st.expander(f"भाव {bh.bhava_num}: {bh.sign_hi} राशि (स्वामी: {bh.lord_hi}) — [{bh.strength_type}]", expanded=(bh.bhava_num in [1, 7, 10])):
                    st.markdown(f"""
                    <div class="predict-card">
                        <div style="color: var(--gold-primary); font-weight: bold; margin-bottom: 6px;">
                            भावाधिपति स्थिति: भाव {bh.lord_house} ({bh.lord_sign_hi}) | 
                            भावस्थ ग्रह: {', '.join(bh.occupants_hi) or 'कोई नहीं (रिक्त)'} | 
                            दृष्टि डालने वाले ग्रह: {', '.join(bh.aspecting_planets_hi) or 'कोई नहीं'}
                        </div>
                        <div style="font-size: 1.12rem; line-height: 1.8; color: var(--text-main); text-align: left; word-wrap: break-word; overflow-wrap: break-word;">{bh.prediction_hi}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Weave matched Bhrigu Sutram & Bhavadhipati sutras into this house
                    m_sutras_in_bh = bhava_map.get(bh.bhava_num, [])
                    if m_sutras_in_bh:
                        st.markdown(f"<b>भाव {bh.bhava_num} पर सक्रिय प्रामाणिक शास्त्रीय सूत्र:</b>", unsafe_allow_html=True)
                        for s in m_sutras_in_bh:
                            st.markdown(f"""
                            <div style="background: var(--card-bg); border-left: 3px solid var(--gold-accent); padding: 8px 12px; margin-top: 6px; border-radius: 6px; border: 1px solid var(--card-border);">
                                <div style="font-weight: 600; color: var(--gold-primary); font-size: 0.92rem;">[{s.source}] {s.sub_category}</div>
                                <div style="color: var(--text-main); font-size: 0.90rem; margin-top: 2px;">{s.prediction_hi}</div>
                            </div>
                            """, unsafe_allow_html=True)

        if _lz_p_tab[2]:
            st.markdown(f'<div class="section-title">{"भावत् भावम् सूक्ष्म सिद्धांत एवं फलित (Bhavat Bhavam Recursive Matrix)" if is_hi else "Bhavat Bhavam Matrix"}</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid var(--gold-accent); margin-bottom: 20px;">
                <div style="font-size: 1.15rem; font-weight: bold; color: var(--gold-primary);">भावत् भावम् सिद्धांत • बृहत्पाराशर होराशास्त्र एवं फलदीपिका</div>
                <p style="color: var(--text-main); margin-top: 6px; font-size: 0.98rem; line-height: 1.6;">
                    वैदिक ज्योतिष का अमर नियम: किसी भी भाव का सूक्ष्म फल जानने के लिए उस भाव से उतनी ही दूरी वाले भाव (H-from-H) का परीक्षण करना अनिवार्य है।
                    उदा. द्वितीय का द्वितीय = तृतीय भाव (धन की सुरक्षा व पराक्रम), अष्टम का अष्टम = तृतीय भाव (आयु का आधार), दशम का दशम = सप्तम भाव (व्यापार व प्रतिष्ठा)।
                </p>
            </div>
            """, unsafe_allow_html=True)

            bb_data = forensic_predictor.compute_bhavat_bhavam_analysis(chart, dignities, bhavas, sav)
            bb_table = []
            for b in bb_data:
                bb_table.append({
                    "सम्बद्ध भाव": f"भाव {b['primary_house']} -> भाव {b['secondary_house']}",
                    "शास्त्रीय सूत्र": b["title_hi"],
                    "प्राथमिक स्वामी": f"{b['prim_lord_hi']} ({b['prim_sign_hi']})",
                    "प्राथमिक SAV": b["prim_sav"],
                    "भावत् भावम् स्वामी": f"{b['sec_lord_hi']} ({b['sec_sign_hi']})",
                    "द्वितीयक SAV": b["sec_sav"],
                    "सामर्थ्य निर्णय": b["status_verdict"]
                })
            st.markdown(render_modern_table(bb_table, title="भावत् भावम् द्वादश विश्लेषण तालिका"), unsafe_allow_html=True)

            st.markdown("#### भावत् भावम् द्वादश गहन फलकथन:")
            col_bb1, col_bb2 = st.columns(2)
            for idx_bb, b in enumerate(bb_data):
                target_col = col_bb1 if idx_bb % 2 == 0 else col_bb2
                with target_col:
                    with st.expander(f"{b['title_hi']} [{b['status_verdict']}]", expanded=(b['primary_house'] in [1, 2, 7, 10])):
                        st.markdown(f"""
                        <div style="font-size: 0.9rem; color: var(--gold-primary); margin-bottom: 6px;">
                            <b>मूल कारकत्व:</b> {b['karakatwa_hi']}<br>
                            प्राथमिक भाव {b['primary_house']} ({b['prim_sign_hi']} - {b['prim_sav']} SAV) | 
                            द्वितीयक भाव {b['secondary_house']} ({b['sec_sign_hi']} - {b['sec_sav']} SAV)
                        </div>
                        <div style="font-size: 1.10rem; line-height: 1.8; color: var(--text-main); text-align: left; word-wrap: break-word; overflow-wrap: break-word;">
                            {b['verdict_hi']}
                        </div>
                        """, unsafe_allow_html=True)

        if _lz_p_tab[3]:
            st.markdown(f'<div class="section-title">{"ग्रह अवस्था, अस्त/वक्री एवं दृष्टि बल विश्लेषण" if is_hi else "Planetary Dignities & States"}</div>', unsafe_allow_html=True)
            dig_rows = []
            for p_name, dig in dignities.items():
                p_hi = constants.PLANETS_HI.get(p_name, p_name)
                dig_rows.append({
                    "ग्रह": p_hi,
                    "राशि": dig.sign_hi,
                    "भाव": f"भाव {dig.house}",
                    "अवस्था": dig.awastha_hi,
                    "नवमांश (D9)": dig.d9_sign_hi + (" (वर्गोत्तम)" if dig.is_vargottama else ""),
                    "दृष्टि डालने वाले ग्रह": ", ".join([constants.PLANETS_HI.get(x, x) for x in dig.aspects_received_from]) or "-",
                    "शास्त्रीय गरिमा": dig.dignity_summary_hi
                })
            st.markdown(render_modern_table(dig_rows, title="ग्रह गरिमा, उच्च-नीच व अवस्था परीक्षण"), unsafe_allow_html=True)

        if _lz_p_tab[4]:
            st.markdown(f'<div class="section-title">{"मंगल दोष सम्पूर्ण शास्त्रीय विवेचन एवं परिहार" if is_hi else "Mangal Dosha Assessment"}</div>', unsafe_allow_html=True)
            m_dosha = forensic_predictor.compute_comprehensive_mangal_dosha(chart)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.2rem; font-weight: bold; color: var(--accent-emerald);">स्थिति: {m_dosha['severity']}</div>
                <p style="margin-top: 8px; font-size: 1.05rem; line-height: 1.6; color: var(--text-main);">{m_dosha['summary_hi']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("#### सर्वकल्याणकारी मङ्गल शांति उपाय:")
            for r in m_dosha['remedies_hi']:
                st.markdown(f"• {r}")

        if _lz_p_tab[5]:
            st.markdown(f'<div class="section-title">{"शनि साढ़े साती एवं ढैय्या 46-चरणीय जीवन चक्र" if is_hi else "Shani Sade Sati Full Report"}</div>', unsafe_allow_html=True)
            sade_phases = forensic_predictor.compute_comprehensive_sade_sati(birth["local"], chart.planets["Moon"].longitude, tz_hours=float(birth.get("tz", 5.5)))
            s_table = []
            for sp in sade_phases:
                s_table.append({
                    "साढ़े साती चरण": sp.phase_name_hi,
                    "शनि राशि": sp.saturn_sign_hi,
                    "आरम्भ दिनांक": sp.start_date,
                    "समाप्ति दिनांक": sp.end_date,
                    "चरण भेद": sp.charan_hi,
                    "विशिष्ट शास्त्रीय प्रभाव": sp.impact_hi
                })
            st.markdown(render_modern_table(s_table, title="शनि साढ़ेसाती एवं ढैया संपूर्ण कालखंड"), unsafe_allow_html=True)

        if _lz_p_tab[6]:
            st.markdown(f'<div class="section-title">{"कालसर्प दोष 12 भेदों की सूक्ष्म जाँच" if is_hi else "Kalsarp Dosha Analysis"}</div>', unsafe_allow_html=True)
            k_dosha = forensic_predictor.compute_comprehensive_kalsarp(chart)
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.2rem; font-weight: bold; color: var(--accent-emerald);">निर्णय: {k_dosha['status_hi']}</div>
                <p style="margin-top: 8px; font-size: 1.05rem; line-height: 1.6; color: var(--text-main);">{k_dosha['description_hi']}</p>
            </div>
            """, unsafe_allow_html=True)

        if _lz_p_tab[7]:
            st.markdown(f'<div class="section-title">{"विशिष्ट शास्त्रीय योग एवं दुर्लभ फलित" if is_hi else "Classical Rare Yogas & Forensic Timing"}</div>', unsafe_allow_html=True)
            yoga_scripts_data = vyas_knowledge_engine.synthesize_bhava_and_yogas_scripts(chart)
            st.markdown(yoga_scripts_data["yogas_script"], unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f'<div class="section-title">{"पारंपरिक पाराशरी सूत्र बैंक एवं दशा-गोचर सक्रियता काल" if is_hi else "Traditional Parashari Sutras & Dasha Activation Timing"}</div>', unsafe_allow_html=True)
            sutra_eval = vyas_sutra_bank.evaluate_classical_sutras(chart)
            timeline_map = vyas_sutra_bank.compute_yoga_activation_timeline(chart, sutra_eval, dasha_engine=dasha_engine)

            for se in sutra_eval:
                tl = timeline_map.get(se.sutra_id, {})
                status_badge = tl.get("status_badge", "सक्रिय")
                status_color = tl.get("status_color", "#10b981")
                active_now_desc = tl.get("active_now_desc", "")
                next_window_desc = tl.get("next_window_desc", "")
                peak_mahadasha_desc = tl.get("peak_mahadasha_desc", "")
                gochar_trigger_desc = tl.get("gochar_trigger_desc", "")
                classical_reasoning_hi = tl.get("classical_reasoning_hi", "")
                cur_dasha_str = tl.get("current_dasha_str", "")

                sutra_card_html = f"""<div class="predict-card" style="border-left-color: {status_color};">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
<div class="predict-header">{se.name} — <span style="font-size: 0.85rem; color: var(--text-muted);">[{se.source}]</span></div>
<span style="background: {status_color}22; color: {status_color}; border: 1px solid {status_color}55; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 0.82rem;">{status_badge}</span>
</div>
<div style="font-family: 'Tiro Devanagari Sanskrit', serif; color: var(--gold-primary); font-weight: bold; margin: 4px 0;">{se.shloka_sanskrit}</div>
<div style="color: var(--text-main); font-size: 0.95rem;"><b>सत्यापित स्थिति:</b> {se.condition_description}</div>
<div style="color: var(--accent-emerald); font-size: 0.95rem; margin-top: 4px;"><b>फलकथन:</b> {se.deterministic_result}</div>
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(229, 169, 60, 0.2); border-radius: 8px; padding: 10px; margin-top: 10px;">
<div style="font-size: 0.9rem; color: #facc15; font-weight: 700; margin-bottom: 4px;">दशा-गोचर सक्रियता समय चक्र (Activation Windows)</div>
<div style="font-size: 0.88rem; color: #e2e8f0; line-height: 1.6;">
• <b>वर्तमान दशा स्थिति:</b> {active_now_desc} (दशा: {cur_dasha_str})<br/>
• <b>आगामी सक्रियता काल:</b> <span style="color: #38bdf8; font-weight: 600;">{next_window_desc}</span><br/>
• <b>चरम उत्कर्ष महादशा:</b> <span style="color: #facc15; font-weight: 600;">{peak_mahadasha_desc}</span><br/>
• <b>गोचर ट्रिगर:</b> <span style="color: #cbd5e1;">{gochar_trigger_desc}</span>
</div>
</div>
<div style="font-size: 0.85rem; color: #94a3b8; font-style: italic; margin-top: 6px;">{classical_reasoning_hi}</div>
</div>"""
                st.markdown(sutra_card_html, unsafe_allow_html=True)

    # =========================================================================
    # SUITE 6:  43+ PAGE PUBLICATION PDF   # SUITE 6:  43+ PAGE PUBLICATION PDF (VYAS-Class Publication)
    # =========================================================================
    elif "PDF" in selected_suite or "शोध प्रबंध" in selected_suite:
        st.markdown(f'<div class="section-title">{" 56-पेज सम्पूर्ण वैदिक कुण्डली महा-शोध प्रबंध (VYAS Gold Standard PDF)" if is_hi else " 56-Page Executive Vedic Kundli Dossier (VYAS Gold Standard PDF)"}</div>', unsafe_allow_html=True)
        st.info("यह रिपोर्ट एस्ट्रोसेज की 56-पृष्ठ प्रीमियम कुण्डली के समकक्ष व उससे भी अधिक शुद्ध गणितीय गणनाओं, पाश्चात्य दृष्टि तालिकाओं, षोडशवर्ग चक्रों, सूक्ष्म प्रत्यंतर दशाओं और 100% प्रामाणिक वैदिक फलित से युक्त है।")
        
        # Unique per-run output path. The old fixed filename meant a FAILED
        # Chrome run silently "succeeded" by serving the previously generated
        # PDF (same report regardless of input data — the reported bug).
        _pdf_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_out_path = os.path.join(os.path.dirname(__file__), f"VYAS_VYAS_Standard_Kundli_56_Pages_{_pdf_stamp}.pdf")
        
        col_gen1, col_gen2 = st.columns([1, 1.2])
        with col_gen1:
            pdf_lang_opt = st.radio(
                "रिपोर्ट की भाषा चुनें (Select Report Language):",
                ["English (VYAS Gold Standard)", "Hindi (हिंदी)"],
                index=0,
                horizontal=True,
                key="suite6_pdf_lang"
            )
            selected_pdf_lang = "en" if "English" in pdf_lang_opt else "hi"

            varsh_choice_pdf = st.number_input(
                "वर्षफल वर्ष का चयन (Varshphal Year in PDF):" if is_hi else "Varshphal Year in PDF:",
                min_value=birth['local'].year,
                max_value=birth['local'].year + 100,
                value=max(2026, birth['local'].year),
                step=1,
                key="suite6_varsh_year"
            )
            if st.button(" 56-पेज VYAS स्टैंडर्ड महा-रिपोर्ट PDF तैयार करें", type="primary", use_container_width=True):
                with st.spinner("Compiling 56-Page VYAS Gold Standard Dossier with Crisp Diamond Charts, Pratyantar Matrices & Western Aspects..."):
                    success = publication_engine.build_publication_pdf(
                        chart, birth, kp_cusps, dasha_engine, vargas_matrix, pdf_out_path, target_varsh_year=int(varsh_choice_pdf), lang=selected_pdf_lang
                    )
                    if success and os.path.exists(pdf_out_path):
                        # Retire the previous session PDF (unique per-run name).
                        _old_pdf = st.session_state.get('pdf_out_path')
                        if _old_pdf and _old_pdf != pdf_out_path and os.path.exists(_old_pdf):
                            try:
                                os.remove(_old_pdf)
                            except OSError:
                                pass
                        st.session_state['pdf_out_path'] = pdf_out_path
                        st.session_state['pdf_input_sig'] = st.session_state.get('_birth_input_sig')
                        st.success(f" 56-पेज VYAS स्टैंडर्ड कुण्डली PDF सफलतापूर्वक तैयार हो गया है! (आकार: {os.path.getsize(pdf_out_path)/1024/1024:.2f} MB)")
                    else:
                        from vyas import chrome_runtime
                        _chrome = publication_engine.find_chrome()
                        _present = bool(_chrome) and os.path.exists(_chrome)
                        # Try to capture the real failure reason (missing shared lib,
                        # sandbox error, etc.) by invoking the binary once.
                        _diag = ""
                        try:
                            import subprocess as _sp
                            _r = _sp.run(
                                [_chrome, "--version"], capture_output=True, text=True, timeout=20
                            )
                            _diag = (_r.stderr or "") + (_r.stdout or "")
                        except Exception as _e:
                            _diag = repr(_e)
                        st.error(
                            "PDF तैयार नहीं हो सका — HTML→PDF engine (Chromium) चल नहीं पा रहा है।\n\n"
                            f"Resolved binary: `{_chrome}`  \n"
                            f"File मौजूद: **{'हाँ' if _present else 'नहीं'}**\n\n"
                            "**संभावित कारण:** Chromium को चलाने के लिए OS-level shared libraries "
                            "(libnss3, libatk, libgbm, libasound आदि) चाहिए होती हैं, जो Streamlit "
                            "Cloud base image में default नहीं होतीं।\n\n"
                            "**ठीक करने के लिए (कोई एक):**\n"
                            "1. Repo root mein `packages.txt` banayein jisme sirf `chromium` likha ho "
                            "(Streamlit Cloud apt se install karega; auto-download fallback bhi kaam karega), या\n"
                            "2. `CHROME_BIN` secret mein ek working browser ka full path dein, या\n"
                            "3. Local machine par Chrome install karke wahan PDF generate karein.\n\n"
                            "Note: ab app pure-Python fallback (xhtml2pdf) bhi try karta hai, isliye "
                            "Chrome na ho tab bhi PDF generate hona chahiye.\n\n"
                            "Last fallback error: " + repr(getattr(__builtins__, "_vyas_last_pdf_fallback_error", "n/a"))
                        )
                        with st.expander("तकनीकी विवरण (Debug)"):
                            st.code(
                                "find_chrome() -> " + repr(_chrome) + "\n"
                                + "exists        -> " + str(_present) + "\n"
                                + "chrome --version -> " + repr(_diag.strip()) + "\n"
                                + "platform      -> " + sys.platform + " / " + platform.machine() + "\n"
                                + "CHROME_BIN    -> " + repr(os.environ.get("CHROME_BIN")) + "\n"
                                + "VYAS_AUTO_CHROME -> " + repr(os.environ.get("VYAS_AUTO_CHROME")) + "\n"
                                + "cache dir     -> " + repr(os.environ.get("VYAS_CHROME_CACHE")) + "\n"
                                + "shutil.which(chromium) -> " + repr(shutil.which("chromium")) + "\n"
                                + "shutil.which(google-chrome) -> " + repr(shutil.which("google-chrome")) + "\n"
                                + "PATH (first 300) -> " + repr(os.environ.get("PATH", "")[:300]),
                                language="text",
                            )

        # Only offer the download when it was generated for the CURRENT inputs.
        _dl_path = st.session_state.get('pdf_out_path')
        _dl_ok = (
            _dl_path and os.path.exists(_dl_path)
            and st.session_state.get('pdf_input_sig') == st.session_state.get('_birth_input_sig')
        )
        if _dl_ok:
                pdf_out_path = _dl_path
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    with open(pdf_out_path, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        label=" PDF डाउनलोड (Local)",
                        data=pdf_bytes,
                        file_name=f"VYAS_Kundli_{birth.get('name', 'Native').replace(' ', '_')}_56_Pages_{selected_pdf_lang}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                with col_btn2:
                    if st.button(" Save to Google Drive", type="secondary", use_container_width=True):
                        u_curr = st.session_state.get("user", {})
                        u_toks = auth_vault.get_google_tokens(u_curr.get("id", 1))
                        active_tok = st.session_state.get("google_access_token") or (u_toks.get("access_token") if u_toks else None)
                        
                        if not active_tok:
                            auth_g_url = google_drive_sync.get_google_auth_url()
                            if auth_g_url:
                                st.warning("पहले Google से लॉगिन करें ताकि कुण्डली आपके Google Drive में सुरक्षित हो सके:")
                                st.markdown(f'<a href="{auth_g_url}" target="_top" rel="noopener"><button style="background: #ffffff; color: #3c4043; border: 1px solid #dadce0; border-radius: 6px; padding: 6px 12px; font-weight: 700; width: 100%; cursor: pointer;"> Connect Google Drive</button></a>', unsafe_allow_html=True)
                            else:
                                st.info("कृपया साइडबार के ' Google Cloud API Credentials' में अपनी Google Client ID दर्ज करें।")
                        else:
                            with st.spinner("Google Drive पर फ़ोल्डर 'VYAS Kundli & Horoscopes' में अपलोड किया जा रहा है..."):
                                f_display = f"VYAS_Kundli_{birth.get('name', 'Native').replace(' ', '_')}_56_Pages_{selected_pdf_lang}.pdf"
                                ok_up, msg_up, res_up = google_drive_sync.upload_pdf_to_google_drive(
                                    active_tok, pdf_out_path, file_display_name=f_display
                                )
                                # If token expired, try refresh
                                if not ok_up and u_toks and u_toks.get("refresh_token"):
                                    new_tok = google_drive_sync.refresh_access_token(u_toks["refresh_token"])
                                    if new_tok:
                                        auth_vault.save_google_tokens(u_curr["id"], new_tok)
                                        st.session_state["google_access_token"] = new_tok
                                        ok_up, msg_up, res_up = google_drive_sync.upload_pdf_to_google_drive(
                                            new_tok, pdf_out_path, file_display_name=f_display
                                        )
                                if ok_up and res_up:
                                    st.session_state["gdrive_last_link"] = res_up.get("web_view_link")
                                    st.toast("Google Drive पर सुरक्षित हो गया!", icon="")
                                    st.rerun()
                                else:
                                    st.error(f"Google Drive अपलोड विफल: {msg_up}")

                if st.session_state.get("gdrive_last_link"):
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; border-radius: 8px; padding: 10px 14px; margin-top: 10px; text-align: center;">
                        <div style="color: #6ee7b7; font-weight: 700; font-size: 0.95rem; margin-bottom: 4px;"> कुण्डली Google Drive पर सुरक्षित हो गई है!</div>
                        <a href="{st.session_state['gdrive_last_link']}" target="_blank" style="color: #f0c05a; font-weight: 800; text-decoration: underline; font-size: 0.95rem;">
                             Google Drive में खोलें (Open in Google Drive)
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

        if (not _dl_ok) and st.session_state.get('pdf_out_path') and os.path.exists(st.session_state['pdf_out_path']):
            st.caption("पिछली बार बना PDF अलग इनपुट का है — नया रिपोर्ट देखने के लिए ऊपर फिर से जनरेट करें।")

        with col_gen2:
            st.markdown("""
            <div class="glass-card">
                <div style="font-weight: bold; color: #f0c05a; font-size: 1.1rem;">56-पेज VYAS गोल्ड स्टैंडर्ड की प्रमुख सामग्री:</div>
                <ul style="color: #cbd5e1; font-size: 0.92rem; margin-top: 6px; line-height: 1.55;">
                    <li><b>पारंपरिक चक्र एवं ग्रह स्थिति:</b> अवकहड़ा चक्र, बेसिक विवरण, अनुकूल बिन्दु, घातक चक्र, पारंपरिक लग्न व नवमांश डायमंड चार्ट, चलित सारणी।</li>
                    <li><b>जीवन एवं ग्रह फलित:</b> लग्न फल, नक्षत्र फल, 4-पृष्ठ सम्पूर्ण जीवन फलित (चरित्र, करियर, आजीविका, स्वास्थ्य, वित्त, शिक्षा)।</li>
                    <li><b>दोष एवं दशा चक्र:</b> मंगल दोष विस्तृत विवेचन, साढ़े साती सम्पूर्ण 46-अवधि तालिका व फलित, कालसर्प योग, ताजिक वर्षफल (मुन्था व मुद्धा दशा), विंशोत्तरी महादशा फल, योगिनी दशा (36 वर्ष चक्र)।</li>
                    <li><b>जैमिनी, गोचर एवं लाल किताब:</b> जैमिनी कारकांश व स्वांश चार्ट, चर महादशा व 12 अंतर्दशाएं, आज का गोचर (Transit Today), लाल किताब 9 ग्रह फल व उपाय, 35-साला लाल किताब दशा।</li>
                    <li><b>सूक्ष्म गणित एवं वर्ग चक्र:</b> षोडशवर्ग सारणी व 16 वर्ग चक्र (D1-D60), केपी कस्प व कारकत्व, 60 अंतर्दशाओं की संपूर्ण विंशोत्तरी प्रत्यंतर सारणियां, पंचधा मैत्री, षड्बल व भावबल, पाश्चात्य दृष्टि चक्र (Western Aspects, भाव मध्य व केपी कस्प), अष्टकवर्ग व संपूर्ण 7-ग्रह प्रस्तराष्टकवर्ग।</li>
                    <li><b>सिस्टम प्रणेता:</b> निखिल व्यास (एम.ए. ज्योतिष) • 9414121172 • inikhilvyas@gmail.com</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================================
    #  ACHARYA VYAS LIVE VEDIC BOT POPUP MODAL (आचार्य व्यास AI ज्योतिषी)
    # =========================================================================
    @st.dialog(" आचार्य व्यास • प्रत्यक्ष वैदिक AI परामर्श (Live Consultation)", width="large")
    def show_acharya_consultation_dialog(ch, b_info, c_dasha, p_meta):
        # Header profile card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(240, 192, 90, 0.2) 0%, rgba(14, 23, 42, 0.95) 100%);
                    border: 1px solid rgba(240, 192, 90, 0.5); border-radius: 14px; padding: 12px 18px; margin-bottom: 12px; display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 2.2rem; background: rgba(240,192,90,0.15); border: 2px solid #f0c05a; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(240,192,90,0.3); color: #f0c05a; font-weight: bold;">
                ॐ
            </div>
            <div style="flex-grow: 1;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #f0c05a; display: flex; align-items: center; gap: 8px;">
                    आचार्य व्यास <span style="font-size: 0.75rem; background: #166534; color: #bbf7d0; padding: 2px 8px; border-radius: 12px; font-weight: 600;">ऑनलाइन उपस्थित</span>
                </div>
                <div style="font-size: 0.85rem; color: #e2e8f0; margin-top: 2px;">
                    <b>{constants.SIGNS_HI[ch.ascendant_sign]} लग्न</b>, <b>{constants.SIGNS_HI[ch.planets['Moon'].sign_index]} राशि</b>
                </div>
                <div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 2px;">
                    महर्षि पाराशर, भृगु एवं जैमिनी ज्योतिष सिद्धांतों पर आधारित प्रामाणिक संवाद
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Calculate native age for Desh, Kaal & Paristhiti context
        birth_dt_obj = b_info.get('local')
        age_val = None
        if isinstance(birth_dt_obj, datetime):
            age_val = datetime.now().year - birth_dt_obj.year
        else:
            try:
                dt_raw = str(b_info.get('dt', ''))
                age_val = datetime.now().year - int(dt_raw.split('-')[0])
            except Exception:
                age_val = 32

        if age_val is None or age_val <= 0:
            age_val = 32

        # Life-Stage appropriate Normal & Dignified Consultation Queries (देश, काल, परिस्थिति)
        if age_val >= 55:
            # Senior / Elder stage (55+ years)
            suggested_queries = [
                "स्वास्थ्य रक्षा, दीर्घायु एवं शारीरिक कल्याण के क्या संकेत हैं?",
                "पारिवारिक सुख, शांति एवं संतान की प्रगति कैसी रहेगी?",
                "आर्थिक स्थिति, संचय एवं संपत्ति संरक्षण का समय कैसा है?",
                "आध्यात्मिक उन्नति, मानसिक शांति व साधना हेतु मार्गदर्शन दें।",
                "दैनिक जीवन में सकारात्मक ऊर्जा हेतु कौन से सात्विक उपाय करें?"
            ]
            welcome_msg = (
                f"सादर प्रणाम {b_info.get('name', 'जातक')} जी।\n\n"
                f"मैं **आचार्य व्यास** हूँ। आपकी जन्म कुण्डली मेरे समक्ष खुली है। "
                f"आप स्वास्थ्य रक्षा, पारिवारिक सुख-शांति, संतान की उन्नति, आर्थिक संचय अथवा आध्यात्मिक साधना के विषय में सीधे प्रश्न पूछ सकते हैं।"
            )
        elif age_val >= 32:
            # Mature adult stage (32-54 years)
            suggested_queries = [
                "कार्यक्षेत्र, व्यवसाय एवं आजीविका में प्रगति के क्या योग हैं?",
                "आर्थिक स्थिति, धन संचय एवं निवेश के अवसर कैसे रहेंगे?",
                "दांपत्य जीवन, गृहस्थ सुख एवं पारिवारिक सामंजस्य कैसा रहेगा?",
                "संतान पक्ष, विद्या एवं पारिवारिक दायित्वों की क्या स्थिति है?",
                "स्वास्थ्य रक्षा एवं मानसिक शांति हेतु कौन से सात्विक उपाय करें?"
            ]
            welcome_msg = (
                f"सादर प्रणाम {b_info.get('name', 'जातक')} जी।\n\n"
                f"मैं **आचार्य व्यास** हूँ। आपकी जन्म कुण्डली मेरे समक्ष खुली है। "
                f"आप कार्यक्षेत्र, पदोन्नति, आर्थिक स्थिति, दांपत्य जीवन, संतान अथवा स्वास्थ्य के विषय में सीधे प्रश्न पूछ सकते हैं।"
            )
        elif age_val >= 18:
            # Youth / Career Entry stage (18-31 years)
            suggested_queries = [
                "करियर, रोजगार एवं आजीविका के क्या योग हैं?",
                "उच्च शिक्षा, कौशल विकास एवं कार्यक्षेत्र में सफलता की संभावना?",
                "आर्थिक स्थिति एवं भविष्य के विकास के अवसर कैसे रहेंगे?",
                "विवाह एवं व्यक्तिगत जीवन के ग्रह क्या संकेत दे रहे हैं?",
                "एकाग्रता, स्वास्थ्य एवं सफलता हेतु कौन से सात्विक उपाय करें?"
            ]
            welcome_msg = (
                f"सादर प्रणाम {b_info.get('name', 'जातक')} जी।\n\n"
                f"मैं **आचार्य व्यास** हूँ। आपकी जन्म कुण्डली मेरे समक्ष खुली है। "
                f"आप करियर, उच्च शिक्षा, आजीविका, विवाह अथवा भविष्य की दिशा के विषय में सीधे प्रश्न पूछ सकते हैं।"
            )
        else:
            # Student / Child stage (< 18 years)
            suggested_queries = [
                "विद्या, एकाग्रता एवं शैक्षणिक उन्नति के क्या योग हैं?",
                "स्वास्थ्य, मानसिक ऊर्जा एवं शारीरिक विकास की स्थिति कैसी है?",
                "भविष्य की अनुकूल दिशा एवं स्वाभाविक प्रतिभा क्या है?",
                "विद्या वृद्धि एवं कल्याण हेतु कौन से सात्विक उपाय करें?"
            ]
            welcome_msg = (
                f"स्नेह व शुभाशीर्वाद {b_info.get('name', 'जातक')}।\n\n"
                f"मैं **आचार्य व्यास** हूँ। आपकी जन्म कुण्डली मेरे समक्ष खुली है। "
                f"आप विद्या, एकाग्रता, प्रतिभा एवं स्वास्थ्य के विषय में सीधे प्रश्न पूछ सकते हैं।"
            )

        # Quick chips inside popup
        st.markdown("<div style='font-size: 1.02rem; color: #f0c05a; font-weight: 700; margin-bottom: 8px;'>त्वरित शास्त्रीय प्रश्न (Quick Consultation):</div>", unsafe_allow_html=True)
        
        chip_col1, chip_col2 = st.columns(2)
        chosen_chip = None
        for i, q_chip in enumerate(suggested_queries):
            target_col = chip_col1 if i % 2 == 0 else chip_col2
            with target_col:
                if st.button(q_chip, key=f"dialog_chip_{i}", use_container_width=True):
                    chosen_chip = q_chip

        # Initialize session state for dialog chat history
        if "dialog_chat_history" not in st.session_state or not st.session_state["dialog_chat_history"]:
            st.session_state["dialog_chat_history"] = [
                {
                    "role": "assistant",
                    "content": welcome_msg
                }
            ]

        # Spacious chat message log container
        chat_container = st.container(height=440)
        with chat_container:
            for msg in st.session_state["dialog_chat_history"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Chat Input inside popup
        dialog_user_input = st.chat_input("आचार्य व्यास जी से अपना प्रश्न यहाँ पूछें...")
        if chosen_chip:
            dialog_user_input = chosen_chip

        if dialog_user_input:
            st.session_state["dialog_chat_history"].append({"role": "user", "content": dialog_user_input})
            try:
                cur_raw_pos = _cached_transit_positions(datetime.now().strftime("%Y-%m-%d"))
            except Exception:
                cur_raw_pos = None

            bot_reply = vyas_chatbot.consult(
                query=dialog_user_input,
                chart=ch,
                cur_dasha=c_dasha,
                birth_info=b_info,
                transit_pos=cur_raw_pos,
                prashna_meta=p_meta,
                chat_history=st.session_state["dialog_chat_history"]
            )
            st.session_state["dialog_chat_history"].append({"role": "assistant", "content": bot_reply})
            st.session_state["show_acharya_dialog"] = True
            st.rerun()

        col_act1, col_act2 = st.columns([4, 1])
        with col_act2:
            if st.button(" साफ करें", key="clear_dialog_chat_btn", use_container_width=True):
                st.session_state["dialog_chat_history"] = []
                st.rerun()

    # Trigger Dialog if requested (one-shot: clear the flag after opening, else
    # the next rerun re-opens the popup even after the user closed it).
    if st.session_state.get("show_acharya_dialog"):
        st.session_state["show_acharya_dialog"] = False
        show_acharya_consultation_dialog(chart, birth, cur_dasha, st.session_state.get('prashna_meta'))

    # Acharya Vyas Live Consultation is readily launched via top bar & sidebar

    with st.sidebar:
        st.markdown("---")
        if st.button("आचार्य व्यास जी से परामर्श करें (Live Consultation)", key="open_acharya_bot_sidebar_btn", use_container_width=True):
            st.session_state["show_acharya_dialog"] = True
            st.rerun()

# ---------------- SCRIPT TIMING (opt-in) ----------------
# Set VYAS_SHOW_TIMING=1 (env var or secret) to see how long this rerun took.
# Useful for verifying that cached engines and lazy sections really are skipping
# work: an unchanged rerun should be well under a second.
import time as _time_mod

def _timing_enabled() -> bool:
    raw = os.environ.get("VYAS_SHOW_TIMING", "")
    if str(raw).strip() not in ("", "0", "false", "False"):
        return True
    try:
        return bool(st.secrets.get("VYAS_SHOW_TIMING", False))
    except Exception:
        return False

if _timing_enabled():
    if "_vyas_script_start" in st.session_state:
        _elapsed = _time_mod.perf_counter() - st.session_state["_vyas_script_start"]
        with st.sidebar:
            st.caption(f" Rerun: {_elapsed * 1000:.0f} ms")

st.session_state["_vyas_script_start"] = _time_mod.perf_counter()


# Main Page Bottom Footer
st.markdown("""
<footer style="text-align: center; margin-top: 45px; padding: 22px 10px; border-top: 1px solid rgba(240, 192, 90, 0.22); font-size: 0.85rem; color: #94a3b8; line-height: 1.7;">
    <b>VYAS ASTRA</b> &bull; Vedic Yield Astrology Systems &bull; High-Precision Astronomical Intelligence<br/>
    वेबसाइट निर्माण एवं शोधकर्ता: <b style="color: #f0c05a;">निखिल व्यास (Nikhil Vyas)</b> &bull; 
     <a href="mailto:inikhilvyas@gmail.com" style="color: #93c5fd; text-decoration: none;">inikhilvyas@gmail.com</a> &bull; 
     <a href="tel:+919414121172" style="color: #93c5fd; text-decoration: none;">+91 94141 21172</a>
</footer>
""", unsafe_allow_html=True)
