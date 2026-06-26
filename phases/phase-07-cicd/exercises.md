# 🏋️ World 7 — Exercises

Extra reps to make pipelines second nature. None are required to advance, but each makes you faster and safer. The Side Quest awards **+50 XP**.

[← World Home](README.md) · [✅ Checklist](checklist.md) · [👹 Boss Battle](boss-battle.md)

---

## Warm-ups (workflow fluency)

Do these in your `~/projects/taskflow` repo and watch the **Actions** tab.

1. Add a step that prints the runner's OS and the workflow's name.
   <details><summary>Hint</summary>`run: echo "${{ runner.os }} — ${{ github.workflow }}"`</details>
2. Make a workflow run **only** on pushes to `main` (not other branches).
   <details><summary>Hint</summary>`on: { push: { branches: [ main ] } }`</details>
3. Add a step that runs **only when a previous step failed**.
   <details><summary>Hint</summary>Add `if: failure()` to the step.</details>
4. Add a manual "run it now" button to a workflow.
   <details><summary>Hint</summary>Add `workflow_dispatch:` under `on:`, then use the **Run workflow** button in the Actions tab.</details>
5. Cancel an in-progress run automatically when you push again to the same branch.
   <details><summary>Hint</summary>Add a `concurrency:` block with `cancel-in-progress: true`.</details>

## Pipeline warm-ups

6. Run the test job against a **matrix** of Node 18 and 20 (from Level 2's challenge) and confirm two parallel runs.
7. Add a step that fails the build if `npm audit` finds a high-severity vulnerability.
   <details><summary>Hint</summary>`run: npm audit --audit-level=high`</details>
8. Tag the pushed image with the **branch name** in addition to the SHA.
   <details><summary>Hint</summary>Add `${{ steps.img.outputs.name }}:${{ github.ref_name }}` to the `tags:` list.</details>

---

## 🌟 Side Quest — Add a Manual Approval Gate (+50 XP)

Real teams don't let *every* green build hit production unattended. A human glances at it first. GitHub gives you this for free with **environment protection rules** — a required reviewer must click **Approve** before the `deploy` job runs.

**1. Create a protected environment.** Repo → **Settings → Environments → New environment** → name it `production`. Under it, enable **Required reviewers** and add yourself.

**2. Attach the environment to the deploy job** in `.github/workflows/ci.yml`:

```yaml
  deploy:
    name: Deploy to EC2
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    environment:
      name: production            # 👈 now requires approval before running
      url: http://${{ secrets.EC2_HOST }}
    steps:
      - name: Compute short SHA
        id: vars
        run: echo "sha=${GITHUB_SHA:0:7}" >> "$GITHUB_OUTPUT"
      - name: SSH in and roll out the new image
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/projects/taskflow
            export TAG=${{ steps.vars.outputs.sha }}
            docker compose pull
            docker compose up -d
            docker image prune -f
```

**3. Push to `main`.** The pipeline runs test → build, then **pauses** on `deploy` with a "Waiting for review" banner. Click **Review deployments → Approve and deploy**. Only then does it SSH in and ship.

🎯 **Side quest complete when:** a push to `main` pauses before deploy, you approve it, and the deploy then completes. Add **+50 XP**.

> 💡 Why this matters: it's the simplest form of a **release gate**. The build is always ready; *shipping* becomes a deliberate one-click decision — and the approval is logged with who clicked it.

---

[← World Home](README.md) · [✅ Checklist →](checklist.md)
