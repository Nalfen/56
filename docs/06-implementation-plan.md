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
**Status**: todo — see `work/5.0/`

| Feature | Status |
|---|---|
| Mono-Med Customs: force availability to UNIQUE instead of shifting by avail_mod | todo |
| Size changes shown + highlighted in medical gear shop when manufacturer changes size | todo |
| Size changes shown + highlighted in datacom picker when manufacturer changes size | todo |

---

## Backlog (unscheduled)

- Rename "armor" references throughout the character creator to "defense" for clarity → see drafts if created
- Spell picker for character creator (browse `g.spells`)
- Per-item notes/memo field on character creator slots
- Character save/load via localStorage
- Print-friendly export (CSS print media)
- Starmap pin/gate editor UX improvements
