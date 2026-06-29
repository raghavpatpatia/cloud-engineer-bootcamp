# ✅ World 4 — Readiness Checklist

Before you face "The Infinite Dungeon" and unlock World 5, make sure all of this is true. The boss assumes *every* skill below — it's one infinite, navigable world that exercises the whole world at once: the right data structures, a grid seen as a graph, A\* pathfinding, procedural generation, and a spatial grid for neighbor queries. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Big-O & Data Structures:** I can reason about complexity and pick arrays / `List` / `Dictionary` / `HashSet` / `Queue` / `Stack` by access pattern — and I built Ashfall's tile-map data model
- [ ] **L2 — Graphs, Grids & Traversal:** I can treat a grid as a graph (neighbors), run BFS/DFS, and flood-fill — and I built connectivity checks + BFS reachability over the dungeon grid
- [ ] **L3 — A\* Pathfinding:** I understand A\* = Dijkstra + an admissible heuristic, open/closed sets, and Manhattan distance — and I built a reusable `Pathfinder` returning a path of tiles
- [ ] **L4 — Procedural Generation & Spatial Grids:** I understand seeded PRNG, room/corridor generation, and a spatial hash grid — and I built Ashfall's dungeon generator + a spatial grid for fast neighbor queries

## 🧰 What I've built / set up
- [ ] A `TileMap` data model using the right structure for O(1) coordinate lookup, in `Assets/Scripts/World`
- [ ] A `GridGraph` exposing walkable neighbors, with BFS/DFS and a flood-fill connectivity check
- [ ] A reusable `Pathfinder` (A\* with open/closed sets + Manhattan heuristic) returning a tile path, in `Assets/Scripts/AI`
- [ ] A `DungeonGenerator` (seeded PRNG → rooms + corridors, guaranteed connected) in `Assets/Scripts/World`
- [ ] A `SpatialHashGrid` answering "entities near a point" in near-constant time
- [ ] All of it committed on branches and merged/pushed

## 🧠 Skills I can do without looking up
- [ ] Pick the right container for a given access pattern and justify it with Big-O
- [ ] Write BFS (Queue) and DFS (Stack) and use flood fill to prove connectivity
- [ ] Implement A\* — open set by `f = g + h`, closed set, `cameFrom` reconstruction (reversed!)
- [ ] Explain why the heuristic must be admissible and why Manhattan fits a 4-neighbor grid
- [ ] Generate a seeded, repeatable dungeon and guarantee it's fully connected
- [ ] Use a spatial hash grid to answer neighbor queries without an O(N) scan

---

## 🔎 Self-test (from memory, no peeking)

1. You query "is (x, y) a wall?" thousands of times a frame. What structure do you use and why not a `List` you scan?
   <details><summary>Answer</summary>A 2D <strong>array</strong> (or a <code>Dictionary&lt;(int,int),Tile&gt;</code> for sparse maps) — <strong>O(1)</strong> lookup by coordinate. Scanning a <code>List</code> is O(n) per query, so it collapses under thousands of frame-time lookups.</details>
2. BFS and DFS differ by one container. Which uses what, and what does that change?
   <details><summary>Answer</summary>BFS uses a <strong>Queue</strong> (FIFO) and expands the nearest frontier first → shortest path in an unweighted grid. DFS uses a <strong>Stack</strong> (LIFO) and dives deep down one branch → good for reachability/flood fill, not shortest path.</details>
3. What is A\* in terms of Dijkstra, and why must its heuristic be admissible?
   <details><summary>Answer</summary>A\* is <strong>Dijkstra + a heuristic</strong>: it orders the open set by <code>f = g + h</code> (cost-so-far + estimate-to-goal) so it searches <em>toward</em> the goal. If <code>h</code> never overestimates the true remaining cost (admissible — e.g. Manhattan on a 4-neighbor grid), A\* is guaranteed to return a shortest path.</details>
4. You generated rooms but one is unreachable. How do you prove connectivity and fix it?
   <details><summary>Answer</summary><strong>Flood-fill</strong> (BFS/DFS) from one floor tile and count reached floor tiles; if that's fewer than the total floor tiles, regions are walled off. Carve a corridor connecting the disconnected regions (or regenerate) until one flood fill reaches every floor tile.</details>
5. "Which enemies are near the player?" naïvely loops over all N enemies every frame. What's the cost and the fix?
   <details><summary>Answer</summary>O(N) per query (O(N²) if every enemy asks). A <strong>spatial hash grid</strong> buckets entities by cell, so you only check the player's cell and its neighbors — roughly O(1) for the nearby ones, regardless of N.</details>

---

## 👹 Boss readiness
- [ ] I can generate a **random, connected** dungeon from a **seed** every run (and reproduce a run from its seed)
- [ ] I can spawn an enemy that **A\*-paths** from the entrance to the player around the walls
- [ ] I can use a **spatial grid** to answer "enemies near the player" without scanning everything
- [ ] I can explain which data structure / algorithm owns each behavior (map → graph → A\* → generator → spatial grid)
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed Side Quest 1 — Weighted A\* & Jump-Point Pruning (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Quadtree Neighbor Queries (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Infinite Dungeon](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
