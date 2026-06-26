# ✅ World 9 — Readiness Checklist

Before you face the Boss Battle and unlock World 10, make sure all of this is true. If any box is empty, revisit that lesson — the Traffic Surge tests all of it at once.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Cluster & tools
- [ ] `kubectl version --client` prints a version
- [ ] My local cluster runs (`kubectl get nodes` → a `Ready` node) via minikube or kind
- [ ] `metrics-server` works (`kubectl top pods` returns numbers, not an error)

## 🗂️ Manifests in `~/projects/taskflow/k8s/`
- [ ] `deployment.yaml` (replicas, labels, probes, resource requests/limits)
- [ ] `service.yaml` (selector matches Pod labels)
- [ ] `configmap.yaml` and a **git-ignored** `secret.yaml`
- [ ] `hpa.yaml` (min/max replicas, CPU target)

## 🧠 Skills I can do without looking up
- [ ] Apply a manifest (`kubectl apply -f`) and read its status
- [ ] Scale a Deployment (`kubectl scale`) and explain Deployment → ReplicaSet → Pods
- [ ] Reach the app through a Service (NodePort / port-forward / `minikube service`)
- [ ] Inject config + secrets with `envFrom` and verify with `printenv`
- [ ] Explain the difference between a liveness and a readiness probe
- [ ] Explain why an HPA needs a CPU `request` + a metrics source

## 🔎 Self-test (do this from memory)
Against your cluster, without notes:
1. Apply the Deployment and Service, confirm `READY 3/3`
2. Delete one Pod and watch a replacement reach `Running`
3. Reach TaskFlow *through the Service*
4. Confirm the HPA shows a real `TARGETS` percentage

<details>
<summary>✅ One correct sequence</summary>

```bash
kubectl apply -f ~/projects/taskflow/k8s/
kubectl get deployment taskflow                 # READY 3/3
kubectl delete pod $(kubectl get pods -l app=taskflow -o jsonpath='{.items[0].metadata.name}')
kubectl get pods -l app=taskflow -w             # replacement appears (Ctrl+C)
kubectl port-forward service/taskflow 8080:80 & # reach via the Service
curl -s http://localhost:8080 ; kill %1
kubectl get hpa taskflow                        # TARGETS shows e.g. 5%/50%
```
</details>

If you did that without peeking — you're ready for the surge.

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I did the Side Quest (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Traffic Surge](boss-battle.md)

[← World Home](README.md)
