# Task 7.0 — Identity Tab UX Refinements (Think)

## Context

After Milestone 6.0 (character creator coverage gap), the Identity and Attributes tabs
had grown cluttered. The Attributes tab existed separately from Identity despite being
tightly coupled. The Origin block (Clone/Natural Birth) was buried mid-page.

## Goals

1. Merge the Attributes tab into Identity — eliminate the standalone tab from the nav
2. Move the Origin block to top of the combined Identity tab (first thing the user sees)
3. Left/right two-column layout: left = personal fields, right = full attribute table with XP costs
4. Health/Morale/CHI + Initiative as a single full-width row below the two-column grid
5. Racial traits (racial/evolution/environment) in their own detail box below
6. Background and Occupation pickers sorted alphabetically
7. Race selector sorted alphabetically

## Scope

All changes in `56th_century_compendium_v11.html` (and/or `56th_century_compendium.html`).
No new state fields — purely layout/render reorganization.

## Bug fixes bundled in this milestone

- BF-1: XP bar negative on fresh load — secondary attrs initialized to 0 in `ccMakeFreshState()`
- BF-2: Skills grid clips Acuity column on mobile — `repeat(auto-fill,minmax(160px,1fr))`
- BF-3: Picker modal off-screen on mobile when scrolled — `position:fixed` overlay
- BF-4: Manufacturer badge on all picker items — `anyChg` guard for weapon/armor/datacom

## Approach

SEAMLESS mode. Implement in order: M7-1 → M7-2 → M7-3 → M7-4 → M7-5/6 → bug fixes.
