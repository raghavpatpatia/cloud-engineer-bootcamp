# 👹 Boss Battle — The Broken Workstation

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 1 — Internet Fundamentals |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    IT Support <it@cloudforge.inc>
To:      You
Subject: [URGENT] Teammate's laptop is a mess — can you sanity-check yours?

A new hire's machine "kind of works but kind of doesn't." Before we
trust you with a real ticket, prove YOUR environment is solid AND that
you can diagnose a broken one. No step-by-step this time — you know
enough now. Show me you can think.

— IT
```

> ⚔️ **Boss Battle rules:** No tutorials. Use your notes, the docs, and everything you built. You win when every victory condition is met **and you can explain why**.

---

## 🎯 Your mission

There are **two parts**. Do both.

### Part A — Prove your environment (the audit)
Produce a single command sequence (or short script) that proves your setup is healthy. It must demonstrate, with real output, that:

1. You're running **Linux via WSL2** (not Windows/PowerShell)
2. **Node.js** and **npm** are installed (show versions)
3. You can **create, write, read, and delete** a file from the terminal
4. You can **run a `.js` file** with Node

Save the output to a file named `audit-report.txt` in `~/projects`.

### Part B — Diagnose the broken machine (the puzzle)
A teammate reports these three symptoms. For **each**, explain the likely cause **and** the fix. Write your answers in `~/projects/diagnosis.md`.

> **Symptom 1:** "I typed `wsl --install` but got *'Access is denied'*."
>
> **Symptom 2:** "Inside Ubuntu, `node hello.js` says *'node: command not found'* — but my friend installed Node yesterday on the same machine in PowerShell."
>
> **Symptom 3:** "VS Code opens, but the bottom-left corner doesn't say *WSL: Ubuntu*, and my edits don't show up when I `cat` the file in Ubuntu."

---

## 🏆 Victory conditions

- [x] `~/projects/audit-report.txt` exists and shows all four proofs from Part A
- [x] `~/projects/diagnosis.md` explains a **cause and a fix** for all three symptoms
- [x] You can say out loud *why* each fix works (not just *what* to type)

---

## 🧪 How you'll know you won

Run your audit. If the report contains a Linux kernel line, two version numbers, a file round-trip, and Node output — Part A is done. For Part B, your explanations should match the spirit of the reference below.

<details>
<summary>🔎 Reference solution — only after you've tried! (Part A)</summary>

```bash
cd ~/projects
{
  echo "=== 1. Linux/WSL2 ==="
  uname -a
  echo "=== 2. Node & npm ==="
  node --version
  npm --version
  echo "=== 3. File round-trip ==="
  echo "hello boss" > tmp.txt && cat tmp.txt && rm tmp.txt && echo "(file created, read, deleted)"
  echo "=== 4. Run a JS file ==="
  echo "console.log('node runs files ✅')" > t.js && node t.js && rm t.js
} | tee audit-report.txt
```
`tee` prints to screen *and* writes to the file.
</details>

<details>
<summary>🔎 Reference solution — Part B diagnoses</summary>

**Symptom 1 — "Access is denied" on `wsl --install`**
- *Cause:* PowerShell wasn't run as Administrator. WSL installation changes system features, which needs admin rights.
- *Fix:* Right-click PowerShell → **Run as administrator**, then re-run `wsl --install`. Restart afterward.

**Symptom 2 — `node: command not found` in Ubuntu**
- *Cause:* Node was installed on the **Windows** side (in PowerShell), not inside **Ubuntu**. WSL2's Ubuntu is a separate OS with its own software. Installing Node in Windows doesn't put it in Ubuntu.
- *Fix:* Install Node *inside* Ubuntu: `sudo apt update && sudo apt install -y nodejs npm`. Then `node --version` works in the Ubuntu shell.

**Symptom 3 — VS Code not showing "WSL: Ubuntu"**
- *Cause:* VS Code opened a **Windows** folder, not the Linux one — so it's editing different files than the ones Ubuntu sees. The WSL extension isn't connected.
- *Fix:* Install the **WSL** extension, then launch from inside Ubuntu with `code .` from the target folder (e.g. `~/projects`). The corner will show **WSL: Ubuntu**, and edits will match what `cat` shows.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🔓 **World 1 — Internet Fundamentals** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 0 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: which symptom would have stumped you yesterday? That gap you just closed is exactly what this world was for.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🌐 Enter World 1 →](../phase-01-internet-fundamentals/README.md)
