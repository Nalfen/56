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

### Inline decisions

#### Single-file delivery
- **Problem**: RPG reference tools need to be shareable without a server or install step.
- **Decision**: Embed all data, CSS, and JS inline in one HTML file.
- **Trade-off**: File grows large (~3MB+); no incremental loading. Accepted because the target audience uses it as a local file.

#### Manufacturer modifiers applied at render time
- **Problem**: Items need to show both base and manufacturer-modified stats.
- **Decision**: `applyWpnMfr()` / `applyArmorMfr()` are pure functions that return modified copies. The `base_data` field on each slot stores the original catalog item so manufacturer can be changed without data loss.
- **Trade-off**: Every re-render recomputes modifications. Acceptable at this data scale.

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
