# CLAUDE.md — 56th Century Compendium

## Project Overview

This repository contains the **56th Century Compendium**, a self-contained browser-based reference tool for the *56th Century* tabletop RPG system. The compendium is delivered as single-file HTML documents with all data, styles, and logic embedded inline — no build system, no external dependencies (except Google Fonts via CDN), and no server required.

The project is released under **CC0 1.0 Universal** (public domain).

---

## Repository Structure

```
/
├── 56th_century_compendium_v3.html   # Version 3 (431 lines, archived)
├── 56th_century_compendium_v5.html   # Version 5 (838 lines, archived)
├── 56th_century_compendium_v8.html   # Version 8 (current/latest)
├── ship_components.csv               # Exported flat ship component catalog (generated)
├── inject_engines.py                 # Dev helper: injects ENGINE codes into ship data
└── LICENSE                           # CC0 1.0 Universal
```

**v8 is the canonical/latest version.** Work on v8 unless explicitly told otherwise. v3 and v5 are kept for reference.

---

## Architecture

Each compendium file is a single self-contained HTML file with three parts:

### 1. CSS (inside `<style>`)
- Uses CSS custom properties (`:root` variables) for the entire color palette
- Dark sci-fi theme with cyan (`--a: #00c8ff`), orange (`--a2: #ff6b35`), and purple (`--a3: #a855f7`) accents
- Fonts: `Orbitron` (headings/labels), `Share Tech Mono` (data/code), `Exo 2` (body) — loaded from Google Fonts
- Fully responsive grid via `auto-fill`/`minmax` — no media queries needed
- No external CSS frameworks

### 2. HTML Body
- Fixed-height layout: `header` → `aside` (nav) + `main` (content area)
- Sidebar navigation with `data-s` attribute buttons (one per section)
- `<div id="main">` is dynamically rewritten by `render()` on every interaction
- Tooltip element `<div id="tt">` positioned absolutely via JS

### 3. JavaScript (inside `<script>`)
All logic is vanilla JS with no frameworks. Key globals:

| Variable | Purpose |
|---|---|
| `g` | Master data object (all RPG content) |
| `cs` | Current section string (e.g. `'weapons'`) |
| `sq` | Current search query (lowercase) |
| `af` | Active filter category string |
| `mfrState` | Per-section manufacturer selection `{weapons, armor, datacoms, medical}` |

Key functions:

| Function | Purpose |
|---|---|
| `render()` | Main render function — rewrites `main` innerHTML based on `cs`, `sq`, `af` |
| `ms(array)` | Search match — returns true if any element contains `sq` |
| `hl(s, q)` | HTML-escape and highlight search matches with `.hl` spans |
| `tog(id)` | Toggle `.x` class on a card (expand/collapse) |
| `esc(s)` | HTML-escape a string |
| `tc(v)` | Map a value string to a tag CSS class (color by type/legality/availability) |
| `rarCls(avail)` | Map availability string to a `.rar-*` card border class |
| `defCls(tier)` | Map defense tier string to a `.dp-*` pill class |
| `fmt(n)` | Format credit amounts with thousands separators (e.g. `1000000` → `1 000 000`) |
| `descHtml(str, sq)` | Render description with search highlights |
| `applyWpnMfr(item, mfr)` | Apply manufacturer stat modifiers to a weapon |
| `applyArmorMfr(item, mfr)` | Apply manufacturer stat modifiers to armor |
| `applyMedMfr(item, mfr)` | Apply manufacturer stat modifiers to medical items |
| `defShift(current, mod)` | Shift a defense tier by a numeric modifier |
| `mfrBar(sec, list, cur)` | Render the manufacturer selector bar HTML |
| `fcBtn(label, val, cur)` | Render a filter chip button HTML (uses `data-cat` attribute, no inline eval) |
| `bst(sp)` | Parse and render special property tags with tooltips |

---

## Data Structure (`g` object)

All game data lives in the `const g = {...}` constant. Top-level keys:

