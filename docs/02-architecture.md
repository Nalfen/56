# 02 — Architecture

## Delivery modes

There are two builds. Both share the same JS renderer and `g` data object interface:

| Mode | Canonical file | Data source | Hosting |
|---|---|---|---|
| **Embedded** | `56th_century_compendium.html` | `const g = {...}` inline in `<script>` | `file://` or HTTP |
| **Data-driven** | `56th_century_compendium_v11.html` | `data/v8/*.json` fetched on load | HTTP only |

### Embedded-data diagram

```
56th_century_compendium.html
│
├── <style>          CSS custom properties (:root palette) + all layout rules
├── <body>
│   ├── <header>     Title bar + global search input + section nav tabs
│   ├── <aside>      Sidebar nav — <button data-s="section_id"> per section
│   ├── <div id="main">  Dynamic content area — rewritten by render() on every interaction
│   └── <div id="tt">   Tooltip overlay (absolutely positioned)
└── <script id="main-src">
    ├── const g = {...}          Master data object (all RPG content — ~2 MB inline)
    ├── Manufacturer constants   WPN_MFRS, ARMOR_MFRS, DATACOM_MFRS, MEDICAL_MFRS
    ├── Ship/drone constants     SCOMP_DEF, DB_COMP, SCOMP_CLASSES, etc.
    ├── Render pipeline          render() → section-specific renderers
    ├── Character Creator        ccState, ccRender*, ccPickFromCache, ccExportRoll20
    ├── Enemy Generator          egState, egAuto*, egExportVTT
    └── Event delegation         Single click listener on #main (data-tog, data-s, data-cat)
```

### Data-driven load path (v11, canonical)

```
Browser opens 56th_century_compendium_v11.html
  → Boot script shown (loading spinner / progress bar)
  → fetch('data/v8/manifest.json')
     → reads man.files array (11 filenames)
  → Promise.all(files.map(fn => fetch('data/v8/' + fn)))
     → each JSON merged into window.__DATA via Object.assign-style loop
  → <script id="main-src"> text is injected as a new <script> element
     → const g = window.__DATA          ← single line; g is the merged payload
     → Manufacturer constants, SCOMP_DEF, DB_COMP, etc. (still inline)
     → render pipeline, CC, EG, event delegation (identical to embedded build)
  → Boot overlay fades out; render() called to show default section
```

Key difference: the data-driven build keeps all generator constants (`SCOMP_DEF`, `DB_COMP`, `EG_ARCHETYPES`, etc.) inline in the HTML because they are code parameters, not content. Only flat content arrays live in JSON.

## Request flow (user interaction)

```
User clicks sidebar nav button
  → sets cs (current section string)
  → calls render()
     → clears #main.innerHTML
     → dispatches to section renderer (e.g. ccRenderCombat, render weapons, etc.)
     → injects HTML string
  → event delegation on #main handles all clicks/changes inside rendered HTML
```

## Component descriptions

### `const g` — Master data object
Owns all RPG content: weapons, armor, spells, skills, talents, evolutions, datacoms, equipment, medical items, ships, vehicles, drones, factions, galaxy, star systems. Never mutated at runtime — renderers read it and manufacturer functions produce modified copies.

### `render()` — Main render function
Sole writer to `#main.innerHTML`. Reads `cs` (section), `sq` (search query), `af` (active filter). Dispatches to sub-renderers. Called on every state mutation.

### Character Creator (`ccState` + `cc*` functions)
Stateful interactive form. `ccState` is a plain JS object. All mutations call `render()`. `ccExportRoll20()` serializes state to Roll20 JSON. Does NOT persist to server — export is the save mechanism.

### Manufacturer system (`applyWpnMfr`, `applyArmorMfr`, `applyMedMfr`)
Pure functions that take a base item + manufacturer name and return a modified copy with adjusted stats (damage, range, defense tiers, cost, special properties). Applied at render time; base data is stored in `base_data` field of each slot.

### Enemy Generator (`egState` + `eg*` functions)
Procedural NPC builder. Stateful but ephemeral (no persistence). Exports to VTT-ES JSON.

### Ship/Drone builder systems
`calcShip(comps, cls)` and `calcDrone(dbState)` accumulate stats from component lists. `buildShipComps()` and `buildDroneParts()` expand compact definition constants into flat catalogs at startup.

