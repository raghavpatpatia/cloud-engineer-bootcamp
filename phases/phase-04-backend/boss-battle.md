# 👹 Boss Battle — The Flaky API

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 40 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 5 — Docker |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Dana <dana@cloudforge.inc>
To:      You <new-hire@cloudforge.inc>
Subject: [INCIDENT-041] Sam's TaskFlow build is flaky — fix it

A teammate (Sam) hacked together a tasks API while you were heads-down.
QA is filing bugs faster than we can read them:

  • "Creating a task returns 200, not 201."
  • "Sending a request with no body CRASHES the whole server."
  • "Two new tasks ended up with the SAME id."
  • "Deleting a task that doesn't exist returns 200 like it worked."
  • "GET a missing task hangs / returns nothing instead of 404."

I've pasted Sam's app.js below. Find every bug, fix it, and PROVE the
fixes with curl and tests. You wrote a clean API last week — you know
what good looks like. Go.

— Dana
```

> ⚔️ **Boss Battle rules:** No tutorials, no copying your Level 5 file wholesale. Read Sam's code, find the bugs by reasoning about them, fix them in place, and prove each fix. You win when every victory condition is met **and you can explain each bug**.

---

## 🐛 The buggy code

Save this as `flaky-app.js` in a scratch folder (e.g. `~/projects/flaky-api`), `npm init -y`, `npm install express`, and create an `index.js` that does `require("./flaky-app")` + `listen` so you can run it. There are **five** distinct bugs.

```javascript
// flaky-app.js — Sam's TaskFlow API. Looks fine. Isn't.
const express = require("express");
const app = express();

// (Sam swears the body parser is "probably fine")

let tasks = [
  { id: 1, title: "First task", status: "todo" },
];

// READ one
app.get("/tasks/:id", (req, res) => {
  const task = tasks.find((t) => t.id === req.params.id);
  res.json(task);
});

// READ all
app.get("/tasks", (req, res) => {
  res.json(tasks);
});

// CREATE
app.post("/tasks", (req, res) => {
  const task = {
    id: tasks.length + 1,
    title: req.body.title,
    status: req.body.status || "todo",
  };
  tasks.push(task);
  res.status(200).json(task);
});

// DELETE
app.delete("/tasks/:id", (req, res) => {
  const index = tasks.findIndex((t) => t.id === req.params.id);
  tasks.splice(index, 1);
  res.status(200).json({ deleted: true });
});

module.exports = app;
```

### 🔍 The five bugs to hunt

1. **No body parser** — `req.body` is `undefined`, so `POST` with any body (or none) misbehaves/crashes.
2. **Wrong CREATE status** — returns `200` instead of `201 Created`.
3. **Colliding ids** — `id: tasks.length + 1` reuses ids after a delete (delete #2 of 3, create → new id `3` collides).
4. **Type-mismatch lookups** — `t.id === req.params.id` compares a number to a string, so GET-one and DELETE never find anything by id.
5. **No 404 handling** — a missing task returns `null`/empty (GET) or pretends success (DELETE) instead of `404`. The `DELETE` also crashes when `findIndex` returns `-1` and `splice(-1, 1)` removes the wrong row.

---

## 🎯 Your mission

Fix `flaky-app.js` so it behaves like a correct REST API:

- `express.json()` is registered and a missing/empty body never crashes the server.
- `POST /tasks` returns **201** and the created task; rejects a missing `title` with **400**.
- New ids **never collide**, even after deletes.
- `GET /tasks/:id` and `DELETE /tasks/:id` find tasks reliably by id.
- A missing task returns **404** for both GET-one and DELETE; a successful delete returns **204**.

Then **prove it** with curl and a short test file.

---

## 🏆 Victory conditions

- [ ] `POST /tasks` with a valid body returns **`201`** and the new task
- [ ] `POST /tasks` with **no body** returns **`400`** and the server stays up (no crash)
- [ ] Creating, deleting, then creating again yields a **unique** id (no collision)
- [ ] `GET /tasks/:id` returns the right task (200) and a missing id returns **`404`**
- [ ] `DELETE /tasks/:id` returns **`204`** on success and **`404`** when the id doesn't exist
- [ ] You wrote at least 3 passing tests (Jest + Supertest) proving the above
- [ ] You can explain, out loud, the cause of **all five** bugs

---

## 🧪 How you'll know you won

Run these against your fixed server — every line should behave as the comment says:

```bash
# 201 on create
curl -i -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" -d '{"title":"Fixed"}'        # → 201

