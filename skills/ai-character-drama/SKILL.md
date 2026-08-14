---
name: ai-character-drama
description: >-
  Produce a short multi-character AI video drama / skit / sitcom with CONSISTENT
  character faces across every shot. Use this whenever the user wants to make an
  AI short film, a 1-minute (or N-second) story video, a cartoon/3D-animated
  skit, a multi-cut narrative video with recurring characters, an explainer with
  the same mascot in every scene, an ad, or any video where the SAME character(s)
  must look identical shot-to-shot. Triggers on requests like "make a short
  drama", "AI 숏드라마/숏폼 만들어줘", "1분짜리 영상", "캐릭터가 나오는 영상", "make a sitcom with
  these characters", "character sheet + video", or any mention of Seedance /
  Higgsfield / 시댄스 / character consistency in video. Covers the full pipeline:
  storyboard + element matrix → character sheets (GPT Image 2 for characters,
  props/products, and environments) → reusable face/prop
  consistency Elements (@tags) → per-cut video (Seedance 2.0, genre drama, baked
  lip-synced dialogue) → SFX + narration
  (ElevenLabs) → burned-in subtitles + audio mix + final concat (ffmpeg) →
  background music (Suno) laid over the finished video as the default final pass
  — one continuous instrumental mixed low (~0.10), never baked per-cut; visual
  style follows the user's request (no hardcoded Disney/Pixar look). Supports
  both 16:9 and vertical 9:16 (shorts/reels/릴스/쇼츠 → default 9:16); runs an
  automated QC gate on every rendered cut (frame extraction + STT transcript)
  before assembly; keeps a project.json state file so work can resume across
  sessions and partial re-renders stay safe; shows a credit/cost estimate before
  the expensive video step; optional final passes: virality prediction and
  multi-language dubbing. Prefer this skill over ad-hoc single image/video calls
  whenever recurring characters or a multi-shot story are involved.
---

# AI Character Drama — consistent multi-shot video production

This skill builds a short narrative video (default ~1 min = 4 × 15s cuts) where
the **same characters keep the same face in every shot**. The whole trick to
consistency is: generate a clean character sheet once, register it as a reusable
**Element**, and reference it by an `@tag` placeholder in every downstream image
and video prompt.

## The one rule that makes or breaks this

**Every recurring entity — each character, the environment, AND every recurring
prop or product — must be a registered Element, and every prompt that shows it
must reference it via its `<<<element_id>>>` placeholder.** The backend swaps the
placeholder for the real reference image and rewrites it to `@name`. Anything you
only *describe in words* (not tagged) will look different in every shot — a glass
bottle becomes a different bottle, a hero product becomes a lookalike, a sword
changes shape. The most common mistakes are (a) forgetting a minor-but-recurring
character (e.g. the boss who appears in cut 1 and cut 4) and (b) forgetting a
**prop/product** that's central to the plot (the bottle that's found, thrown,
washed ashore, and opened across four cuts). If a person, place, prop, OR product
appears in 2+ cuts — or it's a hero object the story revolves around even in a
single cut — it needs an Element. **This is non-negotiable for real products**: if
the video features an actual product/SKU, the real product image must be the
Element; never let the model synthesize a lookalike.

### Storyboard-first, with an element matrix (before generating ANY cut)

Plan the shots on paper FIRST, then derive the complete asset list from them — not
the other way around. Build an **element matrix**: a table with one row per cut and
columns for *characters*, *environment*, and *props/products*, naming the exact
Element each cut needs. The matrix is the single source of truth — it tells you
(1) every asset you must generate and register up front, and (2) exactly which
`<<<id>>>` placeholders each cut's prompt must contain. Generate and register
*all* of those assets (characters + backgrounds + every prop/product) **before**
rendering any cut, so the bottle in cut 1 is the same Element as the bottle in cut
4. Save the matrix in `STORYBOARD.md`. Example:

| Cut | Characters | Environment | Props / Products |
|-----|-----------|-------------|------------------|
| 1   | `king`            | `shore_joseon` | `bottle` |
| 2   | `king`, `minister`| `shore_joseon` | `bottle` |
| 3   | `heroine`         | `beach_hawaii` | `bottle` |
| 4   | `heroine`, `king` | `beach_hawaii` | `bottle` |

When you generate each cut, cross-check its prompt against the matrix row: every
entity listed must appear as a `<<<id>>>` placeholder, or it will drift. If a
later revision changes a prop or product, regenerate its Element and re-render
*every* cut in that prop's matrix column — not just the one you noticed.

