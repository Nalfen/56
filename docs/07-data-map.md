# 07 — Data Map: Where Everything Lives in the HTML File

> All code and data lives in `56th_century_compendium_v8.html`.
> The file has two distinct storage patterns:
> - **Inline in `const g`** (line 726) — one giant minified JSON-like object, all on a single line. Edit by searching for the item's name string.
> - **Separate assignments** (`g.key = [...]` or `const KEY = ...`) — defined later in the file, each on their own line block. Edit by navigating to the line number.

---

## Part 1 — `const g` (line 726, single minified line)

All keys below are packed inside the `g` object on line 726. To locate a specific item, **search by name string** in your editor (e.g. `"Pulse Rifle"`).

| Key | Entries | Description |
|---|---|---|
| `g.specials` | 86 | Special property codes → `{name, desc}` |
| `g.code` | 2473 | Encoded reference entries |
| `g.weapons` | 178 | All weapons — see schema in `03-code-map.md` |
| `g.spells` | 97 | Spells with school, range, duration, effect |
| `g.talents` | 382 | Talents `{name, skill, category, effect, cost}` |
| `g.evolutions` | dict | Outer dict; sub-key `entries` has 273 evo entries |
| `g.equipment` | 183 | General gear `{name, category, size, effect, cost, availability, legality}` |
| `g.software` | dict | 4 sub-keys: `actions`, `programs`, `gadgets`, `routines` |
| `g.medical` | 35 | Medical items with manufacturer variants |
| `g.armor` | 168 | ALL defensive items: armors, forcefields, barriers, defensive datacoms |
| `g.datacoms` | 25 | Datacom devices |
| `g.hacking_rules` | 15 | Hacking rule entries |
| `g.hacking_keywords` | 22 | Hacking keyword definitions |
| `g.magic_rules` | 114 | Magic/spell rule entries |
| `g.magic_domains` | 4 | Magic domain entries |
| `g.skill_rules` | 10 | Skill rule blocks |
| `g.skills` | 40 | Skills `{name, category, desc}` |
| `g.toxic_shock` | dict | 2 sub-keys: `rules` (string) + `table` (array) |
| `g.races` | 14 | See schema below |
| `g.backgrounds` | 38 | Character backgrounds `{name, race, desc, traits[]}` |
| `g.occupations` | 32 | Occupations `{name, desc, details[]}` |
| `g.options` | 101 | Weapon/armor/datacom options (same array, filtered by flags) |
| `g.armor_options` | 101 | (alias/duplicate of g.options — same data) |
| `g.weapon_options` | 41 | Weapon-specific option subset |
| `g.manufacturers` | 19 | Manufacturer stat modifiers for weapons/armor/datacoms |
| `g.medical_manufacturers` | 6 | Manufacturer stat modifiers for medical items |
| `g.rules_grouped` | 10 | Rule groups for the Rules & Glossary section |
| `g.glossary_clean` | 195 | Flat glossary entries `{name, desc}` |
| `g.catalog` | dict | 6 sub-keys — see below |
| `g.armor_images` | 41 | Armor image paths (display only) |
| `g.weapon_images` | 177 | Weapon image paths (display only) |

### `g.catalog` sub-keys (inside line 726)

| Sub-key | Entries | Description |
|---|---|---|
| `g.catalog.ships` | 48 | Spaceships with component slot lists |
| `g.catalog.vehicles` | 35 | Ground/air vehicles |
| `g.catalog.drones` | 19 | Pre-built drone entries |
| `g.catalog.chassis` | 5 | Drone chassis size definitions |
| `g.catalog.modules` | 43 | Drone & vehicle modules |
| `g.catalog.manufacturers` | 6 | Catalog-specific manufacturer entries |

> `g.catalog.ship_components` and `g.catalog.drone_parts` are NOT in the raw data — they are built at startup by `buildShipComps()` and `buildDroneParts()` from `SCOMP_DEF` and `DB_COMP`.

### `g.races` entry schema

```js
{
  name:        "Hakari",
  mods:        ["+2 Physical", "-1 Mental", ...],   // display mod list
  racial:      "Armored Skin: ...",                  // racial ability text
  evolution:   "The Veil: ...",                      // racial evo text
  environment: "Shared Suffering: ...",              // env ability text
  stats: {
    physical:  { min: "-1", avg: "2", max: "5" },
    acuity:    { min: "-3", avg: "0", max: "3" },
    mental:    { min: "-2", avg: "1", max: "4" },
    social:    { min: "-6", avg: "-3", max: "0" },
    endurance: { min: "-1", avg: "3", max: "5" },
    speed:     { min: "-2", avg: "2", max: "4" },
    wits:      { min: "-1", avg: "3", max: "5" },
    willpower: { min: "0",  avg: "4", max: "6" },
  }
}
```
14 races: Hakari, Human, Jaulaus, Skalander, Patriark, Nerulian, Psylon, + 7 Non-Born variants.

