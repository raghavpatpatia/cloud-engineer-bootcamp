# 🏋️ World 10 — Exercises

Extra reps to make the *production engineering* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "Ship the Server" demands — measuring before optimizing, automating the build, containerizing for the cloud, codifying infra, and operating a live server without blowing the budget. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [🚀 Boss Battle](boss-battle.md)

---

## Warm-ups (profiling, CI/CD, containers, IaC, ops)

1. Why must you **profile before** you optimize a build, and what's the **frame budget** at 60 FPS?
   <details><summary>Hint</summary>Your intuition about where time goes is usually wrong — the real hotspot is rarely the loop you suspect. Profiling tells you the <em>actual</em> CPU/GPU/memory breakdown so you fix the biggest bar, not a guess. The <strong>frame budget</strong> is the wall-clock time you have per frame to do everything: at 60 FPS that's <strong>~16.6 ms</strong> (1000 ms ÷ 60). Every system has to fit inside it; if the sum of your work exceeds the budget, you drop frames. "Measure, don't guess" — and know your budget so you know when you've broken it.</details>
2. What does **CI/CD** stand for, and what problem does it actually solve?
   <details><summary>Hint</summary><strong>CI</strong> = Continuous Integration: every push is automatically built and tested, so broken commits surface in minutes instead of at launch. <strong>CD</strong> = Continuous Delivery/Deployment: that validated build is automatically packaged (and optionally shipped) the same way every time. The problem it solves is <strong>"works on my machine"</strong> — manual builds are inconsistent, easy to forget, and hide breakage until it's expensive. CI/CD makes the build a deterministic, automated, version-controlled process anyone can trust.</details>
3. In **GitHub Actions**, what are a **workflow**, a **job**, a **step**, and a **runner**?
   <details><summary>Hint</summary>A <strong>workflow</strong> is a YAML file in <code>.github/workflows/</code> triggered by an event (e.g. <code>on: push</code>). It contains one or more <strong>jobs</strong>, which run in parallel by default (or in sequence with <code>needs:</code>). Each job runs on a <strong>runner</strong> — a fresh virtual machine — and is made of ordered <strong>steps</strong>: either a shell command (<code>run:</code>) or a reusable action (<code>uses:</code>). Build then test is two steps; build then deploy might be two jobs with a dependency.</details>
4. What's the difference between a Docker **image** and a **container**, and why is the image the unit you ship to the cloud?
   <details><summary>Hint</summary>An <strong>image</strong> is the immutable, built artifact — your server code plus its entire runtime, frozen and layered. A <strong>container</strong> is a running instance of an image, a live process. You ship the <em>image</em> because it's identical everywhere: build it once, push it to a registry, and any machine — your laptop, a teammate's, a Kubernetes node in AWS — pulls the exact same bytes and runs the exact same server. That reproducibility is the entire point: "it runs in this container" travels, "it runs on my machine" doesn't.</details>
5. In **Kubernetes**, what are a **Pod**, a **Deployment**, and a **Service**?
   <details><summary>Hint</summary>A <strong>Pod</strong> is the smallest unit — one (or a few tightly-coupled) running containers. Pods are disposable; they come and go. A <strong>Deployment</strong> manages a set of identical Pods: it keeps the desired number alive, replaces crashed ones, and does <strong>rolling updates</strong> when you ship a new image. A <strong>Service</strong> gives those ever-changing Pods a stable network identity/address so clients (and other services) can reach them without caring which Pod is which. Deployment = how many and which version; Service = how to reach them.</details>
6. What is a **container registry**, and why push your image to one instead of building it on the cluster?
   <details><summary>Hint</summary>A registry (Docker Hub, AWS ECR, GitHub Container Registry) is a versioned store for built images — like a git remote, but for containers. You build the image <em>once</em> in CI, push it tagged (e.g. <code>:v1.2</code> or the commit SHA), and the cluster <strong>pulls</strong> exactly that. Building on the cluster would be slow, non-reproducible, and couple your runtime to your build toolchain. The registry is the handoff point between "CI built it" and "the cloud runs it" — one image, one tag, pulled identically everywhere.</details>
