# ✅ World 12 — The Ultimate Ship-Readiness Checklist

This is the last checklist of the bootcamp. Before you face "Launch Day" and graduate, make sure *every* box below is true — because the boss assumes all three milestones at once: a fully integrated vertical slice, polished to a stable 60 FPS, then built, deployed, documented, and tagged `v1.0` for the public. This isn't a "you can revisit a lesson" checklist; it's a **launch checklist**. An empty box here is a thing that breaks on launch day. Don't ship around it — fix it.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👑 Boss Battle](boss-battle.md)

---

## 🧩 Milestone 1 — Systems & Architecture (integration)
- [ ] **Every system is integrated** into ONE running vertical slice — architecture (W1), math (W2), player/camera/save (W3), dungeon gen + A* (W4), items/combat/loot (W5), enemy AI + boss (W6), rendering/juice (W7), co-op (W8), ECS-lite engine (W9), CI/CD + cloud (W10) — no orphaned systems, no dead wires
- [ ] The slice runs **end to end**: start → enter a generated dungeon → fight enemies and the Ashen Warden → loot/grow → win/lose → save, with no broken handoff between systems
- [ ] It all sits under **one clean architecture** — managers/events/interfaces from W1, layered subsystems from W9 — not a tangle of special cases bolted together
- [ ] The **feature set is LOCKED** — scope is frozen, a v1.1 backlog holds everything new, and nothing crosses the line into the ship phase

## 💎 Milestone 2 — Optimization & Polish (shippable quality)
- [ ] A **profiling pass** holds a **stable 60 FPS** — the *worst* frames (not just the average) stay under the ~16.6 ms budget; GC spikes, heavy spawns, and unbatched draws are handled
- [ ] **Game feel** is in: hit-stop/screen shake, impact VFX/particles, the W7 polish reading on every meaningful action
- [ ] **UX is finished** — readable HUD, working menus (start/pause/death/restart), clear feedback, no first-frame hitches or placeholder text
- [ ] **Audio** is present — SFX on actions and a music/ambience bed (free assets), mixed so nothing clips
- [ ] The **bug list is clear** of anything that breaks a run or reads as unfinished

## 🚀 Milestone 3 — Build, Deploy & Document (release)
- [ ] **Final builds** are produced through the **CI/CD pipeline** (W10) — green, automated, artifacts out the other end — not hand-cranked
- [ ] The **co-op server is LIVE in the cloud** — deployed to the Terraform-defined cluster (W10), health-checked, monitored, reachable by a client that isn't on your laptop
- [ ] A **public release page** exists (GitHub Release and/or itch.io) where a logged-out stranger can find and download the game
- [ ] **Full documentation** is written — a complete **README** (what it is, how to install, how to play), a **case study** (what you built + the engineering decisions), and a **trailer** (gameplay footage)
- [ ] A **`v1.0` git tag** is cut and a **GitHub Release** carries the built artifacts — the exact thing that shipped is frozen and downloadable
- [ ] The **billing alarm is armed** and you know the cost/teardown story for the live server (W10) — shipping doesn't mean a surprise bill

## 🧠 Skills I can do without looking up
- [ ] Explain what a **vertical slice** is and why you ship one instead of "the whole game"
- [ ] Explain why **locking scope** comes before polishing, and the difference between "it works" and "it's polished"
- [ ] State the **60 FPS frame budget** (~16.6 ms) and why the *worst* frame matters more than the average
- [ ] Explain why a shipped game needs **docs + a release tag**, not just a build
- [ ] Run a **launch checklist** and explain why "works on my machine" is the failure mode launches die on

---

## 🔎 From-memory self-test — the whole bootcamp (no peeking)

Five questions spanning Worlds 0–12. If you can answer these cold, you've earned the title.

1. **(W1–W2)** Why do we favor **composition over inheritance** and decouple systems with **events**, and why must game movement use **`Time.deltaTime`**?
   <details><summary>Answer</summary><strong>Composition over inheritance</strong>: deep class hierarchies are rigid and fragile — a change high up ripples everywhere, and "is-a" relationships rarely survive contact with real features. Composing an entity from small components (Health, Mover, Inventory) lets you mix capabilities freely, which is exactly why engines use a component model. <strong>Events / the observer pattern</strong> decouple who-does-what from who-cares: combat can fire <code>OnPlayerDamaged</code> without knowing the UI, audio, and VFX are listening — so systems wire in without touching each other (the cure for spaghetti). <strong><code>Time.deltaTime</code></strong> makes motion <strong>framerate-independent</strong>: you multiply per-frame movement by the time the frame took, so the player travels the same distance per second whether running at 30 or 144 FPS. Without it, the game literally plays faster on faster hardware.</details>
