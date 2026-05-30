# 03 — Code Map

> All code lives in `56th_century_compendium_v8.html`. Line numbers are approximate and shift with edits.

## Character Creator tabs (`char_creator` section)

| Tab ID | Label | Renderer | Notes |
|---|---|---|---|
| `identity` | Identity | `ccRenderIdentity()` | Default tab; contains full attribute editor + origin block + detail boxes |
| `skills` | Skills | `ccRenderSkills()` | |
| `talents` | Talents & Evos | `ccRenderTalents()` | Passive Abilities panel at bottom |
| `combat` | Combat | `ccRenderCombat()` | Background Combat Notes panel at bottom |
| `tech` | Tech | `ccRenderTech()` | |
| `magic` | Magic | `ccRenderMagicGear()` | |
| `gear` | Gear | `ccRenderMagicGear()` | Same renderer as Magic, different branch |

`'attributes'` tab was removed in M7.0. Any `ccState.tab === 'attributes'` is silently redirected to `'identity'` in the render dispatch.

---

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
| `ccApplyOccBonus(pi, newPicks?)` | Apply occupation skill bonuses | `pi` = pair/pick index or null; `newPicks` = explicit picks array (optional) | Clears old OCC bonuses, applies new ones to `sk_bonus`, writes `occ_bonus_skills`, `occ_bonus_picks`, `occupation_bonus_choice` |
| `ccToggleOccPick(sk)` | Toggle a skill in pick-N selection | skill key string | Adds/removes from `occ_bonus_picks`, calls `ccApplyOccBonus`, calls `render()` |
| `ccRenderPicker()` | Render browse picker modal | none (reads ccState.picker) | HTML string; sorted A-Z for background/occupation types; includes mfr dropdown for weapon/armor/datacom; effect text shown for talent/evo types; highlights changed stats |
| `ccRenderIdentity()` | Render Identity tab (merged with Attributes, M7.0) | none (reads ccState) | HTML string. Structure: (1) Origin block full-width, (2) 2-col grid: left=identity fields, right=full attribute table with XP costs + racial range, (3) full-width Health/Morale/CHI + Initiative row, (4) detail boxes: Background (traits grid + notes), Occupation (bonus picker + notes), Racial Traits (racial/evolution/environment), Evolution Attribute Notes |
| `ccRenderOriginBlock()` | Render Clone Vat / Natural Birth selector | none (reads ccState) | HTML string; shows selection UI when `clone===null`, compact status bar when chosen |
| `ccRenderAttributes()` | (Dead code — M7.0) | — | Was the standalone Attributes tab renderer; route redirected to `ccRenderIdentity()`. Retained in file but no longer called. |
| `ccRenderSkills()` | Render Skills tab | none (reads ccState) | HTML string; OCC pill on skills with `occ_bonus_skills` bonus; ◆ crit pill on skills with non-default crit range |
| `ccRenderTalents()` | Render Talents & Evos tab | none (reads ccState) | HTML string; effect text shown beneath each slot; Passive Abilities panel at bottom (auto-compiled from active talents + evos, grouped by talent category / evo type) |
| `ccRenderCombat()` | Render Combat tab | none (reads ccState) | HTML string; Background Combat Notes panel at bottom (BENEFIT 1/2/DRAWBACK cards, color-coded) |
| `ccRenderTech()` | Render Tech tab | none (reads ccState) | HTML string; labeled inputs, bst() hoverable special tags on datacoms |
| `ccAutoTrackedSpent()` | Sum auto-tracked costs | none (reads ccState) | number — total credits for weapons+armor+datacoms+evos |
| `ccCalcWeaponCost(wp)` | Weapon credit cost | weapon slot object | number |
| `ccCalcArmorCost(ar)` | Armor/defense credit cost | armor slot object | number |
| `ccCalcDatacomCost(dc)` | Datacom credit cost | datacom slot object | number |
| `ccCalcEvoCreditCost(e)` | Evolution credit cost | evo slot object | number (0 if free/bg_granted) |
| `ccRecalcHealthMorale()` | Recalculate resource maximums | none (reads ccState) | Mutates `HEALTH_max`, `MORALE_max`, `CHI_max`; respects `bgGrant.chi_lock`, `bgGrant.health/morale/chi` |
| `egExportVTT()` | Export enemy to VTT-ES JSON | none (reads egState) | Downloads JSON file |

## Milestone 6.0 constants

| Constant | Purpose |
|---|---|
| `OCC_BONUS` | Dict of occupation name → skill bonus definition. Four schema variants supported: |

**OCC_BONUS schema variants:**

| Variant | Shape | Behaviour |
|---|---|---|
| Standard (pair choice) | `[[skA,skB],[skC,skD]]` | Player picks one of two pairs; UI shows two buttons |
| Fixed (auto-apply) | `{fixed:[sk,...]}` | Bonuses applied immediately on occupation pick; no player choice needed |
| Pick-N | `{pick:N, from:[sk,...]}` | Player picks exactly N skills from the list (e.g. Soldier picks 2 from 4) |
| Fixed + Pick-1 | `{fixed:[sk,...], pick:1, from:[sk,...]}` | Fixed skills auto-applied, player also picks 1 from the list (e.g. Mage) |

