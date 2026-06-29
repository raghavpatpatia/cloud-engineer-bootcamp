# ✅ World 11 — Readiness Checklist

Before you face "Portfolio Review" and unlock World 12, make sure all of this is true. The boss assumes a **presentable portfolio**: at least three standalone, public, polished prototypes — each its own repo with clean architecture, a README led by a screenshot/GIF, and a short devlog — that you can walk a hiring panel through and defend. You don't need all six briefs; you need **three you'd be proud to show**. If a box is empty, go back and finish that project (or pick a different brief).

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👔 Boss Battle](boss-battle.md)

---

## 🎨 Briefs — pick at least three and polish to a presentable bar
*(You do NOT need all six. Check the ones you fully built and presented.)*
- [ ] **Brief 1 — 2D Platformer:** precise movement (coyote time, jump buffering, variable jump) — re-applying W2 math + W3 controllers, in its own public repo with README/GIF/devlog
- [ ] **Brief 2 — Tower Defense:** pathfinding/grids + economy/waves + simple AI — re-applying W4/W5/W6, in its own public repo with README/GIF/devlog
- [ ] **Brief 3 — Puzzle Game:** grid/logic puzzle with clean state + undo — re-applying W4 data structures + W1 architecture, in its own public repo with README/GIF/devlog
- [ ] **Brief 4 — Turn-Based Roguelike:** procedural gen + AI + items in a turn loop — re-applying W4/W6/W5, in its own public repo with README/GIF/devlog
- [ ] **Brief 5 — Top-Down Shooter:** bullet-heavy, pooling/DOD + juice, performant under load — re-applying W9 + W7, in its own public repo with README/GIF/devlog
- [ ] **Brief 6 — Multiplayer Mini-Engine:** a tiny networked slice built from scratch — re-applying W8 networking + W9 architecture, in its own public repo with README/GIF/devlog
- [ ] **At least THREE of the above are fully done** — and I picked them for **contrast** (different muscles), not because they were the three easiest

## 🧰 Per project — each one I'm presenting is...
- [ ] Its **own standalone public GitHub repo** (not a folder/branch inside Ashfall, not a mono-repo)
- [ ] **Clean architecture** — sensible structure, no single mega-file, readable to a stranger
- [ ] **Runnable by a stranger** — documented setup (Unity version, "open this scene"), real `.gitignore`, no committed build cruft or secrets
- [ ] A **README led by a screenshot/GIF**, with a one-line pitch, run steps, and a short how-it-works/architecture section
- [ ] A **short devlog** — the story/decision/trade-off behind it — linked from the README
- [ ] A **tidy commit history** (meaningful messages) I wouldn't be embarrassed to have a reviewer open

## 🧠 Things I can do without looking up
- [ ] Say, for each project, **which prior-world skills it re-applies** and **what genre contrast it adds** to the set
- [ ] Walk someone through one project's **architecture** and name the **trade-off** I chose and why
- [ ] Explain why **range across three contrasting projects** beats depth in one for a hiring manager
- [ ] Make a project **legible in thirty seconds** to a non-cloning reviewer (README + GIF)

---

## 🔎 Self-test (from memory, no peeking)

1. A hiring manager has **thirty seconds** on your repo and won't clone it. What must they be able to see, and why does it sink a great project if it's missing?
   <details><summary>Answer</summary>They must see, from the README front page alone: <strong>what it is</strong> (one-line pitch), <strong>that it works and what it looks like</strong> (a <strong>GIF/screenshot</strong> at the top — gameplay moving, no clone needed), <strong>how it's built</strong> (a short architecture note showing deliberate structure), and <strong>how to run it</strong> (exact steps + engine version). It sinks the project because a reviewer who can't quickly see what it is and that it works simply <em>bounces</em> — they assume it doesn't run or isn't worth the time, and they never reach the gameplay you're proud of. As far as a reviewer is concerned, the README <em>is</em> the project.</details>
2. Why **at least three** projects, and why pick them for **contrast** instead of doing the three easiest?
   <details><summary>Answer</summary>One project proves you can build <em>one</em> thing; multiple projects prove <strong>range</strong> — that your skills transfer to problems you haven't seen, which is the exact question a hiring manager is asking. But three <em>similar</em> projects barely prove more than one — three real-time action games all flex the same muscle. Picking for <strong>contrast</strong> (e.g. a precision platformer for feel, a tower defense for systems/economy, a multiplayer slice for architecture/netcode) shows distinctly different skills, so the reviewer learns far more from the spread. Quality and breadth over raw count.</details>
3. What's the difference between a **README** and a **devlog**, and why does a strong portfolio want both?
   <details><summary>Answer</summary>The <strong>README</strong> documents the <em>finished thing</em> — what it is, how to run it, how it's built; it proves the project exists and works. The <strong>devlog</strong> tells the <em>story</em> — what you set out to do, the hard problem you hit, the trade-off you chose and why, what you'd do next; it proves there's a <em>thinking engineer</em> behind the code. A portfolio wants both because the README gets a reviewer to take the project seriously, while the devlog shows <em>how you reason</em> — the thing they most want to evaluate and can't get from the code alone.</details>
4. Why **standalone public repos**, and what do your **repo structure and commit history** signal to a reviewer?
   <details><summary>Answer</summary><strong>Standalone public repos</strong> let a reviewer open one focused, clean project at a time — its own front page, README, history, and "this is a complete small thing" signal. Burying prototypes inside Ashfall hides them and muddies that project's story; a six-in-one mono-repo makes none of them skimmable. The <strong>repo structure and commit history</strong> signal your <em>craft and work habits</em>: meaningful commit messages (not "stuff"/"fix"), a sensible folder layout, a real <code>.gitignore</code>, no committed artifacts or secrets, ideally green CI. Reviewers <em>do</em> open the file tree and the log — they read it the way you'd read a teammate's PR. A tidy repo says "I'd be low-friction to work with."</details>
5. How do you present a prototype's **scope and limitations** so they read as strengths, and why does this matter to a hiring panel?
   <details><summary>Answer</summary>Frame limitations as <strong>decisions</strong>, not apologies: "scoped to one level to nail the jump feel" reads as <em>judgment</em>; "didn't have time for more levels" reads as <em>unfinished</em>. A short "scope &amp; next steps" section that names what you deliberately left out — and what you'd build next — shows you understand product scope and can prioritize. It matters because a hiring panel values <strong>engineering judgment</strong> as much as raw output: a clearly-scoped, polished small thing demonstrates that you can ship something <em>complete</em> and reason about trade-offs, which they trust far more than a sprawling, half-finished project.</details>

---

## 👔 Boss readiness
- [ ] **At least three** standalone, public, polished portfolio repos are live on GitHub, chosen for **contrast**
- [ ] Each has **clean architecture**, a **README led by a screenshot/GIF**, and a **short devlog** — and runs for a stranger
- [ ] I can **present each project to a panel** — what it proves, the architecture, the trade-off I made
- [ ] I can articulate why this set shows **range**, mapping each project back to the prior-world skills it re-applies
- [ ] Ashfall is **untouched** this world (it waits for Launch Day) — these are separate projects
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to present (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP in [PROGRESS.md](../../PROGRESS.md) for each brief I fully built (125 XP each)
- [ ] (Optional) I completed Side Quest 1 — Ship a Great README + GIF (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Write a Devlog Post (+50 XP)

---

> All checked? → [👔 Face the Boss Battle: Portfolio Review](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
