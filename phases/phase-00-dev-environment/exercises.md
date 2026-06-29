# 🏋️ World 0 — Exercises

Extra reps to make your tools and instincts automatic before real gameplay work begins. None are required to advance, but each makes you a sharper engineer. Each **Side Quest** awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (loop, tools & Git fluency)

1. From memory, draw the game loop and label where `deltaTime` is used.
   <details><summary>Hint</summary>input → update → render, looping; <code>deltaTime</code> multiplies every per-second rate in the <strong>update</strong> phase.</details>
2. In Unity, identify which window shows the **render** output and which lists the objects **update** touches.
   <details><summary>Hint</summary>Game view = render output; Hierarchy = objects in the scene.</details>
3. Run `git status` in `~/projects/ashfall` and confirm `Library/` does **not** appear but `.meta` files do.
   <details><summary>Hint</summary>If <code>Library/</code> shows, your <code>.gitignore</code> is missing/misplaced; if <code>.meta</code> is hidden, you over-ignored.</details>
4. Make a tiny change, commit it on a new branch, merge it to `main`, delete the branch.
   <details><summary>Hint</summary><code>git switch -c x</code> → edit → <code>git add</code>/<code>commit</code> → <code>git switch main</code> → <code>git merge x</code> → <code>git branch -d x</code>.</details>
5. Add a `Debug.Log` inside `Update()` and confirm it fires once per frame; then guard it so it stops after 2 seconds.
   <details><summary>Hint</summary><code>if (Time.time &lt; 2f) Debug.Log(Time.frameCount);</code></details>

## Mindset warm-ups

6. Write down, in one sentence each, the five steps of the debugging loop without looking.
7. Explain to a rubber duck (out loud) what `MonoBehaviour` gives you and why `Start()` runs.
8. Given a `NullReferenceException` on `Player.cs:42`, state the *exact* question you'd ask first.
   <details><summary>Hint</summary>"What on line 42 was <code>null</code> when it was used?"</details>

---

## 🌟 Side Quest 1 — The Bouncing Sprite (+50 XP)

Prove you own the game loop with something visible. In Ashfall, create a script that moves any object back and forth at a constant **real-world** speed (frame-rate independent), bouncing between two x-positions.

**Requirements:**
1. A `Bouncer` MonoBehaviour on a GameObject (a default Sprite works — `GameObject → 2D Object → Sprite`).
2. Movement uses `Time.deltaTime` (NOT per-frame constants).
3. It reverses direction at `minX` and `maxX` (expose them as public fields so you can tune them in the Inspector).
4. It still bounces at the same speed if you force a low frame rate.

```
Test: drag minX/maxX/speed in the Inspector during Play and watch it retune live.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
using UnityEngine;

public class Bouncer : MonoBehaviour
{
    public float speed = 3f;     // units PER SECOND
    public float minX = -4f;
    public float maxX =  4f;
    private int dir = 1;

    void Update()
    {
        Vector3 p = transform.position;
        p.x += speed * dir * Time.deltaTime;   // frame-rate independent

        if (p.x > maxX) { p.x = maxX; dir = -1; }
        if (p.x < minX) { p.x = minX; dir =  1; }

        transform.position = p;
    }
}
```

🎯 **Side quest complete when:** the sprite bounces smoothly between `minX`/`maxX`, the speed is consistent regardless of frame rate, and you tuned the values live in the Inspector. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Bug Hunt & Git Recovery (+50 XP)

Practice both core survival skills at once: fixing a bug *and* using Git as a safety net.

**Steps:**
1. On a new branch `bug/hunt`, deliberately break `HelloAshfall` — introduce a `NullReferenceException` (e.g. call a method on a `null` GameObject in `Start()`).
2. Press Play, **read** the Console error, and write down (in a note) the message, the file, and the line number it reports.
3. Fix the bug. Confirm a clean Console.
4. Now practice recovery: make a *bad* edit, **don't** commit it, then throw it away with Git and confirm the file is back to its committed state.

```bash
# discard uncommitted changes to a file (Git as undo)
git restore Assets/Scripts/HelloAshfall.cs
git switch main          # leave the throwaway branch behind
git branch -D bug/hunt   # delete it
```

<details>
<summary>💡 What you should have learned</summary>

- A `NullReferenceException` names the **file and line** — read it before doing anything else.
- `git restore <file>` reverts uncommitted edits to the last commit; this is why committing often is freeing — you can always experiment and roll back.
- A committed, pushed `main` means no experiment can ever cost you real work.

🎯 **Side quest complete when:** you can quote the error you triggered (message/file/line), the bug is fixed, and you successfully used `git restore` to undo a bad edit. Add **+50 XP** to PROGRESS.md.
</details>

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
