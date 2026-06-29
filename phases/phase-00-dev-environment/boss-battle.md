# 👹 Boss Battle — First Build, First Commit

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 40 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 1 — Programming Mastery |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Kenji <kenji@pixelforge.studio>
To:      You <new-hire@pixelforge.studio>
Cc:      Theo <theo@pixelforge.studio>
Subject: [ONBOARD-FINAL] Prove it. Build, commit, and fix the gremlin.

Onboarding's over — time to prove the toolchain works end to end, by
YOU, with no hand-holding. Three things, and Theo's watching:

  1. Produce a RUNNABLE build of the empty Ashfall project. An actual
     executable that opens a window. "It runs in the Editor" is not a build.
  2. Push a CLEAN first commit (or commits) to GitHub — .gitignore working,
     NO Library/, .meta files present.
  3. I dropped a gremlin into a bootstrap script (below). It throws on
     Play. Reproduce it, READ the error, and fix it — the way I showed you.

No step-by-step from me. You have all four lessons. Go earn World 1.

— Kenji
```

> ⚔️ **Boss Battle rules:** No tutorials, no copying lesson files wholesale. Apply World 0: build it yourself, reason about the bug from the error message, and prove each result. You win when every victory condition is met **and you can explain the bug out loud.**

---

## 🐛 The seeded bug

Kenji added this script to Ashfall. Drop it on an empty GameObject and press Play — it throws. Find out *why* from the Console (don't just pattern-match the fix; read it).

```csharp
using UnityEngine;

public class WorldBootstrap : MonoBehaviour
{
    public GameObject player;   // Kenji "forgot" to assign this in the Inspector

    void Start()
    {
        Debug.Log("Ashfall booting...");

        // Intended: announce where the player spawned.
        Debug.Log("Player spawned at " + player.transform.position);

        Debug.Log("Boot complete.");
    }
}
```

It logs `"Ashfall booting..."` and then dies before `"Boot complete."`. Your job: name the exception, explain the cause, and fix it so all three logs appear.

---

## 🎯 Your mission

Take Ashfall from "opens in the Editor" to **built, committed, and bug-free**:

1. **Build:** produce a runnable standalone build of the empty Ashfall project (`File → Build Settings` → add the open scene → **Build**), into a `Build/` folder. Launch the built executable — it should open a window with no errors.
2. **Commit clean:** ensure `Build/` and `Library/` are git-ignored, then commit and push your work to GitHub. The remote must show your `Assets/` + `.meta` files and **must not** show `Library/` or `Build/`.
3. **Fix the gremlin:** add `WorldBootstrap`, reproduce the crash, read the error, fix it, and confirm all three logs print. Commit the fix on a branch and merge it.

---

## 🏆 Victory conditions

- [ ] A standalone Ashfall **build** exists and **launches** (a window opens), not just Play Mode
- [ ] `Build/` and `Library/` are git-ignored and **absent** from the GitHub repo
- [ ] The GitHub `ashfall` repo shows `Assets/` source **with** `.meta` files and a sane history
- [ ] `WorldBootstrap` no longer throws — all three `Debug.Log`s print in order
- [ ] The fix is committed on a branch and merged to `main`, then pushed
- [ ] You can explain, out loud, the exact exception and its cause

---

## 🧪 How you'll know you won

```bash
cd ~/projects/ashfall

# Library/ and Build/ are ignored — neither should be tracked:
git status --ignored | grep -E "Library/|Build/"     # appears under "Ignored", not staged
git ls-files | grep -E "Library/|Build/"             # → prints NOTHING

# .meta files ARE tracked:
git ls-files | grep "\.meta$" | head                 # → prints some .meta files

# History is pushed:
git log --oneline
git status            # "Your branch is up to date with 'origin/main'"
```

Then launch the built executable from your `Build/` folder — a window opens, clean. And in the Editor, Play `WorldBootstrap` → Console shows all three logs, no red. If all that holds, you've won.

<details>
<summary>🔎 Reference solution — only after you've tried! (bug fix + approach)</summary>

**The bug:** a **`NullReferenceException`** on the `player.transform.position` line. The public `player` field was never assigned in the Inspector, so at runtime `player` is `null` — dereferencing `.transform` on `null` throws. The Console points right at that line; that's the read-the-error skill from Level 4.

**Two valid fixes:**

*Option A — assign the reference (designer-friendly):* in the Hierarchy create a GameObject to act as the player (e.g. a Sprite), then drag it onto the `Player` slot of `WorldBootstrap` in the Inspector. Now `player` isn't null.

*Option B — guard the code (defensive):*

```csharp
void Start()
{
    Debug.Log("Ashfall booting...");

    if (player != null)
        Debug.Log("Player spawned at " + player.transform.position);
    else
        Debug.LogWarning("No player assigned — skipping spawn log.");

    Debug.Log("Boot complete.");   // now always reached
}
```

A real codebase usually does *both*: assign the reference AND guard against null. Either way, all three logs print and the crash is gone.

**Build + commit approach:**
```bash
# after Build Settings → Build into ./Build
# ensure Build/ is ignored (add to .gitignore if not already):
grep -q "Build/" .gitignore || echo "[Bb]uild/" >> .gitignore

git switch -c fix/worldbootstrap-null
git add .
git commit -m "fix: guard WorldBootstrap against unassigned player (NRE)"
git switch main
git merge fix/worldbootstrap-null
git push
```
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **🖥️ Onboarded** — working dev box, version control, and the debugging instinct
- 🔓 **World 1 — Programming Mastery** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 0 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: you just did the entire real-world inner loop in miniature — *build, version, debug.* Every world after this assumes you can do these in your sleep. You can now. Welcome to the team for real.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🧠 Enter World 1 →](../phase-01-programming-mastery/README.md)
