# 🏋️ World 1 — Exercises

Extra reps to make HTTP feel automatic. None are required to advance, but each makes the Boss Battle (and all of World 4) easier. Side Quests award **+50 XP** each. Do these in your **Ubuntu** terminal.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (curl drills)

1. Fetch `httpbin.org/get` and find your public IP in the response.
   <details><summary>Hint</summary>`curl https://httpbin.org/get` — look at the `"origin"` field.</details>
2. Resolve `wikipedia.org` to an IP, two different ways.
   <details><summary>Hint</summary>`dig +short wikipedia.org` and `nslookup wikipedia.org`</details>
3. Make a POST request that sends `{"hello":"world"}` as JSON.
   <details><summary>Hint</summary>`curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"hello":"world"}'`</details>
4. Get **only** the status code of `httpbin.org/get` (no body).
   <details><summary>Hint</summary>`curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/get`</details>
5. Show the full request *and* response headers for `httpbin.org/get`.
   <details><summary>Hint</summary>`curl -v https://httpbin.org/get` (look for `>` sent and `<` received).</details>
6. Follow a redirect all the way to its destination.
   <details><summary>Hint</summary>`curl -L -i "https://httpbin.org/redirect-to?url=https://httpbin.org/get"`</details>
7. Send a custom header and confirm the server received it.
   <details><summary>Hint</summary>`curl -H "X-Bootcamp: world1" https://httpbin.org/headers`</details>
8. Make a request that returns a delayed response (3 seconds).
   <details><summary>Hint</summary>`curl https://httpbin.org/delay/3` — useful later for testing timeouts.</details>

---

## 🌟 Side Quest — Trigger & Explain a 301, 404, and 500 (+50 XP)

Use `httpbin.org/status/CODE` to make the server return each of these on demand, then explain — in one sentence each — what the code means and whose "fault" it is.

```bash
# 301 — Moved Permanently (a redirect)
curl -i https://httpbin.org/status/301

# 404 — Not Found (client asked for something that isn't there)
curl -i https://httpbin.org/status/404

# 500 — Internal Server Error (the server broke)
curl -i https://httpbin.org/status/500
```

Write your three explanations into a file so you can prove your understanding:

```bash
cd ~/projects
cat > status-codes-explained.md << 'EOF'
# Status codes I triggered

- 301 Moved Permanently: a REDIRECT — the resource now lives at a new URL
  (look for the Location header). Not an error.
- 404 Not Found: a CLIENT-side problem — the path/resource doesn't exist.
  The server is fine; the request asked for the wrong thing.
- 500 Internal Server Error: a SERVER-side problem — the server crashed or
  errored while handling a valid request. Not the client's fault.
EOF
cat status-codes-explained.md
```

🎯 **Side quest complete when:** you've triggered all three codes with curl **and** `status-codes-explained.md` correctly explains each. Add **+50 XP**.

---

## 🌟 Side Quest — Build a "Where Does It Live?" Report (+50 XP)

Combine DNS, IP, and ports into one investigation of a real site. Pick any site you use and answer, with real commands:

```bash
SITE=github.com   # change to any site you like

echo "== Name -> IP (DNS) =="
dig +short "$SITE"

echo "== Reachability (round-trip time) =="
ping -c 3 "$SITE" || echo "(this host may block ping — that's OK)"

echo "== What port does HTTPS use, and does it answer? =="
curl -s -o /dev/null -w "HTTPS status from $SITE: %{http_code}\n" "https://$SITE"
```

🎯 **Complete when:** you can state, for your chosen site: its IP (from DNS), whether it answers ping, and the HTTPS status code it returned — and explain that HTTPS used **port 443**. Add **+50 XP**.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
