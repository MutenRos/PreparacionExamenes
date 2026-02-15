from __future__ import annotations

import argparse
from datetime import datetime


def greet(name: str) -> str:
    return f"Hola, {name}!"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dario",
        description="CLI de ejemplo para el proyecto base en Python",
    )
    parser.add_argument("name", nargs="?", default="mundo", help="Nombre a saludar")
    parser.add_argument(
        "--when",
        choices=["date", "time", "none"],
        default="none",
        help="Opcional: mostrar fecha u hora",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(args=argv)

    msg = greet(args.name)
    if args.when == "date":
        msg += f" Hoy es {datetime.now().date()}"
    elif args.when == "time":
        msg += f" Son las {datetime.now().time().strftime('%H:%M:%S')}"

    print(msg)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
