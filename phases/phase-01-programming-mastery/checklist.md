# ✅ World 1 — Readiness Checklist

Before you face "Refactor the Spaghetti" and unlock World 2, make sure all of this is true. The boss assumes *every* skill below — it's one task that exercises the whole world at once. If a box is empty, revisit that lesson.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Types & Memory:** I can predict value-copy vs reference-copy and explain GC frame hitches
- [ ] **L2 — OOP & Composition:** I can build an entity from components instead of an inheritance tree
- [ ] **L3 — Interfaces & SOLID:** `IDamageable`/`IInteractable` exist; I can name all five SOLID principles
- [ ] **L4 — Events & Observer:** `GameEvents` bus exists; systems react by subscribing and unsubscribe cleanly
- [ ] **L5 — Managers & State:** a `GameManager` singleton + FSM drives Menu/Playing/Paused/GameOver

## 🧰 What I've built / set up
- [ ] `Stats` (struct) and `Health` (class) in `Assets/Scripts/Core`
- [ ] A Player GameObject assembled purely from `Health` + `Mover` components (no entity subclass)
- [ ] `IDamageable`/`IInteractable` contracts; `Attacker` depends on the interface, not concrete types
- [ ] A central `GameEvents` EventBus with `HealthBarHUD` and `ScoreSystem` decoupled through it
- [ ] A `GameManager` (with duplicate guard + `DontDestroyOnLoad`) and a working state machine
- [ ] All of it committed on branches and merged/pushed to `main`

## 🧠 Skills I can do without looking up
- [ ] Decide struct vs class for a given piece of game data and justify it
- [ ] Refactor a deep inheritance tree into composed components
- [ ] Spot which SOLID principle a smelly class violates and fix it
- [ ] Wire two systems together with an event so neither references the other
- [ ] Unsubscribe correctly to avoid leaks/double-fires after a scene reload
- [ ] Model app flow as an FSM and explain why scattered booleans are a bug factory

---

## 🔎 Self-test (from memory, no peeking)

1. You write `Stats b = a; b.hp = 1;` — is `a.hp` changed? What if `Stats` were a `class`?
   <details><summary>Answer</summary><strong>No</strong>, a struct copies the data, so <code>a.hp</code> is unchanged. As a <strong>class</strong>, <code>b</code> and <code>a</code> share one heap object, so <code>a.hp</code> would also be 1.</details>
2. Why does the studio "favor composition over inheritance," and how does Unity's component model embody it?
   <details><summary>Answer</summary>Inheritance forces one rigid is-a tree that can't express mixed capabilities; composition snaps independent parts together. A Unity <code>GameObject</code> is a container you give abilities to via <code>AddComponent</code> — that's composition.</details>
3. A `Projectile` should deal damage to enemies, barrels, and walls. What lets it not know about any of those types?
   <details><summary>Answer</summary>An <strong>interface</strong> (<code>IDamageable</code>) — the projectile depends on the contract (Dependency Inversion), so new damageable types need zero changes to it (Open/Closed).</details>
4. The HUD logs twice per hit after you reload the scene. Cause and fix?
   <details><summary>Answer</summary>The old subscription was never removed (static events outlive scenes), so two handlers fire. Fix: <code>+=</code> in <code>OnEnable</code>, <code>-=</code> in <code>OnDisable</code>, using a named handler.</details>
5. Why model game flow as an `enum` FSM instead of `bool isPaused`, `bool isDead`, …?
   <details><summary>Answer</summary>Scattered booleans allow impossible combos (paused <em>and</em> dead) and scatter the rules. One <code>enum</code> state with defined transitions makes illegal states unrepresentable.</details>

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — The Pooling Patch (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — The Achievement Listener (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: Refactor the Spaghetti](boss-battle.md)

[← World Home](README.md)
