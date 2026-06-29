# 🏋️ World 2 — Exercises

Extra reps to make the math *intuition* automatic before the boss battle. None are required to advance, but each one is exactly the kind of reasoning "The Aiming Reticle" demands — directions you trust, "where is that relative to me," angles from `atan2`, and smoothing that feels the same on every machine. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (vectors, dot/cross & trig fluency)

1. Given `a = (3, 4)`, what is `a.magnitude`, and what is `a.normalized`? Why would you *ever* normalize before using a direction?
   <details><summary>Hint</summary>magnitude = √(3²+4²) = <strong>5</strong>; normalized = (0.6, 0.8) (length 1). You normalize so speed doesn't depend on how far the input/target happens to be — direction × speed, not raw vector × speed.</details>
2. Player presses up+right. Raw input is `(1, 1)`. Why is the player faster diagonally, and what's the one-line fix?
   <details><summary>Hint</summary>`(1,1)` has length √2 ≈ 1.41, not 1. Normalize the input vector before applying speed: `input.normalized * speed`.</details>
3. `Vector2.Dot(forward, toTarget)` is **positive**, **zero**, and **negative** — what does each say about where the target is?
   <details><summary>Hint</summary>Positive → in front (angle < 90°); zero → exactly to the side (90°); negative → behind (> 90°). With both vectors normalized, the dot <em>is</em> cos(angle).</details>
4. You want a 90° field-of-view cone. What dot-product threshold gates "inside the cone"?
   <details><summary>Hint</summary>Half-angle 45° → `Dot(forwardN, toTargetN) >= cos(45°) ≈ 0.707`.</details>
5. The 2D cross product `a.x*b.y - a.y*b.x` is positive vs negative — what does the sign tell you, and what's it good for?
   <details><summary>Hint</summary>Sign = which <strong>side</strong> the target is on (left vs right of forward). Perfect for "turn left or right to aim" and for a perpendicular/normal.</details>
6. Why `Mathf.Atan2(dir.y, dir.x)` instead of `Atan(dir.y / dir.x)` to get an aim angle?
   <details><summary>Hint</summary>`Atan2` uses both signs to pick the correct quadrant (full −π…π) and never divides by zero. Plain `Atan` collapses two quadrants and explodes at x=0.</details>

## Smoothing & frame-rate warm-ups

7. Convert: 180° to radians, and π/2 radians to degrees. Which unit do `Mathf.Sin/Cos/Atan2` use?
   <details><summary>Hint</summary>180° = π rad; π/2 rad = 90°. The trig functions work in <strong>radians</strong> — convert with `Mathf.Deg2Rad` / `Mathf.Rad2Deg`.</details>
8. `transform.position += velocity` vs `transform.position += velocity * Time.deltaTime` — what breaks, and on whose machine?
   <details><summary>Hint</summary>Without `* deltaTime`, speed scales with frame rate — fast on a 144 Hz desktop, slow on a 30 fps laptop. Multiplying by deltaTime makes it metres-per-<em>second</em>, identical everywhere.</details>
9. Why is `current = Lerp(current, target, 0.1f)` per frame *not* framerate-independent, and what's the standard fix?
   <details><summary>Hint</summary>It applies 10% per <em>frame</em>, so it converges faster at high FPS. Fix: `Lerp(current, target, 1 - Mathf.Exp(-k * Time.deltaTime))` (or feed `t = k * deltaTime`).</details>
10. When do you reach for `Slerp`/`RotateTowards` over `Lerp` for an angle?
    <details><summary>Hint</summary>Angles wrap (359°→1°). Lerping the raw number spins the long way; slerp/`Mathf.LerpAngle`/`RotateTowards` take the short arc.</details>

---

## 🌟 Side Quest 1 — The Homing Missile (+50 XP)

Prove you can *steer* a direction over time instead of snapping it. Build a projectile that curves toward a target each frame using normalize + slerp — framerate-independent — but can only turn so fast (so the player can dodge).

