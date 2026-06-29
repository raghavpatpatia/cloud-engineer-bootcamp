# 🏋️ World 9 — Exercises

Extra reps to make the *engine architecture* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "1000 Entities at 60 FPS" demands — laying data out for the cache, killing per-frame allocations, processing entities in bulk, and proving the win with the profiler. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [🏗️ Boss Battle](boss-battle.md)

---

## Warm-ups (data layout, pooling, ECS, profiling)

1. In one sentence each, what are **AoS** and **SoA**, and why is SoA usually faster for a hot loop?
   <details><summary>Hint</summary><strong>AoS</strong> (array of structs) stores whole objects together: `[ {x,y,hp,sprite}, {x,y,hp,sprite}, ... ]`. <strong>SoA</strong> (struct of arrays) stores each field in its own tight array: `xs[]`, `ys[]`, `hps[]`. A loop that only touches positions in AoS drags the entire object (hp, sprite, everything) through the cache; in SoA it streams just `xs[]`/`ys[]` contiguously, so every cache line is 100% useful data. SoA wins because the CPU reads memory in <strong>cache lines</strong>, and SoA wastes none of them.</details>
2. What is a **cache line**, and why does it mean "memory layout" decides performance more than "algorithm cleverness" in a tight loop?
   <details><summary>Hint</summary>A cache line is the fixed chunk (typically 64 bytes) the CPU pulls from RAM at once. RAM is ~100× slower than cache, so the real cost in a hot loop is usually <em>cache misses</em>, not arithmetic. If your data is contiguous and accessed in order, one fetch serves many iterations (the prefetcher even reads ahead); if it's scattered across the heap (pointer-chasing objects), nearly every access is a miss. So laying data out so the loop walks it linearly beats a "smarter" algorithm that thrashes the cache.</details>
3. Why does calling `new` (or instantiating a prefab) in a per-frame loop cause **GC spikes**, and what's the fix?
   <details><summary>Hint</summary>Every `new`/`Instantiate` allocates managed heap memory. Spawn hundreds of bullets a frame and you generate garbage fast; when the GC eventually runs to reclaim it, it can <strong>stall the main thread for milliseconds</strong> — a visible hitch. The fix is <strong>object pooling</strong>: pre-allocate a pool of reusable objects once, then "spawn" = take a dead one and reactivate it, "despawn" = deactivate and return it. You allocate at load time, never in the hot loop, so there's no garbage to collect.</details>
4. In **ECS**, what do **Entity**, **Component**, and **System** each mean, and how is that different from a MonoBehaviour-per-enemy?
   <details><summary>Hint</summary>An <strong>Entity</strong> is just an id (a handle). A <strong>Component</strong> is plain <em>data</em> with no behavior (Position, Velocity, Health). A <strong>System</strong> is <em>behavior</em> that runs over all entities with the components it cares about, in bulk (a MovementSystem iterates every Position+Velocity once per frame). The MonoBehaviour model couples data and behavior on each object and calls `Update()` per object (scattered, virtual calls, cache-hostile). ECS splits data from behavior and processes it in tight, contiguous batches — which is exactly what the cache and the profiler reward.</details>
5. Why must you **profile before** you optimize, and what's the danger of optimizing by intuition?
   <details><summary>Hint</summary>Your intuition about where time goes is almost always wrong — the real hotspot is usually somewhere boring. Optimize by guess and you spend a day shaving a loop that costs 0.1 ms while a single GC spike eats 8 ms untouched. The profiler tells you the <em>actual</em> frame-time and allocation breakdown; you fix the biggest bar, then measure again. "Measure, don't guess" — every change is a before/after on the profiler, not a vibe.</details>
6. When should a save be **JSON** and when should it be **binary**, and what's the trade-off?
   <details><summary>Hint</summary><strong>JSON</strong> is human-readable, debuggable, and easy to diff/edit — great for config, settings, and dev iteration — but it's larger and slower to parse. <strong>Binary</strong> is compact and fast to read/write — great for big save states and shipping builds — but opaque and harder to inspect. Trade-off: readability/debuggability vs size/speed. Many games use JSON in dev and binary in release, or JSON for small config and binary for the heavy world state.</details>
