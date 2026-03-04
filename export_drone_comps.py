#!/usr/bin/env python3
"""
Export drone component data from 56th_century_compendium_v8.html to CSV.
Re-run after editing the CSV to validate, or use import_drone_comps.py to push back.
"""
import re, csv, sys

HTML = '56th_century_compendium_v8.html'
OUT  = 'drone_components.csv'

# Category comment markers (in order they appear in DB_COMP)
CATEGORY_COMMENTS = [
    ('POWER',           '// ── POWER'),
    ('PROPULSION',      '// ── PROPULSION'),
    ('SENSING',         '// ── SENSING'),
    ('DEFENSE',         '// ── DEFENSE'),
    ('WEAPONS',         '// ── WEAPONS'),
    ('COMBAT_SUPPORT',  '// ── COMBAT SUPPORT'),
    ('MANIPULATION',    '// ── MANIPULATION'),
    ('HACKING',         '// ── HACKING'),
    ('COMMS',           '// ── COMMS'),
    ('MEDICAL',         '// ── MEDICAL'),
    ('ENGINEERING',     '// ── ENGINEERING'),
    ('UTILITY',         '// ── UTILITY'),
    ('PROCESSING',      '// ── PROCESSING'),
    ('AI',              '// ── AI'),
]

# All possible tier fields and their CSV column names / default values
COLUMNS = [
    'type_key',
    'category',
    'cat_name',
    'icon',
    'loc',          # pipe-separated: core|int|ext
    'exclusive',    # TRUE / FALSE
    'tier_index',
    'tier_name',
    'slots',
    'pwr',
    'pwr_give',
    'price',
    'dc',
    'component_dur',
    'rarity',
    'legality',
    'autonomy',
    'note',
    'spd_mod',
    'dur_bonus',
    'sys_bonus',
    'soak_bonus',
    'phys_def',
    'energy_def',
    'tech_def',
    'spirit_def',
    'awareness',
    'sensor_range',
    'comm_range',
    'ecm',
    'ammo_cap',
    'drive_mode',
    'drive_speed',
    'weapon_type',
    'weapon_size',
    'needs_ammo',
    'auto_aim',
    'arms',
    'str',
    'fine_motor',
    'skills_n',
    'skill_rank',
]

def js_str(s):
    """Strip JS quotes from a value string."""
    s = s.strip()
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    return s

def js_bool(s):
    s = s.strip()
    if s == 'true': return 'TRUE'
    if s == 'false': return 'FALSE'
    return s

def js_num(s):
    return s.strip()

def parse_inline_obj(text):
    """Parse a flat JS object literal like {key:val,key2:val2,...} into a dict.
    Handles string values with commas (unlikely here but safe), arrays, booleans, numbers."""
    result = {}
    # Remove outer braces
    text = text.strip()
    if text.startswith('{') and text.endswith('}'):
        text = text[1:-1]

    # Tokenise key:value pairs. Values can be: number, 'string', true, false
    # We parse char by char to handle nested arrays e.g. loc:[...]
    i = 0
    n = len(text)
    while i < n:
        # Skip whitespace
        while i < n and text[i] in ' \t\n\r': i += 1
        if i >= n: break
        # Read key (identifier, no quotes)
        key_start = i
        while i < n and text[i] not in ':,': i += 1
        key = text[key_start:i].strip()
        if not key: i += 1; continue
        if i >= n: break
        i += 1  # skip ':'
        # Skip whitespace
        while i < n and text[i] in ' \t\n\r': i += 1
        if i >= n: break
        # Read value
        ch = text[i]
        if ch in ("'", '"'):
            # String
            q = ch; i += 1; val = ''
            while i < n and text[i] != q:
                if text[i] == '\\': i += 1
                val += text[i]; i += 1
            i += 1  # closing quote
            result[key] = val
        elif ch == '[':
            # Array (for loc)
            depth = 0; j = i
            while i < n:
                if text[i] == '[': depth += 1
                elif text[i] == ']': depth -= 1;
                i += 1
                if depth == 0: break
            arr_text = text[j+1:i-1]
            vals = [js_str(v) for v in arr_text.split(',') if v.strip()]
            result[key] = '|'.join(vals)
        else:
            # number / true / false / null
            j = i
            while i < n and text[i] not in ',}': i += 1
            raw = text[j:i].strip()
            if raw in ('true','false'):
                result[key] = js_bool(raw)
            else:
                result[key] = raw
        # Skip comma
        while i < n and text[i] in ', \t\n\r': i += 1
    return result

def extract_db_comp(html):
    """Extract the raw DB_COMP block from the HTML file."""
    start = html.find('const DB_COMP={')
    if start == -1:
        sys.exit('ERROR: could not find DB_COMP in HTML')
    # Find the matching closing brace
    depth = 0; i = start + len('const DB_COMP=')
    block_start = i
    while i < len(html):
        if html[i] == '{': depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                return html[block_start:i+1]
        i += 1
    sys.exit('ERROR: DB_COMP block not closed')

def assign_categories(html, type_keys):
    """For each type_key, find its category by looking at the preceding comment."""
    cat_map = {}
    # Build list of (line_number, category) from comments
    lines = html.split('\n')
    current_cat = 'UNKNOWN'
    # Map from type key -> category using the order they appear
    type_positions = {}
    for i, line in enumerate(lines):
        for cat, marker in CATEGORY_COMMENTS:
            if marker in line:
                current_cat = cat
                break
        for key in type_keys:
            pat = re.compile(r'^\s+' + re.escape(key) + r'\s*:')
            if pat.match(line) and key not in type_positions:
                type_positions[key] = (i, current_cat)
    for key, (_, cat) in type_positions.items():
        cat_map[key] = cat
    return cat_map