7. What is **Infrastructure as Code**, and why is `terraform plan` before `terraform apply` such a big deal?
   <details><summary>Hint</summary>IaC means your infrastructure — clusters, networks, load balancers — is defined in <strong>declarative files</strong> you commit to git, not clicked together by hand in a console. <code>terraform plan</code> computes the <em>diff</em> between what's described in your files and what actually exists in the cloud, and shows you exactly what it will create, change, or destroy — <strong>before it touches anything</strong>. That preview is the safety rail: you review it, catch the accidental "destroy database," and only then <code>apply</code>. Click-ops gives you no diff and no undo; IaC gives you both.</details>
8. What is **Terraform state**, and why does it matter (and why is it dangerous to lose)?
   <details><summary>Hint</summary>State (the <code>terraform.tfstate</code> file) is Terraform's record of which real cloud resources map to which blocks in your config — the link between "my <code>aws_eks_cluster.this</code>" and the actual cluster's ID. It's how <code>plan</code> knows what already exists. Lose or corrupt it and Terraform forgets it owns those resources: it may try to <strong>recreate things that already exist</strong> (duplication, errors) or <strong>orphan</strong> running infra it can no longer manage (and can no longer destroy — hello, surprise bill). That's why teams store state remotely (e.g. S3) with locking, and never hand-edit it.</details>
9. Why does a deployed server need a **health check**, and what's the difference between **liveness** and **readiness**?
   <details><summary>Hint</summary>The orchestrator can't tell a healthy server from a hung one by looking at the process — it needs the server to <em>answer</em>. A <strong>liveness</strong> probe asks "are you alive, or wedged and should I restart you?" — fail it and Kubernetes kills and replaces the Pod. A <strong>readiness</strong> probe asks "are you ready to take traffic <em>right now</em>?" — fail it and the Service stops routing players to that Pod (e.g. during startup or while it's overloaded) without killing it. Liveness = restart-if-dead; readiness = route-only-if-ready. Both are just endpoints your server exposes.</details>
10. Why is a **documented teardown / cost control** a production skill, not an afterthought — and what's the cheapest mistake to make in the cloud?
    <details><summary>Hint</summary>Cloud resources bill by the hour whether anyone's using them or not. The classic, expensive mistake is <strong>leaving something running</strong> — an EKS control plane, a load balancer, an idle node — because you didn't have a one-command way to remove it. A documented teardown (<code>terraform destroy</code> plus any manual leftovers) means you can spin infra up to learn, then take it to <em>zero</em> when you're done. Pair it with a <strong>billing alarm</strong> so spend can't silently creep. Knowing how to delete it all, on command, is exactly as important as knowing how to create it.</details>

---

## 🌟 Side Quest 1 — Manual Approval Gate in CI/CD (+50 XP)

Prove you understand that "Continuous Delivery" doesn't mean "no human ever looks." Production deploys are usually **gated**: CI builds and tests automatically, but a human clicks "approve" before anything touches the live cluster. You'll add that gate to Ashfall's pipeline.

**Requirements:**
1. Split your pipeline into two jobs: a **build-and-test** job that runs automatically on every push, and a **deploy** job that `needs:` the first one.
2. Gate the deploy job behind a **manual approval** — in GitHub Actions, attach it to an **Environment** (e.g. `production`) with a **required reviewer**. The deploy job pauses and waits for a human to approve in the GitHub UI before it runs.
3. Show that a push runs build+test immediately, but deploy sits in a **"Waiting"** state until approved — and that **rejecting** it stops the deploy cleanly with nothing shipped.
4. Note *why* this exists: automation should make shipping *safe and fast*, not *unsupervised*. The gate is where a human confirms "yes, ship this to players."