7. What is **save versioning**, and why does an old save break a new build without it?
   <details><summary>Hint</summary>A save is a snapshot of your data <em>schema at the time it was written</em>. Change the schema (rename a field, add a stat, restructure inventory) and an old save no longer matches what the loader expects — it crashes or loads garbage. <strong>Versioning</strong> stamps each save with a version number; the loader checks it and runs <strong>migrations</strong> to upgrade old saves to the current shape. Without it, every save your players made becomes unloadable the moment you patch — a cardinal sin in a shipped game.</details>
8. What does an **asset pipeline / addressables** buy you over referencing every asset directly?
   <details><summary>Hint</summary>Direct references (e.g. a hard prefab link) force everything they touch to <strong>load into memory at once</strong> and ship in the build whether used or not — memory bloat and long loads. An asset pipeline (Unity <strong>Addressables</strong>) references content by <em>address</em> and loads it <strong>on demand</strong> (and unloads it when done), so you stream the dungeon room you're in, not the whole game. It also decouples content from code, enabling patching/DLC. The instinct: don't hold what you're not using.</details>
9. What are the typical **engine layers** (core / platform / gameplay) and why does dependency direction matter?
   <details><summary>Hint</summary><strong>Core</strong> = engine-agnostic fundamentals (math, ECS, pooling, serialization). <strong>Platform</strong> = OS/engine-specific glue (Unity input, rendering, file I/O). <strong>Gameplay</strong> = Ashfall's actual rules (combat, dungeon, enemies). Dependencies point <strong>downward only</strong>: gameplay depends on core, core depends on nothing game-specific. If core reaches up into gameplay, you've got a tangle you can't test, reuse, or reason about. Clean layering is what lets W10 build and deploy the thing without surprises.</details>
10. **Service locator** vs **dependency injection** — what's the difference, and why have a deliberate **bootstrap order**?
    <details><summary>Hint</summary>Both solve "how does code find the services it needs (audio, save, input) without `new`-ing or hard-coupling them." <strong>DI</strong> hands a system its dependencies from outside (explicit, testable, more wiring). <strong>Service locator</strong> is a central registry systems ask for a service (convenient, but the dependency is hidden). Either way you need a <strong>bootstrap order</strong>: subsystems must come up in dependency order (e.g. save system before the thing that loads a save, input before gameplay) — a deliberate startup sequence, not random `Awake()` timing — or you get null-reference races on launch.</details>

---

## 🌟 Side Quest 1 — Job/Worker-Thread Experiment (+50 XP)

Prove you understand *why* data-oriented layout unlocks parallelism by pushing your entity update **off the main thread**. A tight SoA loop over thousands of independent entities is the perfect candidate for multithreading — and you'll feel the difference on the frame timer.

**Requirements:**
1. Take a hot, **independent** per-entity update (e.g. integrate position from velocity for 5000+ pooled entities) and run it across **multiple worker threads** — Unity's **Job System** (`IJobParallelFor` + Burst) is the natural fit; a `Parallel.For` over your SoA arrays also demonstrates the idea.
2. Split the work into **chunks** so each thread owns a contiguous slice of the arrays (no two threads writing the same element — data-oriented layout makes this clean).
3. **Profile both:** single-threaded vs jobified. Record the main-thread time for the entity update before and after.
4. Note *why* it parallelized so easily: the data is contiguous, the work is independent, and there's no shared mutable state in the loop — the exact properties SoA + ECS give you for free.

```
Test: 5000 pooled entities integrating position each frame. Single-threaded:
the update eats ~X ms of the main thread. Jobified across N worker threads:
it drops to ~X/N (minus overhead) and the main thread breathes. Same result,
same data layout — just spread across cores because nothing is entangled.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
// SoA arrays make this trivially parallel: each index is independent.
struct IntegrateJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float2> velocities;
    public NativeArray<float2> positions;
    public float dt;
    public void Execute(int i) => positions[i] += velocities[i] * dt;  // no shared state
}

// Schedule across workers, batch of 64 per chunk, then complete before render.
var handle = new IntegrateJob { velocities = vel, positions = pos, dt = Time.deltaTime }
                 .Schedule(count, 64);
handle.Complete();
```