## Tools used (load via ToolSearch first)

- **Images — characters, props, products, environments (everything):** Higgsfield
  MCP `generate_image`, model **`gpt_image_2`** (good text/typography → readable
  product labels and shirt names) or `nano_banana_2`. Use this for realistic
  people, stylized/non-human characters, props/products, and background plates
  alike — one model for all image assets. **MANDATORY on EVERY image call:
  `quality:"high"`, `resolution:"2k"`, `aspect_ratio:"<project AR>"` (16:9 or
  9:16, decided in step 1) — never omit `quality`; if omitted the API silently
  defaults to low and the asset comes out soft/blurry.**
- **Face consistency:** Higgsfield `show_reference_elements` (action=create) +
  `show_generations` / `job_display` to read results. (Register the `gpt_image_2`
  output as an `image_job` Element; Seedance then references it by `<<<id>>>`.)
- **Video (default):** Higgsfield `generate_video`, model **`seedance_2_0`
  (Seedance 2.0)** — reference-Element driven identity, `duration` 4–15s, the
  project AR (16:9 or 9:16), and
  a literal **`genre:"drama"`**. It bakes the characters' **lip-synced dialogue** and
  sets `generate_audio:true` itself, so spoken lines come out of the render — mix
  around that native audio (see Audio design). Seedance honors `<<<element_id>>>`
  references for character/prop consistency. Express the dramatic tone in both
  `genre:"drama"` and the prompt ("cinematic drama, emotional, moody dramatic
  lighting, filmic").
- **Sound effects (SFX):** ElevenLabs MCP `text_to_sound_effects` — the only music
  layer the default pipeline adds. Generate short cues (whoosh, magic poof, cork
  pop, waves, sparkle) and place them on the action beats.
- **Narration/TTS:** ElevenLabs MCP `text_to_speech` + `search_voices`.
- **QC + subtitle timing (mandatory per cut):** ffmpeg frame extraction
  (`scripts/qc_frames.sh`) + Read for visual checks, and ElevenLabs
  `speech_to_text` on each cut's native audio — one transcript serves both the
  language/dialogue QC check AND the subtitle timing (word-level timestamps).
  Higgsfield `video_analysis_create`/`video_analysis_status` is an optional
  deeper check when frames alone are ambiguous.
- **Cost estimate (before video):** Higgsfield `balance` (+ ElevenLabs
  `check_subscription` if narration-heavy) — read remaining credits and show a
  rough per-cut estimate on the casting board before any Seedance render.
- **Vertical / reframing:** generate natively in the target aspect ratio
  (`aspect_ratio:"9:16"` end-to-end for shorts/reels); Higgsfield `reframe` only
  to convert an *already-finished* video to another ratio.
- **Optional final passes:** Higgsfield `virality_predictor` (hook/retention
  report on the finished video) and ElevenLabs `dubbing` (multi-language
  versions of `FULL_bgm.mp4`).
- **Background music (default final pass):** Suno — no MCP exists for it; the
  user generates an instrumental on suno.com (prompt provided by this skill) and
  saves it as `music/bgm.mp3`. One continuous instrumental matched to the full
  runtime, laid over the **assembled** video and mixed UNDER dialogue+SFX at ~0.10
  — never per cut, never inside the Seedance renders (see Audio design).
- **Assembly:** local `ffmpeg` + `python3`/Pillow for subtitles.

The Higgsfield MCP server name is a UUID (e.g. `915f7826-...`); tools look like
`mcp__<uuid>__generate_image`. Find them with ToolSearch keyword `generate_image`,
`seedance`, `reference_elements`, etc.

## Workflow (run top to bottom)

Read `references/workflow.md` for the detailed, copy-pasteable version with exact
parameters and every gotcha.

**MANDATORY before writing ANY prompt (bible, storyboard, image, video, audio):
read `references/prompt-mastery.md` and run its self-review rubric (§6) on every
prompt before submitting it.** That file encodes the prompt-writing judgment this
skill depends on — beat budgets, dialogue syllable limits, camera grammar, face
anchors, the wish-sentence test — so output quality stays constant regardless of
which model executes the skill. Templates (prompt-templates.md) are the skeleton;
prompt-mastery.md is how to fill the blanks well.

For dialogue-free, continuity-critical cuts (animal leads, spatial tricks like
off-screen transformations, clip-chained sequences), read
`references/higgsfield-structure.md` — a 12-section structured prompt format
(OPTICS with FOV°+distance, HARD CUT shot design, PHYSICS contracts, POSITIVE
LOCKS) distilled from Higgsfield Cinema Studio, plus revision recipes for common
failures. Dialogue cuts stay on the compact format — never mix the two.

Two more references upgrade the whole pipeline (from Higgsfield's open-sourced
95-min feature "Hell Grind", 2026-08):
- `references/hellgrind-playbook.md` — asset-craft hacks (headless full-body
  sheet, boring-sheet rule, catch-light check, masked point-edits, stress test,
  crowd/giant scale anchors, reverse-angle-via-video), prompt techniques (GEO
  SPATIAL LAYOUT, first-second wide + dialogue-tail seams, EXACT N header,
  positive-form-only actions, no-age rule, ban dictionary, lens decision tree,
  lighting priority locks, context isolation), the surgical image-edit lane
  (CHANGE / PRESERVE EXACTLY), and production discipline (one-line iterations +
  log, 10–15 rule, trim 0.5s at clip edges).
- `references/acting-system.md` — the acting playbook: behavior-not-emotion,
  five pillars, master profiles, eye life, voice lock, ensemble rules, and the
  bad-acting diagnosis table. Consult it for every cut with performance in it.
Originals live in `references/source/` (CINEDANCE V4, ACTING, LIRA, brief).

The high-level arc:

1. **Write the bible first.** Decide characters (name, personality, outfit, a
   distinctive color, what's printed on their shirt), the environment, and a tight
   beat sheet split into N 15-second cuts, each cut with per-second beats and one
   or two lines of dialogue. Save it as `CREATIVE_BIBLE.md`. Comedy needs each
   character to react *differently* to the same trigger — that contrast is the joke.
   **Lock each main character's ACTING here too** (read
   `references/acting-system.md`): a master acting profile (one English
   paragraph — engine, vocal profile, tics WITH triggers, named gait, mask +
   crack "However, when X...") and a **Voice prompt** (1–2 quoted sentences:
   age-range/accent/timbre/pace/emotional character) that gets pasted VERBATIM
   into every cut where that character speaks — never adapted per scene. Every
   cut's acting is a scene-adaptation of the master profile, never a
   contradiction of it.
   **Pick the visual style from what the USER asked for — do NOT default to Disney /
   Pixar / 3D-animation.** If the user wants real-looking people, the unified style
   is photoreal/cinematic live-action (e.g. "cinematic photorealistic, natural skin,
   soft daylight, shallow depth of field"). Only use a cartoon/3D style if the user
   explicitly requests it. Write the chosen style string once and reuse it verbatim
   in every prompt so all cuts match.
   **Also decide the aspect ratio HERE, before any asset exists.** If the user
   says 숏폼/쇼츠/릴스/틱톡/shorts/reels/vertical → **9:16**; cinematic/YouTube/TV
   → 16:9; default to 16:9 only when there's no platform signal. The chosen AR
   goes into *every* image call, *every* Seedance call, and the subtitle canvas
   (16:9 → 1280×720, 9:16 → 720×1280) — mixing ratios mid-pipeline means
   regenerating assets, so lock it now and record it in `project.json`.
   **Create `project.json` in the project root now** and update it after every
   step (see "Project state & resume" below) — it's what makes the pipeline
   resumable and partial re-renders safe.
   **Peek at credits here too** — one `balance` call before generating anything.
   The full cost gate comes on the casting board, but image assets are spent
   *before* that gate; if the balance already can't cover images + video + one
   retry, agree on a smaller shape (fewer cuts/characters) before spending.
2. **Storyboard + element matrix (mandatory, before any generation).** Break the
   beat sheet into per-cut shots and build the element matrix (see "Storyboard-first"
   above): for each cut list its characters, environment, and **props/products**.
   Save `STORYBOARD.md`. The union of all matrix cells = the exact asset list to
   generate next. Nothing gets generated until this list exists.
   **Blocking lock (블로킹 락) — mandatory for every scene that spans 2+ cuts in the
   same location.** Elements lock *who* the characters are; the blocking lock locks
   *where* they are. For each such scene, write ONE fixed spatial sentence in
   `STORYBOARD.md` and copy it **verbatim into every cut prompt of that scene**:
   who is on screen-left vs screen-right, facing which way, sitting/standing where
   relative to the set (e.g. *"<<<king>>> sits on the LEFT side of the table facing
   right; <<<minister>>> stands on the RIGHT facing left; all shots stay on the same
   side of the action axis (180-degree rule); the characters never swap screen sides
   between shots or cuts."*). Without this line Seedance re-invents the staging for
   every cut — same faces, but positions/left-right flip between cuts and the
   assembled scene breaks continuity. Record the lock string in `project.json`
   alongside the scene so partial re-renders reuse it exactly.
3. **Generate every asset the matrix names** with **`gpt_image_2`** (or
   `nano_banana_2`) — one model for everything; the asset type only changes the
   variant count and the approval gate:
   - **Main protagonist(s) → 4 variants, user picks (approval gate).** For each lead
     render **4 candidate portraits** (`gpt_image_2` with `count:4`), download all
     four, show them labelled ①②③④, and **STOP — wait for the user to choose**.
     Register only the chosen image as that character's Element.
   - **Supporting human characters (조연) → 2 variants each, user picks.** Every
     other *person* in the cast gets **2 candidates** (`gpt_image_2` with `count:2`),
     presented labelled ①② for the user to choose. Register only the chosen one.
   - **Non-human characters (mascots, creatures) → single shot, no gate** unless the
     user asks for options.
   - **Environments, props/products → `gpt_image_2`** — a wide empty plate per
     environment; **a clean centered product-style shot per prop/product** (neutral
     studio background, e.g. "a small antique glass bottle with a cork, single
     object, centered"). For a real product, use its actual photo, not a generated
     lookalike.

   Apply the user's chosen unified style string (from step 1) to *everything* so cuts
   match. Download and **look at every asset** to confirm.

   **HARD GATE: do not register any human-character Element, generate the storyboard
   preview, or render ANY cut until the user has picked every person's image** (lead
   from 4 options, each supporting human from 2). Video is the expensive step — lock
   all the faces with the user first. Present every person's options together in one
   round so the user picks them all at once.

   **Present the character candidates as a CASTING BOARD (HTML), not a bare list.**
   Build a single `casting_board.html` in the project root that lays out every
   character's candidates in a clean grid — one labelled section per character
   (`주인공`, `신하` …), each candidate shown as its actual downloaded image with a big
   number badge `①②③④` / `①②` overlaid, the character's name/role as a section
   heading, and a short caption line telling the user how to answer (e.g. "주인공 3,
   신하 1"). **Embed every image as a base64 `data:` URI inside the HTML — never use a
   relative/local `src` like `characters/<name>_1.png`.** Relative paths render blank
   in most preview/chat surfaces (the file is opened outside its folder, so the PNGs
   don't resolve) — this is the #1 reason a casting board "shows nothing". Downscale
   each candidate to a small JPEG (~800px wide) and inline it so the board is a single
   self-contained file that displays anywhere. Recipe:
   ```bash
   # shrink every candidate, then base64-inline into the HTML.
   # Glob — do NOT hardcode 1..4: leads have 4 variants, supporting humans only 2.
   for p in characters/*_[0-9].png; do
     sips -s format jpeg -s formatOptions 80 --resampleWidth 800 \
       "$p" --out "/tmp/$(basename "${p%.png}").jpg" >/dev/null
   done
   python3 - <<'PY'
   import base64, glob, os
   def b64(p): return "data:image/jpeg;base64,"+base64.b64encode(open(p,'rb').read()).decode()
   html = open('casting_board.html').read()
   for png in glob.glob('characters/*_[0-9].png'):
       jpg = '/tmp/' + os.path.basename(png)[:-4] + '.jpg'
       if os.path.exists(jpg):
           html = html.replace(f'src="{png}"', f'src="{b64(jpg)}"')
   open('casting_board.html','w').write(html)
   PY
   ```
   Use a dark board background with card framing so faces read clearly, and make it
   responsive. **Below the candidate grid, add a "STORY" section** showing
   the story they're casting for as reference — a one-line logline plus the per-cut
   beat outline from `STORYBOARD.md` (CUT 1~N: 장소 · 등장인물 · 핵심 비트/대사 한 줄) —
   so the user can judge each face against the actual story while picking.
   **Also add a "COST" section — the cost gate.** Before building the board, call
   Higgsfield `balance` and put a small table on the board: remaining credits, the
   planned spend (N cuts × 15s Seedance renders + the storyboard preview + any
   assets still to generate), and what one full re-render of a single cut costs —
   so the user can decide to trim 4 cuts to 3 (or shorten durations) *before* the
   expensive step, in the same reply as their casting picks. If remaining credits
   look insufficient for the plan + at least one retry cut, say so explicitly and
   propose the cheaper shape.
   **The moment the board is complete, open it in the browser automatically — run
   `open casting_board.html` (macOS) right away.** Don't just send the file or ask
   whether to open it; launching the HTML window is the default delivery. (Also send
   the file with SendUserFile as a backup for mobile/remote sessions.) Then **STOP
   for their pick.** The casting board is the standard way to show character options.

   **Always NUMBER what you show so the user can reply with just numbers.** Label each
   candidate clearly per character — e.g. `주인공 ①②③④`, `신하 ①②` — and tell the user
   how to answer (e.g. "주인공 3, 신하 1"). Keep the numbering consistent for any later
   re-pick. This applies to *every* set of options you ever show (candidates, style
   choices, BGM takes, edits) — number them, no exceptions, so picking is one tap.
4. **Register every asset as an Element** — characters, environments, AND every
   prop/product (`show_reference_elements` action=create, `type:"image_job"` + the
   job id + its CloudFront url; props use `category:"prop"`). Save each returned
   `element_id` next to its row in the matrix. Give them short tag names
   (`king`, `minister`, `shore_joseon`, `bottle`). **A real photo (actual product
   shot, user-supplied image) has no image_job id** — upload it first with
   `media_upload` / `media_import_url` and register the returned media id/url with
   the type the upload reports (details: workflow §4); verify with one cheap test
   image before any video spend.
5. **Storyboard keyframe images — MANDATORY user OK gate before ANY video render.**
   For every cut, generate ONE keyframe image (`gpt_image_2`, project AR,
   `quality:"high"`, `resolution:"2k"`) embedding that cut's Elements via
   `<<<id>>>` — the cut's key moment, matching the blocking lock. Build a
   **storyboard board HTML** (`storyboard_board.html`, same conventions as the
   casting board: base64-inlined images, numbered `CUT` sections, each cut's
   beats + dialogue captioned under its keyframe, a cost table for the planned
   video renders), open it with `open` AND send it via SendUserFile, then
   **STOP and wait for the user's explicit OK.** Only images may be generated
   before this OK — no Seedance/video job of any kind. Record the keyframe job
   ids under `storyboard.keyframes` in `project.json`, and set
   `storyboard.approved: true` only when the user says OK — a resumed session
   checks that flag and re-presents the board instead of rendering if it isn't
   true. If the user requests changes, regenerate only the affected keyframes
   and re-present. (User rule, 2026-07-06: "필요한 이미지만 만들고 스토리보드처럼
   보고 → OK 사인 후에만 영상".)
6. **Generate each cut** with `seedance_2_0` (Seedance 2.0), `genre:"drama"`,
   `duration:15`, a **drama tone in the prompt** ("cinematic drama, emotional,
   dramatic lighting, filmic"), embedding **every** Element from that cut's matrix
   row (characters + environment + props/products) via `<<<id>>>`. Cross-check the
   prompt against the matrix row before submitting — a missing placeholder =
   guaranteed drift. Label the prompt `CUT N (0-15초)` and give per-second beats.
   **Make each cut MULTI-SHOT, not one locked-off take — but let the AI direct it.**
   Don't hard-assign shots to fixed second ranges; instead ask for natural coverage
   that follows standard film grammar — e.g. *"edited as a multi-shot scene with
   motivated hard cuts between varied angles (establishing, two-shot, close-ups,
   reaction, insert) chosen naturally to fit the action and dramatic beats; dynamic
   cinematic coverage."* Let the model decide how many shots and where the cuts fall.
   (If the workspace exposes a dedicated multishot video tool, prefer it; otherwise
   the multi-shot instruction in the `seedance_2_0` prompt is the lever.) Keep the
   tagged Elements identical across the shots so faces/props stay consistent through
   the angle changes.
   **If the cut belongs to a multi-cut same-location scene, paste that scene's
   blocking-lock sentence (from `STORYBOARD.md` / `project.json`) verbatim into the
   prompt, right after the character line** — same wording in every cut of the scene,
   so screen positions and the camera axis hold across cuts, not just within one.
   (Complex geography → use a GEO SPATIAL LAYOUT block instead; see
   `references/hellgrind-playbook.md` §4.1.)
   **Three Hell Grind cut rules:** (a) open the scene's FIRST cut with a ~1-second
   position-fixing wide (no lines, no action — optionally one short word like "hm");
   on seam cuts, feed the tail of the previous cut's line into that first second so
   the clips glue at the join; (b) start multi-character cuts with an
   "EXACT N CHARACTERS — NO DUPLICATES: ..." header and lock prop counts
   ("exactly ONE ..."); (c) write actions in positive form only, never write a
   young character's age, and adapt each present character's acting from their
   bible master profile (state / wants / hides / rhythm / what changes).
   **Write spoken dialogue in the target language** (Korean lines for Korean speech).
   Seedance bakes the characters' **lip-synced dialogue** and `generate_audio:true`
   itself, so spoken lines come out of the render — mix around that native audio
   (step 8). **In EVERY cut prompt, explicitly forbid background music** — append a
   line like *"no background music, no BGM, no soundtrack — only spoken dialogue and
   natural diegetic sound (footsteps, waves, etc.)."* Seedance auto-generates audio
   and will otherwise drop a **different** music bed into each 15s clip; those beds
   **audibly jump/glitch at every concat seam** and can't be cleanly removed. Keep
   the cuts music-free; the soundtrack is added **once at the very end** as a single
   continuous ~1-minute Suno track over the whole assembled video (step 9). Generate
   cuts in parallel; retry transient errors. If a cut returns a "preset
   recommendation" notice instead of a job, resubmit with
   `declined_preset_id:"<id from the notice>"`.
6b. **QC gate — verify every cut BEFORE assembly (mandatory).** The skill's
   whole point is consistency, so consistency gets checked by machine+eyes, not
   vibes. As each cut finishes: (a) extract sample frames with
   `scripts/qc_frames.sh videos/cutN.mp4` and **Read them next to the character
   sheets** — same face? same prop? environment matches? style string holding?
   **Blocking check:** for multi-cut same-location scenes, compare this cut's
   frames against the previous cut's — is each character still on the same side
   of the screen, facing the same way, per the scene's blocking lock? A left-right
   swap between cuts is a QC fail even if every face is perfect.
   (b) run ElevenLabs `speech_to_text` on the cut's audio — is the dialogue in
   the target language, are the scripted lines actually spoken, and is there any
   music bed that slipped past the no-BGM clause? Record pass/fail per check in
   `project.json` (`cuts[N].qc`). **A failed cut gets regenerated NOW** (fix the
   prompt — usually a missing `<<<id>>>`, wrong-language dialogue, or a dropped
   no-BGM line — and resubmit) — never assembled around. Keep the STT transcript
   (word timestamps) — it drives subtitle timing in step 8. If frames alone are
   ambiguous (e.g. "is that the same bottle?"), `video_analysis_create` is the
   deeper second opinion.
7. **Sound effects + narration** in parallel with the video renders. **SFX**
   (ElevenLabs `text_to_sound_effects`): short cues on the action beats (whoosh,
   magic poof, cork pop, waves, sparkle). **Narration** (ElevenLabs `text_to_speech`,
   pick a voice in the right language) for intro/outro bookends. **No background
   music** at this stage.
8. **Assemble** with ffmpeg: dialogue-first audio mix (native dialogue loud +
   SFX cues placed on beats + narration only in gaps), burned-in subtitles, then
   concat to the full timeline. **Time the subtitles from the step-6b STT
   transcripts, not from the scripted beats** — the word-level timestamps say
   exactly when each line is spoken, so subtitle windows land on the actual
   speech (see Subtitles). **No BGM in this pass** — it goes on next, over the
   whole timeline at once (step 9), never per cut.
9. **Background music — default final pass.** Once `FULL.mp4` is concatenated,
   have the user generate **one continuous instrumental matched to the full
   runtime** (~1 minute for a 4-cut video) on suno.com (Instrumental toggle ON;
   hand them a ready-to-paste prompt and ask for the mp3 as `music/bgm.mp3`) — a
   single track, NOT one per cut — and lay it across the **already-concatenated
   `FULL.mp4`**, re-mixed UNDER the existing dialogue+SFX at a low level (~0.10).
   Mixing over the full timeline (not per-cut) is what keeps the music seamless
   across cut boundaries. Exception: a musical/choreography cut with baked-in
   music (seedance-cut-prompt musical recipe) gets NO Suno bed over its time
   range — duck the BGM to 0 there with volume automation (workflow §9).
   Export as `FULL_bgm.mp4` — **this is the headline
   deliverable**; keep the BGM-free `FULL.mp4` alongside it as a fallback.
10. **Optional final passes (offer, don't force).** Once `FULL_bgm.mp4` exists,
   offer two add-ons: (a) **virality report** — run Higgsfield
   `virality_predictor` on the finished video and summarize hook strength /
   retention risk with 1–2 concrete edit suggestions (e.g. tighten the first 3
   seconds); (b) **multi-language versions** — ElevenLabs `dubbing` on
   `FULL_bgm.mp4` for each requested language (`FULL_bgm_<lang>.mp4`). Note the
   burned-in subtitles stay in the original language; for a properly localized
   version, re-run step 8 with translated `subs.json` on the dubbed audio.

## Audio design — the lesson that matters

The native Seedance audio already contains the characters' (lip-synced) dialogue.
So **make dialogue the loud main layer (volume 1.0), add SFX cues on the action
beats, and place TTS narration ONLY where nobody is speaking.** Characters usually
talk ~most of each 15s cut (verify with `ffmpeg silencedetect`), so a long narrator
VO will collide with dialogue. Use narration as short bookends (an intro line over
the silent opening, an outro over the end card) rather than wall-to-wall. If a
narration line won't fit a gap, make it a subtitle instead of audio.

**Background music is a deliberate END-of-pipeline step** — it ships by default,
but never lives inside the per-cut renders. Two reasons it must be one track over
the *whole* video, not per-cut: (1) Seedance's auto-generated audio would put a
different bed in each 15s clip, and (2) any per-cut music **jumps/glitches at every
concat seam** because the clips aren't musically continuous. So forbid BGM in every
cut prompt (see step 6), assemble the SFX-only `FULL.mp4` first, then lay **one
continuous ~1-minute Suno instrumental** across the entire timeline and mix it under
everything at ~0.10, delivered as `FULL_bgm.mp4` (the headline deliverable; keep the
SFX-only `FULL.mp4` too). The single full-length track is what keeps the music
seamless across cut boundaries.

## Subtitles

Many ffmpeg builds on macOS lack `libass`/`drawtext`. The reliable path is:
render each subtitle line to a transparent full-frame PNG with Pillow
(Korean-capable font `/System/Library/Fonts/AppleSDGothicNeo.ttc`), then
composite with ffmpeg `overlay` gated by `enable='between(t,start,end)'`. Use
the bundled `scripts/gen_subs.py` (manifest-driven). Dialogue = white,
narration/labels = warm yellow, both with a black stroke + semi-transparent box
for readability.

**Canvas matches the project AR:** 16:9 → `--w 1280 --h 720` (default); 9:16 →
`--w 720 --h 1280 --margin 190` — the raised margin keeps lines above the
platform UI (progress bar, captions, action buttons) in shorts/reels players.

**Timing comes from the STT transcript, not guesswork.** Each cut already has a
word-level transcript from the QC gate (step 6b). Map every dialogue line to its
first/last word timestamps and use those (±0.2s padding) as the
`between(t,start,end)` window in assemble.sh. Narration/label lines go in the
transcript's silence gaps. Scripted-beat timing is only the fallback when STT
fails on a cut; then ±0.5s vs lip movement is acceptable.

## Project state & resume — `project.json`

The pipeline is long and expensive; the conversation is not the database.
**`project.json` in the project root is the single machine-readable state file**
— create it in step 1 and update it *immediately* after every step completes
(asset generated, user pick recorded, Element registered, cut submitted, QC
pass/fail, assembly done). Schema template in
`references/prompt-templates.md`; the essentials per entry: aspect ratio +
unified style string, every character/env/prop with its image job id, chosen
variant, and `element_id`, every scene's blocking-lock sentence (`scenes`), the
storyboard keyframes + the **`storyboard.approved` flag** (the video gate — a
resumed session must not render while it's false), and every cut with its
Seedance job id, local file, QC result, and status
(`pending / rendered / qc_failed / final`).

Why it matters:
- **Resume:** if the session dies or context is summarized away, the next
  session reads `project.json` + `STORYBOARD.md` and continues from the first
  incomplete step — no re-generating paid assets, no re-asking the user for
  picks already made.
- **Partial re-renders:** "컷 3만 다시" or a changed prop = look up the entity's
  `element_id` and its matrix column in the state file, regenerate exactly those
  cuts, flip their status back to `pending`, and re-run QC — nothing else moves.
- **Never re-register an Element that already has an id** — check the state
  file first; duplicates break the `@tag` mapping and waste calls.

## Bundled scripts

- `scripts/gen_subs.py` — reads a `subs.json` manifest (`{id,text,type}` per line)
  and writes styled transparent subtitle PNGs. `type` is `dlg` or `narr`.
  `--w/--h` set the canvas (720×1280 for 9:16), `--margin` raises the baseline
  clear of vertical-player UI.
- `scripts/qc_frames.sh` — extracts N evenly-spaced frames per cut into
  `qc/<cut>/` for the step-6b visual QC (compare against character sheets).
- `scripts/assemble.sh` — reference ffmpeg recipe for the audio mix (dialogue +
  SFX + optional narration) and subtitle overlay, then concat into the final video.
  Copy and adjust timings/inputs per project. **Keep BGM out of the per-cut mix**;
  the final step lays the Suno track over the concatenated `FULL.mp4` at ~0.10 (§9).

## Gotchas (learned the hard way — see references/workflow.md for fixes)

- **Workspace credit/quota limit** on one provider → switch providers (this is why
  Higgsfield is the primary path; Runway's `gpt-image-2`/`seedance-2` are an
  alternate if available).
- **`job_display` status can lag** (shows `in_progress` after completion). Trust
  `show_generations` (lists completed jobs with result URLs) to confirm + fetch URLs.
- **Seedance "preset recommendation" notice** instead of submitting → resubmit with
  `declined_preset_id: "<id from the notice>"`.
- **Transient "Invalid or expired token" / server-not-responding** → just retry.
- **Wrong spoken language** → rewrite dialogue (and prompt) in the target language
  and regenerate that cut.
- **Inconsistent recurring character** → make them an Element and regenerate the
  cuts they appear in with the new `@tag`.
- **Characters swap positions between cuts of the same scene** (A was screen-left
  in cut 1, screen-right in cut 2, even though faces are consistent) → the cut
  prompts described the staging loosely (or differently per cut), so Seedance
  re-invented the blocking each time. Elements don't fix this — they lock identity,
  not position. Write the scene's **blocking lock** sentence (fixed screen sides +
  facing directions + 180-degree rule, see step 2) and paste it verbatim into every
  cut of that scene, then regenerate the cuts that violate it.
- **Inconsistent / missing prop or product** (e.g. the bottle changes shape or
  vanishes between cuts) → you forgot to tag it. Create a `prop` Element from a
  clean product shot, then regenerate **every cut in that prop's matrix column**
  with the new `<<<id>>>`. Fixing only the one cut you noticed leaves the others
  mismatched.
- **Skipping the QC gate because a cut "looks fine" in the thumbnail** →
  thumbnails hide drift. Run `qc_frames.sh` + STT on every cut, every time; a
  wrong-language line or a swapped face found *after* assembly costs a full
  re-assemble on top of the re-render.
- **BGM leaked into a cut despite the no-BGM clause** → the STT/audio QC pass is
  where you catch it; regenerate that cut (strengthen the clause), don't try to
  filter the music out — it can't be cleanly stripped.
- **Aspect ratio drift** (one asset generated 16:9 in a 9:16 project) → every
  downstream composite letterboxes. `project.json` records the AR; check it
  before every generate call.

## Output

Deliver a project folder: `characters/`, `background/`, `props/`, `storyboard/`,
`videos/` (the N 15s cuts + `FULL.mp4` + `FULL_bgm.mp4`), `sfx/`, `narration/`,
`music/`, `qc/` (QC frames + STT transcripts), plus `CREATIVE_BIBLE.md`,
`STORYBOARD.md` (the element matrix), `project.json` (the state file — leave it
accurate and final; it's what makes future revisions cheap), and a short
`README.md`. The headline deliverable is **`FULL_bgm.mp4`** — the final
concatenated video with consistent faces, consistent props/products, dialogue,
SFX, STT-timed subtitles, and one continuous Suno BGM mixed under everything at
~0.10. Keep the BGM-free `FULL.mp4` alongside it in case the user prefers the
clean mix, plus any optional-pass outputs (`FULL_bgm_<lang>.mp4`, virality
report).
