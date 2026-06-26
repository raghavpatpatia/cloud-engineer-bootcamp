# ✅ World 10 — Readiness Checklist

This is the final gate before **Launch Day**. If any box is empty, revisit that lesson — you do not want to discover a gap during the boss battle (or in front of real users).

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 What I built this world
- [ ] TaskFlow is reachable at a **human-readable domain** (DNS resolves to my app)
- [ ] TaskFlow serves over **HTTPS** with a valid, auto-renewing Let's Encrypt cert
- [ ] Plain HTTP **redirects** to HTTPS
- [ ] The app exposes `/health/live`, `/health/ready` (DB-aware), and `/health`
- [ ] Liveness, readiness, and startup **probes** are wired into the Deployment
- [ ] An **uptime monitor** checks `/health` and **alerts** me on down + recovery
- [ ] The app emits **structured (JSON) logs**
- [ ] A **README** (with architecture diagram) and a **RUNBOOK** are committed

## 🧠 Skills I can do without looking up
- [ ] Create a DNS A/CNAME record and verify it with `dig`
- [ ] Explain how Let's Encrypt proves domain ownership (ACME / HTTP-01)
- [ ] State the difference between liveness and readiness — and why each fails the way it does
- [ ] Name the three pillars (metrics, logs, alerts) and what each answers
- [ ] Roll back a bad deploy with `kubectl rollout undo`

## 🔎 Self-test (do this from memory)
Without notes, write down the **request path** for a user loading TaskFlow:

1. What translates the domain name into an IP?
2. What terminates TLS and presents the certificate?
3. What decides which Pod gets the request?
4. What stops traffic going to a Pod whose database is down?
5. What tells *you* the whole thing is down?

<details>
<summary>✅ One correct answer</summary>

1. **DNS** resolves `taskflow.yourname.dev` → the ingress/load-balancer IP.
2. The **Ingress controller** (with the cert-manager-issued cert) terminates **TLS**.
3. The **Service** load-balances to a healthy **Pod**.
4. The **readiness probe** fails → Kubernetes removes that Pod from the Service.
5. The **uptime monitor** (UptimeRobot) fails its `/health` check and **alerts** you.

If you wrote all five without peeking — you understand your production system end to end.
</details>

---

## 🚦 Production readiness checklist
The real-world "are we allowed to launch?" list. Every box should be checked before the boss battle:

- [ ] **HTTPS** — valid cert, no browser warning, HTTP → HTTPS redirect, auto-renewal confirmed
- [ ] **Health** — readiness reflects real dependencies; liveness is cheap; no crash loops
- [ ] **Monitoring** — uptime check on a real health endpoint; alert *tested* (you got a real page)
- [ ] **Docs** — README + runbook exist, are accurate, and render on GitHub
- [ ] **Backups** — the database has a backup/restore plan (e.g. RDS automated snapshots, or a documented `pg_dump` cron); you know how to restore
- [ ] **Cost** — no leftover **paid** AWS resources running; billing alarm still active

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I did the Side Quest (+50 XP)

---

> All checked? → [👹 Face the FINAL Boss Battle: Launch Day](boss-battle.md)

[← World Home](README.md)
