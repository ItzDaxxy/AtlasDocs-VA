"""
Tests for api_keys.py - API key management.

Run with: pytest tests/test_api_keys.py -v
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from api_keys import (
    get_api_key,
    save_api_key,
    delete_api_key,
    detect_provider_from_key,
    is_keyring_available,
    _get_key_for_provider,
    SERVICE_NAME,
)


class TestDetectProviderFromKey:
    """Tests for API key provider detection."""
    
    def test_detect_anthropic_key(self):
        assert detect_provider_from_key("sk-ant-abc123") == "anthropic"
        assert detect_provider_from_key("sk-ant-api03-xyz789") == "anthropic"
    
    def test_detect_openai_key(self):
        assert detect_provider_from_key("sk-abc123xyz") == "openai"
        assert detect_provider_from_key("sk-proj-abc123") == "openai"
    
    def test_unknown_key_format(self):
        assert detect_provider_from_key("unknown-key-format") is None
        assert detect_provider_from_key("api-key-12345") is None
        assert detect_provider_from_key("") is None


class TestGetApiKeyFromEnv:
    """Tests for getting API keys from environment variables."""
    
    def test_get_anthropic_key_from_env(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test123"}):
            with patch("api_keys.KEYRING_AVAILABLE", False):
                key, provider = get_api_key("anthropic")
                assert key == "sk-ant-test123"
                assert provider == "anthropic"
    
    def test_get_openai_key_from_env(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test456"}):
            with patch("api_keys.KEYRING_AVAILABLE", False):
                key, provider = get_api_key("openai")
                assert key == "sk-test456"
                assert provider == "openai"
    
    def test_get_any_key_tries_anthropic_first(self):
        with patch.dict(os.environ, {
            "ANTHROPIC_API_KEY": "sk-ant-first",
            "OPENAI_API_KEY": "sk-second"
        }):
            with patch("api_keys.KEYRING_AVAILABLE", False):
                key, provider = get_api_key(None)
                assert key == "sk-ant-first"
                assert provider == "anthropic"
    
    def test_get_any_key_falls_back_to_openai(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-fallback"}, clear=False):
            # Remove ANTHROPIC key if present
            env = os.environ.copy()
            env.pop("ANTHROPIC_API_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                with patch("api_keys.KEYRING_AVAILABLE", False):
                    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-fallback"}):
                        key, provider = get_api_key(None)
                        if key:
                            assert provider == "openai"
    
    def test_no_key_returns_none(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("api_keys.KEYRING_AVAILABLE", False):
                key, provider = get_api_key("anthropic")
                assert key is None
                assert provider is None


class TestKeyringIntegration:
    """Tests for keyring-based storage (mocked)."""
    
    @pytest.fixture
    def mock_keyring_module(self):
        """Create a mock keyring module and inject it into api_keys."""
        import api_keys
        mock_keyring = MagicMock()
        # Store original state
        orig_available = api_keys.KEYRING_AVAILABLE
        orig_keyring = getattr(api_keys, 'keyring', None)
        # Inject mock
        api_keys.keyring = mock_keyring
        api_keys.KEYRING_AVAILABLE = True
        yield mock_keyring
        # Restore original state
        api_keys.KEYRING_AVAILABLE = orig_available
        if orig_keyring:
            api_keys.keyring = orig_keyring
        elif hasattr(api_keys, 'keyring'):
            delattr(api_keys, 'keyring')
    
    def test_get_key_from_keyring(self, mock_keyring_module):
        mock_keyring_module.get_password.return_value = "sk-ant-keyring-key"
        
        key, provider = get_api_key("anthropic")
        
        mock_keyring_module.get_password.assert_called_with(SERVICE_NAME, "anthropic_api_key")
        assert key == "sk-ant-keyring-key"
        assert provider == "anthropic"
    
    def test_keyring_fallback_to_env(self, mock_keyring_module):
        mock_keyring_module.get_password.return_value = None  # Keyring returns nothing
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-env-fallback"}):
            key, provider = get_api_key("anthropic")
            
            assert key == "sk-ant-env-fallback"
            assert provider == "anthropic"
    
    def test_save_key_to_keyring(self, mock_keyring_module):
        result = save_api_key("anthropic", "sk-ant-new-key")
        
        mock_keyring_module.set_password.assert_called_with(
            SERVICE_NAME, "anthropic_api_key", "sk-ant-new-key"
        )
        assert result is True
    
    def test_save_key_fails_without_keyring(self):
        with patch("api_keys.KEYRING_AVAILABLE", False):
            result = save_api_key("anthropic", "sk-ant-test")
            assert result is False
    
    def test_delete_key_from_keyring(self, mock_keyring_module):
        result = delete_api_key("openai")
        
        mock_keyring_module.delete_password.assert_called_with(
            SERVICE_NAME, "openai_api_key"
        )
        assert result is True
    
    def test_delete_key_fails_without_keyring(self):
        with patch("api_keys.KEYRING_AVAILABLE", False):
            result = delete_api_key("openai")
            assert result is False
    
    def test_keyring_exception_handled(self, mock_keyring_module):
        mock_keyring_module.get_password.side_effect = Exception("Keyring error")
        
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-backup"}):
            key, provider = get_api_key("anthropic")
            # Should fall back to env var
            assert key == "sk-ant-backup"


class TestIsKeyringAvailable:
    """Tests for keyring availability check."""
    
    def test_keyring_available_when_imported(self):
        with patch("api_keys.KEYRING_AVAILABLE", True):
            assert is_keyring_available() is True
    
    def test_keyring_unavailable_when_not_imported(self):
        with patch("api_keys.KEYRING_AVAILABLE", False):
            assert is_keyring_available() is False


class TestServiceName:
    """Tests for service name constant."""
    
    def test_service_name_is_damgood(self):
        assert SERVICE_NAME == "damgood"
