# 👹 Boss Battle — The 2 AM Deploy

| | |
|---|---|
| 🎚️ **Difficulty** | 🟡 Medium |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 8 — Terraform |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Priya <priya@cloudforge.inc>
To:      You
Subject: [SEV-2 / POSTMORTEM] TaskFlow went down at 2 AM — fix the pipeline

At 02:14 someone pushed a hotfix. The tests were FAILING, but it deployed
to prod anyway and took TaskFlow down for 40 minutes. While digging in, I
found three things wrong with the pipeline a teammate "improved":

  1. The deploy runs even when tests fail — there's no gate.
  2. The EC2 host and SSH key are HARD-CODED in the workflow file. 😱
  3. It deploys on every branch, not just main.

I've attached the broken ci.yml below. Make this pipeline SAFE. A failing
test must make it IMPOSSIBLE to deploy. Secrets must be secrets. And only
main ships. No tutorials — you've built every piece of this already.

— Priya
```

> ⚔️ **Boss Battle rules:** No step-by-step tutorials. Use your four lessons, the GitHub Actions docs, and everything you built. You win when every victory condition is met **and you can explain why each fix prevents the 2 AM outage.**

---

## 🧨 The broken workflow

Here is the `.github/workflows/ci.yml` that shipped the outage. It has at least **four** problems. Fix it.

```yaml
name: CI

on:
  push:

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      # ⚠️ tests run but their result is thrown away
      - run: npm test || true
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: my-github-user
          password: ghp_HARDCODEDtoken1234567890   # ⚠️ secret in plain text
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/my-github-user/taskflow:latest

  deploy:
    runs-on: ubuntu-latest
    # ⚠️ no 'needs', so this runs in parallel with build — even if build fails
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: 13.50.1.2                          # ⚠️ hard-coded host
          username: ubuntu
          key: |                                    # ⚠️ private key in the repo!
            -----BEGIN OPENSSH PRIVATE KEY-----
            b3BlbnNzaC1rZXktdjEAAAAA... (a real key, committed forever)
            -----END OPENSSH PRIVATE KEY-----
          script: |
            cd ~/projects/taskflow
            docker compose pull && docker compose up -d
```

---

## 🎯 Your mission

Rewrite `ci.yml` so the pipeline is **safe**. Specifically:

- **Tests gate everything.** A failing `npm test` must stop the pipeline — no build, no deploy. (Kill the `|| true`.)
- **Deploy depends on a green build.** The deploy job must not start unless tests *and* build succeeded.
- **Secrets are secrets.** The SSH key, host, and user move to encrypted **GitHub Secrets**. Use `GITHUB_TOKEN` for GHCR — store no registry password.
- **Only `main` ships.** Pushes to other branches may test/build but must **never** deploy.
- **Traceable images.** Tag the pushed image with the short commit **SHA** (keep `latest` too).

Apply the fix to your real TaskFlow repo and prove it works.

---

## 🏆 Victory conditions

- [ ] `npm test` runs **without** `|| true` — a failing test turns the build red and **stops** it
- [ ] The `deploy` job has `needs:` so it can't run unless the build succeeded
- [ ] No SSH key, host, user, or token is hard-coded — all are `${{ secrets.* }}`
- [ ] GHCR login uses `secrets.GITHUB_TOKEN` with `permissions: packages: write`
- [ ] The deploy job has `if: github.ref == 'refs/heads/main'`
- [ ] The image is tagged with the short **SHA** (and `latest`)
- [ ] **Proof:** a push with a failing test does **not** deploy; a green push to `main` does
- [ ] You can explain out loud *why* each fix prevents the 2 AM outage

---

## 🧪 How you'll know you won

Run two experiments on your real repo:

1. **Break a test, push to `main`.** The `test` job goes red, and `build-and-push` + `deploy` are **skipped**. Production is untouched. ✅
2. **Fix the test, push to `main`.** All three jobs go green and the live EC2 URL serves the new SHA-tagged image. ✅

If a red test can't reach production and a green push to `main` ships automatically — you've beaten the boss.

<details>
<summary>🔎 Reference solution — only after you've tried!</summary>

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    name: Run tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test            # ✅ no '|| true' — a failure stops the pipeline

  build-and-push:
    name: Build & push image
    runs-on: ubuntu-latest
    needs: test                  # ✅ only on green tests
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write            # ✅ lets GITHUB_TOKEN push
    steps:
      - uses: actions/checkout@v4
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}   # ✅ no stored password
      - name: Prepare image name
        id: img
        run: |
          OWNER=$(echo "${{ github.repository_owner }}" | tr '[:upper:]' '[:lower:]')
          echo "name=ghcr.io/${OWNER}/taskflow" >> "$GITHUB_OUTPUT"
          echo "sha=${GITHUB_SHA:0:7}" >> "$GITHUB_OUTPUT"
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ${{ steps.img.outputs.name }}:${{ steps.img.outputs.sha }}
            ${{ steps.img.outputs.name }}:latest

  deploy:
    name: Deploy to EC2
    runs-on: ubuntu-latest
    needs: build-and-push                     # ✅ gated on green build
    if: github.ref == 'refs/heads/main'       # ✅ only main ships
    steps:
      - name: Compute short SHA
        id: vars
        run: echo "sha=${GITHUB_SHA:0:7}" >> "$GITHUB_OUTPUT"
      - name: SSH in and roll out the new image
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.EC2_HOST }}        # ✅ secrets, not literals
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/projects/taskflow
            export TAG=${{ steps.vars.outputs.sha }}
            docker compose pull
            docker compose up -d
            docker image prune -f
```

**Why each fix stops the 2 AM outage:**
- **Removing `|| true`** lets the non-zero exit code from a failing test fail the `test` job. `npm test || true` always exits 0, which is exactly why broken code shipped.
- **`needs: test` / `needs: build-and-push`** chain the jobs so a red upstream job *skips* everything downstream — a failing test makes deploy impossible.
- **Moving the key/host/user to secrets** removes the private key from git history (a committed key is compromised forever and must be rotated). GitHub masks secrets in logs.
- **`if: github.ref == 'refs/heads/main'`** ensures only the official branch deploys; the 2 AM hotfix on a random branch couldn't have reached prod.
- **SHA tagging** makes every deploy traceable and gives you a precise earlier tag to roll back to.

> ⚠️ If a real key was ever committed (like in the broken file), treat it as compromised: delete it from the EC2 instance's `authorized_keys`, generate a new key pair, and store the new private key as `EC2_SSH_KEY`.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🤖 Achievement unlocked: **Robot Overlord** — you taught a machine to ship your code safely
- 🔓 **World 8 — Terraform** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 7 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: the dangerous part of a deploy was never the typing — it was a tired human skipping a check. You just made skipping checks impossible. That's the real win of CI/CD.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [🏗️ Enter World 8 →](../phase-08-terraform/README.md)
