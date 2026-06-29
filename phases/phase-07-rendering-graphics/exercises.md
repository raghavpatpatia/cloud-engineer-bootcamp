# 🏋️ World 7 — Exercises

Extra reps to make the *rendering & graphics* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "Atmosphere Pass" demands — understanding how the GPU draws, writing a fragment shader, lighting a scene for mood, layering juice, and keeping all of it inside a framerate budget. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [🎨 Boss Battle](boss-battle.md)

---

## Warm-ups (pipeline, shaders, lighting, juice, performance)

1. In one sentence each, what happens in the **vertex** stage vs the **fragment** stage of the GPU pipeline?
   <details><summary>Hint</summary>The <strong>vertex</strong> stage runs once per vertex — it transforms each vertex's position from object space into clip/screen space (the geometry's shape and where it lands on screen). The <strong>fragment</strong> (pixel) stage runs once per covered pixel — it computes the final color of each pixel the triangle covers (texture sample, lighting, your hit-flash/dissolve math). Vertices = where; fragments = what color.</details>
2. What *is* a "draw call," and why is the count the number Lena cares about?
   <details><summary>Hint</summary>A draw call is one command from the CPU telling the GPU to draw a batch of geometry with a given material/state. Each one has CPU overhead (state setup), so *many* small draw calls bottleneck the CPU and tank framerate even when the GPU is idle. Fewer, bigger batches = more FPS. It's the cheapest single metric for "am I about to drop frames."</details>
3. Two sprites use the same texture and material but render as two draw calls. What's the fix, and why does it work?
   <details><summary>Hint</summary><strong>Batching</strong> — SRP Batcher / dynamic batching / a shared sprite atlas. Sprites that share a material *and* texture can be merged into one draw call. The win is fewer CPU→GPU state changes; that's why an atlas (one texture for many sprites) is the classic 2D performance move. Same material + same texture = batchable.</details>
