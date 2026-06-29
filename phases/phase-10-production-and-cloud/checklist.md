# ✅ World 10 — Readiness Checklist

Before you face "Ship the Server" and unlock World 11, make sure all of this is true. The boss assumes *every* skill below — it's one end-to-end pipeline that exercises the whole world at once: a trusted, profiled build, automated by CI/CD, containerized and pushed to a registry, deployed to a Terraform-defined cloud cluster, then health-checked, monitored, documented in a runbook, and torn down cleanly. If a box is empty, revisit that lesson.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [🏋️ Exercises](exercises.md) · [🚀 Boss Battle](boss-battle.md)

---

## 📚 Lessons completed
- [ ] **L1 — Profiling & Optimization:** I understand CPU/GPU/memory profiling and the frame budget — and I ran a profiling pass on Ashfall, fixed the real hotspots, and locked in a measured build
- [ ] **L2 — Automated Builds & CI/CD:** I understand CI/CD first principles and GitHub Actions (workflows/jobs/steps/runners) — and I built a pipeline that builds + tests Ashfall on every push and produces artifacts
- [ ] **L3 — Containers & the Cloud:** I understand the cloud model, images vs containers, registries, and Kubernetes pods/services/deployments — and I containerized the W8 server, pushed it to a registry, and ran it on a local k8s cluster
- [ ] **L4 — Infrastructure as Code with Terraform:** I understand IaC, providers, state, and `plan`/`apply` — and I wrote Terraform that stands up an AWS Kubernetes (EKS) cluster reproducibly
- [ ] **L5 — Deploy, Monitor & Operate:** I understand rolling updates, health checks, logs/metrics/alerts, and cost teardown — and I deployed the Ashfall server live with monitoring and a runbook

## 🧰 What I've built / set up
- [ ] A **profiling pass** on Ashfall (CPU/GPU/memory) with the real hotspots fixed and a documented **frame budget**, in the repo
- [ ] A **green GitHub Actions pipeline** in `.github/workflows/` that builds + tests Ashfall on every push and uploads artifacts
- [ ] The **dedicated server containerized** and the image **pushed to a registry**, running on a **local Kubernetes** cluster (pods/service/deployment)
- [ ] **Terraform** (`infra/`) that provisions an AWS Kubernetes (EKS) cluster — `plan`/`apply` clean, state managed, version-controlled
- [ ] The server **deployed to the cluster** with **health checks** (liveness/readiness) and **monitoring** (logs/metrics + an alert), reachable by a client
- [ ] A **runbook + cost teardown** documented (`ops/`), with the **billing alarm armed** — and I've successfully run `terraform destroy` at least once

## 🧠 Skills I can do without looking up
- [ ] Explain why you profile before optimizing and what the 60 FPS frame budget (~16.6 ms) is
- [ ] Explain what CI/CD solves and name a workflow/job/step/runner in GitHub Actions
- [ ] Distinguish a Docker image from a container, and a Pod from a Deployment from a Service
- [ ] Explain what Terraform state is, why `plan` before `apply` matters, and what IaC buys you
- [ ] Explain liveness vs readiness probes and why a documented teardown + billing alarm is non-negotiable

---

## 🔎 Self-test (from memory, no peeking)

1. Why **profile before** you optimize, and what is the **frame budget** at 60 FPS?
   <details><summary>Answer</summary>Because intuition about where time goes is almost always wrong — the real hotspot is rarely the code you suspect, so guessing wastes effort on cheap loops while the expensive bar goes untouched. The <strong>profiler</strong> gives you the actual CPU/GPU/memory breakdown; you fix the biggest bar, then measure again. The <strong>frame budget</strong> is the wall-clock time available per frame: at 60 FPS it's <strong>~16.6 ms</strong> (1000 ÷ 60). All your per-frame work must sum to under that or you drop frames — so you optimize toward a known budget, not toward "feels fast."</details>