| Key | Description |
|---|---|
| `g.specials` | Dictionary of weapon/ability special property codes → `{name, desc}` |
| `g.rules_grouped` | Array of rule groups, each with `{title, sections:[{title, entries:[{key,text}]}]}` |
| `g.glossary_clean` | Flat glossary entries `{name, desc}` — used by the standalone `glossary_only` section |
| `g.code` | Encoded reference entries `{name, desc}` |
| `g.races` | Array of playable races with stats (PHYS, ACUITY, MENTAL, SOCIAL, ENDUR, SPEED, WITS, WILL — each as `{min,avg,max}`) |
| `g.backgrounds` | Character backgrounds `{name, race, desc, traits:[]}` |
| `g.occupations` | Occupations `{name, desc, details:[]}` |
| `g.skills` | Skills `{name, category, desc}` |
| `g.talents` | Talents `{name, skill, category, effect, cost}` |
| `g.evolutions` | `{entries:[{name, evo_type, tier, effect}]}` |
| `g.weapons` | Weapons `{name, category, type, damage, range, legality, special, notes, desc, variants:{}}` |
| `g.armor` | Armor items with defense values and manufacturer variants |
| `g.options` | Weapon/armor options `{name, desc, wpn_ranged, wpn_melee, availability, legality}` |
| `g.spells` | Spells with school, range, duration, effect |
| `g.datacoms` | Datacom devices with manufacturer variants |
| `g.medical` | Medical items with manufacturer variants |
| `g.catalog` | Vehicle/drone/ship catalog (new in v8) — see below |
| `g.catalog.vehicles` | Vehicles `{name, manufacturer, size, availability, durability, structure, deflect, soak, wall, integrity, special}` |
| `g.catalog.drones` | Drones `{name, manufacturer, size, availability, durability, structure, deflect, soak, wall, integrity, special}` |
| `g.catalog.chassis` | Drone chassis sizes `{size, core, internal, external, durability, structure, base_price}` |
| `g.catalog.modules` | Drone & vehicle modules `{name, size, availability, description, cost}` |
| `g.catalog.ships` | Spaceships `{name, class, role, description, power, total_size, total_cost, core_size, core:[], internal_size, internal:[], external_size, external:[]}` |
| `g.catalog.ship_components` | Flat array of ship component catalog entries — built at startup by `buildShipComps()` from `SCOMP_DEF` |

---

## Navigation Sections (v8)

| Section ID | Label | Icon |
|---|---|---|
| `glossary` | Rules & Glossary | 📖 |
| `glossary_only` | Glossary | 📚 |
| `specials` | Special Properties | 🔖 |
| `races` | Races | 👁 |
| `backgrounds` | Backgrounds | 📜 |
| `occupations` | Occupations | 💼 |
| `skills` | Skills | 🎯 |
| `talents` | Talents | ⚡ |
| `evolutions` | Evolutions | 🧬 |
| `weapons` | Weapons | 🔫 |
| `weapon_options` | Weapon Options | 🔧 |
| `armor` | Armor | 🛡 |
| `armor_options` | Armor Options | ⚙ |
| `spells` | Spells | ✨ |
| `datacoms` | Datacoms | 📡 |
| `hacking` | Hacking Software | 💻 |
| `vehicles` | Vehicles | 🚗 |
| `cat_drones` | Drones | 🤖 |
| `modules` | Modules | 🔧 |
| `ships` | Spaceships | 🚀 |
| `ship_components` | Ship Components | ⚙ |
| `equipment` | Equipment | 🎒 |
| `medical` | Medical | 💉 |

**New in v8:** `glossary_only` (flat glossary view from `g.glossary_clean`), `vehicles`, `cat_drones`, `modules`, `ships`, and `ship_components` (all sourced from `g.catalog`).

### Rule Groups (in `rules_grouped`)

| Group | Key Sections |
|---|---|
| CREATING A CHARACTER | Character creation steps |
| CHARACTER ADVANCEMENT | XP, levelling |
| BASIC RULES | Core mechanics, combat, actions |
| ARMORS | Armor rules |
| WEAPONS | Weapon rules |
| MAGIC | Spell rules |
| HACKING AND DRONES | Hacking, drone control |
| EVOLUTION | Genetics, cybernetics, magic evolutions |
| GLOSSARY | In-rules glossary |
| SPACE COMBAT | Ship combat job order, roles, movement, damage, environment |

The **SPACE COMBAT** group covers: job order, all five ship roles (Commander/Engineer/Navigator/Pilot/Gunner), role advantage/disadvantage, space movement & sensor ranges, damage/trauma/repairs, environmental rules (gravity, suffocation), and galactic regions.

---

## Manufacturer System

Weapons, armor, datacoms, and medical items support manufacturer variants that modify stats:

