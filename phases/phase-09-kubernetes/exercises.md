# 🏋️ World 9 — Exercises

Extra reps to make `kubectl` muscle memory. None are required to advance, but each makes the Boss Battle smoother. The Side Quest awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (kubectl fluency)

Run these against your running TaskFlow cluster:

1. List every Pod with its node and IP.
   <details><summary>Hint</summary>`kubectl get pods -o wide`</details>
2. Show the logs of one TaskFlow Pod, following live.
   <details><summary>Hint</summary>`kubectl logs -f <pod-name>`</details>
3. Open an interactive shell inside a running Pod.
   <details><summary>Hint</summary>`kubectl exec -it <pod-name> -- /bin/sh`</details>
4. Describe the Deployment and find the image it's running.
   <details><summary>Hint</summary>`kubectl describe deployment taskflow`</details>
5. List the Service's current Endpoints (the live Pod IPs).
   <details><summary>Hint</summary>`kubectl get endpoints taskflow`</details>
6. Show recent cluster events, newest last.
   <details><summary>Hint</summary>`kubectl get events --sort-by=.lastTimestamp`</details>

## Manifest warm-ups

7. Render the YAML of your live Deployment without opening the file.
   <details><summary>Hint</summary>`kubectl get deployment taskflow -o yaml`</details>
8. Apply *all* manifests in your k8s folder in one command.
   <details><summary>Hint</summary>`kubectl apply -f ~/projects/taskflow/k8s/`</details>
9. Trigger a restart of all Pods without changing replica count.
   <details><summary>Hint</summary>`kubectl rollout restart deployment/taskflow`</details>
10. Check the rollout status and history.
    <details><summary>Hint</summary>`kubectl rollout status deployment/taskflow` then `kubectl rollout history deployment/taskflow`</details>

---

## 🌟 Side Quest — Readiness Probe + Rolling Update Strategy (+50 XP)

Priya wants **zero-downtime deploys**: when you ship a new image, old Pods should only be retired once new ones are *ready* to serve. That needs two things working together — a **readiness probe** and a **rolling update strategy**.

Add a `strategy` block and a `readinessProbe` to your Deployment:

```yaml
# inside spec: of deployment.yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0     # never drop below desired count during a rollout
      maxSurge: 1           # bring up 1 extra Pod at a time
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
          readinessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

Then trigger and watch a rollout:

```bash
kubectl apply -f ~/projects/taskflow/k8s/deployment.yaml
kubectl set image deployment/taskflow taskflow=ghcr.io/YOUR_USER/taskflow:v2
kubectl rollout status deployment/taskflow      # progresses only as new Pods pass readiness
```

> 💡 With `maxUnavailable: 0`, Kubernetes won't terminate an old Pod until a new one is **ready**, so the Service always has healthy backends. That's a zero-downtime deploy.

🎯 **Side quest complete when:** your Deployment has a `RollingUpdate` strategy + a `readinessProbe`, and `kubectl rollout status` shows a rollout completing while `kubectl get endpoints taskflow` always lists at least one ready Pod. Add **+50 XP**.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
