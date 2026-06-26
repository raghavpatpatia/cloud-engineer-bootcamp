# 🏋️ World 4 — Exercises

Extra reps to make Express and REST automatic. None are required to advance, but each makes you a sharper backend engineer. The Side Quest awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (Express & curl fluency)

Do these against your TaskFlow API (`npm start` in one terminal, run these in another):

1. Add a route `GET /version` that returns `{ "version": "1.0.0" }` as JSON.
   <details><summary>Hint</summary><code>app.get("/version", (req, res) => res.json({ version: "1.0.0" }))</code></details>
2. Use `curl` to create a task **and** pretty-print the JSON response.
   <details><summary>Hint</summary>Pipe to a formatter: <code>curl ... | python3 -m json.tool</code> (or install <code>jq</code> and pipe to <code>jq</code>).</details>
3. Count how many tasks exist using only `curl` + a SQL query in `db.js`'s file.
   <details><summary>Hint</summary><code>node -e "console.log(require('better-sqlite3')('taskflow.db').prepare('SELECT COUNT(*) AS n FROM tasks').get())"</code></details>
4. Send a `POST /tasks` **without** the `Content-Type` header and observe what `req.body` becomes.
   <details><summary>Hint</summary>Without the header, <code>express.json()</code> won't parse it — your `title is required` check should fire (`400`).</details>
5. Add a `GET /tasks/count` route that returns the number of tasks. Watch out for route order vs `/tasks/:id`.
   <details><summary>Hint</summary>Define <code>/tasks/count</code> <strong>before</strong> <code>/tasks/:id</code>, or `:id` will swallow the word "count".</details>

## REST design warm-ups

6. Write down, for each: `GET /tasks`, `POST /tasks`, `DELETE /tasks/5` — what is the resource, the action, and the expected success status code?
7. A client wants "all done tasks, newest first." Sketch the URL using query parameters (don't build it yet).
   <details><summary>Hint</summary><code>GET /tasks?status=done&sort=dueDate&order=desc</code></details>
8. Explain why `PUT /tasks/5` is **idempotent** (sending it twice has the same effect) but `POST /tasks` is not.

---

## 🌟 Side Quest — Input Validation & Friendly Errors (+50 XP)

Right now your API trusts the client. Real APIs don't. Harden TaskFlow so bad input gets a clear **400** instead of a crash or silent garbage.

**Requirements — your `POST /tasks` and `PUT /tasks/:id` must reject, with `400` and a helpful message:**

1. Missing or empty `title` (already partly done — make it reject whitespace-only too).
2. A `title` longer than 200 characters.
3. A `status` that isn't one of `"todo"`, `"in-progress"`, `"done"`.
4. A `dueDate` that isn't a valid `YYYY-MM-DD` date string (when provided).

Add **one reusable validation function** rather than copy-pasting checks into both routes.

```bash
# These should all return 400 with a clear error message:
curl -i -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"   "}'
curl -i -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"ok","status":"banana"}'
curl -i -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"ok","dueDate":"July 4th"}'
```

<details>
<summary>💡 Reference approach (try first!)</summary>

Add a validator in `app.js` and call it at the top of both write routes:

```javascript
const STATUSES = ["todo", "in-progress", "done"];

// Returns an error string, or null if the input is valid.
function validateTask(body, { requireTitle }) {
  const { title, status, dueDate } = body;

  if (requireTitle && (typeof title !== "string" || title.trim() === "")) {
    return "title is required and cannot be empty";
  }
  if (title !== undefined && typeof title === "string" && title.length > 200) {
    return "title must be 200 characters or fewer";
  }
  if (status !== undefined && !STATUSES.includes(status)) {
    return `status must be one of: ${STATUSES.join(", ")}`;
  }
  if (dueDate !== undefined && dueDate !== null) {
    // strict YYYY-MM-DD check
    if (!/^\d{4}-\d{2}-\d{2}$/.test(dueDate) || isNaN(Date.parse(dueDate))) {
      return "dueDate must be a valid date in YYYY-MM-DD format";
    }
  }
  return null;
}
```

In `POST /tasks`:

```javascript
const error = validateTask(req.body, { requireTitle: true });
if (error) return res.status(400).json({ error });
```

In `PUT /tasks/:id` (title optional on update):

```javascript
const error = validateTask(req.body, { requireTitle: false });
if (error) return res.status(400).json({ error });
```

🎯 **Side quest complete when:** all three bad-input `curl`s above return `400` with a readable message, valid requests still succeed, and validation logic lives in one shared function. Add **+50 XP** to PROGRESS.md.
</details>

> 💡 Bonus: add tests for these validation cases to `tests/tasks.test.js` — then you can refactor the validator fearlessly.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