**Weapon manufacturers (v8):**
`Generic`, `Malivaux`, `Kintech`, `Nakamura`, `Arms Corp`, `Zang'Hai`, `TORC`, `Voran`, `Dilithium`, `Monomolecular`

- `Dilithium` and `Monomolecular` are melee-only manufacturers (`WPN_MFRS_MELEE_ONLY` set)
- Melee categories tracked in `MELEE_CATS` set

**Armor manufacturers (v8):**
`Generic`, `Harsh`, `Santech`, `BMS`, `Acer`

**Datacom manufacturers (v8):**
`Generic`, `Securicorp`, `Orionworks`, `Biocom`, `Carnifex`, `Saiko`, `Yotoma`

The `mfrState` object tracks the selected manufacturer per section. The `applyWpnMfr` / `applyArmorMfr` / `applyMedMfr` functions return a modified copy of an item with adjusted stats.

---

## CSS Class Conventions

### Tag/Badge Colors
| Class | Color | Meaning |
|---|---|---|
| `.tb` | Cyan (`--a`) | Tech/Blue tags |
| `.to` | Orange (`--a2`) | Orange/physical tags |
| `.tp` | Purple (`--a3`) | Purple/energy/limited tags |
| `.tg` | Green (`--gr`) | Green/uncommon tags |
| `.ty` | Yellow (`--ye`) | Yellow/restricted tags |
| `.tr` | Red (`--re`) | Red/danger/illegal tags |
| `.tgr` | Muted (`--mu`) | Grey/neutral tags |
| `.tw` | White (faint) | Common/no-permit tags |

### Availability / Rarity Card Classes (v8)
Applied to `.card` elements to tint the card left-border by availability tier:
| Class | Availability | Color |
|---|---|---|
| `.rar-common` | Common | White (subtle) |
| `.rar-uncommon` | Uncommon | Green |
| `.rar-rare` | Rare | Blue |
| `.rar-limited` | Limited | Purple |
| `.rar-unique` | Unique | Yellow |
| `.rar-classified` | Classified | Red |

Use `rarCls(item.availability)` to obtain the correct class string.

### Defense Tier Pills (v8)
`.def-pill` is a base pill component; pair with a `.dp-*` modifier for color:
| Class | Tier | Color |
|---|---|---|
| `.dp-none` | None/— | Dark muted |
| `.dp-low` | Low | Dim green |
| `.dp-medium` | Medium | Bright green |
| `.dp-high` | High | Yellow |
| `.dp-extreme` | Extreme | Red |

Use `defCls(tier)` to obtain the correct class string.

### Layout Classes
| Class | Purpose |
|---|---|
| `.grid` | Auto-fill grid, min 310px per column |
| `.grid2` | Auto-fill grid, min 360px per column |
| `.list` | Vertical flex list |
| `.card` | Expandable content card (toggled via `data-tog` attribute in v8) |
| `.card.x` | Expanded card state |
| `.gitem` | Glossary/list row item |
| `.fbar` | Filter bar container |
| `.fc` | Filter chip button |
| `.fc.active` | Selected filter chip |
| `.rule-group` | Collapsible rule group |
| `.rule-group.open` | Open rule group |

### Card Sub-layout Classes (v8)
| Class | Purpose |
|---|---|
| `.cr2` | Second card row — flex wrap, for manufacturer/availability pills |
| `.cr3` | Third card row — space-between flex, left pills + right price |
| `.cr3l` | Left side of `.cr3` — stat/special pills |
| `.cr3r` | Right side of `.cr3` — price in green monospace |
| `.cs-right` | Right-aligned subtitle (size, class, etc.) in card header |

### Weapon/Item Pill Classes (v8)
| Class | Purpose |
|---|---|
| `.wpn-pills` | Container for a row of pills |
| `.wpn-pill` | Generic item info pill (neutral) |
| `.wpill-dmg` | Damage value pill (orange) |
| `.wpill-pwr` | Power/energy pill (yellow) |
| `.wpill-cst` | Cost pill (green) |
| `.wpill-avl` | Availability pill (muted) |

### Data Display Classes
| Class | Purpose |
|---|---|
| `.fg` | Stats grid (field group) |
| `.f` | Single stat field |
| `.fl` | Field label |
| `.fv` | Field value |
| `.hl` | Search highlight span |
| `.stab` | Stats table (races) |
| `.opt-table` | Options table (weapon/armor options) |

