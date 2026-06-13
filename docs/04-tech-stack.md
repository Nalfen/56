# 04 — Tech Stack

## Technologies

| Name | Version | Role | Why chosen |
|---|---|---|---|
| HTML5 | — | Delivery format | Single-file portability, works offline (embedded build), zero install |
| Vanilla JavaScript (ES6+) | — | All UI logic, data rendering, state management | No build step, maximum compatibility, no dependency risk |
| CSS Custom Properties | — | Theming / palette | Runtime theme control via `:root` vars without preprocessor |
| JSON | — | Game content (data-driven build) | Human-editable, no tooling needed, easy to validate |
| Google Fonts CDN | — | Typography: Chakra Petch, Atkinson Hyperlegible, JetBrains Mono (v11) | Cosmetic only; app fully functional offline without them |
| Python 3 | — | Dev helper scripts (inject_engines.py, drone_redesign.py, etc.) | One-off data generation tools only, not part of runtime |
| Node.js | — | JS syntax checking only (`node --check`) | Dev-time validation; not a runtime dependency |

## Hosting requirements

| Build | Hosting | Notes |
|---|---|---|
| Embedded (`56th_century_compendium.html`) | None — `file://` works | All data inline; share the single file |
| Data-driven (`56th_century_compendium_v11.html`) | **HTTP required** | Browser blocks `fetch()` on `file://` (CORS/origin restrictions) |

### Options for data-driven build

- **GitHub Pages**: push repo, enable Pages → works as-is (no config needed, `data/v8/` served alongside HTML)
- **Local dev**: `python -m http.server` in repo root → `http://localhost:8000/56th_century_compendium_v11.html`
- Any static HTTP server works (nginx, Caddy, etc.)

## Known compatibility issues

| Issue | Workaround |
|---|---|
| `node --check` does not accept `.html` files directly | Extract `<script>` blocks with Python regex before running `node --check /tmp/check.js` |
| Google Fonts unavailable offline | Fonts degrade gracefully to system sans-serif; no functional impact |
| Data-driven build fails when opened via `file://` | Must use HTTP server; v11 shows a boot-error panel with instructions if this happens |

## External services

| Service | What we use it for | Notes |
|---|---|---|
| Google Fonts (`fonts.googleapis.com`) | Chakra Petch, Atkinson Hyperlegible, JetBrains Mono typefaces | Loaded via `<link>` in `<head>`; cosmetic only |
| Roll20 (VTT) | Character export target (JSON import) | No live API integration; export is a downloaded `.json` file |
| GitHub Pages | Hosting for data-driven build | Static file hosting; `data/v8/` served alongside HTML |

## Infrastructure

Embedded build: none. No CI/CD, no database, no server.

Data-driven build: GitHub Pages (static hosting only). No backend, no CI/CD pipeline.
