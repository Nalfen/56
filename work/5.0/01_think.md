# Task 5.0 — Manufacturer picker display fixes (next session)

## Context

The character creator browse picker and medical gear shop apply manufacturer
modifiers at render time. Two display gaps were identified after session 4 work:

---

## Task A — Mono-Med Customs: force UNIQUE availability

**Problem:**  
`Mono-Med Customs` has `avail_mod: -10` in `g.medical_manufacturers`, which
is intended to represent "essentially unobtainable / custom order only". However
the current `applyMedMfr` logic shifts the AVAIL array by -10, which can
produce nonsensical results (negative index clamped to COMMON) or just
lands on an arbitrary tier depending on the base item.

**Correct behaviour:**  
Mono-Med Customs should **override** availability to `'UNIQUE'` regardless
of the base item's availability, rather than shifting it. This matches the
in-universe concept that each item is a bespoke custom commission.

**Where to fix:**  
`applyMedMfr()` in `56th_century_compendium_v8.html` (~line 1057).  
Add a special-case check before the `avail_mod` logic:
```js
if(mfrName === 'Mono-Med Customs'){ w.availability = 'UNIQUE'; }
else { /* existing avail_mod shift */ }
```

**Verification:**  
- All medical items with Mono-Med Customs selected should show UNIQUE
  (yellow highlighted, since it's a change for most items)
- No item should be filtered as "impossible" for this manufacturer

---

## Task B — Size changes shown in browse picker

**Problem:**  
Several manufacturers modify item size via `size_mod`:
- Medical: Altair Biomed (+1), Goodman Holistic (+1), Diva Solutions (+2),
  Mono-Med Customs (+5)
- Datacoms: all datacom manufacturers with `size_mod` (check `g.manufacturers`)

Currently, size changes are applied by `applyMedMfr` / `applyDatacomMfr`
but are **not displayed** in the picker preview rows. A user browsing with
Goodman Holistic selected sees no indication the item gets larger.

**Where to fix:**  
- Medical gear shop item rows in `ccRenderMagicGear()` — add size display
  with change highlighting (similar to legality/availability highlighting)
- Datacom picker preview in `ccRenderPicker()` — add size field with
  change highlight

**Change highlight colour convention:**  
- Size increase (worse): orange `var(--a2)`
- Size decrease (better): green `var(--gr)`

**Verification:**  
- Selecting Altair Biomed should show size pill as orange when base size shifts
- Selecting Goodman Holistic should show orange size change
- Selecting Diva Solutions (+2 size) should show orange size change
- Mono-Med Customs (+5 size) should show orange size change
- Datacom manufacturer size changes should show in picker preview

---

## Approach

SEAMLESS mode. Fix Task A first (simpler, isolated), then Task B.

Both changes are in `56th_century_compendium_v8.html` only.  
Update `docs/03-code-map.md` and `docs/05-decisions-and-issues.md` in the
same response as code changes (per 00-ai-rules.md §5).
