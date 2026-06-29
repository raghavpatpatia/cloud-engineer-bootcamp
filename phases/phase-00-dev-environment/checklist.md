# ✅ World 0 — Readiness Checklist

Before you face the Boss Battle and unlock World 1, make sure all of this is true. If any box is empty, revisit that lesson — the Boss Battle assumes every skill below.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Studio & Game Loop:** I can explain input → update → render and `deltaTime`
- [ ] **L2 — Unity & Editor:** Unity Hub + LTS Editor + VS Code/Rider installed; Ashfall (2D) created
- [ ] **L3 — Git:** `~/projects/ashfall` is a Git repo with a Unity `.gitignore`, committed and pushed to GitHub
- [ ] **L4 — Mindset & Debugging:** `HelloAshfall` logs on `Start()`; I can read errors and set a breakpoint

## 🧰 What I've built / set up
- [ ] `~/projects/ashfall` opens in my Unity LTS Editor with a clean Console
- [ ] Play Mode runs (the game loop is live)
- [ ] Git repo with `.gitignore` ignoring `Library/`/`Temp/`/`obj/` and tracking `.meta` files
- [ ] First commit pushed to a GitHub `ashfall` remote
- [ ] `Assets/Scripts/HelloAshfall.cs` attached to a GameObject and logging

## 🧠 Skills I can do without looking up
- [ ] Explain the game loop and why per-frame movement (no `deltaTime`) is a bug
- [ ] Name the six Editor windows and what each shows
- [ ] Run the `add → commit → push` and `branch → merge` Git flows
- [ ] Say why `Library/` is ignored but `.meta` files are committed
- [ ] Use `Debug.Log` and a breakpoint to inspect live state
- [ ] Read an error message (message + file + line) before guessing

---

## 🔎 Self-test (from memory, no peeking)

1. What are the three phases of the game loop, in order?
   <details><summary>Answer</summary><strong>Input → Update → Render</strong>, repeated every frame until quit.</details>
2. You move the player `5 * Time.deltaTime` per `Update`. Why the `deltaTime`?
   <details><summary>Answer</summary>So motion is <strong>frame-rate independent</strong> — the same real-world speed on fast and slow machines (5 units <em>per second</em>, not per frame).</details>
3. In a Unity Git repo, which of `Library/` and `*.meta` do you commit, and which do you ignore?
   <details><summary>Answer</summary>Commit <code>*.meta</code> (asset import settings/links); ignore <code>Library/</code> (regenerated cache).</details>
4. Maya files a ticket. What Git flow do you use so `main` stays safe?
   <details><summary>Answer</summary><code>git switch -c feature/x</code> → commit work → <code>git switch main</code> → <code>git merge feature/x</code> → push. Branch per ticket; never edit <code>main</code> directly.</details>
5. You hit a `NullReferenceException`. What's your literal first action?
   <details><summary>Answer</summary><strong>Read it</strong> — the message names the file and line; ask "what here was <code>null</code> when used?" before touching anything else.</details>

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed Side Quest 1 — Bouncing Sprite (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Bug Hunt & Git Recovery (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: First Build, First Commit](boss-battle.md)

[← World Home](README.md)
