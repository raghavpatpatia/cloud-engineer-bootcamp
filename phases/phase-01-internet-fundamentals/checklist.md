# ✅ World 1 — Readiness Checklist

Before you face the Boss Battle and unlock World 2, make sure all of this is true. The Boss asks you to trace a request from keystroke to rendered page — if any box below is empty, revisit that lesson first.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧠 Concepts I can explain out loud
- [ ] What a **client** and a **server** are, and the **request/response** model (one request → one response)
- [ ] What **DNS** does (name → IP) and roughly the steps of a lookup
- [ ] What an **IP address** and a **port** are (incl. 80 = HTTP, 443 = HTTPS)
- [ ] The four core **HTTP methods**: GET, POST, PUT, DELETE
- [ ] What **status code families** mean (2xx/3xx/4xx/5xx) and the big ones (200/301/404/500)
- [ ] The difference between a response's **status**, **headers**, and **body**

## 🛠️ Skills I can do without looking up
- [ ] Resolve a domain to an IP with `dig +short` (or `nslookup`)
- [ ] Make a GET request with `curl`
- [ ] Make a POST/PUT request sending a JSON body (with the right `Content-Type` header)
- [ ] Make a DELETE request
- [ ] See status + headers with `curl -i`, and the full exchange with `curl -v`
- [ ] Print just the status code with `curl -s -o /dev/null -w "%{http_code}\n"`
- [ ] Follow a redirect with `curl -L`

## 🔎 Self-test (do this from memory)
Open Ubuntu and, without notes:
1. Resolve `httpbin.org` to an IP.
2. Make a POST to `httpbin.org/post` sending `{"task":"learn http","done":true}` as JSON, and find your data echoed back.
3. Trigger a `404` and print **only** the status code.
4. In one sentence each, say what DNS did in step 1 and whose fault a 404 is in step 3.

<details>
<summary>✅ One correct solution</summary>

```bash
# 1. Name -> IP
dig +short httpbin.org

# 2. POST JSON and read it back (look under "json")
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"task":"learn http","done":true}'

# 3. Just the status code for a 404
curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/404
```
- Step 1: DNS translated the name `httpbin.org` into a numeric IP so the connection could be made.
- Step 3: a 404 is a **client-side** issue — the requested thing doesn't exist; the server is fine.
</details>

If you did that without peeking — you're ready.

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I did at least one Side Quest from [exercises.md](exercises.md)

---

> All checked? → [👹 Face the Boss Battle: Trace the Request](boss-battle.md)

[← World Home](README.md)
