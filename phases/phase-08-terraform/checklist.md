# ✅ World 8 — Readiness Checklist

Before you face the Boss Battle and unlock World 9, make sure all of this is true. If any box is empty, revisit that lesson — don't go into "rebuild from nothing" on shaky state knowledge.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Tooling & setup
- [ ] `terraform version` prints a version (Terraform installed)
- [ ] AWS credentials work (Terraform reads my World 6 `~/.aws/credentials`)
- [ ] `~/projects/taskflow-infra` is a git repo with `.terraform/` and `*.tfstate` git-ignored
- [ ] I have an SSH public key for the `aws_key_pair` (`~/.ssh/id_ed25519.pub`)

## 📄 Config I can write
- [ ] A `provider "aws"` block with a region
- [ ] An `aws_instance` (t2.micro/t3.micro), `aws_security_group` (22 + 3000), and `aws_key_pair`
- [ ] An `aws_ami` **data source** instead of a hardcoded AMI ID
- [ ] `variables.tf` + `terraform.tfvars` to parametrize region & instance type
- [ ] `outputs.tf` exposing the public IP / app URL

## 🧠 Concepts I understand
- [ ] Declarative IaC: I describe desired state, Terraform reconciles
- [ ] The loop: `init` → `plan` → `apply` → `destroy` (and what each does)
- [ ] What `terraform.tfstate` is and why I never hand-edit it
- [ ] What **drift** is and how `plan` detects it
- [ ] Why teams use **remote state**

## 🔎 Self-test (do this from memory)
In `~/projects/taskflow-infra`, without notes, run a sequence that:
1. Initializes the project
2. Previews the plan (no changes made)
3. Builds the TaskFlow instance + security group + key pair
4. Prints the public IP from an output
5. Destroys everything so you owe nothing

<details>
<summary>✅ One correct solution</summary>

```bash
cd ~/projects/taskflow-infra
terraform init
terraform plan
terraform apply              # type yes
terraform output public_ip
terraform destroy            # type yes
```
</details>

If you did that without peeking — you're ready.

---

## 💸 Did I stay free?
- [ ] Every instance I created was `t2.micro` or `t3.micro`
- [ ] I ran **`terraform destroy`** after every lab and exercise
- [ ] I confirmed in the AWS console that **no EC2 instance is running**
- [ ] My World 6 billing alarm is still active

> If anything is still running, run `terraform destroy` now and verify in the console before continuing.

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I did the **Refactor into a reusable module** Side Quest (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: Rebuild From Nothing](boss-battle.md)

[← World Home](README.md)
