# ✅ World 8 — Readiness Checklist

Before you face "Co-op in a Container" and unlock World 9, make sure all of this is true. The boss assumes *every* skill below — it's one running session that exercises the whole world at once: two clients in one dungeon, server-authoritative with client prediction + reconciliation and interpolation, gameplay synced via RPCs and network variables off a shared seed, all running against a **headless dedicated server in a Docker container**. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [🌐 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Networking Fundamentals:** I understand TCP vs UDP, latency/packets/packet loss, and client-server vs peer-to-peer — and I drew Ashfall's net topology and chose its authority model on purpose
- [ ] **L2 — State Sync & Authority:** I understand server authority, client prediction + reconciliation, and interpolation (plus anti-cheat basics) — and I built replicated, server-authoritative player movement
- [ ] **L3 — Co-op Gameplay & RPCs:** I understand RPCs, network variables, and ownership — and I got two players into one dungeon off a shared seed with synced combat/loot
- [ ] **L4 — Dedicated Server & Docker:** I understand headless server builds, Docker images/containers, and the `Dockerfile` — and I built and ran a Dockerized Ashfall dedicated server locally

## 🧰 What I've built / set up
- [ ] Ashfall on **Netcode for GameObjects** with a chosen **transport** and a deliberate **client-server topology**, in `Networking/`
- [ ] **Server-authoritative movement** with client **prediction + reconciliation** and remote-player **interpolation** — wired to the W3 input/movement
- [ ] **2-player co-op** — both players spawn into **one** dungeon from a **shared server seed**, with **RPCs / network variables / ownership** syncing combat and loot
- [ ] A **headless dedicated server** build and a **`Dockerfile`** that builds an image, in `Server/` + `Docker/`
- [ ] The server **running in a Docker container**, with the port mapped, that **two clients connect to** — committed and pushed

## 🧠 Skills I can do without looking up
- [ ] Explain TCP vs UDP, why games use UDP, and the client-server vs peer-to-peer trade-off
- [ ] Explain server authority and walk through client prediction → reconciliation → interpolation, and what each one fixes
- [ ] Choose between a **network variable** and an **RPC** for a given piece of gameplay, and explain ownership
- [ ] Explain why both clients need the same dungeon seed and who owns it
- [ ] Write a basic `Dockerfile`, build an image, and `docker run` a server with a mapped port — and explain why a container is a reproducible server

---

## 🔎 Self-test (from memory, no peeking)

1. What do **TCP** and **UDP** each guarantee, and why do fast-paced games usually choose UDP?
   <details><summary>Answer</summary><strong>TCP</strong> = ordered, reliable, connection-based: it resends lost packets and delivers in order, but one lost packet stalls everything behind it (head-of-line blocking). <strong>UDP</strong> = fire-and-forget: no ordering, no resends, no waiting. Games choose UDP because a <em>stale</em> position update is worthless — you'd rather drop it and get the next one instantly than wait. Reliability you genuinely need (spawns, "you took damage") is layered back on selectively, not paid on every packet.</details>
2. What does **server-authoritative** mean, and walk the path of one keypress through **prediction → reconciliation → interpolation**.
   <details><summary>Answer</summary>Server-authoritative = the server holds the only canonical state; clients send <em>inputs</em>, not results. Path: you press move-right → your client <strong>predicts</strong> the move and renders it immediately (no waiting for the server) while recording the input → the server processes inputs authoritatively and sends back the official state → your client <strong>reconciles</strong>: it snaps to the server position and replays any un-acknowledged inputs from there (small correction if it had drifted) → meanwhile the <em>other</em> player's updates arrive as discrete snapshots, so your client <strong>interpolates</strong> them ~100 ms in the past for smooth motion. Prediction = your responsiveness; reconciliation = your accuracy; interpolation = their smoothness.</details>
3. When do you use a **network variable** vs an **RPC**, and what does **ownership** control?
   <details><summary>Answer</summary><strong>Network variable</strong> = replicated <em>state</em> that's auto-synced and persists (health, position, gold) — set it once, everyone reads the value. <strong>RPC</strong> = a one-shot <em>event/call</em> across the wire (ServerRpc: client→server "I want to attack"; ClientRpc: server→clients "play this effect"). Rule of thumb: persistent state → variable; momentary action → RPC. <strong>Ownership</strong> controls which client is allowed to drive a given networked object (usually you own your own character — you can send its inputs); the server still validates so ownership can't be abused.</details>
4. Why must both players use the **same dungeon seed**, who provides it, and what actually travels over the network?
   <details><summary>Answer</summary>Ashfall's dungeon is procedurally generated (W4): same seed → same map, enemies, and loot placement. If each client rolled its own seed they'd be in different dungeons. The <strong>server</strong> (the authority) picks the seed and sends it to clients; each client <em>regenerates</em> the identical dungeon locally. Only the tiny <strong>seed</strong> crosses the wire — not the map. (Then live gameplay state — positions, health, loot pickups — syncs via variables/RPCs on top.)</details>
5. What is a **Docker image** vs a **container**, and why is "it runs in a container" a stronger guarantee than "it works on my machine"?
   <details><summary>Answer</summary>An <strong>image</strong> is an immutable, layered package of your headless server <em>plus its whole environment</em> (OS libs, runtime, deps, config), built from a <code>Dockerfile</code>. A <strong>container</strong> is a running instance of that image. "Works on my machine" breaks the moment the next box has a different library version; a container <em>carries its environment with it</em>, so the same image runs identically on your laptop, a teammate's, CI, or AWS. That reproducibility is exactly why clouds deploy containers — and why W10 ships <em>this</em> image to a Kubernetes cluster.</details>

---

## 🌐 Boss readiness
- [ ] **Two clients** can join **one** Ashfall dungeon together over the network
- [ ] Movement is **server-authoritative** with client **prediction + reconciliation**, and remote players **interpolate** smoothly
- [ ] Both players spawn from a **shared dungeon seed** and gameplay (combat/loot) **syncs** via RPCs / network variables with clear ownership
- [ ] A **headless dedicated server** builds, and a **`Dockerfile`** produces an image
- [ ] The server **runs in a Docker container** with its port mapped, and **two separate clients connect to that container** (not to each other)
- [ ] I can explain which layer owns what (wire → authority → gameplay sync → container) and trace one input from keypress to authoritative state
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed Side Quest 1 — Lag Simulator (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Lobby / Host-Join UI (+50 XP)

---

> All checked? → [🌐 Face the Boss Battle: Co-op in a Container](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
