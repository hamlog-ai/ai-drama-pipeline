# Detailed workflow & exact MCP calls

This is the copy-pasteable companion to SKILL.md. Tool names are
`mcp__<server-uuid>__<tool>`; discover via ToolSearch (`generate_image` for
`gpt_image_2`, `seedance`, `reference_elements`, `text_to_sound_effects`,
`text_to_speech`, and `suno_generate_music` for the final BGM pass).

**Prompt quality gate: before writing any prompt in any step below, read
`prompt-mastery.md` and pass its self-review rubric (§6). It holds the craft rules
(beat budgets, dialogue syllable limits, camera grammar, face anchors) that the
templates alone don't enforce.**

## 0. Set up the project folder + state file

```
project/
  characters/  background/  props/  storyboard/  videos/  sfx/  narration/  subs/
  music/  qc/  continuity/
  CREATIVE_BIBLE.md  STORYBOARD.md  project.json  README.md
```
Confirm `ffmpeg` and `python3` + Pillow are available.

**Early credit peek:** call Higgsfield `balance` once here, before generating any
image. Image assets (4 lead variants + 2 per supporting human + environments +
props) are spent *before* the full cost gate on the casting board — if the
balance already looks too thin for images + video + one retry, say so now and
agree on a smaller shape (fewer cuts / fewer characters) before spending.

**Create `project.json` immediately** (template in prompt-templates.md) and
update it after *every* completed step — every job id, chosen variant,
`element_id`, cut status, and QC result goes in the moment you have it. This
file is the resume point: a fresh session reads `project.json` +
`STORYBOARD.md` and continues from the first incomplete entry without
regenerating paid assets or re-asking the user for picks. **Before any
`show_reference_elements` create call, check the state file — an entity that
already has an `element_id` must NOT be re-registered.**

## 1. CREATIVE_BIBLE.md (do this before generating anything)

For each character capture: **name, personality (one comedic flaw), outfit + a
unique color, and exactly what's printed on the shirt** (use the character's name
— it's a great consistency anchor and an on-screen label). Define one **unified
style string** reused verbatim in every prompt — and **take it from what the USER
asked for; do NOT default to Disney / Pixar / 3D animation.** For real-looking
people use a photoreal/cinematic string, e.g.
`cinematic photorealistic, natural skin texture, soft natural daylight, shallow depth of field`.
Use a cartoon/3D style only when the user explicitly requests it.

**Decide the aspect ratio here and record it in `project.json`.** 숏폼/쇼츠/릴스/
틱톡/shorts/reels/vertical → `9:16`; cinematic/YouTube/TV → `16:9`; no platform
signal → `16:9`. The AR goes into every `gpt_image_2` call, every `seedance_2_0`
call, and the subtitle canvas (16:9 → 1280×720 / 9:16 → 720×1280 with
`--margin 190`). Never mix ratios — one 16:9 asset in a 9:16 project letterboxes
every composite. (`reframe` exists only to convert a *finished* video to another
ratio afterwards, not as a substitute for generating natively vertical.)

Write the beat sheet as N cuts of 15s, each with per-second beats and **2–3
short dialogue lines** (dialogue scenes; 1 line is a floor only for wordless
action cuts). For comedy, the engine is: same trigger → each character reacts
in-character differently.

**Dialogue-density check (mandatory before the storyboard).** Count the lines
in the source script against the runtime: a drama needs ≥2 spoken lines per
15s cut, and no shot longer than ~3s without a line or a physical action. If
the source is sparser (도어록 2026-09-18: 11 lines / 120s → "호흡이 너무 길다"),
run a **dialogue-augmentation pass** and record the choice in
`CREATIVE_BIBLE.md` + `project.json` (`pacing`): (a) add 1–2 short reaction
lines per cut that do not change the plot ("...네?", "잠깐만", "누구셔?"),
or (b) shorten the cuts (10s instead of 15s). Show the augmented beat sheet on
the casting board's STORY section so the user approves the extra lines with
the faces.

## 2. STORYBOARD.md + element matrix (mandatory — gate before any generation)

