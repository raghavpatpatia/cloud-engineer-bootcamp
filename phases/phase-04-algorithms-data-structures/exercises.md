# 🏋️ World 4 — Exercises

Extra reps to make the *algorithms* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "The Infinite Dungeon" demands — picking the right container, treating a grid as a graph, searching it efficiently, and making neighbor queries fast. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (complexity, structures, graphs, search & generation)

1. You need to ask "is tile (x, y) a wall?" thousands of times per frame. Which structure, and why not a `List<Tile>` you scan?
   <details><summary>Hint</summary>A 2D array (or a <code>Dictionary&lt;(int,int),Tile&gt;</code> for sparse maps) gives <strong>O(1)</strong> lookup by coordinate. Scanning a <code>List</code> is O(n) per query — death by a thousand frames.</details>
2. BFS uses a `Queue` and DFS uses a `Stack`. What does that one swap actually change about the search?
   <details><summary>Hint</summary>A Queue is FIFO, so BFS expands the <em>nearest</em> frontier first → shortest path in an unweighted grid. A Stack is LIFO, so DFS dives deep down one branch first → great for "can I reach it / flood fill," not shortest path.</details>
3. Why must A\*'s heuristic be **admissible** (never overestimate the real cost)?
   <details><summary>Hint</summary>If the heuristic can overestimate, A\* may close the goal via a costlier route and return a non-shortest path. Manhattan distance on a 4-neighbor grid never overestimates, so it stays optimal — and faster than Dijkstra because it aims toward the goal.</details>
4. What's the difference between A\* and Dijkstra, in one sentence?
   <details><summary>Hint</summary>A\* <em>is</em> Dijkstra plus a heuristic: it prioritizes nodes by <code>g + h</code> (cost-so-far + estimate-to-goal) instead of just <code>g</code>, so it explores toward the goal instead of in all directions.</details>
5. Why use a `HashSet` for the "closed set" instead of a `List`?
   <details><summary>Hint</summary>You ask "have I already visited this node?" constantly. <code>HashSet.Contains</code> is O(1); <code>List.Contains</code> is O(n). Same reason "visited" tracking in BFS/DFS uses a set.</details>
6. You generate rooms randomly and some are unreachable. How do you *prove* the dungeon is fully connected — and what do you do if it isn't?
   <details><summary>Hint</summary>Flood-fill (BFS/DFS) from one floor tile and count reached floor tiles. If that count &lt; total floor tiles, some are walled off — carve a corridor between disconnected regions (or regenerate) until one flood fill reaches every floor tile.</details>
7. Why seed your PRNG, and store the seed in the save file?
   <details><summary>Hint</summary>A seeded generator is <strong>deterministic</strong> — the same seed rebuilds the exact same dungeon. Storing the seed lets you reproduce a run for saving/loading and bug reports without serializing every tile.</details>
8. Naïve "enemies within radius R of the player" loops over all N enemies every frame. What's the cost, and what fixes it?
   <details><summary>Hint</summary>That's O(N) per query, O(N²) if every enemy queries. A <strong>spatial hash grid</strong> buckets entities by cell so you only check the player's cell and its neighbors — roughly O(1) for the nearby ones.</details>
9. Manhattan vs Euclidean vs Chebyshev distance — which heuristic for a 4-neighbor (no-diagonal) grid?
   <details><summary>Hint</summary><strong>Manhattan</strong> (|dx| + |dy|). It matches the actual movement cost on a 4-neighbor grid, so it's admissible and tight. Euclidean underestimates (still admissible but looser); Chebyshev fits 8-neighbor diagonal movement.</details>
10. Your A\* returns a path but the agent zig-zags weirdly. Where's the bug usually?
    <details><summary>Hint</summary>Reconstruction. You walk the <code>cameFrom</code> map from goal → start and then forget to <strong>reverse</strong> it, or you push the wrong parent. Double-check you record <code>cameFrom[neighbor] = current</code> only when you find a <em>better</em> g-cost.</details>

---

## 🌟 Side Quest 1 — Weighted A\* & Jump-Point Pruning (+50 XP)

Prove you can *tune the speed/quality tradeoff* of a search, not just run a textbook A\*. Take your `Pathfinder` and make it explore far fewer nodes on big open dungeons by (a) **weighting** the heuristic and (b) **pruning** straight-line runs so you don't expand every cell of a corridor.

