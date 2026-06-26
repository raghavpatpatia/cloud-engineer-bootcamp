# 👹 Boss Battle — The Merge Conflict from Hell

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 4 — Backend Development |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Marcus <marcus@cloudforge.inc>
To:      You <new-hire@cloudforge.inc>
Subject: [INCIDENT] TaskFlow won't merge — CONFLICT everywhere

So this happened. Priya and I both edited the SAME lines of TaskFlow's
README on two different branches. Now when I try to merge, Git slams the
brakes:

    Auto-merging README.md
    CONFLICT (content): Merge conflict in README.md
    Automatic merge failed; fix conflicts and then commit the result.

The file is full of <<<<<<< and ======= and >>>>>>> garbage and the team
is blocked. No tutorial this time — you know enough now. Reproduce a
conflict yourself, resolve it CLEANLY, and explain what those markers
mean. Prove you're not afraid of conflicts.

— Marcus
```

> ⚔️ **Boss Battle rules:** No tutorials, no copy-paste-a-guide. Use your notes, the docs, and everything you built. You win when every victory condition is met **and you can explain why**.

---

## 🎯 Your mission

A **merge conflict** happens when two branches change the *same lines* of the same file, and Git can't decide which version wins — so it asks *you*. Your job is to deliberately cause one, then resolve it like a pro.

### Part A — Reproduce the conflict
In your `taskflow` repo, create the exact situation Marcus hit: two branches that edit the **same lines** of a file (e.g. `README.md`), then attempt to merge them so Git reports a `CONFLICT`.

### Part B — Resolve it cleanly
Open the conflicted file, understand the markers, and produce a **final, correct version** that keeps the right content from *both* sides (no leftover `<<<<<<<`, `=======`, or `>>>>>>>` markers). Commit the resolution.

### Part C — Explain it
Be able to say out loud — or jot in `~/projects/taskflow/CONFLICT_NOTES.md` — what each of these means:
- `<<<<<<< HEAD`
- `=======`
- `>>>>>>> <branch-name>`

…and *why* a conflict happened here but didn't in your earlier (fast-forward) merges.

---

## 🏆 Victory conditions

- [ ] You **caused** a real merge conflict (Git printed `CONFLICT (content): ...`)
- [ ] You **resolved** it: the file has no conflict markers and contains the intended content from both branches
- [ ] You **committed** the resolution (a merge commit) and `git status` is clean
- [ ] You can explain `<<<<<<<`, `=======`, `>>>>>>>` and why this merge conflicted while earlier ones didn't

---

## 🧪 How you'll know you won

After your resolution commit, run:

```bash
git status                       # clean, "nothing to commit"
grep -nE '^(<<<<<<<|=======|>>>>>>>)' README.md   # prints NOTHING (no markers left)
git log --oneline --graph        # shows the two branches converging at a merge commit
```

If `grep` finds no markers and the graph shows a merge, you've won Part A & B. Part C is in your head (or your notes).

<details>
<summary>🔎 Reference solution — only after you've tried! (Part A: reproduce)</summary>

Set up two branches that edit the **same line**:

```bash
cd ~/projects/taskflow
git switch main

# Make sure README.md has a known first line to fight over
# (skip if it already has a title line)
git switch -c branch-marcus
# Edit the title line — e.g. change it to:
#   # TaskFlow — Task Manager (by Marcus)
# then:
git commit -am "Marcus: reword README title"

git switch main
git switch -c branch-priya
# Edit the SAME title line differently — e.g.:
#   # TaskFlow — The Task Platform (by Priya)
git commit -am "Priya: reword README title"

# Now merge one into main, then try to merge the other → CONFLICT
git switch main
git merge branch-marcus        # clean (fast-forward or simple)
git merge branch-priya         # 💥 CONFLICT on the title line
```

Git stops and reports:
```
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```
</details>

<details>
<summary>🔎 Reference solution — Part B: resolve + Part C: explain</summary>

Open `README.md`. The conflicted region looks like this:

```
<<<<<<< HEAD
# TaskFlow — Task Manager (by Marcus)
=======
# TaskFlow — The Task Platform (by Priya)
>>>>>>> branch-priya
```

**What the markers mean:**
- `<<<<<<< HEAD` — start of *your current branch's* version (here, `main`, which already has Marcus's change).
- `=======` — the divider between the two versions.
- `>>>>>>> branch-priya` — end of the *incoming branch's* version.

**Resolve** by editing the region down to the single line you actually want — combining both intentions and **deleting all three markers**. For example:

```
# TaskFlow — The Task Manager Platform
```

Then stage and commit to finish the merge:

```bash
git add README.md
git commit                 # opens an editor with a prepared merge-commit message; save & close
# (or: git commit -m "Merge branch-priya: resolve README title conflict")

# Verify
grep -nE '^(<<<<<<<|=======|>>>>>>>)' README.md   # no output = all markers gone
git status                                         # clean
git log --oneline --graph                          # shows the merge commit

# Tidy up
git branch -d branch-marcus branch-priya
```

**Why this conflicted (Part C):** earlier merges were *fast-forwards* — only one branch had changed, so Git just slid the pointer forward; there was nothing to reconcile. Here, **both** `main` and `branch-priya` changed the **same line** after they diverged, so Git can't know which intent is correct. It marks the spot and hands the decision to a human — you.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🌿 If you completed the Time Traveler Side Quest, claim the **Time Traveler** achievement too
- 🔓 **World 4 — Backend Development** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 3 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: merge conflicts feel scary the first time and routine by the tenth. You just learned that Git never *loses* in a conflict — it *asks*. That's a feature.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [⚙️ Enter World 4 →](../phase-04-backend/README.md)
