# 👹 Boss Battle — Trace the Request

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 40 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 2 — Linux |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Marcus <marcus@cloudforge.inc>
To:      You
Subject: [PROVE-IT] Before World 2 — trace a request end to end

You've sent requests and read responses all week. Now prove you
understand the WHOLE journey — not just the curl commands, but every
hop in between.

Here's the scenario I give every new engineer: someone types a URL,
hits Enter, and a page appears. I want you to narrate every step that
happened — DNS, IP, the port, the TCP connection, the HTTP request,
the status code, the response — AND back it up with live curl output.

No tutorials this time. You know enough. Show me you can think like
someone who'll soon be on call for TaskFlow at 2 AM.

— Marcus
```

> ⚔️ **Boss Battle rules:** No step-by-step guides. Use your notes, the official docs, and everything you built. You win when every victory condition is met **and you can explain *why* each hop happens.**

---

## 🎯 Your mission

Two parts. Do both.

### Part A — Narrate the journey (the explanation)
Write a file `~/projects/request-journey.md` that explains, in your own words, **every hop** that happens when someone types `https://httpbin.org/get` and presses Enter. It must cover, in order:

1. **DNS** — the name `httpbin.org` becomes an IP address
2. **IP + Port** — which machine, and which door (which port, and why)
3. **TCP connection** — the client opens a connection to that IP:port (a quick "handshake" before any HTTP is sent)
4. **HTTP request** — the method + path the client actually sends
5. **Status code** — what the server's verdict means
6. **Response** — headers + body, and what the client does with them

A simple Mermaid `sequenceDiagram` in your file earns bonus respect (optional).

### Part B — Prove it with curl (the demonstration)
Produce a single command sequence (or short script) that **demonstrates** the journey with real output, capturing it to `~/projects/request-proof.txt`. It must show, with real data:

1. The **IP** that `httpbin.org` resolves to (DNS)
2. curl **connecting to that IP on port 443** (the verbose connection line)
3. A successful **GET** request and its `200` status + headers
4. A deliberately triggered **404** and a **500**, printed as bare status codes
5. A **POST** with a JSON body, echoed back by the server

---

## 🏆 Victory conditions

- [ ] `~/projects/request-journey.md` explains all **six** hops in order (DNS → IP/port → TCP → HTTP request → status → response)
- [ ] `~/projects/request-proof.txt` contains: a resolved IP, a verbose connection line showing `:443`, a `200`, a `404`, a `500`, and a successful POST echo
- [ ] I can say **out loud** *why* each hop happens (not just what to type)
- [ ] I can correctly answer: "a user got a 404 — is the server down?" (and why)

---

## 🧪 How you'll know you won

Open `request-proof.txt`. If it contains a real IP for httpbin.org, a `Trying ...:443` line, an `HTTP/2 200`, a lonely `404` and `500`, and your POSTed JSON echoed under `"json"` — Part B is done. For Part A, your six-hop explanation should match the spirit of the reference below. Then narrate the whole thing to an imaginary teammate without notes.

<details>
<summary>🔎 Reference solution — only after you've tried! (Part B proof script)</summary>

```bash
cd ~/projects
{
  echo "===== 1. DNS: name -> IP ====="
  dig +short httpbin.org

  echo "===== 2. Connect on port 443 (verbose) ====="
  # Show just the connection lines so we can see the IP:443 it dials
  curl -v https://httpbin.org/get 2>&1 | grep -E "Trying|Connected" | head -n 3

  echo "===== 3. Successful GET: status + headers ====="
  curl -s -i https://httpbin.org/get | head -n 12

  echo "===== 4. A 404 and a 500 (bare status codes) ====="
  echo -n "404 endpoint -> "; curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/404
  echo -n "500 endpoint -> "; curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/500

  echo "===== 5. POST a JSON body, server echoes it ====="
  curl -s -X POST https://httpbin.org/post \
    -H "Content-Type: application/json" \
    -d '{"title":"trace the request","done":true}' | grep -A2 '"json"'
} | tee request-proof.txt
```
`tee` prints to the screen *and* writes `request-proof.txt`. `grep` trims the noise so the proof is readable.
</details>

<details>
<summary>🔎 Reference solution — Part A six-hop narration</summary>

When you type `https://httpbin.org/get` and press Enter:

1. **DNS (name → IP).** The browser doesn't know what `httpbin.org` *means* — computers route by number. It asks a DNS resolver, which walks the chain (root → `.org` → httpbin's authoritative server) and returns an IP (e.g. `3.x.x.x`). The result is cached so next time is instant. *Why:* humans use names, networks use numbers; DNS bridges them.

2. **IP + Port.** Now we know *which machine* (the IP) and *which door* (the port). The scheme `https` implies **port 443**. *Why:* one machine runs many programs; the port routes us to the web server specifically.

3. **TCP connection (handshake).** Before any HTTP is sent, the client opens a reliable connection to `IP:443` — a brief back-and-forth ("SYN → SYN-ACK → ACK") that sets up a channel both sides agree on. (With HTTPS, a TLS handshake then encrypts it.) *Why:* HTTP needs a dependable, ordered pipe to talk over.

4. **HTTP request.** Over that connection the client sends the actual request: a **method + path** (`GET /get`) plus headers (Host, User-Agent, Accept…). *Why:* this is the polite, structured way to say exactly what we want.

5. **Status code.** The server processes the request and replies with a three-digit verdict. `200` = OK. `4xx` = the client/request was wrong (e.g. `404` not found). `5xx` = the server itself errored (e.g. `500`). *Why:* a universal signal every client and monitor understands instantly.

6. **Response (headers + body).** Along with the status come **headers** (metadata: `Content-Type`, `Content-Length`, …) and the **body** (the actual JSON/HTML). The browser reads the headers to learn how to interpret the body, then renders the page. *Why:* status tells you *if* it worked, headers tell you *how to read it*, the body *is* the content.

**"A user got a 404 — is the server down?"** No. A 404 is a **client-side** outcome: the server is healthy and is *correctly telling you* the requested thing doesn't exist (wrong path/URL). A truly broken server returns **5xx**, not 4xx.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🔓 **World 2 — Linux** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 1 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: a week ago, "the internet happened" was your whole answer. Now you can name all six hops and prove each with curl. That mental model is the foundation everything in World 4 (the backend) builds on — you'll be *creating* the responses you just learned to read.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🐧 Enter World 2 →](../phase-02-linux/README.md)
