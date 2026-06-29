# 🏋️ World 3 — Exercises

Extra reps to make the *gameplay* skills automatic before the boss battle. None are required to advance, but each one is exactly the kind of reasoning "The Playable Slice" demands — input you can rebind, physics that moves correctly, collisions vs triggers, a camera that frames the action, and state that survives a restart. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (input, physics, collision, camera & saving)

1. Why route the keyboard *and* a gamepad through a single `Move` action instead of reading `Input.GetKey` in the controller?
   <details><summary>Hint</summary>The controller should depend on an <strong>intent</strong> ("move this direction"), not a device. One action layer means adding a pad — or rebinding keys — never touches gameplay code. That's the same decoupling as W1's architecture.</details>
2. **Polling** (`GetAxis` every frame) vs **events** (a callback on press) — when do you want each?
   <details><summary>Hint</summary>Poll continuous things you sample every frame (movement, aim). Use events for discrete one-shots (jump, fire, open menu) so you don't miss or double-fire a press between frames.</details>
3. You move a `Rigidbody2D` with `transform.position +=` and tunneling/jitter appears. Why, and the fix?
   <details><summary>Hint</summary>Teleporting the transform bypasses the physics solver, so collisions are skipped. Drive the body through physics: set <code>rb.velocity</code> (or <code>MovePosition</code>) in <code>FixedUpdate</code>.</details>
4. Why does physics-driven movement go in `FixedUpdate` and not `Update`?
   <details><summary>Hint</summary><code>FixedUpdate</code> runs on the <strong>fixed timestep</strong> the physics engine steps on. Putting forces/velocity there keeps simulation stable and consistent regardless of frame rate.</details>
5. A **collision** vs a **trigger** — what's the difference and when do you use each?
   <details><summary>Hint</summary>A collider blocks/pushes (a wall) and fires <code>OnCollision*</code>. A trigger (<code>Is Trigger</code> on) overlaps without stopping anything and fires <code>OnTrigger*</code> — perfect for pickups, doors, damage zones.</details>
6. Two objects overlap but `OnTrigger` never fires. What are the usual suspects?
   <details><summary>Hint</summary>Neither has a <strong>Rigidbody2D</strong>; the <strong>layer collision matrix</strong> has those layers unticked; one collider isn't marked <code>Is Trigger</code>; or the script is on the wrong object.</details>
7. Your follow camera judders even though the player moves smoothly. Likely cause?
   <details><summary>Hint</summary>Camera follow in <code>Update</code> reads the player's position <em>before</em> physics finished moving it. Follow in <code>LateUpdate</code> (after all movement) and smooth with a framerate-independent lerp (W2).</details>
8. What does a camera **deadzone** buy you, and what does **clamping to bounds** prevent?
   <details><summary>Hint</summary>A deadzone lets the player wiggle near center without the camera twitching (less motion sickness). Clamping stops the camera from showing the void outside the room.</details>
9. Why save to `Application.persistentDataPath` and not next to the `.exe` or in `Assets/`?
   <details><summary>Hint</summary>It's the only per-user, writable, platform-correct location. The install folder may be read-only, and <code>Assets/</code> doesn't exist in a build at all.</details>
10. You serialize the player to JSON but the save file is empty `{}`. Common reason?
    <details><summary>Hint</summary>The fields aren't serializable — Unity's <code>JsonUtility</code> only serializes <strong>public</strong> fields (or <code>[SerializeField]</code> private ones) on a <code>[System.Serializable]</code> plain class, not properties.</details>

---

## 🌟 Side Quest 1 — Coyote-Time Jump Feel (+50 XP)

Prove you can shape *feel* on top of input + physics, not just wire a button. Add **coyote time** (a tiny grace window where a jump still works just after leaving a ledge) and **jump buffering** (a press just *before* landing still counts). These two tricks are why good platformers feel forgiving — and they're pure timers over your input layer.

**Requirements:**
1. Read jump as an **event** off the input layer (not raw `GetKeyDown` in physics code).
2. Track `timeSinceGrounded`; allow a jump if it's `<= coyoteTime` even when not currently grounded.
3. On a jump press while airborne, remember it for `jumpBufferTime`; consume it the instant you land.
4. Everything time-based uses `Time.deltaTime` so the window is the *same* on every machine.

