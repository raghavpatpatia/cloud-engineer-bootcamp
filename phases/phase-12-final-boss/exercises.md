# 🏋️ World 12 — Exercises

Pre-launch warm-ups to get your head in *shipping* mode before "Launch Day." None of these are about learning a new skill — by now you have them all. They're about the mindset that turns a pile of good systems into a finished, released game: scope discipline, knowing what "done" means, and the not-code parts of shipping (a press kit, a post-mortem) that real studios live and die by. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👑 Boss Battle](boss-battle.md)

---

## Warm-ups (integration, polish, release)

1. What is a **vertical slice**, and why ship one instead of "the whole game"?
   <details><summary>Hint</summary>A vertical slice is a small but <em>complete</em> chunk of the game that exercises <strong>every layer</strong> — art, audio, gameplay, AI, UI, networking, polish — at shippable quality, rather than a wide-but-shallow "everything roughed in." You ship a slice because it proves the game is <em>real and finished-feeling</em> in one representative experience (one polished co-op dungeon run), which is exactly what a publisher, a hiring manager, or a player needs to see. Wide-and-rough impresses no one; narrow-and-finished sells.</details>
2. Why is **locking the feature set** the first thing you do in a shipping phase?
   <details><summary>Hint</summary>Because you can't polish, profile, or document a moving target. Every new feature added during the ship phase is unprofiled, unpolished, and untested — it resets the clock. "Scope creep" is the number-one reason games miss launch. Locking scope draws a line: <em>everything inside the line gets finished; nothing new crosses it.</em> The discipline isn't "stop having ideas" — it's "the next idea goes in the backlog for v1.1, not into v1.0."</details>
3. What's the difference between **"it works"** and **"it's polished"**?
   <details><summary>Hint</summary>"It works" means the system is functionally correct — damage applies, the dungeon generates, co-op syncs. "Polished" means it <em>feels</em> good: hit-stop and screen shake on impact, audio on every action, readable UI, no first-frame hitches, menus that respond, a death that reads clearly. Game feel is the gap between a tech demo and a product. The systems were World 1–11; the polish is what makes a stranger call it "a game" instead of "a prototype."</details>
4. What is the **frame budget** at 60 FPS, and why does the *worst* frame matter more than the average?
   <details><summary>Hint</summary>At 60 FPS you have <strong>~16.6 ms</strong> per frame (1000 ÷ 60) to do everything. Average FPS lies: a game that averages 60 but spikes to 40 ms once a second feels <em>janky</em>, because players perceive the stutters, not the smooth stretches. Shippable performance means a <strong>stable</strong> frame time — the 99th-percentile frame stays under budget — not a flattering average. You profile for the spikes (GC, a heavy spawn, an unbatched draw call) and kill them.</details>
5. Why does a shipped game need **documentation** (README, case study) and not just a build?
   <details><summary>Hint</summary>A build with no docs is a black box: nobody knows how to run it, what it demonstrates, or why it's impressive. The <strong>README</strong> tells a player how to install and play; the <strong>case study</strong> tells a hiring manager what you built and the engineering decisions behind it; the <strong>trailer/GIFs</strong> let someone judge it in 20 seconds. Documentation is how your work travels to people who weren't there. A game nobody can figure out how to play, or appreciate, is a game nobody plays.</details>
6. What is a **release tag** (`v1.0`), and why cut one instead of just leaving `main`?
   <details><summary>Hint</summary>A tag is an immutable, named point in git history — "this exact commit is the thing we shipped." <code>main</code> keeps moving; a tag is frozen. Cutting <code>v1.0</code> (and attaching the built artifacts to a <strong>GitHub Release</strong>) means anyone can download <em>exactly</em> what launched, you can hotfix from a known baseline, and "the released version" is unambiguous. Shipping without a tag is shipping without an address — you can never point back at what went out the door.</details>
7. What belongs in a **launch checklist**, and why run one even when "it all works on your machine"?
   <details><summary>Hint</summary>A launch checklist is the pre-flight: builds are green in CI, the cloud server is live and reachable (not just your laptop), the release page loads for a logged-out stranger, the download actually runs on a clean machine, the docs are accurate, the tag is cut, monitoring is armed, and the rollback path is known. You run it because "works on my machine" is exactly the failure mode launches die on — the player isn't on your machine. The checklist is how studios stop shipping a broken link to the world.</details>
8. Why write a **post-mortem** after you ship, and what makes a good one?
   <details><summary>Hint</summary>Because shipping is the best teacher and the lessons evaporate fast. A post-mortem captures, while it's fresh: <strong>what went well</strong> (keep doing it), <strong>what went wrong</strong> (and the root cause, not the blame), and <strong>what you'd do differently</strong>. A good one is honest, specific, and forward-looking — "the GC spike cost us a week because we profiled too late" beats "performance was hard." Every studio does them; it's how a team gets better at the one skill that matters most — finishing.</details>

---

## 🌟 Side Quest 1 — The Press Kit (+50 XP)

