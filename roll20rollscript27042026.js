function formatDiceList(dice, successFn) {
    return dice.map((d, i) => {
        let isSuccess = successFn(d.value);
        let cssClass = isSuccess ? "sheet-die-success" : "sheet-die-fail";

        // Luck die (first die)
        if (i === 0) {
            return `<span class="sheet-die-luck">${d.value}</span>`;
        }

        return `<span class="${cssClass}">${d.value}</span>`;
    }).join(" ");
}
on("chat:message", function(msg) {
    if (msg.type !== "api") return;

    let args = msg.content.trim().split(/\s+/);
    if (args[0] !== "!roll") return;

    let skillName = args[1];          // e.g. "Might"
    let attributeName = args[2];      // e.g. "Physical"
    
    if (!skillName || !attributeName) {
        sendChat("System", "/w " + msg.who + " Usage: !roll <Skill> <Attribute>");
        return;
    }

    if (!msg.selected || msg.selected.length === 0) {
        sendChat("System", "/w " + msg.who + " You must select a token.");
        return;
    }

    let token = getObj("graphic", msg.selected[0]._id);
    let character = getObj("character", token.get("represents"));
    if (!character) {
        sendChat("System", "/w " + msg.who + " Token is not linked to a character.");
        return;
    }

    function getAttr(name, fallback = 0) {
        let obj = findObjs({
            type: "attribute",
            characterid: character.id,
            name: name
        })[0];
        if (!obj) return fallback;
        let v = parseInt(obj.get("current"), 10);
        return isNaN(v) ? fallback : v;
    }

    // Pull EXACT attribute names from sheet
    let skillValue = getAttr(skillName, 0);
    let bonusValue = getAttr(skillName + "_bonus", 0);
    let attributeValue = getAttr(attributeName, 0);

    if (skillValue <= 0) {
        sendChat("System", "/w " + msg.who + " Skill " + skillName + " is 0 or missing.");
        return;
    }

    // Roll N d10
    let dice = [];
    for (let i = 0; i < skillValue; i++) {
        dice.push({
            index: i + 1,
            value: randomInteger(10),
            isLuck: i === 0,
            rerolled: false,
            oldValue: null
        });
    }

    function isSuccess(v) { return v >= 5; }

    let initialSuccesses = dice.filter(d => isSuccess(d.value)).length;

        // Reroll logic (properly capped)
    let rerollDetails = [];

    // How many rerolls allowed by attribute
    let maxRerolls = Math.abs(attributeValue);

    if (attributeValue !== 0 && maxRerolls > 0) {

        // Collect candidates:
        // - attribute > 0 → reroll failures
        // - attribute < 0 → reroll successes
        let candidates = dice.filter(d => {
            if (attributeValue > 0) {
                return !isSuccess(d.value); // failures
            } else {
                return isSuccess(d.value);  // successes
            }
        });

        // Cap rerolls by:
        // 1. attribute value
        // 2. number of candidates
        // 3. number of dice rolled (skill value)
        let allowed = Math.min(maxRerolls, candidates.length, dice.length);

        // Reroll only the first N candidates
        candidates.slice(0, allowed).forEach(d => {
            d.oldValue = d.value;
            d.value = randomInteger(10);
            d.rerolled = true;
            rerollDetails.push(`Die #${d.index}: ${d.oldValue} → ${d.value}`);
        });
    }
    let finalSuccesses = dice.filter(d => isSuccess(d.value)).length;
    let totalSuccesses = finalSuccesses + bonusValue;

let initialLine = formatDiceList(
    dice.map(d => ({
        value: d.oldValue !== null ? d.oldValue : d.value
    })),
    isSuccess
);

let finalLine = formatDiceList(dice, isSuccess);


    let rerollLine = rerollDetails.length ? rerollDetails.join(" | ") : "None";

let content =
    "&{template:skillroll}" +
    ` {{name=${character.get("name")}}}` +
    ` {{skill=${skillName}}}` +
    ` {{skill_level=${skillValue}}}` +
    ` {{attribute=${attributeName} (${attributeValue})}}` +
    ` {{initial_dice=${initialLine}}}` +
    ` {{initial_successes=${initialSuccesses}}}` +
    ` {{rerolls=${rerollLine}}}` +
    ` {{finaldice=${finalLine}}}` +
    ` {{final_successes=${finalSuccesses}}}` +
    ` {{bonus_successes=${bonusValue}}}` +
    ` {{total_successes=${totalSuccesses}}}`;

    sendChat(character.get("name"), content);
});
// ============================================================
//  WEAPON ATTACK SYSTEM
//  - Recoil display
//  - Crit / Fumble via Luck Die (die #1)
//  - Color-coded + icon output
//  - Max / Min damage on special outcomes
//  - Bonus parsing fixed
//  - Single / Burst / Auto
// ============================================================

