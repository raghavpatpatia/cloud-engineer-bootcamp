# 👹 Boss Battle — The "Works on My Machine" Incident

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 6 — AWS |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Priya <priya@cloudforge.inc>
To:      You
Subject: [INCIDENT-051] Marcus's TaskFlow image won't run on a clean machine

We tried to deploy Marcus's "containerized" TaskFlow to a fresh staging
box this morning. It's a disaster:

  • `docker compose up` fails / the API container crashes on boot
  • When it does start, curl to the API just hangs — wrong port?
  • The API logs scream that it can't reach the database
  • And the one time it limped along, all the tasks vanished on restart

Marcus is out today. I'm handing you his Dockerfile and compose.yaml
(below). They're broken in several ways. Fix them so that a clean
`docker compose up` gives us a WORKING, PERSISTENT API. You've done every
piece of this in the lessons — now do it under fire.

— Priya
```

> ⚔️ **Boss Battle rules:** No tutorials, no step-by-step. Use your notes, the docs, your own working files, and your head. You win when every victory condition passes **and you can explain why each fix was needed.**

---

## 🗂️ The broken artifacts

Marcus's **`Dockerfile`** (broken):

```dockerfile
FROM node:20-slim
COPY . .
RUN npm install
EXPOSE 8080
CMD ["node"]
```

Marcus's **`compose.yaml`** (broken):

```yaml
services:
  api:
    build: .
    ports:
      - "3000:8080"
    environment:
      DB_HOST: localhost
      DB_USER: taskflow
      DB_PASSWORD: taskflow_pw
      DB_NAME: taskflow

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: taskflow
      POSTGRES_PASSWORD: wrong_password
      POSTGRES_DB: taskflow
```

---

## 🎯 Your mission

Replace these with corrected files in a working TaskFlow copy, then prove the fixed stack runs and persists.

There are **at least five distinct defects** across the two files. Find and fix them so that:

1. The image builds and the API **actually starts** (and stays up).
2. `curl http://localhost:3000/tasks` reaches the API — **correct port mapping**.
3. The API can **reach the database** (right host, matching credentials).
4. Postgres **data survives** a `docker compose down` + `up` (a volume).
5. The API waits for the DB to be **ready** before connecting (no crash-on-boot race).

Work in a scratch copy so you don't clobber your good files:

```bash
cp -r ~/projects/taskflow ~/projects/taskflow-boss
cd ~/projects/taskflow-boss
# overwrite Dockerfile and compose.yaml with Marcus's broken versions, then fix them
```

---

## 🏆 Victory conditions

- [ ] `docker compose up -d --build` starts **both** `api` and `db`, and they stay running
- [ ] `curl http://localhost:3000/tasks` returns a valid response (not a hang / connection refused)
- [ ] Creating a task via `curl -X POST .../tasks` works and the API does **not** report DB connection errors in `docker compose logs`
- [ ] After `docker compose down` then `docker compose up -d`, previously created tasks **still exist**
- [ ] You can name each of the 5+ defects and explain the fix

---

## 🧪 How you'll know you won

```bash
docker compose up -d --build
docker compose ps                         # both services up/healthy
curl -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"survived the boss"}'
curl http://localhost:3000/tasks          # task present
docker compose down && docker compose up -d
curl http://localhost:3000/tasks          # task STILL present
```

If that last `curl` shows your task after a full down/up cycle, the stack is correct and persistent. 🏆

---

<details>
<summary>🔎 Reference solution — only after you've tried! (the defects)</summary>

**Defects in the Dockerfile**
1. **`CMD ["node"]`** launches the Node REPL, not the app — the container has nothing to serve and effectively does nothing useful. Fix: `CMD ["npm", "start"]` (or `["node", "index.js"]`).
2. **`EXPOSE 8080`** doesn't match the app's port (3000), which also drives the wrong compose mapping. Fix: `EXPOSE 3000`.
3. **`COPY . .` before installing deps** (and no `WORKDIR`, no layer-friendly ordering) bloats the image and re-installs on every change; with no `.dockerignore`, the host `node_modules` can leak in. Fix: set `WORKDIR /app`, copy `package*.json` first, `RUN npm ci --omit=dev`, then `COPY . .`, and add a `.dockerignore`.

**Defects in compose.yaml**
4. **`DB_HOST: localhost`** — from inside the `api` container, `localhost` is the api container itself, not Postgres. Fix: `DB_HOST: db` (the service name).
5. **`ports: "3000:8080"`** maps to the wrong container port. With the app on 3000, it should be `"3000:3000"` (host:container).
6. **Mismatched DB password** — `api` uses `taskflow_pw` but the `db` sets `POSTGRES_PASSWORD: wrong_password`. Fix: make them match.
7. **No volume on Postgres** — data is lost on `down`/`up`. Fix: add a named volume mounted at `/var/lib/postgresql/data`.
8. **No `depends_on`/healthcheck** — the API can start before Postgres is ready and crash. Fix: add a healthcheck on `db` and `depends_on: { db: { condition: service_healthy } }` on `api`.

**Corrected `Dockerfile`**
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Corrected `.dockerignore`**
```dockerignore
node_modules
.git
.env
*.db
*.sqlite
Dockerfile
.dockerignore
```

**Corrected `compose.yaml`**
```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_USER: taskflow
      DB_PASSWORD: taskflow_pw
      DB_NAME: taskflow
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: taskflow
      POSTGRES_PASSWORD: taskflow_pw
      POSTGRES_DB: taskflow
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskflow"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  db-data:
```
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🐳 **Achievement unlocked: Captain Container** — you can package, run, persist, and orchestrate any app
- 🔓 **World 6 — AWS** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 5 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: "works on my machine" is now "works on *every* machine." The same image you just fixed is the one you'll push to a real cloud server next world.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [☁️ Enter World 6 →](../phase-06-aws/README.md)
