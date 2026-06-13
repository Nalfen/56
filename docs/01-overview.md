# 01 — Project Overview

## What it is

The **56th Century Compendium** is a browser-based reference tool and character creator for the *56th Century* tabletop RPG system. It exists in two delivery modes:

| Mode | File | Data location | Hosting |
|---|---|---|---|
| **Embedded** | `56th_century_compendium.html` (v8 promoted) | Inline in the HTML | Any — `file://` works |
| **Data-driven** | `56th_century_compendium_v11.html` (**canonical**) | `data/v8/*.json` fetched at runtime | Requires HTTP (GitHub Pages or `python -m http.server`) |

The data-driven v11 is the active development target. All game content is edited in the `data/v8/` JSON files; the HTML is the shell/renderer.

Both variants are CC0 public domain.

## Repository structure

```
/
├── 56th_century_compendium_v11.html  # CANONICAL — data-driven, requires HTTP hosting
├── 56th_century_compendium.html      # Embedded-data build (v8 promoted, no server needed)
├── 56th_century_compendium_v9_datadriven.html  # First data-driven build (historical)
├── 56th_century_compendium_v10.html  # Incomplete intermediate (abandoned)
├── data/
│   ├── v8/                           # Single source of truth for all game content (11 JSON files)
│   │   ├── manifest.json             # Load order for the 11 data files
│   │   ├── weapons.json              # weapons, weapon_options, manufacturers, ammo_types, ammo_opts
│   │   ├── armor.json                # armor, armor_options
│   │   ├── equipment.json            # equipment, options, datacoms, software
│   │   ├── medical.json              # medical, medical_manufacturers
│   │   ├── characters.json           # races, backgrounds, occupations, evolutions, skills
│   │   ├── talents.json              # talents
│   │   ├── magic.json                # spells, magic_rules, magic_domains, specials
│   │   ├── hacking.json              # hacking_rules, hacking_keywords
│   │   ├── rules.json                # rules_grouped, code, toxic_shock
│   │   ├── glossary.json             # glossary_clean
│   │   ├── galaxy.json               # galaxy, factions, catalogue_systems, catalog
│   │   ├── README.md                 # Editing guide for JSON data
│   │   └── _archive_partial/         # Unused earlier extraction — deletable
│   └── v8_pre_skillmigration/        # Snapshot before skill migration (5 files differ from v8)
├── CLAUDE.md                         # AI project instructions
├── BEMYAGENT.md                      # BEMYAGENT bootstrap protocol definition
├── README.md                         # BEMYAGENT repo README (not compendium docs)
├── LICENSE                           # CC0 1.0 Universal
├── ship_components.csv               # Generated flat ship component catalog
├── drone_components.csv              # Generated flat drone component catalog
├── drone_components_final.csv        # Final drone component export
├── inject_engines.py                 # Dev helper: inject ENGINE codes into ship data
├── drone_redesign.py                 # Dev helper: generate/export drone component data
├── export_drone_comps.py             # Dev helper: export drone components to CSV
├── gen_db_comp.py                    # Dev helper: generate DB_COMP constant data
├── db_comp_new.js                    # Dev helper: JS snippet for drone component data
├── docs/                             # Project documentation
│   ├── 00-ai-rules.md
│   ├── 01-overview.md
│   ├── 02-architecture.md
│   ├── 03-code-map.md
│   ├── 04-tech-stack.md
│   ├── 05-decisions-and-issues.md
│   ├── 06-implementation-plan.md
│   ├── 07-data-map.md
│   ├── decisions/
│   ├── specs/
│   └── drafts/
├── work/                             # TTE task logs (5.0/, 6.0/, 7.0/)
└── archive/                          # Retired versions — read-only
```

## Quick start

### Data-driven (v11, canonical)

```bash
# Must be served over HTTP — double-clicking won't work
cd /path/to/repo
python -m http.server
# open http://localhost:8000/56th_century_compendium_v11.html

# Edit game content: modify any file in data/v8/*.json, then refresh
```

### Embedded (v8, no server needed)

```bash
open 56th_century_compendium.html
```

### JS syntax check (dev)

```bash
python3 -c "
import re
with open('56th_century_compendium_v11.html') as f: c = f.read()
scripts = re.findall(r'<script[^>]*>(.*?)</script>', c, re.DOTALL)
open('/tmp/check.js','w').write('\n'.join(scripts))
"
node --check /tmp/check.js
```

## Environment variables

None.

## Ports

`python -m http.server` uses port 8000 by default. Only needed for local dev of the data-driven build.
