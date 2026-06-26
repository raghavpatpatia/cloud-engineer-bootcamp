# ✅ World 3 — Readiness Checklist

Before you face the Boss Battle and unlock World 4, make sure all of this is true. If any box is empty, revisit that lesson — the boss battle assumes you can do every one of these.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Repo set up
- [ ] `git --version` works and my `user.name` / `user.email` are configured
- [ ] `~/projects/taskflow` is a Git repo (`git status` runs without error)
- [ ] I have a `.gitignore` that excludes `node_modules/` and `*.tar.gz`
- [ ] `git log --oneline` shows a real commit history
- [ ] The repo is pushed to **GitHub** and `git remote -v` shows `origin`

## 🧠 Skills I can do without looking up
- [ ] Stage and commit changes (`git add`, `git commit -m`)
- [ ] Check status and history (`git status`, `git log --oneline`)
- [ ] Create, switch, and delete branches (`git switch -c`, `git branch -d`)
- [ ] Merge a branch into `main` (`git merge`)
- [ ] Push and pull (`git push`, `git pull`)
- [ ] Open and merge a Pull Request on GitHub
- [ ] Recover a deleted file (`git restore`) — the Time Traveler skill

## 🔎 Self-test (do this from memory)
In a throwaway repo (`mkdir ~/gittest && cd ~/gittest && git init`), without notes, run a sequence that:
1. Commits a file `app.txt` containing the word `main`
2. Creates and switches to a branch `feature`
3. Changes `app.txt` on the branch and commits
4. Merges `feature` into `main`
5. Deletes the `feature` branch
6. Prints the commit history

<details>
<summary>✅ One correct solution</summary>

```bash
cd ~/gittest
echo "main" > app.txt
git add app.txt && git commit -m "Add app.txt"

git switch -c feature
echo "feature work" >> app.txt
git add app.txt && git commit -m "Add feature work"

git switch main
git merge feature
git branch -d feature

git log --oneline
```
</details>

If you did that without peeking — you're ready.

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I completed the 🌿 **Time Traveler** Side Quest (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The Merge Conflict from Hell](boss-battle.md)

[← World Home](README.md)
