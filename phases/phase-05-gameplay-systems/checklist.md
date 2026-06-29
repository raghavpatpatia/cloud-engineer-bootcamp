# ✅ World 5 — Readiness Checklist

Before you face "The Loot Run" and unlock World 6, make sure all of this is true. The boss assumes *every* skill below — it's one full loot run that exercises the whole world at once: data-driven items and abilities, an inventory + equipment that changes stats, abilities on cooldowns, a real damage pipeline, status effects, and weighted loot + gold. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Data-Driven Design with ScriptableObjects:** I can separate data from code with `ScriptableObject` assets — and I built `ItemSO`/`AbilitySO` data assets the systems consume (tune without recompiling)
- [ ] **L2 — Inventory & Equipment:** I can model stacking inventory, equip slots, and item events — and I built Ashfall's `Inventory` + equipment that modifies `Stats` via base+modifier
- [ ] **L3 — Abilities & Cooldowns:** I understand the command-object ability pattern, cooldown timers, and costs — and I built a dash + a projectile driven by `AbilitySO`
- [ ] **L4 — Combat & Damage:** I understand the damage pipeline on `IDamageable` (W1), hit detection, i-frames, and knockback — and I built Ashfall's combat resolver applying damage to player and enemies
- [ ] **L5 — Status Effects, Loot & Economy:** I understand modular status effects (DoT/buffs), weighted loot tables, and currency — and I built poison/burn, loot drops, and gold

## 🧰 What I've built / set up
- [ ] `ItemSO` and `AbilitySO` ScriptableObjects (data a designer tunes in the Inspector), in `Assets/Scripts/Data`
- [ ] An `Inventory` (stacking + item events) and `Equipment` slots that modify the player's `Stats`, in `Assets/Scripts/Items`
- [ ] An ability system (command objects + per-caster cooldowns + costs) with a dash and a projectile, in `Assets/Scripts/Abilities`
- [ ] A damage pipeline on `IDamageable` with hit detection, i-frames, and knockback, in `Assets/Scripts/Combat`
- [ ] A modular status-effect system (poison/burn that ticks), a weighted `LootTable`, and a gold/economy
- [ ] All of it persisted by the W3 save system (inventory, gold, equipped gear) and committed/pushed

## 🧠 Skills I can do without looking up
- [ ] Decide what belongs in a ScriptableObject (data) vs a system (behavior) and justify it
- [ ] Add/stack/remove items and compute a final stat as `base + sum(modifiers)` so equip/unequip is clean
- [ ] Implement an ability as a command object with a per-caster cooldown (state) vs SO duration (data)
- [ ] Route all damage through `IDamageable` and guard it with i-frames so one touch isn't instant death
- [ ] Build a modular status effect (duration, tick, expire) and a weighted random loot roll

---

## 🔎 Self-test (from memory, no peeking)

1. A designer wants to retune item damage without a recompile. What construct enables that, and what goes *in* it vs stays in code?
   <details><summary>Answer</summary>A <strong>ScriptableObject</strong> (<code>ItemSO</code>) — a shared data asset edited in the Inspector. It holds <em>data</em> (name, icon, damage, max stack, cost); the <em>behavior</em> (swing, apply damage, VFX) stays in systems you own. Edit the asset once, every reference sees it, no recompile.</details>
2. You equip a sword that grants +5 attack. How do you apply it so unequipping is clean?
   <details><summary>Answer</summary>Keep <strong>base stats separate from modifiers</strong>. Equipment adds a modifier; the final stat is <code>base + sum(modifiers)</code>, recomputed on equip/unequip. Never bake the bonus into the base value — you can't subtract it back reliably on a swap.</details>
3. A dash ability is shared by many entities but each has its own cooldown. What's data and what's runtime state?
   <details><summary>Answer</summary>Cooldown <strong>duration</strong> is data on the shared <code>AbilitySO</code>; cooldown <strong>remaining time</strong> is per-caster runtime state. Storing "time remaining" on the shared SO would make every caster share one timer — track it in a per-entity cooldown map instead.</details>
4. Why route all damage through `IDamageable`, and what do i-frames prevent?
   <details><summary>Answer</summary>The player, enemies, and breakables all implement <code>IDamageable</code>, so <em>one</em> damage pipeline hits anything damageable — no type checks, no duplicated code (the W1 contract). <strong>I-frames</strong> are a short invulnerability window after a hit, preventing per-physics-frame re-damage that would kill in an instant.</details>
5. A loot table drops commons often and legendaries rarely. How does a weighted random roll pick a drop?
   <details><summary>Answer</summary>Each entry has a <strong>weight</strong>. Sum all weights, roll a random value in <code>[0, total)</code>, then walk the entries subtracting each weight until the roll goes negative — that entry drops. A larger weight is a larger slice of the range, so it's picked more often.</details>

---

## 👹 Boss readiness
- [ ] I can clear a generated room: **cast an ability** (on cooldown, paying its cost)
- [ ] The player **takes damage** through the pipeline and survives a touch thanks to **i-frames**
- [ ] I can **apply a status effect** (poison/burn) to an enemy that ticks over time
- [ ] Killing an enemy rolls **weighted loot + gold** that I can **pick up**
- [ ] I can **equip** a dropped item and **see my stats change** (base + modifier)
- [ ] The whole run is **persisted** (inventory, gold, equipped gear) via the W3 save system
- [ ] Everything is **data-driven** — I can rebalance via `ItemSO`/`AbilitySO` without editing code
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — Crafting Recipe System (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Rarity-Colored Tooltips (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Loot Run](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
