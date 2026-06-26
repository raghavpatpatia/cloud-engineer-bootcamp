# 🏋️ World 5 — Exercises

Extra reps to make Docker muscle-memory. None are required to advance, but each makes the Boss Battle (and World 6) smoother. Side Quests award **+50 XP** each.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (Docker fluency)

Do these in your **Ubuntu** terminal (or Play with Docker):

1. List all images on your machine.
   <details><summary>Hint</summary>`docker images`</details>
2. List **all** containers, including stopped ones.
   <details><summary>Hint</summary>`docker ps -a`</details>
3. Run `alpine` and have it print "hi", then exit.
   <details><summary>Hint</summary>`docker run --rm alpine echo hi`</details>
4. Pull the `postgres:16` image without running it.
   <details><summary>Hint</summary>`docker pull postgres:16`</details>
5. Remove a stopped container and a dangling image.
   <details><summary>Hint</summary>`docker rm <name>` and `docker image prune`</details>
6. Show the disk space Docker is using.
   <details><summary>Hint</summary>`docker system df`</details>

## Build & Compose warm-ups

7. Rebuild TaskFlow and tag it `taskflow:dev`, then list it.
   <details><summary>Hint</summary>`docker build -t taskflow:dev . && docker images | grep taskflow`</details>
8. With your stack up, open a `psql` shell and list the tables.
   <details><summary>Hint</summary>`docker compose exec db psql -U taskflow -d taskflow -c "\dt"`</details>
9. Stream only the `api` service's logs.
   <details><summary>Hint</summary>`docker compose logs -f api`</details>

---

## 🌟 Side Quest — Shrink the Image with a Multi-Stage Build (+50 XP)

Your current image carries build tooling it never needs at runtime. A **multi-stage build** uses one stage to install/build and a smaller final stage that copies in only what's needed — often cutting image size dramatically.

First, baseline the current size:

```bash
cd ~/projects/taskflow
docker build -t taskflow:fat .
docker images taskflow:fat        # note the SIZE
```

Now create a multi-stage `Dockerfile` (and make sure your `.dockerignore` excludes `node_modules`, `.git`, `*.db`, `.env`):

```dockerfile
# ---- Stage 1: build/install dependencies ----
FROM node:20-slim AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# ---- Stage 2: lean runtime image ----
FROM node:20-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
# Copy only the installed deps and the source — no build tooling
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

Build the slim version and compare:

```bash
docker build -t taskflow:slim .
docker images | grep -E "taskflow:(fat|slim)"
```

🎯 **Side quest complete when:** `taskflow:slim` builds and runs (`curl /tasks` works), and you can state the size difference between `taskflow:fat` and `taskflow:slim` and explain *why* the final stage is smaller (it never carries the build context or layers it didn't copy). Add **+50 XP**.

> 💡 Bonus: try the `node:20-alpine` base for an even smaller image and note any trade-offs (Alpine uses musl libc — most Node apps are fine, some native modules need extra packages).

---

## 🌟 Side Quest — Master the `.dockerignore` (+50 XP)

A fat build context slows builds and can leak secrets. Measure and fix it.

```bash
cd ~/projects/taskflow

# Temporarily rename .dockerignore to see the difference
mv .dockerignore .dockerignore.bak
docker build -t taskflow:noignore .   # watch the "transferring context" size at the top

# Restore it and rebuild
mv .dockerignore.bak .dockerignore
docker build -t taskflow:ignore .     # context should be much smaller
```

🎯 **Complete when:** you can describe how much smaller the build context becomes with `.dockerignore`, and name at least two things it should always exclude (`node_modules`, `.git`, `.env`, `*.db`). Add **+50 XP**.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
