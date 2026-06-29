#!/usr/bin/env python3
"""Regenerate the derived sections of PROGRESS.md from the Detailed checklist.

The "✅ Detailed checklist" section is the single source of truth. Tick boxes
there, run this script (or just `git commit` — see the pre-commit hook), and it
recomputes:

  • 🗺️ World completion  (Status + XP earned + TOTAL)
  • 🧙 Character          (XP + Rank)
  • 🏆 Achievements unlocked  (incl. 💯 Completionist when all Side Quests are ticked)

Both the "✅ Detailed checklist" and "🌟 Side Quests" sections feed the totals.

XP rules (from RULES.md): Lesson = 125 XP (100 Quest + 25 Quiz),
Side Quest = 50 XP, Boss Battle = 500 XP, finishing a World = +250 XP bonus.
"""

import re
import sys
from pathlib import Path

PROGRESS = Path(__file__).resolve().parent.parent / "PROGRESS.md"

# Lessons per world (counted from phases/*/lessons/). Used to value the single
# "Lessons complete" checkbox for worlds that don't list lessons individually.
LESSONS_PER_WORLD = [4, 5, 5, 5, 4, 5, 5, 4, 4, 4, 5, 6, 3]

LESSON_XP = 125
BOSS_XP = 500
WORLD_BONUS = 250
SIDE_QUEST_XP = 50

# Total XP -> Rank ladder (highest threshold first).
RANKS = [
    (17000, "🏆 **Master Game Developer**"),
    (13000, "🧠 Lead Engineer"),
    (9000, "⚙️ Senior Gameplay Engineer"),
    (5000, "🎮 Gameplay Programmer"),
    (1500, "🐣 Junior Gameplay Programmer"),
    (0, "🥚 Intern"),
]

CHECKED = re.compile(r"^\s*-\s*\[[xX]\]")
UNCHECKED = re.compile(r"^\s*-\s*\[\s*\]")
WORLD_HEADER = re.compile(r"^###\s+.*World\s+(\d+)\b")


def parse_checklist(text):
    """Return {world_num: {lessons_done, lessons_total, boss, complete}}."""
    lines = text.splitlines()
    # Isolate the Detailed checklist section.
    start = next(i for i, l in enumerate(lines) if l.startswith("## ") and "Detailed checklist" in l)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))

    worlds = {}
    cur = None
    for line in lines[start:end]:
        m = WORLD_HEADER.match(line)
        if m:
            cur = int(m.group(1))
            worlds[cur] = {"lessons_done": 0, "lesson_lines": 0, "boss": False,
                           "complete": False, "header": line}
            continue
        if cur is None:
            continue
        is_box = CHECKED.match(line) or UNCHECKED.match(line)
        if not is_box:
            continue
        checked = bool(CHECKED.match(line))
        low = line.lower()
        if "🏆" in line or "complete" in low and "world" in low:
            worlds[cur]["complete"] = checked
        elif "boss" in low:
            worlds[cur]["boss"] = checked
        elif "lesson" in low:
            worlds[cur]["lesson_lines"] += 1
            if checked:
                worlds[cur]["lessons_done"] += 1
    return worlds