---

## Development Conventions

### Making Changes

Since each file is self-contained, the workflow for modifications is:

1. **Edit the HTML file directly** — all CSS, HTML structure, JS logic, and data live in a single file
2. **Open in a browser** to verify changes — no build step needed
3. **Test search** — the `ms()` function checks all relevant data fields; ensure new data fields are included in search calls
4. **Test all manufacturer variants** — if adding a new item type with manufacturers, test each mfr variant

### Adding New Data Entries

Data is embedded in the `g` object literal inside `<script>`. When adding entries:

- Follow the existing object structure for that data type exactly
- Ensure all fields the `render()` function references are present (use `null` if not applicable)
- Add new items to the appropriate array within `g`
- If adding a new category, add it to the category filter logic in `render()`

### Adding New Sections

To add a new navigation section:

1. Add a `<button class="nb" data-s="section_id">` in the `<aside>` nav
2. Add a corresponding `else if(cs==='section_id'){...}` branch in `render()`
3. Add the section's data to the `g` object
4. Ensure the search `ms()` call covers all relevant fields

### CSS Changes

- All colors must use CSS custom properties from `:root` — do not hardcode colors
- New UI components should follow existing class naming patterns
- CSS is written minified/compact inline — maintain that style for consistency

### Card Interaction Pattern (v8)

In v8, cards use a `data-tog` attribute instead of inline `onclick`. The main event listener delegates clicks:

```js
const card = e.target.closest('[data-tog]');
if (card) tog(card.dataset.tog);
```

Card structure:
```html
<div class="card [rar-*]" id="cID" data-tog="ID">
  <div class="ch">Name <span class="xi">▼</span></div>  <!-- always visible header -->
  <div class="cr2">…pills…</div>                        <!-- always visible row 2 -->
  <div class="cr3"><div class="cr3l">…</div><div class="cr3r">price</div></div>
  <div class="cb">…expanded content…</div>              <!-- hidden until toggled -->
</div>
```

CSS: `.cb{display:none}` / `.card.x .cb{display:block}`. The `.cb` class is the v8 expand container — do **not** use `.exp`/`.exb` (those were older patterns).

### Ship Component System (v8)

Ship components are the building blocks installed in spaceship slot lists (`core[]`, `internal[]`, `external[]`). Each entry is a component code string in the format:

```
TYPE_CLASSIDX-CLASS_TIERIDX-QUALITY
```

Example: `ENGINEBALANCED_4-FRIGATE_2-AVERAGE`

#### Key data structures

| Constant | Purpose |
|---|---|
| `COMP_NAMES` | Map of type key → human display name (44 types) |
| `COMP_Q` | Map of quality string → integer index (BASIC:0, AVERAGE:1, GOOD:2, UNIVERSAL:3, …) |
| `COMP_QCOL` | Map of quality → inline CSS style string for badge coloring |
| `COMP_CC` | Stat contributions per component type: `{stat:[base, per_q], …}` — value = base + per_q × q |
| `ENG_SPD` | Engine types → speed base tier (all currently 2 = LOW); speed = base + q |
| `SPD_STR` | Speed tier index → string: `['NONE','VERY LOW','LOW','MEDIUM','HIGH','VERY HIGH','ULTRA']` |
| `SHIP_BASE` | Per-class base stats: `{structure, hull, crew_min, command}` |
| `SENSOR_MULT` | Per-class sensor range multiplier (CORVETTE=1×, scaling to NOVA=32×) |
| `SCOMP_DEF` | Compact component catalog: see below |
| `SCOMP_CLASSES` | `['DRONE','FIGHTER','CORVETTE','FRIGATE','CRUISER','BATTLECRUISER','CARRIER','NOVA']` |
| `SCOMP_TIERS` | `['BASIC','AVERAGE','GOOD']` |

#### SCOMP_DEF schema

Each entry in `SCOMP_DEF` has:
```js
TYPE_KEY: {
  name: 'Display Name',
  classes: 'ALL' | ['CLASS', ...],  // which ship classes can use this
  unit: [d,f,c,fr,cr,bc,ca,no],    // unit space per class [DRONE..NOVA]
  pwr:  [d,f,c,fr,cr,bc,ca,no],    // power draw per class
  price:[d,f,c,fr,cr,bc,ca,no],    // credit cost per class
  tiers:[{statKey:value,...}, ...], // stat bonuses for [BASIC, AVERAGE, GOOD]
}
```

