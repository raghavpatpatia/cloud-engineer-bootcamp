# 🛠️ Authoring Spec (for content builders)

> This is an **internal authoring guide**, not a learner-facing document. It defines the exact format, tone, and conventions every world must follow so the bootcamp feels consistent. Match World 0 exactly. The single source of truth for *what each lesson covers* is [CURRICULUM.md](../CURRICULUM.md) — never invent scope; read it first.

## Tone & philosophy
- Write like a **friendly senior mentor**, never academic. Short sections, bullets, examples over definitions.
- **Build first, theory second. Explain WHY before HOW.** Every concept must solve a felt production problem.
- **20% reading / 80% building.** Every lesson ends with something built that contributes to **Ashfall**.
- **First principles, engine-agnostic.** The *tool* is Unity/C#, but teach the underlying idea (the game loop, vectors, the FSM, the render pipeline) so it transfers to Unreal, Godot, or a custom engine. Say so explicitly when relevant ("this is how every engine does it").
- **No API memorization.** Never ask the learner to memorize method signatures. Teach the mental model; let them look up the call.
- Lessons are **20–35 minutes**. Never overwhelm.
- Use **Mermaid diagrams** liberally (flowchart / sequenceDiagram / stateDiagram-v2 / classDiagram). Prefer Mermaid over ASCII. Every lesson needs at least one.
- Use emojis as visual anchors (sparingly, consistent with World 0).

## Story (continuous narrative)
- Learner is a new-hire **Junior Gameplay Programmer** at indie studio **Pixel Forge Studios**.
- The flagship evolving project is **Ashfall**: a **2D top-down action-roguelite** built in **Unity / C#**. It is **ONE project that grows across all 13 worlds**, like a real production codebase. Each world's Project Missions advance Ashfall and leave it ready for the next world.
- Every world README opens with an **in-world Slack message / ticket / email** from a teammate stating a real production problem the world solves.
- NPC roster (use consistently — do not invent new core NPCs):
  - **Maya** — Lead Designer. Files the tickets / feature requests.
  - **Kenji** — Senior Gameplay Engineer and **the learner's mentor**. The warm "let me show you" voice.
  - **Lena** — Tech Artist. Shaders, lighting, VFX, the look.
  - **Priya** — Backend / DevOps. Servers, CI/CD, cloud, infrastructure.
  - **Theo** — Studio Director. Sets stakes, ships the game, gives the launch speech.
  - **IT Support** — World 0 only (machine + tooling setup).

## Resources rule (IMPORTANT)
- **Only FREE resources.** No paid courses, no paid assets. Unity Personal, free art/audio (Kenney.nl, OpenGameArt, freesound), in-browser playgrounds, official free docs, AWS **free tier only** (cost warnings + billing-alarm reminders in Worlds 8 & 10).
- Don't paste long link lists in lessons — point to the root [RESOURCES.md](../RESOURCES.md) (curated free links per world **with steps to use them**). In lessons you may say "see RESOURCES.md for this world."
- Prefer open-source / free-tier / in-browser tools whenever a tool is mentioned.

## File layout per world (match exactly)
```
phase-NN-slug/
  README.md          # world intro: ticket, goals, level-map table, mermaid order, project status, nav
  lessons/
    01-*.md ... 0N-*.md   # exact count & slugs from CURRICULUM.json
  exercises.md       # warm-ups + 1–2 side quests (+50 XP each)
  checklist.md       # readiness checklist + a from-memory self-test
  boss-battle.md     # the finale (see below)
```

