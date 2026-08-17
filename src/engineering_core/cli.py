from __future__ import annotations

import sys

from engineering_core.catalog_model import (
    DISCIPLINES,
    DISCIPLINE_FILES,
    LANES,
    LANE_FILES,
    TEMPLATES,
    TEMPLATE_FILES,
)

ADOPTION_COMMANDS = {"init", "migrate"}


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command in ADOPTION_COMMANDS:
        from engineering_core.adoption_cli import main as adoption_main

        adoption_main(sys.argv[1:])
        return

    from engineering_core.core_cli import main as core_main

    core_main()


if __name__ == "__main__":
    main()