Break the beat sheet into per-cut shots, then build the **element matrix**: one
row per cut, columns = *characters | environment | props/products*, each cell
naming the exact Element tag the cut needs. This is the source of truth.

| Cut | Characters        | Environment    | Props / Products |
|-----|-------------------|----------------|------------------|
| 1   | `king`            | `shore_joseon` | `bottle`         |
| 2   | `king`,`minister` | `shore_joseon` | `bottle`         |
| 3   | `heroine`         | `beach_hawaii` | `bottle`         |
| 4   | `heroine`,`king`  | `beach_hawaii` | `bottle`         |

The **union of all cells** is the complete asset list for §3 — every character,
every environment, AND every prop/product. Do not start §3 until the matrix is
written; do not start §6 until every tag in the matrix has a registered Element.
Props/products are first-class here: if it appears in 2+ cuts, or it's the hero
object the plot revolves around, it gets its own Element. For a real product, the
Element MUST be the actual product image — never a generated lookalike
(registration mechanics for a real photo: §4).

**Blocking lock (블로킹 락) — for every scene spanning 2+ cuts in one location.**
Write ONE fixed spatial sentence per such scene (screen-LEFT/RIGHT per character,
facing direction, 180-degree-rule declaration — see prompt-mastery §3) here in
`STORYBOARD.md`, and record it in `project.json` under `scenes` so partial
re-renders reuse it verbatim. Every cut prompt of that scene must contain the
sentence unchanged.

## 3. Generate every asset the matrix names — one model: `gpt_image_2`

Submit all in parallel. **Every image asset — human characters, stylized/non-human
characters, environments, props/products → Higgsfield `gpt_image_2`** (or
`nano_banana_2`). **Every call MUST include `quality:"high"` and `resolution:"2k"`
explicitly — omitting `quality` silently falls back to low.** The asset type only
changes the variant `count` and whether there's an approval gate. Human / character
sheet:
```
params: { model:"gpt_image_2", resolution:"2k", quality:"high", aspect_ratio:"<AR from project.json>",
  count:4,   // PROTAGONIST: 4 variants. SUPPORTING humans (조연): count:2.
  prompt: "Character reference, single person, front-facing 3/4 body portrait
  centered, <UNIFIED STYLE>, clean neutral light-grey studio background. <PERSON:
  age, face, hair, expression, outfit + a unique colour>. Full clear face,
  flattering, consistent appealing design." }
```
(`gpt_image_2` is text-to-image here; the output PNG becomes the Element media in §4.
You can't pass `<<<id>>>` placeholders *into* a gpt_image_2 call — that's fine, we
only use its output as a reference image for Seedance.)

**Approval gate for every person:** make **4 candidates for each lead** and **2 for
each supporting human (조연)**, download them, and present them as a **casting board
(`casting_board.html`)** — one labelled grid covering everyone. **STOP until the user
picks one per character.** Only the chosen image becomes that character's Element in
§4. Non-human characters and one-off extras can be a single shot with no gate.

**Casting board (`casting_board.html`):** write a single HTML file in the project
root. One section per character (name/role heading); inside it, each candidate is a
card with a large number badge `①②③④` / `①②` in the corner. Dark board background, card
framing, responsive grid, and a caption telling the user how to answer
(`"주인공 3, 신하 1"`).