Prove you can package Ashfall so a stranger — a journalist, a publisher, a hiring manager — can grasp it in under a minute. Real studios maintain a **press kit**: the single page that sells the game. You'll build Ashfall's.

**Requirements:**
1. Write a one-page **press kit** (a `presskit.md` or a simple page in the repo / on the release) with: the game's **name + one-line hook**, a **short description** (2–3 sentences), a **feature list** (5–7 bullets), **key art / screenshots**, an **animated GIF** of gameplay, the **trailer link**, **system requirements**, the **release link**, and your **credits/contact**.
2. The hook must be sharp enough to make someone want to play it: *"A co-op action-roguelite where every dungeon is new and the dark fights back."*
3. Capture the visuals from the *polished* build — lit, juiced, at 60 FPS — not an early prototype.
4. Make it self-contained: someone who has never spoken to you should be able to understand and play Ashfall from this page alone.

```
Test: hand the press kit (just the page, no explanation) to a friend. In 60
seconds they should be able to tell you what Ashfall is, why it looks fun, and
how to play it. If they have to ask "wait, what is this?" — the kit isn't done.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```markdown
# Ashfall — a co-op action-roguelite where the dark fights back

> Descend into ever-shifting dungeons, alone or with a friend. Smart enemies
> hunt you, the Ashen Warden waits below, and no two runs are the same.

![Ashfall gameplay](media/ashfall.gif)

## Features
- ⚔️ Tight top-down action combat — abilities, dashes, status effects, loot
- 🧩 Procedurally generated dungeons — every run is new
- 🤖 Enemies that actually path, sense, and adapt; a multi-phase boss
- 🎨 Dynamic 2D lighting, shaders, and game feel at a locked 60 FPS
- 🌐 Server-authoritative 2-player online co-op

## Trailer · Download · Specs · Credits
- ▶️ Trailer: <link>   📦 Play: <release link>   🖥️ Win/Mac, 4 GB RAM
- Built solo in Unity/C# · contact: <you>
```

- Borrow the proven shape: indie press kits (see the well-known **presskit()** format by Rami Ismail) all hit the same beats — hook, description, features, media, facts, contact.
- The media does the selling. One great 5-second GIF of a juicy boss hit is worth three paragraphs.
- This is portfolio gold too: it's the artifact a hiring manager actually opens.

🎯 **Side quest complete when:** a self-contained press kit exists in the repo/release with hook, description, features, real polished-build media (screenshots + a GIF), trailer link, specs, download link, and credits — and a friend can understand and play Ashfall from it alone. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — The Post-Mortem (+50 XP)

Prove you can do the thing that separates people who *finish* games from people who don't: reflect honestly on the whole build and write it down. You'll write Ashfall's **post-mortem** — the document a studio writes after every ship.

**Requirements:**
1. Write a **post-mortem** (`POSTMORTEM.md` in the repo) covering the full bootcamp build of Ashfall, World 0 → Launch Day.
2. Structure it in the classic three sections: **What went well**, **What went wrong**, **What I'd do differently** — each with specific, concrete examples drawn from the actual build (e.g. "ECS-lite in W9 should have come before W6's enemy spawns," "I profiled too late and the GC spike cost me M2 time").
3. Tie at least three lessons back to **specific worlds** — show the build taught you something, not just that it happened.
4. End with a **forward look**: what you'd build next, and the one engineering habit you're keeping forever.

```
Test: a future you (or a teammate) reads the post-mortem and learns something
actionable about how to ship a game — not a diary of what you did, but a map of
what to repeat and what to avoid. Vague = fail. "Performance was hard" is a
diary entry; "profiling late cost a week, so I now profile from M1" is a lesson.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```markdown
# Ashfall — Post-Mortem

## What went well
- Clean architecture (W1) paid off for two years' worth of features — events
  meant W5 combat and W7 VFX wired in without touching W3's controller.
- Locking scope at M1 is the only reason M2/M3 finished. No new features = polish
  actually converged.

## What went wrong
- Profiled too late. The GC spike from per-frame allocations (should've been
  caught in W9) ate days in M2 before I opened the profiler.
- Underestimated polish. "It works" (W5) and "it feels good" (M2) were weeks apart.

## What I'd do differently
- Profile from the first integration, not the last. Frame budget is a constraint,
  not a finishing step.
- Capture media as I go — recreating a polished GIF at the end is painful.

## Next & the habit I keep
- Next: turn the W11 top-down shooter into a full slice.
- Habit: measure before optimizing, and lock scope before polishing. Always.
```

- Honesty is the whole point — a post-mortem that's all wins teaches nothing. Root cause over blame.
- Every studio does this (search "GDC post-mortem" — they're famous). It's a real professional artifact and great portfolio material.
- Keep it tied to the *specific* worlds; that's what proves the build, not just the project, taught you to ship.

🎯 **Side quest complete when:** a `POSTMORTEM.md` exists covering the full Ashfall build with concrete what-went-well / what-went-wrong / what-I'd-do-differently sections, at least three lessons tied to specific worlds, and a forward look — honest and specific enough that someone else could learn to ship from it. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