```
Test: push a commit. The build-and-test job goes green automatically. The
deploy job shows "Waiting for review." You approve → it deploys. Or you
reject → it stops, and the live cluster never changed. Same pipeline, with
a human in the loop exactly where it matters.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```yaml
# .github/workflows/deploy.yml — build runs free, deploy waits for a human.
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh        # build the Ashfall server image
      - run: ./test.sh         # run the tests

  deploy:
    needs: build-and-test       # only after build+test pass
    runs-on: ubuntu-latest
    environment: production     # <-- the gate lives here
    steps:
      - run: ./deploy.sh        # kubectl apply / terraform apply, etc.
```

- The gate is **not** in the YAML logic — it's on the **Environment**. In repo Settings → Environments → `production`, add **Required reviewers**. Any job that declares `environment: production` now pauses for their approval.
- This is the real-world shape of CI/CD: CI (build/test) is fully automatic; the *delivery* step is deliberately supervised. Many teams gate `production` but auto-deploy `staging`.
- Engine-agnostic: GitLab calls them "manual jobs / protected environments," Jenkins has "input" steps — same idea everywhere. The principle: **automate the toil, keep the judgment.**

🎯 **Side quest complete when:** your pipeline builds and tests automatically on push, the deploy job is gated behind a required-reviewer environment that visibly waits for approval, and you've demonstrated both an approved deploy and a rejected one that ships nothing. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Autoscaling Experiment (+50 XP)

Prove you understand that the cloud's superpower is **elasticity** — capacity that grows and shrinks with load instead of being fixed. You'll make Ashfall's server deployment scale itself under pressure and watch it happen on a local cluster (free).

**Requirements:**
1. On a **local Kubernetes** (Docker Desktop / kind / minikube — no cloud bill), deploy the Ashfall server with explicit CPU **resource requests/limits** (the scaler needs them to reason about utilization).
2. Add a **Horizontal Pod Autoscaler (HPA)** targeting that deployment — e.g. "keep average CPU around 50%, between 1 and 5 replicas."
3. **Generate load** (a simple load-test client, a `kubectl run` busy-loop hitting the service, or a stress endpoint on the server) and watch `kubectl get hpa -w` / `kubectl get pods` as the replica count **climbs** under load.
4. **Stop the load** and watch it **scale back down** after the cooldown. Note the before/after replica counts.

```
Test: 1 replica at idle. Pour load on the service → CPU crosses the target →
the HPA spins up replica 2, 3, 4... up to the max. Cut the load → after the
cooldown it drains back toward 1. The cluster matched capacity to demand
without you touching a thing — that's elasticity.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```yaml
# The Deployment MUST declare resource requests or the HPA has nothing to measure.
resources:
  requests: { cpu: "100m" }
  limits:   { cpu: "250m" }
```
```bash
# Create an autoscaler: 1–5 pods, target 50% average CPU.
kubectl autoscale deployment ashfall-server --cpu-percent=50 --min=1 --max=5

# Watch it react:
kubectl get hpa -w          # CURRENT vs TARGET CPU, REPLICAS climbing
kubectl get pods -w         # new pods appearing/terminating

# Generate load (one simple way): a pod that hammers the service in a loop.
kubectl run loader --rm -it --image=busybox -- /bin/sh \
  -c "while true; do wget -q -O- http://ashfall-server; done"
```

- The HPA needs the **metrics-server** running in the cluster to read CPU; on minikube it's `minikube addons enable metrics-server`, on Docker Desktop/kind you install it once.
- The key insight isn't the command — it's *why the cloud bills the way it does*. Elastic capacity means you pay for load, not for peak-you-might-hit. Autoscaling is how a server survives a launch-day spike without you babysitting it.
- **Do this on a local cluster.** Real cloud autoscaling spinning up real nodes spins up real bills — practice the mechanism for free first, and if you ever test it on AWS, tear it down immediately.
- Engine-agnostic: every orchestrator (ECS, Nomad, cloud-managed services) has the same "scale on a metric" primitive — declare a target, set bounds, let it react.

🎯 **Side quest complete when:** an HPA scales your Ashfall server deployment up under generated load and back down when it stops, on a local cluster, and you can explain why elasticity is the cloud's core value (pay for load, not for peak) — and why you'd never leave an autoscaling cloud cluster running unattended. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
