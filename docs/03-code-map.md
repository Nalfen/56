# 03 — Code Map

> All code lives in `56th_century_compendium_v8.html`. Line numbers are approximate and shift with edits.

## Navigation sections (sidebar → renderer mapping)

| `data-s` value | Label | Renderer / Logic |
|---|---|---|
| `glossary` | Rules & Glossary | `render()` rules_grouped branch |
| `glossary_only` | Glossary | `g.glossary_clean` flat list |
| `specials` | Special Properties | `g.specials` |
| `galaxy` | Galactic Catalogue | `g.catalogue_systems` + `GALAXY_SECTIONS` |
| `starmap` | Star Map | `initStarmap()`, `g.galaxy[].map_pos`, `STARGATE_LINKS` |
| `factions` | Factions | `g.factions` |
| `gm_tools` | Enemy Generator | `egState`, `EG_ARCHETYPES`, `eg*` functions |
| `races` | Races | `g.races` |
| `backgrounds` | Backgrounds | `g.backgrounds` |
| `occupations` | Occupations | `g.occupations` |
| `skills` | Skills | `g.skills` |
| `talents` | Talents | `g.talents` |
| `evolutions` | Evolutions | `g.evolutions.entries` |
| `weapons` | Weapons | `g.weapons`, `applyWpnMfr`, `WPN_MFRS` |
| `weapon_options` | Weapon Options | `g.options` |
| `armor` | Armor | `g.armor`, `applyArmorMfr`, `ARMOR_MFRS` |
| `armor_options` | Armor Options | `g.options` (armors flag) |
| `ammo` | Ammunition | `g.ammo_types`, `g.ammo_opts`, `AMMO_COMPAT` |
| `spells` | Spells | `g.spells` |
| `datacoms` | Datacoms | `g.datacoms`, `DATACOM_MFRS` |
| `hacking` | Hacking Software | `g.software.{actions,programs,gadgets}` |
| `vehicles` | Vehicles | `g.catalog.vehicles` |
| `cat_drones` | Drones | `g.catalog.drones` |
| `modules` | Modules | `g.catalog.modules` |
| `ships` | Spaceships | `g.catalog.ships`, `calcShip` |
| `ship_components` | Ship Components | `g.catalog.ship_components`, `buildShipComps()` |
| `drone_builder` | Drone Builder | `dbState`, `calcDrone()`, `DB_COMP` |
| `drone_parts` | Drone Parts | `g.catalog.drone_parts`, `buildDroneParts()` |
| `equipment` | Equipment | `g.equipment` |
| `medical` | Medical | `g.medical`, `g.toxic_shock`, `applyMedMfr` |

## `g` object — top-level keys

