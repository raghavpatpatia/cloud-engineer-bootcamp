# 👹 Boss Battle — The Locked Server

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 3 — Git |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Priya (DevOps Lead) <priya@cloudforge.inc>
To:      You
Subject: [URGENT] TaskFlow staging box is misbehaving — help

The staging server hosting an early TaskFlow build is a mess and I'm in
back-to-back meetings. Three things are wrong at once:

  1. The nightly backup script won't run — just says "Permission denied."
  2. A config file got the wrong owner/permissions during a sloppy deploy:
     it's owned by root and is world-readable, even though it holds a secret.
  3. Something is pinning the CPU at 100% and the box is crawling. Find it
     and stop it.

You know enough Linux now. Diagnose and fix all three. No step-by-step —
show me you can think on a server. Write down what you did and WHY.

— Priya
```

> ⚔️ **Boss Battle rules:** No tutorials. Use your notes, `man <command>`, and everything you built this world. You win when every victory condition is met **and you can explain why** each fix works.

---

## 🎯 Your mission

You'll reproduce all three problems in a safe sandbox, then fix them. Set the scene first:

```bash
# Build the broken "server" sandbox
mkdir -p ~/locked-server && cd ~/locked-server

# Problem 1: a backup script with NO execute bit
cat > backup.sh << 'EOF'
#!/bin/bash
echo "Backing up TaskFlow at $(date +%Y-%m-%d_%H-%M-%S)"
EOF
chmod 644 backup.sh                    # note: no +x

# Problem 2: a secret config file, world-readable AND owned by root
echo "DB_PASSWORD=supersecret" > config.env
sudo chown root:root config.env
sudo chmod 644 config.env              # -rw-r--r-- : others can read the secret!

# Problem 3: a runaway process eating CPU
( while true; do :; done ) &           # infinite busy loop in the background
echo "Runaway PID: $!"                 # $! is the PID of the last background job
```

Now **fix all three** using what you learned. Record your diagnosis and fixes in `~/locked-server/INCIDENT.md`.

### Part A — The script that won't run
Make `backup.sh` runnable, then run it. Explain *why* it failed.

### Part B — The exposed secret
`config.env` is owned by `root` and readable by everyone. Make it owned by **you** and readable/writable by **only you**. Explain the risk it posed.

### Part C — The runaway process
Find the process pinning the CPU, confirm it with a live view, and kill it. Explain how you identified it.

---

## 🏆 Victory conditions

- [ ] `ls -l backup.sh` shows an execute bit (e.g. `-rwxr-xr-x`) and `./backup.sh` runs
- [ ] `ls -l config.env` shows it owned by **you** and permissions `-rw-------` (`600`)
- [ ] The runaway busy-loop process is gone (`top`/`htop` shows CPU back to normal; `jobs` is empty)
- [ ] `~/locked-server/INCIDENT.md` records the **cause and fix** for all three problems
- [ ] You can say out loud *why* each fix works — not just *what* you typed

---

## 🧪 How you'll know you won

After your fixes: `./backup.sh` prints a backup line, `ls -l config.env` reads `-rw------- 1 yourname yourname`, and `top` no longer shows a process near 100% CPU. If `INCIDENT.md` explains all three in your own words, you've beaten the boss.

<details>
<summary>🔎 Reference solution — only after you've tried! (Part A — the script)</summary>

```bash
cd ~/locked-server
ls -l backup.sh            # -rw-r--r--  → no x, so the OS refuses to run it
chmod +x backup.sh         # add the execute bit
./backup.sh                # now it runs
```

**Why:** The kernel won't execute a file that lacks the execute permission. The script was created `644` (read/write only). `chmod +x` adds `x`, making it a runnable program.
</details>

<details>
<summary>🔎 Reference solution — Part B (the exposed secret)</summary>

```bash
ls -l config.env                  # -rw-r--r-- root root  → world-readable secret, wrong owner
sudo chown $USER:$USER config.env # take ownership (needs sudo — it's root's file)
chmod 600 config.env              # owner rw, group nothing, others nothing
ls -l config.env                  # -rw------- yourname yourname
```

**Why:** A file holding a password should never be readable by `others` (the `r` in the last triplet) — anyone with an account on the box could `cat` the secret. `600` removes group/other access entirely. Ownership had to change with `sudo` because you can't modify a file root owns until it's yours.
</details>

<details>
<summary>🔎 Reference solution — Part C (the runaway process)</summary>

```bash
# Spot the CPU hog live (look for ~100% CPU, then quit with q)
top
# or:
htop

# Find its PID without scrolling — the busy loop is a bash subshell
ps aux --sort=-%cpu | head -5     # highest-CPU processes first
pgrep -f "while true"             # or grab the PID you printed earlier ($!)

# Stop it politely; if it ignores you, force it
kill <PID>
# kill -9 <PID>                   # last resort

jobs                              # confirm the background job is gone
```

**Why:** A process is identified by its **PID**. `top`/`htop` reveal which PID is burning CPU; `ps aux --sort=-%cpu` lists the worst offenders. `kill <PID>` sends a polite terminate signal; `kill -9` force-kills if it won't stop. Always confirm you're killing the *right* PID before pulling the trigger.
</details>

<details>
<summary>🔎 Reference — a tidy INCIDENT.md</summary>

```markdown
# Incident report — TaskFlow staging

## 1. Backup script wouldn't run
- Cause: backup.sh had no execute bit (644).
- Fix: `chmod +x backup.sh`. The OS won't run a file without x.

## 2. Exposed secret config
- Cause: config.env owned by root and 644 (world-readable) — anyone could read DB_PASSWORD.
- Fix: `sudo chown $USER:$USER config.env && chmod 600 config.env`. Secrets must be owner-only.

## 3. Runaway CPU process
- Cause: an infinite busy-loop process pinned the CPU at ~100%.
- Fix: found the PID with `top` / `ps aux --sort=-%cpu`, then `kill <PID>`.
```
</details>

> 🧹 Clean up the sandbox when you're done: `cd ~ && rm -r ~/locked-server`. If any background loop survived, `pkill -f "while true"`.

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🐧 Achievement unlocked: **Penguin Whisperer** — you can survive on a Linux box alone
- 🔓 **World 3 — Git** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 2 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: all three problems are *real* — engineers hit them on production servers constantly. The reflex you just built (read permissions, check ownership, find the runaway PID) is exactly what on-call work feels like.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🌿 Enter World 3 →](../phase-03-git/README.md)