### Event delegation
One `click` and `change` listener on `document`. Routes `data-tog` (card expand), `data-s` (nav), `data-cat` (filter chips). No inline `onclick` except in dynamically rendered character creator HTML.

---

## Card interaction pattern (v8)

Cards use `data-tog` attribute; the main listener delegates:
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
`.cb{display:none}` / `.card.x .cb{display:block}`. Do NOT use `.exp`/`.exb` (older patterns, removed in v8).

---

## CSS class conventions

### Tag / Badge colours
| Class | Colour | Meaning |
|---|---|---|
| `.tb` | Cyan `--a` | Tech/Blue |
| `.to` | Orange `--a2` | Physical |
| `.tp` | Purple `--a3` | Energy/limited |
| `.tg` | Green `--gr` | Uncommon |
| `.ty` | Yellow `--ye` | Restricted |
| `.tr` | Red `--re` | Danger/illegal |
| `.tgr` | Muted `--mu` | Grey/neutral |
| `.tw` | White (faint) | Common |

### Availability / Rarity card border classes
Applied to `.card` elements via `rarCls(item.availability)`:
| Class | Availability |
|---|---|
| `.rar-common` | Common |
| `.rar-uncommon` | Uncommon |
| `.rar-rare` | Rare |
| `.rar-limited` | Limited |
| `.rar-unique` | Unique |
| `.rar-classified` | Classified |

### Defense tier pill classes
Base `.def-pill` + modifier from `defCls(tier)`:
| Class | Tier |
|---|---|
| `.dp-none` | None/— |
| `.dp-low` | Low |
| `.dp-medium` | Medium |
| `.dp-high` | High |
| `.dp-extreme` | Extreme |

### Layout classes
| Class | Purpose |
|---|---|
| `.grid` | Auto-fill grid, min 310 px per column |
| `.grid2` | Auto-fill grid, min 360 px per column |
| `.list` | Vertical flex list |
| `.card` | Expandable content card |
| `.card.x` | Expanded card state |
| `.gitem` | Glossary/list row item |
| `.fbar` | Filter bar container |
| `.fc` | Filter chip button |
| `.fc.active` | Selected filter chip |
| `.rule-group` | Collapsible rule group |
| `.rule-group.open` | Open rule group |

### Card sub-layout classes
| Class | Purpose |
|---|---|
| `.cr2` | Second card row — flex wrap, manufacturer/availability pills |
| `.cr3` | Third card row — space-between, left pills + right price |
| `.cr3l` | Left side of `.cr3` |
| `.cr3r` | Right side of `.cr3` — price in green monospace |
| `.cs-right` | Right-aligned subtitle in card header |

### Weapon/item pill classes
| Class | Purpose |
|---|---|
| `.wpn-pills` | Container for a row of pills |
| `.wpn-pill` | Generic item info pill (neutral) |
| `.wpill-dmg` | Damage value pill (orange) |
| `.wpill-pwr` | Power/energy pill (yellow) |
| `.wpill-cst` | Cost pill (green) |
| `.wpill-avl` | Availability pill (muted) |

### Data display classes
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

## Development conventions

### Making changes
1. Edit `56th_century_compendium_v8.html` directly — all CSS, HTML, JS, and data live in one file.
2. Open in a browser to verify — no build step needed.
3. Test search — `ms()` checks all relevant data fields; ensure new data fields are included.
4. Test all manufacturer variants if adding a new item type.
5. **Update `docs/03-code-map.md` and `docs/05-decisions-and-issues.md` in the same response as any code change.**

### Adding new data entries
- Follow the existing object structure for that data type exactly.
- Ensure all fields the `render()` function references are present (use `null` if not applicable).
- If adding a new category, add it to the category filter logic in `render()`.

### Adding new sections
1. Add `<button class="nb" data-s="section_id">` in `<aside>`.
2. Add `else if(cs==='section_id'){...}` branch in `render()`.
3. Add data to `g` object.
4. Ensure `ms()` call covers all relevant fields.

### CSS changes
- All colours must use CSS custom properties from `:root` — no hardcoded colours.
- New components follow existing class naming patterns.
- CSS is written minified/compact inline — maintain that style.

### Versioning convention
New versions are new files: `56th_century_compendium_vN.html`. Copy the latest, rename it, never modify old versions. v11 is the current active version. `archive/` is read-only. `v10` was an abandoned intermediate and is not used.
