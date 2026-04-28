// 56th Century — Action/Soak API Script
// Handles: !armor-roll, !talent, !evo, !datacom, !program, !gadget, !backpack, !spell

// ── helpers ──────────────────────────────────────────────────────────────────

function getAttr(charId, attrName, fallback) {
    var found = findObjs({ _type: "attribute", _characterid: charId, name: attrName });
    if (found && found.length > 0) {
        var v = found[0].get("current");
        return (v !== undefined && v !== null && v !== "") ? String(v) : (fallback || "—");
    }
    return fallback || "—";
}

function getChar(msg) {
    if (!msg.selected || msg.selected.length === 0) return null;
    var token = getObj("graphic", msg.selected[0]._id);
    if (!token) return null;
    var charId = token.get("represents");
    if (!charId) return null;
    return getObj("character", charId);
}

function row(label, value) {
    return "<tr><td style='color:#aaa;padding:2px 6px;white-space:nowrap;'>" + label + "</td>"
         + "<td style='padding:2px 6px;'>" + value + "</td></tr>";
}

function section(title) {
    return "<tr><td colspan='2' style='color:#4fc3f7;font-weight:bold;padding:4px 6px 2px;border-top:1px solid #333;'>"
         + title + "</td></tr>";
}

function card(title, subtitle, tableRows, footerHtml) {
    var html = "<div style='background:#111;border:1px solid #359fcf;padding:8px;font-size:12px;color:#eee;font-family:sans-serif;'>";
    html += "<div style='font-size:15px;font-weight:bold;color:#4fc3f7;margin-bottom:3px;'>" + title + "</div>";
    if (subtitle) html += "<div style='color:#aaa;font-size:11px;margin-bottom:5px;'>" + subtitle + "</div>";
    if (tableRows) {
        html += "<table style='width:100%;border-collapse:collapse;'>" + tableRows + "</table>";
    }
    if (footerHtml) html += "<div style='margin-top:6px;'>" + footerHtml + "</div>";
    html += "</div>";
    return html;
}

function defBadge(tier) {
    var colors = { "None": "#555", "Low": "#4caf50", "Medium": "#8bc34a", "High": "#ffc107", "Extreme": "#f44336" };
    var c = colors[tier] || "#555";
    return "<span style='background:" + c + ";color:#fff;padding:1px 5px;border-radius:3px;font-size:10px;'>" + tier + "</span>";
}

// ── !armor-roll N ─────────────────────────────────────────────────────────────

