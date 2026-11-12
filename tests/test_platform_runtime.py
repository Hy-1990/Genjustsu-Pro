"""OS routing contracts; no real credentials or cloud calls."""
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import credential_store
import platform_runtime


class PlatformRuntimeTests(unittest.TestCase):
    def test_windows_uses_native_vault_for_save_read_delete(self):
        values = {}
        vault = Mock()
        vault.set_password.side_effect = lambda service, provider, value: values.update({(service, provider): value})
        vault.get_password.side_effect = lambda service, provider: values.get((service, provider))
        vault.delete_password.side_effect = lambda service, provider: values.pop((service, provider))
        module = types.ModuleType('keyring.backends.Windows')
        module.WinVaultKeyring = Mock(return_value=vault)
        with patch.object(sys, 'platform', 'win32'), patch.dict(sys.modules, {'keyring.backends.Windows': module}):
            credential_store.save_key('dreamapi', ' dummy-token ')
            credential_store.save_key('replicate', ' other-token ')
            self.assertEqual(credential_store.get_key('dreamapi'), 'dummy-token')
            self.assertEqual(credential_store.key_status(), {'dreamapi': True, 'replicate': True})
            credential_store.delete_key('dreamapi')
            self.assertEqual(credential_store.get_key('dreamapi'), '')
            self.assertEqual(credential_store.get_key('replicate'), 'other-token')

    def test_real_native_backend_can_be_loaded_without_reading_keys(self):
        if sys.platform not in ("darwin", "win32"):
            self.skipTest("Native desktop OS required")
        backend = credential_store._backend()
        self.assertGreater(backend.priority, 0)
        expected = "keyring.backends.Windows" if sys.platform == "win32" else "keyring.backends.macOS"
        self.assertEqual(type(backend).__module__, expected)

    def test_mac_backend_retained(self):
        module = types.ModuleType('keyring.backends.macOS')
        module.Keyring = Mock()
        with patch.object(sys, 'platform', 'darwin'), patch.dict(sys.modules, {'keyring.backends.macOS': module}):
            self.assertIs(credential_store._backend(), module.Keyring.return_value)

    def test_unsupported_system_has_no_plaintext_fallback(self):
        with patch.object(sys, 'platform', 'linux'):
            with self.assertRaises(RuntimeError):
                credential_store._backend()

    def test_windows_worker_path(self):
        # Swap the module's os reference so pathlib keeps the real host semantics.
        with patch.object(platform_runtime, 'os', types.SimpleNamespace(name='nt')):
            self.assertEqual(platform_runtime.venv_python(Path('worker')), Path('worker/Scripts/python.exe'))

    def test_windows_lock_uses_same_byte_for_acquire_and_release(self):
        module = types.ModuleType('msvcrt')
        module.LK_NBLCK, module.LK_UNLCK = 2, 0
        module.locking = Mock()
        with tempfile.TemporaryFile('a+b') as handle:
            handle.write(b'existing')
            with patch.object(platform_runtime, 'os', types.SimpleNamespace(name='nt')), patch.dict(sys.modules, {'msvcrt': module}):
                platform_runtime.lock_runtime(handle)
                self.assertEqual(handle.tell(), 0)
                platform_runtime.unlock_runtime(handle)
                self.assertEqual(handle.tell(), 0)
            self.assertEqual(module.locking.call_args_list[0].args, (handle.fileno(), 2, 1))
            self.assertEqual(module.locking.call_args_list[1].args, (handle.fileno(), 0, 1))

    def test_native_lock_excludes_another_handle_and_can_be_released(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'runtime.lock'
            with path.open('a+b') as first, path.open('a+b') as second:
                platform_runtime.lock_runtime(first)
                try:
                    with self.assertRaises(OSError):
                        platform_runtime.lock_runtime(second)
                finally:
                    platform_runtime.unlock_runtime(first)
                platform_runtime.lock_runtime(second)
                platform_runtime.unlock_runtime(second)


if __name__ == '__main__':
    unittest.main()
