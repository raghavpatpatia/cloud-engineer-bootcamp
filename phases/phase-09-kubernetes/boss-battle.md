# 👹 Boss Battle — The Traffic Surge

| | |
|---|---|
| 🎚️ **Difficulty** | 🔴 Hard |
| ⏱️ **Estimated time** | 45 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 10 — Final Production Deployment |
| 🏅 **Achievement** | 🌊 Surge Survivor |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Priya <priya@cloudforge.inc>
To:      You
Subject: [SEV-1] TaskFlow is falling over under load — fix it on K8s NOW

We're trending again and TaskFlow keeps tipping over. The single
container can't take it, and every time it dies we're down until a
human restarts it. This is exactly what we moved to Kubernetes for.

Stand TaskFlow up on the cluster properly and prove it survives:

  - multiple replicas, managed by a Deployment
  - one stable, load-balanced Service in front
  - it SELF-HEALS  (kill a Pod -> it comes back, no human)
  - it SCALES under load  (HPA adds Pods as CPU climbs)

No hand-holding this time — you've built every piece. Show me the
surge can't take us down.

— Priya
```

> ⚔️ **Boss Battle rules:** No tutorials. Use your notes, your manifests in `~/projects/taskflow/k8s/`, and the docs. You win when every victory condition is met **and you can explain why each one works**.

---

## 🎯 Your mission

Bring TaskFlow up on your local cluster as a **resilient, self-scaling service**, then prove it survives both a **Pod failure** and a **load spike**.

You need, all working together:
1. A **Deployment** with **≥3 replicas** (labels, CPU `requests`/`limits`).
2. A **Service** that load-balances across the Pods (stable address).
3. **Self-healing**: kill a Pod and a replacement reaches `Running` on its own.
4. A **HorizontalPodAutoscaler** that **adds Pods under load** and removes them after.

Then run the **surge test**: generate load, watch the HPA scale out, kill a Pod mid-surge, and confirm TaskFlow stays reachable the whole time.

---

## 🏆 Victory conditions

- [ ] **Replicas running:** `kubectl get deployment taskflow` shows `READY 3/3` (or more)
- [ ] **Service reachable:** you reach TaskFlow *through the Service* (NodePort / port-forward / `minikube service`) and get a valid response
- [ ] **Self-heals:** after `kubectl delete pod <one>`, a new Pod appears and reaches `Running` with no manual action — Pod count returns to desired
- [ ] **HPA scales on load:** `kubectl get hpa taskflow` shows a real `TARGETS` %, and under load `REPLICAS` rises (then falls when load stops)
- [ ] You can **explain** why each piece works (desired-state reconciliation, label selectors, utilization = usage ÷ request)

---

## 🧪 How you'll know you won

Run the surge test end to end:

```bash
# Bring everything up
kubectl apply -f ~/projects/taskflow/k8s/

# Confirm baseline
kubectl get deployment taskflow      # READY 3/3
kubectl get service taskflow
kubectl get hpa taskflow             # TARGETS shows a real %, not <unknown>

# Generate load (in a second terminal)
kubectl run load --rm -it --image=busybox --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://taskflow; done"

# Watch it scale OUT (first terminal)
kubectl get hpa taskflow -w          # REPLICAS climbs

# Mid-surge, kill a Pod and confirm it heals while staying reachable
kubectl delete pod $(kubectl get pods -l app=taskflow -o jsonpath='{.items[0].metadata.name}')
kubectl get pods -l app=taskflow     # replacement appears; count holds

# Stop the load -> watch it scale back IN over a few minutes
```

If the Pod count rose under load, a deleted Pod was replaced automatically, and the Service answered throughout — **you survived the surge.** 🌊

---

<details>
<summary>🔎 Reference manifests — only after you've tried!</summary>

`~/projects/taskflow/k8s/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskflow
  labels:
    app: taskflow
spec:
  replicas: 3
  selector:
    matchLabels:
      app: taskflow
  template:
    metadata:
      labels:
        app: taskflow
    spec:
      containers:
        - name: taskflow
          image: ghcr.io/YOUR_USER/taskflow:latest
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: taskflow-config
            - secretRef:
                name: taskflow-db
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
```

`~/projects/taskflow/k8s/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: taskflow
  labels:
    app: taskflow
spec:
  type: NodePort
  selector:
    app: taskflow
  ports:
    - name: http
      port: 80
      targetPort: 3000
      nodePort: 30080
```

`~/projects/taskflow/k8s/hpa.yaml`
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: taskflow
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: taskflow
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

> Remember: the HPA needs the `metrics-server` running and a CPU `request` on the container. `secret.yaml`/`configmap.yaml` come from Level 4 — keep `secret.yaml` out of Git.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **🌊 Surge Survivor**
- 🔓 **World 10 — Final Production Deployment** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 9 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: yesterday, a 3am Pod crash meant a pager and a human. Now it means... nothing — the cluster already handled it. That's the whole point of Kubernetes.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🚀 Enter World 10 →](../phase-10-final-production/README.md)