## Lesson template (every lesson MUST include, in this order)
1. Title `# Level N — Title`
2. A metadata table: Difficulty (🟢 Easy / 🟡 Medium / 🔴 Hard), Estimated time, XP reward (`100 (Quest) + 25 (Quiz)`)
3. Top navigation line: `[← Prev](...) · [↑ Phase Home](../README.md) · [→ Next](...)`
4. `## 📖 Story` — short in-world scene (a teammate, a ticket, a moment on the team)
5. `## 🎯 Goal` — bullets
6. `## 🧠 Concepts` — with at least one **Mermaid diagram** and a `### Why this exists` subsection (the first-principles "why", and the engine-agnostic note)
7. `## 🛠️ Hands-on Lab` — numbered steps with **real, runnable C# / Unity code** in fenced ` ```csharp ` blocks (use ` ```bash ` for git/CLI, ` ```hlsl ` for shaders, ` ```yaml `/` ```hcl ` for CI/Terraform in Worlds 8 & 10). Comments via `//`.
8. `## 🎮 Mini Challenge` — small task + a `<details>` reveal answer
9. `## 📦 Project Mission` — advances **Ashfall**; ends with a clear "🎯 **Mission complete when:**" line
10. `## ⚠️ Common Mistakes` — a table (Mistake | What happens | Fix)
11. `## 🤔 Reflection Questions` — 3 questions
12. `## 📝 Quiz` — 3 multiple-choice Qs + a `<details>` answers block
13. `## ✅ Completion Checklist` — checkboxes incl. "Added **+125 XP** to PROGRESS.md"
14. Bottom navigation line (same as top)

## Boss battle template
- Metadata table (Difficulty, time, XP **500**, "Unlocks: next world").
- An **incident** Slack/ticket from a teammate (Maya/Kenji/Theo). Rules reminder (no tutorials — apply the world).
- A clear mission with **victory conditions** (checkboxes) that integrates the whole world into Ashfall.
- `<details>` reference solution(s) — gated behind "only after you've tried."
- Rewards section: +500 XP, unlocks next world, +250 world-complete bonus, update PROGRESS.md.
- Nav links including "→ Enter World N+1". (World 12's boss = ship.)

## Navigation conventions (relative links — get these exact)
**From a lesson file (`phase-NN-slug/lessons/0N-*.md`):**
- Phase / world home → `../README.md`
- Root files (README, ROADMAP, PROGRESS, CURRICULUM, RESOURCES) → `../../../FILE.md`
- Sibling lessons → `<slug>.md` (e.g. `02-vectors-and-movement.md`)
- Prev link **of the first lesson** → `../README.md`
- Next link **of the last lesson** → `../boss-battle.md`

**From a world README (`phase-NN-slug/README.md`):**
- Root files → `../../FILE.md`
- Lessons → `lessons/<slug>.md`
- Next world → `../<next-slug>/README.md`
- Top nav line: `[↑ Home](../../README.md) · [🗺️ Roadmap](../../ROADMAP.md) · [📊 Progress](../../PROGRESS.md)`

Every doc has nav at top and bottom. The learner must never wonder what's next.

## XP conventions
- Lesson = 100 (Quest) + 25 (Quiz) = **125**. Side quest = **50**. Boss = **500**. World-complete bonus = **250**.

## Project (Ashfall) continuity — DO NOT BREAK
- Tech: **Unity (Personal) + C#**, **git** version control, free assets. Cloud/DevOps folds in at **World 8** (Docker + dedicated server) and **World 10** (CI/CD, profiling, AWS, Kubernetes, Terraform) — both applied to **game servers + build pipelines**, not generic web apps.
- One growing codebase. The *features* and *architecture* compound: W0 project+repo → W1 clean architecture → W2 movement math → W3 player/camera/input/save → W4 dungeon gen + A* → W5 inventory/combat/loot → W6 enemy AI + boss → W7 lighting/shaders/polish → W8 co-op + Dockerized server → W9 ECS-lite refactor + serialization → W10 CI/CD + cloud deploy → W11 portfolio prototypes → W12 ship the vertical slice.
- Project code lives in the learner's `~/projects/ashfall` (created in World 0), **NOT** in this repo.
- Each world's Project Missions must continue from the previous world's state and leave it ready for the next.
- **Special cases:** World 11's six "lessons" are portfolio project **briefs** (other-genre prototypes), not Ashfall additions. World 12's three "lessons" are capstone **milestones** that ship Ashfall.

Match the **voice, structure, density, and Mermaid usage of World 0** (`phase-00-dev-environment/`). Read those files and [CURRICULUM.md](../CURRICULUM.md) before writing.