| Key | Description |
|---|---|
| `g.specials` | Dict of special property codes → `{name, desc}` |
| `g.rules_grouped` | Array of rule groups `{title, sections:[{title, entries:[{key,text}]}]}` |
| `g.glossary_clean` | Flat glossary entries `{name, desc}` |
| `g.code` | Encoded reference entries `{name, desc}` |
| `g.races` | Playable races with stat ranges (`{min,avg,max}` per attribute) |
| `g.backgrounds` | Backgrounds `{name, race, desc, traits[]}` |
| `g.occupations` | Occupations `{name, desc, details[]}` |
| `g.skills` | Skills `{name, category, desc}` |
| `g.talents` | Talents `{name, skill, category, effect, cost}` |
| `g.evolutions` | `{entries:[{name, evo_type, tier, effect}]}` |
| `g.weapons` | Weapons — see schema below |
| `g.armor` | Armor/forcefields/barriers/defensive datacoms — all defensive item types unified here |
| `g.options` | Weapon/armor/datacom options `{name, desc, wpn_ranged, wpn_melee, armors, datacom, availability, legality}` |
| `g.ammo_types` | Ammunition type definitions — displayed in `ammo` section |
| `g.ammo_opts` | Ammunition option modifiers — compatibility matrix data |
| `g.spells` | Spells `{name, school, range, duration, effect}` |
| `g.datacoms` | Datacom devices `{name, cpu, memory, nanites, def_physical, def_energy, def_tech, def_spiritual, special, …}` |
| `g.software` | `{actions[], programs[], gadgets[]}` — used by `hacking` section |
| `g.equipment` | General gear `{name, category, size, effect, cost, availability, legality}` |
| `g.medical` | Medical items with manufacturer variants |
| `g.toxic_shock` | `{rules:'…', table:[{result, name, duration, effect}]}` — displayed in `medical` section |
| `g.manufacturers` | Dict of manufacturer stat modifiers for weapons/armor/datacoms |
| `g.medical_manufacturers` | Dict of manufacturer stat modifiers for medical items |
| `g.catalog.vehicles` | Vehicles |
| `g.catalog.drones` | Drones |
| `g.catalog.chassis` | Drone chassis sizes |
| `g.catalog.modules` | Drone & vehicle modules |
| `g.catalog.ships` | Spaceships `{name, class, role, core[], internal[], external[], …}` |
| `g.catalog.ship_components` | Flat array built at startup by `buildShipComps()` from `SCOMP_DEF` |
| `g.catalog.drone_parts` | Flat array built at startup by `buildDroneParts()` from `DB_COMP` |
| `g.factions` | Faction/organisation lore entries — see schema below |
| `g.galaxy` | Galactic region overview entries with `map_pos` for star map |
| `g.catalogue_systems` | Star system entries with planet lists |

### Rule groups in `g.rules_grouped`
CREATING A CHARACTER · CHARACTER ADVANCEMENT · BASIC RULES · ARMORS · WEAPONS · MAGIC · HACKING AND DRONES · EVOLUTION · GLOSSARY · SPACE COMBAT

---

## Manufacturer constants

| Constant | Members |
|---|---|
| `WPN_MFRS` | Generic, Malivaux, Kintech, Nakamura, Arms Corp, Zang'Hai, TORC, Voran, Dilithium, Monomolecular |
| `WPN_MFRS_MELEE_ONLY` | Set — Dilithium, Monomolecular |
| `MELEE_CATS` | Set of melee weapon category strings (includes Powered Melee) |
| `ARMOR_MFRS` | Generic, Kintech, Harsh, Santech, BMS, Acer |
| `DATACOM_MFRS` | Generic, Securicorp, Orionworks, Biocom, Carnifex, Saiko, Yotoma, Zang'Hai |
| `MEDICAL_MFRS` | Generic, Altair Biomed, RX Generic, Goodman Holistic, Diva Solutions, Mono-Med Customs |

Picker melee filter uses `MELEE_THROW_CATS = new Set(['Melee Weapons (Martial Arts)', 'Ranged / Throwing Weapons (Dexterity)'])` — Powered Melee is intentionally excluded.

Size scales used by `apply*Mfr`:
- `WPN_SIZES = ['Tiny','Small','Medium','Large']` — weapon size (used by `applyWpnMfr`)
- `MED_SIZES = ['TINY','SMALL','MEDIUM','LARGE','EX.LARGE']` — medical item size (used by `applyMedMfr`)

Manufacturers with `size_mod`:
| Manufacturer | Section | size_mod |
|---|---|---|
| Kintech | weapons | +1 |
| Arms Corp | weapons | +1 |
| Securicorp | datacoms | +1 |
| Carnifex | datacoms | +1 |
| Altair Biomed | medical | +1 |
| Goodman Holistic | medical | +1 |
| Diva Solutions | medical | +2 |
| Mono-Med Customs | medical | +5 |

---

## Ammunition system constants

