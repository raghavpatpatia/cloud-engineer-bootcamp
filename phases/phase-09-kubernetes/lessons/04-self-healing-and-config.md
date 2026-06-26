# Level 4 — Self-Healing, Config & Secrets

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 25 minutes |
| ⭐ **XP reward** | 100 (Quest) + 25 (Quiz) |

[← Prev: Services & Networking](03-services-and-networking.md) · [↑ Phase Home](../README.md) · [→ Next: Autoscaling Under Load](05-autoscaling.md)

---

## 📖 Story

> *"Two things keep me up at night. One: when a Pod dies at 3am, does it come back **without me**? Two: TaskFlow needs its database URL and password — and I am **not** baking secrets into the image. Show me self-healing in action, and move the config and DB creds out of the container and into Kubernetes where they belong. — Priya"*

This is where Kubernetes earns its keep: it heals itself, and it manages your configuration and secrets cleanly.

---

## 🎯 Goal

- See **self-healing** firsthand: kill a Pod and watch K8s replace it
- Move app config into a **ConfigMap** and DB credentials into a **Secret**
- Inject both into TaskFlow as environment variables
- Add **liveness** and **readiness probes** so K8s knows when a Pod is *actually* healthy

---

## 🧠 Concepts

**Self-healing** is the reconciliation loop you've been hearing about. The Deployment's controller constantly compares *desired* replicas to *actual* running Pods; any gap, it fixes — no human needed.

```mermaid
flowchart LR
    Desired["🎯 Desired: 3 Pods"] --> Compare{"actual == desired?"}
    Actual["👀 Actual: observed Pods"] --> Compare
    Compare -->|"yes"| Wait["✅ do nothing"]
    Compare -->|"no (a Pod died)"| Heal["🛠️ create/delete Pods"]
    Heal --> Actual
    Wait --> Compare
    style Desired fill:#dbeafe,stroke:#2563eb
    style Heal fill:#fee2e2,stroke:#b91c1c
    style Wait fill:#dcfce7,stroke:#166534
```

**ConfigMap** = non-secret config (URLs, feature flags, ports). **Secret** = sensitive values (passwords, tokens), base64-encoded and handled more carefully. Both let you change config **without rebuilding the image** — the same image runs in dev, staging, and prod with different config injected.

**Probes** tell K8s what "healthy" means:
- **Liveness probe**: "is this Pod alive?" If it fails, K8s **restarts** the container (heals a hung app).
- **Readiness probe**: "is this Pod ready for traffic?" If it fails, the Service **stops sending requests** to it until it recovers (no traffic to a Pod still warming up).

### Why this exists

Hardcoding config and secrets into an image is how credentials leak and how "works in dev, breaks in prod" happens. ConfigMaps/Secrets externalize that. And probes turn "the process is running" (a weak signal) into "the app can actually serve requests" (the real signal) — so self-healing fixes the *right* Pods at the *right* time.

---

## 🛠️ Hands-on Lab

### Step 1 — Watch self-healing live

```bash
# Watch Pods in real time (leave this running in one terminal)
kubectl get pods -l app=taskflow -w
```

In a **second** terminal, kill one Pod:

```bash
kubectl delete pod $(kubectl get pods -l app=taskflow -o jsonpath='{.items[0].metadata.name}')
```

Back in the first terminal you'll see the Pod go `Terminating`, and a **brand-new Pod** appear and reach `Running` within seconds. You did nothing — the Deployment healed itself. (Ctrl+C to stop watching.)

### Step 2 — Create a ConfigMap

Create `~/projects/taskflow/k8s/configmap.yaml`:

```yaml
# ~/projects/taskflow/k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: taskflow-config
data:
  NODE_ENV: "production"
  PORT: "3000"
  LOG_LEVEL: "info"
```

```bash
kubectl apply -f ~/projects/taskflow/k8s/configmap.yaml
```

### Step 3 — Create a Secret (DB credentials)

The clean, repeatable way (Kubernetes does the base64 encoding for you):

```bash
kubectl create secret generic taskflow-db \
  --from-literal=DATABASE_URL='postgres://taskflow:s3cr3t@taskflow-db:5432/taskflow' \
  --from-literal=DB_PASSWORD='s3cr3t' \
  --dry-run=client -o yaml > ~/projects/taskflow/k8s/secret.yaml

kubectl apply -f ~/projects/taskflow/k8s/secret.yaml
```

> 🔐 Secrets are only **base64-encoded**, not encrypted at rest by default — never commit `secret.yaml` to Git. Keep it out of version control (e.g. add it to `.gitignore`). In World 10 we'll talk about real secret stores.

### Step 4 — Inject config + secret + probes into the Deployment

Update the `containers` section of `deployment.yaml`:

