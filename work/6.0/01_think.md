# Task 6.0 — Character Creator Coverage Gap (Think)

## Context

A full audit of `g.backgrounds`, `g.occupations`, `g.talents`, and `g.evolutions.entries`
was run against what the character creator currently tracks. 112 mechanical effects
described in game data are not surfaced or stored anywhere in `ccState` or the CC UI.

## Audit summary

| Category | Gaps |
|---|---|
| Backgrounds | 24 |
| Occupations | 17 |
| Talents | 31 |
| Evolutions | 40 |
| **Total** | **112** |

---

## Tier 1 — Display only (no new state) ~1–3h each

Data is already in `g.*`. Just not rendered in CC slots.

### T1-A: Talent effect text on Advancement tab
- Talent slots show name + XP cost only
- `g.talents[].effect` is never displayed in CC
- Fix: add collapsible/inline effect line under each talent slot in `ccRenderAdvancement()`

### T1-B: Evolution effect text on Evolutions tab
- Evo slots show name/tier/type only
- `g.evolutions.entries[].effect` is never displayed in CC
- Fix: same pattern in the evolutions render section

### T1-C: Background traits list on Origin tab
- Background shows as a name only
- `g.backgrounds[].traits[]` text is never displayed in CC
- Fix: render traits list beneath background selector

---

## Tier 2 — Small state additions ~3–5h each

### T2-A: Background racial max modifiers
Backgrounds that reduce a specific attribute racial max (beyond Subject 0056):
- Imaginary Friend: −1 WITS max
- Street Urchin: vulnerability/social max (needs exact field from data)
- Darkspacer: social racial max reduction
- Deep Space Explorer: racial max reduction
- Family of Thieves: racial max reduction
- Sorcerous Background / Source Bound: CHI-related racial max

Fix: extend `BG_GRANTS` with `attr_max_mods: {WITS: -1}` etc.
`ccRenderAttributes()` already handles this pattern (Subject 0056 `no_racial_max`).

### T2-B: Occupation skill bonus choice (all 17 occupations)
Every occupation grants "SMALL bonus to one of two skill pairs" — never presented or stored.

Occupations and their pairs:
| Occupation | Option A | Option B |
|---|---|---|
| Arms Collector | Gunslinger + Engineering | Marksman + Technology |
| Bartender | Charm + Subterfuge | Flair + Etiquette |
| Bounty Hunter | Intimidation + Martial Arts | Cyberintel + Gunslinger |
| Corporate | Leadership + Etiquette | Technology + Intuition |
| Diplomat | Charm + Subterfuge | Negotiation + Etiquette |
| Drug Dealer | Science + Academic | Scavenging + Medicine |
| Entertainer | Flair + Etiquette | Acting + Charm |
| Explorer | Survival + Marksman | Scavenge + Gunslinger |
| Hooverboard Pro | Piloting + Flair | Athletic + Navigation |
| Investigator | Subterfuge + Search | Concealment + Streetwise |
| Law Enforcement | Intimidate + Martial Arts | Academics + Streetwise |
| Outlaw | Subterfuge + Concealment | Streetwise + Dexterity |
| Scientific | Medicine + Science | Academic + Galactic Knowledge |
| Trader | Negotiation + Charm | Scavenging + Streetwise |
| Transporter | Piloting + Etiquette | Negotiation + Journeyman |
| Virtual Activist | Cyberintel + Hacking | Technology + Operator |
| Worker | Journeyman + Scavenging | Science + Engineering |

Fix:
- Add `occupation_bonus_choice` (0 or 1) to `ccState` + `ccMakeFreshState()`
- On occupation pick, show radio/dropdown for the two pairs
- Display chosen pair as a "SMALL bonus" reminder pill on the Skills tab
- No mechanical enforcement — display reminder only

### T2-C: Special resource locks
Backgrounds/evolutions that zero-out a resource pool:
- Spirit Judge background: SURGE max = 0
- Imaginary Friend background: CHI max = 0
- Fledgling AI background: double morale loss vs Tronik/AI (display note)
- Void Soul evo (Tier I+): CHI max = 0

Fix: add `resource_locks[]` to `BG_GRANTS` and evo detection; display locked resources
on the Attributes tab with a lock icon / "0 (locked)" label.

---

## Tier 3 — Passive abilities summary panel ~5–8h total

31 talent effects and 40 evolution effects describe conditional passive bonuses that fire
during play (e.g., "SMALL bonus to soak when wearing ARMOR", "LARGE WITS defense bonus").
These cannot be mechanically enforced but must be visible to the player during combat.

Fix: add a **Passive Abilities** read-only panel (new sub-section on Advancement or
a dedicated strip on Combat tab):
- Iterates `ccState.talents[]` + `ccState.evolutions[]`
- Matches to `g.talents` and `g.evolutions.entries` by name
- Renders `effect` text grouped by category: COMBAT / DEFENSE / SKILL / SPECIAL
- ~60–80 lines of render code, no state changes

---

## Tier 4 — Medium complexity ~1–2 days each

### T4-A: Occupation skill bonuses as tracked modifiers (not just display)
- Needs a "skill modifiers" layer separate from skill rank
- Skills tab would show base rank + passive bonus badge
- Deferred — requires skills system redesign

### T4-B: Evolution attribute bonuses on Attributes tab
- Optimized Systems (+1 chosen attr), Ironmind (+WITS), Blindsenses, God Bound, etc.
- Need to detect which tier is owned and which choice was made at creation
- Some are fixed, some are player-chosen — data inconsistent
- Deferred — needs per-evo data enrichment

### T4-C: Background combat/vulnerability notes
- Mangaran Brave/Savage (damage bonus vs specific factions)
- Politician (penalty to enemy defenses)
- Subject 0056 (periodic HP damage)
- Best rendered as "Combat Notes" display rather than enforced

---

## Tier 5 — Backlog / extensive design needed

- Contacts / faction access section (no data structure exists)
- Starting equipment grants from backgrounds (no equipment data on backgrounds)
- Full passive modifier enforcement (modifier stack system — fundamental change)
- Narrative special rules (Salvaged Droid, Trueborn, Assassin cult) — best as lore text

---

## Approach

SEAMLESS mode. Implement in tier order:
1. T1-A → T1-B → T1-C (display only, fastest ROI)
2. T2-A (BG_GRANTS attr_max_mods)
3. T2-B (occupation skill bonus choice)
4. T2-C (resource locks)
5. T3 (passive abilities panel)

All changes in `56th_century_compendium_v8.html`.
Update `docs/03-code-map.md` and `docs/05-decisions-and-issues.md` in same response as code changes.

---

## File size note

Currently 2.8 MB / 13,132 lines. Tiers 1–3 together ~400 lines. Tier 4 another ~600 lines.
Projects to ~14,000 lines / ~3.0 MB — well within single-file range. No split needed yet.
Splitting becomes relevant only if large new *data* sections are added (contacts catalogue, etc.).
