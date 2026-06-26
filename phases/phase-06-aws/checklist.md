# ✅ World 6 — Readiness Checklist

Before you face the Boss Battle and unlock World 7, make sure all of this is true. If any box is empty, revisit that lesson — and on AWS, an unchecked box can mean a **surprise charge**, so be honest.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 💸 Cost safety (the most important section)
- [ ] A **billing alarm at $1** exists and its email subscription is **confirmed**
- [ ] **Free Tier usage alerts** and **Billing alerts** are enabled
- [ ] Root user has **MFA** turned on
- [ ] I only ever launched **`t2.micro` / `t3.micro`** instances
- [ ] I never ran **more than one** instance at a time
- [ ] I have **no Elastic IPs** reserved and no extra/forgotten resources

## ☁️ Cloud skills
- [ ] I can explain the cloud, **regions**, and **availability zones** in plain words
- [ ] I launched a free-tier EC2 instance and reached **Running · 2/2 checks**
- [ ] I have my **`.pem` key** saved with `chmod 400`
- [ ] I configured **security group** inbound rules (22 from My IP, 3000 from Anywhere)
- [ ] I can **SSH** into the instance with `ssh -i`
- [ ] I installed **Docker** on the instance and ran TaskFlow with `docker compose up -d`
- [ ] `curl http://<PUBLIC_IP>:3000` works **from outside** the server
- [ ] I created a private **S3 bucket** and uploaded a backup with the CLI

## 🔎 Self-test (do this from memory — no notes)
Picture a fresh, blank AWS account. Without looking, list the **ordered** steps to get TaskFlow live and reachable while staying free:

<details>
<summary>✅ One correct ordering</summary>

1. **Set the $1 billing alarm + enable MFA** (before anything billable).
2. Pick region **`us-east-1`**.
3. Launch **one `t2.micro`** Ubuntu instance; create + save the **`.pem` key** (`chmod 400`).
4. **Security group:** open **22 (My IP)** and **3000 (Anywhere)**.
5. **SSH in** with `ssh -i`.
6. **Install Docker**, get TaskFlow code on the box, `docker compose up -d`.
7. **`curl http://<PUBLIC_IP>:3000`** from outside → confirm it's live.
8. Create a private **S3 bucket**, upload a backup.
9. When done: **Stop or Terminate** the instance.
</details>

If you produced that order without peeking — you're ready for the boss.

---

## 🛑 "Did I shut everything down / am I still free?" check
Run through this **every time** you stop working, especially before closing your laptop:

- [ ] EC2 → Instances: instance is **Stopped** or **Terminated** (not silently Running)
- [ ] EC2 → Elastic IPs: **none reserved** (an unattached one bills)
- [ ] EC2 → Volumes: no stray volumes beyond your instance's
- [ ] S3: only small backups, well under **5 GB**
- [ ] **Billing → Free Tier**: usage under all limits
- [ ] **Billing → Bills**: estimated charges this month = **$0.00**
- [ ] My **$1 alarm** is still armed and hasn't fired

<details>
<summary>🔎 Fast CLI sweep (optional)</summary>

```bash
# Any running instances?
aws ec2 describe-instances \
  --query "Reservations[].Instances[?State.Name=='running'].[InstanceId,InstanceType]" \
  --output table

# Any reserved Elastic IPs (these can bill if unattached)?
aws ec2 describe-addresses --query "Addresses[].PublicIp" --output table

# Bucket sizes / contents
aws s3 ls
```
</details>

> If everything's stopped/terminated, no Elastic IPs, and the bill reads **$0.00** — you stayed free. That's the real win of this world.

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I did the **least-privilege IAM user** Side Quest (+50 XP)

---

> All checked — *and your bill is $0.00*? → [👹 Face the Boss Battle: The Empty Cloud](boss-battle.md)

[← World Home](README.md)