```yaml
      containers:
        - name: taskflow
          image: ghcr.io/YOUR_USER/taskflow:latest
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: taskflow-config     # injects NODE_ENV, PORT, LOG_LEVEL
            - secretRef:
                name: taskflow-db         # injects DATABASE_URL, DB_PASSWORD
          readinessProbe:                 # ready for traffic?
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:                  # still alive?
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
```

```bash
kubectl apply -f ~/projects/taskflow/k8s/deployment.yaml
```

> 🩺 No `/healthz` route in TaskFlow yet? Either add a tiny Express route that returns `200 OK`, or temporarily point the probes at `/`. A real health endpoint is the right long-term move (and a Side Quest in [exercises.md](../exercises.md)).

### Step 5 — Verify the config landed inside the Pod

```bash
POD=$(kubectl get pods -l app=taskflow -o jsonpath='{.items[0].metadata.name}')

# Confirm env vars from the ConfigMap are present
kubectl exec "$POD" -- printenv NODE_ENV PORT LOG_LEVEL

# Confirm the Pod reports readiness
kubectl get pods -l app=taskflow      # READY column should be 1/1 for each
```

---

## 🎮 Mini Challenge

Make a Pod's **readiness** probe fail on purpose (e.g. point it at a path that returns 404) and re-apply. What happens to that Pod's `READY` status — and does the Service still send it traffic?

<details>
<summary>💡 Reveal answer</summary>

The Pod shows `READY 0/1` (still `Running`, but not ready). The Service **removes it from its Endpoints**, so no traffic goes to it until the probe passes again. The Pod isn't restarted (that's the liveness probe's job) — readiness only gates *traffic*. Revert the path and it rejoins the Service. Check with `kubectl get endpoints taskflow`.
</details>

---

## 📦 Project Mission

Externalize TaskFlow's config + secrets, add health probes, and prove self-healing.

```bash
# 1. Apply config + secret
kubectl apply -f ~/projects/taskflow/k8s/configmap.yaml
kubectl apply -f ~/projects/taskflow/k8s/secret.yaml

# 2. Apply the updated Deployment (envFrom + probes)
kubectl apply -f ~/projects/taskflow/k8s/deployment.yaml

# 3. Confirm config landed
POD=$(kubectl get pods -l app=taskflow -o jsonpath='{.items[0].metadata.name}')
kubectl exec "$POD" -- printenv NODE_ENV DATABASE_URL

# 4. Prove self-healing: delete a Pod, watch it come back
kubectl delete pod "$POD"
kubectl get pods -l app=taskflow -w   # a replacement reaches Running
```

🎯 **Mission complete when:** TaskFlow reads `NODE_ENV`/`DATABASE_URL` from a ConfigMap + Secret (verified with `printenv`), the Deployment has readiness + liveness probes, and deleting a Pod produces an automatic replacement that reaches `Running`.

---

## ⚠️ Common Mistakes

| Mistake | What happens | Fix |
|--------|--------------|-----|
| Putting passwords in a ConfigMap | Secrets exposed in plain config | Use a **Secret** for anything sensitive |
| Committing `secret.yaml` to Git | Credentials leak | Add it to `.gitignore`; never commit Secrets |
| Liveness probe too aggressive | Pods restart in a crash loop | Raise `initialDelaySeconds`; give the app time to boot |
| Probe path returns non-200 | Pod never becomes `READY` / restarts | Point probes at a real endpoint that returns 200 |
| Editing a ConfigMap and expecting instant pickup | Env vars don't refresh in running Pods | Roll the Deployment: `kubectl rollout restart deployment/taskflow` |

---

## 🤔 Reflection Questions

1. Why externalize config + secrets instead of baking them into the image?
2. What's the difference between a liveness probe and a readiness probe?
3. When you deleted a Pod, *what* recreated it, and *how* did it know to?

---

## 📝 Quiz

1. **Sensitive values like DB passwords belong in a…**
   - a) ConfigMap
   - b) Secret
   - c) the Docker image
2. **A failing *liveness* probe causes Kubernetes to…**
   - a) restart the container
   - b) delete the Service
   - c) scale the Deployment
3. **A failing *readiness* probe causes…**
   - a) the Pod to be deleted forever
   - b) the Service to stop sending it traffic until it's ready
   - c) the cluster to shut down

<details>
<summary>✅ Answers</summary>

1: **b** · 2: **a** · 3: **b**
</details>

---

## ✅ Completion Checklist

- [ ] I watched a deleted Pod get replaced automatically
- [ ] `configmap.yaml` and `secret.yaml` exist; values inject via `envFrom`
- [ ] `printenv` inside a Pod shows `NODE_ENV` and `DATABASE_URL`
- [ ] Deployment has readiness + liveness probes
- [ ] `secret.yaml` is git-ignored
- [ ] I passed the quiz
- [ ] I added **+125 XP** to [PROGRESS.md](../../../PROGRESS.md)

---

[← Prev: Services & Networking](03-services-and-networking.md) · [↑ Phase Home](../README.md) · [→ Next: Autoscaling Under Load](05-autoscaling.md)
