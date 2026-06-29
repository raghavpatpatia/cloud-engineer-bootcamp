# 🏋️ World 5 — Exercises

Extra reps to make the *gameplay systems* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "The Loot Run" demands — keeping data out of code, modeling inventory and stats cleanly, gating abilities behind cooldowns, resolving damage safely, and rolling loot by weight. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (data, inventory, abilities, combat, loot)

1. A designer wants to retune every sword's damage at midnight without you. Why does that argue for a `ScriptableObject` asset over a `[SerializeField] float damage` on a MonoBehaviour?
   <details><summary>Hint</summary>An <code>ItemSO</code> is a <strong>shared data asset</strong> on disk — edit it once in the Inspector and every instance/scene that references it sees the change, no recompile, no per-prefab editing. A field on a MonoBehaviour lives per-instance in a scene/prefab, so balancing means hunting down every copy.</details>
2. Why should `ItemSO` hold *data* (name, icon, damage, max stack) but **not** the logic that swings the sword?
   <details><summary>Hint</summary>Data vs code separation: the SO is the tunable knob a designer owns; the *behavior* (apply damage, play VFX) is code you own. Mixing them means designers can break gameplay logic and you can't reuse the data. SOs are "what," systems are "how."</details>
3. Picking up a 3rd health potion when you already hold 2 — what should the inventory do, and what data does a stack need?
   <details><summary>Hint</summary>Stack it: find an existing slot for that item with room under <code>maxStack</code>, increment count; only take a new slot if none has room. A stack is <em>(ItemSO reference, int count)</em> — never duplicate the item data itself.</details>
4. When you equip a sword that gives +5 attack, how do you change the player's stats *without* baking +5 into the base stat (so unequipping is clean)?
   <details><summary>Hint</summary>Keep <strong>base stats</strong> separate from <strong>modifiers</strong>. Equipment adds a modifier; the final stat is <code>base + sum(modifiers)</code>, recomputed on equip/unequip. Never mutate the base — you'll never get it back when you swap gear.</details>
5. Why model an ability as a command object (an `AbilitySO` + a small runtime) instead of a giant `switch (abilityName)` in the player?
   <details><summary>Hint</summary>The Command pattern: each ability is self-contained (its cost, cooldown, effect), so adding a new one is a new asset + class, not another branch in a growing <code>switch</code>. It's open for extension, closed for modification — and a designer can assign abilities to slots as data.</details>
6. A dash has a 2s cooldown. Where does the cooldown timer live, and why not on the `AbilitySO`?
   <details><summary>Hint</summary>Cooldown <em>duration</em> is data (on the SO); cooldown <em>state</em> (time remaining) is per-caster runtime. If you store "time remaining" on the shared SO, every entity using that ability shares one timer — chaos. Track remaining time in a per-entity cooldown map.</details>
7. Without i-frames, walking into an enemy deals damage *every physics frame*. What do i-frames give you and how do you implement them simply?
   <details><summary>Hint</summary>Invulnerability frames: after taking a hit, the entity ignores damage for a short window (e.g. 0.5s). Implement as a timer/flag — <code>if (invulnerable) return;</code> at the top of <code>TakeDamage</code>, set <code>invulnerable</code> true and start a countdown after a successful hit.</details>
8. Your damage code calls `enemy.GetComponent<Enemy>().hp -= dmg`. Why route it through the W1 `IDamageable` interface instead?
   <details><summary>Hint</summary>The player, enemies, and breakable barrels can all be <code>IDamageable</code>. Coding to the interface means one damage pipeline hits anything damageable — no type checks, no duplicated logic. That's the W1 contract paying off.</details>
9. A loot table should drop commons often and legendaries rarely. How do weighted random rolls work?
   <details><summary>Hint</summary>Each entry has a <strong>weight</strong>. Sum all weights, roll a random number in <code>[0, total)</code>, then walk the entries subtracting weights until the roll goes negative — that entry drops. Bigger weight = bigger slice of the range = more likely.</details>
10. Poison should tick 2 damage/sec for 5s and *not* be re-applied infinitely by overlapping hits. How do you model a status effect cleanly?
    <details><summary>Hint</summary>A status effect is a small object with <em>duration, tick interval, and an Apply/Tick/Expire</em>. Hold a list of active effects per entity; on re-apply, refresh duration or stack (a design choice) rather than spawning unbounded copies. Update ticks each frame and remove when expired.</details>

---

## 🌟 Side Quest 1 — Crafting Recipe System (+50 XP)

Prove your data-driven inventory is *composable*, not just a list. Let the player **combine items into new ones** via designer-authored recipes — `2 × Iron Ore + 1 × Coal → 1 × Steel Ingot` — defined entirely as data, with the crafting *logic* owned by code.

