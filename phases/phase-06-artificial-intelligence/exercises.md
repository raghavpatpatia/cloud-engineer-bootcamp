# 🏋️ World 6 — Exercises

Extra reps to make the *enemy AI* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "The Ashen Warden" demands — modeling state cleanly, sensing the world honestly, steering without clipping geometry, composing decisions in a tree, and scoring actions by utility. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (FSM, perception, steering, trees, utility AI)

1. Your enemy logic is a 200-line `Update()` full of nested `if (sawPlayer && !lowHp && inRange)`. Why does an FSM beat this, and what are its two core pieces?
   <details><summary>Hint</summary>An FSM has exactly two pieces: <strong>states</strong> (Patrol, Chase, Attack, Flee — each owns its own behavior) and <strong>transitions</strong> (the conditions that move between them). Only one state is active at a time, so each state's code is small and self-contained. The "if-soup" collapses combinatorially as you add conditions; the FSM stays linear — one block per state.</details>
2. Where should "what do I do this frame" live — in the state, or in the machine?
   <details><summary>Hint</summary>In the <strong>state</strong>. Each state implements <code>Enter()</code> / <code>Tick()</code> / <code>Exit()</code> and owns its own behavior; the <strong>machine</strong> only holds the current state and runs its <code>Tick()</code>, swapping when a transition fires. That's the State pattern — behavior is polymorphic, not a switch.</details>
3. An enemy should only "see" the player inside a 90° cone in front of it. How do you test that with the W2 dot product?
   <details><summary>Hint</summary>Normalize the enemy's facing vector and the (player − enemy) direction, take their <strong>dot product</strong>, and compare to <code>cos(halfAngle)</code>. If <code>dot >= cos(45°)</code> the player is within the 90° cone. Dot product of unit vectors *is* the cosine of the angle between them — that's the W2 math paying rent.</details>
4. The cone says "in front of me," but the enemy still sees you through a wall. What's missing, and how do you fix it?
   <details><summary>Hint</summary><strong>Line-of-sight.</strong> After the cone test passes, fire a <code>Raycast</code> from the enemy toward the player against the wall/obstacle layer. If it hits a wall before reaching the player, sight is blocked — no detection. Cone = "facing the right way," raycast = "nothing solid in between."</details>
5. Once detected, why not just teleport the enemy along the A\* path node-to-node? What does steering add?
   <details><summary>Hint</summary>Raw path-following snaps and clips corners and ignores other movers. <strong>Steering</strong> (seek toward the next waypoint, arrive to slow into it, avoid to push off obstacles/other enemies) produces smooth, believable, force-based movement <em>on top of</em> the A\* route. A\* picks the *route*; steering walks it like something alive.</details>
6. What's the difference between `seek` and `arrive`, and when do you want each?
   <details><summary>Hint</summary><code>seek</code> drives at full speed toward a target and overshoots; <code>arrive</code> scales speed down inside a slowing radius so the agent eases to a stop on the target. Use <code>seek</code> for the chase, <code>arrive</code> for the final waypoint / attack position so it doesn't jitter past you.</details>
7. A behavior tree has Selectors and Sequences. What's the difference in plain terms?
   <details><summary>Hint</summary>A <strong>Sequence</strong> is AND — it runs children left-to-right and fails the moment one fails (do A *then* B *then* C). A <strong>Selector</strong> is OR — it tries children until one succeeds (try A, *else* B, *else* C). Sequence = "all of these in order"; Selector = "the first of these that works."</details>
8. Why reach for a behavior tree once an enemy's FSM has ~8 states and tangled transitions?
   <details><summary>Hint</summary>FSM transitions grow O(n²) with states — every state potentially needs an edge to every other. A behavior tree is <strong>composable and hierarchical</strong>: you add a branch, not N new edges, and the tree reads top-to-bottom like a priority list a designer can follow. Decorators (cooldown, invert, repeat) add conditions without new states.</details>
9. The boss could throw a slam, a dash, or a ranged volley. Utility AI scores each. What goes into a score?
   <details><summary>Hint</summary>Each action has a <strong>scoring function</strong> over the current situation — distance to player, the boss's HP, whether the move is off cooldown, player's exposure. You evaluate every candidate, then pick the <strong>highest score</strong> (or weighted-random among the top). That's smarter than a fixed rotation and more authored than pure random.</details>
10. Why must every boss attack be *telegraphed*, and how does that interact with the player's i-frames (W5)?
    <details><summary>Hint</summary>A telegraph (wind-up animation, ground marker, a beat of delay) is what makes a boss <em>fair</em> — it gives the player a readable window to dodge or i-frame through. No telegraph = damage feels random and cheap. The telegraph duration is the contract; the W5 i-frame window is the player's answer to it.</details>

---

## 🌟 Side Quest 1 — Flocking Swarm Enemy (+50 XP)

Prove your steering is *composable*. Build a swarm enemy (bats, spores, embers) where many agents move as a believable flock using the three classic **boids** rules — **separation**, **alignment**, **cohesion** — layered on top of a shared `seek` toward the player. No agent has a brain; the *group* behavior emerges from local rules.

**Requirements:**
1. Spawn N swarm agents, each a lightweight steering agent (no per-agent FSM — they share one goal: the player).
2. Each frame, every agent sums four steering forces: **separation** (push away from neighbors that are too close), **alignment** (match neighbors' average heading), **cohesion** (steer toward neighbors' average position), and **seek** (toward the player). Use the W4 spatial hash grid for the neighbor query.
3. Weight the four forces (separation usually strongest) — expose the weights as data so the feel is tunable without a recompile.
4. Verify the flock holds together, doesn't pile into one point, and chases the player as a cloud — and that killing one agent doesn't break the rest.

