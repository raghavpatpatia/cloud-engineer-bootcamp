# ✅ World 0 — Readiness Checklist

Before you face the Boss Battle and unlock World 1, make sure all of this is true. If any box is empty, revisit that lesson — don't push forward on a shaky setup.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Tools installed
- [ ] WSL2 is installed and Ubuntu launches
- [ ] I have a Linux username and remember my Linux password
- [ ] VS Code is installed with the **WSL** extension
- [ ] Opening a folder with `code .` shows **"WSL: Ubuntu"** in the corner
- [ ] `node --version` prints a version
- [ ] `npm --version` prints a version

## 🧠 Skills I can do without looking up
- [ ] Open a terminal and tell what folder I'm in (`pwd`)
- [ ] List files, including hidden ones (`ls -la`)
- [ ] Create a folder (`mkdir`) and a file (`touch` / `echo >`)
- [ ] Read a file's contents (`cat`)
- [ ] Run a JavaScript file with `node file.js`

## 🔎 Self-test (do this from memory)
Open Ubuntu and, without notes, run a sequence that:
1. Goes to your home folder
2. Creates a folder called `selftest`
3. Creates a file in it containing your username
4. Prints that file
5. Deletes the folder

<details>
<summary>✅ One correct solution</summary>

```bash
cd ~
mkdir selftest
echo "$(whoami)" > selftest/me.txt
cat selftest/me.txt
rm -r selftest
```
</details>

If you did that without peeking — you're ready.

---

## 🎓 XP check
- [ ] I recorded XP for all 3 lessons in [PROGRESS.md](../../PROGRESS.md) (375 XP)
- [ ] (Optional) I did at least one Side Quest

---

> All checked? → [👹 Face the Boss Battle: The Broken Workstation](boss-battle.md)

[← World Home](README.md)