**Requirements:**
1. Add a `heuristicWeight` to A\*: priority becomes `g + weight * h`. With `weight = 1` it's exact-optimal; bump it above 1 for a faster, slightly-longer path (a "weighted A\*").
2. Add a count of **nodes expanded** and log it. Show weighted A\* expands measurably fewer nodes than `weight = 1` on an open room.
3. Implement a simple **jump/skip** optimization: when stepping in a straight line through open floor with no forced turns, advance multiple tiles in one expansion instead of one cell at a time (a lightweight jump-point idea).
4. Verify the path is still **valid** (every tile walkable, start→goal connected) even though it explored less.

```
Test: on a 50x50 open dungeon, log nodes-expanded for weight=1 vs weight=1.5 + jumping. The optimized run expands far fewer nodes and still reaches the player with a walkable path.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
// Weighted A*: the ONLY change from plain A* is the priority key.
// f = g + weight * h.  weight == 1 → optimal (classic A*).
//                      weight  > 1 → "greedier", expands fewer nodes, path may be slightly longer.
float Priority(Node n, Vector2Int goal, float weight)
    => n.g + weight * Heuristic(n.pos, goal);   // Heuristic = Manhattan on a 4-neighbor grid

// Lightweight "jump": while the next step is a straight, unforced run through
// open floor, skip ahead instead of enqueuing every single cell.
Vector2Int Jump(Vector2Int from, Vector2Int dir, Vector2Int goal)
{
    var p = from + dir;
    while (Walkable(p) && p != goal && !HasForcedNeighbor(p, dir))
        p += dir;                 // collapse a corridor/open run into one expansion
    return p;                     // enqueue p, not every tile between
}
```

- Weighting `h` makes A\* aim harder at the goal: fewer nodes expanded, at the cost of (sometimes) a path 5–15% longer. That tradeoff is *exactly* what shipped games tune.
- The jump idea is the seed of **Jump Point Search**: on uniform-cost grids, long straight runs have no decision points, so expanding every cell is wasted work — skip to the next "interesting" tile.
- Counting nodes-expanded is the honest metric: an optimization you can't *measure* isn't an optimization.

🎯 **Side quest complete when:** weighted A\* + jumping expands measurably fewer nodes than plain A\* on an open dungeon, and still returns a walkable start→player path. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Quadtree Neighbor Queries (+50 XP)

Your spatial *hash* grid is great for uniform density — but when entities clump (a swarm in one room, an empty corridor elsewhere) a **quadtree** adapts: it subdivides only where it's crowded. Build one and use it to answer "all entities within a rectangle / radius of the player" faster than a brute-force scan.

**Steps:**
1. Implement a `Quadtree` node holding up to `capacity` points; when it overflows, **subdivide** into four child quadrants and redistribute.
2. Add `Insert(entity, position)` and `Query(Rect area)` returning every entity whose position falls in `area` (prune whole branches whose bounds don't intersect `area`).
3. Wire a radius query: query the bounding box, then filter by actual distance.
4. Compare against a brute-force loop: same results, far fewer distance checks when entities clump.

```
Test: spawn 500 entities clustered in one quadrant. A radius query around the player returns the same set as brute force, but visits a fraction of the nodes (log the comparison-count).
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
public class Quadtree
{
    private readonly Rect bounds;
    private readonly int capacity;
    private readonly List<(int id, Vector2 pos)> points = new();
    private Quadtree[] children;   // null until subdivided (NW, NE, SW, SE)

    public Quadtree(Rect bounds, int capacity = 4) { this.bounds = bounds; this.capacity = capacity; }

    public bool Insert(int id, Vector2 pos)
    {
        if (!bounds.Contains(pos)) return false;            // not mine → prune
        if (children == null && points.Count < capacity) { points.Add((id, pos)); return true; }
        if (children == null) Subdivide();                  // overflow → split
        foreach (var c in children) if (c.Insert(id, pos)) return true;
        return false;
    }

    public void Query(Rect area, List<int> results)
    {
        if (!bounds.Overlaps(area)) return;                 // prune whole branch
        foreach (var (id, pos) in points) if (area.Contains(pos)) results.Add(id);
        if (children != null) foreach (var c in children) c.Query(area, results);
    }

    private void Subdivide() { /* make 4 child quadtrees over the 4 sub-rects, then re-insert points */ }
}
```

- The win is **pruning**: `Overlaps`/`Contains` rejects entire subtrees the query can't touch, so a clustered query visits a tiny fraction of nodes.
- Hash grid vs quadtree is a real engineering choice: hash grid is simplest and great for uniform density; a quadtree adapts to clumping. Knowing *both* — and when each wins — is the point.
- Always validate against brute force: identical result set, fewer comparisons. That's how you trust a spatial structure.

🎯 **Side quest complete when:** the quadtree returns the same entities as a brute-force radius scan while visiting far fewer nodes on clustered data. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
