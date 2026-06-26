# ✅ World 4 — Readiness Checklist

Before you face the Boss Battle and unlock World 5, make sure all of this is true. If any box is empty, revisit that lesson — the Boss Battle assumes every skill below.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 What I've built (in `~/projects/taskflow`)
- [ ] An Express server that starts with `npm start`
- [ ] `GET /tasks` and `GET /tasks/:id` (with `404` for missing ids)
- [ ] `POST /tasks` returning `201`, `PUT /tasks/:id` returning `200`, `DELETE /tasks/:id` returning `204`
- [ ] `express.json()` registered before the routes
- [ ] Data persisted in a **SQLite** file (`taskflow.db`) that survives restarts
- [ ] Code split into `app.js` (exports app) and `index.js` (calls listen)
- [ ] Jest + Supertest tests that all pass with `npm test`
- [ ] Each step committed to git (`git log` tells the story)

## 🧠 Skills I can do without looking up
- [ ] Explain REST: resources, collection vs item URLs, method → action
- [ ] Map CRUD to the right HTTP method **and** status code (201/200/204/400/404)
- [ ] Read a request body via `req.body` (and why `express.json()` is required)
- [ ] Use `req.params.id` and `req.query`
- [ ] Write a SQL query with `?` placeholders (and say why)
- [ ] Send `POST`/`PUT`/`DELETE` requests with `curl` (`-X`, `-H`, `-d`, `-i`)

## 🔎 Self-test (do this from memory)
Without looking at your code, in a scratch file write a single Express route from scratch:

> `PUT /tasks/:id` that updates a task's `status`, returns `404` if the task doesn't exist, `400` if `status` is missing, and the updated task as JSON otherwise.

<details>
<summary>✅ One correct solution</summary>

```javascript
app.put("/tasks/:id", (req, res) => {
  const task = db.prepare("SELECT * FROM tasks WHERE id = ?").get(req.params.id);
  if (!task) return res.status(404).json({ error: "Task not found" });

  const { status } = req.body;
  if (status === undefined) return res.status(400).json({ error: "status is required" });

  db.prepare("UPDATE tasks SET status = ? WHERE id = ?").run(status, req.params.id);
  res.json(db.prepare("SELECT * FROM tasks WHERE id = ?").get(req.params.id));
});
```

If you wrote that — the right method, the `404` check, the `400` check, and a JSON response — without peeking, you're ready.
</details>

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed the Side Quest (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Flaky API](boss-battle.md)

[← World Home](README.md)
