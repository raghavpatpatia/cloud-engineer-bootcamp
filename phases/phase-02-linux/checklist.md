# ✅ World 2 — Readiness Checklist

Before you face the Boss Battle and unlock World 3, make sure all of this is true. If any box is empty, revisit that lesson — the Boss Battle assumes you can do all of it from memory.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧭 Navigation & files
- [ ] I can say where I am (`pwd`) and move around (`cd`, `..`, `~`, `-`)
- [ ] I can tell an absolute path from a relative one
- [ ] I can create files (`touch`) and folders (`mkdir -p`)
- [ ] I can copy (`cp -r`), move/rename (`mv`), and delete (`rm -r`) safely
- [ ] I can read files (`cat`, `less`) and edit them (`nano`)

## 🔐 Permissions & ownership
- [ ] I can read an `rwx` string and name owner/group/others
- [ ] I can set permissions with `chmod` (symbolic and octal: `600`, `644`, `755`)
- [ ] I can change ownership with `chown` (and know it needs `sudo`)
- [ ] I know why a script needs `+x` and a secret file needs `600`

## ⚙️ Processes & packages
- [ ] I can list processes (`ps aux`, `top`/`htop`) and kill one by PID
- [ ] I can background a command with `&`
- [ ] I can install software with `sudo apt update && sudo apt install`

## 📜 Scripting
- [ ] I can write a script with a shebang, variables, and `$(...)`
- [ ] I can make it executable and run it with `./`
- [ ] I understand `tar -czf` for creating archives

## 📦 TaskFlow is born
- [ ] `~/projects/taskflow/` exists with `README.md`, `.gitignore`, `src/`, and `scripts/`
- [ ] `.env` is locked to `600`
- [ ] `scripts/backup.sh` runs and produces a dated archive in `~/backups`

---

## 🔎 Self-test (do this from memory)

Open Ubuntu and, **without notes**, do all of this:

1. Go to `~/projects/taskflow`.
2. Create a script `scripts/info.sh` that prints the current date and the project's folder name.
3. Make it executable and run it.
4. Lock it so only you can read/write/execute it.
5. Show its permission string to confirm.

<details>
<summary>✅ One correct solution</summary>

```bash
cd ~/projects/taskflow
cat > scripts/info.sh << 'EOF'
#!/bin/bash
echo "Date: $(date +%Y-%m-%d)"
echo "Project: $(basename "$PWD")"
EOF
chmod 700 scripts/info.sh
./scripts/info.sh
ls -l scripts/info.sh        # → -rwx------
```
</details>

If you did that without peeking — you're ready for the locked server.

---

## 🎓 XP check
- [ ] I recorded XP for all 5 lessons in [PROGRESS.md](../../PROGRESS.md) (625 XP)
- [ ] (Optional) I did at least one Side Quest (cron and/or `.bashrc` aliases)

---

> All checked? → [👹 Face the Boss Battle: The Locked Server](boss-battle.md)

[← World Home](README.md)
