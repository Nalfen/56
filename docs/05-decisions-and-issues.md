# 05 — Decisions & Issues

## Decisions index

| # | Decision | Summary | File |
|---|---|---|---|
| 1 | Single-file delivery | All CSS, HTML, JS, and data in one `.html` file | inline |
| 2 | No build system | Edit-and-refresh workflow; no webpack/vite/npm | inline |
| 3 | Manufacturer mods at render time | `applyWpnMfr` / `applyArmorMfr` produce modified copies; base data stored in `base_data` slot field | inline |
| 4 | Card expand via `data-tog` attribute | Event delegation replaces inline `onclick` for card toggles (v8) | inline |
| 5 | `g.armor` holds all defensive types | Armors, forcefields, barriers, and defensive datacoms all live in the same array for unified browsing | inline |
| 6 | Credits: auto-tracked vs manual | Weapons/armor/datacoms/EVOs costs are auto-computed; equipment shop costs are manually tracked in `credits_spent` | inline |
| 7 | Manufacturer selection lives inside picker | Manufacturer dropdown is rendered inside the browse modal, not as a pre-selection on each slot. `ccState.picker.mfr` stores the in-picker choice; propagated to `ccPickFromCache` on confirm | inline |
| 8 | Melee-only manufacturers use restricted category set | `WPN_MFRS_MELEE_ONLY` (Dilithium, Monomolecular) filter picker to `Melee Weapons (Martial Arts)` + `Ranged / Throwing Weapons (Dexterity)` only — Powered Melee excluded | inline |
| 9 | Data field name divergence: datacoms | `g.datacoms` uses `nanites` (plural) and `def_physical`/`def_spiritual`; `ccState.datacoms[]` uses `nanite` (singular) and `def_phys`/`def_spirit`. Mapping happens in `ccPickFromCache` | inline |
| 10 | Racial max removed for Subject 0056 | `BG_GRANTS['Subject 0056'].no_racial_max = true` causes `ccRenderAttributes()` to render `∞` instead of the racial max value | inline |

### Inline decisions

#### Single-file delivery
- **Problem**: RPG reference tools need to be shareable without a server or install step.
- **Decision**: Embed all data, CSS, and JS inline in one HTML file.
- **Trade-off**: File grows large (~3MB+); no incremental loading. Accepted because the target audience uses it as a local file.

#### Manufacturer modifiers applied at render time
- **Problem**: Items need to show both base and manufacturer-modified stats.
- **Decision**: `applyWpnMfr()` / `applyArmorMfr()` are pure functions that return modified copies. The `base_data` field on each slot stores the original catalog item so manufacturer can be changed without data loss.
- **Trade-off**: Every re-render recomputes modifications. Acceptable at this data scale.

#### Manufacturer selection inside picker (Decision 7)
- **Problem**: Having manufacturer select outside the browse window meant users had to close the picker, change manufacturer, then reopen — and the external select cluttered each slot card.
- **Decision**: Move manufacturer dropdown entirely into `ccRenderPicker()`. `ccState.picker.mfr` holds the choice during the browse session. On confirm (`ccPickFromCache`), `picker.mfr` is written to the slot's `mfr` field.
- **Trade-off**: Manufacturer choice is lost if user closes the picker without selecting. Acceptable — the slot retains its previously set `mfr`.

#### Melee-only manufacturer category filter (Decision 8)
- **Problem**: Dilithium and Monomolecular are melee-only brands but the picker showed all weapon categories.
- **Decision**: `MELEE_THROW_CATS = new Set(['Melee Weapons (Martial Arts)', 'Ranged / Throwing Weapons (Dexterity)'])`. When `WPN_MFRS_MELEE_ONLY.has(pickerMfr)`, the picker filters to only those categories. Powered Melee is intentionally excluded from this set.
- **Trade-off**: Hard-coded category strings — if category names change in data, filter must be updated.

#### Datacom field name divergence (Decision 9)
- **Problem**: `g.datacoms` data uses `nanites` (plural) and `def_physical` / `def_spiritual`. Character state uses `nanite` (singular) and `def_phys` / `def_spirit`.
- **Decision**: Mapping is performed explicitly in `ccPickFromCache` when a datacom is picked. No renaming of either side.
- **Trade-off**: Future data additions must keep this mapping in sync.

#### Racial max for Subject 0056 (Decision 10)
- **Problem**: Subject 0056 background removes racial attribute maximums, but the attributes tab showed static racial max values.
- **Decision**: `BG_GRANTS['Subject 0056'] = {no_racial_max: true}`. `ccRenderAttributes()` checks this flag and renders `∞` (yellow, with tooltip) instead of the racial max. Natural Birth variance still applies to min/avg.
- **Trade-off**: Only affects display — the character sheet has no hard enforcement of racial caps anyway.

#### OPT / OPT+ gates option button
- **Problem**: Not all items accept options; adding options to non-OPT items was silently incorrect.
- **Decision**: `+ Option` button is only rendered when `special` contains `\bOPT\b` (max 1) or `\bOPT\+` (max 2). Manufacturer-added OPT (e.g. Kintech adds OPT to armor) is reflected automatically since `special` is the post-manufacturer applied value.
- **Trade-off**: If a user manually types OPT into special, the button appears — intentional, allows manual overrides.

#### Credits: auto-tracked vs manual split
- **Problem**: Weapons/armor/datacoms have computable costs (base × mfr price_mult × option multipliers). Equipment from the gear shop is bought explicitly. EVOs have a real credit cost.
- **Decision**: `ccAutoTrackedSpent()` computes combat/tech/evo costs automatically. `credits_spent` is the manual gear-shop bucket. Remaining = budget − auto − manual.
- **Trade-off**: If a user manually edits a weapon name without picking from catalog (`base_data` is null), cost is 0. Acceptable — manual entry implies the user manages cost themselves.

---

## Known issues

### None currently tracked

Add new issues here as they are discovered. Format:

#### [Issue title]
- **Symptom**: what the user/developer sees
- **Root cause**: why it happens
- **Status**: Active / Mitigated / Won't Fix
- **Workaround**: how to deal with it now