**Embed images as base64 — do NOT use relative `src`.** A relative path like
`characters/heroine_2.png` renders blank in preview/chat surfaces (the HTML is opened
outside its folder, so the PNGs don't resolve) — this is the most common "casting
board shows nothing" bug. Downscale each candidate to a ~800px JPEG and inline it as a
`data:image/jpeg;base64,…` URI so the board is one self-contained file that displays
anywhere:
```bash
# works for ANY variant count (leads have 4, supporting humans 2) — glob, don't hardcode 1..4
for p in characters/*_[0-9].png; do
  sips -s format jpeg -s formatOptions 80 --resampleWidth 800 \
    "$p" --out "/tmp/$(basename "${p%.png}").jpg" >/dev/null
done
python3 - <<'PY'
import base64, glob, os
def b64(p): return "data:image/jpeg;base64,"+base64.b64encode(open(p,'rb').read()).decode()
h = open('casting_board.html').read()
for png in glob.glob('characters/*_[0-9].png'):
    jpg = '/tmp/' + os.path.basename(png)[:-4] + '.jpg'
    if os.path.exists(jpg):
        h = h.replace(f'src="{png}"', f'src="{b64(jpg)}"')
open('casting_board.html','w').write(h)
PY
```
(Build the HTML with the relative `src` placeholders first, then run the inliner to
swap them for data URIs. Also send the JPEGs directly as a fallback.)

**Below the grid, add a "STORY" reference block**: a one-line
logline + the per-cut beat outline pulled from `STORYBOARD.md` (CUT 1~N — 장소 ·
등장인물 · 핵심 비트/대사 한 줄) so the user can weigh each face against the story while
picking.

**Below STORY, add a "COST" block — the cost gate.** Call Higgsfield `balance`
first and render a small table: remaining credits · planned spend (N × 15s
`seedance_2_0` cuts + storyboard preview + any remaining image assets) · the
cost of one single-cut re-render. State the headroom plainly ("4컷 + 재렌더
1회 여유" / "크레딧 부족 — 3컷 권장"). The user answers the casting picks and the
cut-count decision in one reply, *before* any Seedance spend. If credits can't
cover the plan plus at least one retry, propose the cheaper shape (fewer cuts
or shorter durations) as the recommended option.

Open the board (or send the file) and wait for the numbers. Reuse the same
file/numbering for any later re-pick.

**Non-human characters, environments, props/products → same `gpt_image_2`**
(or `nano_banana_2`), single shot, no gate:
```
params: { model:"gpt_image_2", resolution:"2k", quality:"high", aspect_ratio:"<AR from project.json>",
  prompt: "Character reference sheet, single character, front-facing 3/4 body portrait
  centered, <UNIFIED STYLE>, clean neutral light-grey studio background. <CHARACTER:
  face, expression, pose>. Full clear face, consistent appealing character design." }
```
Background: same style, "wide empty establishing shot … no people, clean
background plate for character animation".
Per prop/product (one clean reference per object in the matrix):
```
prompt: "Product reference, single object centered, <UNIFIED STYLE>, clean neutral
  light-grey studio background. <PROP: shape, material, colour, distinctive detail>.
  Clean product shot, consistent design."
```
(For a real product, skip generation — use its actual photo as the Element media.)

Each call returns a job id + `status:"pending"`. **Poll with `show_generations`
(type=image)** — it lists *completed* jobs with `results.rawUrl`. (`job_display`
sometimes reports `in_progress` even after completion — don't trust it for status;
use it only to re-render a known id.) Download the PNGs and *visually inspect*
them (Read the image) to confirm faces, readable names, and that each prop matches
how it must look on screen.

## 4. Register Elements (the consistency mechanism) — `show_reference_elements`

For **every** tag in the matrix — each character, each environment, each recurring
extra (the boss!), and each prop/product. **For every human character, register only
the ONE variant the user picked at the §3 gate** (lead chosen from 4, each 조연 from
2 — use that variant's `image_job` id):
```
action:"create", name:"king", category:"character",   // or "environment" / "prop"
medias:[{ id:"<image_job_id>", url:"<CloudFront rawUrl>", type:"image_job" }]
```
Save every returned `element.id` next to its matrix row. In later prompts, embed
`<<<element_id>>>` where that entity appears; the backend injects its reference
image and rewrites to `@name`. Multiple placeholders per prompt are allowed — a
cut that shows two characters in a place holding a prop has four placeholders.

**Registering a REAL photo (actual product shot, user-supplied image) — not a
generated job.** A local/user image has no `image_job` id, so upload it first:
`media_upload` (local file; follow with `media_confirm` if the flow requires it)
or `media_import_url` (already hosted). The upload returns a media id + URL —
pass those in `medias` with the `type` the upload response reports (it will not
be `"image_job"`; use the returned media type verbatim). Verify on first use:
render one cheap test image embedding the new `<<<id>>>` and confirm the real
product appears before committing any video spend. The same path uploads a
cut's extracted last frame for the continuity chain (§6a) — as a `start_image`
media for Seedance 2.5, or registered as a `continuity` Element on 2.0.

## 5. Storyboard keyframes — MANDATORY user OK gate before ANY video render

**Only images may be generated before this gate passes — no Seedance/video job
of any kind.** (User rule, 2026-07-06: "필요한 이미지만 만들고 스토리보드처럼 보고
→ OK 사인 후에만 영상".)

For **every cut**, generate ONE keyframe image — `gpt_image_2`, the project AR,
`quality:"high"`, `resolution:"2k"` — embedding that cut's Elements via
`<<<id>>>`: the cut's key moment, matching the scene's blocking lock. Then build
`storyboard_board.html` (same conventions as the casting board: base64-inlined
images, numbered `CUT` sections, each cut's beats + dialogue captioned under its
keyframe, and a cost table for the planned video renders), `open` it AND send it
via SendUserFile, then **STOP and wait for the user's explicit OK.**

Record in `project.json`: each keyframe's job id/file under `storyboard.keyframes`,
and the approval as `storyboard.approved: true` only when the user says OK. **On
resume, if `storyboard.approved` is not `true`, the gate has NOT passed — re-present
the board; never submit video.** If the user requests changes, regenerate only the
affected keyframes, re-present, and wait again.

## 6. Cuts — `seedance_2_0` (Seedance 2.0), `genre:"drama"`

Per cut, in parallel — **except chained cuts (§6a): a cut that continues the
previous cut's location/blocking is submitted only after that previous cut has
rendered and passed visual QC, because its opening frame comes from that render.**
Cuts from different scenes (or cuts that open on a new location) still run in
parallel. Seedance 2.0 honors `<<<element_id>>>` references for
identity/prop consistency, has a literal `genre:"drama"`, and bakes the characters'
**lip-synced dialogue** (sets `generate_audio:true` itself):
```
params: { model:"seedance_2_0", genre:"drama", duration:15, aspect_ratio:"<AR from project.json>",
  prompt:"CUT N (0-15초). <UNIFIED STYLE>, cinematic drama, emotional, moody
   dramatic lighting, filmic. <env: <<<shore_id>>>>.
   Focus on <<<charA_id>>> ... and <<<charB_id>>>, holding <<<prop_id>>>.
   0-5초: <beat + 한국어 대사 '...'>.
   5-10초: <beat + '...'>.
   10-15초: <beat>. 등장인물은 한국어로 말한다.
   edited as a multi-shot scene with motivated hard cuts between varied angles
   (establishing, two-shot, close-ups, reaction, insert) chosen naturally to fit the
   action and dramatic beats; dynamic cinematic coverage, consistent faces/props
   across shots.
   no background music, no BGM, no soundtrack — only spoken dialogue and natural
   diegetic sound." }
```
Drama is set with `genre:"drama"` AND reinforced in the prompt. Because Seedance
bakes spoken dialogue into the render, write the dialogue lines in the target
language and mix around the native audio in §8.

**Make each cut multi-shot, but let the AI direct it.** Don't pin shot types to
fixed second ranges — that reads stiff. The per-second beats describe action and
dialogue; the shot coverage is a *separate, open* instruction asking for varied
angles cut to standard film grammar, with the model deciding how many shots and
where the cuts land. Keep the same tagged Elements across the shots so faces/props
stay consistent through the angle changes. If the workspace has a dedicated multishot
video tool, prefer it; otherwise this prompt instruction is the lever.

**No BGM in the render (mandatory line in every cut prompt).** Seedance
auto-generates audio and will otherwise lay a *different* music bed under each 15s
clip; those beds jump/glitch at every concat seam (§8) and can't be cleanly stripped
out. Always end the prompt with the "no background music, no BGM, no soundtrack"
clause above so each cut returns dialogue + diegetic sound only. The soundtrack is a
single continuous track added once over the whole assembled video in §9 — never
per cut.

Rules:
- **Cross-check against the matrix:** before submitting, confirm the prompt
  contains a `<<<id>>>` for **every** entity in that cut's matrix row — characters,
  environment, AND props/products. A missing placeholder = guaranteed drift.
- **Language:** write the dialogue (ideally the whole prompt) in the target
  language (Korean lines → Korean speech).
- Tag every on-screen recurring entity (incl. props/products) with its `<<<id>>>`.
  Untagged = inconsistent.
- Keep each cut focused on 1–2 characters for strongest identity; the ensemble
  cut can include all of them. `duration` 4–15.

Poll via `show_generations` (type=video) → `results.rawUrl`; download to
`videos/cutN.mp4`.

### Audio note
- **Dialogue:** Seedance bakes the characters' lip-synced dialogue into the render
  and sets `generate_audio:true` itself, so spoken lines are in the cut's audio
  track. Check the first render to confirm the dialogue language and timing, then
  mix around that native audio (see §8). If a line is unclear, reinforce it with a
  subtitle (it's already on screen via §8 anyway).

### Error handling
- **"preset recommendation" notice** (no job submitted): resubmit the same call
  adding `declined_preset_id:"<preset id from the notice>"`.
- **"Invalid or expired token" / "server isn't responding"**: transient, just retry.

## 6a. Continuity chain — Anchor-and-Extend (mandatory for same-location consecutive cuts)

**When it applies.** Cut N+1 is *chained* to cut N when both are in the same
`scenes[]` entry (same location) and the story continues without a time jump —
the second half of a conversation, the next beat of an action, a reaction shot
in the same room. A 30s or 60s scene split into 15s renders is *always* a chain.
An Element locks *who* and *where*; it does not lock *the state things were left
in* — camera height, which hand holds the cup, the half-open door, who is
standing where. Without the chain Seedance re-stages every cut from scratch and
the assembled scene jumps at each seam even when every face is right.

**Do not chain** when cut N+1 opens somewhere else, after a time skip, or on a
deliberately different establishing angle — there the environment Element +
blocking lock (§2) are enough, and a start frame would fight the new staging.

**Steps, per chained cut (record every field in `cuts[N+1].continuity_ref`):**

1. **Wait for cut N** to reach `rendered` and pass the §6b *visual* check. Never
   chain off a cut that will be re-rendered — a stale anchor is worse than none.
2. **Extract the last frame:**
   ```bash
   bash scripts/last_frame.sh videos/cutN.mp4      # → continuity/cutN_last.jpg
   ```
   **Read the jpg.** It must be a clean, sharp frame with the state you want to
   carry (right people, right sides, right prop state). If it's black, fading,
   motion-blurred or mid-transition, step back: `LAST_OFFSET=0.5 bash
   scripts/last_frame.sh videos/cutN.mp4` (try 0.3 → 0.8) and Read again.
3. **Upload it** — `media_upload` (then `media_confirm` if the flow asks). Keep the
   returned media id + type; a local frame has no `image_job` id.
4. **Pass it to the render — the anchor is for STATE, the seam is hidden by a
   NEW ANGLE.** (Lesson from 도어록 2026-09-18: opening every cut on the
   previous cut's exact last frame with `start_image` produced a visible
   stutter at all 7 seams — the picture stops, re-animates from a still, then
   hard-cuts again. Viewer verdict: "툭툭 끊긴다".)
   - **Default — hard cut to a different angle at the seam.** Register the frame
     as a **continuity Element** (`show_reference_elements` create,
     `category:"environment"`, name `cutN_end`, `medias` = the uploaded media
     with its returned type) and tag it in the prompt with an explicit scope
     line: `<<<cutN_end_id>>> — continuity reference: location geometry,
     character positions and prop state only, not camera angle`. Then open cut
     N+1 on a shot that is NOT the previous cut's last shot — a reverse, a
     wider or tighter size — already mid-action or mid-line. An angle change
     is what makes a cut invisible; a matched still is what makes it stutter.
   - **Never end a cut on a static hold and never open one on a hold.** Cut N
     ends on a movement or the tail of a line; cut N+1 opens with that
     movement/line already in progress (Hell Grind dialogue-tail seam). No
     "Hold." as the last beat of a chained cut.
   - **`start_image` only for a true single continuous take** (a long tracking
     shot, a walk-and-talk that must not cut) → `seedance_2_5`,
     `mode:"omni_reference"` (**required** — with `mode` omitted the backend
     treats the call as t2v and rejects media with 422), `medias:[{value:"<media
     id>", role:"start_image"}]` plus the usual `<<<id>>>` tags (placeholders are
     still injected; the echo lists the media under `reference_images`). It pins
     the first frame pixel-close, so the previous cut MUST end mid-motion and
     the prompt must continue that motion in the first second — otherwise you
     get the stutter above. Expect ~1.5–2× the t2v render time. For an unbroken
     take across the seam, `mode:"video_extension"`, `extension_mode:"forward"`
     on the previous cut's video is the stronger tool (billed by the source
     video, ignores `aspect_ratio`, returns the extended video — re-trim before
     assembly).
5. **Anchor the prompt.** First line of the cut prompt, after the cut header:
   `Frame opens matching the final frame of CUT N: <one-sentence state summary —
   who is where (screen sides), facing which way, camera height/angle, prop
   state>.` Then paste the scene's blocking lock verbatim (§2) and carry any
   hand-off locks from cut N's POSITIVE LOCKS ("the faucet is still running").
   The **last cut of a chain** declares it: `This is the final clip of the scene
   — nothing follows it.` so the model resolves the beat instead of holding a
   hand-off pose.
6. **Record** in `project.json`:
   ```json
   "continuity_ref": { "source_cut": 1, "frame": "continuity/cut1_last.jpg",
     "offset": 0, "media_id": "<id>", "media_type": "<type from upload>",
     "role": "start_image | element | video_extension", "element_id": null }
   ```
   Set `"continuity_ref": null` explicitly on unchained cuts so a resumed session
   knows the decision was made, not skipped.

**Chain invalidation (partial re-renders).** If cut N is re-rendered for any
reason, every cut chained off it is stale: flip `cuts[N+1].status` back to
`pending`, re-extract the frame from the new cut N, re-upload, and re-render N+1
(and so on down the chain). Re-rendering only cut N and keeping the old cut N+1
re-creates exactly the seam jump the chain exists to prevent. The reverse is
free: re-rendering cut N+1 alone reuses cut N's existing anchor as is.

**Pacing rule for dialogue scenes (same 도어록 lesson).** A 15s cut carries
2–3 spoken lines, not 1. No shot longer than ~3s without a line or a physical
action. "She looks from A to B and back" is not a beat unless it is the punch —
cut it. Budget: 4 shots per 15s with dialogue in at least 3 of them. 120s of
drama with 11 lines reads as dead air; the chain seams make it worse.

**QC addition.** At §6b, for a chained cut compare its *first* QC frame against
`continuity/cutN_last.jpg` side by side — same sides, same prop state, same
camera height — and record the result in `cuts[N+1].qc.continuity`.

## 6b. QC gate — verify every cut before assembly (mandatory)

Run this on each cut *as it lands* (don't wait for all N). Checks per cut, all
recorded in `project.json` under `cuts[N].qc`:

**Visual check — frames vs. reference sheets.**
```bash
bash scripts/qc_frames.sh videos/cutN.mp4     # → qc/cutN/f01.jpg … f06.jpg
```
Read the frames side-by-side with the registered character sheets / prop shots
and confirm: same face per character (hair, outfit color, shirt text), same
prop (shape, material, label), environment matches its plate, unified style
holding, correct aspect ratio. **Blocking check** (multi-cut same-location
scenes): compare this cut's frames against the previous cut's — each character
still on the same screen side, facing the same way, per the scene's blocking
lock. A left-right swap between cuts is a QC fail even if every face is
perfect; record it in `cuts[N].qc.blocking`. **Continuity check** (chained
cuts, §6a): put `qc/cutN/f01.jpg` next to `continuity/cut(N-1)_last.jpg` — the
opening must match the anchor's sides, camera height and prop state; record in
`cuts[N].qc.continuity`. If a single frame is ambiguous
("is that the same bottle?"), run Higgsfield `video_analysis_create` on the cut
and ask it the specific question via `video_analysis_status`.

**Audio check — STT transcript.** Extract the audio and transcribe with
ElevenLabs `speech_to_text`:
```bash
ffmpeg -y -loglevel error -i videos/cutN.mp4 -vn -acodec libmp3lame qc/cutN_audio.mp3
```
From the transcript verify: (1) dialogue is in the target language, (2) the
scripted lines were actually spoken (paraphrase is fine; missing/extra lines are
not), (3) no music bed leaked in despite the no-BGM clause (music shows up as
long non-speech energy — if suspicious, listen/check the waveform). **Save the
word-level timestamps to `qc/cutN_stt.json`** — they drive subtitle timing in §8
and locate the real speech gaps for narration placement.

**Fail → regenerate NOW, not after assembly.** Typical causes map to fixes:
face/prop drift → a missing `<<<id>>>` (re-check the matrix row); wrong
language → rewrite dialogue in-language; music bed → strengthen the no-BGM
clause. Resubmit, re-QC, and only flip the cut to `rendered` in `project.json`
when both checks pass. Assembling around a bad cut costs a full re-assemble
later — never do it.

## 7. Sound effects + narration — ElevenLabs (parallel with the video renders)

**SFX are the only music-like layer at the per-cut stage — BGM comes later, once,
over the full video (§9).** Generate short cues for the action beats
(`text_to_sound_effects`) and save to `sfx/`:
```
text:"<short SFX description, e.g. 'magical sparkle poof', 'glass cork pop',
  'gentle ocean waves', 'whoosh throw'>", duration_seconds:<1–3>,
  output_directory:"<.../sfx>"
```
Make one cue per beat that wants punctuation (the transformation poof, the cork
pop, the throw whoosh, an ambient wave bed if a cut is silent). Keep them short;
they sit on top of the native dialogue, ducked slightly so dialogue stays clear.

**Narration** (`text_to_speech`): pick a voice with `search_voices` (e.g. a
Korean voice for Korean VO). Then:
```
text:"<short line>", voice_id:"<id>", model_id:"eleven_multilingual_v2",
language:"ko", stability:0.4, style:0.3, output_directory:"<.../narration>"
```
Keep narration SHORT — it can only live in the gaps between dialogue. Generate an
intro line (for the silent opening of cut 1) and maybe an outro; skip mid-cut VO.

## 8. Assemble — ffmpeg (see scripts/assemble.sh)

1. **Subtitle + narration timing comes from the §6b STT transcripts**
   (`qc/cutN_stt.json`): map each dialogue line to its first/last word
   timestamps and use those (±0.2s padding) as the overlay
   `between(t,start,end)` windows; narration goes only into the transcript's
   silence gaps. Fallback if STT failed on a cut:
   `ffmpeg -i cutN.mp4 -af silencedetect=noise=-30dB:d=0.4 -f null -` for gaps +
   scripted-beat timing (±0.5s tolerance).
2. Render subtitle PNGs: build `subs.json` ({id,text,type:dlg|narr}) and run
   `python3 scripts/gen_subs.py subs.json subs_png` — add
   `--w 720 --h 1280 --margin 190` for a 9:16 project.
3. One ffmpeg pass: audio = `[native dialogue]*1.0 + [SFX cues]*~0.7 placed with
   adelay on their beats (+ [narration]*1.4 delayed into gaps)` via
   `amix=duration=first:normalize=0`; video = subtitle PNGs overlaid with
   `enable='between(t,s,e)'`. **No BGM track in this pass.**
4. Concat the `cutN_final.mp4` with the concat demuxer → `FULL.mp4`.
5. *(§9, default)* Run the BGM pass: lay the Suno track at ~0.10 under everything
   and export `FULL_bgm.mp4` — the headline deliverable.

## 9. Background music — default final pass — `suno_generate_music`

BGM ships by default, but **never per cut** — one continuous track over the
*whole* video is the only way it stays seamless across concat boundaries. Run this
*after* `FULL.mp4` is concatenated (§8):
```
prompt:"<mood> instrumental for a <genre> ... no vocals, loopable, modern",
instrumental:true, model:"chirp-v5-5"
```
Aim for a **single track matched to the full runtime** (~1 minute for a 4-cut
video). Poll `suno_get_task`; it returns 2 takes of differing length — pick the one
closest to your total runtime. Download the mp3 to `music/`, then lay it across
the **already-concatenated `FULL.mp4`** (not the individual cuts), re-mixed UNDER
the existing dialogue+SFX at ~0.10, and export `FULL_bgm.mp4` — the headline
deliverable (keep the SFX-only `FULL.mp4` intact as a fallback).

**Length mismatch — handle it, don't ignore it** (assemble.sh has the recipe):
if the track is *shorter* than the video, loop it (`-stream_loop -1` on the music
input; `amix duration=first` trims to the video) — otherwise the music just stops
mid-video; if *longer*, it's trimmed automatically. Either way, end with a 2s
fade-out (`afade=t=out`) so the music never cuts off abruptly at the last frame.
For platform delivery, an optional final `loudnorm` pass (≈ -14 LUFS) evens the
overall loudness.

**Musical/choreography cut exception:** a cut rendered with baked-in music (the
seedance-cut-prompt musical recipe — uploaded music track, no no-BGM clause)
must NOT get the Suno bed on top. Duck the BGM to 0 over that cut's time range
with volume automation (e.g.
`volume=0.10:enable='not(between(t,<cut_start>,<cut_end>))'` on the [bg] chain,
plus short fades at the edges) instead of mixing at a flat 0.10 across the full
timeline. Note which cuts are music-baked in `project.json`.

## Deliver

Project folder with the N 15s `cutN_final.mp4`, the concatenated `FULL.mp4`, the
BGM-mixed **`FULL_bgm.mp4` (headline deliverable)**, character sheets, backgrounds,
props, storyboard, sfx, narration, `music/` (the Suno track), `qc/` (frames +
STT transcripts), bible, `STORYBOARD.md` (the element matrix), and a final
accurate `project.json` + README.

## 10. Optional final passes (offer after delivery, don't force)

- **Virality report — Higgsfield `virality_predictor`.** Run it on
  `FULL_bgm.mp4` (upload via `media_upload`/`media_import_url` if it needs a
  hosted asset) and summarize: hook strength in the first 3s, retention risk
  points, and 1–2 concrete edits (e.g. open on the cut-2 close-up, tighten the
  intro narration). If the user takes an edit, it's a normal partial re-render:
  update the affected cut(s), re-QC, re-assemble.
- **Multi-language versions — ElevenLabs `dubbing`.** Dub `FULL_bgm.mp4` per
  requested language → `FULL_bgm_<lang>.mp4`. Caveat: burned-in subtitles stay
  in the original language; for a real localized cut, translate `subs.json`,
  re-run §8 on the dubbed audio (STT the dub for timing), then re-lay BGM.

### Revising a prop/product or character later
If a prop, product, or character changes after some cuts are rendered: regenerate
its reference, create a NEW Element, and re-render **every cut in that entity's
matrix column** with the new `<<<id>>>` — not just the one cut you happened to
notice. The matrix tells you exactly which cuts that is; `project.json` holds
each cut's job ids and statuses — flip the affected cuts back to `pending`,
re-render, re-run §6b QC on them, and leave untouched columns (and cuts that
don't reference the changed entity) as they are to save credits.
The hero asset is `FULL_bgm.mp4`: consistent faces/props, in-language dialogue,
SFX, subtitles, and one continuous Suno BGM mixed low (~0.10) from the §9 pass.

## Provider fallback

Primary path is the Higgsfield MCP (its own credits, `gpt_image_2` +
`seedance_2_0` + Elements + `<<<id>>>`). If it hits a workspace credit/quota
limit, the Runway MCP offers `gpt-image-2` + `seedance-2` with `referenceImages`
`[{url,tag}]` and `@tag` in the prompt — same idea, different syntax. Check which
provider has credits with its balance/whoami tool before committing.
