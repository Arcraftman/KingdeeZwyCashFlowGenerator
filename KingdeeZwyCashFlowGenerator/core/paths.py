"""Paths shared by the desktop UI, CLI, and configuration."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
TEMPLATE_DIR = PROJECT_ROOT / "resources" / "templates"
LOG_DIR = PROJECT_ROOT / "runtime" / "logs"


def project_path(*parts: str) -> Path:
    """Return a path relative to the source checkout."""
    return PROJECT_ROOT.joinpath(*parts)


def configure_console_output() -> None:
    """Keep optional console logging from crashing on Windows GBK terminals."""
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