function cmdArmorRoll(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 3) {
        sendChat("System", "/w " + msg.who + " Usage: !armor-roll <1-3>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "armor" + n + "_";

    var name     = getAttr(cid, p + "name");
    var defPhys  = getAttr(cid, p + "def_phys",   "None");
    var defEnergy= getAttr(cid, p + "def_energy",  "None");
    var defTech  = getAttr(cid, p + "def_tech",    "None");
    var defSpirit= getAttr(cid, p + "def_spirit",  "None");
    var defDmg   = getAttr(cid, p + "def_dmg");
    var soak     = getAttr(cid, p + "soak");
    var soakBonus= getAttr(cid, p + "soak_bonus");
    var special  = getAttr(cid, p + "special");
    var notes    = getAttr(cid, p + "notes");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Armor slot " + n + " is empty."); return; }

    var rows = "";
    rows += section("DEFENSE");
    rows += row("Physical",  defBadge(defPhys));
    rows += row("Energy",    defBadge(defEnergy));
    rows += row("Tech",      defBadge(defTech));
    rows += row("Spirit",    defBadge(defSpirit));
    if (defDmg && defDmg !== "—") rows += row("Def Dmg", defDmg);
    rows += section("SOAK");
    rows += row("Soak Dice", soak + (soakBonus && soakBonus !== "—" ? " +" + soakBonus : ""));
    if (special && special !== "—") { rows += section("SPECIAL"); rows += row("", special); }
    if (notes && notes !== "—")    { rows += section("NOTES");   rows += row("", notes); }

    sendChat(char.get("name"), card("🛡 " + name, "Armor Slot " + n, rows, null));
}

// ── !talent N ─────────────────────────────────────────────────────────────────

function cmdTalent(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 10) {
        sendChat("System", "/w " + msg.who + " Usage: !talent <1-10>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "talent" + n + "_";

    var name     = getAttr(cid, p + "name");
    var skill    = getAttr(cid, p + "skill");
    var category = getAttr(cid, p + "category");
    var xpCost   = getAttr(cid, p + "xp_cost");
    var effect   = getAttr(cid, p + "effect");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Talent slot " + n + " is empty."); return; }

    var subtitle = [];
    if (skill && skill !== "—")    subtitle.push("Skill: " + skill);
    if (category && category !== "—") subtitle.push(category);
    if (xpCost && xpCost !== "—") subtitle.push("XP: " + xpCost);

    var rows = "";
    if (effect && effect !== "—") {
        rows += section("EFFECT");
        rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + effect + "</td></tr>";
    }

    sendChat(char.get("name"), card("⚡ " + name, subtitle.join(" · "), rows, null));
}

// ── !evo N ────────────────────────────────────────────────────────────────────

function cmdEvo(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 5) {
        sendChat("System", "/w " + msg.who + " Usage: !evo <1-5>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "evo" + n + "_";

    var name   = getAttr(cid, p + "name");
    var type   = getAttr(cid, p + "type");
    var tier   = getAttr(cid, p + "tier");
    var effect = getAttr(cid, p + "effect");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Evolution slot " + n + " is empty."); return; }

    var subtitle = [];
    if (type && type !== "—") subtitle.push(type);
    if (tier && tier !== "—") subtitle.push("Tier: " + tier);

    var rows = "";
    if (effect && effect !== "—") {
        rows += section("EFFECT");
        rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + effect + "</td></tr>";
    }

    sendChat(char.get("name"), card("🧬 " + name, subtitle.join(" · "), rows, null));
}

// ── !datacom N ────────────────────────────────────────────────────────────────

function cmdDatacom(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 3) {
        sendChat("System", "/w " + msg.who + " Usage: !datacom <1-3>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "datacom" + n + "_";

    var name      = getAttr(cid, p + "name");
    var cpu       = getAttr(cid, p + "cpu");
    var mem       = getAttr(cid, p + "mem");
    var nanite    = getAttr(cid, p + "nanite");
    var defPhys   = getAttr(cid, p + "def_phys",   "None");
    var defEnergy = getAttr(cid, p + "def_energy",  "None");
    var defTech   = getAttr(cid, p + "def_tech",    "None");
    var defSpirit = getAttr(cid, p + "def_spirit",  "None");
    var defDmg    = getAttr(cid, p + "def_dmg");
    var intExt    = getAttr(cid, p + "int_ext");
    var intInt    = getAttr(cid, p + "int_int");
    var intMain   = getAttr(cid, p + "int_main");
    var expertise = getAttr(cid, p + "expertise");
    var special   = getAttr(cid, p + "special");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Datacom slot " + n + " is empty."); return; }

    var rows = "";
    rows += section("RESOURCES");
    rows += row("CPU / Memory / Nanite", cpu + " / " + mem + " / " + nanite);
    if (expertise && expertise !== "—") rows += row("Expertise Bonus", "+" + expertise);
    rows += section("DEFENSE");
    rows += row("Physical",  defBadge(defPhys));
    rows += row("Energy",    defBadge(defEnergy));
    rows += row("Tech",      defBadge(defTech));
    rows += row("Spirit",    defBadge(defSpirit));
    if (defDmg && defDmg !== "—") rows += row("Def Dmg", defDmg);
    rows += section("INTERFACE DC");
    rows += row("External / Internal / Main", intExt + " / " + intInt + " / " + intMain);
    if (special && special !== "—") { rows += section("SPECIAL"); rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + special + "</td></tr>"; }

    sendChat(char.get("name"), card("📡 " + name, "Datacom Slot " + n, rows, null));
}

// ── !program N ────────────────────────────────────────────────────────────────

function cmdProgram(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 10) {
        sendChat("System", "/w " + msg.who + " Usage: !program <1-10>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "program" + n + "_";

    var name    = getAttr(cid, p + "name");
    var type    = getAttr(cid, p + "type");
    var cpu     = getAttr(cid, p + "cpu");
    var mem     = getAttr(cid, p + "mem");
    var passive = getAttr(cid, p + "passive");
    var active  = getAttr(cid, p + "active");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Program slot " + n + " is empty."); return; }

    var subtitle = [];
    if (type && type !== "—") subtitle.push(type);
    if (cpu && cpu !== "—")   subtitle.push("CPU: " + cpu);
    if (mem && mem !== "—")   subtitle.push("Mem: " + mem);

    var rows = "";
    if (passive && passive !== "—") {
        rows += section("PASSIVE");
        rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + passive + "</td></tr>";
    }
    if (active && active !== "—") {
        rows += section("ACTIVE");
        rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + active + "</td></tr>";
    }

    sendChat(char.get("name"), card("💻 " + name, subtitle.join(" · "), rows, null));
}

// ── !gadget N ─────────────────────────────────────────────────────────────────

function cmdGadget(msg, args) {
    var n = parseInt(args[1], 10);
    if (isNaN(n) || n < 1 || n > 5) {
        sendChat("System", "/w " + msg.who + " Usage: !gadget <1-5>");
        return;
    }
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;
    var p = "gadget" + n + "_";

    var name   = getAttr(cid, p + "name");
    var nanite = getAttr(cid, p + "nanite");
    var effect = getAttr(cid, p + "effect");

    if (name === "—" || name === "") { sendChat("System", "/w " + msg.who + " Gadget slot " + n + " is empty."); return; }

    var subtitle = (nanite && nanite !== "—") ? "Nanite Cost: " + nanite : "";

    var rows = "";
    if (effect && effect !== "—") {
        rows += section("EFFECT");
        rows += "<tr><td colspan='2' style='padding:3px 6px;'>" + effect + "</td></tr>";
    }

    sendChat(char.get("name"), card("🔧 " + name, subtitle, rows, null));
}

// ── !backpack N ───────────────────────────────────────────────────────────────

function cmdBackpack(msg, args) {
    var loadout = parseInt(args[1], 10) || 1;
    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;

    var maxLoad = getAttr(cid, "charloadmax");
    var offset = (loadout === 2) ? 20 : 0;
    var rows = "";
    rows += section("ITEMS (Loadout " + loadout + ")");

    var hasItems = false;
    for (var i = 1; i <= 20; i++) {
        var idx = i + offset;
        var itemName = getAttr(cid, "item" + idx + "_name");
        var itemSize = getAttr(cid, "item" + idx + "_size");
        var itemQty  = getAttr(cid, "item" + idx + "_qty");
        if (itemName && itemName !== "—" && itemName !== "") {
            var sizeLabel = { "0": "—", "0.25": "Tiny", "1": "Small", "2": "Medium", "3": "Large" }[itemSize] || itemSize;
            rows += row(itemName, sizeLabel + (itemQty && itemQty !== "—" ? " × " + itemQty : ""));
            hasItems = true;
        }
    }

    if (!hasItems) rows += "<tr><td colspan='2' style='padding:3px 6px;color:#666;'>No items.</td></tr>";
    if (maxLoad && maxLoad !== "—") rows += section("CAPACITY");
    if (maxLoad && maxLoad !== "—") rows += row("Max Load", maxLoad);

    sendChat(char.get("name"), card("🎒 Loadout " + loadout, char.get("name"), rows, null));
}

// ── !spell name tier expertise ────────────────────────────────────────────────

function cmdSpell(msg, args) {
    var spellName = args[1];
    var tier      = parseInt(args[2], 10) || 1;
    var expertise = parseInt(args[3], 10) || 0;

    if (!spellName) {
        sendChat("System", "/w " + msg.who + " Usage: !spell <SpellName> <tier> <expertise>");
        return;
    }

    var char = getChar(msg);
    if (!char) { sendChat("System", "/w " + msg.who + " Select a token first."); return; }
    var cid = char.id;

    // Find the spell slot matching the name
    var foundSlot = null;
    var foundDomain = "—";
    for (var i = 1; i <= 16; i++) {
        var sn = getAttr(cid, "spell" + i + "_name");
        if (sn && sn.toLowerCase() === spellName.toLowerCase()) {
            foundSlot = i;
            foundDomain = getAttr(cid, "spell" + i + "_domain");
            break;
        }
    }

    // Get CHI pool
    var chi = getAttr(cid, "CHI");

    var subtitle = [];
    if (foundDomain && foundDomain !== "—") subtitle.push("Domain: " + foundDomain);
    subtitle.push("Tier: " + tier);
    if (expertise > 0) subtitle.push("Expertise: +" + expertise);

    var rows = "";
    rows += section("CAST");
    rows += row("CHI Cost", tier);
    rows += row("CHI Remaining", chi);
    rows += row("Expertise Bonus", expertise > 0 ? "+" + expertise : "None");

    var footer = "<span style='color:#aaa;font-size:11px;'>Resolve effect per compendium — Tier " + tier + " spell.</span>";

    sendChat(char.get("name"), card("✨ " + spellName, subtitle.join(" · "), rows, footer));
}

// ── main dispatcher ───────────────────────────────────────────────────────────

on("chat:message", function(msg) {
    if (msg.type !== "api") return;

    var args = msg.content.trim().split(/\s+/);
    var cmd  = args[0];

    if      (cmd === "!armor-roll") cmdArmorRoll(msg, args);
    else if (cmd === "!talent")     cmdTalent(msg, args);
    else if (cmd === "!evo")        cmdEvo(msg, args);
    else if (cmd === "!datacom")    cmdDatacom(msg, args);
    else if (cmd === "!program")    cmdProgram(msg, args);
    else if (cmd === "!gadget")     cmdGadget(msg, args);
    else if (cmd === "!backpack")   cmdBackpack(msg, args);
    else if (cmd === "!spell")      cmdSpell(msg, args);
});
