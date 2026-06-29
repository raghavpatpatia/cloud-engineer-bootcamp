# 🏋️ World 1 — Exercises

Extra reps to make clean-architecture instincts automatic before the boss battle. None are required to advance, but each one is exactly the kind of reasoning "Refactor the Spaghetti" demands. Each **Side Quest** awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (types, OOP & SOLID fluency)

1. From memory, state the difference between `struct b = a` and `class b = a` and what each prints after mutating `b`.
   <details><summary>Hint</summary>struct → independent copy (a unchanged); class → shared reference (a changes too).</details>
2. Name one piece of Ashfall data that should be a `struct` and one that should be a `class`, and defend each.
   <details><summary>Hint</summary>Small copied bundle (Stats) = struct; shared living entity (Health) = class.</details>
3. Describe a 4-deep inheritance tree and the *one* feature request that breaks it. Then express the same entities as components.
   <details><summary>Hint</summary>"flying healer that doesn't explode" — attach Flight + Regen, omit Explode.</details>
4. For each: which SOLID letter is violated? (a) new enemy forces editing a switch; (b) Health also saves the file; (c) a 12-method `IEntity`.
   <details><summary>Hint</summary>a = O (also D), b = S, c = I.</details>
5. Why must you `-=` an event handler in `OnDisable`, and why must the handler be a *named* method?
   <details><summary>Hint</summary>Static events outlive scenes → leaks/double-fire; you can't <code>-=</code> a lambda you never stored.</details>

## Architecture warm-ups

6. Sketch the FSM for Menu/Playing/Paused/GameOver and mark which transitions are illegal.
7. Explain to a rubber duck why `Health` should *raise an event* instead of calling the HUD directly.
8. Give one Ashfall system that deserves to be a Singleton and one that absolutely should not be.
   <details><summary>Hint</summary>Yes: GameManager (one app-wide coordinator). No: an individual Enemy (many instances, no global access needed).</details>

---

## 🌟 Side Quest 1 — The Pooling Patch (+50 XP)

Prove you understand the GC by *killing* an allocation hotspot. Create a script that spawns a "hit number" object every frame the naive way, watch the cost, then fix it with a simple object pool.

**Requirements:**
1. A `NaiveSpawner` that `new`s a small object (or instantiates a prefab) every `Update()` — the wrong way.
2. Observe the allocation churn (Unity **Profiler** → GC Alloc, or just reason about it from Level 1).
3. A `PooledSpawner` that pre-allocates a fixed array/`Queue` of reusable objects and recycles them instead of allocating.
4. Confirm the pooled version allocates ~nothing per frame after warm-up.

```
Test: with the Profiler open, the naive version shows steady GC Alloc per frame; the pooled version shows ~0.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using System.Collections.Generic;
using UnityEngine;

public class PooledSpawner : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int size = 32;
    private readonly Queue<GameObject> pool = new();

    void Awake()
    {
        for (int i = 0; i < size; i++)        // allocate ONCE, up front
        {
            var go = Instantiate(prefab);
            go.SetActive(false);
            pool.Enqueue(go);
        }
    }

    public GameObject Get()                    // reuse, don't allocate
    {
        var go = pool.Dequeue();
        go.SetActive(true);
        return go;
    }

    public void Return(GameObject go)          // recycle back into the pool
    {
        go.SetActive(false);
        pool.Enqueue(go);
    }
}
```

🎯 **Side quest complete when:** the pooled spawner reuses objects with ~0 per-frame GC allocation, and you can explain *why* the naive version caused hitches. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — The Achievement Listener (+50 XP)

Prove the EventBus truly decouples by adding a brand-new system that touches **no existing file**. Build an achievement system that unlocks "First Blood" the first time an enemy is killed — purely by subscribing.

**Steps:**
1. Create `AchievementSystem : MonoBehaviour` that subscribes to `GameEvents.EnemyKilled` in `OnEnable` and unsubscribes in `OnDisable`.
2. On the *first* kill, log "🏆 Achievement: First Blood" and ignore further kills.
3. Crucially: do **not** edit `Health`, `GameManager`, or any other existing script. Adding the feature should require *only* the new file (this is Open/Closed in action).
4. Test by raising `GameEvents.RaiseEnemyKilled()` twice — the achievement fires once.

```bash
# the only change to the repo is ONE new file:
git status   # should show only Assets/Scripts/Systems/AchievementSystem.cs (+ .meta)
```

<details>
<summary>💡 What you should have learned</summary>

```csharp
using UnityEngine;

public class AchievementSystem : MonoBehaviour
{
    private bool firstBloodUnlocked;

    void OnEnable()  => GameEvents.EnemyKilled += OnEnemyKilled;
    void OnDisable() => GameEvents.EnemyKilled -= OnEnemyKilled;

    private void OnEnemyKilled()
    {
        if (firstBloodUnlocked) return;
        firstBloodUnlocked = true;
        Debug.Log("🏆 Achievement: First Blood");
    }
}
```

- Adding a feature without touching existing code is the literal definition of **Open/Closed**.
- The publisher (`Health`/enemy) never learned achievements exist — that's the observer pattern's payoff.
- Subscribe/unsubscribe with the lifecycle to avoid the double-fire bug from Level 4.

🎯 **Side quest complete when:** "First Blood" fires exactly once, and the *only* changed file is the new system. Add **+50 XP** to PROGRESS.md.
</details>

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