```
Test: walk off a ledge and press jump ~0.1s late — it still jumps. Press jump just before landing — it jumps the frame you touch ground. Both windows feel identical at 30 fps and 144 fps.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using UnityEngine;

public class JumpFeel : MonoBehaviour
{
    [SerializeField] private float coyoteTime = 0.1f;
    [SerializeField] private float jumpBufferTime = 0.1f;
    [SerializeField] private float jumpVelocity = 9f;
    [SerializeField] private Rigidbody2D rb;

    private float coyoteCounter;   // counts DOWN from coyoteTime while grounded
    private float bufferCounter;   // counts DOWN from a recent press
    private bool grounded;         // set by your collision/ground check

    void Update()
    {
        // grace window after leaving ground
        coyoteCounter = grounded ? coyoteTime : coyoteCounter - Time.deltaTime;

        // buffer a press for a moment (jump action comes from the input layer)
        if (InputReader.JumpPressed) bufferCounter = jumpBufferTime;
        else bufferCounter -= Time.deltaTime;

        if (bufferCounter > 0f && coyoteCounter > 0f)
        {
            rb.velocity = new Vector2(rb.velocity.x, jumpVelocity);
            bufferCounter = 0f;    // consume the press
            coyoteCounter = 0f;    // can't double-jump off one window
        }
    }
}
```

- Both counters are **timers in seconds**, decremented by `deltaTime`, so the forgiveness window is framerate-independent.
- Reading the press from the input layer (not `GetKeyDown`) keeps this device-agnostic and rebindable.
- Coyote time and buffering are independent windows that happen to combine into "press near the ledge and it just works."

🎯 **Side quest complete when:** a late press off a ledge and an early press before landing both jump, and both windows feel the same at any frame rate. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Screen-Shake on Hit (+50 XP)

Prove you can add *juice* to the camera without breaking its follow. Build a reusable **screen shake** that punches the camera on a hit (or pickup) and decays smoothly back to the followed position — framerate-independent, and layered *on top of* your follow logic so it never fights it.

**Steps:**
1. Expose a `Shake(float strength, float duration)` call other systems fire (e.g. on `OnTrigger` pickup or a hit).
2. Track a `trauma` value; each frame, offset the camera by a small random vector scaled by trauma, then **decay** trauma over time.
3. Apply the shake offset *after* the follow target is computed (in `LateUpdate`), so it adds to the smoothed position instead of replacing it.
4. All decay/timing uses `Time.deltaTime`.

```
Test: pick up an item — the camera punches and settles in ~0.3s. The follow still tracks the player the whole time. Decay looks identical at 30 fps and 144 fps.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using UnityEngine;

public class ScreenShake : MonoBehaviour
{
    [SerializeField] private float maxOffset = 0.4f;
    [SerializeField] private float decayPerSec = 1.5f;
    private float trauma;   // 0..1

    // Other systems call this on a hit / pickup.
    public void Shake(float strength) => trauma = Mathf.Clamp01(trauma + strength);

    // Returns the offset to ADD to the followed camera position this frame.
    public Vector3 OffsetThisFrame()
    {
        if (trauma <= 0f) return Vector3.zero;

        float amount = trauma * trauma;                 // square = punchier, snappier tail
        Vector2 jitter = Random.insideUnitCircle * maxOffset * amount;
        trauma = Mathf.Max(0f, trauma - decayPerSec * Time.deltaTime); // framerate-independent
        return new Vector3(jitter.x, jitter.y, 0f);
    }
}
```

```csharp
// In your FollowCamera.LateUpdate(), AFTER computing smoothed followPos:
transform.position = followPos + shake.OffsetThisFrame();
```

- `trauma` decaying by `decayPerSec * deltaTime` makes the settle time identical at any FPS.
- Squaring trauma gives a punch that hits hard then tapers — far better feel than linear.
- Adding the offset in `LateUpdate` *after* the follow keeps shake and follow from fighting each other.

🎯 **Side quest complete when:** a pickup/hit punches the camera and settles smoothly while follow keeps tracking, and decay feels the same at any frame rate. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
