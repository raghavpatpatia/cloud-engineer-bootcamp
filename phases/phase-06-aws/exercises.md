# 🏋️ World 6 — Exercises

Extra reps to make AWS feel routine. None are required to advance, but each makes the boss battle (and real life) smoother. The Side Quest awards **+50 XP**.

> 💸 **Cost note:** every exercise here is free-tier safe. Anything that touches a running instance, **Stop** it when you finish.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (console + concepts)

Do these in the AWS Console / CLI:

1. Confirm which **region** you're in and switch it to `us-east-1`.
   <details><summary>Hint</summary>Top-right region dropdown. Resources are per-region.</details>
2. Open **Billing → Free Tier** and read your current EC2 and S3 usage.
   <details><summary>Hint</summary>Account menu → Billing and Cost Management → Free Tier.</details>
3. From the EC2 console, find your instance's **Public IPv4** and its **AMI ID**.
   <details><summary>Hint</summary>EC2 → Instances → select → Details tab.</details>
4. List your security group's **inbound rules** and state the purpose of each.
   <details><summary>Hint</summary>EC2 → instance → Security tab → click the SG.</details>
5. SSH in and report the instance's **uptime** and **free disk space**.
   <details><summary>Hint</summary>`ssh -i ... ubuntu@<IP>` then `uptime` and `df -h`.</details>

## CLI warm-ups

6. Use the AWS CLI to list **all your S3 buckets**.
   <details><summary>Hint</summary>`aws s3 ls`</details>
7. Use the CLI to show the **caller identity** of your configured credentials.
   <details><summary>Hint</summary>`aws sts get-caller-identity`</details>
8. Copy a small text file to S3 and then **delete** it again with the CLI.
   <details><summary>Hint</summary>`aws s3 cp file.txt s3://<bucket>/` then `aws s3 rm s3://<bucket>/file.txt`</details>

---

## 🌟 Side Quest — Create a Least-Privilege IAM User (+50 XP)

Using the **root user** for daily work is risky (Level 1). Real engineers create an **IAM user** with only the permissions they need. Build one.

**Goal:** an IAM user named `taskflow-deployer` that can manage EC2 and S3 but **cannot** touch billing or delete the account.

1. Console → **IAM → Users → Create user**. Name it `taskflow-deployer`.
2. **Permissions:** attach the AWS-managed policies **`AmazonEC2FullAccess`** and **`AmazonS3FullAccess`** (a deliberately *scoped* set — not `AdministratorAccess`). This is "least privilege": only what the role needs.
3. Create the user. Then **Security credentials → Create access key** (choose "CLI") and save the key pair safely.
4. On your laptop, configure a **named profile** so you can switch between root and this user:
   ```bash
   aws configure --profile deployer
   # paste the new access key / secret / us-east-1 / json
   aws sts get-caller-identity --profile deployer   # should show the IAM user's ARN, not root
   ```
5. Use it for an S3 command to prove it works:
   ```bash
   aws s3 ls --profile deployer
   ```
6. Now prove the **boundary**: try a billing action and watch it get denied (it lacks billing permissions). That denial *is the point* — a leaked deployer key can't run up surprise charges via billing changes or spin up resources outside EC2/S3.

🎯 **Side quest complete when:** `aws sts get-caller-identity --profile deployer` shows the **IAM user** (not root), the user can do EC2/S3 work, and you can explain in one sentence why least privilege limits the blast radius of a leaked key. Add **+50 XP**.

> 🔒 After this, **enable MFA on the IAM user too**, and from now on prefer the `deployer` profile over root for World 6 work.

---

## 🌟 Bonus drill — Stop/Start round-trip (no XP, pure muscle memory)

1. **Stop** your instance, watch the state go `stopping → stopped`.
2. Note that compute billing pauses while stopped.
3. **Start** it again; observe it gets a **new public IP** (you didn't reserve an Elastic IP — good).
4. Update your `aws-setup-notes.md` with the new IP and re-test `curl http://<IP>:3000`.

This is exactly the habit that keeps your bill at $0.00: **stop when idle, start when needed.**

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