2. **(W4)** What is **A\*** pathfinding, how does it relate to Dijkstra, and what makes a heuristic **admissible**?
   <details><summary>Answer</summary><strong>A\*</strong> finds the shortest path on a graph (the dungeon grid) by expanding nodes in order of <code>f = g + h</code>: <code>g</code> is the known cost from the start, <code>h</code> is a <em>heuristic</em> estimate of the cost remaining to the goal. It's <strong>Dijkstra plus a heuristic</strong> — Dijkstra is A* with <code>h = 0</code> (it explores blindly in all directions); the heuristic steers A* toward the goal, so it explores far fewer nodes for the same optimal answer. A heuristic is <strong>admissible</strong> if it <em>never overestimates</em> the true remaining cost (e.g. Manhattan distance on a 4-connected grid). Admissibility is what guarantees A* still returns the genuinely shortest path — overestimate and it may take a shortcut that isn't.</details>
3. **(W6)** When would you use an **FSM**, a **behavior tree**, and **utility AI**, and why does a boss combine them?
   <details><summary>Answer</summary>An <strong>FSM</strong> (states + transitions: Patrol/Chase/Attack) is simple and readable for a small number of clearly-distinct modes — perfect for a basic enemy, but it sprawls into unmanageable transition-soup as behavior grows. A <strong>behavior tree</strong> composes behavior from reusable selectors/sequences/decorators, so complex, designer-readable AI scales without an explosion of transitions — better for an elite enemy with many conditional actions. <strong>Utility AI</strong> <em>scores</em> candidate actions by context and picks the best, giving fluid, situational decisions rather than hard-coded branches. A <strong>boss</strong> combines them because it needs all three: an FSM for clean high-level <em>phases</em> (the Ashen Warden changes behavior at low HP), a BT for the structured attack patterns within a phase, and utility scoring to choose <em>which</em> attack fits the moment. The right tool per layer.</details>
4. **(W8–W9)** Why do networked games use **server authority**, and why does **data-oriented design + object pooling** beat naive OOP for thousands of entities?
   <details><summary>Answer</summary><strong>Server authority</strong> means the server holds the true game state and clients send <em>inputs</em>, not results — the server simulates and replicates back. It's the foundation of fairness and anti-cheat: a client can't simply declare "I hit you" or "I have 999 gold," because the authoritative server decides. Clients hide latency with <strong>prediction + reconciliation</strong> and smooth others with <strong>interpolation</strong>, but the server is the single source of truth. <strong>Data-oriented design</strong> stores components as <em>struct-of-arrays</em> so hot loops walk contiguous memory — the CPU cache loads neighbors you'll actually use next, instead of thrashing on pointer-chasing through scattered OOP objects. <strong>Object pooling</strong> reuses pre-allocated instances (bullets, enemies) instead of <code>new</code>/destroy every frame, which eliminates the per-frame allocations that trigger <strong>GC spikes</strong> — the stutters that blow your frame budget. Together they're how you hold 1000+ entities at a locked 60 FPS.</details>
5. **(W10–W12)** Walk the path from a **git push** to a **shipped, tagged `v1.0`** live in the cloud — naming what each stage owns.
   <details><summary>Answer</summary>A <strong>push</strong> triggers <strong>CI/CD</strong> (GitHub Actions), which <em>builds</em> the game/server and <em>runs the tests</em> — green or red automatically, killing "works on my machine." The pipeline <em>containerizes</em> the server and <em>pushes the tagged image</em> (commit SHA) to a <strong>registry</strong> — one portable unit, identical bytes everywhere. The cluster it deploys to is defined in <strong>Terraform</strong> (<code>plan</code>→<code>apply</code>): reproducible infra you can stand up <em>and tear down</em> from a file. <strong>Kubernetes</strong> runs the server as a <em>Deployment + Service</em> with <em>liveness/readiness probes</em> — self-healing, reachable, traffic-gated until ready. <strong>Monitoring</strong> (logs/metrics + an alert) means you find out when it breaks. Then the ship phase (W12): the slice is <em>integrated</em> (M1), <em>polished to 60 FPS</em> (M2), and <em>released</em> (M3) — final CI builds, a public release page, full docs, and a frozen <strong>`v1.0` tag + GitHub Release</strong> anyone can download. Each stage owns one job: CI = trusted automated build · registry = portable image · Terraform = reproducible infra · k8s = running + healthy · monitoring = you'll know when it breaks · the tag = the exact thing that shipped, frozen forever.</details>

---

## 👑 Boss readiness
- [ ] Ashfall is **one integrated vertical slice** — every system fits together and a full run plays end to end (M1)
- [ ] The slice is **polished to a stable 60 FPS** with game feel, finished UX, and audio — it reads as a *game*, not a demo (M2)
- [ ] **Final builds** come through CI/CD and the **co-op server is live in the cloud**, reachable by a client (M3)
- [ ] A **public release page**, a complete **README + case study + trailer**, and a **tagged `v1.0` GitHub release** all exist (M3)
- [ ] The **billing alarm is armed** and the live server's cost/teardown is understood — shipping safely, not expensively
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to *ship*, not tutorial my way through it

---

## 🎓 XP check
- [ ] I recorded XP for all 3 milestones in [PROGRESS.md](../../PROGRESS.md) (375 XP)
- [ ] (Optional) I completed Side Quest 1 — The Press Kit (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — The Post-Mortem (+50 XP)

---

> All checked? → [👑 Face the Final Boss: Launch Day](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
