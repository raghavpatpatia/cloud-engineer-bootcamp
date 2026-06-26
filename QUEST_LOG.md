# ⚔️ Quest Log

Every quest and side quest in the bootcamp, in one place. Use this when you want the big picture, or to find a specific challenge.

- **⚔️ Quest** — the main lab in a lesson. Building it = **100 XP**.
- **🌟 Side Quest** — optional bonus. = **50 XP**.
- **👹 Boss Battle** — the world finale. = **500 XP**.

[↑ Back to README](README.md)  ·  [📊 Progress](PROGRESS.md)

---

## 🖥️ World 0 — Environment Setup
- ⚔️ Open a terminal and report your system info
- ⚔️ Install WSL2 + Ubuntu and launch your first Linux shell
- ⚔️ Install VS Code, the WSL extension, and Node.js
- 🌟 Customize your shell prompt
- 👹 **The Broken Workstation** — diagnose and repair a misconfigured environment

## 🌐 World 1 — Internet Fundamentals
- ⚔️ Make your first request with `curl` and read the response
- ⚔️ Inspect headers and status codes against `httpbin.org`
- ⚔️ Resolve a domain to an IP and watch the journey
- 🌟 Trigger and explain a `301`, `404`, and `500`
- 👹 **Trace the Request** — narrate every hop from URL to rendered response

## 🐧 World 2 — Linux
- ⚔️ Navigate the filesystem and create the **TaskFlow** project folder
- ⚔️ Create, move, copy, and read files from the terminal
- ⚔️ Master permissions (`chmod`/`chown`) and ownership
- ⚔️ Manage processes and install software with `apt`
- ⚔️ Write a Bash **backup script** for the project
- 🌟 Schedule the backup with `cron`
- 👹 **The Locked Server** — recover from broken permissions and a stuck process

## 🌿 World 3 — Git
- ⚔️ Initialize a repo and make your first commit
- ⚔️ Branch, switch, and merge
- ⚔️ Create a GitHub repo and push TaskFlow
- ⚔️ Open and merge a Pull Request
- 🌟 Recover a deleted file with `git restore`/`reflog`
- 👹 **The Merge Conflict from Hell** — resolve a tangled multi-branch conflict

## ⚙️ World 4 — Backend Development
- ⚔️ Build a "Hello, world" HTTP server
- ⚔️ Add REST routes (`GET`/`POST`/`PUT`/`DELETE`) for tasks
- ⚔️ Persist tasks in a database
- ⚔️ Return correct status codes and JSON
- ⚔️ Write your first automated tests
- 🌟 Add input validation and error handling
- 👹 **The Flaky API** — find and fix the bugs in a broken backend

## 🐳 World 5 — Docker
- ⚔️ Run your first container
- ⚔️ Write a `Dockerfile` for TaskFlow
- ⚔️ Build and run the TaskFlow image
- ⚔️ Use volumes so data survives restarts
- ⚔️ Orchestrate app + database with Docker Compose
- 🌟 Shrink your image with a multi-stage build
- 👹 **The "Works on My Machine" Incident**

## ☁️ World 6 — AWS
- ⚔️ Create a free-tier account and set a billing alarm
- ⚔️ Launch an EC2 instance (free tier)
- ⚔️ SSH in and configure security groups
- ⚔️ Deploy the TaskFlow container to EC2
- ⚔️ Store artifacts/backups in S3
- 🌟 Create a least-privilege IAM user
- 👹 **The Empty Cloud** — blank account to live app

## 🔁 World 7 — CI/CD
- ⚔️ Create your first GitHub Actions workflow
- ⚔️ Run tests automatically on every push
- ⚔️ Build and push a Docker image in the pipeline
- ⚔️ Deploy automatically to EC2
- 🌟 Add a manual approval gate before production
- 👹 **The 2 AM Deploy** — make deploys safe and automatic

## 🏗️ World 8 — Terraform
- ⚔️ Write your first resource and `terraform apply`
- ⚔️ Define the EC2 instance + security group in code
- ⚔️ Use variables and outputs
- ⚔️ Manage and inspect state
- 🌟 Refactor into reusable modules
- 👹 **Rebuild From Nothing** — `destroy` then recreate the whole stack

## ☸️ World 9 — Kubernetes
- ⚔️ Start a local cluster and run a pod
- ⚔️ Write a Deployment and scale it
- ⚔️ Expose it with a Service
- ⚔️ Watch self-healing (kill a pod, see it return)
- ⚔️ Manage config & secrets
- 🌟 Add a horizontal autoscaler
- 👹 **The Traffic Surge** — survive a load spike

## 🚀 World 10 — Final Production
- ⚔️ Point a domain at your app
- ⚔️ Add HTTPS with a free certificate
- ⚔️ Add health checks and readiness probes
- ⚔️ Set up monitoring and alerts
- ⚔️ Write the production README & runbook
- 🌟 Add structured logging and a dashboard
- 👹 **Launch Day** — ship the whole thing, for real

---

## 🌟 Completionist track

Finish **every 🌟 Side Quest** above to earn the **💯 Completionist** achievement. Tick them off in [PROGRESS.md](PROGRESS.md).

---

[↑ Back to README](README.md)  ·  [🚀 Start World 0 →](phases/phase-00-environment-setup/)