| Constant | Purpose |
|---|---|
| `AMMO_OPT_CODES` | Ordered array of ammo option code strings: `DP, S, HE, LB, AR, STN, FIRE, EMP, CRIT, SB` |
| `AMMO_COMPAT` | IIFE — builds compatibility lookup: ammo type name → Set of compatible option codes |

---

## Ship component system constants

| Constant | Purpose |
|---|---|
| `COMP_NAMES` | Map of type key → human display name (44 types) |
| `COMP_Q` | Quality string → integer index (BASIC:0, AVERAGE:1, GOOD:2, UNIVERSAL:3) |
| `COMP_QCOL` | Quality → inline CSS style string |
| `COMP_CC` | Stat contributions per component type: `{stat:[base, per_q]}` |
| `ENG_SPD` | Engine type → speed base tier |
| `SPD_STR` | Speed tier index → string `['NONE','VERY LOW','LOW','MEDIUM','HIGH','VERY HIGH','ULTRA']` |
| `SHIP_BASE` | Per-class base stats: `{structure, hull, crew_min, command}` |
| `SENSOR_MULT` | Per-class sensor range multiplier (CORVETTE=1× … NOVA=32×) |
| `SCOMP_DEF` | Compact component catalog — expanded by `buildShipComps()` at startup |
| `SCOMP_CLASSES` | `['DRONE','FIGHTER','CORVETTE','FRIGATE','CRUISER','BATTLECRUISER','CARRIER','NOVA']` |
| `SCOMP_TIERS` | `['BASIC','AVERAGE','GOOD']` |
| `STARGATE_LINKS` | Array of `[nameA, nameB]` pairs — drawn as lines on the star map |
| `GALAXY_SECTIONS` | Ordered array grouping catalogue systems by region/colour |

Ship classes rendered in order: `DRONE → FIGHTER → CORVETTE → FRIGATE → CRUISER → BATTLECRUISER → CARRIER → NOVA`.

---

## Drone builder system constants

| Constant | Purpose |
|---|---|
| `DB_SIZES` | Chassis sizes `{TINY,SMALL,MED,LARGE,XL,HUGE}` — each has `{name, slots, max_comp, dur, sys, soak, spd_mod, price, dc}` |
| `DB_MOB` | Mobility types `{STATIC,WALK,CLIMB,HOVER,FLY}` — each has `{name, base_mode, base_spd, alt_mode, alt_spd, price, dc}` |
| `DB_ZONE` | Zone modifiers `{core, internal, external}` — `{label, color, dc_mod, cost_mod, info}` |
| `DB_DEF_RANKS` | `['NONE','LOW','MEDIUM','HIGH','EXTREME']` |
| `DB_SKILLS` | Available skills by attribute — used by SKILL_MODULE picker |
| `DB_COMP` | All drone component definitions — expanded by `buildDroneParts()` at startup |

Zone dc/cost mods: core (+1 DC, ×1.30 cost) · internal (0, ×1.00) · external (−1 DC, ×0.85 cost).

---

## Data schemas

### `g.factions` entry
```js
{ id, name, short, category, subcategory, alignment, hq,
  presence[], desc, known_for[], regions[], status, legal_standing }
```
Faction categories: Megacorporation · Corporation · Political/Religious · Political/Synthetic · Trade Organization · Local Faction · Outlaw.
Alignment badge class (`fAlignCls`): illegal/hostile/criminal → `.tr` · restricted/grey → `.ty` · legal → `.tg` · independent → `.tb` · neutral → `.tw` · defunct → `.tgr`.

> **Note:** `g.factions` is lore only. `g.manufacturers` is the separate dict for stat modifiers applied to items at render time.

### `g.galaxy` entry (region overview)
```js
{ entry_type:'faction', name, tags[], rarity, status, territory, span, discovered,
  population_est, government, desc, history, known_for[], notable_systems[],
  lore_notes[], map_pos:{x,y} }
```
`map_pos` is percentage coordinates on the star map PNG.