def parse_component_block(block_text):
    """Parse the whole DB_COMP {...} block and return list of (type_key, meta, tiers)."""
    # Find each top-level key like:  POWER_CELL:{...
    # We'll walk line by line and track brace depth for top-level keys
    components = []
    lines = block_text.split('\n')
    i = 0
    n = len(lines)

    # Regex for top-level component entry
    key_re = re.compile(r'^\s{2}([A-Z_]+)\s*:\s*\{(.*)')
    # inline tiers line
    tier_re = re.compile(r'^\s+\{([^{}]*)\}')

    while i < n:
        line = lines[i]
        m = key_re.match(line)
        if m:
            type_key = m.group(1)
            # Collect the full component body
            # Count braces from this line onward
            body_lines = [line[line.index('{'):]]
            depth = body_lines[0].count('{') - body_lines[0].count('}')
            i += 1
            while i < n and depth > 0:
                body_lines.append(lines[i])
                depth += lines[i].count('{') - lines[i].count('}')
                i += 1
            body = '\n'.join(body_lines)
            # Parse meta fields (name, icon, loc, exclusive) from first line
            meta = {}
            # name
            nm = re.search(r"name\s*:\s*'([^']*)'", body)
            if nm: meta['name'] = nm.group(1)
            # icon
            ic = re.search(r"icon\s*:\s*'([^']*)'", body)
            if ic: meta['icon'] = ic.group(1)
            # loc
            lc = re.search(r"loc\s*:\s*\[([^\]]*)\]", body)
            if lc:
                vals = [js_str(v) for v in lc.group(1).split(',') if v.strip()]
                meta['loc'] = '|'.join(vals)
            else:
                meta['loc'] = ''
            # exclusive
            meta['exclusive'] = 'TRUE' if 'exclusive:true' in body else 'FALSE'
            # Parse tiers — find the tiers:[...] block
            tiers_m = re.search(r'tiers\s*:\s*\[', body)
            tiers = []
            if tiers_m:
                tiers_start = tiers_m.end()
                # Find all tier objects {...} in the tiers array
                j = tiers_start
                blen = len(body)
                while j < blen:
                    # Skip to next '{'
                    while j < blen and body[j] != '{': j += 1
                    if j >= blen: break
                    # Find matching '}'
                    depth2 = 0; k = j
                    while k < blen:
                        if body[k] == '{': depth2 += 1
                        elif body[k] == '}':
                            depth2 -= 1
                            if depth2 == 0:
                                tier_text = body[j:k+1]
                                tiers.append(parse_inline_obj(tier_text))
                                j = k + 1
                                break
                        k += 1
                    else:
                        break
            components.append((type_key, meta, tiers))
            continue
        i += 1
    return components

def main():
    with open(HTML, encoding='utf-8') as f:
        html = f.read()

    block = extract_db_comp(html)
    components = parse_component_block(block)

    type_keys = [c[0] for c in components]
    cat_map = assign_categories(html, type_keys)

    rows = []
    for type_key, meta, tiers in components:
        cat = cat_map.get(type_key, 'UNKNOWN')
        for ti, t in enumerate(tiers):
            row = {
                'type_key':      type_key,
                'category':      cat,
                'cat_name':      meta.get('name', ''),
                'icon':          meta.get('icon', ''),
                'loc':           meta.get('loc', ''),
                'exclusive':     meta.get('exclusive', 'FALSE'),
                'tier_index':    str(ti),
                'tier_name':     t.get('name', ''),
                'slots':         t.get('slots', '0'),
                'pwr':           t.get('pwr', '0'),
                'pwr_give':      t.get('pwr_give', ''),
                'price':         t.get('price', '0'),
                'dc':            t.get('dc', '0'),
                'component_dur': t.get('dur', ''),
                'rarity':        t.get('rarity', ''),
                'legality':      t.get('legality', ''),
                'autonomy':      t.get('autonomy', ''),
                'note':          t.get('note', ''),
                'spd_mod':       t.get('spd_mod', ''),
                'dur_bonus':     t.get('dur_bonus', ''),
                'sys_bonus':     t.get('sys_bonus', ''),
                'soak_bonus':    t.get('soak_bonus', ''),
                'phys_def':      t.get('phys', ''),
                'energy_def':    t.get('energy', ''),
                'tech_def':      t.get('tech', ''),
                'spirit_def':    t.get('spirit', ''),
                'awareness':     t.get('awareness', ''),
                'sensor_range':  t.get('range', ''),
                'comm_range':    t.get('comm_range', ''),
                'ecm':           t.get('ecm', ''),
                'ammo_cap':      t.get('ammo_cap', ''),
                'drive_mode':    t.get('mode', ''),
                'drive_speed':   t.get('speed', ''),
                'weapon_type':   t.get('weapon_type', ''),
                'weapon_size':   t.get('weapon_size', ''),
                'needs_ammo':    t.get('needs_ammo', ''),
                'auto_aim':      t.get('auto_aim', ''),
                'arms':          t.get('arms', ''),
                'str':           t.get('str', ''),
                'fine_motor':    t.get('fine_motor', ''),
                'skills_n':      t.get('skills_n', ''),
                'skill_rank':    t.get('rank', ''),
            }
            rows.append(row)

    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Exported {len(rows)} component tiers across {len(components)} component types → {OUT}')

if __name__ == '__main__':
    main()
