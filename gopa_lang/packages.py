"""Package manager for Gopa."""

import os
import shutil
from pathlib import Path
from typing import Dict

try:
    import toml
except ImportError:
    toml = None


class PackageManager:
    """Manages Gopa packages."""

    def __init__(self, permissions, interpreter=None):
        self.permissions = permissions
        self.interpreter = interpreter
        self.packages_dir = Path.home() / '.gopa_packages'
        self.packages_dir.mkdir(exist_ok=True)
        self.loaded_packages: Dict[str, dict] = {}

    def install(self, package_name: str) -> bool:
        """Install a package."""
        self.permissions.check_packages()

        if package_name.startswith('./') or package_name.startswith('../') or os.path.isabs(package_name):
            return self._install_local(package_name)
        else:
            return self._install_registry(package_name)

    def _install_local(self, path: str) -> bool:
        """Install from local path."""
        source_path = Path(path).resolve()

        if not source_path.exists():
            raise RuntimeError(f"Package path not found: {path}")

        manifest_path = source_path / 'gopa.toml'
        if not manifest_path.exists():
            raise RuntimeError(f"Manifest not found: {manifest_path}")

        try:
            if toml:
                manifest = toml.load(manifest_path)
            else:
                manifest = self._parse_simple_toml(manifest_path)
        except Exception as e:
            raise RuntimeError(f"Failed to parse manifest: {e}")

        name = manifest.get('name', source_path.name)
        version = manifest.get('version', '1.0.0')

        target_dir = self.packages_dir / name / version
        target_dir.mkdir(parents=True, exist_ok=True)

        if (source_path / 'src').exists():
            shutil.copytree(source_path / 'src', target_dir / 'src', dirs_exist_ok=True)
        else:
            for item in source_path.iterdir():
                if item.name != 'gopa.toml':
                    if item.is_dir():
                        shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, target_dir / item.name)

        with open(target_dir / 'gopa.toml', 'w') as f:
            if toml:
                toml.dump(manifest, f)
            else:
                self._write_simple_toml(manifest, f)

        print(f"Installed {name} v{version}")
        return True

    def _install_registry(self, package_name: str) -> bool:
        """Install from registry."""
        registry_url = os.environ.get('REGISTRY_URL', '')

        if not registry_url:
            raise RuntimeError("Registry URL not configured. Set REGISTRY_URL environment variable.")

        raise RuntimeError(f"Registry installation not implemented. Use local path: ./{package_name}")

    def use(self, package_name: str, interpreter):
        """Load and use a package."""
        self.permissions.check_packages()

        stdlib_path = Path(__file__).parent / 'stdlib' / f'{package_name}.gopa'
        if stdlib_path.exists():
            self._load_gopa_file(stdlib_path, interpreter)
            return

        package_dir = self.packages_dir / package_name

        if not package_dir.exists():
            raise RuntimeError(f"Package '{package_name}' not found. Install it first.")

        versions = sorted([d.name for d in package_dir.iterdir() if d.is_dir()], reverse=True)
        if not versions:
            raise RuntimeError(f"No version found for package '{package_name}'")

        version_dir = package_dir / versions[0]

        manifest_path = version_dir / 'gopa.toml'
        if not manifest_path.exists():
            raise RuntimeError(f"Manifest not found for package '{package_name}'")

        try:
            if toml:
                manifest = toml.load(manifest_path)
            else:
                manifest = self._parse_simple_toml(manifest_path)
        except Exception as e:
            raise RuntimeError(f"Failed to parse manifest: {e}")

        requested_perms = manifest.get('permissions', [])
        for perm in requested_perms:
            if perm == 'network' and not self.permissions.network:
                raise RuntimeError(f"Package '{package_name}' requires network permission")
            elif perm == 'files' and not self.permissions.files:
                raise RuntimeError(f"Package '{package_name}' requires files permission")
            elif perm == 'graphics' and not self.permissions.graphics:
                raise RuntimeError(f"Package '{package_name}' requires graphics permission")
            elif perm == 'sound' and not self.permissions.sound:
                raise RuntimeError(f"Package '{package_name}' requires sound permission")
            elif perm == 'python_ffi' and not self.permissions.python_ffi:
                raise RuntimeError(f"Package '{package_name}' requires python_ffi permission")

        entry = manifest.get('entry', 'src/main.gopa')
        entry_path = version_dir / entry

        if not entry_path.exists():
            raise RuntimeError(f"Entry file not found: {entry_path}")

        self._load_gopa_file(entry_path, interpreter)
        self.loaded_packages[package_name] = {
            'version': versions[0],
            'manifest': manifest
        }

    def _load_gopa_file(self, file_path: Path, interpreter):
        """Load and execute a .gopa file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        from .lexer import Lexer
        from .parser import Parser

        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        for stmt in ast.statements:
            interpreter.execute(stmt)

    def _parse_simple_toml(self, path: Path) -> dict:
        """Simple TOML parser for MVP (handles basic key=value)."""
        manifest = {}
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value.startswith('[') and value.endswith(']'):
                        items = value[1:-1].split(',')
                        manifest[key] = [item.strip().strip('"').strip("'") for item in items]
                    else:
                        manifest[key] = value
        return manifest

    def _write_simple_toml(self, manifest: dict, f):
        """Simple TOML writer for MVP."""
        for key, value in manifest.items():
            if isinstance(value, list):
                f.write(f'{key} = {value}\n')
            else:
                f.write(f'{key} = "{value}"\n')