---

## Part 2 — Separate multi-line blocks (assigned after line 726)

These are defined as `g.key = [...]` or `const KEY = [...]` on their own lines. Navigate directly by line number.

### Galaxy & World data

| Block | Lines | Entries | Description |
|---|---|---|---|
| `g.galaxy` | 2343 – 2827 | ~18 | Galactic region/faction overviews with `map_pos` for starmap |
| `GALAXY_MAP_POS` | 2828 | dict | Additional map pin positions |
| `STARGATE_LINKS` | 3006 | array | `[nameA, nameB]` pairs drawn as stargate lines on the map |
| `GALAXY_SECTIONS` | 3066 | ~17 | Ordered section descriptors: `{key, factionName, color, sysRegex}` |
| `worldData` | 3087 | dict | Static world detail panels for named systems (used by starmap click) |
| `g.factions` | 3313 – 3907 | ~39 | Faction/organisation lore entries — see schema below |
| `g.catalogue_systems` | 3910 – 6900 | ~70 systems | Star system entries with full planet lists — the largest block in the file |

### Ammunition

| Block | Lines | Entries | Description |
|---|---|---|---|
| `AMMO_OPT_CODES` | 1789 | array | Ordered ammo option code strings |
| `AMMO_COMPAT` | 1790 | IIFE | Builds compatibility lookup: ammo type name → set of valid option codes |
| `g.ammo_types` | 6903 – 6914 | ~10 | Ammunition type definitions |
| `g.ammo_opts` | 6915 – 6950 | ~16 | Ammo option modifier entries |

### Ship component system

| Block | Lines | Entries | Description |
|---|---|---|---|
| `COMP_NAMES` | 1122 | dict | Component type key → display name (44 types) |
| `COMP_QCOL` | 1123 | dict | Quality → CSS colour string |
| `COMP_Q` | 1131 | dict | Quality string → integer index |
| `SHIP_BASE` | 1133 | dict | Per-class base stats: `{structure, hull, crew_min, command}` |
| `COMP_CC` | 1137 | dict | Stat contributions per component type |
| `ENG_SPD` | 1196 | dict | Engine type → speed base tier |
| `SPD_STR` | 1197 | array | Speed tier index → display string |
| `SCOMP_DEF` | 1241 – 1353 | 37 types | Compact ship component catalog (ENGINEBALANCED, RADAR, SHIELD, etc.) |
| `SCOMP_CLASSES` | 1354 | array | `['DRONE','FIGHTER','CORVETTE',…,'NOVA']` |
| `SCOMP_TIERS` | 1355 | array | `['BASIC','AVERAGE','GOOD']` |

### Drone builder system

| Block | Lines | Entries | Description |
|---|---|---|---|
| `DB_SIZES` | 1384 | dict | Chassis sizes: TINY/SMALL/MED/LARGE/XL/HUGE with base stats |
| `DB_MOB` | 1392 | dict | Mobility types: STATIC/WALK/CLIMB/HOVER/FLY |
| `DB_ZONE` | 1399 | dict | Zone modifiers: core/internal/external |
| `DB_DEF_RANKS` | 1404 | array | `['NONE','LOW','MEDIUM','HIGH','EXTREME']` |
| `DB_SKILLS` | 1405 | dict | Skills by attribute for SKILL_MODULE picker |
| `DB_COMP` | 1412 – 1788 | 56 types | All drone component definitions with tiers |

### Enemy Generator (GM Tools)

| Block | Lines | Description |
|---|---|---|
| `EG_NAMES_FIRST` / `EG_NAMES_LAST` | 8163 – 8164 | Random name pools |
| `EG_ARCHETYPES` | 8165 – 8197 | Archetype defs: soldier/sniper/brawler/etc. |
| `EG_TIER_ORDER` / `EG_TIER_BASE` | 8198 – 8199 | Difficulty tier ordering + base HP |
| `EG_AVAIL_BY_TIER` / `EG_LEGAL_BY_TIER` | 8200 – 8201 | Allowed availability/legality per tier |
| `EG_SKILLS_ALL` / `EG_SKILL_DISP` | 8202 – 8212 | Skill lists for NPC assignment |
| `EG_SKILL_WPN_CATS` | 8215 | Maps weapon categories to skill names |
| `EG_ARCH_TALENT_CATS` | 8217 | Talent categories preferred per archetype |
| `EG_ARCH_EVO_TYPES` | 8218 | Evolution types preferred per archetype |
| `EG_CONSUMABLE_LEGAL` | 8219 | Consumable legality rules per tier |
| `EG_SECONDARY_RULES` | 8247 | Secondary weapon assignment rules |
| `EG_GROUP_TEMPLATES` | 8262 | Enemy group composition templates |
| `EG_AVAIL_WEIGHT` | 9922 | Availability weighting for item selection |

### Character Creator

