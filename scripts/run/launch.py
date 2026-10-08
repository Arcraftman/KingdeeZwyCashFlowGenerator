"""Run the GUI or CLI from a source checkout."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "gui"
    if mode not in {"gui", "cli"}:
        print("Usage: python scripts/run/launch.py [gui|cli]", file=sys.stderr)
        return 2

    if len(sys.argv) > 1:
        sys.argv.pop(1)
    if mode == "gui":
        from KingdeeZwyCashFlowGenerator.app.desktop import main as run
    else:
        from KingdeeZwyCashFlowGenerator.cli import main as run
    return run() or 0


if __name__ == "__main__":
    raise SystemExit(main())
