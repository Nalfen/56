import re

with open('/home/user/56/56th_century_compendium_v8.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ─── 1. Replace CSS: add new db classes after .db-empty-msg ───────────────────
OLD_CSS = '.db-empty-icon{font-size:36px;margin-bottom:8px;}.db-empty-msg{font-size:11px;font-family:ShareTechMono,monospace;}'
NEW_CSS = OLD_CSS + (
    '.db-zone-mod{font-size:9px;font-family:ShareTechMono,monospace;color:var(--mu);}'
    '.db-wpn-picker{margin:4px 0 4px 0;padding:8px;background:rgba(0,0,0,.3);border:1px solid rgba(255,107,53,.25);border-radius:3px;}'
    '.db-wpn-list{display:flex;flex-wrap:wrap;gap:3px;max-height:110px;overflow-y:auto;margin-bottom:4px;}'
    '.db-wpn-search{font-size:9px;font-family:ShareTechMono,monospace;background:rgba(255,255,255,.04);border:1px solid var(--b);border-radius:2px;color:var(--tx);padding:2px 6px;}'
    '.rar-classified{border-left:3px solid #ef4444;}'
)
c = c.replace(OLD_CSS, NEW_CSS, 1)

# ─── 2. Update rarCls to include CLASSIFIED ───────────────────────────────────
OLD_RARCLS = "  if(u==='UNIQUE')   return 'rar-unique';\n  return '';"
NEW_RARCLS = "  if(u==='UNIQUE')   return 'rar-unique';\n  if(u==='CLASSIFIED') return 'rar-classified';\n  return '';"
c = c.replace(OLD_RARCLS, NEW_RARCLS, 1)

# ─── 3. Replace dbState + dbAdd init ─────────────────────────────────────────
OLD_STATE = "let dbState={name:'Unnamed Drone',size:null,mob:null,atmo:false,core:[],internal:[],external:[]};\nlet dbAdd={loc:null,type:null,tier:0,skills:[]};"
NEW_STATE = "let dbState={name:'Unnamed Drone',size:null,mob:null,atmo:false,core:[],internal:[],external:[],wpnPicker:null};\nlet dbAdd={loc:null,type:null,tier:0,skills:[],wpnSearch:''};"
c = c.replace(OLD_STATE, NEW_STATE, 1)

# ─── 4. Update input handler to handle wpnsearch ─────────────────────────────
OLD_INP = "document.addEventListener('input',e=>{const ni=e.target.closest('#db-name-inp');if(ni)dbState.name=ni.value;});"
NEW_INP = "document.addEventListener('input',e=>{const ni=e.target.closest('#db-name-inp');if(ni){dbState.name=ni.value;return;}if(e.target.dataset&&e.target.dataset.db==='wpnsearch'){dbAdd.wpnSearch=e.target.value;render();}});"
c = c.replace(OLD_INP, NEW_INP, 1)

# ─── 5. Update event handlers: add wpn* handlers and fix 'open:' to clear wpnPicker ─
OLD_OPEN_H = "    else if(v.startsWith('open:')){dbAdd={loc:v.slice(5),type:null,tier:0,skills:[]};render();}"
NEW_OPEN_H = "    else if(v.startsWith('open:')){dbState.wpnPicker=null;dbAdd={loc:v.slice(5),type:null,tier:0,skills:[],wpnSearch:''};render();}"
c = c.replace(OLD_OPEN_H, NEW_OPEN_H, 1)

OLD_SIZE_H = "    if(v.startsWith('size:')){dbState.size=v.slice(5);dbAdd={loc:null,type:null,tier:0,skills:[]};render();}"
NEW_SIZE_H = "    if(v.startsWith('size:')){dbState.size=v.slice(5);dbState.wpnPicker=null;dbAdd={loc:null,type:null,tier:0,skills:[],wpnSearch:''};render();}"
c = c.replace(OLD_SIZE_H, NEW_SIZE_H, 1)

OLD_RESET_H = "    else if(v==='reset'){\n      dbState={name:'Unnamed Drone',size:null,mob:null,atmo:false,core:[],internal:[],external:[]};\n      dbAdd={loc:null,type:null,tier:0,skills:[]};\n      render();\n    }"
NEW_RESET_H = (
    "    else if(v.startsWith('wpnpick:')){"
    "const[,wz,wi]=v.split(':');dbState.wpnPicker={zone:wz,idx:parseInt(wi)};dbAdd.loc=null;render();}\n"
    "    else if(v==='wpnsel'){"
    "if(dbState.wpnPicker){const{zone,idx}=dbState.wpnPicker;const lk=zone==='core'?'core':zone==='int'?'internal':'external';if(dbState[lk][idx])dbState[lk][idx].weapon=dbEl.dataset.wpn;}render();}\n"
    "    else if(v==='wpndone'||v==='wpnclose'){dbState.wpnPicker=null;render();}\n"
    "    else if(v==='reset'){\n"
    "      dbState={name:'Unnamed Drone',size:null,mob:null,atmo:false,core:[],internal:[],external:[],wpnPicker:null};\n"
    "      dbAdd={loc:null,type:null,tier:0,skills:[],wpnSearch:''};\n"
    "      render();\n"
    "    }"
)
c = c.replace(OLD_RESET_H, NEW_RESET_H, 1)

print("CSS/handlers done, replacing drone builder JS section...")


# ─── 6. Replace the entire drone builder JS section ──────────────────────────
DRONE_JS_START = """// ═══════════════════════════════════════════════════════════════════════════════
// ─── Drone Builder ────────────────────────────────────────────────────────────
// ═══════════════════════════════════════════════════════════════════════════════"""
DRONE_JS_END = "g.catalog.drone_parts=buildDroneParts();"

start_idx = c.find(DRONE_JS_START)
end_idx = c.find(DRONE_JS_END) + len(DRONE_JS_END)
assert start_idx >= 0, "Drone builder start not found"
assert end_idx > start_idx, "Drone builder end not found"

NEW_DRONE_JS = r"""// ═══════════════════════════════════════════════════════════════════════════════
// ─── Drone Builder ────────────────────────────────────────────────────────────
// ═══════════════════════════════════════════════════════════════════════════════

const DB_SIZES={
  TINY:  {name:'Tiny',   slots:12, dur:4,  sys:2,  soak:'0',    spd_mod:2,  price:2000,   dc:1},
  SMALL: {name:'Small',  slots:18, dur:6,  sys:3,  soak:'0',    spd_mod:1,  price:5000,   dc:2},
  MED:   {name:'Medium', slots:30, dur:10, sys:4,  soak:'1',    spd_mod:0,  price:12000,  dc:3},
  LARGE: {name:'Large',  slots:42, dur:15, sys:6,  soak:'1D',   spd_mod:-2, price:30000,  dc:4},
  XL:    {name:'X-Large',slots:54, dur:22, sys:8,  soak:'1D+1', spd_mod:-4, price:80000,  dc:5},
  HUGE:  {name:'Huge',   slots:72, dur:35, sys:10, soak:'1D+2', spd_mod:-6, price:200000, dc:6},
};
const DB_MOB={
  STATIC:{name:'Stationary', base_mode:null,  base_spd:0,  alt_mode:null, alt_spd:0, price:0,     dc:0},
  WALK:  {name:'Walker',     base_mode:'Walk',base_spd:10, alt_mode:null, alt_spd:0, price:2000,  dc:1},
  CLIMB: {name:'Climber',    base_mode:'Walk',base_spd:10, alt_mode:'Climb',alt_spd:6,price:3000, dc:1},
  HOVER: {name:'Hover',      base_mode:'Hover',base_spd:14,alt_mode:null, alt_spd:0, price:5000,  dc:2},
  FLY:   {name:'Flyer',      base_mode:'Fly', base_spd:20, alt_mode:null, alt_spd:0, price:10000, dc:3},
};
const DB_ZONE={
  core:    {label:'CORE',     color:'#00c8ff', dc_mod:1,  cost_mod:1.30, info:'+1 DC / x1.3 cost (protected)'},
  internal:{label:'INTERNAL', color:'#a855f7', dc_mod:0,  cost_mod:1.00, info:'Standard DC & cost'},
  external:{label:'EXTERNAL', color:'#ff6b35', dc_mod:-1, cost_mod:0.85, info:'-1 DC / x0.85 cost (exposed)'},
};
const DB_DEF_RANKS=['NONE','LOW','MEDIUM','HIGH','EXTREME'];
const DB_SKILLS={
  Physical:['Athletics','Craft','Heavy Weapons','Martial Arts','Might','Piloting','Repair','Resilience','Scavenge','Survival'],
  Mental:  ['Academic','Cyberintel','Engineering','Galactic Knowledge','Hacking','Medicine','Navigation','Parascience','Science','Technology'],
  Social:  ['Acting','Charm','Etiquette','Flair','Intimidation','Leadership','Negotiation','Spiritual','Streetwise','Subterfuge'],
  Acuity:  ['Awareness','Binding','Concealment','Dexterity','Gunslinger','Intuition','Marksman','Operator','Search','Tactics'],
};

const DB_COMP={
  // ── POWER ──────────────────────────────────────────────────────────────────
  POWER_CELL:{name:'Power Cell',icon:'⚡',loc:['core'],
    tiers:[
      {name:'Micro Cell',    pwr_give:6,  pwr:0,slots:1,price:500,   dc:1,dur:3, rarity:'COMMON',    legality:'LEGAL'},
      {name:'Standard Cell', pwr_give:12, pwr:0,slots:2,price:1500,  dc:2,dur:4, rarity:'COMMON',    legality:'LEGAL'},
      {name:'Power Bank',    pwr_give:22, pwr:0,slots:3,price:4000,  dc:3,dur:5, rarity:'UNCOMMON',  legality:'LEGAL'},
      {name:'Reactor Core',  pwr_give:40, pwr:0,slots:4,price:12000, dc:5,dur:6, rarity:'RARE',      legality:'RESTRICTED'},
      {name:'Fusion Reactor',pwr_give:70, pwr:0,slots:6,price:35000, dc:7,dur:8, rarity:'CLASSIFIED',legality:'MILITARY'},
    ]},
  SOLAR_PANEL:{name:'Solar Panel',icon:'☀',loc:['ext'],
    tiers:[
      {name:'Basic Array',    pwr_give:3, pwr:0,slots:2,price:800,   dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL',note:'Generates power in light only'},
      {name:'Efficient Array',pwr_give:6, pwr:0,slots:3,price:2500,  dc:2,dur:2, rarity:'UNCOMMON',legality:'LEGAL',note:'Generates power in light only'},
      {name:'Deep Cycle',     pwr_give:10,pwr:0,slots:4,price:8000,  dc:3,dur:3, rarity:'RARE',    legality:'LEGAL',note:'Stores 4hr power surplus'},
    ]},
  ENERGY_BANK:{name:'Energy Bank',icon:'🔋',loc:['core','int'],
    tiers:[
      {name:'Capacitor',    pwr_give:3, pwr:0,slots:1,price:600,  dc:1,dur:3, rarity:'COMMON',  legality:'LEGAL',note:'Stores 1hr surplus power'},
      {name:'Power Buffer', pwr_give:6, pwr:0,slots:2,price:2000, dc:2,dur:4, rarity:'UNCOMMON',legality:'LEGAL',note:'Stores 4hr surplus power'},
      {name:'Hypercharged', pwr_give:12,pwr:0,slots:3,price:7000, dc:4,dur:5, rarity:'RARE',    legality:'LEGAL',note:'Stores 12hr surplus power'},
    ]},
  // ── PROPULSION (secondary drives) ─────────────────────────────────────────
  DRIVE_AQUATIC:{name:'Aquatic Drive',icon:'🌊',loc:['ext'],
    tiers:[
      {name:'Swim Fins',    mode:'Swim',speed:8, pwr:2,slots:2,price:2000,  dc:2,dur:4, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Jet Drive',    mode:'Swim',speed:14,pwr:4,slots:3,price:6000,  dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Combat Sub',   mode:'Swim',speed:18,pwr:5,slots:4,price:18000, dc:5,dur:6, rarity:'RARE',    legality:'RESTRICTED',note:'Depth rated to 2km'},
    ]},
  DRIVE_CLIMBER:{name:'Climbing Drive',icon:'🦎',loc:['ext'],
    tiers:[
      {name:'Gecko Pads',  mode:'Climb',speed:8, pwr:2,slots:2,price:2500,  dc:2,dur:4, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Mag Treads',  mode:'Climb',speed:12,pwr:3,slots:3,price:6000,  dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL',note:'Metal surfaces only'},
      {name:'Spider Limbs',mode:'Climb',speed:16,pwr:4,slots:4,price:15000, dc:5,dur:5, rarity:'RARE',    legality:'LEGAL'},
    ]},
  DRIVE_TRACKED:{name:'Tracked Drive',icon:'🚜',loc:['ext'],
    tiers:[
      {name:'Light Treads', mode:'Track',speed:8, pwr:2,slots:2,price:1500, dc:2,dur:5, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Combat Treads',mode:'Track',speed:12,pwr:3,slots:3,price:4000, dc:3,dur:7, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Heavy Tracks', mode:'Track',speed:10,pwr:4,slots:4,price:10000,dc:4,dur:10,rarity:'RARE',    legality:'RESTRICTED',dur_bonus:3},
    ]},
  DRIVE_HOVER:{name:'Hover Drive',icon:'💨',loc:['ext'],
    tiers:[
      {name:'Repulsor Unit',mode:'Hover',speed:12,pwr:4,slots:3,price:4000, dc:2,dur:4, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Mag-Lev Array',mode:'Hover',speed:18,pwr:6,slots:4,price:10000,dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'AG Lifters',   mode:'Hover',speed:24,pwr:8,slots:5,price:30000,dc:5,dur:6, rarity:'RARE',    legality:'RESTRICTED'},
    ]},
  DRIVE_FLYER:{name:'Flight Drive',icon:'🦅',loc:['ext'],
    tiers:[
      {name:'Rotor System', mode:'Fly',speed:20,pwr:5, slots:4,price:8000, dc:3,dur:4, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Jet Thrusters',mode:'Fly',speed:30,pwr:8, slots:5,price:18000,dc:4,dur:5, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Gravitic Drive',mode:'Fly',speed:40,pwr:12,slots:6,price:50000,dc:6,dur:6, rarity:'RARE',   legality:'RESTRICTED'},
    ]},
  JUMP_JETS:{name:'Jump Jets',icon:'🚀',loc:['ext'],
    tiers:[
      {name:'Micro Jets',    mode:'Leap',speed:8, pwr:3,slots:2,price:3000, dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL',     note:'3 bursts before recharge'},
      {name:'Booster Pack',  mode:'Leap',speed:15,pwr:5,slots:3,price:8000, dc:4,dur:4, rarity:'RARE',    legality:'RESTRICTED',note:'5 bursts before recharge'},
      {name:'Thruster Array',mode:'Leap',speed:25,pwr:8,slots:4,price:20000,dc:6,dur:5, rarity:'LIMITED', legality:'MILITARY',  note:'Unlimited short burst jumps'},
    ]},
  // ── SENSING ───────────────────────────────────────────────────────────────
  SENSOR_OPTICAL:{name:'Optical Sensor',icon:'👁',loc:['core','int','ext'],
    tiers:[
      {name:'Basic Camera', awareness:1,range:'20m', pwr:1,slots:1,price:500,   dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL'},
      {name:'HD Array',     awareness:2,range:'60m', pwr:2,slots:2,price:2000,  dc:2,dur:3, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'LIDAR Suite',  awareness:3,range:'200m',pwr:3,slots:3,price:8000,  dc:4,dur:4, rarity:'RARE',    legality:'LEGAL'},
      {name:'Deep Vision',  awareness:4,range:'500m',pwr:5,slots:4,price:25000, dc:6,dur:5, rarity:'LIMITED', legality:'RESTRICTED'},
    ]},
  SENSOR_THERMAL:{name:'Thermal Sensor',icon:'🌡',loc:['core','int','ext'],
    tiers:[
      {name:'Heat Detector',awareness:1,range:'15m', pwr:2,slots:1,price:800,  dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Thermal Array',awareness:2,range:'50m', pwr:3,slots:2,price:3000, dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'IR Scanner',   awareness:3,range:'150m',pwr:4,slots:3,price:10000,dc:4,dur:4, rarity:'RARE',    legality:'LEGAL'},
    ]},
  SENSOR_CHEMICAL:{name:'Chemical Sensor',icon:'🧪',loc:['int','ext'],
    tiers:[
      {name:'Sniffer Array', awareness:1,range:'10m', pwr:1,slots:1,price:600,   dc:2,dur:2, rarity:'COMMON',  legality:'LEGAL',     note:'Detects explosives, drugs, biologicals'},
      {name:'Spectrometer',  awareness:2,range:'30m', pwr:2,slots:2,price:3000,  dc:3,dur:3, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Full chemical analysis'},
      {name:'Neural Gas Det.',awareness:3,range:'100m',pwr:3,slots:2,price:10000,dc:5,dur:3, rarity:'RARE',    legality:'MILITARY',  note:'Detects nerve agents and bioweapons'},
    ]},
  SENSOR_BIOMETRIC:{name:'Biometric Sensor',icon:'🧬',loc:['int','ext'],
    tiers:[
      {name:'ID Scanner',    awareness:1,range:'10m',pwr:1,slots:1,price:1000, dc:2,dur:2, rarity:'UNCOMMON',legality:'LEGAL',     note:'Reads biometrics and ID implants'},
      {name:'Medical Scan',  awareness:2,range:'20m',pwr:3,slots:2,price:5000, dc:3,dur:3, rarity:'RARE',    legality:'RESTRICTED',note:'Full life-signs analysis'},
      {name:'Psych Profiler',awareness:3,range:'10m',pwr:4,slots:3,price:20000,dc:6,dur:3, rarity:'LIMITED', legality:'MILITARY',  note:'Behavioral and emotional analysis'},
    ]},
  SENSOR_EM:{name:'EM Sensor',icon:'📡',loc:['core','int','ext'],
    tiers:[
      {name:'EM Detector',  awareness:1,range:'30m', pwr:2,slots:2,price:1200, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',     note:'Detects powered devices'},
      {name:'RF Array',     awareness:2,range:'100m',pwr:3,slots:3,price:4000, dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL',     note:'Full spectrum radio intercept'},
      {name:'Signal Intel', awareness:3,range:'1km', pwr:5,slots:4,price:15000,dc:5,dur:4, rarity:'RARE',    legality:'RESTRICTED',note:'Comms intercept and decryption'},
    ]},
  SENSOR_TRACKING:{name:'Tracking System',icon:'🎯',loc:['core','int','ext'],
    tiers:[
      {name:'Motion Track',  awareness:1,range:'50m', pwr:2,slots:2,price:1500, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Multi-Track',   awareness:2,range:'150m',pwr:4,slots:3,price:6000, dc:4,dur:4, rarity:'UNCOMMON',legality:'LEGAL',    note:'Tracks up to 20 targets'},
      {name:'Target Network',awareness:3,range:'500m',pwr:6,slots:4,price:20000,dc:6,dur:5, rarity:'RARE',    legality:'MILITARY', note:'Network target sharing'},
    ]},
  // ── DEFENSE ───────────────────────────────────────────────────────────────
  ARMOR_COMBAT:{name:'Combat Armor',icon:'🛡',loc:['ext'],exclusive:true,
    tiers:[
      {name:'Light Plate',  phys:'LOW',   energy:'LOW',   tech:'NONE',  spirit:'NONE', soak_bonus:2, spd_mod:-1,dur_bonus:3,  pwr:0,slots:2,price:2000,  dc:2,dur:6, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Combat Shell', phys:'MEDIUM',energy:'LOW',   tech:'NONE',  spirit:'NONE', soak_bonus:4, spd_mod:-2,dur_bonus:6,  pwr:0,slots:4,price:5000,  dc:3,dur:8, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Heavy Plate',  phys:'HIGH',  energy:'MEDIUM',tech:'NONE',  spirit:'NONE', soak_bonus:6, spd_mod:-3,dur_bonus:10, pwr:0,slots:6,price:15000, dc:5,dur:10,rarity:'RARE',    legality:'RESTRICTED'},
      {name:'Siege Armor',  phys:'EXTREME',energy:'HIGH', tech:'NONE',  spirit:'NONE', soak_bonus:10,spd_mod:-5,dur_bonus:15, pwr:0,slots:8,price:45000, dc:7,dur:14,rarity:'LIMITED', legality:'MILITARY'},
    ]},
  ARMOR_TECH:{name:'Tech-Resist Armor',icon:'🔮',loc:['ext'],exclusive:true,
    tiers:[
      {name:'Faraday Shell',  phys:'NONE',energy:'NONE',  tech:'LOW',   spirit:'NONE', soak_bonus:1, spd_mod:0, dur_bonus:2, pwr:1,slots:2,price:3000, dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'ECM Plating',    phys:'NONE',energy:'LOW',   tech:'MEDIUM',spirit:'NONE', soak_bonus:2, spd_mod:-1,dur_bonus:4, pwr:2,slots:4,price:8000, dc:4,dur:7, rarity:'RARE',    legality:'RESTRICTED'},
      {name:'Nullfield Hull', phys:'LOW', energy:'MEDIUM',tech:'HIGH',  spirit:'NONE', soak_bonus:4, spd_mod:-2,dur_bonus:8, pwr:3,slots:6,price:25000,dc:6,dur:10,rarity:'LIMITED', legality:'MILITARY'},
    ]},
  ARMOR_SPIRIT:{name:'Spiritual Shielding',icon:'✨',loc:['ext'],exclusive:true,
    tiers:[
      {name:'Null Coating',      phys:'NONE',energy:'NONE',tech:'NONE',spirit:'LOW',    soak_bonus:1,spd_mod:0, dur_bonus:2, pwr:2,slots:2,price:5000,  dc:4,dur:4, rarity:'RARE',      legality:'LEGAL'},
      {name:'Warding Shell',     phys:'NONE',energy:'NONE',tech:'NONE',spirit:'MEDIUM', soak_bonus:3,spd_mod:-1,dur_bonus:5, pwr:3,slots:4,price:15000, dc:6,dur:6, rarity:'LIMITED',   legality:'RESTRICTED'},
      {name:'Parascience Shield',phys:'NONE',energy:'NONE',tech:'LOW', spirit:'EXTREME',soak_bonus:6,spd_mod:-2,dur_bonus:8, pwr:5,slots:6,price:50000, dc:8,dur:8, rarity:'CLASSIFIED',legality:'MILITARY'},
    ]},
  SHIELD_ENERGY:{name:'Energy Shield',icon:'💠',loc:['core','int'],
    tiers:[
      {name:'Flicker Shield',phys:'NONE',energy:'LOW',   tech:'NONE',spirit:'NONE',soak_bonus:0,dur_bonus:0,pwr:4,slots:3,price:5000, dc:4,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'20hp absorb before overload'},
      {name:'Full Barrier',  phys:'LOW', energy:'MEDIUM',tech:'NONE',spirit:'NONE',soak_bonus:0,dur_bonus:2,pwr:7,slots:4,price:15000,dc:5,dur:5, rarity:'RARE',    legality:'RESTRICTED',note:'50hp absorb, recharge 5/round'},
      {name:'Hardlight Wall',phys:'MEDIUM',energy:'HIGH',tech:'LOW', spirit:'NONE',soak_bonus:0,dur_bonus:4,pwr:12,slots:6,price:45000,dc:7,dur:6,rarity:'LIMITED', legality:'MILITARY',  note:'100hp absorb, recharge 10/round'},
    ]},
  REACTIVE_ARMOR:{name:'Reactive Armor',icon:'💥',loc:['ext'],
    tiers:[
      {name:'ERA Panels',   phys:'LOW',   energy:'NONE',tech:'NONE',spirit:'NONE',soak_bonus:2,spd_mod:0,dur_bonus:3,pwr:0,slots:2,price:3000, dc:3,dur:4, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Single-use blast absorption per panel'},
      {name:'NERA Array',   phys:'MEDIUM',energy:'LOW', tech:'NONE',spirit:'NONE',soak_bonus:4,spd_mod:-1,dur_bonus:5,pwr:1,slots:4,price:10000,dc:4,dur:5,rarity:'RARE',    legality:'MILITARY',  note:'Active counter-explosion system'},
      {name:'Trophy System',phys:'HIGH',  energy:'MEDIUM',tech:'NONE',spirit:'NONE',soak_bonus:6,spd_mod:-1,dur_bonus:8,pwr:3,slots:5,price:30000,dc:6,dur:6,rarity:'LIMITED',legality:'MILITARY',  note:'Intercepts incoming projectiles'},
    ]},
  // ── WEAPONS ───────────────────────────────────────────────────────────────
  WEAPON_MOUNT:{name:'Weapon Mount',icon:'🔫',loc:['ext','int'],
    tiers:[
      {name:'Lt. Energy Mount', weapon_type:'ENERGY', weapon_size:'Small', needs_ammo:false,pwr:3,slots:2,price:1500, dc:2,dur:5, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Lt. Kinetic Mount',weapon_type:'KINETIC',weapon_size:'Small', needs_ammo:true, pwr:1,slots:2,price:1200, dc:2,dur:6, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Md. Energy Mount', weapon_type:'ENERGY', weapon_size:'Medium',needs_ammo:false,pwr:5,slots:3,price:4000, dc:3,dur:5, rarity:'UNCOMMON',legality:'RESTRICTED'},
      {name:'Md. Kinetic Mount',weapon_type:'KINETIC',weapon_size:'Medium',needs_ammo:true, pwr:2,slots:3,price:3500, dc:3,dur:7, rarity:'UNCOMMON',legality:'RESTRICTED'},
      {name:'Hvy. Energy Mount',weapon_type:'ENERGY', weapon_size:'Large', needs_ammo:false,pwr:9,slots:5,price:12000,dc:5,dur:6, rarity:'RARE',    legality:'MILITARY'},
      {name:'Hvy. Kinetic Mount',weapon_type:'KINETIC',weapon_size:'Large',needs_ammo:true, pwr:3,slots:5,price:10000,dc:5,dur:8, rarity:'RARE',    legality:'MILITARY'},
      {name:'Auto-Turret',      weapon_type:'KINETIC',weapon_size:'Medium',needs_ammo:true, pwr:4,slots:5,price:20000,dc:6,dur:7, rarity:'LIMITED', legality:'MILITARY',auto_aim:true,note:'Dual-barrel auto-targeting'},
    ]},
  AMMO_STORAGE:{name:'Ammo Storage',icon:'📦',loc:['int','ext'],
    tiers:[
      {name:'Basic Mag',    ammo_cap:2, pwr:0,slots:1,price:300,  dc:1,dur:4, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Ammo Locker',  ammo_cap:5, pwr:0,slots:2,price:800,  dc:2,dur:5, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Hardened Mag', ammo_cap:5, pwr:0,slots:2,price:2000, dc:2,dur:8, rarity:'UNCOMMON',legality:'LEGAL',     note:'Blast-resistant'},
      {name:'Expanded Bay', ammo_cap:10,pwr:0,slots:3,price:2500, dc:3,dur:5, rarity:'UNCOMMON',legality:'RESTRICTED'},
      {name:'Reloader Sys.',ammo_cap:10,pwr:2,slots:3,price:8000, dc:4,dur:6, rarity:'RARE',    legality:'MILITARY',  note:'Auto-reloads between rounds'},
    ]},
  // ── COMBAT SUPPORT ────────────────────────────────────────────────────────
  TARGETING_COMP:{name:'Targeting Computer',icon:'🎯',loc:['core','int'],
    tiers:[
      {name:'Basic Targeting',  pwr:2,slots:2,price:2000, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',     note:'Marksman +1'},
      {name:'Predictive Track', pwr:3,slots:3,price:6000, dc:4,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'Marksman +2, Tactics +1'},
      {name:'Fire Control Sys.',pwr:5,slots:4,price:18000,dc:5,dur:5, rarity:'RARE',    legality:'RESTRICTED',note:'Marksman +3, multi-target lock'},
      {name:'Neural Targeting', pwr:7,slots:5,price:50000,dc:7,dur:6, rarity:'LIMITED', legality:'MILITARY',  note:'Marksman +4, Tactics +2, 360 awareness'},
    ]},
  ECM_SUITE:{name:'ECM Suite',icon:'📻',loc:['int','ext'],
    tiers:[
      {name:'Jammer Pod',  ecm:1,pwr:3,slots:2,price:3000, dc:3,dur:3, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Disrupts enemy comms and sensors'},
      {name:'Full ECM',    ecm:2,pwr:5,slots:3,price:9000, dc:5,dur:4, rarity:'RARE',    legality:'MILITARY',  note:'Jams radar, comms and guidance'},
      {name:'AESA Warfare',ecm:3,pwr:8,slots:4,price:28000,dc:7,dur:5, rarity:'LIMITED', legality:'MILITARY',  note:'Active and passive EM warfare suite'},
    ]},
  POINT_DEFENSE:{name:'Point Defense',icon:'🔰',loc:['ext'],
    tiers:[
      {name:'Flare System', pwr:1,slots:2,price:2000, dc:3,dur:3, rarity:'UNCOMMON',legality:'RESTRICTED',note:'3 uses, counters guided weapons'},
      {name:'CIWS Cannon',  pwr:4,slots:3,price:8000, dc:4,dur:5, rarity:'RARE',    legality:'MILITARY',  note:'Intercepts projectiles and missiles'},
      {name:'Laser Defense',pwr:6,slots:4,price:25000,dc:6,dur:5, rarity:'LIMITED', legality:'MILITARY',  note:'360 coverage, unlimited use'},
    ]},
  STEALTH_SYSTEM:{name:'Stealth System',icon:'👻',loc:['int','ext'],
    tiers:[
      {name:'Stealth Coat', pwr:1,slots:2,price:5000, dc:4,dur:2, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Others detect at -2 penalty'},
      {name:'Adaptive Camo',pwr:3,slots:3,price:15000,dc:5,dur:3, rarity:'RARE',    legality:'MILITARY',  note:'Others detect at -4 penalty'},
      {name:'Full Stealth', pwr:5,slots:5,price:45000,dc:7,dur:4, rarity:'LIMITED', legality:'CLASSIFIED',note:'Near-invisible, -6 detect penalty'},
    ]},
  // ── MANIPULATION ──────────────────────────────────────────────────────────
  ARM_GRIPPER:{name:'Gripper Arm',icon:'🦾',loc:['ext'],
    tiers:[
      {name:'Basic Gripper', arms:1,str:5, fine_motor:false,pwr:2,slots:2,price:2000, dc:2,dur:5, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Dual Grippers', arms:2,str:6, fine_motor:false,pwr:3,slots:3,price:5000, dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Heavy Clamp',   arms:1,str:14,fine_motor:false,pwr:4,slots:3,price:10000,dc:4,dur:7, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Industrial Arm',arms:2,str:18,fine_motor:false,pwr:6,slots:5,price:30000,dc:5,dur:8, rarity:'RARE',    legality:'RESTRICTED'},
    ]},
  ARM_PRECISION:{name:'Precision Arm',icon:'✋',loc:['ext'],
    tiers:[
      {name:'Surgeon Limb', arms:1,str:4,fine_motor:true,pwr:3,slots:2,price:4000, dc:3,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'Fine manipulation +2'},
      {name:'Micro-Tools',  arms:2,str:4,fine_motor:true,pwr:4,slots:3,price:10000,dc:4,dur:4, rarity:'RARE',    legality:'LEGAL',     note:'Fine manipulation +3, repair tools'},
      {name:'Nanotech Hand',arms:1,str:3,fine_motor:true,pwr:5,slots:4,price:30000,dc:6,dur:3, rarity:'LIMITED', legality:'RESTRICTED',note:'Sub-mm precision, hacking capable'},
    ]},
  ARM_HEAVY:{name:'Heavy Arm',icon:'💪',loc:['ext'],
    tiers:[
      {name:'Exo Strut',  arms:1,str:12,fine_motor:false,pwr:4,slots:3,price:6000, dc:3,dur:6, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Combat Arm', arms:2,str:16,fine_motor:false,pwr:6,slots:4,price:15000,dc:5,dur:8, rarity:'RARE',    legality:'RESTRICTED',dur_bonus:2},
      {name:'Siege Limbs',arms:2,str:24,fine_motor:false,pwr:9,slots:6,price:45000,dc:7,dur:10,rarity:'LIMITED', legality:'MILITARY',  dur_bonus:4},
    ]},
  // ── HACKING ───────────────────────────────────────────────────────────────
  HACK_TERMINAL:{name:'Hacking Terminal',icon:'💻',loc:['int','ext'],
    tiers:[
      {name:'Basic Interface',pwr:2,slots:2,price:2500, dc:3,dur:3, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Hacking +1, opens simple systems'},
      {name:'ICE Breaker',    pwr:3,slots:3,price:8000, dc:5,dur:4, rarity:'RARE',    legality:'ILLEGAL',  note:'Hacking +2, bypasses standard security'},
      {name:'Ghost Rig',      pwr:5,slots:4,price:25000,dc:7,dur:4, rarity:'LIMITED', legality:'ILLEGAL',  note:'Hacking +3, zero-trace infiltration'},
    ]},
  DATA_CORE:{name:'Data Core',icon:'💾',loc:['core','int'],
    tiers:[
      {name:'Storage Unit',  pwr:1,slots:1,price:1000, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',     note:'1TB local storage, data analysis'},
      {name:'Encrypted Core',pwr:2,slots:2,price:4000, dc:3,dur:4, rarity:'UNCOMMON',legality:'RESTRICTED',note:'10TB encrypted storage, AI sorting'},
      {name:'Quantum Vault', pwr:3,slots:3,price:15000,dc:5,dur:5, rarity:'RARE',    legality:'CLASSIFIED',note:'Unbreakable encryption, remote access'},
    ]},
  TECH_SCANNER:{name:'Tech Scanner',icon:'🔬',loc:['int','ext'],
    tiers:[
      {name:'Device Scanner', pwr:1,slots:1,price:1500, dc:2,dur:2, rarity:'COMMON',  legality:'LEGAL',     note:'Identifies technology and serial numbers'},
      {name:'Diagnostic Rig', pwr:2,slots:2,price:5000, dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL',     note:'Technology +1, full device analysis'},
      {name:'Engineering Eye',pwr:3,slots:3,price:15000,dc:5,dur:4, rarity:'RARE',    legality:'RESTRICTED',note:'Engineering +1, blueprint reconstruction'},
    ]},
  // ── COMMS ─────────────────────────────────────────────────────────────────
  COMM_ARRAY:{name:'Comms Array',icon:'📻',loc:['core','int','ext'],
    tiers:[
      {name:'Short Range',   comm_range:'500m',    ecm:0,pwr:1,slots:1,price:500,   dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Long Range',    comm_range:'50km',    ecm:0,pwr:2,slots:2,price:2000,  dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL'},
      {name:'Encrypted Link',comm_range:'50km',    ecm:1,pwr:3,slots:2,price:6000,  dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL'},
      {name:'Quantum Comm',  comm_range:'Unlimited',ecm:2,pwr:5,slots:3,price:25000,dc:5,dur:4, rarity:'RARE',    legality:'RESTRICTED'},
    ]},
  COMM_JAMMER:{name:'Comms Jammer',icon:'📵',loc:['int','ext'],
    tiers:[
      {name:'Noise Generator',ecm:1,pwr:2,slots:2,price:2000, dc:3,dur:3, rarity:'UNCOMMON',legality:'ILLEGAL',   note:'Disrupts comms in 30m radius'},
      {name:'Spectrum Jammer',ecm:2,pwr:4,slots:3,price:6000, dc:5,dur:3, rarity:'RARE',    legality:'ILLEGAL',   note:'Disrupts all frequencies, 100m'},
      {name:'Blackout System',ecm:3,pwr:7,slots:4,price:20000,dc:7,dur:4, rarity:'LIMITED', legality:'CLASSIFIED',note:'Total comms blackout, 500m radius'},
    ]},
  COMM_RELAY:{name:'Comms Relay',icon:'🔁',loc:['ext'],
    tiers:[
      {name:'Signal Booster',pwr:1,slots:1,price:800,  dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL',     note:'Extends friendly comm range x2'},
      {name:'Relay Node',    pwr:2,slots:2,price:3000, dc:2,dur:3, rarity:'UNCOMMON',legality:'LEGAL',     note:'Acts as comm relay hub for team'},
      {name:'Network Core',  pwr:3,slots:3,price:10000,dc:3,dur:4, rarity:'RARE',    legality:'RESTRICTED',note:'Tactical network for 20 units'},
    ]},
  BROADCAST_UNIT:{name:'Broadcast Unit',icon:'📢',loc:['ext'],
    tiers:[
      {name:'Speaker Array', pwr:1,slots:1,price:600,  dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL',     note:'Loudspeaker and voice modulation'},
      {name:'Psych Array',   pwr:3,slots:3,price:8000, dc:4,dur:3, rarity:'RARE',    legality:'RESTRICTED',note:'Crowd-control frequencies, disorientation'},
      {name:'Holo-Projector',pwr:4,slots:3,price:15000,dc:5,dur:4, rarity:'LIMITED', legality:'RESTRICTED',note:'Holographic display for deception'},
    ]},
  // ── MEDICAL ───────────────────────────────────────────────────────────────
  MED_SYSTEM:{name:'Medical System',icon:'💊',loc:['core','int'],
    tiers:[
      {name:'First Aid Unit',pwr:1,slots:2,price:2000, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',     note:'Medicine +1, field stabilisation'},
      {name:'Medic Bay',     pwr:3,slots:3,price:8000, dc:4,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'Medicine +2, surgery capable'},
      {name:'Nano Medic',    pwr:5,slots:4,price:25000,dc:6,dur:5, rarity:'RARE',    legality:'RESTRICTED',note:'Medicine +3, nanite healing'},
    ]},
  TRAUMA_BAY:{name:'Trauma Bay',icon:'🏥',loc:['int'],
    tiers:[
      {name:'Stabiliser Pod', pwr:2,slots:2,price:4000, dc:3,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'Keeps 1 critical patient stable'},
      {name:'Surgery Station',pwr:4,slots:4,price:15000,dc:5,dur:5, rarity:'RARE',    legality:'LEGAL',     note:'Full surgical suite, 1 patient'},
      {name:'Cryo-Med',       pwr:6,slots:5,price:40000,dc:6,dur:6, rarity:'LIMITED', legality:'RESTRICTED',note:'Cryogenic preservation and revival'},
    ]},
  // ── ENGINEERING ───────────────────────────────────────────────────────────
  REPAIR_ARM:{name:'Repair Arm',icon:'🔧',loc:['ext'],
    tiers:[
      {name:'Tool Arm',    pwr:2,slots:2,price:2000, dc:2,dur:4, rarity:'COMMON',  legality:'LEGAL',note:'Repair +1, basic mechanical repair'},
      {name:'Welder Arm',  pwr:3,slots:3,price:5000, dc:3,dur:5, rarity:'UNCOMMON',legality:'LEGAL',note:'Repair +2, structural and electronic'},
      {name:'Nano-Repair', pwr:5,slots:4,price:18000,dc:5,dur:5, rarity:'RARE',    legality:'LEGAL',note:'Repair +3, repairs 1D per round'},
    ]},
  FABRICATOR:{name:'Fabricator',icon:'⚙',loc:['int'],
    tiers:[
      {name:'Print Unit',    pwr:3,slots:3,price:5000, dc:4,dur:4, rarity:'UNCOMMON',legality:'LEGAL',     note:'Craft +1, prints small items from material'},
      {name:'Micro-Factory', pwr:5,slots:5,price:20000,dc:6,dur:5, rarity:'RARE',    legality:'RESTRICTED',note:'Craft +2, prints components and parts'},
      {name:'Mol. Assembler',pwr:8,slots:6,price:60000,dc:8,dur:6, rarity:'LIMITED', legality:'CLASSIFIED',note:'Craft +3, molecular-level fabrication'},
    ]},
  NANITE_SYS:{name:'Nanite System',icon:'🦠',loc:['core','int'],
    tiers:[
      {name:'Repair Nanites',pwr:3,slots:2,price:6000, dc:4,dur:3, rarity:'RARE',      legality:'RESTRICTED',note:'Self-repairs 1 dur/hr, Engineering +1'},
      {name:'Combat Nanites',pwr:4,slots:3,price:15000,dc:6,dur:4, rarity:'LIMITED',   legality:'MILITARY',  note:'Self-repairs 2 dur/round, can infect enemies'},
      {name:'Swarm Network', pwr:6,slots:4,price:40000,dc:8,dur:5, rarity:'CLASSIFIED',legality:'ILLEGAL',   note:'Autonomous repair and scout nanite swarm'},
    ]},
  // ── UTILITY ───────────────────────────────────────────────────────────────
  STORAGE_BAY:{name:'Storage Bay',icon:'📦',loc:['int','ext'],
    tiers:[
      {name:'Small Hold',  pwr:0,slots:2,price:800,  dc:1,dur:4, rarity:'COMMON',  legality:'LEGAL',note:'5-item cargo capacity'},
      {name:'Cargo Bay',   pwr:0,slots:3,price:2000, dc:2,dur:5, rarity:'COMMON',  legality:'LEGAL',note:'20-item cargo capacity'},
      {name:'Secure Vault',pwr:1,slots:3,price:6000, dc:3,dur:7, rarity:'UNCOMMON',legality:'LEGAL',note:'10-item secure locked storage'},
      {name:'Cold Storage',pwr:2,slots:4,price:10000,dc:3,dur:5, rarity:'UNCOMMON',legality:'RESTRICTED',note:'Bio-safe cold storage, 20 items'},
    ]},
  SURVEY_KIT:{name:'Survey Kit',icon:'🗺',loc:['int','ext'],
    tiers:[
      {name:'Mapping Unit',   pwr:2,slots:2,price:2000, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',note:'Navigation +1, terrain mapping'},
      {name:'Geo-Scanner',    pwr:3,slots:3,price:6000, dc:3,dur:3, rarity:'UNCOMMON',legality:'LEGAL',note:'Science +1, mineral and structural analysis'},
      {name:'Full Survey Rig',pwr:4,slots:4,price:15000,dc:5,dur:4, rarity:'RARE',    legality:'LEGAL',note:'Navigation +2, Science +1, full environmental survey'},
    ]},
  RECORDER_SYS:{name:'Recorder System',icon:'🎥',loc:['int','ext'],
    tiers:[
      {name:'Cam Unit',      pwr:1,slots:1,price:500,  dc:1,dur:2, rarity:'COMMON',  legality:'LEGAL',    note:'360 degree video and audio recording'},
      {name:'Witness Array', pwr:2,slots:2,price:2000, dc:2,dur:3, rarity:'UNCOMMON',legality:'LEGAL',    note:'Tamper-proof evidence recording'},
      {name:'Covert Rec.',   pwr:2,slots:2,price:8000, dc:4,dur:2, rarity:'RARE',    legality:'ILLEGAL',  note:'Undetectable surveillance recording'},
    ]},
  RESCUE_KIT:{name:'Rescue Kit',icon:'🆘',loc:['int','ext'],
    tiers:[
      {name:'Basic Rescue',pwr:1,slots:2,price:1500, dc:2,dur:4, rarity:'COMMON',  legality:'LEGAL',    note:'Survival +1, extraction tools, emergency beacon'},
      {name:'SAR Package', pwr:2,slots:3,price:5000, dc:3,dur:4, rarity:'UNCOMMON',legality:'LEGAL',    note:'Survival +2, stretcher, fire suppression, flares'},
      {name:'CSAR System', pwr:3,slots:4,price:15000,dc:4,dur:5, rarity:'RARE',    legality:'RESTRICTED',note:'Survival +3, combat extraction, breaching tools'},
    ]},
  EXPLOSIVE_UNIT:{name:'Explosive Unit',icon:'💣',loc:['ext'],
    tiers:[
      {name:'Demo Charge',pwr:0,slots:1,price:1000, dc:2,dur:2, rarity:'UNCOMMON',legality:'ILLEGAL',   note:'Single-use demolition charge'},
      {name:'Mine Layer',  pwr:1,slots:2,price:4000, dc:3,dur:3, rarity:'RARE',    legality:'ILLEGAL',   note:'Deploys 3 proximity mines'},
      {name:'Grenade Rack',pwr:1,slots:2,price:5000, dc:3,dur:3, rarity:'RARE',    legality:'ILLEGAL',   note:'Launches 5 grenades'},
      {name:'MIRV System', pwr:2,slots:4,price:25000,dc:7,dur:4, rarity:'LIMITED', legality:'CLASSIFIED',note:'Multiple independently targeted warheads'},
    ]},
  ENV_SYSTEM:{name:'Environment System',icon:'🌬',loc:['int'],
    tiers:[
      {name:'Temp Control',  pwr:2,slots:2,price:2000, dc:2,dur:3, rarity:'COMMON',  legality:'LEGAL',note:'Operates in -50 to +150C'},
      {name:'Radiation Shld',pwr:2,slots:2,price:4000, dc:3,dur:4, rarity:'UNCOMMON',legality:'LEGAL',note:'Radiation and vacuum rated'},
      {name:'Extreme Env.',  pwr:3,slots:3,price:12000,dc:4,dur:5, rarity:'RARE',    legality:'LEGAL',note:'Rated for extreme environments, corrosive, high pressure'},
    ]},
  // ── AI ────────────────────────────────────────────────────────────────────
  SKILL_MODULE:{name:'Skill Module',icon:'🧠',loc:['core','int'],exclusive:true,
    tiers:[
      {name:'Basic AI',   skills_n:1,rank:3,pwr:3, slots:2,price:3000,  dc:3,dur:3, sys_bonus:1, rarity:'UNCOMMON',  legality:'LEGAL'},
      {name:'Standard AI',skills_n:3,rank:4,pwr:5, slots:3,price:9000,  dc:5,dur:4, sys_bonus:2, rarity:'RARE',      legality:'LEGAL'},
      {name:'Advanced AI',skills_n:5,rank:6,pwr:8, slots:4,price:25000, dc:6,dur:5, sys_bonus:3, rarity:'LIMITED',   legality:'RESTRICTED'},
      {name:'Tactical AI',skills_n:8,rank:7,pwr:12,slots:5,price:70000, dc:8,dur:6, sys_bonus:4, rarity:'CLASSIFIED',legality:'MILITARY'},
    ]},
};

// Drone builder state — survives re-renders (module-level)

function parseSk(s){if(!s||s==='0')return{d:0,f:0};const m=String(s).match(/^(\d*)D([+-]\d+)?$/i);if(m)return{d:parseInt(m[1]||1),f:parseInt(m[2]||0)};return{d:0,f:parseInt(s)||0};}
function fmtSk(d,f){if(!d&&!f)return'0';if(!d)return String(f);if(!f)return d+'D';return d+'D'+(f>0?'+':'')+f;}

function calcDrone(){
  if(!dbState.size||!dbState.mob) return null;
  const sz=DB_SIZES[dbState.size];
  const mob=DB_MOB[dbState.mob];
  const defRk=DB_DEF_RANKS;
  const maxDef=(a,b)=>defRk[Math.max(defRk.indexOf(a||'NONE'),defRk.indexOf(b||'NONE'))];
  const sk0=parseSk(sz.soak);
  const r={
    dur:sz.dur, sys:sz.sys, soak_d:sk0.d, soak_f:sk0.f,
    phys:'NONE', energy:'NONE', tech:'NONE', spirit:'NONE',
    prim_spd:mob.base_spd+sz.spd_mod, prim_mode:mob.base_mode,
    alt_mode:mob.alt_mode, alt_spd:mob.alt_spd,
    extra_modes:[],
    pwr_avail:0, pwr_used:0,
    slots_used:0, slots_max:sz.slots,
    awareness:0, sensor_range:null,
    comms:null, ecm:0, ammo_cap:0,
    skills:[], mounts:[], arms:null,
    dc:Math.max(sz.dc, mob.dc),
    cost:sz.price+mob.price,
    warns:[],
  };
  const all=[
    ...dbState.core.map(c=>({...c,loc:'core'})),
    ...dbState.internal.map(c=>({...c,loc:'int'})),
    ...dbState.external.map(c=>({...c,loc:'ext'})),
  ];
  let spd_pen=0;
  for(const comp of all){
    const def=DB_COMP[comp.type];
    if(!def) continue;
    const t=def.tiers[comp.tier];
    if(!t) continue;
    const zkey=comp.loc==='int'?'internal':comp.loc;
    const zone=DB_ZONE[zkey]||{dc_mod:0,cost_mod:1};
    r.cost+=Math.round((t.price||0)*zone.cost_mod);
    r.dc=Math.max(r.dc,(t.dc||0)+zone.dc_mod);
    r.slots_used+=t.slots||0;
    r.pwr_used+=t.pwr||0;
    r.pwr_avail+=t.pwr_give||0;
    if(t.dur_bonus) r.dur+=t.dur_bonus;
    if(t.sys_bonus) r.sys+=t.sys_bonus;
    r.phys=maxDef(r.phys,t.phys);
    r.energy=maxDef(r.energy,t.energy);
    r.tech=maxDef(r.tech,t.tech);
    r.spirit=maxDef(r.spirit,t.spirit);
    if(t.soak_bonus) r.soak_f+=t.soak_bonus;
    if(t.spd_mod) spd_pen+=t.spd_mod;
    if(t.awareness!=null&&t.awareness>r.awareness){r.awareness=t.awareness;r.sensor_range=t.range;}
    if(t.comm_range) r.comms=t.comm_range;
    if(t.ecm) r.ecm+=t.ecm;
    if(t.ammo_cap) r.ammo_cap+=t.ammo_cap;
    if(comp.type==='SKILL_MODULE'&&comp.skills) r.skills.push(...comp.skills.map(s=>s+' '+t.rank));
    if(comp.type==='WEAPON_MOUNT'){
      r.mounts.push({name:t.name,weapon_type:t.weapon_type,weapon_size:t.weapon_size,needs_ammo:t.needs_ammo,auto_aim:t.auto_aim,weapon:comp.weapon||null,zone:comp.loc});
    }
    if((comp.type==='ARM_GRIPPER'||comp.type==='ARM_PRECISION'||comp.type==='ARM_HEAVY')&&(!r.arms||t.str>r.arms.str)){
      r.arms={n:t.arms,str:t.str,fine:t.fine_motor};
    }
    if(t.mode) r.extra_modes.push(t.mode+' '+t.speed+'m/r'+(t.note?' ('+t.note+')':''));
  }
  if(mob.base_mode) r.prim_spd=Math.max(0,r.prim_spd+spd_pen);
  if(dbState.mob==='STATIC') r.prim_spd=0;
  if(dbState.atmo&&dbState.mob==='FLY'){r.dc++;r.cost+=15000;}
  r.soak=fmtSk(r.soak_d,r.soak_f);
  const hasPower=all.some(c=>c.type==='POWER_CELL'||c.type==='SOLAR_PANEL'||c.type==='ENERGY_BANK');
  if(!hasPower) r.warns.push('No power source — drone cannot function');
  if(r.pwr_used>r.pwr_avail) r.warns.push('Power deficit: '+(r.pwr_used-r.pwr_avail)+' over capacity');
  if(r.slots_used>r.slots_max) r.warns.push('Slot overload: '+r.slots_used+'/'+r.slots_max+' slots used');
  const kMounts=r.mounts.filter(m=>m.needs_ammo);
  if(kMounts.length&&!r.ammo_cap) r.warns.push('Kinetic weapon mounts require Ammo Storage');
  return r;
}

function dbTierDesc(type,t){
  const p=[];
  if(t.pwr_give) p.push('⚡ +'+t.pwr_give+' pwr generated');
  if(t.pwr) p.push('⚡ '+t.pwr+' pwr draw');
  p.push('📦 '+t.slots+' slot'+(t.slots>1?'s':''));
  p.push('💰 '+fmt(t.price)+' Cr');
  p.push('DC '+(t.dc||0));
  if(t.dur) p.push('🩹 Dur '+t.dur);
  const defs=[];
  if(t.phys&&t.phys!=='NONE') defs.push('PHYS:'+t.phys);
  if(t.energy&&t.energy!=='NONE') defs.push('NRGY:'+t.energy);
  if(t.tech&&t.tech!=='NONE') defs.push('TECH:'+t.tech);
  if(t.spirit&&t.spirit!=='NONE') defs.push('SPRT:'+t.spirit);
  if(defs.length) p.push('🛡 '+defs.join(' '));
  if(t.soak_bonus) p.push('Soak +'+t.soak_bonus);
  if(t.dur_bonus) p.push('Durability +'+t.dur_bonus);
  if(t.spd_mod) p.push('Speed '+t.spd_mod+'m/r');
  if(t.awareness) p.push('👁 Awareness +'+t.awareness+' Range '+t.range);
  if(t.weapon_type) p.push('🔫 '+t.weapon_type+' '+t.weapon_size+(t.needs_ammo?' (needs ammo)':'')+(t.auto_aim?' auto-aim':''));
  if(t.ammo_cap) p.push('Ammo x'+t.ammo_cap);
  if(t.arms) p.push('🦾 '+t.arms+' arm'+(t.arms>1?'s':'')+' STR '+t.str+(t.fine_motor?' (fine motor)':''));
  if(t.comm_range) p.push('📻 '+t.comm_range+(t.ecm?' ECM +'+t.ecm:''));
  if(t.ecm&&!t.comm_range) p.push('📡 ECM +'+t.ecm);
  if(t.skills_n) p.push('🧠 '+t.skills_n+' skill'+(t.skills_n>1?'s':'')+' rank '+t.rank+' Sys +'+t.sys_bonus);
  if(t.mode) p.push(t.mode+' '+t.speed+'m/r');
  if(t.rarity) p.push(t.rarity);
  if(t.legality) p.push(t.legality);
  if(t.note&&!t.mode) p.push(t.note);
  if(t.size_limit) p.push('⚠ '+t.size_limit.join('/')+' only');
  return p.join('  ·  ');
}

function renderDbZone(loc,stats){
  const zkey=loc==='int'?'internal':loc;
  const zone=DB_ZONE[zkey];
  const locKey=loc==='core'?'core':loc==='int'?'internal':'external';
  const comps=dbState[locKey];
  let h='<div class="db-zone">';
  h+='<div class="db-zone-hd">';
  h+='<span class="db-zone-title" style="color:'+zone.color+'">'+zone.label+'</span>';
  h+='<span class="db-zone-mod">'+zone.info+'</span>';
  h+='</div>';
  if(comps.length===0) h+='<div style="font-size:10px;color:var(--mu);font-style:italic;margin-bottom:6px;padding:2px 0;">Empty</div>';
  comps.forEach((comp,i)=>{
    const def=DB_COMP[comp.type];
    if(!def) return;
    const t=def.tiers[comp.tier];
    if(!t) return;
    h+='<div class="db-comp-row">';
    h+='<span class="db-comp-name">'+def.icon+' '+def.name+'</span>';
    h+='<span class="db-comp-tier">'+esc(t.name)+'</span>';
    if(comp.type==='SKILL_MODULE'&&comp.skills&&comp.skills.length){
      h+='<span class="db-comp-meta" style="color:var(--a3);max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="'+esc(comp.skills.join(', '))+'">'+esc(comp.skills.slice(0,2).join(', '))+(comp.skills.length>2?' +':'')+'</span>';
    } else if(comp.type==='WEAPON_MOUNT'&&comp.weapon){
      h+='<span class="db-comp-meta" style="color:var(--a2);" title="'+esc(comp.weapon)+'">'+esc(comp.weapon.length>12?comp.weapon.substring(0,12)+'..':comp.weapon)+'</span>';
    } else {
      h+='<span class="db-comp-meta">'+t.slots+'U '+t.pwr+'P</span>';
    }
    h+='<button class="db-rm" data-db="rm:'+loc+':'+i+'" title="Remove">✕</button>';
    h+='</div>';
    if(comp.type==='WEAPON_MOUNT'){
      const wPick=dbState.wpnPicker&&dbState.wpnPicker.zone===loc&&dbState.wpnPicker.idx===i;
      if(wPick){
        h+=renderWpnPicker(comp,t,loc,i);
      } else {
        h+='<div style="padding:2px 0 4px 20px;">';
        h+='<button class="db-chip" style="font-size:9px;" data-db="wpnpick:'+loc+':'+i+'">'+(comp.weapon?'✏ '+esc(comp.weapon.length>16?comp.weapon.substring(0,16)+'..':comp.weapon):'🔫 Select Weapon')+'</button>';
        h+='</div>';
      }
    }
  });
  if(dbAdd.loc===loc){
    h+=renderDbAddPanel(loc);
  } else {
    h+='<button class="db-add-btn" data-db="open:'+loc+'">+ Add Component</button>';
  }
  h+='</div>';
  return h;
}

function renderWpnPicker(comp,t,loc,idx){
  const wtype=t.weapon_type;
  const isEnergy=w=>{const tp=((w.type||w.dmg_type||w.damage||'').toUpperCase());return tp.includes('ENERGY')||tp.includes('LASER')||tp.includes('PLASMA');};
  const wpns=(g.weapons||[]).filter(w=>wtype==='ENERGY'?isEnergy(w):!isEnergy(w));
  const q=(dbAdd.wpnSearch||'').toLowerCase();
  const filtered=q?wpns.filter(w=>(w.name||'').toLowerCase().includes(q)||(w.category||'').toLowerCase().includes(q)):wpns;
  const zkey=loc==='int'?'internal':loc;
  let h='<div class="db-wpn-picker">';
  h+='<div style="font-size:9px;color:'+(DB_ZONE[zkey]||{color:'#fff'}).color+';font-family:Orbitron,sans-serif;margin-bottom:4px;">'+wtype+' WEAPONS — SELECT</div>';
  h+='<input type="text" class="db-wpn-search" placeholder="Search..." value="'+esc(dbAdd.wpnSearch||'')+'" data-db="wpnsearch" style="width:100%;box-sizing:border-box;margin-bottom:4px;">';
  h+='<div class="db-wpn-list">';
  if(filtered.length===0){
    h+='<div style="font-size:9px;color:var(--mu);font-style:italic;">No matching weapons</div>';
  }
  filtered.slice(0,24).forEach(w=>{
    const sel=comp.weapon===w.name;
    h+='<button class="db-skill-chip'+(sel?' sel':'')+'" style="font-size:9px;" data-db="wpnsel" data-wpn="'+esc(w.name)+'">'+esc(w.name)+(w.damage?' ['+esc(w.damage)+']':'')+'</button>';
  });
  if(filtered.length>24) h+='<div style="font-size:9px;color:var(--mu);margin-top:2px;">+'+( filtered.length-24)+' more — refine search</div>';
  h+='</div>';
  h+='<div style="margin-top:4px;display:flex;gap:6px;">';
  if(comp.weapon) h+='<button class="db-confirm" style="font-size:9px;" data-db="wpndone">✓ Done</button>';
  h+='<button class="db-cancel" style="font-size:9px;" data-db="wpnclose">✗ Close</button>';
  h+='</div>';
  h+='</div>';
  return h;
}

function renderDbAddPanel(loc){
  const isExclusive=k=>DB_COMP[k].exclusive&&[...dbState.core,...dbState.internal,...dbState.external].some(c=>c.type===k);
  const availTypes=Object.entries(DB_COMP).filter(([k,d])=>d.loc.includes(loc)&&!isExclusive(k));
  let h='<div class="db-add-panel">';
  h+='<div class="db-add-row">';
  h+='<span class="db-add-lbl">COMPONENT TYPE</span>';
  availTypes.forEach(([k,d])=>{
    h+='<button class="db-chip'+(dbAdd.type===k?' sel':'')+'" data-db="atype:'+k+'">'+d.icon+' '+d.name+'</button>';
  });
  h+='</div>';
  if(dbAdd.type){
    const def=DB_COMP[dbAdd.type];
    const sz=dbState.size;
    h+='<div class="db-add-row">';
    h+='<span class="db-add-lbl">TIER</span>';
    def.tiers.forEach((t,i)=>{
      const sizeOk=!t.size_limit||t.size_limit.includes(sz);
      if(!sizeOk) return;
      h+='<button class="db-chip'+(dbAdd.tier===i?' sel':'')+'" data-db="atier:'+i+'">'+esc(t.name)+'</button>';
    });
    h+='</div>';
    const t=def.tiers[dbAdd.tier];
    h+='<div class="db-tier-desc">'+dbTierDesc(dbAdd.type,t)+'</div>';
    if(dbAdd.type==='SKILL_MODULE'){
      const maxSk=t.skills_n;
      const selCount=dbAdd.skills.length;
      h+='<div style="font-size:9px;color:var(--a3);margin-bottom:4px;font-family:Orbitron,sans-serif;letter-spacing:.06em;">SELECT SKILLS ('+selCount+' / '+maxSk+')</div>';
      h+='<div class="db-skill-grid">';
      Object.entries(DB_SKILLS).forEach(([cat,skills])=>{
        h+='<div class="db-skill-cat">'+cat+'</div>';
        skills.forEach(sk=>{
          const sel=dbAdd.skills.includes(sk);
          const maxed=!sel&&selCount>=maxSk;
          h+='<button class="db-skill-chip'+(sel?' sel':maxed?' maxed':'')+'" data-db="askill:'+sk+'" '+(maxed?'disabled':'')+'>'+esc(sk)+'</button>';
        });
      });
      h+='</div>';
    }
    const canConfirm=dbAdd.type&&(dbAdd.type!=='SKILL_MODULE'||dbAdd.skills.length===t.skills_n);
    h+='<div class="db-add-row-btns">';
    h+='<button class="db-confirm" data-db="confirm" '+(canConfirm?'':'disabled style="opacity:.4;cursor:not-allowed;"')+'>✓ Add</button>';
    h+='<button class="db-cancel" data-db="close">✗ Cancel</button>';
    if(dbAdd.type==='SKILL_MODULE'&&dbAdd.skills.length!==t.skills_n) h+='<span style="font-size:9px;color:var(--a2);margin-left:4px;">Select exactly '+t.skills_n+' skill'+(t.skills_n>1?'s':'')+'</span>';
    h+='</div>';
  }
  h+='</div>';
  return h;
}

function renderDbStats(st){
  const defCol={NONE:'var(--mu)',LOW:'#4ade80',MEDIUM:'#34d399',HIGH:'#facc15',EXTREME:'#f87171'};
  const pct=st.pwr_avail?Math.min(100,Math.round(st.pwr_used/st.pwr_avail*100)):0;
  const pwrColor=pct>95?'#f87171':pct>80?'#fb923c':'#34d399';
  let h='<div class="db-stats-panel">';
  h+='<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:8px;">';
  h+='<div><input id="db-name-inp" class="db-name-inp" value="'+esc(dbState.name)+'" placeholder="Drone name..." maxlength="40"><div class="db-ssub">'+esc(DB_SIZES[dbState.size].name)+' · '+esc(DB_MOB[dbState.mob].name)+(dbState.atmo?' · Atmospheric':'')+'</div></div>';
  h+='<button class="db-reset-btn" data-db="reset">↺ Reset</button>';
  h+='</div>';
  const speedStr=st.prim_mode?st.prim_mode+' '+st.prim_spd+'m/r':'Stationary';
  h+='<div class="db-stat-grid">';
  h+='<div class="db-stat-box"><div class="db-stat-lbl">DURABILITY</div><div class="db-stat-val">'+st.dur+'</div></div>';
  h+='<div class="db-stat-box"><div class="db-stat-lbl">SYSTEM</div><div class="db-stat-val">'+st.sys+'</div></div>';
  h+='<div class="db-stat-box"><div class="db-stat-lbl">SOAK</div><div class="db-stat-val">'+esc(st.soak)+'</div></div>';
  h+='<div class="db-stat-box"><div class="db-stat-lbl">SPEED</div><div class="db-stat-val ok">'+speedStr+'</div></div>';
  if(st.alt_mode) h+='<div class="db-stat-box"><div class="db-stat-lbl">'+st.alt_mode.toUpperCase()+'</div><div class="db-stat-val ok">'+st.alt_spd+'m/r</div></div>';
  st.extra_modes.forEach(m=>{const[md,...rest]=m.split(' ');h+='<div class="db-stat-box"><div class="db-stat-lbl">'+esc(md.toUpperCase())+'</div><div class="db-stat-val ok">'+esc(rest.join(' '))+'</div></div>';});
  h+='</div>';
  h+='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:8px;">';
  ['phys','energy','tech','spirit'].forEach(k=>{
    const v=st[k]||'NONE';
    const lbl={phys:'PHYS',energy:'ENERGY',tech:'TECH',spirit:'SPIRIT'}[k];
    h+='<div class="db-stat-box"><div class="db-stat-lbl">'+lbl+'</div><div class="db-stat-val" style="color:'+(defCol[v]||'var(--mu)')+';font-size:10px;">'+v+'</div></div>';
  });
  h+='</div>';
  h+='<div class="db-pwr-wrap">';
  h+='<div class="db-pwr-lbl"><span>⚡ POWER</span><span style="color:'+pwrColor+';">'+st.pwr_used+' / '+st.pwr_avail+' pwr</span></div>';
  h+='<div class="db-pwr-bar"><div class="db-pwr-fill" style="width:'+pct+'%;background:'+pwrColor+';"></div></div>';
  h+='</div>';
  const slotPct=st.slots_max?st.slots_used/st.slots_max:0;
  const slotCol=slotPct>1?'var(--re)':slotPct>0.8?'var(--a2)':'var(--mu)';
  h+='<div style="margin-bottom:8px;"><span style="font-size:10px;font-family:ShareTechMono,monospace;color:'+slotCol+';">📦 Slots '+st.slots_used+' / '+st.slots_max+'</span></div>';
  h+='<hr class="db-divider">';
  if(st.skills.length){h+='<div class="db-info" style="color:#a78bfa;">🧠 '+esc(st.skills.join(' · '))+'</div>';}
  if(st.awareness){h+='<div class="db-info">📡 Awareness +'+st.awareness+(st.sensor_range?' · Range '+st.sensor_range:'')+'</div>';}
  if(st.comms){h+='<div class="db-info">📻 Comms: '+esc(st.comms)+(st.ecm?' · ECM +'+st.ecm:'')+'</div>';}
  else if(st.ecm){h+='<div class="db-info">📡 ECM +'+st.ecm+'</div>';}
  if(st.arms){h+='<div class="db-info">🦾 '+st.arms.n+' arm'+(st.arms.n>1?'s':'')+' STR '+st.arms.str+(st.arms.fine?' (fine motor)':'')+'</div>';}
  if(st.ammo_cap){h+='<div class="db-info">📦 Ammo storage: x'+st.ammo_cap+'</div>';}
  if(st.mounts.length){
    h+='<hr class="db-divider">';
    h+='<div style="font-size:9px;color:var(--a);font-family:Orbitron,sans-serif;letter-spacing:.06em;margin-bottom:4px;">🔫 ARMAMENT</div>';
    st.mounts.forEach(m=>{
      h+='<div class="db-info">';
      h+='<span style="color:var(--mu);">'+esc(m.name)+'</span>';
      h+=' <span class="tag '+(m.weapon_type==='ENERGY'?'tp':'to')+'" style="font-size:8px;">'+m.weapon_type+(m.needs_ammo?' +AMMO':'')+'</span>';
      if(m.auto_aim) h+=' <span class="tag tg" style="font-size:8px;">AUTO</span>';
      if(m.weapon) h+=' → <span style="color:var(--a2);">'+esc(m.weapon)+'</span>';
      else h+=' <span style="color:var(--mu);font-style:italic;">no weapon selected</span>';
      h+='</div>';
    });
  }
  if(st.warns.length){
    h+='<hr class="db-divider">';
    st.warns.forEach(w=>{h+='<div class="db-warn">⚠ '+esc(w)+'</div>';});
  } else {
    h+='<hr class="db-divider">';
    h+='<div class="db-ok">✓ Build valid</div>';
  }
  h+='<div class="db-footer">';
  h+='<span class="db-cost-val">'+fmt(st.cost)+' Cr</span>';
  h+='<span class="db-dc-badge">Craft DC '+st.dc+'</span>';
  h+='</div>';
  h+='</div>';
  return h;
}

// Build drone_parts catalog (all component tiers as flat entries)
function buildDroneParts(){
  const out=[];
  Object.entries(DB_COMP).forEach(([type,def])=>{
    def.tiers.forEach((t,ti)=>{
      out.push({id:type+'_'+ti,type,cat_name:def.name,icon:def.icon,tier_name:t.name,loc:def.loc,exclusive:!!def.exclusive,...t});
    });
  });
  return out;
}
g.catalog.drone_parts=buildDroneParts();"""

c = c[:start_idx] + NEW_DRONE_JS + c[end_idx:]
print("Drone builder JS section replaced. File length:", len(c))


# ─── 7. Replace the drone_parts render section ───────────────────────────────
OLD_DRONE_PARTS = """  else if(cs==='drone_parts'){
    // ── Drone Parts Catalog ─────────────────────────────────────────────────
    const all=g.catalog&&g.catalog.drone_parts||[];
    html+='<div class="fbar"><button class="fc'+(af===''?' active':'')+'" data-cat="ALL">All</button>';
    Object.entries(DB_COMP).forEach(([k,d])=>{if(all.some(p=>p.type===k))html+='<button class="fc'+(af===k?' active':'')+'" data-cat="'+k+'">'+d.icon+' '+d.name+'</button>';});
    html+='</div><div class="grid">';
    all.forEach((p,i)=>{
      if(!ms([p.cat_name,p.tier_name,p.note||'',p.loc.join(' ')])) return;
      if(af&&af!==p.type) return;
      cnt++;
      const cid='dp'+i;
      const locColors={core:'#00c8ff',int:'#a855f7',ext:'#ff6b35'};
      html+='<div class="card" id="'+cid+'" data-tog="'+cid+'">';
      html+='<div class="ch">'+p.icon+' '+hl(p.cat_name,sq)+' <span class="xi">▼</span></div>';
      html+='<div class="cr2">';
      html+='<span class="wpn-pill" style="color:#a78bfa;">'+hl(p.tier_name,sq)+'</span>';
      p.loc.forEach(l=>{html+='<span class="wpn-pill" style="color:'+locColors[l]+';font-size:9px;">'+l.toUpperCase()+'</span>';});
      if(p.unique) html+='<span class="wpn-pill" style="color:var(--ye);font-size:9px;">UNIQUE</span>';
      html+='</div>';
      html+='<div class="cr3"><div class="cr3l">';
      html+='<span class="wpn-pill">📦 '+p.slots+' slots</span>';
      if(p.pwr_give) html+='<span class="wpn-pill" style="color:#facc15;">⚡ +'+p.pwr_give+' pwr</span>';
      if(p.pwr) html+='<span class="wpn-pill" style="color:var(--a2);">⚡ '+p.pwr+' draw</span>';
      html+='<span class="wpn-pill" style="color:var(--a);">DC '+p.dc+'</span>';
      html+='</div><div class="cr3r" style="color:#34d399;font-family:ShareTechMono,monospace;font-size:11px;">'+fmt(p.price)+' Cr</div></div>';
      html+='<div class="cb">';
      if(p.defense) html+='<div class="fg"><div class="f"><div class="fl">Defense</div><div class="fv">'+p.defense+'</div></div><div class="f"><div class="fl">Soak</div><div class="fv">+'+p.soak+'</div></div>'+(p.spd_mod?'<div class="f"><div class="fl">Speed</div><div class="fv">'+p.spd_mod+'m/r</div></div>':'')+(p.dur_bonus?'<div class="f"><div class="fl">Durability</div><div class="fv">+'+p.dur_bonus+'</div></div>':'')+'</div>';
      if(p.awareness) html+='<div class="fg"><div class="f"><div class="fl">Awareness</div><div class="fv">+'+p.awareness+'</div></div><div class="f"><div class="fl">Range</div><div class="fv">'+p.range+'</div></div></div>';
      if(p.weapon_sz) html+='<div class="fg"><div class="f"><div class="fl">Weapon Size</div><div class="fv">'+p.weapon_sz+'</div></div><div class="f"><div class="fl">Mounts</div><div class="fv">'+p.weapon_n+(p.auto_aim?' (auto-aim)':'')+'</div></div></div>';
      if(p.arms) html+='<div class="fg"><div class="f"><div class="fl">Arms</div><div class="fv">'+p.arms+'</div></div><div class="f"><div class="fl">STR</div><div class="fv">'+p.str+(p.fine_motor?' (fine motor)':'')+'</div></div></div>';
      if(p.comm_range) html+='<div class="fg"><div class="f"><div class="fl">Comms Range</div><div class="fv">'+p.comm_range+'</div></div>'+(p.ecm?'<div class="f"><div class="fl">ECM</div><div class="fv">+'+p.ecm+'</div></div>':'')+'</div>';
      if(p.skills_n) html+='<div class="fg"><div class="f"><div class="fl">Skills</div><div class="fv">'+p.skills_n+'</div></div><div class="f"><div class="fl">Rank</div><div class="fv">'+p.rank+'</div></div><div class="f"><div class="fl">System Bonus</div><div class="fv">+'+p.sys_bonus+'</div></div></div>';
      if(p.mode) html+='<div class="fg"><div class="f"><div class="fl">Drive Mode</div><div class="fv">'+p.mode+'</div></div><div class="f"><div class="fl">Speed</div><div class="fv">'+p.speed+'m/r</div></div></div>';
      if(p.swim_spd) html+='<div class="fg"><div class="f"><div class="fl">Swim Speed</div><div class="fv">'+p.swim_spd+'m/r</div></div></div>';
      if(p.note) html+='<div class="desc" style="margin-top:6px;">'+esc(p.note)+'</div>';
      if(p.size_limit) html+='<div style="font-size:9px;color:var(--a2);margin-top:4px;">⚠ '+p.size_limit.join(' / ')+' chassis only</div>';
      html+='</div></div>';
    });
    html+='</div>';
  }"""

NEW_DRONE_PARTS = r"""  else if(cs==='drone_parts'){
    // ── Drone Parts Catalog ─────────────────────────────────────────────────
    const all=g.catalog&&g.catalog.drone_parts||[];
    const rarCol={COMMON:'var(--fg)',UNCOMMON:'#4ade80',RARE:'#60a5fa',LIMITED:'#a78bfa',UNIQUE:'#fbbf24',CLASSIFIED:'#f87171'};
    const legCol={LEGAL:'#4ade80',RESTRICTED:'#facc15',MILITARY:'#f87171',ILLEGAL:'#ef4444'};
    const defCol={NONE:'var(--mu)',LOW:'#4ade80',MEDIUM:'#34d399',HIGH:'#facc15',EXTREME:'#f87171'};
    const locColors={core:'#00c8ff',int:'#a855f7',ext:'#ff6b35'};
    const filtered=all.filter(p=>{
      if(!ms([p.cat_name,p.tier_name,p.note||'',p.loc.join(' '),p.rarity||'',p.legality||''])) return false;
      if(af&&af!==p.type) return false;
      return true;
    });
    cnt=filtered.length;
    html='<div class="stitle">🔧 DRONE PARTS <span class="badge">'+cnt+'</span></div>';
    html+='<div class="fbar"><button class="fc'+(af===''?' active':'')+'" data-cat="">All</button>';
    Object.entries(DB_COMP).forEach(([k,d])=>{if(all.some(p=>p.type===k))html+='<button class="fc'+(af===k?' active':'')+'" data-cat="'+k+'">'+d.icon+' '+d.name+'</button>';});
    html+='</div><div class="grid">';
    filtered.forEach((p,i)=>{
      const cid='dp'+i;
      html+='<div class="card '+rarCls(p.rarity)+'" id="'+cid+'" data-tog="'+cid+'">';
      html+='<div class="ch"><div><div class="cn">'+p.icon+' '+hl(p.cat_name,sq)+'</div>';
      html+='<div class="cs">'+hl(p.tier_name,sq)+'</div></div><span class="xi">▼</span></div>';
      html+='<div class="cr2">';
      p.loc.forEach(l=>{html+='<span class="wpn-pill" style="color:'+locColors[l]+';font-size:9px;">'+l.toUpperCase()+'</span>';});
      if(p.rarity) html+='<span class="wpn-pill" style="color:'+(rarCol[p.rarity]||'#fff')+';font-size:9px;">'+p.rarity+'</span>';
      if(p.legality) html+='<span class="wpn-pill" style="color:'+(legCol[p.legality]||'#fff')+';font-size:9px;">'+p.legality+'</span>';
      if(p.exclusive) html+='<span class="wpn-pill" style="color:var(--ye);font-size:9px;">EXCL</span>';
      if(p.weapon_type) html+='<span class="wpn-pill" style="color:'+(p.weapon_type==='ENERGY'?'#a78bfa':'#fb923c')+';font-size:9px;">'+p.weapon_type+'</span>';
      html+='</div>';
      html+='<div class="cr3"><div class="cr3l">';
      html+='<span class="wpn-pill">📦 '+p.slots+' slots</span>';
      if(p.pwr_give) html+='<span class="wpn-pill" style="color:#facc15;">⚡ +'+p.pwr_give+'</span>';
      if(p.pwr) html+='<span class="wpn-pill" style="color:var(--a2);">⚡ '+p.pwr+' draw</span>';
      html+='<span class="wpn-pill" style="color:var(--a);">DC '+(p.dc||0)+'</span>';
      if(p.dur) html+='<span class="wpn-pill">🩹 '+p.dur+' dur</span>';
      html+='</div><div class="cr3r" style="color:#34d399;font-family:ShareTechMono,monospace;font-size:11px;">'+fmt(p.price)+' Cr</div></div>';
      html+='<div class="cb">';
      const defs=[['PHYS',p.phys],['ENERGY',p.energy],['TECH',p.tech],['SPIRIT',p.spirit]].filter(([,v])=>v&&v!=='NONE');
      if(defs.length){
        html+='<div class="fg">';
        defs.forEach(([k,v])=>{html+='<div class="f"><div class="fl">'+k+' Def</div><div class="fv" style="color:'+(defCol[v]||'#fff')+';">'+v+'</div></div>';});
        if(p.soak_bonus) html+='<div class="f"><div class="fl">Soak Bonus</div><div class="fv">+'+p.soak_bonus+'</div></div>';
        if(p.spd_mod) html+='<div class="f"><div class="fl">Speed Mod</div><div class="fv">'+p.spd_mod+'m/r</div></div>';
        if(p.dur_bonus) html+='<div class="f"><div class="fl">Durability</div><div class="fv">+'+p.dur_bonus+'</div></div>';
        html+='</div>';
      }
      if(p.awareness) html+='<div class="fg"><div class="f"><div class="fl">Awareness</div><div class="fv">+'+p.awareness+'</div></div><div class="f"><div class="fl">Range</div><div class="fv">'+p.range+'</div></div></div>';
      if(p.weapon_type) html+='<div class="fg"><div class="f"><div class="fl">Mount Type</div><div class="fv">'+p.weapon_type+'</div></div><div class="f"><div class="fl">Size</div><div class="fv">'+p.weapon_size+(p.needs_ammo?' (ammo req.)':'')+'</div></div>'+(p.auto_aim?'<div class="f"><div class="fl">Auto-Aim</div><div class="fv">Yes</div></div>':'')+'</div>';
      if(p.ammo_cap) html+='<div class="fg"><div class="f"><div class="fl">Ammo Cap.</div><div class="fv">x'+p.ammo_cap+'</div></div></div>';
      if(p.arms) html+='<div class="fg"><div class="f"><div class="fl">Arms</div><div class="fv">'+p.arms+'</div></div><div class="f"><div class="fl">STR</div><div class="fv">'+p.str+(p.fine_motor?' (fine)':'')+'</div></div></div>';
      if(p.comm_range) html+='<div class="fg"><div class="f"><div class="fl">Comms</div><div class="fv">'+p.comm_range+'</div></div>'+(p.ecm?'<div class="f"><div class="fl">ECM</div><div class="fv">+'+p.ecm+'</div></div>':'')+'</div>';
      if(p.ecm&&!p.comm_range) html+='<div class="fg"><div class="f"><div class="fl">ECM</div><div class="fv">+'+p.ecm+'</div></div></div>';
      if(p.skills_n) html+='<div class="fg"><div class="f"><div class="fl">Skills</div><div class="fv">'+p.skills_n+'</div></div><div class="f"><div class="fl">Rank</div><div class="fv">'+p.rank+'</div></div><div class="f"><div class="fl">Sys Bonus</div><div class="fv">+'+p.sys_bonus+'</div></div></div>';
      if(p.mode) html+='<div class="fg"><div class="f"><div class="fl">Drive Mode</div><div class="fv">'+p.mode+'</div></div><div class="f"><div class="fl">Speed</div><div class="fv">'+p.speed+'m/r</div></div></div>';
      if(p.note) html+='<div class="desc" style="margin-top:6px;">'+esc(p.note)+'</div>';
      if(p.size_limit) html+='<div style="font-size:9px;color:var(--a2);margin-top:4px;">⚠ '+p.size_limit.join(' / ')+' chassis only</div>';
      html+='</div></div>';
    });
    html+='</div>';
  }"""

assert OLD_DRONE_PARTS in c, "drone_parts section not found!"
c = c.replace(OLD_DRONE_PARTS, NEW_DRONE_PARTS, 1)
print("drone_parts render section replaced")


# ─── 8. Replace the drone_builder render section ─────────────────────────────
OLD_DRONE_BUILDER = """  else if(cs==='drone_builder'){
    // ── Drone Builder ───────────────────────────────────────────────────────
    cnt=1; // suppress empty-search message
    // Setup bar
    html+='<div class="db-setup">';
    html+='<div class="db-step"><span class="db-step-lbl">CHASSIS SIZE</span>';
    Object.entries(DB_SIZES).forEach(([k,v])=>{
      html+='<button class="db-chip'+(dbState.size===k?' sel':'')+'" data-db="size:'+k+'">'+v.name+'</button>';
    });
    html+='</div>';
    html+='<div class="db-step"><span class="db-step-lbl">MOBILITY</span>';
    Object.entries(DB_MOB).forEach(([k,v])=>{
      html+='<button class="db-chip'+(dbState.mob===k?' sel':'')+'" data-db="mob:'+k+'">'+v.name+'</button>';
    });
    if(dbState.mob==='FLY') html+='<button class="db-chip'+(dbState.atmo?' sel-o':'')+'" data-db="atmo">✈ Atmospheric</button>';
    html+='</div>';
    if(dbState.size&&dbState.mob){
      html+='<div style="font-size:10px;color:var(--mu);margin-top:4px;">Chassis: '+fmt(DB_SIZES[dbState.size].price)+' Cr · Mobility: '+fmt(DB_MOB[dbState.mob].price)+' Cr · Base DC '+Math.max(DB_SIZES[dbState.size].dc,DB_MOB[dbState.mob].dc)+'</div>';
    }
    html+='</div>'; // db-setup
    if(!dbState.size||!dbState.mob){
      html+='<div class="db-empty"><div class="db-empty-icon">🤖</div><div class="db-empty-msg">Select a chassis size and mobility type to begin</div></div>';
    } else {
      const st=calcDrone();
      html+='<div class="db-zones">';
      html+=renderDbZone('core','⬡ CORE','#00c8ff',st);
      html+=renderDbZone('int','◈ INTERNAL','#a855f7',st);
      html+=renderDbZone('ext','◇ EXTERNAL','#ff6b35',st);
      html+='</div>';
      html+=renderDbStats(st);
    }
  }"""

NEW_DRONE_BUILDER = r"""  else if(cs==='drone_builder'){
    // ── Drone Builder ───────────────────────────────────────────────────────
    cnt=1; // suppress empty-search message
    html='<div class="stitle">🤖 DRONE BUILDER</div>';
    html+='<div class="db-setup">';
    html+='<div class="db-step"><span class="db-step-lbl">CHASSIS SIZE</span>';
    Object.entries(DB_SIZES).forEach(([k,v])=>{
      html+='<button class="db-chip'+(dbState.size===k?' sel':'')+'" data-db="size:'+k+'">'+v.name+'<span style="font-size:8px;color:var(--mu);display:block;">'+v.slots+' slots</span></button>';
    });
    html+='</div>';
    html+='<div class="db-step"><span class="db-step-lbl">MOBILITY</span>';
    Object.entries(DB_MOB).forEach(([k,v])=>{
      html+='<button class="db-chip'+(dbState.mob===k?' sel':'')+'" data-db="mob:'+k+'">'+v.name+'</button>';
    });
    if(dbState.mob==='FLY') html+='<button class="db-chip'+(dbState.atmo?' sel-o':'')+'" data-db="atmo">✈ Atmospheric</button>';
    html+='</div>';
    if(dbState.size&&dbState.mob){
      const sz=DB_SIZES[dbState.size];const mob=DB_MOB[dbState.mob];
      html+='<div style="font-size:10px;color:var(--mu);margin-top:4px;">Chassis '+fmt(sz.price)+' Cr · Mobility '+fmt(mob.price)+' Cr · Base DC '+Math.max(sz.dc,mob.dc)+' · '+sz.slots+' total slots</div>';
    }
    html+='</div>';
    if(!dbState.size||!dbState.mob){
      html+='<div class="db-empty"><div class="db-empty-icon">🤖</div><div class="db-empty-msg">Select a chassis size and mobility type to begin</div></div>';
    } else {
      const st=calcDrone();
      html+='<div class="db-zones">';
      html+=renderDbZone('core',st);
      html+=renderDbZone('int',st);
      html+=renderDbZone('ext',st);
      html+='</div>';
      html+=renderDbStats(st);
    }
  }"""

assert OLD_DRONE_BUILDER in c, "drone_builder section not found!"
c = c.replace(OLD_DRONE_BUILDER, NEW_DRONE_BUILDER, 1)
print("drone_builder render section replaced")

# ─── 9. Write the result ─────────────────────────────────────────────────────
with open('/home/user/56/56th_century_compendium_v8.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done! File written.")
import os
print("Final file size:", os.path.getsize('/home/user/56/56th_century_compendium_v8.html'), "bytes")