**Requirements:**
1. Create a `RecipeSO` ScriptableObject: a list of input `(ItemSO, count)` requirements and an output `(ItemSO, count)`. A designer authors recipes in the Inspector — no code per recipe.
2. Write a `CraftingSystem` that, given a recipe, checks the inventory has every input, **consumes** the inputs, and **adds** the output. Fail cleanly (no partial consumption) if anything's missing.
3. Drive a tiny crafting UI (or a debug button) off the recipe list — only show recipes the player can currently afford.
4. Persist the result through the W3 save system: craft, save, reload — the ingredients are gone and the output is in the bag.

```
Test: hold 2 Iron Ore + 1 Coal, craft Steel Ingot → inventory now shows 1 Steel Ingot and 0 ore/coal. Try again with 1 ore → craft is rejected, nothing consumed.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
[CreateAssetMenu(menuName = "Ashfall/Recipe")]
public class RecipeSO : ScriptableObject
{
    public List<ItemStack> inputs;   // ItemStack = (ItemSO item, int count) — DATA, designer-authored
    public ItemStack output;
}

public class CraftingSystem
{
    public bool TryCraft(RecipeSO recipe, Inventory inv)
    {
        // 1. Check FIRST — never consume on a recipe you can't complete.
        foreach (var need in recipe.inputs)
            if (inv.CountOf(need.item) < need.count) return false;

        // 2. Consume all inputs, then add the output (all-or-nothing).
        foreach (var need in recipe.inputs) inv.Remove(need.item, need.count);
        inv.Add(recipe.output.item, recipe.output.count);
        return true;
    }
}
```

- The recipe is **pure data** — a designer can add "Steel Sword = 2 Steel Ingot + 1 Leather" without touching `CraftingSystem`. That's the L1 lesson paying rent.
- **Check before consume** is the whole correctness story: validate the full recipe, *then* mutate. A half-consumed craft on failure is the classic bug.
- Reuse the L2 inventory's `CountOf` / `Add` / `Remove` — crafting is a *consumer* of inventory, not a reimplementation of it.

🎯 **Side quest complete when:** a designer-authored `RecipeSO` crafts its output by consuming inputs, rejects cleanly when inputs are missing (nothing consumed), and the result survives a save/reload. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Rarity-Colored Tooltips (+50 XP)

Loot is only satisfying if the player can *read* it at a glance. Add an item **rarity** tier driven by data, and a hover **tooltip** that colors the item name by rarity (gray common → green uncommon → blue rare → purple epic → orange legendary) and lists its stat modifiers.

**Steps:**
1. Add a `Rarity` enum and a `rarity` field to `ItemSO`, plus a designer-tunable color per rarity (a small `RaritySO`/color table — data, not hard-coded hex in the UI script).
2. Build a `Tooltip` UI that, on hover over an inventory slot, shows the item name in its rarity color, its description, and a formatted list of its stat modifiers (e.g. "+5 Attack, +2 Crit").
3. Make legendary drops visually pop — e.g. a subtle name shimmer or icon glow — so a great drop *feels* great.
4. Verify it reads correctly across every rarity tier using a few test `ItemSO` assets.

```
Test: hover a common dagger → gray name, "+1 Attack". Hover a legendary blade → orange name (with glow), "+12 Attack, +5 Crit". Colors come from the data table, not literals in the UI code.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
public enum Rarity { Common, Uncommon, Rare, Epic, Legendary }

// Color lives in DATA so design can rebalance the palette without a recompile.
[CreateAssetMenu(menuName = "Ashfall/Rarity Palette")]
public class RarityPaletteSO : ScriptableObject
{
    public Color[] byRarity;   // indexed by (int)Rarity
    public Color Of(Rarity r) => byRarity[(int)r];
}

public class Tooltip : MonoBehaviour
{
    public RarityPaletteSO palette;
    public TMP_Text nameLabel, statsLabel;

    public void Show(ItemSO item)
    {
        nameLabel.text  = item.displayName;
        nameLabel.color = palette.Of(item.rarity);          // color BY DATA, not literal
        statsLabel.text = string.Join(", ", item.Modifiers  // reuse L2 stat modifiers
            .Select(m => $"{(m.value >= 0 ? "+" : "")}{m.value} {m.stat}"));
        gameObject.SetActive(true);
    }
}
```

- Rarity and its color are **data** (`ItemSO.rarity` + a palette asset) — the UI just *reads* them. Hard-coding `if (rarity == Legendary) color = orange` in the UI is exactly the coupling L1 teaches you to avoid.
- The tooltip **reuses** L2's stat modifiers rather than re-deriving stats — one source of truth for "what does this item do."
- Readability *is* a feature: weighted loot (L5) is only fun if the player can instantly tell a legendary from vendor trash.

🎯 **Side quest complete when:** items carry a data-driven rarity, the tooltip colors the name by rarity from a palette asset (no literals in UI code) and lists stat modifiers, and legendaries visibly stand out. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
