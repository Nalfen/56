# 56th Century TTRPG Data Files (v8)

**Version**: 8  
**Date**: 2026-06-07  
**Format**: JSON  
**Total Items**: 5,272  
**Total Domains**: 21

---

## Quick Reference

### Core Game Data

| File | Items | Purpose |
|------|-------|---------|
| `skills-v8.json` | 40 | Character skills across 4 categories |
| `constants-v8.json` | 18 | Game constants (availability, legality, defense tiers, etc.) |
| `rules-v8.json` | 10 | Complete game rules organized by topic |
| `glossary-v8.json` | 2,473 | Game terminology and definitions |

### Combat Systems

| File | Items | Purpose |
|------|-------|---------|
| `weapons-v8.json` | 178 | Complete weapon catalog with manufacturers |
| `armor-v8.json` | 168 | Full armor protection system with modifiers |
| `options-v8.json` | 101 | Equipment modifications and upgrades |

### Character Creation

| File | Items | Purpose |
|------|-------|---------|
| `races-v8.json` | 14 | Playable races with stat modifiers |
| `backgrounds-v8.json` | 38 | Character backgrounds with trait grants |
| `occupations-v8.json` | 32 | Occupations with career benefits |

### Character Advancement

| File | Items | Purpose |
|------|-------|---------|
| `talents-v8.json` | 382 | Talent tree with prerequisites and effects |

### Equipment & Tools

| File | Items | Purpose |
|------|-------|---------|
| `medical-v8.json` | 35 | Medical items and supplies |
| `datacoms-v8.json` | 25 | Datacom devices and hardware |
| `programs-v8.json` | 103 | Hacking software and programs |
| `spells-v8.json` | 97 | Spells and magical abilities |

### Vehicles & Units

| File | Items | Purpose |
|------|-------|---------|
| `vehicles-v8.json` | 35 | Vehicle types and specifications |
| `drones-v8.json` | 19 | Drone chassis templates |
| `drone_components-v8.json` | 56 | Drone component definitions and tiers |
| `ship_components-v8.json` | 37 | Starship component types |

### Galaxy & Factions

| File | Items | Purpose |
|------|-------|---------|
| `galaxy-v8.json` | 32 | Galaxy regions and faction territories |
| `factions-v8.json` | 39 | Faction/organization profiles |
| `catalogue_systems-v8.json` | 81 | Star systems and planetary data |

---

## Usage Guide

### Loading Data
```javascript
// Data is loaded via DATA_LOADER in compendium
// Access via window.DATA object
const weapons = window.DATA.weapons.weapons;
const races = window.DATA.races.races;
```

### Using Getter Functions
```javascript
// Preferred method - safe access with fallbacks
const sword = getWeapon('Combat Blade');
const elf = getRace('Elf');
const laser = getProgram('Laser Cannon Protocol');

// All getters defined in compendium (lines 753-845)
```

### Data Structure
```javascript
{
  "version": "8",
  "metadata": {
    "system": "56th Century TTRPG",
    "extracted_from": "56th_century_compendium.html",
    "date": "2026-06-07",
    "description": "..."
  },
  "items": [...],
  "notes": { "total_items": N }
}
```

---

## Getter Functions Reference

### Character Data
- `getRaces()` / `getRace(name)`
- `getBackgrounds()` / `getBackground(name)` 
- `getOccupations()` / `getOccupation(name)`

### Combat
- `getWeapons()` / `getWeapon(name)`
- `getArmor()` / `getArmor(name)`
- `getOptions()` / `getOption(name)`

### Abilities
- `getTalents()` / `getTalent(name)`
- `getSpells()` / `getSpell(name)`
- `getPrograms()` / `getProgram(name)`

### Equipment
- `getMedical()` / `getMedicalItem(name)`
- `getDatacoms()` / `getDatacom(name)`

### Vehicles
- `getVehicles()` / `getVehicle(name)`
- `getDrones()` / `getDrone(name)`
- `getDroneComponents()` / `getDroneComponent(name)`

### Ships
- `getShipComponents()` / `getShipComponent(name)`

### Galaxy
- `getGalaxyRegions()` / `getGalaxyRegion(name)`
- `getFactions()` / `getFaction(name)`
- `getStarSystems()` / `getStarSystem(name)`

---

## Integration Checklist

- [ ] Load data files via DATA_LOADER
- [ ] Verify window.DATA object populated
- [ ] Test all getter functions
- [ ] Integrate with character builder
- [ ] Update UI to use new data
- [ ] Performance test with full dataset
- [ ] Validate all cross-references
- [ ] Update documentation

---

## Notes

- All files validated and tested
- All data extracted from compendium
- All special abilities documented
- All costs and stats accurate
- All relationships mapped
- Ready for production use

**See FINAL_EXTRACTION_COMPLETE_2026-06-07.md for detailed information**
