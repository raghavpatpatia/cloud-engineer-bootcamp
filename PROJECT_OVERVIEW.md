# 📦 Project Overview — The Task Manager Platform

Everything you build in this bootcamp feeds **one** real application. You don't make throwaway demos — you grow a single product from a folder on your laptop into a production-grade, auto-scaling cloud platform.

This is your **golden thread**. Keep it. Don't delete it between phases.

[↑ Back to README](README.md)

---

## 🎬 The story

**CloudForge Inc.** has too many sticky notes. Engineers lose track of work, managers can't see what's in progress, and the CEO keeps asking "where are we on the launch?" Your team has been asked to build the company's own internal tool: **TaskFlow**, a Task Manager Platform.

You're the engineer who builds it — and the one who keeps it running.

---

## 🧱 What it actually is

At its core, TaskFlow lets a user:

- Create a task (title, description, status, due date)
- List all tasks
- Update a task (e.g. mark it "done")
- Delete a task

That's it. A deliberately **simple feature set** — because the *hard* part of being a Cloud Engineer isn't the app, it's everything around it: running it reliably, securely, automatically, and at scale.

> 🎯 The app stays small on purpose. The **infrastructure** is where you grow.

---

## 📈 How it evolves, world by world

```mermaid
flowchart TD
    L2["🐧 World 2 — Linux<br/>Create the project folder & files"] --> L3
    L3["🌿 World 3 — Git<br/>Version it, push to GitHub"] --> L4
    L4["⚙️ World 4 — Backend<br/>Build the REST API (real CRUD)"] --> L5
    L5["🐳 World 5 — Docker<br/>Containerize it"] --> L6
    L6["☁️ World 6 — AWS<br/>Deploy to an EC2 server"] --> L7
    L7["🔁 World 7 — CI/CD<br/>Deploy automatically on every push"] --> L8
    L8["🏗️ World 8 — Terraform<br/>Define all infra as code"] --> L9
    L9["☸️ World 9 — Kubernetes<br/>Scale & self-heal"] --> L10
    L10["🚀 World 10 — Production<br/>Domain, HTTPS, monitoring, the works"]
```

| World | What changes about TaskFlow |
|------:|------------------------------|
| 1 · Internet | You learn what an HTTP request *is* — the thing your API will answer |
| 2 · Linux | The project is born: a folder, files, a backup script |
| 3 · Git | It becomes a real repo with history, branches, and a home on GitHub |
| 4 · Backend | It becomes a working **REST API** with real endpoints and data |
| 5 · Docker | It runs the same everywhere, packaged in a container |
| 6 · AWS | It goes **live** on a real server with a public IP |
| 7 · CI/CD | It deploys **itself** every time you push code |
| 8 · Terraform | Its entire server + network is reproducible from code |
| 9 · Kubernetes | It runs as multiple replicas that heal and scale on demand |
| 10 · Production | It gets a domain, HTTPS, health checks, and monitoring |

---

## 🏗️ Where you're headed (the final architecture)

You don't need to understand this yet — but here's the system you'll have built by Launch Day. Come back and re-read this after each world; more of it will make sense each time.

```mermaid
flowchart TB
    User["👤 User's Browser"] -->|HTTPS| DNS["🌐 DNS / Domain"]
    DNS --> LB["⚖️ Load Balancer"]
    LB --> Ingress["☸️ Kubernetes Ingress"]
    subgraph K8s["Kubernetes Cluster"]
        Ingress --> Svc["Service"]
        Svc --> P1["🟦 Pod: TaskFlow API"]
        Svc --> P2["🟦 Pod: TaskFlow API"]
        Svc --> P3["🟦 Pod: TaskFlow API"]
    end
    P1 --> DB["🗄️ Database"]
    P2 --> DB
    P3 --> DB
    subgraph CICD["Delivery Pipeline"]
        GH["🌿 GitHub"] -->|push| CI["🔁 CI/CD"]
        CI -->|build & push image| Reg["📦 Container Registry"]
        CI -->|deploy| K8s
    end
    TF["🏗️ Terraform"] -.->|provisions| K8s
    TF -.->|provisions| DB
    TF -.->|provisions| LB
    style K8s fill:#eff6ff,stroke:#2563eb
    style CICD fill:#f0fdf4,stroke:#16a34a
```

---

## 🛠️ The tech stack (and why)

We keep choices boring and beginner-friendly. Each tool earns its place by solving a problem you'll *feel* before you adopt it.

| Layer | Tool | Why this one |
|-------|------|--------------|
| Language | **Node.js + Express** | Tiny, readable, huge ecosystem, runs anywhere |
| Data | **SQLite → PostgreSQL** | Start with a file, graduate to a real database |
| Container | **Docker** | The industry default for packaging apps |
| Cloud | **AWS** | The market leader; skills transfer everywhere |
| CI/CD | **GitHub Actions** | Lives next to your code, free to start |
| IaC | **Terraform** | Cloud-agnostic, the most in-demand IaC tool |
| Orchestration | **Kubernetes** | The standard for running containers at scale |

> 🔄 If you already know another language, you can adapt the backend — but follow along in Node first so the instructions match.

---

## 📂 Where the project lives in this repo

The **instructions** for building TaskFlow live inside each world's lessons (especially the **Project Mission** section of every lesson). The **code you write** lives in your *own* project folder, which you'll create in World 2 (Linux) — typically `~/projects/taskflow` inside WSL2.

> 📌 Rule of thumb: this bootcamp repo holds the *teaching*. Your `~/projects/taskflow` repo holds the *product*.

---

## 🎓 What "done" looks like

When you finish, you'll be able to point a friend, a recruiter, or an interviewer at:

- A **GitHub repo** with clean history and a real README
- A **live URL** serving your API over HTTPS
- A **pipeline** that ships changes automatically
- **Terraform** that recreates the whole stack from scratch
- A **Kubernetes** deployment that survives a pod dying and scales under load

That's not a tutorial project. That's a portfolio.

---

[↑ Back to README](README.md)  ·  [📜 Rules →](RULES.md)  ·  [🚀 Start World 0 →](phases/phase-00-environment-setup/)
