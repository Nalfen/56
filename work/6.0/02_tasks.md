# Task 6.0 — Character Creator Coverage Gap (Checklist)

## Tier 1 — Display only

| # | Item | Status |
|---|---|---|
| T1-A | Talent effect text shown beneath each talent slot in `ccRenderAdvancement()` | done — upgraded from `<input>` to `<textarea rows="2">` |
| T1-B | Evolution effect text shown beneath each evo slot | done — upgraded from `<input>` to `<textarea rows="2">` |
| T1-C | Background `traits[]` list displayed on Origin tab below background selector | done — formatted BENEFIT 1 / BENEFIT 2 / DRAWBACK cards rendered from `g.backgrounds` |

## Tier 2 — Small state additions

| # | Item | Status |
|---|---|---|
| T2-A | Extend `BG_GRANTS` with `attr_max_mods` for all backgrounds that reduce an attribute racial max | done — Imaginary Friend (WITS-1), Darkspacer (WITS-1), Family of Thieves (SOCIAL-1), Sorcerous Background (SPEED-1), Street Urchin (ENDURANCE-1) |
| T2-A | `ccRenderAttributes()` reads `attr_max_mods` and adjusts displayed racial max accordingly | done — reduced max shown in red with tooltip |
| T2-B | Add `occupation_bonus_choice` (0 or 1) to `ccState` + `ccMakeFreshState()` | done |
| T2-B | On occupation pick, render radio / two-option selector for skill pair choice | done — two-button selector in Identity right column |
| T2-B | Display chosen occupation skill bonus pair as reminder pill on Skills tab | done — reminder shown inline below the selector |
| T2-C | Add resource lock flags to `BG_GRANTS`: `chi_lock:true` (Imaginary Friend), `surge_lock:true` (Spirit Judge) | done |
| T2-C | `ccRecalcHealthMorale()` sets CHI_max=0 when `bg.chi_lock` is true | done |
| T2-C | Health & Morale section shows red lock labels for CHI MAX=0 and SURGE MAX=0 | done |
| T2-C | Detect Void Soul evo ownership; apply CHI=0 lock dynamically | deferred — Void Soul is rare; background lock covers most cases |

## Tier 3 — Passive abilities panel

| # | Item | Status |
|---|---|---|
| T3 | Build passive abilities read-only panel from active talents + evos | done |
| T3 | Group passive effects by COMBAT / DEFENSE / SKILL / SPECIAL | done — grouped by talent category (color-coded) and evo type (GENETICS/CYBER/MAGIC) |
| T3 | Decide placement: Advancement tab sub-section or Combat tab strip | done — placed at bottom of Advancement tab below the talents+evos grid |

## Tier 4 — Medium complexity (deferred)

| # | Item | Status |
|---|---|---|
| T4-A | Occupation skill bonuses as tracked modifiers on Skills tab (not just reminder) | deferred |
| T4-B | Evolution attribute bonuses auto-applied to Attributes tab | deferred |
| T4-C | Background combat/vulnerability notes panel | deferred |

## Tier 5 — Backlog

| # | Item | Status |
|---|---|---|
| T5-A | Contacts / faction access section | backlog |
| T5-B | Starting equipment grants from backgrounds | backlog |
| T5-C | Full passive modifier enforcement (modifier stack) | backlog |
| T5-D | Narrative special rules as lore/note text | backlog |

## Post-task

| # | Item | Status |
|---|---|---|
| D1 | Update `docs/03-code-map.md` with new CC state fields and render functions | todo |
| D2 | Update `docs/05-decisions-and-issues.md` with decisions made | todo |
| D3 | Commit + push both branches | todo |

---

## Known gaps by source (full audit reference)

### Backgrounds with attr max reductions
- Imaginary Friend: −1 WITS max
- Darkspacer: social max reduction
- Deep Space Explorer: racial max reduction
- Family of Thieves: racial max reduction
- Sorcerous Background: racial max reduction
- Street Urchin: social vulnerability / max reduction

### Backgrounds with special resource locks
- Spirit Judge: SURGE max locked at 0
- Imaginary Friend: CHI max locked at 0
- Fledgling AI: double morale loss vs Tronik/AI (display note only)

### Backgrounds with untrackable special rules (Tier 5 / narrative)
- Assassin: no ASSIST benefits, cult contracts
- Master of None: cannot take 40/50pt talents (enforcement hard)
- Resurected: old enemies (contacts)
- Salvaged Droid: no eat/drink/auto-repair (narrative)
- Trueborn: requires breathing mask (narrative)
- Spirit Judge: no SURGES (resource lock — T2-C)
- Weird Upbringing: social contact penalty (narrative)
- Scholar: theoretical experience penalty (narrative)

### All talent effects (display in Passive Abilities panel — T3)
Armor Specialist, Assassination, Berserk, Cool Headed, Coordinated Assault,
Encrypted Channels, Enslaver, Family Connexions, Finetune, Firestarter,
Just Do It, Living Horror, Look Out, Loyal Defender, Make It Count,
Mind Reader, Mr. Torgue, Nightstalker, Noogie Slam, Power Though,
Rending Claws, Single-Mindedness, Sniff Out Weakness, Toxicologist,
Versatile Fighter, Vicious Counter, Viral Code, Well Connected, Whirling Dervish

### All evolution effects with trackable passive bonuses (T3 panel / T4-B deferred)
Alpha Specimen (I/II), Blindsenses (II/III), Combat Analyser (III), Datacom Implant (III),
Exo Behemoth (I/II), Exterminate Protocols (I), Ghost (I), God Bound (I/III),
High Metabolism (I/II), Hyperawareness (I/II), Ironmind (I/II), Nerve Dampening (III),
Optimized Systems (I), Personal Space (II/III), Polyglot (II/III), Residual Energy (II),
Sealed Mind (II), Spirit Infusion (II/III), Spirit Monk (I), Streetfighter (I/II),
Subdermal Plating (III), Synaptic Reinforcement (I/II), Void Soul (I/II/III)
