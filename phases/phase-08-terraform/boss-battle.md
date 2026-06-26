# 👹 Boss Battle — Rebuild From Nothing

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 45 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 9 — Kubernetes |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Priya (DevOps Lead) <priya@cloudforge.inc>
To:      You <you@cloudforge.inc>
Subject: [INCIDENT-008] Prove the infra is REALLY code

It's review time. You've told me TaskFlow's infrastructure is "code now."
I'm going to make you prove it.

The claim: if I delete the entire TaskFlow environment, you can rebuild
it from your .tf files alone — same instance, same security group, same
key — and the app comes back reachable. No console clicking. No sticky
notes. Just `terraform apply`.

So do it for real:
  1. terraform destroy the WHOLE environment. Watch it go to nothing.
  2. terraform apply and rebuild it from code.
  3. Confirm TaskFlow answers on http://<public-ip>:3000.

And because real incidents are never clean: a colleague "helpfully"
started a fresh infra folder for our new region and it's BROKEN. I've
dropped their files below. Fix them so they apply correctly — that's
your proof you actually understand HCL, not just copy-paste.

⚠️ t2.micro/t3.micro ONLY, and terraform destroy when you're done.
   I will personally check the bill.

— Priya
```

> ⚔️ **Boss Battle rules:** No tutorials. Use your `.tf` files, the docs, and everything you built across Levels 1–4. You win when every victory condition is met **and you can explain why each fix works**.

---

## 🎯 Your mission

There are **two parts**. Do both.

### Part A — Rebuild from nothing (the proof)
Using your `~/projects/taskflow-infra` config:

1. **Destroy** the entire environment and confirm it's gone (state empty, nothing in the console).
2. **Apply** to rebuild the instance + security group + key pair **from code alone**.
3. **Confirm reachability:** the app responds on `http://<public-ip>:3000`.

> 🧩 To actually serve TaskFlow on the rebuilt box you need the app running. You may either SSH in and run TaskFlow's Docker container (as in World 6), **or** add a `user_data` startup script to your `aws_instance` that installs Docker and runs a placeholder web server on port 3000. Either proves the box is reachable on 3000. Whichever you pick, the *infrastructure* must come entirely from `terraform apply`.

<details>
<summary>💡 Optional: a minimal `user_data` to prove port 3000 is reachable</summary>

