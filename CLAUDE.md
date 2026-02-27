# CLAUDE.md — 56th Century Compendium

## Project Overview

This repository contains the **56th Century Compendium**, a self-contained browser-based reference tool for the *56th Century* tabletop RPG system. The compendium is delivered as single-file HTML documents with all data, styles, and logic embedded inline — no build system, no external dependencies (except Google Fonts via CDN), and no server required.

The project is released under **CC0 1.0 Universal** (public domain).

---

## Repository Structure

```
/
├── 56th_century_compendium_v3.html   # Version 3 (431 lines, earlier iteration)
├── 56th_century_compendium_v5.html   # Version 5 (838 lines, current/latest)
└── LICENSE                            # CC0 1.0 Universal
```

**v5 is the canonical/latest version.** Work on v5 unless explicitly told otherwise. v3 is kept for reference.

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
| `tog(id)` | Toggle `.x` class on a card (expand/collapse) |
| `esc(s)` | HTML-escape a string |
| `tc(v)` | Convert numeric defense modifier to text tier |
| `descHtml(str, sq)` | Render description with search highlights |
| `applyWpnMfr(item, mfr)` | Apply manufacturer stat modifiers to a weapon |
| `applyArmorMfr(item, mfr)` | Apply manufacturer stat modifiers to armor |
| `applyMedMfr(item, mfr)` | Apply manufacturer stat modifiers to medical items |
| `defShift(current, mod)` | Shift a defense tier by a numeric modifier |
| `mfrBar(sec, list, cur)` | Render the manufacturer selector bar HTML |
| `fcBtn(label, val, cur)` | Render a filter chip button HTML |
| `bst(sp)` | Parse and render special property tags with tooltips |

---

## Data Structure (`g` object)

All game data lives in the `const g = {...}` constant. Top-level keys:

| Key | Description |
|---|---|
| `g.specials` | Dictionary of weapon/ability special property codes → `{name, desc}` |
| `g.rules_grouped` | Array of rule groups, each with `{title, sections:[{title, entries:[{key,text}]}]}` |
| `g.code` | Encoded reference entries `{name, desc}` |
| `g.races` | Array of playable races with stats (PHYS, ACUITY, MENTAL, SOCIAL, ENDUR, SPEED, WITS, WILL — each as `{min,avg,max}`) |
| `g.backgrounds` | Character backgrounds `{name, race, desc, traits:[]}` |
| `g.occupations` | Occupations `{name, desc, details:[]}` |
| `g.skills` | Skills `{name, category, desc}` |
| `g.talents` | Talents `{name, skill, category, effect}` |
| `g.evolutions` | `{entries:[{name, evo_type, tier, effect}]}` |
| `g.weapons` | Weapons `{name, category, type, damage, range, legality, special, notes, desc, variants:{}}` |
| `g.armor` | Armor items with defense values and manufacturer variants |
| `g.options` | Weapon/armor options `{name, desc, wpn_ranged, wpn_melee, availability, legality}` |
| `g.spells` | Spells with school, range, duration, effect |
| `g.datacoms` | Datacom devices with manufacturer variants |
| `g.medical` | Medical items with manufacturer variants |

---

## Navigation Sections (v5)

| Section ID | Label | Icon |
|---|---|---|
| `glossary` | Rules & Glossary | 📖 |
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
| `equipment` | Equipment | 🎒 |
| `medical` | Medical | 💉 |

v3 additionally has separate `magic_rules`, `hacking_ref`, and `evo_rules` sections that v5 consolidates into the `glossary` section via collapsible rule groups.

---

## Manufacturer System

Weapons, armor, datacoms, and medical items support manufacturer variants that modify stats:

**Weapon manufacturers (v5):**
`Generic`, `Malivaux`, `Kintech`, `Nakamura`, `Arms Corp`, `Zang'Hai`, `TORC`, `Voran`, `Dilithium`, `Monomolecular`

- `Dilithium` and `Monomolecular` are melee-only manufacturers (`WPN_MFRS_MELEE_ONLY` set)

**Armor manufacturers (v5):**
`Generic`, `Harsh`, `Santech`, `BMS`, `Acer`

The `mfrState` object tracks the selected manufacturer per section. The `applyWpnMfr` / `applyArmorMfr` / `applyMedMfr` functions return a modified copy of an item with adjusted stats.

---

## CSS Class Conventions

### Tag/Badge Colors
| Class | Color | Meaning |
|---|---|---|
| `.tb` | Cyan (`--a`) | Tech/Blue tags |
| `.to` | Orange (`--a2`) | Orange tags |
| `.tp` | Purple (`--a3`) | Purple tags |
| `.tg` | Green (`--gr`) | Green tags |
| `.ty` | Yellow (`--ye`) | Yellow tags |
| `.tr` | Red (`--re`) | Red/danger tags |
| `.tgr` | Muted (`--mu`) | Grey/neutral tags |

### Layout Classes
| Class | Purpose |
|---|---|
| `.grid` | Auto-fill grid, min 310px per column |
| `.grid2` | Auto-fill grid, min 360px per column |
| `.list` | Vertical flex list |
| `.card` | Expandable content card |
| `.card.x` | Expanded card state |
| `.gitem` | Glossary/list row item |
| `.fbar` | Filter bar container |
| `.fc` | Filter chip button |
| `.fc.active` | Selected filter chip |
| `.rule-group` | Collapsible rule group |
| `.rule-group.open` | Open rule group |

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

### Versioning Convention

New versions are created as new files: `56th_century_compendium_vN.html`. When creating a new version:
- Copy the latest version file and rename it
- Do not modify old version files
- v5 is the current latest

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
