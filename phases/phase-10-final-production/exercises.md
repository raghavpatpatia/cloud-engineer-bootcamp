# 🏋️ World 10 — Exercises

Extra reps to harden your production skills before Launch Day. None are required to advance, but each makes you a more credible operator. The Side Quest awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (DNS, TLS, health)

1. Resolve your domain using a **public** resolver to bypass local cache.
   <details><summary>Hint</summary>`dig @8.8.8.8 +short taskflow.yourname.dev`</details>
2. Inspect the live certificate's expiry and issuer from the command line.
   <details><summary>Hint</summary>`echo | openssl s_client -connect taskflow.yourname.dev:443 -servername taskflow.yourname.dev 2>/dev/null | openssl x509 -noout -dates -issuer`</details>
3. Confirm plain HTTP redirects to HTTPS (look for a 301/308).
   <details><summary>Hint</summary>`curl -I http://taskflow.yourname.dev`</details>
4. Hit both health endpoints and check the status codes.
   <details><summary>Hint</summary>`curl -s -o /dev/null -w "%{http_code}\n" https://taskflow.yourname.dev/health/ready`</details>
5. Watch the cert-manager Certificate go ready.
   <details><summary>Hint</summary>`kubectl get certificate -w`</details>

## Probes & self-healing

6. Force a rolling restart and watch zero-downtime behaviour (readiness gates traffic).
   <details><summary>Hint</summary>`kubectl rollout restart deployment/taskflow` then `kubectl get pods -l app=taskflow -w`</details>
7. Read a pod's probe results from its events.
   <details><summary>Hint</summary>`kubectl describe pod <pod>` → "Events" section</details>
8. Roll back to the previous deployment revision and confirm `/health` still returns 200.
   <details><summary>Hint</summary>`kubectl rollout undo deployment/taskflow`</details>

## Monitoring & logs

9. Trigger a real DOWN alert and a recovery alert (scale to 0, then back up).
10. Filter your structured logs for error-level lines only.
    <details><summary>Hint</summary>`kubectl logs -l app=taskflow | grep '"level":50'`</details>

---

## 🌟 Side Quest — Structured Logging + a Simple Metrics Dashboard (+50 XP)

You added uptime monitoring in Lesson 4. Now make TaskFlow *observable* from the inside: emit clean structured logs **and** expose basic metrics on a small dashboard — all free and self-hosted.

### Part 1 — Pretty, structured logs

Confirm pino is emitting JSON, and view it human-readably in dev:

```bash
npm install --save-dev pino-pretty
# Pipe logs through pino-pretty locally (prod stays raw JSON for machines)
kubectl logs -l app=taskflow -f | npx pino-pretty
```

Add a request ID and basic fields to each log so you can trace a single request end-to-end (pino-http adds `req.id` automatically).

### Part 2 — Expose metrics

Add a `/metrics` endpoint with `prom-client` (Prometheus format — the industry standard, free):

```bash
npm install prom-client
```

```javascript
// src/metrics.js
const client = require('prom-client');
client.collectDefaultMetrics();                 // process CPU, memory, etc.

const httpRequests = new client.Counter({
  name: 'taskflow_http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
});

// src/app.js
app.use((req, res, next) => {
  res.on('finish', () =>
    httpRequests.inc({ method: req.method, route: req.path, status: res.statusCode }));
  next();
});
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

```bash
curl -s localhost:3000/metrics | grep taskflow_http_requests_total
```

### Part 3 — A simple dashboard

Two free options — pick one:

- **Quick & free:** UptimeRobot's free **public status page** — turns your monitor into a shareable uptime dashboard in two clicks.
- **Full metrics:** run **Prometheus + Grafana** in your cluster (both free, open source), scrape `/metrics`, and build a panel for request rate and error rate.

🎯 **Side quest complete when:** TaskFlow exposes `/metrics` in Prometheus format, your logs are structured JSON you can filter by level, **and** you have a dashboard (a public status page *or* a Grafana panel) showing TaskFlow's health. Add **+50 XP**.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
