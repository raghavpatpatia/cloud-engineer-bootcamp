# 👹 Boss Battle — Refactor the Spaghetti

| | |
|---|---|
| 🎚️ **Difficulty** | 🔴 Hard |
| ⏱️ **Estimated time** | 60 minutes |
| ⭐ **XP reward** | 500 |
| 🔓 **Unlocks** | World 2 — Mathematics for Games |

[← Checklist](checklist.md) · [↑ Phase Home](README.md)

---

## 📨 The incident

```
From:    Kenji <kenji@pixelforge.studio>
To:      You <new-hire@pixelforge.studio>
Cc:      Theo <theo@pixelforge.studio>
Subject: [W1-BOSS] The god-class is back. Kill it — without breaking it.

Remember the 3000-line prototype I told you we deleted? I found a
descendant of it in an old branch: GameThing.cs. It "works" — it moves,
takes damage, plays a hurt sound, updates a score, and on death triggers
game over. It is also a single class that does ALL of that, with public
fields, hard-coded references, and zero seams. Touch one line and pray.

Your job is the exact thing this world trained you for: refactor it into
the clean architecture you've been building — components, interfaces,
an event bus, a GameManager + state machine — with ZERO behavior change.
Same inputs, same outputs. Just code we can live with.

No tutorials. No hand-holding. You have all five lessons. Theo wants to
see GameThing.cs gone and the behavior intact. Beat this and World 2 — the
movement math — is yours.

— Kenji
```

> ⚔️ **Boss Battle rules:** No tutorials, no copying lesson files wholesale. **Apply** World 1: decompose the god-class yourself, reason about each responsibility, and prove behavior is unchanged. You win when every victory condition is met **and you can explain which SOLID principle each split honors.**

---

## 🍝 The spaghetti