def parse_side_quests(text):
    """Return ({world_num: side_quests_done}, total_quests, done_quests)."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("## ") and "Side Quests" in l)
    except StopIteration:
        return {}, 0, 0
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))

    per_world = {}
    total = done = 0
    cur = None
    for line in lines[start:end]:
        m = WORLD_HEADER.match(line)
        if m:
            cur = int(m.group(1))
            per_world.setdefault(cur, 0)
            continue
        if cur is None or not (CHECKED.match(line) or UNCHECKED.match(line)):
            continue
        total += 1
        if CHECKED.match(line):
            done += 1
            per_world[cur] += 1
    return per_world, total, done


def compute(worlds, side_quests=None):
    """Return per-world dict with status + xp, in world order."""
    side_quests = side_quests or {}
    out = {}
    prev_complete = True  # World 0 is never locked.
    for n in sorted(worlds):
        w = worlds[n]
        total_lessons = LESSONS_PER_WORLD[n] if n < len(LESSONS_PER_WORLD) else w["lesson_lines"]

        # Worlds with a single "Lessons complete" box: 1 box stands for all lessons.
        if w["lesson_lines"] <= 1:
            lessons_done = total_lessons if w["lessons_done"] else 0
        else:
            lessons_done = w["lessons_done"]

        sq_done = side_quests.get(n, 0)
        xp = (
            lessons_done * LESSON_XP
            + (BOSS_XP if w["boss"] else 0)
            + (WORLD_BONUS if w["complete"] else 0)
            + sq_done * SIDE_QUEST_XP
        )
        any_progress = lessons_done or w["boss"] or w["complete"] or sq_done

        if w["complete"]:
            status = "✅ Complete"
        elif not prev_complete:
            status = "🔒 Locked"
        elif any_progress:
            status = "🔄 In progress"
        else:
            status = "⬜ Not started"

        emoji, name = split_header(w.get("header", ""), n)
        out[n] = {
            "status": status, "xp": xp, "complete": w["complete"],
            "lessons_done": lessons_done, "lessons_total": total_lessons,
            "boss": w["boss"], "sq_done": sq_done, "emoji": emoji, "name": name,
        }
        prev_complete = w["complete"]
    return out


def split_header(line, n):
    """'### 🖥️ World 0 — Environment Setup' -> ('🖥️', 'Environment Setup')."""
    m = re.match(r"^###\s+(\S+)\s+World\s+\d+\s+—\s+(.+?)\s*$", line)
    if m:
        return m.group(1), m.group(2)
    return "🎮", f"World {n}"


def max_xp(sq_total):
    """Total XP attainable: every lesson + boss + world bonus + every side quest."""
    lessons = sum(LESSONS_PER_WORLD) * LESSON_XP
    worlds = len(LESSONS_PER_WORLD) * (BOSS_XP + WORLD_BONUS)
    return lessons + worlds + sq_total * SIDE_QUEST_XP


def _badge(label, color):
    return f"![{label.lower()}](https://img.shields.io/badge/{label}-{color}?style=for-the-badge)"


def render_milestones(text, pct, started):
    """Rewrite the auto-generated badge block between the MILESTONES markers."""
    first_step = _badge("Unlocked", "22c55e") if started else _badge("Locked", "lightgrey")
    halfway = _badge("Unlocked", "9b59b6") if pct >= 50 else _badge("Locked", "lightgrey")
    certified = _badge("Unlocked", "FFD700") if pct >= 100 else _badge("Locked", "lightgrey")
    block = (
        f"\n![Progress](https://img.shields.io/badge/Progress-{pct}%25-2563eb?style=for-the-badge)\n\n"
        "| Reward | How to earn | Status |\n"
        "|--------|-------------|--------|\n"
        f"| 🌱 **First Steps** | Tick your **first** box — the journey begins | {first_step} |\n"
        f"| 🎖️ **Halfway Hero** | Reach **50%** total completion | {halfway} |\n"
        f"| 🏅 **Master Game Developer Certified** | Reach **100%** total completion | {certified} |\n"
    )
    return re.sub(
        r"(<!-- BEGIN:MILESTONES[^>]*-->).*?(<!-- END:MILESTONES -->)",
        lambda m: m.group(1) + block + m.group(2),
        text,
        flags=re.DOTALL,
    )


def rank_for(xp):
    for threshold, name in RANKS:
        if xp >= threshold:
            return name
    return RANKS[-1][1]


def render(text, computed, completionist=False):
    total_xp = sum(c["xp"] for c in computed.values())
    lines = text.splitlines()

    # --- World completion table: rewrite status (col 2) + xp (col 3) per world.
    row_re = re.compile(r"^\|\s*(\d+)\s*·")
    for i, line in enumerate(lines):
        m = row_re.match(line)
        if m:
            n = int(m.group(1))
            if n in computed:
                cells = line.split("|")
                # cells: ['', ' 0 · Name ', ' status ', ' xp ', '']
                cells[2] = f" {computed[n]['status']} "
                cells[3] = f" {computed[n]['xp']} "
                lines[i] = "|".join(cells)
        elif re.match(r"^\|\s*\|?\s*\*\*TOTAL\*\*", line):
            cells = line.split("|")
            cells[-2] = f" **{total_xp}** "
            lines[i] = "|".join(cells)

    # --- Character sheet XP + Rank (inside the ``` code block).
    for i, line in enumerate(lines):
        if re.match(r"^XP:\s", line):
            lines[i] = f"XP:     {total_xp}"
        elif re.match(r"^Rank:\s", line):
            # Strip markdown bold for the plain code block.
            lines[i] = f"Rank:   {rank_for(total_xp).replace('**', '')}"

    # --- Achievements: tick the box if its world is complete. Each achievement
    # line carries the same emoji as that world's "🏆 World N complete" line.
    world_complete_emoji = {}
    in_checklist = False
    cur_world = None
    for line in lines:
        if line.startswith("## ") and "Detailed checklist" in line:
            in_checklist = True
            continue
        if in_checklist and line.startswith("## "):
            in_checklist = False
        if not in_checklist:
            continue
        m = WORLD_HEADER.match(line)
        if m:
            cur_world = int(m.group(1))
        elif cur_world is not None and "🏆" in line and "complete" in line.lower():
            # Grab the achievement emoji after the "·" if present.
            tail = line.split("·")[-1]
            em = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", tail)
            if em:
                world_complete_emoji[em[0]] = cur_world

    in_ach = False
    for i, line in enumerate(lines):
        if line.startswith("## ") and "Achievements unlocked" in line:
            in_ach = True
            continue
        if in_ach and line.startswith("## "):
            in_ach = False
        if not in_ach or not (CHECKED.match(line) or UNCHECKED.match(line)):
            continue
        # 💯 Completionist unlocks when every Side Quest box is ticked.
        if "Completionist" in line:
            mark = "[x]" if completionist else "[ ]"
            lines[i] = re.sub(r"\[[ xX]\]", mark, line, count=1)
            continue
        ems = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", line)
        world = next((world_complete_emoji[e] for e in ems if e in world_complete_emoji), None)
        if world is not None:
            mark = "[x]" if computed.get(world, {}).get("complete") else "[ ]"
            lines[i] = re.sub(r"\[[ xX]\]", mark, line, count=1)

    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


EMOJI_RE = r"[\U0001F300-\U0001FAFF☀-➿️⃣]"


def parse_character(text):
    name = started = ""
    for line in text.splitlines():
        m = re.match(r"^Name:\s*(.*)$", line)
        if m:
            name = m.group(1).strip()
        m = re.match(r"^Started:\s*(.*)$", line)
        if m:
            started = m.group(1).strip()
    if not name or set(name) <= {"_"}:
        name = "Recruit"
    if not started or set(started) <= {"_"}:
        started = "—"
    return name, started


def parse_achievements(text):
    lines = text.splitlines()
    try:
        s = next(i for i, l in enumerate(lines) if l.startswith("## ") and "Achievements unlocked" in l)
    except StopIteration:
        return []
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    out = []
    for line in lines[s:e]:
        if not (CHECKED.match(line) or UNCHECKED.match(line)):
            continue
        unlocked = bool(CHECKED.match(line))
        body = re.sub(r"^\s*-\s*\[[ xX]\]\s*", "", line).strip()
        ems = re.findall(EMOJI_RE, body)
        emoji = ems[0] if ems else "🏆"
        name = re.sub(rf"^(?:{EMOJI_RE}|\s)+", "", body).strip()
        out.append({"emoji": emoji, "name": name, "unlocked": unlocked})
    return out


def rank_progress(total):
    asc = sorted(RANKS, key=lambda t: t[0])
    cur, nxt = asc[0], None
    for i, band in enumerate(asc):
        if total >= band[0]:
            cur = band
            nxt = asc[i + 1] if i + 1 < len(asc) else None
    cur_name = cur[1].replace("**", "")
    if nxt:
        span = nxt[0] - cur[0]
        into = total - cur[0]
        pct = round(into / span * 100) if span else 100
        return cur_name, nxt[1].replace("**", ""), into, span, pct, nxt[0]
    return cur_name, None, 0, 0, 100, None


PROFILE = PROGRESS.parent / "profile.html"

PROFILE_CSS = """
:root{--bg:#0b1020;--bg2:#141b33;--card:#1a2342;--card2:#222d52;--ink:#e8ecf8;
--muted:#8b95b8;--line:#2c3760;--green:#22c55e;--amber:#f59e0b;--purple:#9b59b6;
--gold:#ffd700;--blue:#3b82f6;--grey:#4b5575}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:
radial-gradient(1200px 600px at 80% -10%,#1e2a52 0,transparent 60%),
radial-gradient(900px 500px at -10% 10%,#2a1a44 0,transparent 55%),var(--bg);
color:var(--ink);min-height:100vh;padding:32px 18px;line-height:1.5}
.wrap{max-width:1080px;margin:0 auto}
h1{font-size:1.7rem;letter-spacing:.5px}
.sub{color:var(--muted);font-size:.9rem;margin-top:4px}
.sec{margin-top:34px}
.sec h2{font-size:1.05rem;text-transform:uppercase;letter-spacing:2px;
color:var(--muted);margin-bottom:14px;display:flex;align-items:center;gap:8px}
.hero{display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center;
background:linear-gradient(135deg,var(--card),var(--bg2));border:1px solid var(--line);
border-radius:20px;padding:26px 28px;box-shadow:0 12px 40px rgba(0,0,0,.35)}
.avatar{font-size:4.4rem;filter:drop-shadow(0 4px 14px rgba(155,89,182,.5));line-height:1}
.rank-name{font-size:1.5rem;font-weight:700}
.xp-big{font-size:2.4rem;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#a78bfa);
-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.bar{height:14px;border-radius:99px;background:#0c1430;border:1px solid var(--line);
overflow:hidden;margin-top:8px}
.bar>span{display:block;height:100%;border-radius:99px;
background:linear-gradient(90deg,#38bdf8,#a78bfa);box-shadow:0 0 12px rgba(124,58,237,.6)}
.bar.lg{height:20px}.bar.lg>span{background:linear-gradient(90deg,#22c55e,#7dd3fc)}
.tiny{font-size:.78rem;color:var(--muted);margin-top:6px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:16px;
padding:18px;text-align:center}
.tile .n{font-size:1.8rem;font-weight:800}
.tile .l{font-size:.74rem;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.world{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;position:relative}
.world.done{border-color:rgba(34,197,94,.5)}
.world.locked{opacity:.5}
.world .top{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.world .ico{font-size:1.6rem}
.world .nm{font-weight:700;font-size:.98rem}
.pill{font-size:.68rem;padding:3px 9px;border-radius:99px;font-weight:700;white-space:nowrap}
.p-done{background:rgba(34,197,94,.18);color:#86efac}
.p-prog{background:rgba(245,158,11,.18);color:#fcd34d}
.p-none{background:rgba(139,149,184,.16);color:#aeb6d6}
.p-lock{background:rgba(75,85,117,.3);color:#9aa3c4}
.world .row{display:flex;justify-content:space-between;font-size:.78rem;color:var(--muted);margin-top:8px}
.world .xp{font-weight:700;color:#a78bfa}
.badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:14px}
.badge{background:radial-gradient(circle at 50% 30%,var(--card2),var(--card));
border:1px solid var(--line);border-radius:16px;padding:18px 10px;text-align:center}
.badge .m{font-size:2.6rem;line-height:1;filter:drop-shadow(0 3px 10px rgba(167,139,250,.45))}
.badge .t{font-size:.8rem;font-weight:600;margin-top:8px}
.badge.locked{opacity:.4}
.badge.locked .m{filter:grayscale(1)}
.badge .s{font-size:.66rem;margin-top:6px;letter-spacing:1px;text-transform:uppercase}
.badge.unlocked .s{color:#86efac}.badge.locked .s{color:var(--muted)}
.rewards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.reward{border-radius:18px;padding:20px;border:1px solid var(--line);background:var(--card);position:relative;overflow:hidden}
.reward.on{border-color:transparent}
.reward.first.on{background:linear-gradient(135deg,#14532d,#0b1020)}
.reward.half.on{background:linear-gradient(135deg,#4c1d95,#0b1020)}
.reward.cert.on{background:linear-gradient(135deg,#854d0e,#0b1020)}
.reward .rm{font-size:2.4rem}
.reward .rt{font-weight:700;margin-top:6px}
.reward .rd{font-size:.78rem;color:var(--muted);margin-top:4px}
.reward .tag{position:absolute;top:12px;right:12px;font-size:.66rem;font-weight:700;
padding:3px 9px;border-radius:99px;text-transform:uppercase;letter-spacing:1px}
.reward.on .tag{background:rgba(34,197,94,.25);color:#86efac}
.reward.off{opacity:.5}.reward.off .tag{background:rgba(75,85,117,.3);color:#9aa3c4}
.foot{margin-top:36px;text-align:center;color:var(--muted);font-size:.75rem}
@media(max-width:640px){.tiles{grid-template-columns:repeat(2,1fr)}.hero{grid-template-columns:1fr;text-align:center}}
"""


def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_profile_html(text, computed, sq_done, sq_total, total_xp, pct):
    name, started = parse_character(text)
    achievements = parse_achievements(text)
    cur_rank, next_rank, into, span, rank_pct, next_th = rank_progress(total_xp)

    lessons_done = sum(c["lessons_done"] for c in computed.values())
    lessons_total = sum(LESSONS_PER_WORLD)
    worlds_done = sum(1 for c in computed.values() if c["complete"])

    # World cards.
    pill = {"✅ Complete": ("p-done", "Complete"), "🔄 In progress": ("p-prog", "In progress"),
            "⬜ Not started": ("p-none", "Not started"), "🔒 Locked": ("p-lock", "Locked")}
    world_cards = []
    for n in sorted(computed):
        c = computed[n]
        cls, label = pill.get(c["status"], ("p-none", c["status"]))
        klass = "world" + (" done" if c["complete"] else (" locked" if "Locked" in c["status"] else ""))
        lp = round(c["lessons_done"] / c["lessons_total"] * 100) if c["lessons_total"] else 0
        boss = "👹 ✓" if c["boss"] else "👹 —"
        world_cards.append(f"""
      <div class="{klass}">
        <div class="top"><span class="ico">{c['emoji']}</span>
          <div><div class="nm">{_esc(c['name'])}</div>
          <div class="tiny">World {n}</div></div></div>
        <span class="pill {cls}">{label}</span>
        <div class="bar" style="margin-top:12px"><span style="width:{lp}%"></span></div>
        <div class="row"><span>📚 {c['lessons_done']}/{c['lessons_total']} lessons</span><span>{boss}</span></div>
        <div class="row"><span class="xp">⚡ {c['xp']} XP</span><span>🌟 {c['sq_done']} side</span></div>
      </div>""")

    # Achievement badge medallions.
    badge_cards = []
    for a in achievements:
        st = "unlocked" if a["unlocked"] else "locked"
        tag = "Unlocked" if a["unlocked"] else "Locked"
        badge_cards.append(f"""
      <div class="badge {st}"><div class="m">{a['emoji']}</div>
        <div class="t">{_esc(a['name'])}</div><div class="s">{tag}</div></div>""")

    # Milestone reward cards.
    def reward(kind, mark, title, desc, on):
        cls = f"reward {kind} " + ("on" if on else "off")
        tag = "Unlocked" if on else "Locked"
        return f"""
      <div class="{cls}"><span class="tag">{tag}</span>
        <div class="rm">{mark}</div><div class="rt">{title}</div>
        <div class="rd">{desc}</div></div>"""

    rewards = [
        reward("first", "🌱", "First Steps", "Tick your first box", total_xp > 0),
        reward("half", "🎖️", "Halfway Hero", "Reach 50% completion", pct >= 50),
        reward("cert", "🏅", "Master Game Developer", "Reach 100% completion", pct >= 100),
    ]

    next_line = (f"{span - into} XP to <b>{_esc(next_rank)}</b>"
                 if next_rank else "Max rank reached — you are a <b>Master Game Developer</b>! 🏆")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(name)} · The Combined Bootcamp</title>
<style>{PROFILE_CSS}</style></head><body><div class="wrap">

  <h1>🎮 {_esc(name)}'s Character Sheet</h1>
  <div class="sub">The Combined Bootcamp · Pixel Forge Studios · Started {_esc(started)} · auto-generated from PROGRESS.md</div>

  <div class="sec">
    <div class="hero">
      <div class="avatar">{cur_rank.split(' ')[0]}</div>
      <div>
        <div class="rank-name">{_esc(cur_rank)}</div>
        <div class="xp-big">{total_xp:,} XP</div>
        <div class="bar" style="max-width:520px"><span style="width:{rank_pct}%"></span></div>
        <div class="tiny">{next_line}</div>
        <div class="bar lg" style="max-width:520px;margin-top:14px"><span style="width:{pct}%"></span></div>
        <div class="tiny"><b>{pct}%</b> of the bootcamp complete</div>
      </div>
    </div>
  </div>

  <div class="sec"><div class="tiles">
    <div class="tile"><div class="n">{total_xp:,}</div><div class="l">⚡ Total XP</div></div>
    <div class="tile"><div class="n">{lessons_done}/{lessons_total}</div><div class="l">📚 Lessons</div></div>
    <div class="tile"><div class="n">{worlds_done}/{len(LESSONS_PER_WORLD)}</div><div class="l">🗺️ Worlds</div></div>
    <div class="tile"><div class="n">{sq_done}/{sq_total}</div><div class="l">🌟 Side Quests</div></div>
  </div></div>

  <div class="sec"><h2>🎁 Milestone Rewards</h2><div class="rewards">{''.join(rewards)}</div></div>

  <div class="sec"><h2>🗺️ World Completion</h2><div class="grid">{''.join(world_cards)}</div></div>

  <div class="sec"><h2>🏆 Badges Earned</h2><div class="badges">{''.join(badge_cards)}</div></div>

  <div class="foot">🎮 Open this file in a browser. It regenerates every time you update
  PROGRESS.md (via <code>scripts/update_progress.py</code> or the git pre-commit hook).</div>

</div></body></html>"""
    return html


def main():
    text = PROGRESS.read_text(encoding="utf-8")
    worlds = parse_checklist(text)
    side_quests, sq_total, sq_done = parse_side_quests(text)
    computed = compute(worlds, side_quests)
    completionist = sq_total > 0 and sq_done == sq_total
    new_text = render(text, computed, completionist)

    total_xp = sum(c["xp"] for c in computed.values())
    cap = max_xp(sq_total)
    pct = round(total_xp / cap * 100) if cap else 0
    new_text = render_milestones(new_text, pct, started=total_xp > 0)

    changed = False
    if new_text != text:
        PROGRESS.write_text(new_text, encoding="utf-8")
        milestone = " · 🏅 Master Game Developer Certified!" if pct >= 100 else (" · 🎖️ Halfway Hero!" if pct >= 50 else "")
        print(f"✅ PROGRESS.md updated — {total_xp} XP ({pct}%), rank {rank_for(total_xp).replace('**', '')}{milestone}")
        changed = True

    # Regenerate the graphical profile from the (updated) progress data.
    html = generate_profile_html(new_text, computed, sq_done, sq_total, total_xp, pct)
    if not PROFILE.exists() or PROFILE.read_text(encoding="utf-8") != html:
        PROFILE.write_text(html, encoding="utf-8")
        print(f"🎮 profile.html updated — {pct}% complete")
        changed = True

    if not changed:
        print("PROGRESS.md & profile.html already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
