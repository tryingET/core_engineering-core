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

COMMAND_ROUTERS = {
    "init": "adoption",
    "migrate": "adoption",
    "scan-adoption": "scan",
}


def _print_help() -> None:
    print(
        "engineering-core\n\n"
        "Guidance retrieval:\n"
        "  list, list-disciplines, list-templates, list-profiles, catalog\n"
        "  recommend, overview, show, show-discipline, show-all-for\n\n"
        "Repository lifecycle:\n"
        "  doctor, init, migrate\n\n"
        "Fleet lifecycle:\n"
        "  scan-adoption\n\n"
        "Repository maintenance:\n"
        "  sync, check-self\n\n"
        "Run `engineering-core <command> --help` for command options."
    )


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command in {None, "-h", "--help"}:
        _print_help()
        return

    router = COMMAND_ROUTERS.get(command)
    if router == "adoption":
        from engineering_core.adoption_cli import main as routed_main

        routed_main(sys.argv[1:])
        return
    if router == "scan":
        from engineering_core.scan_cli import main as routed_main

        routed_main(sys.argv[1:])
        return

    from engineering_core.core_cli import main as core_main

    core_main()


if __name__ == "__main__":
    main()
