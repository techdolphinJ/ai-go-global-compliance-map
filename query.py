#!/usr/bin/env python3
"""Query country compliance cards from the repository's Markdown source files.

The Markdown files remain the only source of truth. This program parses their
existing country tables at runtime and deliberately stores no compliance facts
or official-source URLs of its own.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_FILES = (
    ("Depth", ROOT / "data" / "official-compliance-map.md"),
    ("Breadth", ROOT / "data" / "breadth-tier.md"),
)

# Interface vocabulary only. Compliance content is always read from Markdown.
ALIASES = {
    "eu": "european union",
    "europe": "european union",
    "european union": "european union",
    "korea": "south korea",
    "south korea": "south korea",
    "republic of korea": "south korea",
    "singapore": "singapore",
    "indonesia": "indonesia",
    "japan": "japan",
    "us": "united states",
    "u s": "united states",
    "usa": "united states",
    "united states": "united states",
    "brazil": "brazil",
    "brasil": "brazil",
    "uae": "united arab emirates",
    "united arab emirates": "united arab emirates",
    "emirates": "united arab emirates",
    "uk": "united kingdom",
    "u k": "united kingdom",
    "united kingdom": "united kingdom",
    "great britain": "united kingdom",
    "britain": "united kingdom",
    "india": "india",
    "vietnam": "viet nam",
    "viet nam": "viet nam",
    "thailand": "thailand",
    "malaysia": "malaysia",
    "mexico": "mexico",
    "saudi": "saudi arabia",
    "saudi arabia": "saudi arabia",
    "ksa": "saudi arabia",
    "nigeria": "nigeria",
    "australia": "australia",
    "canada": "canada",
}

DIMENSION_ORDER = (
    "Data compliance",
    "Tax",
    "Legal entity / contracts / IP",
    "AI regulatory status",
    "Payments and funds — legal layer",
)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def normalise(value: str) -> str:
    """Normalise user input and country headings for case-insensitive lookup."""
    value = value.casefold().replace("_", " ")
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_table(lines: list[str]) -> list[dict[str, str]]:
    """Parse one ordinary pipe-delimited Markdown table."""
    start = next((index for index, line in enumerate(lines) if line.startswith("|")), None)
    if start is None or start + 1 >= len(lines):
        return []

    headers = cells(lines[start])
    rows: list[dict[str, str]] = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        values = cells(line)
        if len(values) != len(headers):
            raise ValueError("A country-table row does not match its header.")
        rows.append(dict(zip(headers, values)))
    return rows


def clean_markdown(value: str) -> str:
    value = LINK_RE.sub(lambda match: match.group(1), value)
    return value.replace("**", "").replace("`", "").strip()


def source_urls(value: str) -> list[str]:
    urls: list[str] = []
    for match in LINK_RE.finditer(value):
        if match.group(2) not in urls:
            urls.append(match.group(2))
    return urls


def country_name_from_heading(heading: str) -> str:
    """Remove explanatory suffixes such as '— tax-reform transition'."""
    return heading.split(" —", 1)[0].strip()


def parse_source_file(tier: str, path: Path) -> dict[str, dict[str, object]]:
    try:
        markdown = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ValueError(f"Data source not found: {path}") from error

    cards: dict[str, dict[str, object]] = {}
    for chunk in re.split(r"(?m)^## ", markdown)[1:]:
        heading, _, body = chunk.partition("\n")
        table = parse_table(body.splitlines())
        if not table or "Dimension" not in table[0]:
            continue

        country = country_name_from_heading(heading)
        status_column = next(
            (column for column in table[0] if "regulatory status and practical gate" in column.casefold()),
            None,
        )
        required_columns = ("Dimension", "Official source", "Source / version year", "Last verified")
        if status_column is None or any(column not in table[0] for column in required_columns):
            raise ValueError(f"{country_name_from_heading(heading)} has an unexpected country-table schema.")
        dimensions = {
            row["Dimension"]: {
                "Status": row[status_column],
                "Official source": row["Official source"],
                "Source / version year": row["Source / version year"],
                "Last verified": row["Last verified"],
            }
            for row in table
        }
        missing = [dimension for dimension in DIMENSION_ORDER if dimension not in dimensions]
        if missing:
            raise ValueError(f"{country} is missing dimensions: {', '.join(missing)}")

        key = normalise(country)
        if key in cards:
            raise ValueError(f"Duplicate country card: {country}")
        cards[key] = {
            "country": country,
            "tier": tier,
            "source_file": path.relative_to(ROOT).as_posix(),
            "dimensions": dimensions,
        }
    if not cards:
        raise ValueError(f"No country cards found in {path.relative_to(ROOT)}")
    return cards


def load_cards() -> dict[str, dict[str, object]]:
    cards: dict[str, dict[str, object]] = {}
    for tier, path in SOURCE_FILES:
        for key, card in parse_source_file(tier, path).items():
            if key in cards:
                raise ValueError(f"Country appears in more than one source file: {card['country']}")
            cards[key] = card
    return cards


def print_sources(value: str) -> None:
    urls = source_urls(value)
    if urls:
        for url in urls:
            print(f"  Official source: {url}")
    else:
        print("  Official source: —")


def print_dimension(name: str, row: dict[str, str]) -> None:
    print(name.upper())
    print(clean_markdown(row["Status"]))
    print_sources(row["Official source"])
    print(f"  Source / version year: {clean_markdown(row['Source / version year'])}")
    print(f"  Last verified: {clean_markdown(row['Last verified'])}")


def print_country(card: dict[str, object]) -> None:
    country = str(card["country"])
    tier = str(card["tier"])
    dimensions = card["dimensions"]
    assert isinstance(dimensions, dict)

    print("AI GO GLOBAL COMPLIANCE MAP")
    print(f"Market: {country}")
    print(f"Coverage tier: {tier} ({'5 dimensions' if tier == 'Depth' else '2 anchored dimensions + 3 explicit coverage boundaries'})")
    print(f"Data source: {card['source_file']} (Markdown is the sole source of truth)")

    for dimension in DIMENSION_ORDER:
        print()
        row = dimensions[dimension]
        assert isinstance(row, dict)
        print_dimension(dimension, row)

    print()
    print("Not legal advice — verify the latest official text and obtain qualified local advice before launch.")


def truncate(value: str, limit: int = 64) -> str:
    value = clean_markdown(value)
    return value if len(value) <= limit else value[: limit - 3] + "..."


def print_all(cards: dict[str, dict[str, object]]) -> None:
    rows: list[tuple[str, str, str, str]] = []
    for card in sorted(cards.values(), key=lambda item: str(item["country"])):
        dimensions = card["dimensions"]
        assert isinstance(dimensions, dict)
        rows.append(
            (
                str(card["country"]),
                str(card["tier"]),
                truncate(dimensions["Data compliance"]["Status"]),
                truncate(dimensions["AI regulatory status"]["Status"]),
            )
        )

    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(("Market", "Tier", "Data compliance", "AI regulatory status"))
    ]
    print("AI GO GLOBAL COMPLIANCE MAP — ALL MARKETS")
    print("Data source: data/official-compliance-map.md + data/breadth-tier.md")
    print()
    print(f"{'Market':<{widths[0]}}  {'Tier':<{widths[1]}}  {'Data compliance':<{widths[2]}}  AI regulatory status")
    print(f"{'-' * widths[0]}  {'-' * widths[1]}  {'-' * widths[2]}  {'-' * widths[3]}")
    for market, tier, data, ai in rows:
        print(f"{market:<{widths[0]}}  {tier:<{widths[1]}}  {data:<{widths[2]}}  {ai}")
    print("\nRun `python3 query.py <country>` for the complete source-linked card.")
    print("Not legal advice — verify the latest official text and obtain qualified local advice before launch.")


def print_usage(cards: dict[str, dict[str, object]]) -> None:
    grouped: dict[str, list[str]] = {"Depth": [], "Breadth": []}
    for card in cards.values():
        grouped[str(card["tier"])].append(str(card["country"]))

    print("Usage: python3 query.py <country>")
    print("       python3 query.py --all")
    print("       (use `python` instead when that is your Python 3 command)")
    print("Example: python3 query.py korea")
    print(f"Depth tier ({len(grouped['Depth'])}): {', '.join(sorted(grouped['Depth']))}")
    print(f"Breadth tier ({len(grouped['Breadth'])}): {', '.join(sorted(grouped['Breadth']))}")
    print("Accepted short names include: eu, korea, us, uae, uk, vietnam, and saudi.")


def main(argv: list[str]) -> int:
    try:
        cards = load_cards()
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if len(argv) != 2:
        print_usage(cards)
        return 0

    query = normalise(argv[1])
    if query == "all":
        print_all(cards)
        return 0

    country_key = ALIASES.get(query, query)
    card = cards.get(country_key)
    if card is None:
        print(f"Unknown market: {argv[1]}\n")
        print_usage(cards)
        return 2

    print_country(card)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
