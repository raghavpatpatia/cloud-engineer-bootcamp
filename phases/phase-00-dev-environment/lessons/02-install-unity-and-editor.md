# Level 2 — Install Unity & Your Editor

| | |
|---|---|
| 🎚️ **Difficulty** | 🟢 Easy |
| ⏱️ **Estimated time** | 30 minutes |
| ⭐ **XP reward** | 100 (Quest) + 25 (Quiz) |

[← Prev](01-meet-the-studio-and-the-loop.md) · [↑ Phase Home](../README.md) · [→ Next](03-version-control-with-git.md)

---

## 📖 Story

> *"Ticket from IT: your box is bare. Get Unity Hub, a Unity LTS version, and a real C# editor on it. Then make me an empty Ashfall project and open it — I just want to see green, nothing fancy. When the Editor opens and you can find the Console window, you've passed onboarding. — IT Support (cc: Kenji)"*

Kenji adds: *"Unity is a tool sitting on top of the runtime you learned about last lesson. The Editor just lets you see and arrange the game world while that loop runs. Install it, poke around, don't be afraid — you can't break anything that a re-open won't fix."*

---

## 🎯 Goal

- Install **Unity Hub** (the launcher/version manager) and a **Unity LTS** version (Personal — free)
- Install a free C# editor: **VS Code** (with the C# extension) or **Rider** (free for non-commercial use)
- Create the empty **Ashfall** 2D project on disk in `~/projects`
- Tour the Editor: Scene, Game, Hierarchy, Inspector, Project, Console — and connect them to the game loop

---

## 🧠 Concepts

You don't install "Unity." You install **Unity Hub** — a small launcher that manages which *versions* of the Unity Editor you have and which projects use which version. This matters: a team must all use the **same** editor version or projects subtly break. We pick an **LTS** (Long-Term Support) version because it's stable and patched for ~2 years — exactly what a real codebase that lives for years needs.

```mermaid
flowchart TD
    Hub["🧰 Unity Hub<br/>(launcher / version manager)"] --> V["Unity Editor LTS<br/>(e.g. 2022.3.x / 6000.x)"]
    Hub --> Projects["Your projects list"]
    V --> Editor["The Editor app<br/>(Scene/Game/Inspector/...)"]
    Editor --> Runtime["▶️ Play Mode<br/>= runs the game loop"]
    Editor -.writes/reads.-> Disk["📁 ~/projects/ashfall<br/>(Assets, ProjectSettings, ...)"]
    Code["⌨️ VS Code / Rider"] -.edits .cs.-> Disk
    style Hub fill:#ede9fe,stroke:#6d28d9
    style Runtime fill:#dcfce7,stroke:#166534
```

The **Editor** is a tool *over* a runtime. When you press **Play**, Unity starts running the exact game loop from Level 1 (its `Update()` is called every frame). When you stop, you're back to arranging the world. Your **C# editor** (VS Code/Rider) is separate — it edits the `.cs` script files that Unity compiles. Two tools, one project folder on disk.

The six windows you'll live in:

| Window | What it is | Loop connection |
|--------|-----------|-----------------|
| **Scene** | The world you edit, freely moveable camera | Where you arrange state before/while it runs |
| **Game** | What the player sees through the game camera | The **Render** output of the loop |
| **Hierarchy** | List of every object in the current scene | The objects the **Update** phase touches |
| **Inspector** | Properties of the selected object | The data your scripts read/write |
| **Project** | All files on disk (assets, scripts, scenes) | Your actual `Assets/` folder |
| **Console** | Logs, warnings, errors | Where `Debug.Log` and crashes show up (Level 4) |

### Why this exists

Early game devs hand-wrote engines: their own loop, their own renderer, their own asset loader — months of work before a single sprite moved. An engine like Unity gives you that loop, a renderer, a physics system, and an *editor to see it all* for free, so you spend your time on the *game*, not the plumbing. The Hub-and-versions split exists because real projects outlive any single editor release — you need reproducible, pinned tooling, the same reason backend teams pin their language version. This is engine-agnostic thinking: Unreal has the Epic Launcher + Unreal Editor, Godot has its own; the *shape* (version manager → editor → project on disk → external code editor) is universal.

---

## 🛠️ Hands-on Lab

> 💻 Exact buttons shift between OS and versions; follow the spirit. All links live in [RESOURCES.md](../../../RESOURCES.md) for this world — grab the official Unity and editor downloads there.

### Step 1 — Install Unity Hub

Download **Unity Hub** from the official Unity site (RESOURCES.md) and install it. Launch it and sign in with a free **Unity account** — choose the **Unity Personal** license when asked (free; for individuals/small revenue).

### Step 2 — Install a Unity LTS Editor through the Hub

In Unity Hub → **Installs** → **Install Editor** → pick the recommended **LTS** release. In the modules step, make sure these are checked:

- **Build Support** for your platform (e.g. *Windows Build Support* / *Mac Build Support*) — you'll need it for the Boss Battle build.
- A code editor integration if offered (you can also install the editor separately below).

