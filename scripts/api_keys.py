"""
Secure API key management for DAMGood.

Uses keyring for cross-platform secure storage:
- macOS: Keychain
- Windows: Credential Locker
- Linux: Secret Service (GNOME Keyring, KWallet, etc.)

Falls back to environment variables if keyring is not available.
"""

import os

SERVICE_NAME = "damgood"

# Try to import keyring, but don't fail if not installed
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


def get_api_key(provider: str = None) -> tuple[str | None, str | None]:
    """
    Get API key for the specified provider.
    
    Args:
        provider: 'anthropic' or 'openai'. If None, tries both.
    
    Returns:
        Tuple of (api_key, provider) or (None, None) if not found.
    """
    providers = [provider] if provider else ["anthropic", "openai"]
    
    for p in providers:
        key = _get_key_for_provider(p)
        if key:
            return key, p
    
    return None, None


def _get_key_for_provider(provider: str) -> str | None:
    """Get API key for a specific provider, checking keyring then env."""
    env_var = f"{provider.upper()}_API_KEY"
    keyring_key = f"{provider}_api_key"
    
    # Try keyring first (most secure)
    if KEYRING_AVAILABLE:
        try:
            key = keyring.get_password(SERVICE_NAME, keyring_key)
            if key:
                return key
        except Exception:
            pass
    
    # Fall back to environment variable
    return os.environ.get(env_var)


def save_api_key(provider: str, api_key: str) -> bool:
    """
    Save API key to secure storage.
    
    Args:
        provider: 'anthropic' or 'openai'
        api_key: The API key to store
    
    Returns:
        True if saved successfully, False otherwise.
    """
    if not KEYRING_AVAILABLE:
        return False
    
    keyring_key = f"{provider}_api_key"
    
    try:
        keyring.set_password(SERVICE_NAME, keyring_key, api_key)
        return True
    except Exception:
        return False


def delete_api_key(provider: str) -> bool:
    """
    Delete API key from secure storage.
    
    Args:
        provider: 'anthropic' or 'openai'
    
    Returns:
        True if deleted successfully, False otherwise.
    """
    if not KEYRING_AVAILABLE:
        return False
    
    keyring_key = f"{provider}_api_key"
    
    try:
        keyring.delete_password(SERVICE_NAME, keyring_key)
        return True
    except Exception:
        return False


def detect_provider_from_key(api_key: str) -> str | None:
    """
    Detect provider based on API key format.
    
    Args:
        api_key: The API key to check
    
    Returns:
        'anthropic', 'openai', or None if unknown.
    """
    if api_key.startswith("sk-ant-"):
        return "anthropic"
    elif api_key.startswith("sk-"):
        return "openai"
    return None


def is_keyring_available() -> bool:
    """Check if keyring is available for secure storage."""
    return KEYRING_AVAILABLE
