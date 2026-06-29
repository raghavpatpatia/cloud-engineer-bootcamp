# ✅ World 7 — Readiness Checklist

Before you face "Atmosphere Pass" and unlock World 8, make sure all of this is true. The boss assumes *every* skill below — it's one room that exercises the whole world at once: Ashfall on URP with an audited draw-call budget, a hit-flash and dissolve shader, dynamic 2D lighting with shadows, and impact particles + post-processing + screen shake / hit-stop — all holding a stable 60 FPS. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [🎨 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — The Rendering Pipeline:** I understand the GPU pipeline (vertices → fragments), draw calls, and batching — and I put Ashfall on URP and audited its draw calls
- [ ] **L2 — Shaders & Materials:** I understand vertex/fragment shaders, UVs, and material properties — and I built a hit-flash and a dissolve shader (Shader Graph + a hand-written HLSL example)
- [ ] **L3 — 2D Lighting & Shadows:** I understand 2D lights, normal maps, shadow casters, and emissive glow — and I lit the dungeon with torch/player lighting for mood
- [ ] **L4 — Particles, Post-Processing & Juice:** I understand particle systems, a post stack (bloom/vignette/chromatic aberration), screen shake, and hit-stop — and I added impact VFX + post + camera shake

## 🧰 What I've built / set up
- [ ] Ashfall rendering on **URP** with a known **draw-call / framerate budget**, in `Assets/Rendering` (URP assets + renderer)
- [ ] A **hit-flash** shader (white-out on damage) and a **dissolve** shader (burn-away on death), in `Assets/Shaders` — wired to the W5 damage / death events
- [ ] **Dynamic 2D lighting** — global light dimmed, torch/point lights, a player glow, and **shadow casters** on walls/pillars — in the dungeon scene
- [ ] **Impact particles**, a **post-processing volume** (bloom + vignette + a touch of chromatic aberration), and **screen shake / hit-stop**, in `Assets/VFX`
- [ ] All of it holding a **stable 60 FPS** (measured), committed and pushed

## 🧠 Skills I can do without looking up
- [ ] Explain the GPU pipeline (vertex → fragment), what a draw call costs, and how batching/atlasing cuts the count
- [ ] Write a fragment shader that flashes a sprite white via a `_FlashAmount` property, and one that dissolves via a noise threshold + `clip()`
- [ ] Light a 2D scene for mood with a dimmed global light, point lights, and shadow casters
- [ ] Layer particles + a post stack + screen shake + hit-stop so a hit *feels* like it lands
- [ ] Open the profiler / Frame Debugger, read draw calls and frame time, and cut back under budget without losing the look

---

## 🔎 Self-test (from memory, no peeking)

1. What happens in the **vertex** stage vs the **fragment** stage of the GPU pipeline, and which one runs your hit-flash and dissolve?
   <details><summary>Answer</summary>The <strong>vertex</strong> stage runs once per vertex and transforms geometry positions into clip/screen space (the *shape* and *where*). The <strong>fragment</strong> (pixel) stage runs once per covered pixel and computes its final color (texture sample + lighting + effects). Your <strong>hit-flash and dissolve are fragment shaders</strong> — they decide each pixel's color (lerp to white) or whether it survives (<code>clip()</code> against a noise threshold). Vertices = where; fragments = what color.</details>
2. What is a **draw call**, why does the count drive your framerate, and what reduces it in a 2D game?
   <details><summary>Answer</summary>A draw call is one CPU→GPU command to draw a batch of geometry with a given material/state; each carries CPU overhead, so *many* small ones bottleneck the CPU and drop frames. <strong>Batching</strong> reduces the count — the SRP Batcher, shared materials, and especially a <strong>sprite atlas</strong> (one texture for many sprites) so sprites sharing a material+texture merge into one call. Vary per-object properties with a <strong>MaterialPropertyBlock</strong> so you don't break the batch with new materials.</details>
3. How does a **hit-flash** shader work, and how does a **dissolve** shader make pixels vanish at different times?
   <details><summary>Answer</summary><strong>Hit-flash:</strong> sample the texture, then <code>lerp</code> the color toward white by a <code>_FlashAmount</code> (0→1) property while keeping the texture's alpha; code spikes <code>_FlashAmount</code> to 1 on a damage event and decays it over a few frames. <strong>Dissolve:</strong> sample a <strong>noise texture</strong> per pixel for a 0–1 threshold, compare to an animated <code>_DissolveAmount</code> uniform, and <code>clip()</code>/discard pixels below it — so a ragged set of pixels disappears as the amount climbs 0→1, with an HDR emissive edge near the cutoff for the glowing burn rim.</details>
4. What turns a flat, uniformly bright 2D dungeon into a moody, torch-lit scene with depth?
   <details><summary>Answer</summary>Dim the <strong>global/ambient 2D light</strong> so the room is dark, then add <strong>point/spot Light 2D</strong> sources for torches and a glow on the player, and put <strong>shadow casters</strong> on the walls/pillars so those lights actually cast shadows. The 2D renderer composites the lights over the sprites (optionally using <strong>normal maps</strong> for surface relief and <strong>emissive</strong> for self-lit glow). Mood comes from the *contrast* — bright pools of torchlight against dark — not from more brightness.</details>
5. Name three "juice" techniques and explain why **hit-stop** makes a hit feel powerful without changing the damage number.
   <details><summary>Answer</summary>Examples: <strong>impact particles</strong>, <strong>screen shake</strong>, <strong>hit-stop</strong>, a <strong>hit-flash</strong>, and a <strong>post stack</strong> (bloom/vignette/chromatic aberration). <strong>Hit-stop</strong> is a brief freeze (a few frames, often a momentary <code>Time.timeScale</code> dip) at the instant of impact — the action stops dead, then resumes, so the brain registers a *collision* and the hit reads as weight/force. It's pure <strong>feedback</strong>: the same damage value feels far stronger with hit-stop, flash, shake, and particles than without.</details>

---

## 🎨 Boss readiness
- [ ] One dungeon room is **lit for mood** — dimmed global light, torch/point lights, a player glow, and **shadow casters** giving real depth
- [ ] Struck enemies **flash white** (hit-flash shader) and dying enemies **dissolve** (burn-away shader), wired to the W5 damage/death events
- [ ] Hits land with **impact particles**, a **post-processing stack** (bloom/vignette/chromatic aberration), and **screen shake + hit-stop**
- [ ] The whole atmosphere pass holds a **stable 60 FPS** — and I **checked the draw calls / frame time** to prove it
- [ ] Key knobs are **data** (light intensities, flash/dissolve durations, shake amplitude, post settings) — I can retune the feel without editing code
- [ ] I can explain which layer owns each effect (pipeline → shader → light → juice) and where my framerate budget went
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed Side Quest 1 — Enemy Dissolve Shader (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Draw-Call Budget Audit (+50 XP)

---

> All checked? → [🎨 Face the Boss Battle: Atmosphere Pass](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