### `g.catalogue_systems` entry
```js
{ id, name, region, classification, faction, status, tags[], desc,
  planets:[{ id, name, type, status, statusLabel, atmosphere, atm_note, climate,
    gravity, grav_note, faction, population, demographics, government, tech_level,
    economy, access, access_note, hazards[], notable_locations:[{name,desc}],
    hooks[], desc }] }
```

### `GALAXY_SECTIONS` entry
```js
{ key, factionName, color, sysRegex }
```
Last entry always has `sysRegex: null` (catches unmatched systems as "Others").

---

## Key functions

| Function | Role | Inputs | Outputs/Side effects |
|---|---|---|---|
| `render()` | Main render dispatch | none (reads globals: cs, sq, af) | Rewrites `#main.innerHTML` |
| `ms(array)` | Search match helper | string array | bool — any element contains `sq` |
| `hl(s, q)` | Highlight search match | string, query | HTML string with `.hl` spans |
| `tog(id)` | Toggle card expand | card id string | Toggles `.x` class on `#id` |
| `esc(s)` | HTML-escape | string | safe HTML string |
| `fmt(n)` | Format credits | number | string with space thousands sep |
| `tc(v)` | Tag CSS class | value string | tag class string |
| `rarCls(avail)` | Rarity border class | availability string | `.rar-*` class |
| `defCls(tier)` | Defense pill class | tier string | `.dp-*` class |
| `bst(sp)` | Special property tags | special string | HTML pill string with tooltips |
| `applyWpnMfr(item, mfr)` | Apply weapon mfr mods | item obj, mfr name | Modified item copy (or null if avail exceeded); applies avail, power, damage, range, expertise, size (`WPN_SIZES`), cost, special |
| `applyArmorMfr(item, mfr)` | Apply armor mfr mods | item obj, mfr name | Modified item copy (or null); applies avail, cost, defense tiers, soak, Kintech def-choice bonus |
| `applyMedMfr(item, mfr)` | Apply medical mfr mods | item obj, mfr name | Modified item copy (or null); Mono-Med Customs always sets availability to UNIQUE; others shift via avail_mod |
| `defShift(current, mod)` | Shift defense tier | tier string, numeric mod | New tier string |
| `calcShip(comps, cls)` | Accumulate ship stats | component code array, class string | Stats object |
| `calcDrone(dbState)` | Accumulate drone stats | dbState object | Stats object or null |
| `buildShipComps()` | Expand ship catalog | none | Populates `g.catalog.ship_components` |
| `buildDroneParts()` | Expand drone catalog | none | Populates `g.catalog.drone_parts` |
| `ccExportRoll20()` | Export character to JSON | none (reads ccState) | Downloads Roll20 JSON file |
| `ccPickFromCache(pidx)` | Apply picker selection | picker cache index | Mutates ccState slot (applying `picker.mfr`), calls render() |
| `ccRenderPicker()` | Render browse picker modal | none (reads ccState.picker) | HTML string; includes mfr dropdown for weapon/armor/datacom, applies mfr mods to item previews, filters melee-only mfrs; highlights changed stats orange/yellow (damage, range, soak, size, availability) and green/purple (defense, special) |
| `ccRenderCombat()` | Render Combat tab | none (reads ccState) | HTML string; labeled inputs, mfr-change highlight coloring, bst() hoverable special tags |
| `ccRenderTech()` | Render Tech tab | none (reads ccState) | HTML string; labeled inputs, bst() hoverable special tags on datacoms |
| `ccAutoTrackedSpent()` | Sum auto-tracked costs | none (reads ccState) | number — total credits for weapons+armor+datacoms+evos |
| `ccCalcWeaponCost(wp)` | Weapon credit cost | weapon slot object | number |
| `ccCalcArmorCost(ar)` | Armor/defense credit cost | armor slot object | number |
| `ccCalcDatacomCost(dc)` | Datacom credit cost | datacom slot object | number |
| `ccCalcEvoCreditCost(e)` | Evolution credit cost | evo slot object | number (0 if free/bg_granted) |
| `egExportVTT()` | Export enemy to VTT-ES JSON | none (reads egState) | Downloads JSON file |

