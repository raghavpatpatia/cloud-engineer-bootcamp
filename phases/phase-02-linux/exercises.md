# 🏋️ World 2 — Exercises

Extra reps to make Linux automatic. None are required to advance, but each one makes the Boss Battle (and every future world) easier. Side Quests award **+50 XP** each.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (navigation & files)

Do these inside **Ubuntu**:

1. Print your current folder, then list everything including hidden files in long format.
   <details><summary>Hint</summary>`pwd` then `ls -la`</details>
2. From your home folder, list the contents of `/etc` using an absolute path.
   <details><summary>Hint</summary>`ls /etc`</details>
3. Create three nested folders in one command, then draw them.
   <details><summary>Hint</summary>`mkdir -p a/b/c` then `tree a`</details>
4. Create a file, append two lines to it, then read it back.
   <details><summary>Hint</summary>`echo "one" > f.txt` then `echo "two" >> f.txt` then `cat f.txt`</details>
5. Copy a folder and everything inside it to a new name, then delete the copy.
   <details><summary>Hint</summary>`cp -r a a-copy` then `rm -r a-copy`</details>

## Permissions & processes

6. Make a file executable, then read its permission string and give the octal.
   <details><summary>Hint</summary>`chmod +x f.sh` then `ls -l f.sh` — `-rwxr-xr-x` is `755`</details>
7. Lock a file so only you can read/write it; confirm with `ls -l`.
   <details><summary>Hint</summary>`chmod 600 f.txt` → `-rw-------`</details>
8. Start `sleep 200 &`, find its PID, then kill it.
   <details><summary>Hint</summary>`sleep 200 &` then `pgrep -f "sleep 200"` then `kill <PID>`</details>
9. Install a package, check its version, then (optionally) remove it.
   <details><summary>Hint</summary>`sudo apt update && sudo apt install -y ncdu` then `ncdu --version`</details>

## Scripting

10. Write a one-line script that prints `Backing up <foldername>` for the current folder, make it executable, and run it.
    <details><summary>Hint</summary>`#!/bin/bash` then `echo "Backing up $(basename $(pwd))"`; `chmod +x`; `./script.sh`</details>

---

## 🌟 Side Quest — Schedule the Backup with cron (+50 XP)

You wrote `backup.sh` in Level 5. A backup you have to *remember* to run is a backup that won't happen. Let's make Linux run it automatically.

**`cron`** is the built-in scheduler. Each line in your "crontab" (cron table) says *when* to run *what*.

```bash
# Open YOUR personal crontab in an editor
crontab -e
```
(The first time, it asks which editor — pick `nano`.)

Add this line at the bottom, then save and exit:

```cron
# ┌ minute (0)  ┌ hour (2 = 2 AM)  ┌ every day  ┌ every month  ┌ any weekday
0 2 * * * /home/YOURNAME/projects/taskflow/scripts/backup.sh
```

Replace `YOURNAME` with your username (find it with `whoami`). This runs the backup **every day at 2 AM**.

The five fields are: `minute hour day-of-month month day-of-week`. A `*` means "every." So `0 2 * * *` = "at minute 0 of hour 2, every day."

```bash
# Confirm your scheduled job is registered
crontab -l
```

> 💡 **Test it without waiting until 2 AM:** temporarily set the schedule to run a couple of minutes from now (e.g. if it's 14:10, use `12 14 * * *`), watch `~/backups` for a new archive, then change it back to `0 2 * * *`. WSL note: cron only runs while WSL is open — start it with `sudo service cron start` if your backup never appears.

🎯 **Side quest complete when:** `crontab -l` shows your backup line, and you can explain what each of the five fields means. Add **+50 XP**.

---

## 🌟 Side Quest — Make Your Aliases Permanent (+50 XP)

In World 0 you made a temporary alias that vanished when you closed the terminal. Now make it stick by saving it to `~/.bashrc` — the file Bash reads every time it starts.

```bash
# Append two handy aliases to your shell startup file
echo "alias ll='ls -la'" >> ~/.bashrc
echo "alias backup='~/projects/taskflow/scripts/backup.sh'" >> ~/.bashrc

# Reload .bashrc so the changes take effect now (instead of reopening the terminal)
source ~/.bashrc

# Test them
ll
backup
```

🎯 **Complete when:** opening a *fresh* terminal and typing `ll` runs `ls -la`, and `backup` runs your script. Explain why these now survive a restart (hint: they live in `~/.bashrc`). Add **+50 XP**.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
