# ✅ World 2 — Readiness Checklist

Before you face "The Aiming Reticle" and unlock World 3, make sure all of this is true. The boss assumes *every* skill below — it's one feature that exercises the whole world at once: vectors, dot/cross, `atan2`, lerp/slerp, and `Time.deltaTime`. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Vectors & Coordinate Spaces:** I can explain position vs direction vs displacement, find magnitude, and normalize — and I built an equal-speed movement direction from input
- [ ] **L2 — Dot & Cross Products:** I can use the dot product for facing/FOV and the cross product for sidedness — and I built an "is the player in front of me?" vision check
- [ ] **L3 — Trigonometry & Rotation:** I know radians vs degrees and use `atan2` to aim at a point — and I built aim-angle-to-mouse plus a spread
- [ ] **L4 — Interpolation & Easing:** I can lerp/slerp with easing **framerate-independently** — and I built smooth camera follow and smoothed aim
- [ ] **L5 — Transforms & Delta Time:** I understand transforms (position/rotation/scale) and `* Time.deltaTime` — and I folded it all into a reusable `Mover`

## 🧰 What I've built / set up
- [ ] An equal-speed 8-directional movement direction (input `.normalized * speed`) in `Assets/Scripts/Movement`
- [ ] A `Vision` check (FOV cone via dot product + left/right via cross product) in `Assets/Scripts/AI`
- [ ] `AimAtMouse` (screen→world, `atan2` to an angle) and a facing-aware `SpreadShooter` in `Assets/Scripts/Combat`
- [ ] A `SmoothAim` and a framerate-independent `CameraFollow` using lerp/slerp
- [ ] One reusable `Mover` that the player (and later enemies) drive, all motion `* Time.deltaTime`
- [ ] All of it committed on branches and merged/pushed

## 🧠 Skills I can do without looking up
- [ ] Normalize a direction and explain why diagonal movement is faster without it
- [ ] Read a dot product's sign to answer "in front / to the side / behind"
- [ ] Use the 2D cross product's sign to decide "left or right"
- [ ] Turn a direction into an aim angle with `atan2` (and remember it's radians)
- [ ] Write a lerp that converges the *same* at 30 fps and 200 fps
- [ ] Explain why every per-frame motion is multiplied by `Time.deltaTime`

---

## 🔎 Self-test (from memory, no peeking)

1. Input is `(1, 1)`. Why does the player move faster diagonally, and what's the fix?
   <details><summary>Answer</summary>`(1,1)` has length √2 ≈ 1.41, not 1, so applying speed to it moves ~41% faster. <strong>Normalize</strong> the input first: `input.normalized * speed * Time.deltaTime`.</details>
2. `Vector2.Dot(forwardN, toTargetN)` returns `-0.3`. Where is the target, and how do you know?
   <details><summary>Answer</summary><strong>Behind</strong> the entity. With both vectors normalized, the dot equals cos(angle); a negative value means the angle exceeds 90°, so it's behind the forward direction.</details>
3. You need to know whether to turn left or right to aim at a target. Dot or cross — and why?
   <details><summary>Answer</summary>The <strong>cross product</strong> (`forward.x*to.y - forward.y*to.x`). Its <em>sign</em> tells you which side the target is on (left vs right); the dot only tells you how aligned/in-front it is, not which way to turn.</details>
4. Write the call that gives the angle (degrees) from this object to the mouse world point `m`.
   <details><summary>Answer</summary><code>float deg = Mathf.Atan2(m.y - transform.position.y, m.x - transform.position.x) * Mathf.Rad2Deg;</code> — `Atan2(dy, dx)` picks the correct quadrant; convert radians→degrees for `Quaternion.Euler`.</details>
5. `cam = Lerp(cam, player, 0.1f)` every frame looks smooth at 60 fps but snappier at 144 fps. Why, and the fix?
   <details><summary>Answer</summary>It applies 10% per <em>frame</em>, so more frames = faster convergence — not framerate-independent. Fix: `Lerp(cam, player, 1 - Mathf.Exp(-k * Time.deltaTime))` so the rate is per <em>second</em>.</details>

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — The Homing Missile (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — The Radar Blip (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Aiming Reticle](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
