# 🎬 AI Drama Pipeline — by Hamlog

**From a single story idea to a finished AI short drama.**
A set of four Claude Code skills covering the entire pipeline:
"screenplay → cut prompts → video render → QC → assembly."

> Two commands in Claude Code and you're set up. Jump to [Install](#-install-just-2-lines).

🇰🇷 [한국어 README](README.md)

## 🆕 v2.6 — Cut chaining (continuity lock): the previous cut's last frame becomes the next cut's start

When a 30s/60s scene is split into 15s renders, faces stay consistent but camera height, prop state and positions get re-staged per cut, so the assembled scene "jumps" at every seam. That is now a formal pipeline step.

- **`scripts/last_frame.sh`** — extracts the true final frame of a rendered cut into `continuity/` (`LAST_OFFSET` steps back from a fade/blurred ending).
- **New workflow §6a** — mandatory chain for cuts that continue the same location with no time jump: previous cut rendered + QC passed → extract last frame → upload → feed into the next cut → first prompt line "Frame opens matching the final frame of CUT N: <state summary>".
- **Pick the input by the kind of seam** — same shot continues → Seedance 2.5 `start_image` (pins the first frame); hard cut to a new angle → continuity Element scoped to geometry/positions/prop state only, not camera angle; unbroken take required → `video_extension`.
- **`continuity_ref` in project.json** — per cut: source cut, media id, role. Re-rendering a cut invalidates every cut chained after it → re-extract and re-render.
- **New QC item** — chained cuts compare their first frame against the previous cut's last frame (`qc.continuity`).

## 🆕 v2.5 — Upgraded to the Seedance 2.5 spec

Validated against a 123-cut feature production in Higgsfield Studio and the official Seedance 2.5 prompting guide.

- **Single structured format** — every cut, with or without dialogue, uses the uppercase-header structure (SCENE CONTEXT … POSITIVE LOCKS … NEGATIVE). The compact format is retired.
- **2.5 extension blocks** — world-style prefix, ★LOCK★ (speaker/address, prop counts, axis), EVENT TRACK (timecoded events), CHARACTER ACTING, and a trailing NEGATIVE block.
- **30-second multi-shot as a standard pattern** — about 5 shots + 5 beats, HARD CUT timecodes at every shot boundary. One-take 30s only for traversal/chase cuts.
- **Updated length budget** — 400–600 words for a standard 15s cut, up to ~18,000 characters of platform input; measure with `wc -m` before delivery.
- **Mandatory closes on every cut** — the no-BGM close plus a caption close ("no captions, no subtitles, no on-screen text").
- **Background music as the final pass** — after assembly, one continuous Suno instrumental mixed low (≈0.10) over the whole runtime; never baked per cut.

## ✨ What can it do?

- "Here's my story — write me a 3-part short drama script" → A **complete screenplay** is built step by step, from treatment to a Word file.
- "Give me the video prompt for S#3" → The scene is converted into a **15/30-second cut prompt for Seedance 2.5** (3-beat structure, dialogue syllable budget, character Element tags).
- "Turn this script into a 1-minute short drama" → It **directs the entire production**: character sheets, cut renders, subtitles/SFX/narration, final assembly, and BGM.
- "Make a casting board / run QC / concat the cuts" → **Repetitive production chores are automated** with scripts: candidate comparison boards, frame-level QC, concat assembly.

## 🚀 Install (just 2 lines)

Open Claude Code and enter these two commands, one at a time:

① Add the marketplace:

```
/plugin marketplace add hamlog-ai/ai-drama-pipeline
```

② Install the plugin:

```
/plugin install hamlog-ai-drama-pipeline@hamlog-ai
```

Restart Claude Code and all four skills are recognized automatically.

<details>
<summary>Prefer to copy the skill folders manually? (manual install)</summary>

```bash
git clone https://github.com/hamlog-ai/ai-drama-pipeline.git
cp -R ai-drama-pipeline/skills/* ~/.claude/skills/
```

