# 02 — Architecture

## System diagram

```
56th_century_compendium_v8.html
│
├── <style>          CSS custom properties (:root palette) + all layout rules
├── <body>
│   ├── <header>     Title bar + global search input + section nav tabs
│   ├── <aside>      Sidebar nav — <button data-s="section_id"> per section
│   ├── <div id="main">  Dynamic content area — rewritten by render() on every interaction
│   └── <div id="tt">   Tooltip overlay (absolutely positioned)
└── <script>
    ├── const g = {...}          Master data object (all RPG content — ~2 MB)
    ├── Manufacturer constants   WPN_MFRS, ARMOR_MFRS, DATACOM_MFRS, MEDICAL_MFRS
    ├── Ship/drone constants     SCOMP_DEF, DB_COMP, SCOMP_CLASSES, etc.
    ├── Render pipeline          render() → section-specific renderers
    ├── Character Creator        ccState, ccRender*, ccPickFromCache, ccExportRoll20
    ├── Enemy Generator          egState, egAuto*, egExportVTT
    └── Event delegation         Single click listener on #main (data-tog, data-s, data-cat)
```

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
