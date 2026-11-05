"""VYAS Enterprise Multi-Key AI Pool & Auto-Failover Orchestrator.

Key Capabilities:
1. Multi-Key Backup Pool (Auto-Failover):
   Rotates through multiple backup API keys if a primary key hits rate limits (HTTP 429),
   quota exhaustion, or network timeout.
2. Calculation / Task Specific Segregation:
   Allows different keys for different astrological computations:
   - 'chat': Interactive live consultation with Acharya Vyas (Groq LPU / Gemini)
   - 'report': 56-page deep publication synthesis (Gemini Pro / Flash)
   - 'daily': Daily horoscope, transit & Gochar synthesis
   - 'prashna': Horary and compatibility judgement
3. Safe Secret Discovery:
   Seamlessly checks Streamlit Cloud Secrets (st.secrets), environment variables (os.environ),
   and local config with zero leaks to git.
"""
from typing import List, Optional, Dict, Set
import os
import time

# In-memory tracking of temporarily exhausted keys (key -> timestamp until backed off)
_EXHAUSTED_KEY_COOLDOWNS: Dict[str, float] = {}
_COOLDOWN_DURATION_SEC = 60.0  # 60s cooldown for rate-limited keys before retry


def _clean_key(k: Optional[str]) -> Optional[str]:
    if not k or not isinstance(k, str):
        return None
    k_clean = k.strip().strip("'\"")
    return k_clean if len(k_clean) > 8 else None


def _extract_from_secrets(secret_name: str) -> List[str]:
    """Safely extracts one or multiple keys from streamlit secrets."""
    results = []
    try:
        import streamlit as st
        val = st.secrets.get(secret_name)
        if val:
            if isinstance(val, (list, tuple)):
                for item in val:
                    ck = _clean_key(str(item))
                    if ck:
                        results.append(ck)
            elif isinstance(val, str):
                for part in val.replace("\n", ",").split(","):
                    ck = _clean_key(part)
                    if ck:
                        results.append(ck)
    except Exception:
        pass
    return results


def _extract_from_env(env_name: str) -> List[str]:
    """Safely extracts one or multiple keys from environment variables."""
    results = []
    val = os.environ.get(env_name)
    if val:
        for part in val.replace("\n", ",").split(","):
            ck = _clean_key(part)
            if ck:
                results.append(ck)
    return results


def get_groq_key_pool(task: str = "chat") -> List[str]:
    """
    Returns an ordered, deduplicated pool of Groq API keys.
    Priority:
    1. Dedicated task key (e.g., CHAT_GROQ_API_KEY, REPORT_GROQ_API_KEY)
    2. Primary GROQ_API_KEY
    3. Multi-key pool GROQ_API_KEYS (comma-separated)
    4. Backup numbered keys: GROQ_API_KEY_1 .. GROQ_API_KEY_5, GROQ_BACKUP_KEY
    """
    candidates: List[str] = []
    task_upper = (task or "chat").upper()

    # 1. Dedicated task key
    candidates.extend(_extract_from_secrets(f"{task_upper}_GROQ_API_KEY"))
    candidates.extend(_extract_from_env(f"{task_upper}_GROQ_API_KEY"))

    # 2. Primary key
    candidates.extend(_extract_from_secrets("GROQ_API_KEY"))
    candidates.extend(_extract_from_env("GROQ_API_KEY"))

    # 3. Comma-separated pool
    candidates.extend(_extract_from_secrets("GROQ_API_KEYS"))
    candidates.extend(_extract_from_env("GROQ_API_KEYS"))

    # 4. Numbered backups (1 to 5) + GROQ_BACKUP_KEY
    for idx in range(1, 6):
        candidates.extend(_extract_from_secrets(f"GROQ_API_KEY_{idx}"))
        candidates.extend(_extract_from_env(f"GROQ_API_KEY_{idx}"))
    candidates.extend(_extract_from_secrets("GROQ_BACKUP_KEY"))
    candidates.extend(_extract_from_env("GROQ_BACKUP_KEY"))

    # Deduplicate while preserving order
    seen: Set[str] = set()
    pool: List[str] = []
    for k in candidates:
        if k and k not in seen:
            seen.add(k)
            pool.append(k)

    # Sort so that non-cooldown keys come first
    now = time.time()
    healthy_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) < now]
    cooldown_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) >= now]

    return healthy_keys + cooldown_keys


def get_gemini_key_pool(task: str = "chat") -> List[str]:
    """
    Returns an ordered, deduplicated pool of Google Gemini API keys.
    Priority:
    1. Dedicated task key (e.g., REPORT_GEMINI_API_KEY, CHAT_GEMINI_API_KEY)
    2. Primary GEMINI_API_KEY / GOOGLE_API_KEY
    3. Multi-key pool GEMINI_API_KEYS (comma-separated)
    4. Backup numbered keys: GEMINI_API_KEY_1 .. GEMINI_API_KEY_5, GOOGLE_API_KEY_1..3
    """
    candidates: List[str] = []
    task_upper = (task or "chat").upper()

    # 1. Dedicated task key
    candidates.extend(_extract_from_secrets(f"{task_upper}_GEMINI_API_KEY"))
    candidates.extend(_extract_from_env(f"{task_upper}_GEMINI_API_KEY"))

    # 2. Primary keys
    candidates.extend(_extract_from_secrets("GEMINI_API_KEY"))
    candidates.extend(_extract_from_secrets("GOOGLE_API_KEY"))
    candidates.extend(_extract_from_env("GEMINI_API_KEY"))
    candidates.extend(_extract_from_env("GOOGLE_API_KEY"))

    # 3. Comma-separated pool
    candidates.extend(_extract_from_secrets("GEMINI_API_KEYS"))
    candidates.extend(_extract_from_env("GEMINI_API_KEYS"))

    # 4. Numbered backups (1 to 5)
    for idx in range(1, 6):
        candidates.extend(_extract_from_secrets(f"GEMINI_API_KEY_{idx}"))
        candidates.extend(_extract_from_env(f"GEMINI_API_KEY_{idx}"))
        candidates.extend(_extract_from_secrets(f"GOOGLE_API_KEY_{idx}"))
        candidates.extend(_extract_from_env(f"GOOGLE_API_KEY_{idx}"))

    # Deduplicate while preserving order
    seen: Set[str] = set()
    pool: List[str] = []
    for k in candidates:
        if k and k not in seen:
            seen.add(k)
            pool.append(k)

    # Sort so that non-cooldown keys come first
    now = time.time()
    healthy_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) < now]
    cooldown_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) >= now]

    return healthy_keys + cooldown_keys


def mark_key_rate_limited(api_key: str, cooldown_sec: float = _COOLDOWN_DURATION_SEC) -> None:
    """Marks a key as temporarily exhausted due to HTTP 429 or quota limit."""
    if api_key:
        _EXHAUSTED_KEY_COOLDOWNS[api_key] = time.time() + cooldown_sec


def mark_key_healthy(api_key: str) -> None:
    """Removes a key from cooldown when it successfully serves a request."""
    if api_key in _EXHAUSTED_KEY_COOLDOWNS:
        _EXHAUSTED_KEY_COOLDOWNS.pop(api_key, None)
