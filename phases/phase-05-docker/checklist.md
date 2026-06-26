# ✅ World 5 — Readiness Checklist

Before you face the Boss Battle and unlock World 6, make sure all of this is true. If any box is empty, revisit that lesson — the boss assumes you can do all of it.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Tools & setup
- [ ] Docker is installed (or Play with Docker is available) and `docker info` shows a reachable daemon
- [ ] `docker run hello-world` succeeds
- [ ] TaskFlow has a committed `Dockerfile` and `.dockerignore`
- [ ] TaskFlow has a committed `compose.yaml` with `api` + `db` services

## 🧠 Skills I can do without looking up
- [ ] Explain the difference between an **image** and a **container**
- [ ] Build an image: `docker build -t taskflow:1.0 .`
- [ ] Run a container with a port mapping: `docker run -d -p 3000:3000 ...`
- [ ] Read logs (`docker logs`) and get a shell inside (`docker exec -it ... sh`)
- [ ] Persist data with a **named volume** (`-v name:/path`)
- [ ] Bring a multi-container stack up/down (`docker compose up -d` / `down`)
- [ ] Explain why services connect by **service name**, not `localhost`

## 🔎 Self-test (do this from memory)
Without notes, in `~/projects/taskflow`:
1. Build the image as `taskflow:test`
2. Run it on host port 3000 with a named volume mounted for its data
3. Create a task via `curl`
4. Remove the container, recreate it with the same volume
5. Confirm the task survived

<details>
<summary>✅ One correct solution</summary>

```bash
cd ~/projects/taskflow
docker build -t taskflow:test .
docker volume create tf-test
docker run -d -p 3000:3000 --name tf \
  -v tf-test:/app/data -e DB_PATH=/app/data/taskflow.db taskflow:test
curl -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"survive"}'
docker rm -f tf
docker run -d -p 3000:3000 --name tf \
  -v tf-test:/app/data -e DB_PATH=/app/data/taskflow.db taskflow:test
curl http://localhost:3000/tasks      # the task is still there
```
</details>

If you did that without peeking — you're ready for the boss.

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I did at least one Side Quest (+50 XP each)

---

> All checked? → [👹 Face the Boss Battle: The "Works on My Machine" Incident](boss-battle.md)

[← World Home](README.md)