### BG_GRANTS extended fields (Milestone 6.0)

| Field | Type | Purpose |
|---|---|---|
| `attrs` | `{ATTR: number}` | Free base attribute bonuses from background (shown in yellow in attribute table) |
| `attr_max_mods` | `{ATTR: number}` | Reduces displayed racial max for named attributes; shown in red with tooltip in Identity tab |
| `no_racial_max` | `true` | Removes racial max cap entirely; renders ∞ in yellow (Subject 0056 background) |
| `chi_lock` | `true` | Sets CHI_max to 0 in `ccRecalcHealthMorale()`; shown as red label in Health section |
| `surge_lock` | `true` | Display-only: shows "SURGE MAX locked at 0" label; SURGE not tracked in ccState |
| `health` | number | Bonus HP added to HEALTH_max |
| `morale` | number | Bonus Morale added to MORALE_max |
| `chi` | number | Bonus CHI added to CHI_max |

Backgrounds with `attr_max_mods`: Imaginary Friend (WITS−1), Darkspacer (WITS−1), Family of Thieves (SOCIAL−1), Sorcerous Background (SPEED−1), Street Urchin (ENDURANCE−1).
Backgrounds with resource locks: Imaginary Friend (`chi_lock`), Spirit Judge (`surge_lock`).

---

## Character Creator state (`ccState`) — key fields

| Field | Type | Description |
|---|---|---|
| `tab` | string | Active tab: `'identity'`, `'skills'`, `'talents'`, `'combat'`, `'tech'`, `'magic'`, `'gear'`. Note: `'attributes'` no longer exists (merged into `'identity'` in M7.0). Any persisted `'attributes'` state is redirected to `'identity'` at render time. |
| `name` | string | Character name |
| `race` | string | Race name (matches `g.races[].name`) |
| `occupation` | string | Occupation name |
| `background` | string | Background name |
| `sex` | string | Character sex/gender text |
| `age` / `apparent_age` | string | Real and apparent ages |
| `notes` | string | Free-form character notes |
| `clone` | bool \| null | `true` = Clone Vat, `false` = Natural Birth, `null` = not yet chosen |
| `nb_rolled` | bool | Whether Natural Birth attribute variance dice have been rolled |
| `attr_variance` | obj | Natural Birth variance per attribute: `{PHYSICAL:{minVar,maxVar}, …}` |
| `PHYSICAL_perm` … `WILLPOWER_perm` | number | XP-purchased permanent attribute value for each of 8 attributes |
| `PHYSICAL_bonus` … `WILLPOWER_bonus` | number | Circumstantial attribute bonus (0, ±1, ±3) |
| `HEALTH` / `MORALE` / `CHI` | number | Current resource values (editable) |
| `HEALTH_max` / `MORALE_max` / `CHI_max` | number | Max resource values (auto-calculated by `ccRecalcHealthMorale()`) |
| `init_move` / `init_standard` / `init_quick` / `init_complex` | string | Initiative values (free-text) |
| `weapons[6]` | array | Weapon slots: `{name, skill, dmg, dmgtype, power, expertise, special, close_range, medium_range, long_range, rof, ammo, currentammo, reload, mfr, base_data, options[]}` |
| `armor[2]` | array | Defense slots: `{name, type, def_phys/energy/tech/spirit, special, soak_expr, charges, regen, mfr, base_data, options[]}` |
| `datacoms[3]` | array | Datacom slots: `{name, cpu, mem, nanite, def_phys/energy/tech/spirit, def_dmg, int_ext/int_int/int_main, expertise, special, mfr, base_data, options[]}` — note: `nanite` in state vs `nanites` in `g.datacoms`; `def_phys` in state vs `def_physical` in data |
| `evolutions[]` | array | `{name, type, tier, effect, credited, bg_granted?, free?}` |
| `talents[]` | array | `{name, skill, category, xp_cost, effect, credited, bg_granted?}` |
| `credits` | number | Starting budget |
| `credits_spent` | number | Manual gear purchases (Gear Shop) |
| `background_desc` | string | Player notes for background box |
| `occupation_desc` | string | Player notes for occupation box |
| `occupation_bonus_choice` | null \| number | Which bonus option was picked from `OCC_BONUS[occupation]`: index of pair (standard), 0 (fixed/pick-N complete), or index of pick-1 choice. `null` = not yet chosen. |
| `occ_bonus_skills[]` | string[] | Skill keys currently carrying the OCC bonus (+1). Cleared and rewritten by `ccApplyOccBonus()` on every occupation or choice change. |
| `occ_bonus_picks[]` | string[] | In-progress skill picks for pick-N occupation types (e.g. Soldier). Accumulates until `entry.pick` count is reached. |
| `picker` | obj \| null | Active picker: `{type, slot, mfr?}` — `mfr` tracks selected manufacturer inside the picker window |
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
