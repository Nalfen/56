# 56th Century Compendium — Data Files

These JSON files are the **single source of truth** for all game content in
`56th_century_compendium_v9_datadriven.html`. Edit them directly to change any
value, item, or description — no need to touch the HTML.

## How it works
On load, the compendium reads `manifest.json`, then loads every file listed in
it and merges them into the game-data object `g`. Each JSON file is an object
whose top-level keys map exactly to the data the compendium expects.

## The files
| File | Contains |
|------|----------|
| `weapons.json` | weapons, weapon_options, weapon_images, manufacturers, ammo_types, ammo_opts |
| `armor.json` | armor, armor_options, armor_images |
| `equipment.json` | equipment, options, datacoms, software |
| `medical.json` | medical, medical_manufacturers |
| `characters.json` | races, backgrounds, occupations, evolutions, skills, skill_rules |
| `talents.json` | talents |
| `magic.json` | spells, magic_rules, magic_domains, specials |
| `hacking.json` | hacking_rules, hacking_keywords |
| `rules.json` | rules_grouped, code (action codex), toxic_shock |
| `glossary.json` | glossary_clean |
| `galaxy.json` | galaxy, factions, catalogue_systems, catalog |
| `manifest.json` | list of files to load (edit if you add/remove a data file) |

## Editing tips
- Keep it valid JSON: double-quoted keys/strings, commas between items, no
  trailing commas, no comments. (If unsure, paste into jsonlint.com.)
- To add an item, copy an existing object in the relevant array and change its
  fields.
- To add a whole new data file, create it and add its name to `manifest.json`.

## Viewing / hosting
The browser blocks reading these files when you double-click the HTML
(`file://`). It must be served over HTTP:

- **GitHub Pages (your plan):** put the `.html` file and this `data/` folder in
  the repo, enable Pages, share the URL. Works as-is.
- **Local testing:** open a terminal in the folder containing the HTML and run
  `python -m http.server`, then visit `http://localhost:8000/` and open the
  file. Edits to these JSON files appear on refresh.

## Notes
- The earlier, incomplete extraction attempt (`_archive_partial/`) and the
  pre-skill-migration data snapshot (`v8_pre_skillmigration/`) have been moved out
  of the data directory to `Claude Code/Archive/`. The data directory now holds
  only the master files listed above.
- A few small mechanics/config tables (ship- and drone-component generator
  definitions: `SCOMP_DEF`, `DB_COMP`, etc.) are still inline in the HTML because
  they are generator parameters tied to code, not flat content. They can be
  externalized later if you want.