2. What does **CI/CD** mean, and what problem does it solve?
   <details><summary>Answer</summary><strong>CI</strong> (Continuous Integration): every push is automatically built and tested, so breakage surfaces in minutes. <strong>CD</strong> (Continuous Delivery/Deployment): the validated build is automatically packaged and (optionally) shipped the same way every time. Together they kill <strong>"works on my machine"</strong> — manual builds are inconsistent, forgettable, and hide breakage until it's expensive to fix. CI/CD makes building, testing, and shipping a deterministic, automated, version-controlled process the whole team can trust, with a green check or red X on every commit.</details>
3. What's the difference between a Docker **image** and a **container**, and how do **Pod / Deployment / Service** relate in Kubernetes?
   <details><summary>Answer</summary>An <strong>image</strong> is the immutable built artifact (server + runtime, layered and frozen); a <strong>container</strong> is a running instance of that image. You ship the image because it's identical everywhere — build once, push to a registry, run the same bytes anywhere. In Kubernetes: a <strong>Pod</strong> runs one (or a few) containers and is disposable; a <strong>Deployment</strong> keeps a desired number of identical Pods alive and does rolling updates to new image versions; a <strong>Service</strong> gives those churning Pods a stable address so clients can reach them. Image = what runs; Pod = where it runs; Deployment = how many/which version; Service = how to reach it.</details>
4. What is **Terraform state**, and why is `terraform plan` before `apply` important?
   <details><summary>Answer</summary><strong>State</strong> is Terraform's record mapping each resource block in your config to the real cloud resource it created (IDs and all). It's how Terraform knows what already exists; lose it and Terraform may recreate duplicates or orphan running infra it can no longer manage or destroy (a silent bill). <strong><code>plan</code></strong> computes the diff between your files and reality and shows exactly what it will create/change/destroy <em>before touching anything</em> — your safety rail to catch an accidental "destroy the cluster" and review the change. Only after the plan looks right do you <code>apply</code>. Click-ops gives you neither a diff nor an undo; IaC gives you both.</details>
5. What's the difference between **liveness** and **readiness** health checks, and why is a documented **teardown + billing alarm** non-negotiable?
   <details><summary>Answer</summary>A <strong>liveness</strong> probe asks "are you alive or wedged?" — fail it and Kubernetes restarts the Pod. A <strong>readiness</strong> probe asks "ready for traffic right now?" — fail it and the Service stops routing to that Pod (e.g. during startup/overload) without killing it. Liveness = restart-if-dead; readiness = route-only-if-ready. The <strong>teardown + billing alarm</strong> is non-negotiable because cloud resources bill by the hour whether used or not: a forgotten EKS cluster or load balancer is the classic four-figure surprise. A one-command teardown (<code>terraform destroy</code> + any manual leftovers) lets you spin up to learn and go to zero when done, and a billing alarm catches creep before it hurts. Knowing how to delete it all is as important as knowing how to build it.</details>

---

## 🚀 Boss readiness
- [ ] Ashfall has a **profiled, trusted build** — the thing I'm about to automate is worth automating
- [ ] A **green CI/CD pipeline** builds, tests, and **containerizes** the dedicated server automatically on push
- [ ] The server image is **pushed to a registry**, and I can deploy it to **Kubernetes** (pods/service/deployment)
- [ ] The cloud infrastructure is **defined in Terraform** — `plan`/`apply` clean, reproducible, version-controlled
- [ ] The deployed server has **health checks and monitoring** (logs/metrics + an alert) and is **reachable by a client**
- [ ] I've written a **runbook** and a **cost teardown**, the **billing alarm is armed**, and I've run `terraform destroy` cleanly
- [ ] I've skimmed the [boss battle](boss-battle.md) and I'm ready to apply the world (no tutorials)

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I completed Side Quest 1 — Manual Approval Gate in CI/CD (+50 XP)
- [ ] (Optional) I completed Side Quest 2 — Autoscaling Experiment (+50 XP)

---

> All checked? → [🚀 Face the Boss Battle: Ship the Server](boss-battle.md)

[↑ Phase Home](README.md) · [↑ Home](../../README.md)
