"""VYAS Enterprise Multi-Key AI Pool & Auto-Failover Orchestrator.

Key Capabilities:
1. Multi-Provider AI Model Support:
   - Groq (Llama-3.3, Qwen-2.5/3.8, GPT-OSS)
   - Google Gemini (Gemini 3.8 Flash, Gemini 2.5 Pro)
   - OpenAI (GPT-4o, GPT-4o-mini)
   - DeepSeek (DeepSeek-V3, DeepSeek-R1)
   - OpenRouter (Unified router for 200+ models)
   - Anthropic Claude (Claude 3.5 Sonnet, Haiku)
2. Multi-Key Backup Pool (Auto-Failover):
   Rotates through multiple backup API keys if a primary key hits rate limits (HTTP 429),
   quota exhaustion, or network timeout.
3. Calculation / Task Specific Segregation:
   Allows different keys for different astrological computations:
   - 'chat': Interactive live consultation with Acharya Vyas
   - 'report': 56-page deep publication synthesis
   - 'daily': Daily horoscope, transit & Gochar synthesis
4. Safe Secret Discovery:
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


def _get_provider_key_pool(provider_prefix: str, task: str = "chat", extra_names: Optional[List[str]] = None) -> List[str]:
    """
    Generic discovery for any LLM provider key pool with task-priority, backup numbered keys,
    and automatic failover tracking.
    """
    candidates: List[str] = []
    task_upper = (task or "chat").upper()
    prefix = provider_prefix.upper()

    # 1. Dedicated task key (e.g. CHAT_OPENAI_API_KEY)
    candidates.extend(_extract_from_secrets(f"{task_upper}_{prefix}_API_KEY"))
    candidates.extend(_extract_from_env(f"{task_upper}_{prefix}_API_KEY"))

    # 2. Primary key (e.g. OPENAI_API_KEY)
    candidates.extend(_extract_from_secrets(f"{prefix}_API_KEY"))
    candidates.extend(_extract_from_env(f"{prefix}_API_KEY"))

    # 2b. Extra aliases (e.g. GOOGLE_API_KEY for Gemini, CLAUDE_API_KEY for Anthropic)
    if extra_names:
        for en in extra_names:
            candidates.extend(_extract_from_secrets(en))
            candidates.extend(_extract_from_env(en))

    # 3. Comma-separated pool (e.g. OPENAI_API_KEYS)
    candidates.extend(_extract_from_secrets(f"{prefix}_API_KEYS"))
    candidates.extend(_extract_from_env(f"{prefix}_API_KEYS"))

    # 4. Numbered backups (1 to 5) + BACKUP_KEY
    for idx in range(1, 6):
        candidates.extend(_extract_from_secrets(f"{prefix}_API_KEY_{idx}"))
        candidates.extend(_extract_from_env(f"{prefix}_API_KEY_{idx}"))
    candidates.extend(_extract_from_secrets(f"{prefix}_BACKUP_KEY"))
    candidates.extend(_extract_from_env(f"{prefix}_BACKUP_KEY"))

    # Deduplicate while preserving priority order
    seen: Set[str] = set()
    pool: List[str] = []
    for k in candidates:
        if k and k not in seen:
            seen.add(k)
            pool.append(k)

    # Sort so healthy non-cooldown keys come first
    now = time.time()
    healthy_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) < now]
    cooldown_keys = [k for k in pool if _EXHAUSTED_KEY_COOLDOWNS.get(k, 0) >= now]

    return healthy_keys + cooldown_keys


def get_groq_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of Groq API keys."""
    return _get_provider_key_pool("GROQ", task)


def get_gemini_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of Google Gemini API keys."""
    return _get_provider_key_pool("GEMINI", task, extra_names=["GOOGLE_API_KEY", "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2"])


def get_openai_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of OpenAI API keys."""
    return _get_provider_key_pool("OPENAI", task)


def get_deepseek_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of DeepSeek API keys."""
    return _get_provider_key_pool("DEEPSEEK", task)


def get_openrouter_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of OpenRouter API keys."""
    return _get_provider_key_pool("OPENROUTER", task)


def get_anthropic_key_pool(task: str = "chat") -> List[str]:
    """Returns an ordered, deduplicated pool of Anthropic Claude API keys."""
    return _get_provider_key_pool("ANTHROPIC", task, extra_names=["CLAUDE_API_KEY", "CLAUDE_API_KEY_1"])


def mark_key_rate_limited(api_key: str, cooldown_sec: float = _COOLDOWN_DURATION_SEC) -> None:
    """Marks a key as temporarily exhausted due to HTTP 429 or quota limit."""
    if api_key:
        _EXHAUSTED_KEY_COOLDOWNS[api_key] = time.time() + cooldown_sec


def mark_key_healthy(api_key: str) -> None:
    """Removes a key from cooldown when it successfully serves a request."""
    if api_key in _EXHAUSTED_KEY_COOLDOWNS:
        _EXHAUSTED_KEY_COOLDOWNS.pop(api_key, None)
