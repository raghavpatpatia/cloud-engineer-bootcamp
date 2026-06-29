# 🏋️ World 8 — Exercises

Extra reps to make the *networking & multiplayer* skills automatic before the boss battle. None are required to advance, but each is exactly the kind of reasoning "Co-op in a Container" demands — reasoning about the wire, making the server the authority, syncing real gameplay, and packaging a server into a reproducible container. Each **Side Quest** awards **+50 XP**.

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist](checklist.md) · [🌐 Boss Battle](boss-battle.md)

---

## Warm-ups (the wire, authority, sync, containers)

1. In one sentence each, what do **TCP** and **UDP** guarantee, and why do fast-paced games usually pick UDP?
   <details><summary>Hint</summary><strong>TCP</strong> guarantees ordered, reliable delivery (it resends lost packets and waits) — great for files, bad for games because one lost packet stalls everything (head-of-line blocking). <strong>UDP</strong> is fire-and-forget: no ordering, no resend, no waiting — so a dropped packet doesn't hold up the next one. Games pick UDP because a *late* position update is useless; you'd rather get the *next* one immediately than wait for the old one. (Reliability you actually need, like "spawn this object," you layer back on top selectively.)</details>
2. What is **latency** (ping/RTT), and why does it force games to *predict* instead of just waiting for the server?
   <details><summary>Hint</summary>Latency is the time for a message to travel client→server→back (round-trip time). Even at a good 60 ms RTT, if the client waited for the server to confirm every step before moving, the character would feel like it's dragging through mud. So the client <strong>predicts</strong> the result of its own input locally (moves immediately) and later <strong>reconciles</strong> with the server's authoritative answer — instant feel, server still in charge.</details>
3. **Client-server** vs **peer-to-peer:** what's the core trade-off, and why does Ashfall go client-server?
   <details><summary>Hint</summary><strong>Peer-to-peer:</strong> no central server (cheap, simple), but no single source of truth — desyncs are common and any peer can cheat by lying about state. <strong>Client-server:</strong> one authoritative server every client trusts — costs a server to run, but you get consistency and a place to validate against cheating. Ashfall goes client-server because Theo refuses to ship something a cheater can break, and because a dedicated server is what you'll containerize and deploy.</details>
4. What does **"server-authoritative"** actually mean, and what does the client become if the server owns the truth?
   <details><summary>Hint</summary>The server holds the canonical game state and is the only thing allowed to *change* it; clients send <em>inputs</em> ("I pressed move-right"), not <em>results</em> ("I am now at x=5"). The client becomes a <strong>predictor + renderer</strong>: it guesses the outcome locally for responsiveness, displays it, and corrects when the server's authoritative state arrives. A cheating client can lie about its input but can't dictate the world.</details>
5. A remote player "teleports" / stutters across your screen. The packets are arriving fine. What technique smooths it, and why?
   <details><summary>Hint</summary><strong>Interpolation.</strong> Remote players' updates arrive every ~50–100 ms (discrete snapshots), so rendering them raw looks jumpy. You render the remote player slightly *in the past* and smoothly interpolate between the last two received snapshots — trading a tiny bit of latency on remote players (who you don't control anyway) for smooth motion. (Your *own* player uses prediction, not interpolation.)</details>
6. What's the difference between a **network variable** and an **RPC**, and when do you reach for each?
   <details><summary>Hint</summary>A <strong>network variable</strong> is *state* that's automatically replicated and kept in sync (e.g. a player's current health, position) — set it once on the owner/server and everyone sees the value. An <strong>RPC</strong> is an *event/call* sent across the wire (e.g. "play this attack," "open this chest") — a one-shot message, ServerRpc (client→server) or ClientRpc (server→clients). State that persists → network variable; a momentary action → RPC.</details>