- The win is *not* the threading API — it's that **data-oriented layout made the work parallelizable in the first place**. Try to jobify a list of MonoBehaviours and you can't: their data is scattered and tangled with engine objects you can only touch on the main thread.
- `NativeArray<T>` (Unity) is contiguous, blittable, and thread-safe to slice — it *is* SoA the Job System can read. That's not a coincidence; DOTS is built on exactly this idea.
- Always `Complete()` the handle before anything reads the results that frame. Profile the main-thread cost of the update specifically, not total frame time, to see the real speedup.
- Engine-agnostic: every modern engine (Unreal's task graph, custom job systems) parallelizes the same way — contiguous data + independent work. OOP-scattered objects can't go there.

🎯 **Side quest complete when:** an independent per-entity update over 5000+ entities runs across multiple worker threads, you've chunked the SoA arrays with no data races, and you can show a before/after profiler delta proving the main-thread time dropped. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Memory-Profiler Audit (+50 XP)

Prove you can find and kill per-frame allocations the way the boss demands. The boss's hard line is **zero per-frame GC allocation** — this quest is the investigation that gets you there: open the memory profiler, hunt every allocating call in your hot loops, and flatten the GC line.

**Requirements:**
1. With a few hundred entities active, open the **Profiler** (CPU module) and the **Memory Profiler**. Find the **GC Alloc** column / take snapshots and identify *every* call site allocating managed memory **per frame**.
2. Track down the usual suspects: `new` in Update, **LINQ** in hot paths, **boxing** (struct → object), `foreach` over allocating enumerators, string concatenation, closures/lambdas capturing variables, and `Instantiate`/`Destroy` instead of pooling.
3. **Fix them:** pool instead of instantiate, cache reusable buffers, replace LINQ with plain loops, avoid boxing, hoist allocations out of the loop. Re-snapshot after each fix.
4. Drive the per-frame **GC Alloc to 0 B** (or as close as the engine allows) while entity count is high, and capture a before/after of the GC spikes in the CPU timeline.

```
Test: 500 entities active. BEFORE: the CPU timeline shows GC.Collect spikes
every few frames and the GC Alloc column reads kilobytes/frame. AFTER your
audit: GC Alloc reads ~0 B/frame, the spikes are gone, and the frame line
is flat. You didn't make the game do less — you made it stop creating garbage.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```
THE HUNT (find it, then kill it):

1. Profiler → CPU module → sort by "GC Alloc". Any row with bytes/frame in
   a steady state is a leak of garbage. Deep Profile to get exact call sites.
2. Memory Profiler → take a snapshot, run a few frames, take another, DIFF.
   The diff shows exactly what's being allocated and where.
3. Common culprits and fixes:
     - Instantiate/Destroy per spawn        → object POOL (reuse, don't allocate)
     - LINQ (.Where/.Select/.ToList) in loop → hand-written for-loop, reused list
     - boxing (struct passed as object/enum  → generic/typed APIs, no boxing
       as Dictionary key, params object[])
     - string + concatenation each frame     → cache the string / StringBuilder / don't
     - closures capturing locals             → static methods / cached delegates
     - foreach over some collections          → for with index over arrays/Lists
4. Re-snapshot after EACH fix. Watch GC Alloc/frame fall toward 0.
```

- This is the discipline behind the boss's "prove it on the profiler." A flat GC line at 1000 entities is the *evidence*, not the claim.
- The single biggest win is almost always **pooling** — `Instantiate`/`Destroy` is the loudest allocator in most games. Get pooling right first, then chase the smaller leaks.
- Boxing is the sneaky one: passing a struct where an `object` is expected silently allocates. Watch for it in event systems, dictionaries keyed by enums, and `params object[]` logging calls.
- Engine-agnostic: every managed runtime (C#, Java, JS) has this exact failure mode and this exact fix — don't generate garbage in the loop, and there's nothing for the collector to spike on.

🎯 **Side quest complete when:** with several hundred entities active you've used the profiler + memory profiler to identify every per-frame allocation, fixed them (pooling, no LINQ/boxing in hot paths, cached buffers), driven per-frame GC Alloc to ~0 B, and captured a before/after of the GC spikes disappearing. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
