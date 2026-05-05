# 01 — Project Overview

## What it is

The **56th Century Compendium** is a fully self-contained, browser-based reference tool and character creator for the *56th Century* tabletop RPG system. It is delivered as a single HTML file (`56th_century_compendium_v8.html`) with all game data, styles, and logic embedded inline — no build step, no server, no external runtime dependencies. It works on both mobile and desktop and is released as CC0 public domain.

## Repository structure (2 levels)

```
/
├── 56th_century_compendium_v8.html   # CANONICAL active file — all dev goes here
├── CLAUDE.md                         # AI project instructions
├── LICENSE                           # CC0 1.0 Universal
├── ship_components.csv               # Generated flat ship component catalog
├── drone_components.csv              # Generated flat drone component catalog
├── drone_components_final.csv        # Final drone component export
├── inject_engines.py                 # Dev helper: inject ENGINE codes into ship data
├── drone_redesign.py                 # Dev helper: generate/export drone component data
├── export_drone_comps.py             # Dev helper: export drone components to CSV
├── gen_db_comp.py                    # Dev helper: generate DB_COMP constant data
├── db_comp_new.js                    # Dev helper: JS snippet for drone component data
├── docs/                             # Project documentation (this folder)
│   ├── 00-ai-rules.md
│   ├── 01-overview.md
│   ├── 02-architecture.md
│   ├── 03-code-map.md
│   ├── 04-tech-stack.md
│   ├── 05-decisions-and-issues.md
│   ├── 06-implementation-plan.md
│   ├── decisions/
│   ├── specs/
│   └── drafts/
├── work/                             # TTE task logs
└── archive/                          # Retired versions — read-only
```

## Quick start

```bash
# Open the compendium in any browser — no install needed
open 56th_century_compendium_v8.html

# Syntax-check the embedded JS (for dev)
python3 -c "
import re
with open('56th_century_compendium_v8.html') as f: c = f.read()
scripts = re.findall(r'<script[^>]*>(.*?)</script>', c, re.DOTALL)
open('/tmp/check.js','w').write('\n'.join(scripts))
"
node --check /tmp/check.js
```

## Environment variables

None. The compendium is fully client-side with no server component.

## Ports

None. No server is required. File is opened directly in a browser via `file://`.
