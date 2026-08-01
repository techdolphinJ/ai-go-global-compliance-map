---
name: ai-go-global-compliance-map
description: Query source-linked AI go-global compliance cards for 18 markets, covering data, tax, legal entity/IP, AI regulatory status, and payments/funds legal gates.
---

# AI Go Global Compliance Map

Query a market’s official-source compliance card for any AI product before launch. The output keeps the distinction between **depth-tier** markets (five dimensions) and **breadth-tier** markets (two official anchors plus three explicit coverage boundaries).

## Run

```bash
python3 query.py <country>
python3 query.py --all
```

If Python 3 is available as `python`, use `python query.py <country>` instead.

Inputs are case-insensitive. Supported short names include:

```text
eu, korea, singapore, indonesia, japan, us, brazil, uae,
uk, india, vietnam, thailand, malaysia, mexico, saudi,
nigeria, australia, canada
```

Common aliases such as `usa`, `great britain`, `viet nam`, and `ksa` also work.

```bash
python3 query.py korea
```

## Data source

The Markdown files are the sole source of truth:

- `data/official-compliance-map.md` — eight depth-tier markets, five dimensions each.
- `data/breadth-tier.md` — ten breadth-tier markets, with data compliance and AI regulatory-status anchors only.

`query.py` parses those existing tables at runtime. It contains no copied compliance facts, country-card values, or official-source URLs, and no JSON mirror is used.

## Data contract

- Every populated record is anchored to public first-party legal, regulatory, government, official-tax/central-bank, or official-legislative material.
- Each displayed dimension carries its official source URL, source/version year, and verification date from the Markdown card.
- A government guideline, strategy, or bill is not presented as an effective AI Act or a generic licensing requirement.
- In breadth-tier output, tax, legal entity / contracts / IP, and payments / funds — legal layer explicitly say `Not covered in breadth tier — see depth-tier methodology`. This is a coverage boundary, not a claim that no obligation applies.
- `Secondary source only — official original pending verification` is preserved as a source-status finding; it is never converted into legal authority.

## Output example

`python3 query.py korea` currently returns this source-linked fragment:

```text
AI GO GLOBAL COMPLIANCE MAP
Market: South Korea
Coverage tier: Depth (5 dimensions)
Data source: data/official-compliance-map.md (Markdown is the sole source of truth)

DATA COMPLIANCE
The Personal Information Protection Act is the primary legal anchor, including rules relevant to overseas transfer and domestic-agent questions. Validate the current Korean text and applicable thresholds before launch.
  Official source: https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=213857&urlMode=engLsInfoR&viewCls=engLsInfoR
  Source / version year: Official English text page; legal database search showed 2025 amendments
  Last verified: 2026-07-31

AI REGULATORY STATUS
Effective law. The Framework Act on the Development of Artificial Intelligence and the Creation of a Foundation for Trust took effect on 2026-01-22. This is a high-volatility item: review the latest implementing material before any decision.
  Official source: https://www.law.go.kr/LSW/lsInfoP.do?chrClsCd=010203&lsiSeq=268543&urlMode=engLsInfoR&viewCls=engLsInfoR
  Source / version year: Act No. 20676; enacted 2025, effective 2026-01-22
  Last verified: 2026-07-31

Not legal advice — verify the latest official text and obtain qualified local advice before launch.
```

## Disclaimer

This skill is a traceable research aid, **not legal advice**. Verify the latest official material, applicable implementation notices, subnational and sector-specific rules, and the product’s actual data, payment, sales, and operating model before launch.
