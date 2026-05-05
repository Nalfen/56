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
| `applyWpnMfr(item, mfr)` | Apply weapon mfr mods | item obj, mfr name | Modified item copy (or null if avail exceeded) |
| `applyArmorMfr(item, mfr)` | Apply armor mfr mods | item obj, mfr name | Modified item copy |
| `applyMedMfr(item, mfr)` | Apply medical mfr mods | item obj, mfr name | Modified item copy |
| `defShift(current, mod)` | Shift defense tier | tier string, numeric mod | New tier string |
| `calcShip(comps, cls)` | Accumulate ship stats | component code array, class string | Stats object |
| `calcDrone(dbState)` | Accumulate drone stats | dbState object | Stats object or null |
| `buildShipComps()` | Expand ship catalog | none | Populates `g.catalog.ship_components` |
| `buildDroneParts()` | Expand drone catalog | none | Populates `g.catalog.drone_parts` |
| `ccExportRoll20()` | Export character to JSON | none (reads ccState) | Downloads Roll20 JSON file |
| `ccPickFromCache(pidx)` | Apply picker selection | picker cache index | Mutates ccState slot, calls render() |
| `ccAutoTrackedSpent()` | Sum auto-tracked costs | none (reads ccState) | number — total credits for weapons+armor+datacoms+evos |
| `ccCalcWeaponCost(wp)` | Weapon credit cost | weapon slot object | number |
| `ccCalcArmorCost(ar)` | Armor/defense credit cost | armor slot object | number |
| `ccCalcDatacomCost(dc)` | Datacom credit cost | datacom slot object | number |
| `ccCalcEvoCreditCost(e)` | Evolution credit cost | evo slot object | number (0 if free/bg_granted) |
| `egExportVTT()` | Export enemy to VTT-ES JSON | none (reads egState) | Downloads JSON file |

## Character Creator state (`ccState`) — key fields

| Field | Type | Description |
|---|---|---|
| `tab` | string | Active tab: `'origin'`, `'attributes'`, `'advancement'`, `'combat'`, `'tech'`, `'magicgear'` |
| `weapons[6]` | array | Weapon slots: `{name, skill, dmg, dmgtype, power, expertise, special, close_range, medium_range, long_range, rof, ammo, currentammo, reload, mfr, base_data, options[]}` |
| `armor[2]` | array | Defense slots: `{name, type, def_phys/energy/tech/spirit, special, soak_expr, charges, regen, mfr, base_data, options[]}` |
| `datacoms[3]` | array | Datacom slots: `{name, cpu, mem, nanite, def_*, special, mfr, base_data, options[]}` |
| `evolutions[]` | array | `{name, type, tier, effect, credited, bg_granted?, free?}` |
| `talents[]` | array | `{name, skill, category, xp_cost, effect, credited, bg_granted?}` |
| `credits` | number | Starting budget |
| `credits_spent` | number | Manual gear purchases (Gear Shop) |
| `picker` | obj/null | Active picker: `{type, slot}` |
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
