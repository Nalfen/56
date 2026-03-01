#!/usr/bin/env python3
"""
Inject ENGINE components as the first item in the internal[] array
for frigates, cruisers, battlecruisers, carriers, and novas.
"""

import json
import re
import sys

ENGINES = {
    # FRIGATES
    "UNIVERSAL FRIGATE": "ENGINEBALANCED_4-FRIGATE_2-AVERAGE",
    "ESCORT FRIGATE": "ENGINECOMBAT_4-FRIGATE_3-GOOD",
    "YACHT FRIGATE": "ENGINEHANDLING_4-FRIGATE_3-GOOD",
    "ASSAULT FRIGATE": "ENGINECOMBAT_4-FRIGATE_3-GOOD",
    "JUNKER FRIGATE": "ENGINEBALANCED_4-FRIGATE_1-BASIC",
    "SCOUT FRIGATE": "ENGINEHANDLING_4-FRIGATE_3-GOOD",
    "HOPPER FRIGATE": "ENGINEHANDLING_4-FRIGATE_2-AVERAGE",
    "SCIENCE FRIGATE": "ENGINEBALANCED_4-FRIGATE_2-AVERAGE",
    "REPAIR FRIGATE": "ENGINEBALANCED_4-FRIGATE_2-AVERAGE",
    # CRUISERS
    "UNIVERSAL CRUISER": "ENGINEBALANCED_5-CRUISER_2-AVERAGE",
    "FREIGHTER CRUISER": "ENGINEBALANCED_5-CRUISER_1-BASIC",
    "DEEPSPACEEXPLORER CRUISER": "ENGINEHANDLING_5-CRUISER_3-GOOD",
    "SUPERLINER CRUISER": "ENGINEBALANCED_5-CRUISER_2-AVERAGE",
    "RESEARCH CRUISER": "ENGINEBALANCED_5-CRUISER_2-AVERAGE",
    "TANKER CRUISER": "ENGINEBALANCED_5-CRUISER_1-BASIC",
    "DESTROYER CRUISER": "ENGINECOMBAT_5-CRUISER_3-GOOD",
    "MEGAYATCHT CRUISER": "ENGINEHANDLING_5-CRUISER_3-GOOD",
    # BATTLECRUISERS
    "UNIVERSAL BATTLECRUISER": "ENGINEBALANCED_6-BATTLECRUISER_2-AVERAGE",
    "PIRATEFREIGHTER BATTLECRUISER": "ENGINEBALANCED_6-BATTLECRUISER_1-BASIC",
    "GATESHIP BATTLECRUISER": "ENGINEBALANCED_6-BATTLECRUISER_2-AVERAGE",
    "GATESEC BATTLECRUISER": "ENGINECOMBAT_6-BATTLECRUISER_3-GOOD",
    "JUGGERNAUT BATTLECRUISER": "ENGINECOMBAT_6-BATTLECRUISER_3-GOOD",
    # CARRIERS
    "UNIVERSAL CARRIER": "ENGINEBALANCED_7-CARRIER_2-AVERAGE",
    "MEGACARGO CARRIER": "ENGINEBALANCED_7-CARRIER_1-BASIC",
    "INDUSTRIAL CARRIER": "ENGINEBALANCED_7-CARRIER_1-BASIC",
    "MEGALINER CARRIER": "ENGINEBALANCED_7-CARRIER_2-AVERAGE",
    "MISSILE CARRIER": "ENGINECOMBAT_7-CARRIER_3-GOOD",
    "HIVE CARRIER": "ENGINEBALANCED_7-CARRIER_2-AVERAGE",
    # NOVAS
    "UNIVERSAL NOVA": "ENGINEBALANCED_8-NOVA_2-AVERAGE",
    "INTERDICTOR NOVA": "ENGINECOMBAT_8-NOVA_3-GOOD",
    "OBLITERATOR NOVA": "ENGINECOMBAT_8-NOVA_3-GOOD",
    "GENERATIONSHIP NOVA": "ENGINEBALANCED_8-NOVA_1-BASIC",
    "BEHEMOT NOVA": "ENGINEBALANCED_8-NOVA_3-GOOD",
}

def inject_engines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    injected = []
    skipped = []
    not_found = []

    for ship_name, engine_code in ENGINES.items():
        # Find the ship by name
        name_pattern = f'"name":"{ship_name}"'
        name_idx = content.find(name_pattern)

        if name_idx < 0:
            not_found.append(ship_name)
            continue

        # Find "internal":[ after the ship name
        internal_pattern = '"internal":['
        internal_idx = content.find(internal_pattern, name_idx)

        if internal_idx < 0:
            print(f"ERROR: Could not find internal array for {ship_name}")
            sys.exit(1)

        # Position right after the opening bracket
        insert_pos = internal_idx + len(internal_pattern)

        # Check what comes right after the [
        rest = content[insert_pos:insert_pos+50]

        # Check if already has an engine (skip if so)
        if rest.startswith('"ENGINE'):
            skipped.append((ship_name, rest[:30]))
            continue

        # Inject engine as first item
        # If array is non-empty, add comma after engine
        if rest.startswith(']'):
            # Empty internal array
            new_content = content[:insert_pos] + f'"{engine_code}"' + content[insert_pos:]
        else:
            # Non-empty array - insert engine + comma at start
            new_content = content[:insert_pos] + f'"{engine_code}",' + content[insert_pos:]

        content = new_content
        injected.append((ship_name, engine_code))

    print(f"\n=== RESULTS ===")
    print(f"Injected ({len(injected)}):")
    for name, engine in injected:
        print(f"  {name} -> {engine}")

    if skipped:
        print(f"\nSkipped (already has engine) ({len(skipped)}):")
        for name, existing in skipped:
            print(f"  {name}: {existing}")

    if not_found:
        print(f"\nNOT FOUND ({len(not_found)}):")
        for name in not_found:
            print(f"  {name}")

    if injected:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nFile written successfully.")

    return len(not_found) == 0

if __name__ == '__main__':
    filepath = '/home/user/56/56th_century_compendium_v8.html'
    success = inject_engines(filepath)
    sys.exit(0 if success else 1)