Drop this into Ashfall, confirm it runs, then **refactor it**. (It compiles and "works" — that's the trap.)

```csharp
using UnityEngine;

// ❌ The god-class: one class doing movement, health, audio, score, UI, and game flow.
public class GameThing : MonoBehaviour
{
    public float speed = 5f;
    public int hp = 100;
    public int maxHp = 100;
    public int score = 0;
    public AudioSource hurtSound;   // hard-wired dependency
    public GameThing other;         // enemies are... the same class?

    void Update()
    {
        // movement
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        transform.position += new Vector3(h, v, 0) * speed * Time.deltaTime;

        // "attack" the other thing on Space
        if (Input.GetKeyDown(KeyCode.Space) && other != null)
        {
            other.hp -= 25;
            Debug.Log("[UI] Enemy HP: " + other.hp);   // UI logic inline
            if (other.hp <= 0)
            {
                score += 10;
                Debug.Log("[UI] Score: " + score);      // more UI logic
                Debug.Log("Enemy died");
                Destroy(other.gameObject);
            }
        }

        // take damage on T (simulate a hit)
        if (Input.GetKeyDown(KeyCode.T))
        {
            hp -= 25;
            if (hurtSound != null) hurtSound.Play();    // audio inline
            Debug.Log("[UI] Player HP: " + hp);         // UI inline
            if (hp <= 0)
            {
                Debug.Log("GAME OVER");                  // game-flow inline
                Time.timeScale = 0f;
            }
        }
    }
}
```

Count the responsibilities crammed into one class: **movement, health, attacking, audio, score, UI, and game-over flow** — at least seven reasons to change. That's textbook SRP violation, and it's why nobody can safely modify it.

---

## 🎯 Your mission

Refactor `GameThing` into the clean, component-based architecture from this world — **with identical behavior**. The player still moves with WASD/arrows, Space still damages the enemy (and kills + scores at 0 HP), T still damages the player (with sound + game-over at 0 HP). Only the *structure* changes.

Decompose it into (at minimum):

1. **Components (composition — L2):** a `Mover` (movement), and a `Health` component reused by *both* player and enemy. No god-class.
2. **Interfaces (L3):** `Health` implements `IDamageable`; the attack logic depends on `IDamageable`, not on a concrete type. Each class has **one responsibility** (SRP).
3. **Events (L4):** `Health` raises through `GameEvents` (`PlayerDamaged`, `EnemyKilled`, `PlayerDied`) instead of calling UI/audio/score directly. A `ScoreSystem`, a UI logger, and an `AudioReaction` *subscribe* — and unsubscribe in `OnDisable`.
4. **Manager + FSM (L5):** a `GameManager` listens for `PlayerDied` and transitions to `GameOver` (setting `timeScale = 0`) — the game-over logic lives there, not in `Update`.
5. **Delete `GameThing.cs`.** It must be gone.

---

## 🏆 Victory conditions

- [ ] `GameThing.cs` is **deleted** — no single class does movement + health + audio + score + UI + flow
- [ ] Movement lives in a `Mover` component; both player and enemy reuse the same `Health` component
- [ ] `Health` implements `IDamageable`, and attack logic depends on the **interface**, not a concrete type
- [ ] Damage, score, audio, and UI updates happen via **subscribers to `GameEvents`** (no direct cross-system calls)
- [ ] Every subscriber unsubscribes in `OnDisable` (no double-fire after a scene reload)
- [ ] A `GameManager` + state machine owns game-over (driven by a `PlayerDied` event, not inline)
- [ ] **Behavior is identical** to the original: same controls, same outcomes, same logs
- [ ] You can explain which SOLID principle each split honors

---

## 🧪 How you'll know you won

```bash
cd ~/projects/ashfall

# The god-class is gone:
git ls-files | grep -i "GameThing"      # → prints NOTHING

# The clean pieces exist:
ls Assets/Scripts/Core Assets/Scripts/Entities Assets/Scripts/Interfaces Assets/Scripts/Systems
# → Mover.cs, Health.cs, IDamageable.cs, GameEvents.cs, GameManager.cs, ScoreSystem.cs, ...
```

Then in the Editor, play and run the *exact same* inputs as before:
- WASD/arrows move the player the same way.
- Space damages the enemy; at 0 HP it dies, the score goes up by 10, and it's destroyed.
- T damages the player with the hurt sound; at 0 HP the game-over fires and `timeScale` is 0.

Same behavior, brand-new architecture. Reload the scene and confirm logs fire **once** per event, not twice. If all that holds, you've won.

<details>
<summary>🔎 Reference solution — only after you've tried! (decomposition + key code)</summary>

**The decomposition (and the SOLID it honors):**

| New piece | Responsibility | Principle |
|---|---|---|
| `Mover` | movement only | SRP |
| `Health : IDamageable` | HP only; raises events | SRP, DIP (others depend on the interface) |
| `Attacker` | applies damage to any `IDamageable` | DIP, Open/Closed (new damageable types need no change) |
| `GameEvents` | the pub/sub hub | decoupling (observer) |
| `ScoreSystem` / `UiLogger` / `AudioReaction` | each reacts to one event | SRP, Open/Closed (add a reactor without editing publishers) |
| `GameManager` + FSM | owns game-over flow | SRP, single coordinator |

**Health raises instead of calling out:**

```csharp
using UnityEngine;

public class Health : MonoBehaviour, IDamageable
{
    [SerializeField] private int max = 100;
    [SerializeField] private bool isPlayer;
    public int Current { get; private set; }
    void Awake() => Current = max;

    public void TakeDamage(int amount)
    {
        Current = Mathf.Max(0, Current - amount);
        if (isPlayer) GameEvents.RaisePlayerDamaged(amount);
        if (Current == 0)
        {
            if (isPlayer) GameEvents.RaisePlayerDied();
            else { GameEvents.RaiseEnemyKilled(); Destroy(gameObject); }
        }
    }
    public bool IsDead => Current <= 0;
}
```

**Attack depends on the abstraction:**

```csharp
public class Attacker : MonoBehaviour
{
    [SerializeField] private int damage = 25;
    public void Strike(IDamageable target) => target.TakeDamage(damage);
}
```

**Subscribers each do one thing:**

```csharp
public class ScoreSystem : MonoBehaviour
{
    private int score;
    void OnEnable()  => GameEvents.EnemyKilled += OnKill;
    void OnDisable() => GameEvents.EnemyKilled -= OnKill;
    private void OnKill() { score += 10; Debug.Log($"[UI] Score: {score}"); }
}
```

**GameManager owns game-over via the event:**

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    public GameState State { get; private set; } = GameState.Playing;

    void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this; DontDestroyOnLoad(gameObject);
    }
    void OnEnable()  => GameEvents.PlayerDied += OnPlayerDied;
    void OnDisable() => GameEvents.PlayerDied -= OnPlayerDied;

    private void OnPlayerDied()
    {
        State = GameState.GameOver;
        Time.timeScale = 0f;
        Debug.Log("GAME OVER");
    }
}
```

The input/movement that was in `GameThing.Update` splits into `Mover` (reads input, moves) and an `Attacker` trigger on Space — but every *cross-system* effect (UI, audio, score, game-over) now flows through `GameEvents`. The behavior is byte-for-byte the same; the structure is night and day. That's the entire point of World 1.
</details>

---

## 🎁 Rewards

- 🏆 **+500 XP**
- 🏅 Achievement unlocked: **🧠 Architect** — you can turn spaghetti into a system that survives years of change
- 🔓 **World 2 — Mathematics for Games** unlocks
- 📈 Update [PROGRESS.md](../../PROGRESS.md): mark World 1 ✅ and add the **+250 World Complete bonus**

> 🗒️ Reflection: you just did the highest-value thing a senior engineer does — make code *easier to change* without changing what it does. Every world after this adds features *onto* this architecture instead of fighting it. Ashfall now has a backbone. Next, Maya wants the player to actually *move and aim* — and that's all math.

---

[← Checklist](checklist.md) · [↑ Phase Home](README.md) · [📐 Enter World 2 →](../phase-02-math-for-games/README.md)
