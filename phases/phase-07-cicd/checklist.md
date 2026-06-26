# ✅ World 7 — Readiness Checklist

Before you face the Boss Battle and unlock World 8, make sure all of this is true. If a box is empty, revisit that lesson — don't ship a pipeline you don't trust.

[← World Home](README.md) · [🏋️ Exercises](exercises.md) · [👹 Boss Battle](boss-battle.md)

---

## 🧰 Pipeline built
- [ ] My TaskFlow repo is **public** and has `.github/workflows/ci.yml`
- [ ] CI runs automatically on every push (green checks in the Actions tab)
- [ ] A `test` job runs `npm ci` + `npm test`; a failing test turns the build **red**
- [ ] A `build-and-push` job (with `needs: test`) pushes a SHA-tagged image to **GHCR**
- [ ] The GHCR package is **public** and I can `docker pull` it
- [ ] A `deploy` job (with `needs: build-and-push` and a `main` guard) SSHes into EC2
- [ ] A push to `main` deploys the new image with **no manual SSH**

## 🔐 Secrets done right
- [ ] `EC2_SSH_KEY`, `EC2_HOST`, `EC2_USER` are stored as **encrypted repository secrets**
- [ ] No keys, tokens, or passwords are hard-coded in the YAML
- [ ] I use the built-in `GITHUB_TOKEN` to log in to GHCR (no stored registry password)

## 🧠 Skills I can do without looking up
- [ ] Explain the difference between a workflow, a job, a step, and an action
- [ ] Explain why a non-zero exit code fails the build
- [ ] Explain how `needs:` and `if:` gate jobs
- [ ] Explain why an SSH key must be a secret, not a workflow value

## 🔎 Self-test (do this from memory)
Without notes, sketch (on paper or in a scratch file) a `ci.yml` outline that:
1. Triggers on push
2. Has a `test` job that checks out, sets up Node, runs `npm ci` and `npm test`
3. Has a `build-and-push` job that `needs` test
4. Has a `deploy` job that `needs` build and only runs on `main`

<details>
<summary>✅ One correct outline</summary>

```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm test
  build-and-push:
    runs-on: ubuntu-latest
    needs: test
    permissions: { contents: read, packages: write }
    steps: [ "...login to GHCR, build, push SHA tag..." ]
  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    steps: [ "...SSH in, docker compose pull && up -d..." ]
```
</details>

If you could outline that from memory — you're ready.

---

## 🎓 XP check
- [ ] I recorded XP for all 4 lessons in [PROGRESS.md](../../PROGRESS.md) (500 XP)
- [ ] (Optional) I did the **Manual Approval Gate** side quest (+50 XP)

---

> All checked? → [👹 Face the Boss Battle: The 2 AM Deploy](boss-battle.md)

[← World Home](README.md)
