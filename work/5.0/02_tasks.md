# Task 5.0 — Checklist

## Task A — Mono-Med Customs force UNIQUE

| # | Item | Status |
|---|---|---|
| A1 | In `applyMedMfr`, add special-case: if `mfrName === 'Mono-Med Customs'` set `w.availability = 'UNIQUE'` instead of shifting | done |
| A2 | Verify no Mono-Med items appear as "impossible" in the medical shop | done |
| A3 | Verify all Mono-Med items show UNIQUE (yellow highlight) | done |

## Task B — Size changes in picker

| # | Item | Status |
|---|---|---|
| B1 | Medical gear shop: compare `it.size` vs `base.size`; show size in row with orange highlight if increased, green if decreased | done |
| B2 | Datacom picker preview: add size display, highlight change vs base item | done |
| B3 | Check `g.manufacturers` for any weapon/armor `size_mod` entries that also need picker coverage | done — no weapon/armor mfrs have size_mod |

## Post-task

| # | Item | Status |
|---|---|---|
| D1 | Update `docs/03-code-map.md` (applyMedMfr change) | done |
| D2 | Update `docs/05-decisions-and-issues.md` (decision for Mono-Med special-case) | done |
| D3 | Commit + push both branches | done |
