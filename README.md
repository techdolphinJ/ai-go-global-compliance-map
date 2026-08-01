# AI Go Global Compliance Map

For a China-based AI product entering a new market, this map identifies the practical compliance gates to clear before launch—without requiring a founder or operator to start from scratch across national regulatory portals.

This release uses intentional **tiered coverage**: eight depth-tier markets and ten breadth-tier markets. Every populated compliance statement is anchored to public first-party legal, regulatory, government, or official-legislative material.

> **Related work:** [AI Model Economics](https://github.com/techdolphinJ/ai-model-economics) (the cost layer) · [AI Vendor Commercialization Matrix](https://github.com/techdolphinJ/ai-vendor-commercialization-matrix) (the selection layer). This map covers the compliance and landing layer of taking AI global.

## What this map answers

| Layer | Question before launch |
| --- | --- |
| Data compliance | Can personal data leave the market? Is localisation required? Which privacy regime applies? |
| Tax | How are SaaS, digital services, and foreign suppliers taxed? |
| Legal entity and IP | Is a local entity, representative, registration, governing-law review, or trademark step relevant? |
| AI regulatory status | Is there an effective AI law, a government guideline, or only a policy/legislative development? |
| Payments and funds — legal layer | Which payment, foreign-exchange, remittance, or local-licensing rules are official legal gates? |

## Intentional tiered coverage

This is a coverage design, not a list of partly completed countries.

- **Depth tier — 8 markets:** **European Union, South Korea, Singapore, Indonesia, Japan, United States, Brazil, and United Arab Emirates.** [The depth-tier map](data/official-compliance-map.md) covers all five dimensions with official primary-source cards: data compliance, tax, legal entity / contracts / IP, AI regulatory status, and payments / funds — legal layer.
- **Breadth tier — 10 markets:** **United Kingdom, India, Viet Nam, Thailand, Malaysia, Mexico, Saudi Arabia, Nigeria, Australia, and Canada.** [The breadth-tier map](data/breadth-tier.md) deliberately anchors only data compliance and AI regulatory status with official sources. Tax, legal entity / contracts / IP, and payments / funds are visibly marked **Not covered in breadth tier — see depth-tier methodology** rather than guessed.

Every populated card has an official source URL, a source/version year, and the same verification date: **2026-07-31**.

## Query it

Query a complete source-linked country card instead of reading the tables manually:

```bash
python3 query.py korea
python3 query.py uk
python3 query.py --all
```

Inputs are case-insensitive. Short names such as `eu`, `korea`, `us`, `uae`, `uk`, `vietnam`, and `saudi` are supported, as are common aliases including `usa`, `great britain`, and `ksa`.

The script reads [data/official-compliance-map.md](data/official-compliance-map.md) and [data/breadth-tier.md](data/breadth-tier.md) at runtime. It contains no copied compliance claims, country-card values, or official-source URLs; the Markdown files remain the sole source of truth. Depth-tier output displays all five dimensions. Breadth-tier output displays its two official anchors and explicitly marks the other three dimensions as `Not covered in breadth tier — see depth-tier methodology`.

## Installation

**Tested 2026-07-31:** this command installed the `ai-go-global-compliance-map` skill from the public repository into an isolated Codex test directory, including `query.py` and both Markdown data files.

```bash
npx --yes skills add https://github.com/techdolphinJ/ai-go-global-compliance-map --skill ai-go-global-compliance-map
```

Remove `--yes` if you prefer `npx` to ask before downloading the `skills` package. After installation, run `python3 query.py <country>` from the installed skill directory.

## Deliberate handling of complex markets

- **United States:** the map separates the federal layer from clearly labelled **representative state examples, not exhaustive**. It never converts a California or Washington rule into a nationwide rule.
- **Brazil:** the tax card is explicitly a **tax-reform transition** card. LC 214/2025 is not presented as a fully settled, universally applicable end-state; implementation dates must be checked.
- **United Arab Emirates:** the AI card is deliberately labelled **Secondary source only — official original pending verification**. A federal AI-specific legal source for an AI-service entry or registration requirement was not located, and the UAE AI Strategy is not substituted for a legal conclusion.

## Example: the European Union, fully decomposed

| Gate | Practical regulatory question | Official anchor |
| --- | --- | --- |
| AI regulatory status | AI Act obligations depend on the system role and risk category; application is phased rather than a single AI-service licence. | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) (2024) |
| Data compliance | GDPR applies to relevant processing; international transfers require a valid Chapter V mechanism. | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) (2016) |
| Tax | EU VAT rules and the One Stop Shop provide the primary entry point for cross-border B2C digital services. | [European Commission VAT OSS](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en) (2021) |
| Payments and funds | Payment services are regulated; the provider model must be assessed against the EU payment-services framework and relevant Member State implementation. | [Directive (EU) 2015/2366](https://eur-lex.europa.eu/eli/dir/2015/2366/oj) (2015) |
| Legal entity and IP | Entity, contractual-law, and IP choices are not one EU-wide incorporation answer; start with company-law, Rome I, and EUIPO sources, then validate the target Member State. | [Directive (EU) 2017/1132](https://eur-lex.europa.eu/eli/dir/2017/1132/oj) (2017) · [Rome I](https://eur-lex.europa.eu/eli/reg/2008/593/oj) (2008) |

## Data contract

- A regulatory statement must be anchored to a public **government, regulator, tax authority, central bank, official legal database, or official notice**.
- Every source card records its **source or version year** and **last verified date**. A live webpage is not described simply as “current”.
- If an official original source cannot be located, the entry is labelled **Secondary source only — official original pending verification**. Secondary commentary is never presented as legal authority.
- “No AI-specific law located” is a source-status finding, not proof that no obligation exists. Sectoral, consumer-protection, platform, cybersecurity, and local rules can still apply.

## Market operations (non-official sources)

**Non-official source layer — reference only.** Mainstream payment methods, acquirer onboarding experience, pricing practices, and processor availability are market-operating facts rather than legislation. They are intentionally separated from the official legal map and are **not populated in this release** until each claim can be dated, attributed, and visibly labelled as non-official. See [data/market-operations-non-official.md](data/market-operations-non-official.md).

## Scope and disclaimer

This repository is a practical organisation of compliance information, **not legal advice**. Compliance policies change quickly. Before making a launch, product-design, tax, entity, payment, or data-transfer decision, consult qualified local professionals and verify the latest official source.

The first gate to taking an AI product global is not the product. It is the ability to land compliantly. This map breaks “Can we enter this market?” into traceable, practical gates.

## Coverage and next expansion

- **Depth tier (8):** European Union, South Korea, Singapore, Indonesia, Japan, United States, Brazil, and United Arab Emirates.
- **Breadth tier (10):** United Kingdom, India, Viet Nam, Thailand, Malaysia, Mexico, Saudi Arabia, Nigeria, Australia, and Canada.
- **Next expansion:** deepen breadth-tier markets only where all five dimensions can be sourced to official originals; add further representative U.S. state cards, Brazil tax-reform implementation milestones, and UAE emirate/free-zone-specific primary sources only where an official original is located.
