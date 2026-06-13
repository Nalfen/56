# Task 7.0 — Identity Tab UX Refinements (Checklist)

## Milestone 7.0 tasks

| # | Item | Status |
|---|---|---|
| M7-1 | Merge Attributes tab into Identity; remove Attributes from nav | done |
| M7-2 | Origin block (Clone/Natural Birth) moved to top of Identity tab | done |
| M7-3 | Left col: identity fields; Right col: full attribute table with XP costs | done |
| M7-4 | Health/Morale/CHI + Initiative as full-width row below 2-col grid | done |
| M7-5 | Racial traits (racial/evolution/environment) in own detail box | done |
| M7-6 | Background and Occupation pickers sorted alphabetically | done |
| M7-7 | Race selector sorted alphabetically | done |

## Bug fixes

| # | Item | Status |
|---|---|---|
| BF-1 | XP bar negative on fresh load — secondary attrs initialized to 0 in `ccMakeFreshState()` | done |
| BF-2 | Skills grid clips Acuity column on mobile — `repeat(auto-fill,minmax(160px,1fr))` | done |
| BF-3 | Picker modal off-screen on mobile when scrolled — `position:fixed` overlay | done |
| BF-4 | Manufacturer badge on all picker items — `anyChg` guard for weapon/armor/datacom | done |
