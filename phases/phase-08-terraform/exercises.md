# 🏋️ World 8 — Exercises

Extra reps to make Terraform automatic. None are required to advance, but each deepens your IaC instincts. Side Quests award **+50 XP** each.

> 💸 Every exercise that runs `apply` must end in `terraform destroy`. Terraform is free; the AWS resources it builds are not. Stay on `t2.micro`/`t3.micro` and tear down when done.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (HCL & the loop)

Do these inside `~/projects/taskflow-infra` (Ubuntu/WSL2):

1. Format every `.tf` file in the folder to canonical style.
   <details><summary>Hint</summary>`terraform fmt`</details>
2. Check your config for syntax/internal errors without touching AWS.
   <details><summary>Hint</summary>`terraform validate`</details>
3. Show the full plan and save it to a file you can reread.
   <details><summary>Hint</summary>`terraform plan -out=tf.plan` then `terraform show tf.plan`</details>
4. Print just the `public_ip` output without re-applying.
   <details><summary>Hint</summary>`terraform output public_ip` (after an apply)</details>
5. List every resource Terraform is currently tracking in state.
   <details><summary>Hint</summary>`terraform state list`</details>
6. Add a new variable `project_name` (default `"taskflow"`) and use it in your resource `tags`.
   <details><summary>Hint</summary>Declare in `variables.tf`, reference as `var.project_name` inside the `tags` map.</details>
7. Add an output `ssh_command` that prints `ssh ubuntu@<public_ip>`.
   <details><summary>Hint</summary>`value = "ssh ubuntu@${aws_instance.taskflow.public_ip}"`</details>

## Concept reps

8. Explain, in one sentence each, what `init`, `plan`, `apply`, and `destroy` do.
9. Without running it, predict the plan output if you change `instance_type` from `t2.micro` to `t3.micro` on an *already-applied* instance. (Hint: is that change in-place or a replacement?)
   <details><summary>Hint</summary>Changing the instance type forces a stop/replace — look for `~` (update) or `-/+` (replace) in the plan. Try it, then `destroy`.</details>

---

## 🌟 Side Quest — Refactor into a reusable module (+50 XP)

Right now your `main.tf` defines the server inline. Real teams package repeated infrastructure into a **module** — a reusable folder of `.tf` files you call with inputs, like a function for infrastructure. Refactor TaskFlow's server into a module and call it from your root config.

### Step 1 — Create the module folder

```bash
cd ~/projects/taskflow-infra
mkdir -p modules/taskflow-server
```

### Step 2 — Move the server definition into the module

Create `modules/taskflow-server/main.tf` with the AMI data source, key pair, security group, and instance (the same resources you wrote in Level 2). Give the module **its own inputs and outputs**:

```hcl
# modules/taskflow-server/variables.tf
variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "public_key_path" {
  type    = string
  default = "~/.ssh/id_ed25519.pub"
}
```

```hcl
# modules/taskflow-server/outputs.tf
output "public_ip" {
  value = aws_instance.taskflow.public_ip
}
```

Inside the module's `main.tf`, use `var.instance_type` and `file(var.public_key_path)`. (No `provider` block inside a module — it inherits the caller's.)

### Step 3 — Call the module from the root

Replace your root `main.tf` resources with a `module` block:

```hcl
# main.tf (root)
provider "aws" {
  region = var.region
}

module "server" {
  source        = "./modules/taskflow-server"
  instance_type = var.instance_type
}

# Re-expose the module's output from the root
output "public_ip" {
  value = module.server.public_ip
}
```

### Step 4 — Re-init (modules require it) and verify

```bash
terraform init     # picks up the new module
terraform plan     # should still plan the same 3 resources
terraform apply    # type yes
terraform output public_ip
terraform destroy  # stay free!
```

🎯 **Side quest complete when:** the server is defined in `modules/taskflow-server/`, your root config calls it via a `module` block, `terraform apply` builds the same infrastructure through the module, and you can explain why a module is reusable (you could call it twice with different `instance_type`s for two environments). Add **+50 XP**.

> 💡 Bonus thought: how would you spin up *staging* and *production* servers from this one module without duplicating the resource code?

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
