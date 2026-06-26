# 🛠️ Authoring Spec (for content builders)

> This is an **internal authoring guide**, not a learner-facing document. It defines the exact format, tone, and conventions every world must follow so the bootcamp feels consistent. Match World 0 exactly.

## Tone & philosophy
- Write like a **friendly senior mentor**, never academic. Short sections, bullets, examples over definitions.
- **Build first, theory second. Explain WHY before HOW.** Every tool must solve a felt problem.
- **20% reading / 80% building.** Every lesson ends with something built that contributes to the **Task Manager Platform (TaskFlow)**.
- Lessons are **15–25 minutes**. Never overwhelm.
- Use **Mermaid diagrams** liberally (flowchart/sequenceDiagram). Prefer Mermaid over ASCII.
- Use emojis as visual anchors (sparingly, consistent with World 0).

## Story (continuous narrative)
- Learner is a Junior Engineer at **CloudForge Inc.** building **TaskFlow** (Task Manager Platform).
- Every world README opens with an **email/ticket/Slack message** from a teammate stating a real problem the world solves.
- Teammates you can reference: IT Support, your Manager (Dana), a Senior Eng (Marcus), DevOps lead (Priya), the CEO (for launch).

## Resources rule (IMPORTANT)
- **Only FREE resources.** No paid courses. AWS = free tier only, with cost warnings + billing alarm reminders.
- Don't paste long link lists in lessons — point to the root [RESOURCES.md](../RESOURCES.md) which already has 4 curated free links per world **with steps to use them**. In lessons, you may reference "see RESOURCES.md for this world."
- If you mention a tool, prefer ones free to learn (free tiers, open source, in-browser playgrounds).

## File layout per world (match exactly)
```
phase-NN-slug/
  README.md          # world intro: ticket, goals, level-map table, mermaid order, project status, nav
  lessons/
    01-*.md ... 0N-*.md
  exercises.md       # warm-ups + 1–2 side quests (+50 XP each)
  checklist.md       # readiness checklist + a from-memory self-test
  boss-battle.md     # the finale (see below)
```

## Lesson template (every lesson MUST include, in this order)
1. Title `# Level N — Title`
2. A metadata table: Difficulty (🟢 Easy / 🟡 Medium / 🔴 Hard), Estimated time, XP reward (`100 (Quest) + 25 (Quiz)`)
3. Top navigation line: `[← Prev](...) · [↑ Phase Home](../README.md) · [→ Next](...)`
4. `## 📖 Story` — short in-world scene
5. `## 🎯 Goal` — bullets
6. `## 🧠 Concepts` — with at least one **Mermaid diagram** and a `### Why this exists` subsection
7. `## 🛠️ Hands-on Lab` — numbered steps with real, runnable **commands** (in fenced code blocks with the right language). Comments via `#`.
8. `## 🎮 Mini Challenge` — small task + a `<details>` reveal answer
9. `## 📦 Project Mission` — advances TaskFlow; ends with a clear "🎯 Mission complete when:" line
10. `## ⚠️ Common Mistakes` — a table (Mistake | What happens | Fix)
11. `## 🤔 Reflection Questions` — 3 questions
12. `## 📝 Quiz` — 3 multiple-choice Qs + a `<details>` answers block
13. `## ✅ Completion Checklist` — checkboxes incl. "added +125 XP to PROGRESS.md"
14. Bottom navigation line (same as top)

## Boss battle template
- Metadata table (Difficulty, time, XP **500**, "Unlocks: next world").
- An **incident** email/ticket. Rules reminder (no tutorials).
- A clear mission with **victory conditions** (checkboxes).
- `<details>` reference solution(s) — gated behind "only after you've tried."
- Rewards section: +500 XP, unlocks next world, +250 world-complete bonus, update PROGRESS.md.
- Nav links including "→ Enter World N+1".

## Navigation conventions
- Use **relative links**. From a lesson file: phase home is `../README.md`; root files are `../../../FILE.md`. From a world README: root files are `../../FILE.md`; lessons are `lessons/0N-*.md`; next world is `../phase-NN-slug/README.md`.
- Every doc has nav at top and bottom. The learner must never wonder what's next.

## XP conventions
- Lesson = 100 (Quest) + 25 (Quiz) = 125. Side quest = 50. Boss = 500. World complete bonus = 250.

## Project (TaskFlow) continuity — DO NOT BREAK
- Tech stack: **Node.js + Express**, data **SQLite → PostgreSQL**, **Docker**, **AWS free tier**, **GitHub Actions**, **Terraform**, **Kubernetes** (minikube/kind locally).
- The app's features stay simple (CRUD on tasks). The **infrastructure** is what grows.
- Project code lives in the learner's `~/projects/taskflow` (created in World 2), NOT in this repo.
- Each world's Project Missions must continue from the previous world's state and leave it ready for the next.

Match the **voice, structure, density, and Mermaid usage of World 0** (`phase-00-environment-setup/`). Read those files before writing.