A zero `unit` AND zero `price` for a class index means that class cannot use the component.

#### calcShip(comps, cls)

Accumulates all stat contributions for a ship's component list and ship class:
1. Iterates each component code, parses type/quality, looks up `COMP_CC`
2. Applies `stat += (base + per_q * q) * count` for all stats
3. Engine speed: `tier = ENG_SPD[type] + q`; multiple engines stack (each adds +1 tier)
4. After accumulation: scales sensor ranges by `SENSOR_MULT[cls]`; sets `detect_range`/`max_range` to `null` for DRONE/FIGHTER respectively
5. Falls back to `CLASS_MIN_SPD[cls]` (all = 2 = LOW) if no engine found

#### Speed tiers (engines only)

Engine quality maps directly to speed: BASIC → LOW, AVERAGE → MEDIUM, GOOD → HIGH. A second engine of any type adds +1 tier. No ship should show VERY LOW or NONE (minimum fallback is LOW).

#### Sensor ranges

Ranges in `COMP_CC` are defined at **CORVETTE scale (1×)**. `calcShip` multiplies them by `SENSOR_MULT`:

| Class | Multiplier |
|---|---|
| DRONE | 0.1× |
| FIGHTER | 0.3× |
| CORVETTE | 1× |
| FRIGATE | 2× |
| CRUISER | 4× |
| BATTLECRUISER | 8× |
| CARRIER | 16× |
| NOVA | 32× |

DRONEs only have combat range (detect/max = null). FIGHTERs have combat + detect (max = null).

#### Three radar types

| Type | Corvette combat | Corvette detect | Corvette max | Instruments (per quality) |
|---|---|---|---|---|
| `RADAR` | 100 | 1 000 | 10 000 | +1 / +2 / +3 |
| `RADAR_COMBAT` | 300 | 3 000 | 9 000 | 0 / +1 / +2 |
| `RADAR_DEEPSPACE` | 50 | 5 000 | 50 000 | +2 / +3 / +4 |

Quality only affects `instruments` bonus; range values are fixed per type.

#### buildShipComps()

Expands `SCOMP_DEF` into the flat `g.catalog.ship_components` array at startup. Each entry has:

```js
{id, type, name, ship_class, quality, unit_size, pwr_draw, price, stats:{…}}
```

The full catalog is also exported as `ship_components.csv` in the repo root (34 columns, ~768 rows).

#### Helper functions for components

| Function | Purpose |
|---|---|
| `pComp(code)` | Parse a component code string → `{type, quality}` |
| `compLine(code)` | Render a component as a name + quality badge HTML string |
| `qBadge(q)` | Render a standalone quality badge HTML span |

### Ship Classes (v8)

Spaceships in `g.catalog.ships` are grouped by `class` field and rendered in this order:
`DRONE` → `FIGHTER` → `CORVETTE` → `FRIGATE` → `CRUISER` → `BATTLECRUISER` → `CARRIER` → `NOVA`

Each ship has three slot lists: `core[]`, `internal[]`, `external[]` with corresponding `*_size` fields. Component names use `snake_case` and are humanized for display.

### Versioning Convention

New versions are created as new files: `56th_century_compendium_vN.html`. When creating a new version:
- Copy the latest version file and rename it
- Do not modify old version files
- v8 is the current latest

---

## No Build System

There is no:
- Package manager (no `package.json`, `requirements.txt`, etc.)
- Build tool (no webpack, vite, rollup, etc.)
- Test framework
- Linter/formatter configuration
- CI/CD pipeline

All development is edit-and-refresh in a browser.

---

## Key Design Decisions

1. **Single-file delivery** — The entire compendium (data + UI + logic) ships in one HTML file for maximum portability and ease of distribution
2. **No external runtime dependencies** — Works offline except for Google Fonts (cosmetic only)
3. **Data-driven rendering** — All sections are rendered dynamically by a single `render()` function rather than static HTML
4. **Manufacturer modifiers** — Stats are computed at render time by applying manufacturer transforms to base item data, keeping the data layer clean
5. **Search is global** — The search bar filters across the currently active section; switching sections clears search
6. **CSS custom properties** — The entire visual theme can be changed by editing `:root` variables