on("chat:message", function(msg) {
    if (msg.type !== "api") return;

    // Extract arguments safely
    let args = msg.content.match(/(?:[^\s"]+|"[^"]*")+/g);
    if (!args || args[0] !== "!attack") return;

    // Strip quotes
    args = args.map(a => a.replace(/(^")|("$)/g, ""));

    // ------------------------------------------------------------
    //  Skill → Attribute Mapping
    // ------------------------------------------------------------
    const skillToAttribute = {
        "Athletics":"PHYSICAL","Might":"PHYSICAL","Martial_Arts":"PHYSICAL","Heavy_Weapons":"PHYSICAL",
        "Piloting":"PHYSICAL","Repair":"PHYSICAL","Resilience":"PHYSICAL","Scavenging":"PHYSICAL","Survival":"PHYSICAL",

        "Academics":"MENTAL","Cyberintel":"MENTAL","Engineering":"MENTAL","Galactic_Knowledge":"MENTAL",
        "Hacking":"MENTAL","Medicine":"MENTAL","Navigation":"MENTAL","Parascience":"MENTAL","Science":"MENTAL","Technology":"MENTAL",

        "Acting":"SOCIAL","Charm":"SOCIAL","Etiquette":"SOCIAL","Flair":"SOCIAL","Intimidation":"SOCIAL",
        "Leadership":"SOCIAL","Negotiation":"SOCIAL","Spiritual":"SOCIAL","Streetwise":"SOCIAL","Subterfuge":"SOCIAL",

        "Awareness":"ACUITY","Binding":"ACUITY","Concealment":"ACUITY","Dexterity":"ACUITY","Gunslinger":"ACUITY",
        "Intuition":"ACUITY","Marksman":"ACUITY","Operator":"ACUITY","Search":"ACUITY","Speed":"ACUITY",
        "Tactics":"ACUITY","Wits":"ACUITY"
    };

    // ------------------------------------------------------------
    //  FIND SKILL NAME IN ARGUMENT LIST
    // ------------------------------------------------------------
    let skillIndex = args.findIndex(a => skillToAttribute[a]);

    if (skillIndex === -1) {
        sendChat("System", "/w " + msg.who + " ERROR: Skill not found in arguments.");
        return;
    }

    // Weapon name = everything between args[1] and skillIndex-1
    let weaponName = args.slice(1, skillIndex).join(" ");

    // Now extract remaining arguments
    let skillName     = args[skillIndex];
    let dmgExpression = args[skillIndex + 1] || "";
    let powerLevel    = args[skillIndex + 2] || "";
    let maxExpertise  = parseInt(args[skillIndex + 3] || "0", 10);
    let dmgTarget     = args[skillIndex + 4] || "";
    let defenseDC     = parseInt(args[skillIndex + 5] || "2", 10);
    let fireMode      = args[skillIndex + 6] || "single";

    // ------------------------------------------------------------
    //  Token + Character Validation
    // ------------------------------------------------------------
    if (!msg.selected || msg.selected.length === 0) {
        sendChat("System", "/w " + msg.who + " You must select a token.");
        return;
    }

    let token = getObj("graphic", msg.selected[0]._id);
    let character = getObj("character", token.get("represents"));
    if (!character) {
        sendChat("System", "/w " + msg.who + " Token is not linked to a character.");
        return;
    }

    // ------------------------------------------------------------
    //  Attribute Getter
    // ------------------------------------------------------------
    function getAttr(name, fallback = 0) {
        let obj = findObjs({
            type: "attribute",
            characterid: character.id,
            name: name
        })[0];
        if (!obj) return fallback;
        let v = parseInt(obj.get("current"), 10);
        return isNaN(v) ? fallback : v;
    }

    let attributeName  = skillToAttribute[skillName] || "";
    let attributeValue = attributeName ? getAttr(attributeName, 0) : 0;

    // ------------------------------------------------------------
    //  DAMAGE ROLL (supports normal / max / min modes)
    // ------------------------------------------------------------
    function rollDamage(expr, expertiseBonus, mode = "normal") {
        let match = expr.match(/(\d+)d\+?(\d+)?/i);
        if (!match) return { total: 0, detail: "Invalid damage expression" };

        let numDice   = parseInt(match[1], 10);
        let flatBonus = parseInt(match[2] || "0", 10);

        let rolls = [];
        for (let i = 0; i < numDice; i++) {
            rolls.push(randomInteger(10));
        }

        let successes;
        if (mode === "max") {
            // All dice count as successes
            successes = numDice;
        } else if (mode === "min") {
            // No dice count as successes
            successes = 0;
        } else {
            successes = rolls.filter(r => r >= 5).length;
        }

        let total = successes + flatBonus + expertiseBonus;

        return {
            total,
            detail: `Mode: ${mode} | Rolls: ${rolls.join(", ")} | Flat: ${flatBonus} | Expertise: ${expertiseBonus}`
        };
    }

    // ------------------------------------------------------------
    //  SKILL ROLL (with Luck Die, crit/fumble detection)
    // ------------------------------------------------------------
    function rollSkill() {
        let skillValue = getAttr(skillName, 0);

        // Bonus successes – force numeric
        let bonusValue = parseInt(getAttr(skillName + "_bonus", 0), 10) || 0;

        let dice = [];
        for (let i = 0; i < skillValue; i++) {
            dice.push({
                index: i + 1,
                value: randomInteger(10),
                oldValue: null,
                rerolled: false
            });
        }

        function isSuccess(v) { return v >= 5; }

        let initialSuccesses = dice.filter(d => isSuccess(d.value)).length;

        // Rerolls
        let maxRerolls = Math.abs(attributeValue);
        let rerollDetails = [];

        if (attributeValue !== 0 && maxRerolls > 0) {
            let candidates = dice.filter(d => attributeValue > 0 ? !isSuccess(d.value) : isSuccess(d.value));
            let allowed = Math.min(maxRerolls, candidates.length, dice.length);

            candidates.slice(0, allowed).forEach(d => {
                d.oldValue = d.value;
                d.value = randomInteger(10);
                d.rerolled = true;
                rerollDetails.push(`Die #${d.index}: ${d.oldValue} → ${d.value}`);
            });
        }

        let finalSuccesses = dice.filter(d => isSuccess(d.value)).length;
        let totalSuccesses = finalSuccesses + bonusValue;

        // Luck die is die #1 (still counts as a normal die)
        let luckDie = dice.length > 0 ? dice[0].value : null;

        // --------------------------------------------------------
        //  FUTURE: per-weapon crit range
        //  e.g. let critRange = getAttr(weaponName + "_critrange", 10);
        //  For now, crit = natural 10, fumble = natural 1 on luck die.
        // --------------------------------------------------------

        return {
            dice,
            initialSuccesses,
            finalSuccesses,
            totalSuccesses,
            rerollDetails,
            bonusValue,
            luckDie
        };
    }

    // ------------------------------------------------------------
    //  CLASSIFY OUTCOME (Luck Die + success/miss)
    // ------------------------------------------------------------
    function classifyOutcome(skillResult, defenseDC) {
        let luck = skillResult.luckDie;
        let success = skillResult.totalSuccesses >= defenseDC;

        // Default
        let type  = "normal";
        let label = success ? "Hit" : "Miss";
        let icon  = success ? "🎯" : "❌";
        let color = success ? "#4caf50" : "#f44336"; // green / red
        let dmgMode = "normal";

        if (luck === 10 && success) {
            // Critical Success
            type  = "crit";
            label = "Critical Hit";
            icon  = "💥";
            color = "#ffd700"; // gold
            dmgMode = "max";
        } else if (luck === 10 && !success) {
            // Advantageous Failure
            type  = "advantageous_failure";
            label = "Advantageous Failure";
            icon  = "🎯✨";
            color = "#64b5f6"; // blue-ish
            dmgMode = "none";
        } else if (luck === 1 && success) {
            // Weak Success
            type  = "weak_success";
            label = "Weak Success";
            icon  = "⚠️";
            color = "#ff9800"; // orange
            dmgMode = "min";
        } else if (luck === 1 && !success) {
            // True Fumble
            type  = "fumble";
            label = "Fumble";
            icon  = "❌🔥";
            color = "#e53935"; // strong red
            dmgMode = "none";
        }

        return { type, label, icon, color, dmgMode, success };
    }

    // ------------------------------------------------------------
    //  FIRE MODES
    // ------------------------------------------------------------
    let results = [];

    // SINGLE SHOT
    if (fireMode === "single") {
        let skill = rollSkill();
        let outcome = classifyOutcome(skill, defenseDC);

        if (!outcome.success) {
            results.push({ miss: true, skill, outcome });
        } else {
            let expertise = Math.max(0, Math.min(skill.totalSuccesses - defenseDC, maxExpertise));

            let dmg = null;
            if (outcome.dmgMode === "max") {
                dmg = rollDamage(dmgExpression, expertise, "max");
            } else if (outcome.dmgMode === "min") {
                dmg = rollDamage(dmgExpression, expertise, "min");
            } else {
                dmg = rollDamage(dmgExpression, expertise, "normal");
            }

            results.push({ skill, expertise, dmg, outcome });
        }
    }

    // BURST
    else if (fireMode === "burst") {
        let r1 = rollSkill();
        let r2 = rollSkill();
        let best = (r1.totalSuccesses >= r2.totalSuccesses) ? r1 : r2;

        let outcome = classifyOutcome(best, defenseDC);

        if (!outcome.success) {
            results.push({ miss: true, skill: best, outcome });
        } else {
            let expertise = Math.max(0, Math.min(best.totalSuccesses - defenseDC, maxExpertise));

            let dmg = null;
            if (outcome.dmgMode === "max") {
                dmg = rollDamage(dmgExpression, expertise, "max");
            } else if (outcome.dmgMode === "min") {
                dmg = rollDamage(dmgExpression, expertise, "min");
            } else {
                dmg = rollDamage(dmgExpression, expertise, "normal");
            }

            results.push({ skill: best, expertise, dmg, outcome });
        }
    }

    // FULL AUTO — WITH RECOIL DISPLAY
    else if (fireMode === "auto") {
        let penalty = 0;
        while (true) {
            let skill = rollSkill();
            let effective = skill.totalSuccesses - penalty;

            let outcome = classifyOutcome(skill, defenseDC);

            // For auto, we still gate on effective successes vs DC
            if (effective < defenseDC) break;

            let expertise = Math.max(0, Math.min(effective - defenseDC, maxExpertise));

            let dmg = null;
            if (outcome.dmgMode === "max") {
                dmg = rollDamage(dmgExpression, expertise, "max");
            } else if (outcome.dmgMode === "min") {
                dmg = rollDamage(dmgExpression, expertise, "min");
            } else {
                dmg = rollDamage(dmgExpression, expertise, "normal");
            }

            results.push({ skill, expertise, dmg, penalty, outcome });

            penalty++;
            if (penalty >= getAttr(skillName, 0)) break;
        }

        if (results.length === 0) {
            let skill = rollSkill();
            let outcome = classifyOutcome(skill, defenseDC);
            results.push({ miss: true, skill, outcome });
        }
    }

    // ------------------------------------------------------------
    //  OUTPUT
    // ------------------------------------------------------------
    let skillLevel = getAttr(skillName, 0);

    let output = `<div style="border:1px solid #444; padding:5px; background:#111; color:#eee;">`;
    output += `<span style="color:#fff;">${character.get("name")}</span> `;
    output += `attacks with <span style="color:#90caf9;">🔫 ${weaponName}</span><br>`;
    output += `Skill: <b>${skillName} ${skillLevel}</b> (${attributeName} ${attributeValue}) vs DC ${defenseDC}<br><br>`;

    results.forEach((r, i) => {
        let s = r.skill;
        let bonus = s.bonusValue ?? 0;
        let outcome = r.outcome || {
            type: r.miss ? "normal" : "normal",
            label: r.miss ? "Miss" : "Hit",
            icon: r.miss ? "❌" : "🎯",
            color: r.miss ? "#f44336" : "#4caf50",
            dmgMode: "normal",
            success: !r.miss
        };

        // Tooltip for successes
        let hoverTitle =
            `Initial Dice: ${s.dice.map(d => d.oldValue ?? d.value).join(' ')} | ` +
            `Rerolls: ${s.rerollDetails.length ? s.rerollDetails.join(', ') : 'None'} | ` +
            `Final Dice: ${s.dice.map(d => d.value).join(' ')} | ` +
            `Luck Die: ${s.luckDie} | ` +
            `Final Successes: ${s.finalSuccesses} | ` +
            `Bonus Successes: ${bonus} | ` +
            `Total Successes: ${s.totalSuccesses}`;

        let hoverSuccess = `<span title="${hoverTitle}">${s.totalSuccesses}</span>`;

        // FULL AUTO recoil display
        let recoilText = (fireMode === "auto" && !r.miss && r.penalty > 0)
            ? ` (recoil -${r.penalty})`
            : "";

        // Header line (Hit / Miss / Crit / Fumble / etc.)
        output += `<span style="color:${outcome.color}; font-weight:bold;">${outcome.icon} ${outcome.label}`;
        if (fireMode === "auto" && !r.miss) {
            output += ` ${i+1}${recoilText}`;
        }
        output += `</span><br>`;

        // Common info
        output += `Successes: ${hoverSuccess}<br>`;

        if (outcome.type === "advantageous_failure") {
            output += `<span style="color:#ccc;">No damage, but something goes your way.</span><br><br>`;
            return;
        }

        if (outcome.type === "fumble") {
            output += `<span style="color:#ff7043;">No damage. This is a true fumble.</span><br>`;
            // FUTURE: apply jam / mishap effects here.
            output += `<br>`;
            return;
        }

        if (r.miss) {
            output += `<span style="color:#ccc;">No damage.</span><br><br>`;
            return;
        }

        // Hit cases (normal / crit / weak success)
        output += `Expertise: <span style="color:#64b5f6;">🔧 ${r.expertise}</span><br>`;

        let dmg = r.dmg;
        let hoverDamage = `<span title="Damage Rolls: ${dmg.detail}">${dmg.total}</span>`;
        output += `Damage: <span style="color:#ce93d8;">💢 ${hoverDamage} ${dmgTarget} (${powerLevel} power)</span><br><br>`;
    });

    output += `</div>`;

    sendChat(character.get("name"), output);
});