Let it download (it's large — go stretch). When done, the Hub shows your installed version under **Installs**.

### Step 3 — Install a free C# editor

Pick one:

**VS Code (lightweight, free):**
```bash
# After installing VS Code from RESOURCES.md, install the C# extension:
code --install-extension ms-dotnettools.csharp
```
Then in Unity later: **Edit → Preferences → External Tools → External Script Editor → Visual Studio Code**.

**Rider (full IDE, free for non-commercial):** install from JetBrains (RESOURCES.md), then set it the same way under **External Tools**.

> 💡 Either is fine. VS Code is lighter; Rider has deeper C#/Unity tooling. You can switch later.

### Step 4 — Create the Ashfall project

In Unity Hub → **Projects** → **New project**:

1. **Editor version:** your installed LTS.
2. **Template:** **2D** (Ashfall is 2D top-down — pick the 2D / 2D Core template, *not* 3D or URP yet; we add URP in World 7).
3. **Project name:** `ashfall`
4. **Location:** `~/projects` (so the full path is `~/projects/ashfall`).
5. Click **Create project**. Unity generates the folders and opens the Editor.

Verify on disk:

```bash
ls ~/projects/ashfall
# Assets  Packages  ProjectSettings   (and Library/, Logs/, etc. once opened)
```

> 📁 `Assets/` is *your* stuff. `Library/`, `Temp/`, `obj/` are generated caches — remember that, it matters a lot next lesson (Git).

### Step 5 — Tour the Editor

With Ashfall open:

1. Find each window: **Scene**, **Game**, **Hierarchy**, **Inspector**, **Project**, **Console**. (Use **Window** menu if any is hidden; **Console** is under **Window → General → Console**.)
2. In **Hierarchy**, click the **Main Camera** — watch the **Inspector** fill with its properties. That's the camera whose view becomes the **Game** window.
3. Press the **▶️ Play** button at the top. The Game view goes live — *the loop is now running*. You'll see a flat color (an empty world is still a running game). Press **▶️** again to stop.

> ⚠️ Anything you change in **Play Mode** is reverted when you stop. That's a feature (safe experimentation), and a classic "where did my changes go?!" trap.

### Step 6 — Save the scene

**File → Save** (or `Ctrl/Cmd+S`). Unity saves the scene asset (e.g. `Assets/Scenes/SampleScene.unity`). You now have a real, openable, runnable project.

---

## 🎮 Mini Challenge

Without writing any code, make the Game view a different color when you press Play. (Hint: it's a property on the camera.)

<details>
<summary>💡 Reveal answer</summary>

1. In **Hierarchy**, select **Main Camera**.
2. In the **Inspector**, find the **Camera** component → **Background** color swatch.
3. Click it, pick a new color, close the picker.
4. Press **▶️ Play** — the Game view now clears to your color each frame.

That "clear to a color" happens in the **Render** phase of every frame — you just configured the first step of the renderer.
</details>

---

## 📦 Project Mission

Stand up the real Ashfall project and prove it runs.

1. Confirm `~/projects/ashfall` exists with `Assets/`, `Packages/`, `ProjectSettings/`.
2. Open it in Unity, create a `Scenes` folder under `Assets` if the template didn't, and **save the scene**.
3. Press **Play**, confirm the Game view goes live with no errors in the **Console**, then stop.
4. Set your external script editor (VS Code or Rider) in **Edit → Preferences → External Tools**.

🎯 **Mission complete when:** Ashfall opens in your LTS Editor, Play Mode runs with a clean Console, the scene is saved, and your C# editor is wired up — an empty but *real* game project lives at `~/projects/ashfall`.

---

## ⚠️ Common Mistakes

| Mistake | What happens | Fix |
|--------|--------------|-----|
| Installing "Unity" without the Hub | Can't manage versions; team mismatch later | Always install via Unity Hub and pin an LTS version |
| Picking the 3D (or URP) template | Wrong defaults for a 2D game | Recreate with the **2D / 2D Core** template |
| Editing in Play Mode and pressing Stop | All your changes vanish | Make edits with Play Mode **off**; Play is for testing |
| Committing/zipping the `Library/` folder | Huge, machine-specific, regenerates anyway | Leave it out (next lesson's `.gitignore` handles this) |
| No C# extension in VS Code | No autocomplete, red squiggles everywhere | `code --install-extension ms-dotnettools.csharp` |
| Different editor version per teammate | Project upgrades/corrupts on open | Everyone uses the same LTS version from the Hub |

---

## 🤔 Reflection Questions

1. What's the difference between Unity **Hub**, the Unity **Editor**, and your **C# editor** — and why are they three separate things?
2. Which Editor window shows the **Render** output of the game loop, and which lists the objects the **Update** phase acts on?
3. Why does pressing **Play** and changing things, then **Stop**, throw your changes away — and why is that actually good?

---

## 📝 Quiz

1. **Unity Hub's main job is to…**
   - a) write your game code
   - b) manage Unity Editor versions and your projects
   - c) render the final game
2. **You should create Ashfall with which template?**
   - a) 3D
   - b) 2D (2D Core)
   - c) High Definition RP
3. **Pressing ▶️ Play does what, in game-loop terms?**
   - a) saves the project
   - b) starts running the input → update → render loop live
   - c) builds an executable

<details>
<summary>✅ Answers</summary>

1: **b** · 2: **b** · 3: **b**
</details>

---

## ✅ Completion Checklist

- [ ] Unity Hub installed and signed in (Unity Personal)
- [ ] A Unity **LTS** Editor installed via the Hub (with Build Support)
- [ ] VS Code (+ C# extension) or Rider installed and set as External Script Editor
- [ ] `~/projects/ashfall` created from the **2D** template
- [ ] Play Mode runs with a clean Console; scene saved
- [ ] I completed the Mini Challenge (camera background color)
- [ ] I passed the quiz
- [ ] Added **+125 XP** to [PROGRESS.md](../../../PROGRESS.md)

---

[← Prev](01-meet-the-studio-and-the-loop.md) · [↑ Phase Home](../README.md) · [→ Next](03-version-control-with-git.md)
