"""Application-owned secrets in the native OS credential store. Secret values never leave this module's callers."""
import sys
import threading

SERVICE = "com.hy1990.henge"
LEGACY_SERVICE = "com.hy1990.genjustsu-pro"
PROVIDERS = ("dreamapi", "replicate")
_lock = threading.RLock()


def _backend():
    if sys.platform == "darwin":
        from keyring.backends.macOS import Keyring
        return Keyring()
    if sys.platform == "win32":
        from keyring.backends.Windows import WinVaultKeyring
        return WinVaultKeyring()
    raise RuntimeError("Supported credential stores: macOS Keychain and Windows Credential Manager.")


def get_key(provider):
    if provider not in PROVIDERS:
        raise ValueError("Unknown provider")
    with _lock:
        backend = _backend()
        current = backend.get_password(SERVICE, provider)
        if current:
            return current
        legacy = backend.get_password(LEGACY_SERVICE, provider)
        if legacy:
            backend.set_password(SERVICE, provider, legacy)
        return legacy or ""


def save_key(provider, value):
    if provider not in PROVIDERS:
        raise ValueError("Unknown provider")
    value = value.strip()
    if not value or len(value) > 4096 or any(char.isspace() for char in value):
        raise ValueError("Invalid API key")
    with _lock:
        _backend().set_password(SERVICE, provider, value)


def delete_key(provider):
    if provider not in PROVIDERS:
        raise ValueError("Unknown provider")
    from keyring.errors import PasswordDeleteError
    with _lock:
        backend = _backend()
        # Remove both entries so a deleted key cannot reappear through migration.
        for service in (SERVICE, LEGACY_SERVICE):
            try:
                backend.delete_password(service, provider)
            except PasswordDeleteError:
                pass


def key_status():
    return {provider: bool(get_key(provider)) for provider in PROVIDERS}