7. Why must both players generate the dungeon from the **same seed**, and who should own that seed?
   <details><summary>Hint</summary>Ashfall's dungeon is *procedurally generated* (W4) — same seed in, same map out. If each client rolled its own seed they'd be in different dungeons. The <strong>server</strong> picks the seed (it's the authority) and sends it to clients, so everyone generates the identical layout, enemies, and loot placement. The seed is small to send; the *map* is reproduced, not transmitted.</details>
8. What is **ownership** in netcode, and why does it matter for input and authority?
   <details><summary>Hint</summary>Ownership says <em>which client</em> a networked object "belongs" to — typically a player owns their own character. The owner is allowed to send inputs for it (and may own certain network variables); the server still validates. It matters because you don't want Player A able to move Player B's character — ownership scopes who's allowed to drive what, with the server as backstop.</details>
9. What is a **headless** (dedicated) server build, and why is it different from a normal game build?
   <details><summary>Hint</summary>A headless build runs the game logic with <strong>no graphics, no audio, no input window</strong> — just the simulation and the network. It's a server, not a player. It's lighter (no rendering), runs on machines with no GPU/display, and is the build you deploy. In Unity it's the Dedicated Server build target / batchmode-nographics. It's exactly what you put in a container.</details>
10. What problem does **Docker** solve, and why is "it works in a container" stronger than "it works on my machine"?
    <details><summary>Hint</summary>Docker packages your server <em>and its entire environment</em> (OS libs, runtime, dependencies, config) into one immutable <strong>image</strong>; a running copy is a <strong>container</strong>. "Works on my machine" breaks the moment the next machine has a different library version. A container carries its environment with it, so the same image runs identically on your laptop, a teammate's, CI, or (W10) AWS. Containers are <em>reproducible servers</em> — which is why the cloud deploys them.</details>

---

## 🌟 Side Quest 1 — Lag Simulator (+50 XP)

Prove you understand *why* prediction and interpolation exist by making the network **hurt** on purpose. Add artificial latency and packet loss to your co-op build, watch what breaks, then confirm your prediction/interpolation actually papers over it.

**Requirements:**
1. Add a **network simulator** to your transport — inject artificial **latency** (e.g. 100–300 ms RTT) and **packet loss** (e.g. 2–10%). (Unity's transport has a built-in Network Simulator; or gate it behind a debug toggle.)
2. With the simulator **on but prediction/interpolation off**, observe and write down what goes wrong: your own player feels laggy/rubber-bandy, the remote player teleports.
3. Turn **prediction + reconciliation** back on for your own player and **interpolation** on for the remote player. Confirm: your input feels instant again, the remote player moves smoothly despite the lag.
4. Expose the lag/loss values as **tunable knobs** (a debug panel or config) so you can dial the pain up and down without recompiling.

```
Test: set 250 ms RTT + 5% loss. OFF: your player rubber-bands and the other
player stutter-teleports. ON: your movement feels instant (prediction),
the other player glides (interpolation), and a deliberate server correction
visibly snaps you back once — proof reconciliation is doing its job.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```
THE EXPERIMENT (make it hurt, then fix it):

1. Transport simulator → set PacketDelay (ms) and PacketDropRate (%).
   Unity Transport (UTP) exposes a Network Simulator for exactly this.
2. Baseline with everything naive (no prediction, server echoes position):
     - your player: input → server → back. At 250 ms it's unplayable.
     - remote player: raw snapshots applied = teleport.
3. Re-enable the real model:
     - YOUR player: predict locally on input, store input + result, and when
       the server state arrives, REPLAY un-acked inputs from the server's
       position (reconciliation). A mismatch shows as a small snap.
     - REMOTE player: buffer the last few snapshots and interpolate between
       them ~100 ms in the past so motion is smooth.
4. Knob it: a debug UI with sliders for RTT and loss; toggle prediction and
   interpolation independently so you can SEE what each one buys.
```

- The simulator is a *teaching device*: the bugs you see with it off are precisely the bugs prediction (your player) and interpolation (remote players) were invented to fix.
- **Reconciliation is the subtle one** — prediction without reconciliation drifts; the server's correction is what keeps your prediction honest. The occasional snap *is the system working*, not a bug.
- This is engine-agnostic: every netcode stack (NGO, Mirror, custom, AAA) ships with a lag simulator because you *cannot* tune feel on a perfect local connection — real players have 80 ms and 3% loss.

🎯 **Side quest complete when:** with 250 ms RTT and 5% loss injected, your own player feels responsive and reconciles correctly, the remote player interpolates smoothly, and you can toggle each technique on/off via knobs to demonstrate what it buys. Add **+50 XP** to PROGRESS.md.
</details>

---

## 🌟 Side Quest 2 — Lobby / Host-Join UI (+50 XP)

Prove you can drive a real connection flow, not just an auto-connect hack. Build a tiny **lobby screen** that lets a player **Host**, **Join** (by IP/address), or run as a **Server (headless)** — the front door every multiplayer game needs and the thing that lets two clients reach your Dockerized server in the boss.

**Requirements:**
1. A simple in-game UI with three buttons: **Host** (server + local client), **Client** (join an address), and **Server** (headless/dedicated, no local player) — wired to start the network manager in the right mode.
2. An **address/port field** for Client mode so you can point it at `127.0.0.1` (local), a LAN IP, or (boss) the Docker container's mapped port.
3. A **connection status** readout: connecting → connected → players in session (count), plus a clear **disconnect/leave** path back to the lobby.
4. It must support the boss's flow: start the **Server** mode, then have **two Clients** connect to that same address and both spawn into the dungeon.

```
Test: launch one build as Server (or run the Docker container). Launch two
more builds, each enters the lobby, types the server address, hits Client,
and both connect — the status shows "2 players connected" and both spawn
into the same dungeon. Hit Leave → back to the lobby, clean disconnect.
```

<details>
<summary>💡 Reference approach (try first!)</summary>

```csharp
// Three buttons → three start modes on the NetworkManager (NGO).
public class LobbyUI : MonoBehaviour
{
    public string address = "127.0.0.1";
    public ushort port = 7777;

    public void OnHost()   { SetTransport(); NetworkManager.Singleton.StartHost();   }   // server + local player
    public void OnClient() { SetTransport(); NetworkManager.Singleton.StartClient(); }   // join address:port
    public void OnServer() { SetTransport(); NetworkManager.Singleton.StartServer(); }   // headless, no local player

    void SetTransport()
    {
        var t = (UnityTransport)NetworkManager.Singleton.NetworkConfig.NetworkTransport;
        t.SetConnectionData(address, port);   // the address field points clients at host / container
    }
}
```

```csharp
// Status: react to connect/disconnect to drive the UI.
void OnEnable()  { NetworkManager.Singleton.OnClientConnectedCallback += id => RefreshCount(); }
void RefreshCount() => statusLabel.text = $"{NetworkManager.Singleton.ConnectedClients.Count} players connected";
```

- The three modes map cleanly to the boss: **Server** (or the container) is the authority; the **two Clients** are the players. Host mode is the convenient "one of the players also runs the server" shortcut — but the boss wants a *separate* containerized server.
- The **address field is the whole point** — local testing uses `127.0.0.1`; connecting to the Docker container uses the host's address and the container's **mapped port** (`-p 7777:7777/udp`). Same UI, different target.
- Keep the lobby UI thin: it just chooses a mode and an address, then hands off to the network manager. The lobby is plumbing; the game is the payload.

🎯 **Side quest complete when:** the lobby can start Host / Client / Server modes, a Client can join an arbitrary address:port, two clients connect to one server and both spawn in, the status shows the live player count, and Leave returns cleanly to the lobby. Add **+50 XP** to PROGRESS.md.
</details>

---

[↑ Phase Home](README.md) · [↑ Home](../../README.md) · [✅ Checklist →](checklist.md)
