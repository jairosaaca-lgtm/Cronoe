#!/usr/bin/env python3
"""Cronoe OBS installer executable.

Creates/updates a local overlay folder with the scoreboard files so it can be
used by OBS as a Browser Source (local file mode).
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PROJECT_FILES = ["index.html", "styles.css", "app.js", "README.md"]
DEFAULT_FOLDER_NAME = "cronoe-overlay"


def project_root() -> Path:
    """Find project root both in repo mode and packaged .pyz mode."""
    candidates = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent.parent,
    ]
    for base in candidates:
        if (base / "index.html").exists() and (base / "app.js").exists():
            return base
    return Path.cwd()


def find_default_obs_plugin_dir() -> Path | None:
    home = Path.home()

    windows_obs = home / "AppData" / "Roaming" / "obs-studio" / "plugins"
    mac_obs = home / "Library" / "Application Support" / "obs-studio" / "plugins"
    linux_obs = home / ".config" / "obs-studio" / "plugins"

    for candidate in (windows_obs, mac_obs, linux_obs):
        if candidate.exists():
            return candidate
    return None



def copy_overlay_files(destination: Path) -> list[Path]:
    root = project_root()
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []

    for rel in PROJECT_FILES:
        src = root / rel
        if not src.exists():
            raise FileNotFoundError(f"No se encontró el archivo requerido: {src}")
        dst = destination / rel
        shutil.copy2(src, dst)
        copied.append(dst)

    return copied


def write_obs_howto(destination: Path) -> Path:
    guide = destination / "OBS_SETUP.txt"
    local_index = destination / "index.html"
    guide.write_text(
        """
Cronoe Overlay - Configuración rápida OBS
=========================================

1) En OBS: Sources -> + -> Browser Source.
2) Marca "Local file".
3) Selecciona este archivo:
   {index_path}
4) Recomendado: Width=1920, Height=220 (o según tu escena).
5) Activa "Shutdown source when not visible" si quieres ahorrar recursos.

Tip:
- Si actualizas tu proyecto, vuelve a ejecutar este instalador.
""".strip().format(index_path=local_index),
        encoding="utf-8",
    )
    return guide


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instala/actualiza el overlay Cronoe para usarlo como Browser Source en OBS."
    )
    parser.add_argument(
        "--obs-plugin-dir",
        type=Path,
        default=None,
        help="Ruta de plugins de OBS. Si no se define, intenta autodescubrir.",
    )
    parser.add_argument(
        "--folder-name",
        default=DEFAULT_FOLDER_NAME,
        help=f"Nombre de carpeta de instalación dentro de plugins (default: {DEFAULT_FOLDER_NAME}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra acciones sin copiar archivos.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    obs_plugins = args.obs_plugin_dir or find_default_obs_plugin_dir()

    if obs_plugins is None:
        print("❌ No se detectó carpeta de plugins de OBS automáticamente.")
        print("   Usa --obs-plugin-dir <ruta> para especificarla manualmente.")
        return 2

    install_dir = obs_plugins / args.folder_name

    print(f"OBS plugins dir: {obs_plugins}")
    print(f"Destino overlay: {install_dir}")

    if args.dry_run:
        print("[dry-run] No se copiaron archivos.")
        return 0

    copied = copy_overlay_files(install_dir)
    guide = write_obs_howto(install_dir)

    print("\n✅ Instalación completada. Archivos copiados:")
    for path in copied:
        print(f" - {path}")
    print(f" - {guide}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
