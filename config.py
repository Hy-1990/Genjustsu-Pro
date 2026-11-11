"""Non-secret defaults and macOS Keychain access."""
from pathlib import Path
from credential_store import get_key

ROOT = Path(__file__).resolve().parent


def setting(name, default=""):
    if name == "REPLICATE_API_TOKEN":
        return get_key("replicate")
    if name == "DREAMAPI_API_KEY":
        return get_key("dreamapi")
    return default


def credential(name):
    value = setting(name)
    if not value:
        raise ValueError("missing_" + name.lower())
    return value