## Milestone 6.0 constants

| Constant | Purpose |
|---|---|
| `OCC_BONUS` | Dict of occupation name → `[[skillA, skillB], [skillC, skillD]]` — the two skill-pair options the player chooses from at character creation for a SMALL passive bonus |

---

## Character Creator state (`ccState`) — key fields

| Field | Type | Description |
|---|---|---|
| `tab` | string | Active tab: `'origin'`, `'attributes'`, `'advancement'`, `'combat'`, `'tech'`, `'magicgear'` |
| `weapons[6]` | array | Weapon slots: `{name, skill, dmg, dmgtype, power, expertise, special, close_range, medium_range, long_range, rof, ammo, currentammo, reload, mfr, base_data, options[]}` |
| `armor[2]` | array | Defense slots: `{name, type, def_phys/energy/tech/spirit, special, soak_expr, charges, regen, mfr, base_data, options[]}` |
| `datacoms[3]` | array | Datacom slots: `{name, cpu, mem, nanite, def_phys/energy/tech/spirit, def_dmg, int_ext/int_int/int_main, expertise, special, mfr, base_data, options[]}` — note: `nanite` in state vs `nanites` in `g.datacoms` data; `def_phys` in state vs `def_physical` in data |
| `evolutions[]` | array | `{name, type, tier, effect, credited, bg_granted?, free?}` |
| `talents[]` | array | `{name, skill, category, xp_cost, effect, credited, bg_granted?}` |
| `credits` | number | Starting budget |
| `credits_spent` | number | Manual gear purchases (Gear Shop) |
| `occupation_bonus_choice` | null \| 0 \| 1 | Which skill-pair bonus the player picked from `OCC_BONUS[occupation]`; null = not yet chosen |
| `picker` | obj/null | Active picker: `{type, slot, mfr?}` — `mfr` tracks selected manufacturer inside the picker window |
| `bg_choices[]` | array | Pending background skill choices |

## Data schemas

### g.weapons item
| Field | Type | Example |
|---|---|---|
| name | string | `"Pulse Rifle"` |
| category | string | `"Rifles (Marksman)"` |
| damage | string | `"4D + 2"` |
| type | string | `"ENERGY"` |
| cost | string | `"45000"` |
| range_short / range_med / range_long | string | `"50"`, `"200"`, `"500"` |
| rof | string | `"3"` |
| ammo | string | `"30"` |
| reload | string | `"Standard"` |
| power | string | `"High"` |
| power_num | number | `9` |
| max_dice / min_dice | number | `6`, `2` |
| size | string | `"Small"` — Tiny / Small / Medium / Large |
| special | string | `"OPT AUTO"` |
| availability | string | `"UNCOMMON"` |
| legality | string | `"Legal"` |

### g.armor item
| Field | Type | Example |
|---|---|---|
| name | string | `"Combat Vest"` |
| type | string | `"Light Armor"` / `"Combat Forcefield"` / `"Basic Datacom"` |
| category | string | `"Armors"` |
| cost | string | `"12000"` |
| soak / soak_max / soak_min | string / number | `"2D + 1"`, `3`, `1` |
| def_physical / def_energy / def_tech / def_spiritual | string | `"LOW"` / `"NONE"` |
| special | string | `"OPT"` |
| availability | string | `"COMMON"` |

### g.evolutions.entries item
| Field | Type | Example |
|---|---|---|
| name | string | `"Subdermal Plating"` |
| evo_type | string | `"GENETICS"` |
| tier | string | `"TIER II"` |
| cost | number | `50000` |
| effect | string | `"..."` |
| availability | string | `"UNCOMMON"` |
| legality | string | `"Legal"` |
