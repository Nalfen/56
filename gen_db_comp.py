#!/usr/bin/env python3
"""Generate DB_COMP JS block from drone_components_final.csv"""
import csv
from collections import OrderedDict

# Known good icons from current HTML (fallback)
ICON_MAP = {
    'POWER_CELL': '⚡', 'SOLAR_PANEL': '☀', 'ENERGY_BANK': '🔋',
    'FUSION_CORE': '⚛', 'CORONTHIA_REACTOR': '🔥', 'FUEL_CELL': '🛢',
    'DRIVE_AQUATIC': '🌊', 'DRIVE_CLIMBER': '🦎', 'DRIVE_TRACKED': '🚜',
    'DRIVE_HOVER': '💨', 'DRIVE_FLYER': '🦅', 'JUMP_JETS': '🚀',
    'DRIVE_OVERHAUL': '⚙', 'WEIGHT_REDUCTION': '⬇', 'CARGO_HARDPOINT': '🪝',
    'SENSOR_OPTICAL': '👁', 'SENSOR_THERMAL': '🌡', 'SENSOR_CHEMICAL': '🧪',
    'SENSOR_BIOMETRIC': '🧬', 'SENSOR_EM': '📡', 'SENSOR_TRACKING': '🎯',
    'ARMOR_COMBAT': '🛡', 'ARMOR_TECH': '🔮', 'ARMOR_SPIRIT': '✨',
    'SHIELD_ENERGY': '💠', 'REACTIVE_ARMOR': '💥', 'HULL_REINFORCE': '🔩',
    'REPAIR_SYS': '🩺', 'WEAPON_MOUNT': '🔫', 'AMMO_STORAGE': '📦',
    'TARGETING_COMP': '🎯', 'ECM_SUITE': '📻', 'STEALTH_SYSTEM': '👻',
    'ARM_GRIPPER': '🦾', 'ARM_PRECISION': '✋', 'ARM_HEAVY': '💪',
    'HACK_TERMINAL': '💻', 'DATA_CORE': '💾', 'TECH_SCANNER': '🔬',
    'COMM_ARRAY': '📻', 'COMM_JAMMER': '📵', 'COMM_RELAY': '🔁',
    'BROADCAST_UNIT': '📢', 'MED_SYSTEM': '💊', 'TRAUMA_BAY': '🏥',
    'REPAIR_ARM': '🔧', 'FABRICATOR': '⚙', 'NANITE_SYS': '🦠',
    'STORAGE_BAY': '📦', 'SURVEY_KIT': '🗺', 'RECORDER_SYS': '🎥',
    'RESCUE_KIT': '🆘', 'EXPLOSIVE_UNIT': '💣', 'ENV_SYSTEM': '🌬',
    'NEURAL_PROC': '🖥', 'SKILL_MODULE': '🧠',
}

def to_int_if_whole(v):
    """Convert float string to int if whole number, else float, else return None."""
    if v == '' or v is None:
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except:
        return None

def parse_bool(v):
    if v == 'True': return True
    if v == 'False': return False
    return None

def js_val(v):
    """Format a Python value as JS literal."""
    if v is True: return 'true'
    if v is False: return 'false'
    if isinstance(v, str): return f"'{v}'"
    if isinstance(v, int): return str(v)
    if isinstance(v, float): return str(v)
    return str(v)

