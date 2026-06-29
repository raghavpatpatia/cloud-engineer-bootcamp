# ✅ World 9 — Readiness Checklist

Before you face "1000 Entities at 60 FPS" and unlock World 10, make sure all of this is true. The boss assumes *every* skill below — it's one brutal stress test that exercises the whole world at once: 1000+ entities rendered and updated at a locked 60 FPS, built on data-oriented hot paths and an ECS-lite core, with object pooling driving **zero per-frame GC allocation**, all proven on the profiler. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [🏗️ Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Data-Oriented Design:** I understand cache lines, AoS vs SoA, and why OOP-heavy loops thrash the cache — and I profiled and rebuilt Ashfall's projectile hot path as a struct-of-arrays loop
- [ ] **L2 — ECS-lite & Object Pooling:** I understand entities/components/systems and object pooling — and I built Ashfall's ECS-lite bullet/enemy system with pools that allocate nothing per frame
- [ ] **L3 — Serialization & Asset Pipeline:** I understand versioned saves, binary vs JSON, and on-demand asset loading — and I built versioned Ashfall saves plus an asset-loading layer
- [ ] **L4 — Subsystems & Engine Layering:** I understand core/platform/gameplay layering, service locator vs DI, and bootstrap order — and I refactored Ashfall into clean layered subsystems

## 🧰 What I've built / set up
- [ ] A **profiled, struct-of-arrays** projectile hot path that walks memory linearly, in `Engine/` / `Core/`
- [ ] An **ECS-lite** core (entities · components · systems) with **object pools** for bullets/enemies — spawning reuses dead objects, never `new`, in `Systems/` + `Pools/`
- [ ] **Versioned serialization** (binary and/or JSON, chosen on purpose) with a migration path for old saves, plus an **asset pipeline** loading content on demand, in `Serialization/` + `Assets/`
- [ ] Ashfall **layered** into core / platform / gameplay with a deliberate **bootstrap order** and a service-locator-or-DI wiring
- [ ] A **before/after profiler capture** showing frame time held at 60 FPS and per-frame GC Alloc driven to ~0 — committed and pushed

## 🧠 Skills I can do without looking up
- [ ] Explain AoS vs SoA and why SoA is cache-friendly for a hot loop
- [ ] Explain why `new`/`Instantiate` in a per-frame loop causes GC spikes, and how pooling fixes it
- [ ] Define entity/component/system and contrast ECS with a MonoBehaviour-per-object
- [ ] Choose binary vs JSON for a save, and explain why saves need versioning/migration
- [ ] Name the engine layers, the dependency direction, and why bootstrap order matters — and read the profiler well enough to prove a change worked

---

## 🔎 Self-test (from memory, no peeking)

1. What are **AoS** and **SoA**, and why is SoA faster for a loop that touches one field across many entities?
   <details><summary>Answer</summary><strong>AoS</strong> = array of structs/objects: each element holds all fields together (`[{x,y,hp,sprite},...]`). <strong>SoA</strong> = struct of arrays: each field is its own contiguous array (`xs[]`, `ys[]`, `hps[]`). The CPU reads memory in <strong>cache lines</strong> (~64 B). A loop touching only positions in AoS drags every other field (hp, sprite) through cache too, wasting most of each line; in SoA it streams `xs[]`/`ys[]` densely, so every byte fetched is useful and the prefetcher reads ahead. Same data, but SoA turns a cache-miss-bound loop into a streaming one — often several times faster.</details>
2. Why does instantiating in a hot loop cause **GC spikes**, and how does **object pooling** eliminate them?
   <details><summary>Answer</summary>Every `new`/`Instantiate` allocates on the managed heap. Spawn hundreds of bullets a frame and you produce garbage fast; eventually the <strong>garbage collector</strong> runs to reclaim it and <em>stalls the main thread</em> for milliseconds — a visible frame hitch. <strong>Object pooling</strong> pre-allocates a fixed set of reusable objects at load time: "spawn" takes an inactive one and reactivates it, "despawn" deactivates and returns it. You never allocate in the loop, so there's no garbage to collect and no spike. Allocate once, reuse forever.</details>
3. Define **Entity**, **Component**, and **System**, and say how ECS differs from a MonoBehaviour per enemy.
   <details><summary>Answer</summary><strong>Entity</strong> = an id/handle, nothing more. <strong>Component</strong> = pure <em>data</em>, no logic (Position, Velocity, Health). <strong>System</strong> = <em>behavior</em> that runs in bulk over all entities having the components it needs (MovementSystem iterates every Position+Velocity once). A MonoBehaviour-per-enemy couples data and behavior on each object and runs a virtual `Update()` per object — scattered in memory, cache-hostile, hard to batch. ECS splits data from behavior and processes contiguous data in tight loops — cache-friendly, parallelizable, and exactly what the profiler rewards at high entity counts.</details>
4. When do you choose **binary vs JSON** for a save, and why must saves be **versioned**?
   <details><summary>Answer</summary><strong>JSON</strong>: human-readable, debuggable, easy to diff/edit — good for config and dev iteration — but bigger and slower to parse. <strong>Binary</strong>: compact and fast — good for large/shipping save state — but opaque. Choose per use: small/inspectable → JSON; large/perf-critical → binary. <strong>Versioning</strong>: a save is a snapshot of your data schema at write time. Change the schema in a patch and old saves no longer match the loader — crash or corruption. Stamping each save with a version lets the loader run <strong>migrations</strong> to upgrade old saves, so players' saves survive updates.</details>
5. What are the **engine layers**, which way do dependencies point, and why have a deliberate **bootstrap order**?
   <details><summary>Answer</summary>Layers: <strong>core</strong> (engine-agnostic fundamentals — math, ECS, pooling, serialization), <strong>platform</strong> (engine/OS glue — Unity input, rendering, file I/O), <strong>gameplay</strong> (Ashfall's rules — combat, dungeon, enemies). Dependencies point <strong>downward only</strong>: gameplay → core; core depends on nothing game-specific. If core reaches up into gameplay you get an untestable tangle. <strong>Bootstrap order</strong> matters because subsystems must initialize in dependency order (save before load, input before gameplay, services registered before anyone asks for them) — a deliberate startup sequence rather than random `Awake()` timing — or you hit null-reference races on launch. Clean layers + ordered boot are what let W10 build and deploy Ashfall without surprises.</details>

---

## 🏗️ Boss readiness
- [ ] Ashfall can **spawn and sustain 1000+ entities** (bullets and enemies) alive at once
- [ ] The frame rate holds a **stable, locked 60 FPS** (~16.6 ms/frame) with all those entities active
- [ ] The hot paths are **data-oriented** (struct-of-arrays, cache-friendly) and the entities run through the **ECS-lite** core
- [ ] **Object pooling** drives spawning — no `new`/`Instantiate` in the per-frame loop
- [ ] Per-frame **GC allocation is ~0 B**, and I can **prove it on the profiler** (flat GC line, no spikes)
- [ ] I can explain which technique buys what (SoA → cache · ECS → bulk · pooling → zero alloc) and read the profiler to back it up
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed Side Quest 1 — Job/Worker-Thread Experiment (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Memory-Profiler Audit (+50 XP)

---

> All checked? → [🏗️ Face the Boss Battle: 1000 Entities at 60 FPS](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
