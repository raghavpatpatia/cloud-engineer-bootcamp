# 📖 Glossary

Plain-English definitions of the key terms across **The Combined Bootcamp**. No jargon explaining jargon — each entry tells you *what it is* and *why it matters in games*. When a word feels fuzzy, come here.

[↑ Back to README](README.md)  ·  [📚 Resources](RESOURCES.md)  ·  [🎮 Game Overview](GAME_OVERVIEW.md)  ·  [⚔️ Quest Log](QUEST_LOG.md)

> Grouped by topic so related ideas sit together. Within each group, terms run roughly in the order you meet them.

---

## 🧠 Programming & C# (W1)
- **SOLID** — Five design principles (Single-responsibility, Open/closed, Liskov, Interface-segregation, Dependency-inversion) for code that's easy to change. *In games:* the difference between a codebase you can extend for two years and 3000-line spaghetti.
- **Delegate / event** — A delegate is a variable that holds a function; an `event` is a delegate others can subscribe to but not raise. *In games:* lets `OnPlayerDamaged` fire once and the UI, audio, and AI all react, with nothing tightly coupled.
- **Observer pattern** — One object publishes notifications; many subscribe and react, without the publisher knowing them. *In games:* the event bus that keeps systems decoupled.
- **Coroutine** — A function that can pause (`yield`) and resume across frames in Unity. *In games:* ideal for "wait 2 seconds then explode" or animating something over time without blocking the game loop.
- **async/await** — Language feature for non-blocking work that finishes later (I/O, loading). *In games:* load a level or fetch from the network without freezing the frame. (Unlike coroutines, it isn't tied to the frame loop.)
- **ScriptableObject / data-driven design** — A Unity asset that holds data (not scene behavior); data-driven design means systems read tunable data instead of hard-coded values. *In games:* designers tune item stats and abilities without a programmer or a recompile.

## 🔁 The Game Loop & Time (W0, W2, W3)
- **Game loop** — The cycle every engine runs forever: read **input** → **update** the world → **render** a frame. *In games:* it *is* the game; everything you build hangs off it.
- **Delta time** — Seconds elapsed since the last frame (`Time.deltaTime`). *In games:* multiply movement by it so speed is the same on a 30 fps laptop and a 144 Hz desktop (framerate independence).
- **Fixed timestep** — A separate update that runs at a constant rate (e.g. 50 Hz, `FixedUpdate`). *In games:* physics needs steady steps to stay stable and deterministic; variable frames would make it jitter.

## 📐 Math for Games (W2)
- **Vector** — A list of numbers (x, y[, z]) representing a position, direction, or velocity. *In games:* the language of all movement, aiming, and physics.
- **Normalization** — Scaling a vector to length 1 while keeping its direction. *In games:* so diagonal movement isn't faster than straight — direction × speed, not raw vector × speed.
- **Dot product** — A single number from two vectors; with both normalized it equals the cosine of the angle between them. *In games:* "is the target in front of me?" and field-of-view cones (W6 AI vision).
- **Cross product** — A vector (3D) or scalar (2D) perpendicular to its inputs; its sign tells you sidedness. *In games:* "turn left or right to aim?" and computing surface normals.
- **Quaternion** — A 4-number way to store rotations without the gimbal-lock and wrap-around bugs of raw angles. *In games:* Unity's `transform.rotation`; smoothly rotating without flipping.
- **Lerp / Slerp** — Linear interpolation blends two values by a fraction `t` (0→1); spherical interpolation does the same for rotations along the shortest arc. *In games:* smooth camera follow (lerp) and smooth aiming (slerp).
- **Easing** — A curve that makes a 0→1 blend speed up or slow down (ease-in/out) instead of moving linearly. *In games:* UI and motion that feels natural and "juicy," not robotic.
- **Bezier** — A curve defined by control points. *In games:* smooth paths for projectiles, cameras, and UI tweens.
- **Transform / local-vs-world space** — A transform holds position, rotation, and scale; *local* space is relative to a parent, *world* space is the global frame. *In games:* a wheel spins in its local space while the whole car moves in world space.

## 🧮 Algorithms & Data Structures (W4)
- **Big-O** — Shorthand for how an algorithm's cost grows as input grows (O(1), O(n), O(n²)…). *In games:* picking the right approach so checking 1000 entities doesn't tank the frame.
- **BFS / DFS** — Breadth-first search explores a graph level by level (good for shortest unweighted paths); depth-first dives down one branch first. *In games:* "is this dungeon room reachable?" and flood-fill connectivity.
- **A\*** — Pathfinding = Dijkstra + a heuristic that biases the search toward the goal. *In games:* enemies that path *around* walls to the player instead of walking into them.
- **Heuristic** — A cheap estimate of remaining cost (e.g. Manhattan distance) that guides A\*. *In games:* makes pathfinding fast; must never overestimate (be "admissible") or paths go wrong.
- **Spatial partitioning / quadtree** — Dividing space into cells (grid hash, or a quadtree that subdivides) so you only check nearby objects. *In games:* fast "what's near me?" queries for collision and AI instead of checking everything.

## 🤖 Artificial Intelligence (W6)
- **FSM (Finite State Machine)** — Logic as a set of states (Patrol, Chase, Attack) with rules for switching between them. *In games:* clean enemy behavior instead of tangled `if`-soup.
- **Behavior tree** — A tree of composable nodes (selectors/sequences/decorators) that decides what an agent does each tick. *In games:* scales to complex, designer-readable AI better than a giant FSM.
- **Utility AI** — Each possible action gets a score; the agent picks the highest. *In games:* bosses that "choose" sensibly (heal when low, attack when close) instead of fixed scripts.
- **Steering** — Forces that nudge movement (seek, flee, arrive, avoid) layered on top of a path. *In games:* enemies that follow A\* paths smoothly and dodge obstacles instead of snapping.

## 🏗️ Engine Architecture & Performance (W9)
- **Object pooling** — Reusing a pre-made set of objects instead of creating/destroying them at runtime. *In games:* fire 500 bullets with zero garbage-collection hitches.
- **ECS (Entity-Component-System)** — An architecture where entities are IDs, components are plain data, and systems are logic that runs over them. *In games:* simulate thousands of entities fast by keeping data tight and contiguous.
- **Data-oriented design** — Organizing code around how data is laid out in memory, not around objects. *In games:* the mindset behind ECS; cache-friendly loops over many entities.
- **Cache miss (AoS vs SoA)** — The CPU fetches memory in lines; an **A**rray **o**f **S**tructs scatters fields, a **S**truct **o**f **A**rrays packs each field together. *In games:* SoA lets a loop stream data with far fewer cache misses, so 1000 entities hit 60 FPS.

## 🎨 Rendering & Graphics (W7)
- **Draw call** — One command telling the GPU to draw something. *In games:* too many tank the framerate; reducing them is a core optimization.
- **Batching** — Combining many objects into one draw call. *In games:* draw a whole tilemap of sprites cheaply.
- **Culling** — Skipping objects the camera can't see (frustum/occlusion culling). *In games:* don't pay to render what's off-screen.
- **Overdraw** — Drawing the same pixel multiple times (e.g. stacked transparent sprites). *In games:* a hidden framerate killer, especially with particles and lighting.
- **LOD (Level of Detail)** — Swapping in simpler versions of an asset when it's far away. *In games:* keeps distant objects cheap to render.
- **Shader (vertex / fragment)** — A small GPU program; the vertex shader moves points, the fragment (pixel) shader colors them. *In games:* hit-flash, dissolve effects, lighting — all live here.
- **Material** — A configured shader + its property values (textures, colors). *In games:* what you assign to a sprite to give it a look.
- **UV** — 2D coordinates mapping a texture onto geometry. *In games:* how a sprite or model knows which part of an image to show.
- **Normal map** — A texture encoding surface direction so flat art catches light in 3D-looking ways. *In games:* makes 2D sprites react to dynamic lights with fake depth.
- **Post-processing** — Full-screen effects applied after the scene renders (bloom, vignette, chromatic aberration). *In games:* the "atmosphere pass" that makes a scene read as a real game.

## 🌐 Networking & Multiplayer (W8)
- **TCP vs UDP** — TCP guarantees ordered, complete delivery (slower); UDP is fast and unreliable (packets can drop or reorder). *In games:* fast action games use UDP and handle loss themselves; TCP is for things that must arrive.
- **Authority** — Who is the source of truth for game state. *In games:* server authority means the server decides outcomes, so a hacked client can't cheat.
- **Replication / RPC** — Replication keeps state in sync across machines; a Remote Procedure Call invokes a function on another machine. *In games:* "spawn this enemy on all clients," "tell the server I fired."
- **Client-side prediction** — The client acts on input immediately instead of waiting for the server. *In games:* movement feels instant despite network latency.
- **Reconciliation** — Correcting the client when the server's authoritative result differs from its prediction. *In games:* fixes the small mispredictions from prediction without a visible snap.
- **Lag compensation** — The server rewinds time to where a player *saw* things when judging a hit. *In games:* your shots land where you aimed even with ping.
- **Serialization** — Converting objects to bytes (to send over the network or save to disk) and back. *In games:* both save files and network packets depend on it.

## 🚀 Production, Cloud & DevOps (W8, W10)
- **Profiling** — Measuring where time and memory actually go before optimizing. *In games:* find the real hotspot instead of guessing — measure first, then fix.
- **Container** — A lightweight, isolated package of an app plus everything it needs to run identically anywhere. *In games:* run the dedicated server the same on a laptop and in the cloud.
- **Image** — The read-only blueprint a container is created from, built from a `Dockerfile`. *In games:* the shippable artifact for Ashfall's server.
- **CI/CD** — Continuous Integration (auto build + test every change) and Continuous Delivery/Deployment (auto ship it). *In games:* every push builds and tests Ashfall, so "it works on my machine" stops being an excuse.
- **Infrastructure as Code (IaC)** — Defining servers and networks in text files instead of clicking dashboards. *In games:* stand up (and tear down) the whole server infra reproducibly.
- **Terraform** — A popular IaC tool; you declare resources and it plans/applies the changes. *In games:* provisions Ashfall's AWS Kubernetes cluster from code.
- **Kubernetes (K8s)** — A system that runs and manages containers across machines (pods, services, deployments). *In games:* keeps the dedicated server running, restarts it if it dies, and scales it.

---

[↑ Back to README](README.md)  ·  [📚 Resources →](RESOURCES.md)  ·  [🎮 Game Overview](GAME_OVERVIEW.md)  ·  [⚔️ Quest Log](QUEST_LOG.md)  ·  [📊 Progress](PROGRESS.md)