No git? Download `ai-drama-pipeline.zip` from
[Releases](https://github.com/hamlog-ai/ai-drama-pipeline/releases), unzip it,
and copy the contents of its `skills/` folder into `~/.claude/skills/`.

To use the skills in a single project only, copy them into that project's
`.claude/skills/` instead. They take effect after restarting Claude Code.

</details>

## 🔄 Pipeline flow

```
Story idea
   │
   ▼
screenplay-pipeline    Screenwriting (treatment → scene-by-scene script
   │                   → IP check → Word export)
   ▼
seedance-cut-prompt    Scene (S#N) → Seedance 2.5 cut prompt
   │                   (15s / 3 beats, syllable budget, Element tags,
   │                   blocking lock)
   ▼
ai-character-drama     Production director (character sheets → Elements
   │                   → cut renders → subtitles/SFX/narration
   │                   → assembly → BGM)
   ▼
drama-ops              Ops automation (candidate comparison boards
                       · QC frame extraction · retake comparison
                       · concat assembly · assembly logs)
```

## 📦 The four skills

| Skill | Role | Say this to trigger it |
|---|---|---|
| `screenplay-pipeline` | Turns a story pitch into a complete screenplay, step by step (meme-parody inserts, IP checklist, Word export included) | "Here's my story — write the script" |
| `seedance-cut-prompt` | Converts screenplay scenes into 15/30-second Seedance 2.5 cut prompts (★LOCK★, EVENT TRACK, NEGATIVE block); rewrites on policy-violation rejections | "Give me the video prompt for S#3" |
| `ai-character-drama` | Directs the entire production with character consistency (3-view sheets + Elements) | "Make me a 1-minute short drama" |
| `drama-ops` | Three Python scripts for boards/QC/assembly — so you never hand-write an HTML board again | "Make a casting board" |

**Dependency note**: `seedance-cut-prompt` references documents in
`ai-character-drama/references/`, so those two skills must be installed together.
The plugin installs all four at once, so you don't have to think about it.

## 🛠 Requirements

| Purpose | What you need | Required? |
|---|---|---|
| Video generation | A generation MCP server supporting Seedance 2.5 (or 2.0) (must support Element / reference-image registration) | Required for production |
| Assembly / QC | `ffmpeg` (`brew install ffmpeg`) | Required for assembly |
| Word export | Node.js | For .docx script output |
| Narration / SFX | ElevenLabs MCP | Optional |
| BGM | Suno (create on suno.com → save as `music/bgm.mp3`) | Optional |

Screenwriting and cut-prompt conversion work with Claude Code alone — none of the tools above are needed.

## 💬 Usage examples

```
"A brother and sister in the desert, and a single arrow decides their fate.
 Write me a 3-part short drama script"
→ screenplay-pipeline builds everything from treatment to scene-by-scene script

"Give me the video prompt for S#2, vertical 9:16"
→ seedance-cut-prompt converts it into a 15-second cut prompt

"Turn this script into a Short"
→ ai-character-drama runs character sheets → renders → subtitles → assembly

"Make a comparison board for the cut candidates"
→ drama-ops generates an HTML comparison board automatically
```

## ❓ FAQ

**Q. I don't have a video-generation MCP. Can I still use this?**
A. Yes. Screenwriting (`screenplay-pipeline`) and cut-prompt conversion
(`seedance-cut-prompt`) produce text, so they work out of the box. Paste the
prompts into any platform that supports Seedance 2.5 (or 2.0).

**Q. My cut prompt got rejected as a "policy violation."**
A. Paste the rejected prompt back and say "it got a policy violation" —
`seedance-cut-prompt` will rewrite it with IP-safe naming.

**Q. How do I get updates?**
A. Run `/plugin marketplace update hamlog-ai` to pull the latest version.

## 📄 License

CC BY-ND 4.0 — Use it freely and share it as-is, with attribution to Hamlog.
Redistributing modified versions is not permitted. ([LICENSE](LICENSE))

---

Made with 🐹 by **Hamlog**

- 🧵 Threads: [@hamlog_ai](https://www.threads.com/@hamlog_ai)
- 💬 KakaoTalk open chat: [Hamlog AI Video Lecture Room](https://open.kakao.com/o/gMTtW19h)
- 📧 Email: [ai.hamlog@gmail.com](mailto:ai.hamlog@gmail.com)
