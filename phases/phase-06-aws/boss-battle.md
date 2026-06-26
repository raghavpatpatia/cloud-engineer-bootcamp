# 👹 Boss Battle — The Empty Cloud

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 45 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 7 — CI/CD |
| 🏅 **Achievement** | ☁️ **Cloud Walker** |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Dana (Manager) <dana@cloudforge.inc>
To:      You
Subject: [LAUNCH] Demo in 1 hour — get TaskFlow on a clean cloud account

The CEO wants to show TaskFlow to an investor in an hour, from a CLEAN
account (the old sandbox got messy). I've given you a fresh, blank AWS
account. I need TaskFlow live on the public internet, reachable by a
plain curl, with backups in S3 — and our bill stays at $0.00.

No hand-holding this time. You've done every piece. Now do it end to
end, from nothing, fast. Send me the public IP when it's live.

And for the love of all things — set the billing alarm FIRST and
shut everything down after the demo. We are not getting a bill.

— Dana
```

> ⚔️ **Boss Battle rules:** No step-by-step tutorial. Use your notes, the AWS docs, and everything you built across Levels 1–5. You win when every victory condition is met — **and your bill is still $0.00.**

---

## 🎯 Your mission

Starting from a **blank AWS account**, get TaskFlow **live and reachable on the public internet** while **staying in the free tier** — no copying a lesson's steps line by line. You should be able to do this from memory now.

The shape of the job (you decide the exact commands):

1. **Safety first** — alarm + MFA + region, *before* anything billable.
2. **Compute** — one free-tier instance, with a key you control.
3. **Access** — firewall opened correctly; you can SSH in.
4. **Deploy** — Docker + TaskFlow running, reachable from the outside world.
5. **Backups** — a backup archive sitting in a private S3 bucket.
6. **Cleanup** — leave the account at $0.00 when the demo's over.

---

## 🏆 Victory conditions

- [ ] A **billing alarm at $1** exists and its email is **confirmed** (set *before* launching anything)
- [ ] Exactly **one** instance, and it is **`t2.micro` / `t3.micro`** (free-tier eligible)
- [ ] You can **SSH** into the instance with your `.pem` key
- [ ] The **security group** opens 22 (to you) and the app port (to the world)
- [ ] `curl http://<PUBLIC_IP>:<port>` from **outside the server** returns TaskFlow — it is **reachable on the public internet**
- [ ] A **TaskFlow backup** is in a **private S3 bucket** (verified with `aws s3 ls`)
- [ ] **Bill = $0.00** and, after the "demo," the instance is **Stopped or Terminated**
- [ ] You can explain *out loud* why each piece is free-tier safe

---

## 🧪 How you'll know you won

From a device **off the server** (your laptop, ideally your phone on cellular):

```bash
curl -i http://<PUBLIC_IP>:3000      # TaskFlow responds → it's LIVE on the internet
aws s3 ls s3://<your-bucket>/backups/ # your backup is listed → durable copy exists
```

If both succeed and your **Billing → Bills** still reads **$0.00**, you've cleared the Empty Cloud.

<details>
<summary>🔎 Reference outline — only after you've tried it yourself!</summary>

This is an **outline**, not copy-paste commands — fill in the details from the lessons.

**Phase 0 — Safety (Level 1)**
1. Region → `us-east-1`. Enable Free Tier + Billing alerts.
2. CloudWatch (in `us-east-1`) → billing alarm **> $1** → SNS to your email → **confirm the email**.
3. MFA on root.

**Phase 1 — Compute (Level 2)**
4. EC2 → Launch → Ubuntu 22.04, **`t2.micro`** (confirm *Free tier eligible*), **1** instance.
5. New key pair `taskflow-key.pem`; on your laptop `chmod 400` it.
6. Enable auto-assign public IP. Wait for **Running · 2/2 checks**; note the **Public IP**.

**Phase 2 — Access (Level 3)**
7. Security group inbound: **22/TCP from My IP**, **3000/TCP from 0.0.0.0/0**.
8. `ssh -i ~/.ssh/taskflow-key.pem ubuntu@<IP>` → you're in.

**Phase 3 — Deploy (Level 4)**
9. On the box: `sudo apt update && sudo apt install -y docker.io docker-compose-v2 git`; `sudo systemctl enable --now docker`; `sudo usermod -aG docker ubuntu`; re-login.
10. Get the code (git clone HTTPS or `scp` from laptop). `docker compose up -d --build`.
11. `curl localhost:3000` on the box, then `curl http://<IP>:3000` from your laptop → **live**.

**Phase 4 — Backups (Level 5)**
12. Create a **private** bucket `taskflow-backups-<name>-<rand>` in `us-east-1`.
13. `aws configure` (ideally the least-privilege `deployer` profile). `tar` a backup, `aws s3 cp` it to `s3://<bucket>/backups/`. Verify with `aws s3 ls`.

**Phase 5 — Cleanup**
14. After the demo: EC2 → **Stop** (keep it) or **Terminate** (done). Confirm no Elastic IPs, no stray volumes. Bill = **$0.00**.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **☁️ Cloud Walker** — you took an app from a laptop to the public internet
- 🔓 **World 7 — CI/CD** unlocks (you deployed by hand; next you'll *automate* it)
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 6 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: a month ago, "deploy to a server" was a vague phrase. You just did it from a blank account in under an hour — safely. That's a real engineer's superpower.

---

## 🛑 FINAL COST WARNING — read before you walk away

You just left running infrastructure in a cloud account that bills by the hour. **Do not skip this.**

- 🔻 **Stop** the instance if you'll use it again soon, or **Terminate** it if you're done. A forgotten Running instance is *the* classic surprise bill.
- 🔻 Release any **Elastic IPs** (you shouldn't have any — verify).
- 🔻 Delete stray **EBS volumes** and oversized **S3 objects**.
- 🔻 Confirm **Billing → Bills** = **$0.00** and your **$1 alarm** is still armed.
- 🔻 Run the [checklist.md](checklist.md) "Did I shut everything down?" sweep.

> ✅ **You only truly beat this boss when the app went live AND your bill stayed at $0.00.** Live app + clean account = victory.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🔁 Enter World 7 →](../phase-07-cicd/README.md)