4. You change a sprite's `_Color` per-instance and batching breaks. Why, and what preserves it?
   <details><summary>Hint</summary>A different material *instance* (or a per-renderer property that forces a unique material) breaks the batch — each unique material/state is its own draw call. Use a <strong>MaterialPropertyBlock</strong> (or the SRP Batcher's per-object property buffer) to vary a property without instantiating a new material, so the batch holds.</details>
5. Your hit-flash makes the whole sprite solid white for one frame. Conceptually, what does the fragment shader do?
   <details><summary>Hint</summary>Sample the sprite texture as normal, then <code>lerp</code> toward white by a <code>_FlashAmount</code> property (0 = normal, 1 = full white), preserving the texture's alpha so the silhouette stays. Code drives <code>_FlashAmount</code> to 1 on the damage event and back to 0 over a few frames. The shader is dumb; the <em>timing</em> is gameplay.</details>
6. A dissolve shader needs each pixel to disappear at a different time. What drives the per-pixel cutoff?
   <details><summary>Hint</summary>A <strong>noise texture</strong> (or procedural noise) sampled per fragment gives each pixel a threshold value 0–1. Compare it to a <code>_DissolveAmount</code> uniform and <code>clip()</code> / discard pixels whose noise value is below the threshold. As <code>_DissolveAmount</code> animates 0→1, more pixels cross the cutoff and vanish — a ragged burn-away instead of a uniform fade. Add an emissive "edge" near the cutoff for the glowing rim.</details>
7. Your 2D dungeon is uniformly bright. What two pieces turn it into a moody, torch-lit scene?
   <details><summary>Hint</summary>A <strong>Light 2D</strong> setup (global light dimmed down + point/spot lights for torches and a glow on the player) and <strong>shadow casters</strong> on the walls/pillars so the lights actually cast shadows. The 2D renderer composites the lights; the shadow casters give depth. Lower the ambient/global light so the torches *read*.</details>
8. What's the difference between **bloom**, **vignette**, and **chromatic aberration** in a post stack, and what's each *for*?
   <details><summary>Hint</summary><strong>Bloom</strong> makes bright/emissive areas glow and bleed light (sells torches, magic, hits). <strong>Vignette</strong> darkens the screen edges to focus the eye toward the center (mood + framing). <strong>Chromatic aberration</strong> splits color channels slightly at the edges (a subtle "lens" feel — easy to overdo). Post-processing is a full-screen pass after the scene renders; it's flavor on top, used sparingly.</details>
9. What is **hit-stop**, and why does it make a hit feel more powerful than a bigger number ever could?
   <details><summary>Hint</summary>Hit-stop is a tiny freeze (a few frames, often via a brief <code>Time.timeScale</code> drop) at the moment of impact. It makes the brain register a *collision* — the action stops dead, then resumes — so the hit reads as weight/force, not just damage. It's <strong>feedback</strong>: the same hit feels twice as strong with hit-stop, flash, particles, and shake than without, with zero change to the damage value.</details>
10. You added lights and particles and the framerate dropped. What do you open *first*, and what are you looking for?
    <details><summary>Hint</summary>The <strong>Stats overlay / Frame Debugger / Profiler</strong>. You're looking for the draw-call (batch) count, the number of real-time lights, overdraw from overlapping transparent particles, and whether the frame is CPU- or GPU-bound. Measure *which* addition cost the frame, then fix that one — don't guess. "It dropped frames, so it doesn't go in" is Lena's rule; the profiler tells you what to cut.</details>

---

## 🌟 Side Quest 1 — Enemy Dissolve Shader (+50 XP)

Prove you can write a real fragment shader, not just wire a graph. Build a **dissolve** effect so a dying enemy *burns away* — pixels vanish along a noise threshold with a glowing edge — instead of popping out of existence. Drive it from the W5/W6 death event so it fires on every real kill.

**Requirements:**
1. Write a dissolve shader (Shader Graph *or* hand-written HLSL — bonus for both) with a `_DissolveAmount` property (0 = whole, 1 = gone) and a noise texture driving the per-pixel cutoff via `clip()` / discard.
2. Add a **glowing emissive edge** near the dissolve threshold (an HDR color, so bloom makes it glow) so the burn reads as fire/disintegration, not a hole.
3. On enemy death, animate `_DissolveAmount` 0→1 over ~0.4s, *then* despawn/pool the object — the visual must finish before it disappears.
4. Keep it batch-friendly: drive `_DissolveAmount` via a `MaterialPropertyBlock` so animating one enemy doesn't break batching for the rest.

```
Test: kill an enemy. Instead of vanishing, it burns away from a ragged
noise edge with a glowing rim over ~0.4s, then pools out. Kill five at
once → all dissolve independently, framerate holds, draw calls don't spike.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```hlsl
// Fragment of an unlit/sprite dissolve shader (sketch).
// Properties: _MainTex, _NoiseTex, _DissolveAmount (0..1), _EdgeColor (HDR), _EdgeWidth
fixed4 frag (v2f i) : SV_Target
{
    fixed4 col   = tex2D(_MainTex, i.uv);
    float  noise = tex2D(_NoiseTex, i.uv).r;          // per-pixel threshold 0..1

    // Pixels whose noise is below the dissolve amount are cut away.
    clip(noise - _DissolveAmount);                    // discard => the burn

    // Glowing edge: pixels just ABOVE the cutoff get the HDR edge color.
    float edge = step(noise - _DissolveAmount, _EdgeWidth);
    col.rgb = lerp(col.rgb, _EdgeColor.rgb, edge);    // bloom (L4) makes this glow
    col.a  *= col.a;                                   // keep silhouette
    return col;
}
```

```csharp
// Drive it from the death event WITHOUT breaking batching.
IEnumerator Dissolve(SpriteRenderer sr, float dur = 0.4f)
{
    var mpb = new MaterialPropertyBlock();
    for (float t = 0; t < dur; t += Time.deltaTime)
    {
        sr.GetPropertyBlock(mpb);
        mpb.SetFloat("_DissolveAmount", t / dur);     // per-renderer, no new material
        sr.SetPropertyBlock(mpb);
        yield return null;
    }
    Pool.Release(gameObject);                          // pool, don't Destroy (W9 sets this up)
}
```

- The **noise texture is the whole trick** — it turns a uniform fade into a ragged, organic burn. Swap the noise for a different look.
- The **HDR emissive edge** only glows because of the **bloom** in your post stack (L4) — shaders and post compound.
- Driving the property via a **MaterialPropertyBlock** is what keeps five simultaneous dissolves from spawning five materials and five draw calls — the L1 performance lesson paying rent.

🎯 **Side quest complete when:** dying enemies burn away along a noise edge with a glowing rim over ~0.4s before pooling, multiple dissolve at once without breaking batching, and the framerate holds. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Draw-Call Budget Audit (+50 XP)

Prove you can *ship* polish, not just add it. Set a **draw-call budget** for an Ashfall combat scene, measure where you actually stand, and cut the count back under budget without losing the look — the exact discipline that keeps the boss's atmosphere pass at 60 FPS.

**Requirements:**
1. Open a busy combat scene (player + several enemies + torches + particles) and read the **batches / draw-call count** and **frame time** from the Stats overlay / Frame Debugger / Profiler. Write down the starting numbers.
2. Set a **target budget** (e.g. "under N batches at 60 FPS on my machine") and identify the top offenders in the Frame Debugger — usually un-atlased sprites, per-instance materials, too many real-time lights, or overdraw from overlapping transparent particles.
3. Apply at least **two** real reductions: pack sprites into an **atlas**, enable the **SRP Batcher** / share materials, swap per-instance color to a **MaterialPropertyBlock**, cap or bake lights, or reduce particle overdraw.
4. Re-measure and show the **before/after**: lower batch count and stable frame time, *same* visual result.

```
Test: scene starts at, say, 180 batches and dips to 48 FPS in a fight.
After atlasing sprites and switching enemy tint to a property block,
it's 70 batches, locked 60 FPS — and it looks identical. Numbers written
down, before and after.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```
AUDIT LOOP (measure → cut → re-measure):

1. Stats overlay → note "Batches" + "FPS". Profiler → is the frame
   CPU-bound (too many draw calls) or GPU-bound (overdraw / fill rate)?
2. Frame Debugger → step through draw calls. Look for:
     - the SAME sprite drawn many times but NOT batched  → atlas + shared material
     - "SRP Batch broken: different material"            → MaterialPropertyBlock
     - dozens of real-time Light 2D                      → fewer/baked, smaller radii
     - huge overlapping transparent particles            → fewer particles / smaller / opaque where possible
3. Apply ONE fix → re-measure. Keep the ones that help; revert the ones that don't.
```

- **Measure first, always.** "It feels slow" is not a number; "180 batches, 48 FPS" is. You can't optimize what you don't measure, and you'll waste hours guessing.
- The two biggest 2D wins are almost always a **sprite atlas** (collapses many sprite draw calls into one) and **not breaking the batch** (MaterialPropertyBlock instead of per-instance materials).
- **Transparent overdraw** from particles is the silent framerate killer — many big, overlapping, semi-transparent quads cost fill rate even when the scene "looks" cheap. Fewer, smaller, or shorter-lived particles often buys back the frame.
- This is engine-agnostic: Unreal, Godot, and custom engines all live or die by draw-call count and overdraw. The *tool* is Unity's profiler; the *skill* is "measure, find the offender, cut, re-measure."

🎯 **Side quest complete when:** you have written before/after numbers showing a real draw-call reduction at a stable 60 FPS with no visible loss of quality, achieved by at least two measured optimizations. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
