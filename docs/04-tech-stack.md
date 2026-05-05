# 04 — Tech Stack

## Technologies

| Name | Version | Role | Why chosen |
|---|---|---|---|
| HTML5 | — | Delivery format | Single-file portability, works offline, zero install |
| Vanilla JavaScript (ES6+) | — | All UI logic, data rendering, state management | No build step, maximum compatibility, no dependency risk |
| CSS Custom Properties | — | Theming / palette | Runtime theme control via `:root` vars without preprocessor |
| Google Fonts CDN | — | Typography: Orbitron, Share Tech Mono, Exo 2 | Cosmetic only; app fully functional offline without them |
| Python 3 | — | Dev helper scripts (inject_engines.py, drone_redesign.py, etc.) | One-off data generation tools only, not part of runtime |
| Node.js | — | JS syntax checking only (`node --check`) | Dev-time validation; not a runtime dependency |

## Known compatibility issues

| Issue | Workaround |
|---|---|
| `node --check` does not accept `.html` files directly | Extract `<script>` blocks with Python regex before running `node --check /tmp/check.js` |
| Google Fonts unavailable offline | Fonts degrade gracefully to system sans-serif; no functional impact |

## External services

| Service | What we use it for | Notes |
|---|---|---|
| Google Fonts (`fonts.googleapis.com`) | Orbitron, Share Tech Mono, Exo 2 typefaces | Loaded via `<link>` in `<head>`; cosmetic only |
| Roll20 (VTT) | Character export target (JSON import) | No live API integration; export is a downloaded `.json` file |

## Infrastructure

None. The compendium is a static file. Distribution is manual (share the `.html` file directly).

No CI/CD, no hosting, no database, no server.