Add this to your `aws_instance` so the box self-serves something on 3000 at boot (handy if you don't want to SSH in to start the real app):

```hcl
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    systemctl enable --now docker
    # Stand-in web server on 3000 to prove reachability
    docker run -d -p 3000:80 --restart unless-stopped nginxdemos/hello
  EOF
```

Then after apply, `curl http://$(terraform output -raw public_ip):3000` should return HTML. Swap in TaskFlow's real container when you wire up the actual app.
</details>

### Part B — Fix the broken infra (the puzzle)
Your colleague's `main.tf` (below) **fails to apply**. There are **four** distinct bugs. Find and fix all four, then prove it applies cleanly. Write what each bug was and why your fix works in `~/projects/taskflow-infra/INCIDENT_NOTES.md`.

```hcl
# colleague's BROKEN main.tf  --  fix the 4 bugs

provider "aws" {
  region = var.region
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_security_group" "taskflow" {
  name        = "taskflow-sg"
  description = "Allow SSH and app"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # BUG: the app needs to be reachable on 3000 — but nothing opens it

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "taskflow" {
  ami                    = aws_ami.ubuntu.id          # BUG #1
  instance_type          = "m5.large"                 # BUG #2
  vpc_security_group_ids = aws_security_group.taskflow.id   # BUG #3

  tags = {
    Name = "taskflow-server"
  }
}

# BUG #4: var.region is used but never declared anywhere
```

---

## 🏆 Victory conditions

- [ ] **Clean destroy:** `terraform destroy` removed the whole environment (`Resources: N destroyed`), and the AWS console shows nothing running
- [ ] **Clean apply:** `terraform apply` rebuilt the instance + security group + key pair from code (`Apply complete!`)
- [ ] **App reachable:** `http://<public-ip>:3000` responds (curl returns content)
- [ ] **Part B fixed:** the colleague's config applies cleanly with all 4 bugs fixed, documented in `INCIDENT_NOTES.md`
- [ ] **Stays free:** instance is `t2.micro`/`t3.micro`, and you ran `terraform destroy` at the end ($0.00)
- [ ] You can explain **why** each fix works (not just what you typed)

---

## 🧪 How you'll know you won

Run the rebuild loop and watch state go to zero, then back to three resources. Curl the IP on port 3000 and get a response. For Part B, after your fixes `terraform plan` shows a valid plan with **no errors** and a `t2.micro`/`t3.micro` instance. Compare against the references below — but only after you've tried.

<details>
<summary>🔎 Reference solution — Part A (rebuild loop)</summary>

```bash
cd ~/projects/taskflow-infra

# 1. Destroy the whole environment, prove it's gone
terraform destroy            # type yes
terraform state list         # should print nothing

# 2. Rebuild from code alone
terraform apply              # type yes -> 3 resources added (+ user_data if used)

# 3. Confirm reachability on port 3000
IP=$(terraform output -raw public_ip)
echo "Try: http://$IP:3000"
curl -s "http://$IP:3000" | head    # returns HTML once the app/container is up

# 4. Tear it down to stay free
terraform destroy            # type yes
```
The key insight: `destroy` worked off **state**, and `apply` rebuilt from **code** — at no point did you click in the console. That's the proof the infrastructure is truly code.
</details>

<details>
<summary>🔎 Reference solution — Part B (the 4 bugs)</summary>

**Bug #1 — `ami = aws_ami.ubuntu.id`**
- *Cause:* `aws_ami` here is a **data source**, not a resource. Data sources are referenced with the `data.` prefix.
- *Fix:* `ami = data.aws_ami.ubuntu.id`

**Bug #2 — `instance_type = "m5.large"`**
- *Cause:* `m5.large` is **not free-tier eligible** — it bills real money. Violates Priya's rule.
- *Fix:* `instance_type = "t2.micro"` (or `t3.micro`).

**Bug #3 — `vpc_security_group_ids = aws_security_group.taskflow.id`**
- *Cause:* `vpc_security_group_ids` expects a **list**, but a single ID (string) was passed.
- *Fix:* wrap it in brackets → `vpc_security_group_ids = [aws_security_group.taskflow.id]`

**Bug #4 — `var.region` used but never declared**
- *Cause:* the provider references `var.region`, but there's no `variable "region"` declaration, so `plan` errors with "Reference to undeclared input variable."
- *Fix:* add a declaration (in `variables.tf` or this file):
  ```hcl
  variable "region" {
    type    = string
    default = "us-east-1"
  }
  ```

**Bonus — the missing port 3000 ingress** (called out in a comment): the app won't be reachable without it. Add:
```hcl
  ingress {
    description = "TaskFlow app"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
```
(Also note: this config has no `aws_key_pair`, so you couldn't SSH in — fine for a pure-`user_data` box, but add one if you need shell access.)

After all fixes: `terraform validate` passes and `terraform plan` produces a clean plan with a free-tier instance.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **🏗️ The Architect** — *you can summon and dismiss an entire environment from a file.*
- 🔓 **World 9 — Kubernetes** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 8 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: a month ago, rebuilding that server meant a sticky note and a prayer. Now it's one command. That's the entire promise of Infrastructure as Code — and you just proved it works.

---

## 💸 Final cost check — do not skip

```bash
cd ~/projects/taskflow-infra
terraform destroy        # type yes
terraform state list     # should be empty
```

Then open the AWS console (EC2 → Instances) and confirm **nothing is running**. Leaving the boss-battle box up is the single easiest way to get a surprise bill. Verify, then celebrate.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [☸️ Enter World 9 →](../phase-09-kubernetes/README.md)
