# 🏋️ World 3 — Exercises

Extra reps to make Git muscle memory. None are required to advance, but each makes branching, history, and recovery feel automatic. The Side Quest awards **+50 XP** and the 🌿 **Time Traveler** achievement.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (Git fluency)

Do these inside a Git repo (use a throwaway one: `mkdir ~/gitpractice && cd ~/gitpractice && git init`).

1. Show the last 5 commits in compact form.
   <details><summary>Hint</summary>`git log --oneline -5`</details>
2. See exactly what you've changed but not yet staged.
   <details><summary>Hint</summary>`git diff`</details>
3. See what's staged and ready to commit.
   <details><summary>Hint</summary>`git diff --staged`</details>
4. Unstage a file you `git add`ed by mistake (keep the edits).
   <details><summary>Hint</summary>`git restore --staged <file>`</details>
5. Create a branch without switching to it, then list all branches.
   <details><summary>Hint</summary>`git branch experiment` then `git branch`</details>
6. Show who last changed each line of a file.
   <details><summary>Hint</summary>`git blame <file>`</details>
7. Rename your current branch to `develop`.
   <details><summary>Hint</summary>`git branch -m develop`</details>

## GitHub warm-ups

8. Check which remote(s) your repo is connected to.
   <details><summary>Hint</summary>`git remote -v`</details>
9. Fetch remote changes *without* merging them, then see what's new.
   <details><summary>Hint</summary>`git fetch` then `git log HEAD..origin/main --oneline`</details>
10. Practice branching visually at [learngitbranching.js.org](https://learngitbranching.js.org) — finish the "Introduction Sequence" (free, in-browser). See [RESOURCES.md → World 3](../../RESOURCES.md).

---

## 🌟 Side Quest — The Time Traveler (+50 XP) 🌿

**Recover a deleted file using Git.** This is the skill that turns "oh no, I deleted it" into "no problem, I'll just restore it" — and earns you the 🌿 **Time Traveler** achievement.

### Part 1 — Recover a file you deleted but hadn't committed the deletion

```bash
cd ~/projects/taskflow

# Make sure README.md is committed and clean first
git add README.md && git commit -m "Checkpoint before time travel" || true

# 💥 Disaster: delete a tracked file
rm README.md
ls                      # it's gone!

# ⏪ Rescue: restore it from the last commit
git restore README.md
ls                      # it's back!
cat README.md           # contents fully recovered
```

`git restore <file>` rewrites the working file from the latest committed version. Your last commit is a time machine.

### Part 2 — Recover from a commit you "lost" using the reflog

Sometimes you commit, then *reset* and think the work vanished. It usually didn't — Git's **reflog** records where `HEAD` has been.

```bash
# Make a commit we'll pretend to "lose"
echo "Precious feature notes" > notes.txt
git add notes.txt
git commit -m "Add precious notes"

# 💥 Disaster: move HEAD back, seemingly destroying that commit
git reset --hard HEAD~1
ls                      # notes.txt is gone, commit seems lost!

# ⏪ Rescue: the reflog remembers every move HEAD made
git reflog              # find the line for "Add precious notes" — copy its hash

# Restore that exact commit (replace <hash> with the one from reflog)
git reset --hard <hash>
ls                      # notes.txt is back
git log --oneline       # the commit is recovered
```

> 💡 The reflog is your safety net: even `git reset --hard` rarely loses committed work, because Git keeps a log of every position `HEAD` held for ~90 days.

🎯 **Side quest complete when:** you have (1) deleted then `git restore`d a file, and (2) "lost" then recovered a commit via `git reflog`. You can explain the difference between `git restore` (working-dir recovery) and `git reflog` + `git reset` (history recovery). Add **+50 XP** and unlock the 🌿 **Time Traveler** achievement in [PROGRESS.md](../../PROGRESS.md).

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
