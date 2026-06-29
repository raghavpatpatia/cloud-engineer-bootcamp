# ✅ World 6 — Readiness Checklist

Before you face "The Ashen Warden" and unlock World 7, make sure all of this is true. The boss assumes *every* skill below — it's one multi-phase fight that exercises the whole world at once: a clean FSM, perception that drives transitions, steering layered on A\* paths, a behavior tree, and utility AI choosing telegraphed attacks across phases. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Finite State Machines:** I understand states, transitions, and the clean State pattern (vs `if`-soup) — and I built an enemy FSM (Patrol / Chase / Attack / Flee)
- [ ] **L2 — Perception & Sensing:** I understand vision cones (W2 dot product), line-of-sight raycasts, and hearing/aggro — and I built enemy detection that feeds the FSM's transitions
- [ ] **L3 — Steering & Navigation:** I understand seek / flee / arrive / avoid layered on W4 A\* paths — and I built enemy movement that follows a route *and* dodges obstacles
- [ ] **L4 — Behavior Trees:** I understand selectors, sequences, and decorators for composable, designer-readable AI — and I built a BT-driven elite enemy
- [ ] **L5 — Boss Design & Utility AI:** I understand phases, telegraphed attack patterns, and utility scoring — and I built the Ashen Warden's phase logic and decision scoring

## 🧰 What I've built / set up
- [ ] An enemy **FSM** (Patrol / Chase / Attack / Flee) with clean transitions, in `Assets/Scripts/AI/FSM`
- [ ] A **perception** system — vision cone + line-of-sight raycast + hearing/aggro — that triggers FSM transitions, in `Assets/Scripts/AI/Perception`
- [ ] **Steering** behaviors (seek / flee / arrive / avoid) layered on the W4 A\* `Pathfinder`, in `Assets/Scripts/AI/Steering`
- [ ] A **behavior tree** (selector / sequence / decorator) driving an elite enemy, in `Assets/Scripts/AI/BehaviorTree`
- [ ] A multi-phase **boss** (the Ashen Warden) with telegraphed attacks chosen by **utility AI**, in `Assets/Scripts/AI/Boss`
- [ ] All of it using W5 combat against the player and persisted/committed as appropriate, and pushed

## 🧠 Skills I can do without looking up
- [ ] Model an enemy as states + transitions and justify why it beats nested-`if` logic
- [ ] Detect the player with a vision cone (dot product), block sight with a line-of-sight raycast, and feed the result into the FSM
- [ ] Combine seek/arrive/avoid steering forces on top of an A\* path so movement is smooth and corner-safe
- [ ] Compose AI as a behavior tree (selector = OR, sequence = AND, decorators add conditions) and say why it scales past an FSM
- [ ] Score candidate actions with utility AI and pick the best, and explain why every boss attack must be telegraphed

---

## 🔎 Self-test (from memory, no peeking)

1. What are the two core pieces of an FSM, and why does it beat a 200-line `Update()` full of nested `if`s?
   <details><summary>Answer</summary><strong>States</strong> (Patrol/Chase/Attack/Flee — each owns its behavior via Enter/Tick/Exit) and <strong>transitions</strong> (the conditions that switch between them). Only one state is active at a time, so each state's code stays small. Nested-<code>if</code> logic grows combinatorially as conditions multiply; an FSM stays linear — one block per state. The machine just holds the current state and runs its Tick.</details>
2. An enemy should only see the player in a 90° cone in front of it, and walls should block sight. How do you implement both checks?
   <details><summary>Answer</summary><strong>Cone:</strong> normalize the facing vector and the (player − enemy) direction, take the <strong>dot product</strong>, and require <code>dot >= cos(45°)</code> (dot of unit vectors = cosine of the angle — the W2 math). <strong>Line-of-sight:</strong> if the cone passes, fire a <code>Raycast</code> from enemy to player against the wall layer; if it hits a wall first, sight is blocked. Cone = facing; raycast = nothing solid in between.</details>
3. Once detected, why layer steering on the A\* path instead of moving node-to-node? Name two steering behaviors and what they do.
   <details><summary>Answer</summary>Raw node-to-node movement snaps, clips corners, and ignores other movers. <strong>Steering</strong> produces smooth, force-based movement along the route: <code>seek</code> drives toward the next waypoint, <code>arrive</code> eases to a stop inside a slowing radius, <code>avoid</code> pushes off obstacles/other enemies, <code>flee</code> steers directly away. A\* picks the route; steering walks it like something alive.</details>
4. In a behavior tree, what's the difference between a Selector and a Sequence, and what does a decorator add?
   <details><summary>Answer</summary>A <strong>Sequence</strong> is AND — runs children in order, fails on the first failure (A then B then C). A <strong>Selector</strong> is OR — tries children until one succeeds (A else B else C). A <strong>decorator</strong> wraps a single child to modify it — invert its result, gate it behind a cooldown, repeat it, or add a condition — without introducing a new state. Trees scale because you add a branch, not O(n²) FSM edges.</details>
5. The boss can slam, dash, or fire a volley. How does utility AI choose, and why must the chosen attack be telegraphed?
   <details><summary>Answer</summary>Each action has a <strong>scoring function</strong> over the situation (distance, boss HP, cooldown ready, player exposure); evaluate all candidates and pick the <strong>highest score</strong> (optionally weighted-random among the top) — smarter than a fixed rotation, more authored than pure random. Every attack must be <strong>telegraphed</strong> (wind-up, ground marker, a beat of delay) so the fight is fair — it gives the player a readable window to dodge or i-frame (W5) through. No telegraph = cheap, random-feeling damage.</details>

---

## 👹 Boss readiness
- [ ] My boss **perceives** the player (vision cone + line-of-sight) and reacts when sight is gained or lost
- [ ] My boss **paths and steers** to the player (A\* route + seek/avoid steering), no wall-clipping
- [ ] My boss **switches behaviors via a tree** (or FSM phases) — its conduct changes meaningfully across phases
- [ ] My boss uses **utility AI** to score and choose among multiple attacks, not a fixed rotation
- [ ] Every boss attack is **telegraphed** with a fair, dodgeable wind-up window
- [ ] The boss has **multiple phases** that escalate (new attacks / faster / different behavior) as HP drops
- [ ] The fight **uses W5 combat** — real damage pipeline, i-frames on the player, the boss is `IDamageable`
- [ ] It's tunable as **data** where it should be (cone angle, attack scores, phase thresholds), no recompile to retune
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — Flocking Swarm Enemy (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Stealth Alert Propagation (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Ashen Warden](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