with open('/home/user/56/drone_components_final.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Group by type_key preserving order
components = OrderedDict()
for row in rows:
    tk = row['type_key']
    if tk not in components:
        components[tk] = {
            'cat_name': row['cat_name'],
            'icon': ICON_MAP.get(tk, row['icon']),
            'loc': row['loc'].split('|'),
            'exclusive': parse_bool(row['exclusive']),
            'tiers': []
        }

    tier = {}

    # Core fields always present
    tier['name'] = row['tier_name']

    # Numeric fields - only include if non-empty
    def add_num(key, csv_key=None):
        csv_k = csv_key or key
        v = to_int_if_whole(row.get(csv_k, ''))
        if v is not None:
            tier[key] = v

    add_num('slots')
    add_num('pwr')
    add_num('pwr_give')
    add_num('price')
    add_num('dc')
    add_num('dur', 'component_dur')

    # Rarity/legality always present
    tier['rarity'] = row['rarity']
    tier['legality'] = row['legality']

    # Optional string fields
    if row.get('autonomy', '').strip():
        tier['autonomy'] = row['autonomy']
    if row.get('note', '').strip():
        tier['note'] = row['note']

    # Numeric optional fields
    spd = to_int_if_whole(row.get('spd_mod', ''))
    if spd is not None:
        tier['spd_mod'] = spd

    dur_b = to_int_if_whole(row.get('dur_bonus', ''))
    if dur_b is not None:
        tier['dur_bonus'] = dur_b

    sys_b = to_int_if_whole(row.get('sys_bonus', ''))
    if sys_b is not None:
        tier['sys_bonus'] = sys_b

    if row.get('soak_bonus', '').strip():
        # soak_bonus is a string like '1D+2'
        tier['soak_bonus'] = row['soak_bonus']

    # Defense tiers
    for df, jsf in [('phys_def','phys'),('energy_def','energy'),('tech_def','tech'),('spirit_def','spirit')]:
        if row.get(df, '').strip():
            tier[jsf] = row[df]

    # Sensor fields
    aw = to_int_if_whole(row.get('awareness', ''))
    if aw is not None:
        tier['awareness'] = aw
    if row.get('sensor_range', '').strip():
        tier['range'] = row['sensor_range']

    # Comms
    if row.get('comm_range', '').strip():
        tier['comm_range'] = row['comm_range']
    ecm = to_int_if_whole(row.get('ecm', ''))
    if ecm is not None:
        tier['ecm'] = ecm

    # Ammo
    ammo = to_int_if_whole(row.get('ammo_cap', ''))
    if ammo is not None:
        tier['ammo_cap'] = ammo

    # Drive
    if row.get('drive_mode', '').strip():
        tier['mode'] = row['drive_mode']
    spd2 = to_int_if_whole(row.get('drive_speed', ''))
    if spd2 is not None:
        tier['speed'] = spd2

    # Weapon mount
    if row.get('weapon_type', '').strip():
        tier['weapon_type'] = row['weapon_type']
    if row.get('weapon_size', '').strip():
        tier['weapon_size'] = row['weapon_size']
    needs = parse_bool(row.get('needs_ammo', ''))
    if needs is not None:
        tier['needs_ammo'] = needs
    aim = parse_bool(row.get('auto_aim', ''))
    if aim is not None:
        tier['auto_aim'] = aim

    # Arms
    arms = to_int_if_whole(row.get('arms', ''))
    if arms is not None:
        tier['arms'] = arms
    str_v = to_int_if_whole(row.get('str', ''))
    if str_v is not None:
        tier['str'] = str_v
    fm = parse_bool(row.get('fine_motor', ''))
    if fm is not None:
        tier['fine_motor'] = fm

    # Skills
    skn = to_int_if_whole(row.get('skills_n', ''))
    if skn is not None:
        tier['skills_n'] = skn
    skr = to_int_if_whole(row.get('skill_rank', ''))
    if skr is not None:
        tier['rank'] = skr

    components[tk]['tiers'].append(tier)

# Category order from CSV
CAT_ORDER = ['POWER','PROPULSION','SENSING','DEFENSE','WEAPONS','COMBAT_SUPPORT',
             'MANIPULATION','HACKING','COMMS','MEDICAL','ENGINEERING','UTILITY',
             'PROCESSING','AI']

# Group types by category
cat_to_types = OrderedDict()
for tk, comp in components.items():
    cat = None
    # Re-read category from CSV
    for row in rows:
        if row['type_key'] == tk:
            cat = row['category']
            break
    if cat not in cat_to_types:
        cat_to_types[cat] = []
    cat_to_types[cat].append(tk)

# Category display names
CAT_LABELS = {
    'POWER': 'POWER', 'PROPULSION': 'PROPULSION (secondary drives)',
    'SENSING': 'SENSING', 'DEFENSE': 'DEFENSE', 'WEAPONS': 'WEAPONS',
    'COMBAT_SUPPORT': 'COMBAT SUPPORT', 'MANIPULATION': 'MANIPULATION',
    'HACKING': 'HACKING', 'COMMS': 'COMMS', 'MEDICAL': 'MEDICAL',
    'ENGINEERING': 'ENGINEERING', 'UTILITY': 'UTILITY',
    'PROCESSING': 'PROCESSING', 'AI': 'AI',
}

lines = ['const DB_COMP={']

for cat in CAT_ORDER:
    if cat not in cat_to_types:
        continue
    label = CAT_LABELS.get(cat, cat)
    lines.append(f'  // ── {label} {"─"*(68-len(label))}')

    for tk in cat_to_types[cat]:
        comp = components[tk]
        icon = comp['icon']
        loc_str = '[' + ','.join(f"'{l}'" for l in comp['loc']) + ']'

        excl_str = ''
        if comp['exclusive'] is True:
            excl_str = 'exclusive:true,'

        lines.append(f"  {tk}:{{name:'{comp['cat_name']}',icon:'{icon}',loc:{loc_str},{excl_str}")
        lines.append(f"    tiers:[")

        for tier in comp['tiers']:
            parts = []
            for k, v in tier.items():
                parts.append(f"{k}:{js_val(v)}")
            lines.append(f"      {{{','.join(parts)}}},")

        lines.append(f"    ]}},")

lines.append('};')

result = '\n'.join(lines)

# Write to file for inspection
with open('/home/user/56/db_comp_new.js', 'w', encoding='utf-8') as f:
    f.write(result)

print("Generated db_comp_new.js")
print(f"Component types: {len(components)}")
for cat in CAT_ORDER:
    if cat in cat_to_types:
        print(f"  {cat}: {cat_to_types[cat]}")