```
Test: spawn 30 bats across the room. They clump into a loose, moving cloud (not a single dot, not scattered dust), drift toward the player, and split/reform around a pillar. Bump the separation weight in the Inspector → the cloud spreads, no recompile.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
public class SwarmAgent : MonoBehaviour
{
    public SwarmConfigSO cfg;            // DATA: weights + radii, designer-tuned
    Vector2 velocity;

    void FixedUpdate()
    {
        var neighbors = SpatialHash.Query(transform.position, cfg.neighborRadius); // reuse W4 grid

        Vector2 sep = Vector2.zero, ali = Vector2.zero, coh = Vector2.zero;
        int n = 0;
        foreach (var other in neighbors)
        {
            if (other == this) continue;
            Vector2 offset = (Vector2)(transform.position - other.transform.position);
            if (offset.sqrMagnitude < cfg.separationRadius * cfg.separationRadius)
                sep += offset.normalized / Mathf.Max(offset.magnitude, 0.01f); // push harder when closer
            ali += other.velocity;
            coh += (Vector2)other.transform.position;
            n++;
        }
        if (n > 0) { ali = (ali / n).normalized; coh = ((coh / n) - (Vector2)transform.position).normalized; }

        Vector2 seek = ((Vector2)(Player.Position - transform.position)).normalized;

        // Sum WEIGHTED forces — separation strongest so they never collapse to a point.
        Vector2 steer = sep * cfg.wSeparation + ali * cfg.wAlignment
                      + coh * cfg.wCohesion + seek * cfg.wSeek;

        velocity = Vector2.ClampMagnitude(velocity + steer * Time.fixedDeltaTime, cfg.maxSpeed);
        transform.position += (Vector3)(velocity * Time.fixedDeltaTime);
    }
}
```

- The flock has **no central controller** — emergent behavior from three local rules is the whole point. This is the L3 steering idea taken to its limit.
- **Separation must out-weigh cohesion**, or the swarm collapses into a single overlapping dot. Tuning is data, not code.
- Reusing the **W4 spatial hash** for the neighbor query keeps it O(neighbors), not O(N²) — your earlier worlds compounding.

🎯 **Side quest complete when:** a flock of agents chases the player as a coherent, non-collapsing cloud using separation/alignment/cohesion + seek, with weights tunable as data, splitting and reforming around obstacles. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Stealth Alert Propagation (+50 XP)

Make a room of guards feel *connected*. When one enemy detects the player, that alarm should **propagate** to nearby allies (a shout, a flare) so the whole room escalates — and **decay** back to calm if the player stays hidden long enough. This is perception (L2) feeding the FSM (L1) across *multiple* agents.

**Requirements:**
1. Give each enemy an **alert level** (0 = Calm → Suspicious → Alarmed) that its own perception raises when it sees/hears the player, and that **decays** over time when it doesn't.
2. When an enemy reaches **Alarmed**, it broadcasts to allies within a hearing/shout radius (reuse the W4 spatial hash), raising *their* alert level — even allies who never saw the player directly. Alarm spreads outward, not instantly to the whole map.
3. Wire alert level into the FSM transitions: Calm → patrol, Suspicious → investigate last-known position, Alarmed → chase/attack.
4. If the player breaks line of sight and waits, alert decays back down the chain and guards return to patrol (with a believable cooldown, not an instant snap).

```
Test: sneak past guard A. It spots you and shouts. Within a second, guards B and C — who never saw you — go from patrolling to converging on your last-known position. Break line of sight and hide for 10s → the room cools back to Calm, one guard at a time.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
public class AlertSystem : MonoBehaviour
{
    public AlertConfigSO cfg;            // DATA: thresholds, decay rate, shout radius
    public float alert;                  // 0 = Calm
    public AlertState State =>
        alert >= cfg.alarmedThreshold ? AlertState.Alarmed :
        alert >= cfg.suspiciousThreshold ? AlertState.Suspicious : AlertState.Calm;

    void Update()
    {
        if (perception.CanSeePlayer)                          // L2: cone + line-of-sight
            alert = Mathf.Min(alert + cfg.gainPerSec * Time.deltaTime, cfg.max);
        else
            alert = Mathf.Max(alert - cfg.decayPerSec * Time.deltaTime, 0f); // cools when unseen

        if (State == AlertState.Alarmed) Shout();
    }

    void Shout()                                             // PROPAGATE to nearby allies
    {
        foreach (var ally in SpatialHash.Query(transform.position, cfg.shoutRadius)) // reuse W4 grid
            ally.GetComponent<AlertSystem>()?.Hear(transform.position);
    }

    public void Hear(Vector2 source)                        // raised WITHOUT seeing the player
    {
        alert = Mathf.Max(alert, cfg.suspiciousThreshold);
        lastKnown = source;                                 // FSM (L1) investigates this point
    }
}
```

- Alert is a **continuous value** that thresholds into discrete FSM states — smoother than flipping a boolean, and the decay gives you free "cool down" behavior.
- Propagation is **local and outward** (shout radius via the W4 grid), so alarm *spreads* like sound instead of teleporting to every enemy — that's what makes it read as a connected room.
- Perception (L2) raises alert; the FSM (L1) *reads* the resulting state. The two systems stay decoupled — sensing is separate from deciding.

🎯 **Side quest complete when:** one enemy's detection propagates a decaying alert to nearby allies who then converge on the last-known position via their FSM, and the room cools back to patrol when the player stays hidden. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
