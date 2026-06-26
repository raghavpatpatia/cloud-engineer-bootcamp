# 🏋️ World 0 — Exercises

Extra reps to make the basics automatic. None are required to advance, but each makes the rest of the bootcamp smoother. Side Quests award **+50 XP** each.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (terminal fluency)

Do these inside **Ubuntu**:

1. Print your current folder, then list its contents in long format.
   <details><summary>Hint</summary>`pwd` then `ls -la`</details>
2. Create three nested folders in one command.
   <details><summary>Hint</summary>`mkdir -p a/b/c`</details>
3. Create an empty file, then delete it.
   <details><summary>Hint</summary>`touch temp.txt` then `rm temp.txt`</details>
4. Display the current date and time.
   <details><summary>Hint</summary>`date`</details>
5. Clear the screen without closing the terminal.
   <details><summary>Hint</summary>`clear` (or `Ctrl+L`)</details>

## Node warm-ups

6. Use `node -e` to print the result of `2 ** 10`.
   <details><summary>Hint</summary>`node -e "console.log(2 ** 10)"`</details>
7. Write a file `greet.js` that prints today's date using `new Date()`, then run it.
8. Use `npm` to check how many packages are installed globally.
   <details><summary>Hint</summary>`npm list -g --depth=0`</details>

---

## 🌟 Side Quest — Customize Your Shell Prompt (+50 XP)

A good prompt shows you useful info at a glance. Make yours show a friendly message.

```bash
# Temporarily change your prompt for this session
PS1="🚀 \u@\h:\w$ "
```

- `\u` = username, `\h` = hostname, `\w` = current folder.
- Try a few variations. When you find one you like, you *could* add it to `~/.bashrc` (the file Bash reads on startup) — but only if you're comfortable; we cover `.bashrc` properly in World 2.

🎯 **Side quest complete when:** your prompt visibly changes and you can explain what `\u`, `\h`, and `\w` show. Add **+50 XP**.

---

## 🌟 Side Quest — Make an Alias (+50 XP)

Typing `ls -la` constantly is tedious. Create a shortcut:

```bash
alias ll='ls -la'
ll
```

🎯 **Complete when:** typing `ll` runs `ls -la`. Bonus: explain why this alias disappears when you close the terminal (hint: it's not saved to `~/.bashrc` yet).

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