| Block | Lines | Description |
|---|---|---|
| `CC_SKILLS_PHYS/MENT/SOCI/ACUI` | 8272 – 8275 | Skill lists by attribute |
| `CC_ALL_SKILLS` | 8276 | Full skill list for character creator |
| `CC_NAMES_FIRST` / `CC_NAMES_LAST` | 8277 – 8278 | Random name pools |
| `CC_RACE_ATTR_MAP` | 8279 | Race → attribute bonus mapping |
| `BG_GRANTS` | 8281 | Background → auto-granted skills/talents/evos |
| `CC_ATTR_KEYS` | 8349 | Ordered attribute key list |
| `CC_SIZE_TO_VAL` / `CC_SIZE_LOAD` | 8561 – 8562 | Equipment size → carry load values |
| `CC_TALENT_CATS` | 9193 | Talent category list for character creator |
| `ccMakeFreshState()` | 8309 | Returns blank character state object |
| `ccState` | 8346 | Live character creator state (initialised from ccMakeFreshState) |

### Utility constants (weapons/armor rendering)

| Block | Lines | Description |
|---|---|---|
| `AVAIL` | 933 | Availability tier order array |
| `POWER_STR` | 934 | Power level index → string |
| `DEF_TIER_MAP` / `DEF_NAME_TO_NUM` | 975 – 976 | Defense tier ↔ numeric mapping |
| `CAT_LBL` | 1113 | Weapon category → short display label |
| `MELEE_CATS` | 1114 | Set of melee weapon category strings |
| `WPN_MFRS` | 1115 | Array of weapon manufacturer names |
| `WPN_MFRS_MELEE_ONLY` | 1116 | Set of melee-only manufacturer names |
| `ARMOR_MFRS` | 1117 | Array of armor manufacturer names |
| `DATACOM_MFRS` | 1118 | Array of datacom manufacturer names |
| `MEDICAL_MFRS` | 1119 | Array of medical manufacturer names |

---

## Part 3 — g.factions entry schema

```js
{
  id:            'snake_case_id',
  name:          'Full Name',
  short:         'Abbrev',
  category:      'Megacorporation',   // drives filter chip
  subcategory:   'Weapons & Tactical',
  alignment:     'Legal',             // drives badge colour
  hq:            'Planet (Region)',
  presence:      ['Region A', 'Region B'],
  desc:          'Long lore paragraph.',
  known_for:     ['Bullet 1', '…'],
  regions:       ['Alliance Space'],
  status:        'Active',
  legal_standing:'Fully legal; …'
}
```

~39 faction entries. Groups within the array (comment blocks in source):
- Lines 3313–3340 — BIG 3 MEGACORPORATIONS (Galactic Union, Arms Corp, Yamato)
- Lines 3341–~3600 — WEAPONS MANUFACTURERS + ARMOR/TECH/MED manufacturers
- Lines ~3600–3907 — Governments, outlaws, trade bodies, local factions

> **Note:** `g.factions` (lore) and `g.manufacturers` (stat modifiers) are SEPARATE. Editing `g.factions` only affects the Factions page. Editing `g.manufacturers` (inside line 726) affects item stats.

---

## Part 4 — g.catalogue_systems entry schema

```js
{
  id:             'orion',
  name:           'Orion System',
  region:         'Alliance Space',
  classification: 'Core System',
  faction:        'Galactic Union / Alliance',
  status:         'active',
  tags:           ['Alliance Space', 'Seat of Power', …],
  desc:           '…',
  planets: [
    {
      id:          'orion_1',
      name:        'Orion 1',
      type:        'Space Station, Major Spaceport & Trade Hub',
      status:      'active',
      atmosphere:  'Breathable',
      climate:     '…',
      gravity:     'Standard',
      faction:     '…',
      population:  '…',
      tech_level:  'Advanced',
      access:      'Open',
      hazards:     ['…'],
      notable_locations: [{name:'…', desc:'…'}],
      hooks:       ['…'],
      desc:        '…',
    }
  ]
}
```

~70 star systems across lines 3910–6900 — the **largest single block in the file** at ~3000 lines.

---

## Quick edit guide

| What you want to edit | How to find it |
|---|---|
| A specific weapon's stats | Search for `"Weapon Name"` anywhere in file → you're in g.weapons (line 726) |
| A faction's lore/desc | Go to line 3313, search for `"faction_name"` in that block |
| A star system or planet | Go to line 3910, search for the system/planet name |
| Galactic region overview | Go to line 2343 (g.galaxy) |
| Manufacturer stat modifiers | Search for `"ManufacturerName"` near line 726 (inside g.manufacturers) |
| Ship component definitions | Go to line 1241 (SCOMP_DEF) |
| Drone component definitions | Go to line 1412 (DB_COMP) |
| Background auto-grants | Go to line 8281 (BG_GRANTS) |
| Enemy generator archetypes | Go to line 8165 (EG_ARCHETYPES) |