**Requirements:**
1. A `HomingMissile` with a `target` (Transform) and a `turnRateDegPerSec`.
2. Each frame: compute `desiredDir = (target.position - transform.position).normalized`, then rotate the *current* heading toward `desiredDir` capped by `turnRate * Time.deltaTime`.
3. Move forward along the current heading at constant speed (`* Time.deltaTime`).
4. It must visibly **arc**, not teleport its aim — and a fast-strafing target must be able to escape if `turnRate` is low.

```
Test: at 30 fps and at 200 fps the missile follows the SAME curved path to the target. Drop turnRate and the target can juke it.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using UnityEngine;

public class HomingMissile : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float speed = 6f;
    [SerializeField] private float turnRateDegPerSec = 120f;
    private Vector2 heading = Vector2.right;   // current travel direction

    void Update()
    {
        if (target == null) return;

        Vector2 desired = ((Vector2)target.position - (Vector2)transform.position).normalized;

        // turn toward desired, but no faster than turnRate * dt (the "can be dodged" cap)
        float maxStep = turnRateDegPerSec * Time.deltaTime;
        heading = Vector3.RotateTowards(heading, desired, maxStep * Mathf.Deg2Rad, 0f).normalized;

        // face + move forward, framerate-independent
        transform.position += (Vector3)(heading * speed * Time.deltaTime);
        transform.rotation = Quaternion.Euler(0, 0, Mathf.Atan2(heading.y, heading.x) * Mathf.Rad2Deg);
    }
}
```

- `normalized` gives a pure direction; `RotateTowards` caps the turn so the arc is smooth and dodgeable.
- `* Time.deltaTime` on both the turn *and* the move is what makes the path identical at any FPS.
- `Atan2` turns the heading back into a facing angle for the sprite.

🎯 **Side quest complete when:** the missile arcs (never snaps) toward the target, follows the same path at any frame rate, and a low `turnRate` lets a strafing target escape. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — The Radar Blip (+50 XP)

Prove you can convert between *world space* and a *local UI space* — the heart of a minimap. Build a radar that plots every enemy as a dot on a circular HUD, relative to the player's position **and facing**, clamped to the radar's edge.

**Steps:**
1. For each enemy, compute the **relative** vector `enemy.position - player.position` (world offset).
2. Rotate that offset by `-player.facingAngle` so "up on the radar" always means "in front of the player" (this is a change of basis — local space).
3. Scale world metres → radar pixels and **clamp** the magnitude to the radar radius so far-off enemies sit on the rim, not off-screen.
4. Bonus: tint a blip differently when it's *in front* (dot ≥ 0) vs *behind* (dot < 0).

```
Test: walk past an enemy — its blip sweeps from "ahead" (top) to "behind" (bottom) as you turn. Distant enemies pin to the radar edge.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using UnityEngine;

public class RadarBlip : MonoBehaviour
{
    [SerializeField] private Transform player;
    [SerializeField] private float worldRange = 20f; // metres mapped to the radar edge
    [SerializeField] private float radarRadius = 80f; // pixels

    // Returns the blip's local position on the radar (relative to player facing).
    public Vector2 BlipPosition(Vector2 enemyWorld, float playerFacingDeg)
    {
        Vector2 offset = enemyWorld - (Vector2)player.position;          // world-relative

        // rotate into player-local space: -facing so "forward" is up
        float rad = -playerFacingDeg * Mathf.Deg2Rad;
        float cos = Mathf.Cos(rad), sin = Mathf.Sin(rad);
        Vector2 local = new(offset.x * cos - offset.y * sin,
                            offset.x * sin + offset.y * cos);

        Vector2 onRadar = local / worldRange * radarRadius;             // scale to pixels
        return Vector2.ClampMagnitude(onRadar, radarRadius);           // pin to the rim
    }
}
```

- Subtracting positions gives a *relative* vector — the only thing a radar cares about.
- Rotating by `-facing` is a tiny change-of-basis: it re-expresses the offset in the player's local frame so the radar turns with you.
- `ClampMagnitude` keeps out-of-range enemies visible on the edge instead of flying off the HUD.

🎯 **Side quest complete when:** blips orbit correctly as the player turns, distant enemies clamp to the rim, and "in front" vs "behind" is distinguishable. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
