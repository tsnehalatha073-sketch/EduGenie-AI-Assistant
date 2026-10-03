"""
EduGenie - Gemini configuration.
Auto-detects a working model. Never raises. Falls back to Demo Mode.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip().strip('"').strip("'")
REQUESTED_MODEL = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()

_PLACEHOLDERS = (
    "",
    "paste_your_key_here",
    "paste_your_gemini_api_key_here",
    "your-gemini-api-key-here",
    "your_api_key",
)

_CANDIDATES = [
    REQUESTED_MODEL,
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
]

_demo_mode = GOOGLE_API_KEY.lower() in _PLACEHOLDERS
_active_model = None
_available = []
_genai = None
_cache = {}


def _init():
    global _demo_mode, _active_model, _available, _genai

    if _demo_mode:
        print("[EduGenie] No API key found -> DEMO MODE")
        return

    try:
        import google.generativeai as genai
    except ImportError:
        print("[EduGenie] google-generativeai not installed -> DEMO MODE")
        print("[EduGenie] Fix: pip install google-generativeai")
        _demo_mode = True
        return

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        _genai = genai
    except Exception as exc:
        print("[EduGenie] configure() failed:", exc, "-> DEMO MODE")
        _demo_mode = True
        return

    try:
        for m in genai.list_models():
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                _available.append(m.name.replace("models/", ""))
    except Exception as exc:
        print("[EduGenie] Could not list models:", exc)

    for cand in _CANDIDATES:
        if not cand:
            continue
        clean = cand.replace("models/", "").strip()
        if not _available or clean in _available:
            _active_model = clean
            break

    if _active_model is None and _available:
        flash = [m for m in _available if "flash" in m and "thinking" not in m]
        _active_model = flash[0] if flash else _available[0]

    if _active_model is None:
        print("[EduGenie] No usable model -> DEMO MODE")
        _demo_mode = True
        return

    print("[EduGenie] Gemini ready. Model:", _active_model)


_init()


def is_demo():
    return _demo_mode or _active_model is None


def get_active_model():
    return _active_model


def _model_obj(name):
    if name not in _cache:
        _cache[name] = _genai.GenerativeModel(model_name=name)
    return _cache[name]


def extract_text(response):
    try:
        txt = getattr(response, "text", None)
        if txt and txt.strip():
            return txt.strip()
    except Exception:
        pass
    try:
        for cand in getattr(response, "candidates", []) or []:
            content = getattr(cand, "content", None)
            for part in getattr(content, "parts", []) or []:
                t = getattr(part, "text", None)
                if t and t.strip():
                    return t.strip()
    except Exception:
        pass
    return ""


def generate_text(prompt, temperature=0.7, max_tokens=2048):
    """Returns generated text, or empty string if unavailable."""
    if is_demo():
        return ""

    order = [_active_model]
    for c in _CANDIDATES:
        if not c:
            continue
        clean = c.replace("models/", "").strip()
        if clean != _active_model and clean not in order:
            order.append(clean)

    last_error = "unknown"
    for name in order:
        if _available and name not in _available:
            continue
        try:
            model = _model_obj(name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            text = extract_text(response)
            if text:
                return text
            last_error = "empty response"
        except Exception as exc:
            last_error = str(exc)
            continue

    print("[EduGenie] Generation failed:", last_error)
    return ""


def status():
    return {
        "demo_mode": is_demo(),
        "active_model": _active_model,
        "requested_model": REQUESTED_MODEL,
        "available_models": _available[:25],
    }