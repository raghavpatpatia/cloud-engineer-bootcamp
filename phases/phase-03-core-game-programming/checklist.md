# ✅ World 3 — Readiness Checklist

Before you face "The Playable Slice" and unlock World 4, make sure all of this is true. The boss assumes *every* skill below — it's one playable vertical slice that exercises the whole world at once: an input layer, a physics controller, collision + triggers, a follow camera, and a save file that survives a restart. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — The Input System:** I can map devices to *actions* (`Move`/`Aim`/`Fire`), explain polling vs events, and rebind — and I built Ashfall's device-agnostic input layer
- [ ] **L2 — Player Controller & Physics:** I understand `Rigidbody2D` vs transform, the fixed timestep, and forces vs velocity — and I built a top-down `PlayerController` driving the W2 `Mover`
- [ ] **L3 — Collision & Triggers:** I can use colliders, layers, the collision matrix, and raycasts, and tell collision from trigger — and I built walls that stop the player and pickups that fire on overlap
- [ ] **L4 — Camera Systems:** I can build a smoothed follow camera with a deadzone, clamp it to bounds, and convert screen↔world — and I built Ashfall's top-down follow camera
- [ ] **L5 — Saving & Loading:** I understand serialization, JSON, and `persistentDataPath`, and the save/load lifecycle — and I built a `SaveSystem` persisting player position + HP

## 🧰 What I've built / set up
- [ ] An `InputReader` exposing `Move`/`Aim`/`Fire` actions, decoupled from any device, in `Assets/Scripts/Input`
- [ ] A `PlayerController` on a `Rigidbody2D` that moves in `FixedUpdate` via the W2 `Mover`, in `Assets/Scripts/Player`
- [ ] Wall colliders that stop the player and **trigger** pickups that fire on overlap, with a sane layer collision matrix
- [ ] A `FollowCamera` (smoothed in `LateUpdate`, deadzone, clamped to room bounds) in `Assets/Scripts/Camera`
- [ ] A `SaveSystem` writing/reading JSON to `Application.persistentDataPath` (player position + HP)
- [ ] All of it committed on branches and merged/pushed

## 🧠 Skills I can do without looking up
- [ ] Explain why the controller depends on *actions*, not a keyboard
- [ ] Choose polling vs an event for a given input (move vs fire)
- [ ] Move a `Rigidbody2D` correctly (velocity/`MovePosition` in `FixedUpdate`, not transform teleport)
- [ ] Tell when to use a collision vs a trigger, and debug an overlap that won't fire
- [ ] Make a follow camera that doesn't judder (LateUpdate + framerate-independent smoothing) and clamp it to bounds
- [ ] Serialize game state to JSON and load it back from `persistentDataPath`

---

## 🔎 Self-test (from memory, no peeking)

1. Why feed both the keyboard and a gamepad through one `Move` action instead of reading the keyboard in the controller?
   <details><summary>Answer</summary>The controller should depend on <strong>intent</strong> ("move this way"), not a device. A single action layer means adding a pad or rebinding keys never touches gameplay code — the same decoupling principle as W1's architecture.</details>
2. You move a `Rigidbody2D` with `transform.position += dir * speed` and it tunnels through walls. Why, and the fix?
   <details><summary>Answer</summary>Teleporting the transform skips the physics solver, so collisions aren't resolved. Drive the body <em>through</em> physics — set <code>rb.velocity</code> (or call <code>rb.MovePosition</code>) in <code>FixedUpdate</code> so the solver sees the motion.</details>
3. A pickup should disappear when touched but a wall should stop you. Which uses a trigger, which a collision, and why?
   <details><summary>Answer</summary>The <strong>pickup is a trigger</strong> (<code>Is Trigger</code> on): it overlaps without blocking and fires <code>OnTriggerEnter2D</code>. The <strong>wall is a collision</strong>: a solid collider that pushes the player back and fires <code>OnCollisionEnter2D</code>. Pickups shouldn't shove the player; walls must.</details>
4. Your follow camera judders. Where should follow code run and how should it move toward the player?
   <details><summary>Answer</summary>In <strong><code>LateUpdate</code></strong> — after physics has moved the player this frame — and toward the target with a <strong>framerate-independent</strong> lerp (e.g. <code>Lerp(cam, target, 1 - Exp(-k*deltaTime))</code> from W2), not a per-frame fixed fraction.</details>
5. Where do you write the save file, and what kind of class does Unity's `JsonUtility` actually serialize?
   <details><summary>Answer</summary>To <strong><code>Application.persistentDataPath</code></strong> (the per-user, writable, platform-correct location). <code>JsonUtility</code> serializes a <code>[System.Serializable]</code> plain class's <strong>public fields</strong> (or <code>[SerializeField]</code> private ones) — not properties.</details>

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — Coyote-Time Jump Feel (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Screen-Shake on Hit (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Playable Slice](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
