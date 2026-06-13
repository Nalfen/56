# 06 — Implementation Plan

> This document is the high-level Table of Contents for the project. For the execution trace and thought process, refer to the corresponding `work/X.Y/` folders.

---

## Milestone 1.0 — Character Creator (Core)
**Goal**: Full interactive character creation tool embedded in the compendium.
**Status**: done

| Feature | Status |
|---|---|
| Origin block (clone / natural birth) | done |
| Attributes (base + perm + bonus) | done |
| Skills (all categories, XP tracking) | done |
| Talents (10 slots, XP tracking, bg-granted) | done |
| Evolutions (dynamic slots, EP cap, bg-granted, credit cost) | done |
| Background picker (with auto-granted skills/talents/evos) | done |
| Occupation picker (with starting credits auto-populate) | done |
| Race picker | done |
| Roll20 JSON export | done |

---

## Milestone 2.0 — Character Creator (Combat & Tech)
**Goal**: Weapons, armor/defense, and tech slots with full catalog integration.
**Status**: done

| Feature | Status |
|---|---|
| Weapons (6 slots, catalog browse, all fields) | done |
| Defense slots (2 slots, all types from g.armor) | done |
| Manufacturer selector for weapons & armor | done |
| OPT/OPT+ gated options per item | done |
| Datacoms (3 slots, catalog browse, manufacturer) | done |
| Software programs (10 slots) | done |
| Gadgets (5 slots, catalog browse) | done |
| Range / RoF auto-populate from catalog | done |

---

## Milestone 3.0 — Shopping Cart / Credits System
**Goal**: Unified credit tracking across all purchasable content.
**Status**: done

| Feature | Status |
|---|---|
| Budget / Gear-spent manual tracking | done |
| Auto-tracked: weapons + armor + datacoms + EVOs | done |
| Mini credits bar on Combat / Tech / Evos tabs | done |
| Per-item cost badge on each slot | done |
| Gear Shop (equipment catalog with Buy button) | done |
| Credits exported in Roll20 JSON | done |

---

## Milestone 4.0 — Catalog & Reference Sections
**Goal**: Full browsable catalog for ships, drones, vehicles, modules.
**Status**: done

| Feature | Status |
|---|---|
| Vehicles catalog | done |
| Drones catalog | done |
| Modules catalog | done |
| Ships catalog with component breakdown | done |
| Ship Components catalog | done |
| Drone Builder interactive tool | done |
| Drone Parts catalog | done |
| Ammunition section + compatibility matrix | done |
| Enemy Generator (GM tools) | done |

---

## Milestone 5.0 — Manufacturer picker display fixes
**Goal**: Remaining display gaps in the character creator manufacturer system.
**Status**: done

| Feature | Status |
|---|---|
| Mono-Med Customs: force availability to UNIQUE instead of shifting by avail_mod | done |
| Size changes shown + highlighted in medical gear shop when manufacturer changes size | done |
| Size changes shown + highlighted in datacom picker when manufacturer changes size | done |
| Size changes shown + highlighted in weapon picker; `applyWpnMfr` now applies `size_mod` | done |

---

---

## Milestone 7.0 — Identity Tab UX Refinements
**Goal**: Restructure the Identity tab for a cleaner, less cluttered layout.
**Status**: done

| Feature | Status |
|---|---|
| Merge Attributes tab into Identity (eliminate standalone tab) | done |
| Origin block (Clone/Natural Birth) at top full-width | done |
| Left col: identity fields; Right col: full attribute table with XP costs | done |
| Health/Morale/CHI + Initiative as full-width section below 2-col | done |
| Racial traits (racial/evolution/environment) in own detail box below | done |
| Background, Occupation detail boxes below (traits grid + notes) | done |
| Evolution attribute notes box below (T4-B, display-only) | done |
| Background and Occupation pickers sorted alphabetically | done |
| Race selector sorted alphabetically | done |

---

---

## Milestone 8.0 — Data-Driven Architecture
**Goal**: Extract all game content from the embedded HTML into external JSON files; ship a data-driven compendium served over HTTP.
**Status**: done

| Feature | Status |
|---|---|
| Extract all `g.*` content to `data/v8/*.json` (11 files) | done |
| `manifest.json` load order + Promise.all fetch boot sequence | done |
| Boot overlay (progress bar, error panel with instructions) | done |
| `const g = window.__DATA` shell in renderer script | done |
| v9 data-driven prototype | done |
| v11 canonical data-driven build (refined CSS, fonts) | done |
| GitHub Pages hosting path documented | done |
| Skill migration (5 files updated between `data/v8_pre_skillmigration/` and `data/v8/`) | done |

---

## Backlog (unscheduled)

- Rename "armor" references throughout the character creator to "defense" for clarity → see drafts if created
- Spell picker for character creator (browse `g.spells`)
- Per-item notes/memo field on character creator slots
- Character save/load via localStorage
- Print-friendly export (CSS print media)
- Starmap pin/gate editor UX improvements

---

## Milestone 6.0 — Character Creator Coverage Gap
**Goal**: Surface the 112 mechanical effects in backgrounds, occupations, talents, and evolutions that the character creator currently ignores.
**Status**: done — see `work/6.0/`

Full audit conducted 2026-05-12. Gaps categorised into 5 implementation tiers.

| Tier | Feature | Status |
|---|---|---|
| T1-A | Talent effect text displayed beneath each talent slot | done |
| T1-B | Evolution effect text displayed beneath each evo slot | done |
| T1-C | Background traits list on Origin tab | done |
| T1-D | Talent/evo effect text in picker browse list | done |
| T1-E | Skill row visual indicators for bonus and crit range | done |
| T2-A | BG_GRANTS extended with `attr_max_mods` for backgrounds that reduce racial maxes | done |
| T2-B | Occupation skill bonus choice — mechanically enforced via `ccApplyOccBonus()` | done |
| T2-C | Resource locks: Spirit Judge SURGE=0, Imaginary Friend CHI=0, Void Soul CHI=0 | done (bg-based; Void Soul deferred) |
| T3 | Passive Abilities panel — read-only list of passive effects from active talents + evolutions | done |
| T4-A | Occupation skill bonuses enforced as tracked `sk_bonus` modifiers via `occ_bonus_skills[]` | done |
| T4-B | Evolution attribute notes panel on Attributes tab (display-only; bonuses are conditional) | done |
| T4-C | Background combat/vulnerability notes panel on Combat tab | done |
| T5-A | Contacts / faction access section | backlog |
| T5-B | Starting equipment grants from backgrounds | backlog |
| T5-C | Full passive modifier enforcement (modifier stack system) | backlog |