# 400, NOT a crash, on empty body
curl -i -X POST http://localhost:3000/tasks                          # → 400

# id collision check: create, delete it, create again → ids differ
curl -s -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"A"}'
curl -i -X DELETE http://localhost:3000/tasks/2                       # → 204
curl -s -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"B"}'  # new id ≠ 2

# 404 on missing task
curl -i http://localhost:3000/tasks/9999                              # → 404
curl -i -X DELETE http://localhost:3000/tasks/9999                    # → 404
```

If the server never crashes and every status code matches — you've won.

<details>
<summary>🔎 Reference solution — only after you've tried! (fixed code)</summary>

```javascript
// flaky-app.js — fixed
const express = require("express");
const app = express();

app.use(express.json()); // BUG 1 fix: parse JSON bodies

let tasks = [
  { id: 1, title: "First task", status: "todo" },
];
let nextId = 2; // BUG 3 fix: monotonic id counter, never reused

app.get("/tasks", (req, res) => {
  res.json(tasks);
});

app.get("/tasks/:id", (req, res) => {
  const id = Number(req.params.id); // BUG 4 fix: compare numbers
  const task = tasks.find((t) => t.id === id);
  if (!task) return res.status(404).json({ error: "Task not found" }); // BUG 5 fix
  res.json(task);
});

app.post("/tasks", (req, res) => {
  const body = req.body || {};                 // safe even if undefined
  if (!body.title) {                            // BUG 1/5: reject bad input
    return res.status(400).json({ error: "title is required" });
  }
  const task = {
    id: nextId++,                               // BUG 3 fix
    title: body.title,
    status: body.status || "todo",
  };
  tasks.push(task);
  res.status(201).json(task);                   // BUG 2 fix: 201 Created
});

app.delete("/tasks/:id", (req, res) => {
  const id = Number(req.params.id);             // BUG 4 fix
  const index = tasks.findIndex((t) => t.id === id);
  if (index === -1) return res.status(404).json({ error: "Task not found" }); // BUG 5 fix
  tasks.splice(index, 1);
  res.status(204).send();                       // 204 No Content
});

module.exports = app;
```

**The five fixes, explained:**

| # | Bug | Why it broke | Fix |
|---|-----|--------------|-----|
| 1 | No body parser | `req.body` was `undefined`; reading `.title` threw | `app.use(express.json())` + guard `req.body || {}` |
| 2 | Create returned `200` | Misleads clients/caches that watch for `201` | `res.status(201)` |
| 3 | `id: tasks.length + 1` | After deleting, length drops → new id reuses an old one | A `nextId++` counter that only ever grows |
| 4 | `t.id === req.params.id` | `1 === "1"` is `false` — string vs number | `Number(req.params.id)` before comparing |
| 5 | No `404`; `splice(-1,1)` | Missing task returned empty/"success"; delete removed the wrong row | `find`/`findIndex` guards returning `404` |

</details>

<details>
<summary>🔎 Reference solution — proof tests (Jest + Supertest)</summary>

```javascript
// tests/flaky.test.js
const request = require("supertest");
const app = require("../flaky-app");

test("POST /tasks returns 201 with the task", async () => {
  const res = await request(app).post("/tasks").send({ title: "Fixed" });
  expect(res.statusCode).toBe(201);
  expect(res.body.title).toBe("Fixed");
});

test("POST /tasks with no body returns 400 (no crash)", async () => {
  const res = await request(app).post("/tasks").send();
  expect(res.statusCode).toBe(400);
});

test("ids never collide after delete", async () => {
  const a = await request(app).post("/tasks").send({ title: "A" });
  await request(app).delete(`/tasks/${a.body.id}`);
  const b = await request(app).post("/tasks").send({ title: "B" });
  expect(b.body.id).not.toBe(a.body.id);
});

test("GET and DELETE missing task return 404", async () => {
  expect((await request(app).get("/tasks/9999")).statusCode).toBe(404);
  expect((await request(app).delete("/tasks/9999")).statusCode).toBe(404);
});
```

Run with `npm install --save-dev jest supertest` then `npx jest`. All green = boss defeated.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **⚙️ API Architect** — you can build *and* debug a REST API
- 🔓 **World 5 — Docker** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 4 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: every bug here is one a real engineer ships eventually. The difference between junior and senior isn't never writing bugs — it's *recognising the smell* (wrong status code, string-vs-number, reused id) fast. You just trained that instinct.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🐳 Enter World 5 →](../phase-05-docker/README.md)
