# Prompt & manifest templates

> Templates are the skeleton — **how to fill the blanks well is defined in
> `prompt-mastery.md`** (beat budgets, dialogue limits, camera grammar, face
> anchors, self-review rubric). Read it before filling any template.

Fill the `<...>` slots. Keep the **unified style string** identical everywhere.
`<AR>` = the project aspect ratio from `project.json` (`16:9` or `9:16`) — same
value in every image call, every video call, and the subtitle canvas.

**Every `gpt_image_2` call that uses these prompts MUST pass `quality:"high"`,
`resolution:"2k"`, `aspect_ratio:"<AR>"` in params — omitting `quality` silently
defaults to low.**

## Unified style (reuse verbatim in every image & video prompt)

Take this string from **what the USER asked for** — do NOT default to Disney /
Pixar / 3D. Write it once and paste it verbatim into every image & video prompt.

```
<유저가 요청한 비주얼 스타일을 한 줄로>, <조명>, <컬러 그레이딩>, <AR>
```

Examples (pick the register the user wants, then fill in):
```
# 실사 드라마 (16:9)
cinematic photorealistic live-action, natural skin texture, soft natural daylight,
shallow depth of field, warm color grade, 16:9
```
```
# 세로형 숏폼 (9:16) — 쇼츠/릴스/틱톡이면 이쪽
cinematic photorealistic live-action, natural skin texture, soft natural daylight,
shallow depth of field, warm color grade, 9:16 vertical framing, subjects centered
in the vertical safe area
```
```
# 유저가 명시적으로 카툰/3D를 원할 때만
modern 3D animated sitcom, stylized character, soft cinematic studio lighting,
clean expressive faces, warm color grade, <AR>
```

## Character sheet (gpt_image_2)

```
Character reference sheet, single character, front-facing 3/4 body portrait centered,
<UNIFIED STYLE>, clean neutral light-grey studio background. <NAME>: <face, hair,
expression>, <signature pose>. Wears a <COLOR> crew-neck T-shirt with a large bold
clean readable '<NAME>' logo printed across the chest. <one personality cue>. Full
clear face, consistent appealing character design, high detail.
```

## Background plate (gpt_image_2)

```
Wide empty establishing shot of <PLACE>, <UNIFIED STYLE>, soft <time-of-day> light.
<key props/furniture>. No people, clean appealing background plate for character
animation, high detail.
```

## Element registration (show_reference_elements, action=create)

```
name:"<short_tag>", category:"character" | "environment" | "prop",
medias:[{ id:"<image_job_id>", url:"<rawUrl>", type:"image_job" }]
```
(Real photo instead of a generated job — actual product shot, user image: upload
first via `media_upload` / `media_import_url`, then register the returned media
id + url with the `type` the upload response reports, not `"image_job"`. See
workflow §4.)

## Video cut (seedance_2_0) — write dialogue in the target language

```
CUT <N> (0-15초). <UNIFIED STYLE>, <genre>. <장소 <<<env_id>>>>.
<focus chars: <<<a_id>>> (간단 묘사), <<<b_id>>> (간단 묘사)>.
<BLOCKING LOCK — 같은 장소 2컷+ 씬이면 필수, 씬 내 모든 컷에 동일 문장:
<<<a_id>>> on screen-LEFT facing right, <<<b_id>>> on screen-RIGHT facing left;
all shots stay on the same side of the action axis (180-degree rule);
they never swap screen sides between shots or cuts.>
0-5초: <행동 + 대사 '<KOREAN LINE>'>.
5-10초: <행동 + 대사 '<KOREAN LINE>'>.
10-15초: <행동/리액션>. 등장인물은 한국어로 말한다. 표정 풍부한 코미디, 빠른 타이밍.
영화 문법에 맞춰 다양한 앵글(설정샷·투샷·클로즈업·리액션·인서트)을 자연스럽게 하드컷으로 편집한 멀티샷 장면.
샷 수와 컷 타이밍은 AI가 액션/감정 비트에 맞게 알아서; 태그된 Element로 얼굴·소품은 일관 유지.
no background music, no BGM, no soundtrack — only spoken dialogue and natural diegetic sound.
```
(The trailing no-BGM line is mandatory: Seedance auto-generates audio, so without it
each 15s cut gets a different music bed that glitches at concat seams. BGM is added
once over the whole concatenated video in workflow §9, never per cut.)
(The BLOCKING LOCK line is mandatory whenever the same location spans 2+ cuts:
Elements lock faces, not positions — without a verbatim-repeated blocking sentence
Seedance restages every cut and characters flip screen sides between cuts. Keep the
exact same sentence in every cut of the scene; store it in project.json per scene.)

## Storyboard keyframe — one per cut (gpt_image_2, the §5 OK gate)

One image per cut, project AR, `quality:"high"`, `resolution:"2k"`, embedding the
cut's Elements — the cut's key moment, staged per the scene's blocking lock:

```
CUT <N> keyframe. <UNIFIED STYLE>. <장소 <<<env_id>>>>. <<<a_id>>> <action at the
cut's key moment>, <<<b_id>>> <reaction/position>, holding <<<prop_id>>>.
<BLOCKING LOCK sentence if the scene has one.> Single cinematic frame, no panels,
no captions.
```

The keyframes go on `storyboard_board.html` (casting-board conventions) for the
**mandatory user OK** — no video render before `storyboard.approved: true`.

## subs.json (input to scripts/gen_subs.py)

One entry per subtitle line. `type:"dlg"` = spoken (white), `"narr"` = narration
or on-screen label (warm yellow). The `id` maps to the overlay PNG used in
assemble.sh (e.g. c1a/c1b/c1c = cut 1's three lines).

```json
[
  {"id": "c1a", "text": "〔 평범한 아침 〕",               "type": "narr"},
  {"id": "c1b", "text": "[대표]  내일 아침까지 완성!",       "type": "dlg"},
  {"id": "c1c", "text": "[GPT]  네! 당연하죠!",            "type": "dlg"},
  {"id": "c2a", "text": "〔 …말없이 폭풍 타이핑 〕",         "type": "narr"},
  {"id": "c2b", "text": "[CLAUDE]  잠깐, 어떤 사용자를 위한 거죠?", "type": "dlg"}
]
```

## Subtitle timing convention — STT first

Primary: take each line's window from the cut's STT transcript
(`qc/cutN_stt.json`, produced at the QC gate) — first word start −0.2s to last
word end +0.2s. Dialogue lines sit exactly on their spoken words;
narration/label lines sit in the transcript's silence gaps. Fallback (STT
failed): time to the scripted per-second beats; ±0.5s vs the AI lip movement is
acceptable there.

## project.json (state file — create at step 1, update after every step)

```json
{
  "title": "<project title>",
  "aspect_ratio": "16:9",
  "style": "<unified style string, verbatim>",
  "language": "ko",
  "cut_duration": 15,
  "credits": { "checked_at_step": "casting", "balance": null, "planned_spend": null },
  "elements": {
    "king":         { "kind": "character", "variant_jobs": ["<job1>","<job2>","<job3>","<job4>"],
                      "picked": 3, "image_job": "<picked job id>", "url": "<rawUrl>",
                      "element_id": "<id>" },
    "shore_joseon": { "kind": "environment", "image_job": "<id>", "url": "<rawUrl>",
                      "element_id": "<id>" },
    "bottle":       { "kind": "prop", "image_job": "<id>", "url": "<rawUrl>",
                      "element_id": "<id>" }
  },
  "scenes": [
    { "id": "shore_scene", "cuts": [1, 2],
      "blocking_lock": "<the scene's fixed spatial sentence, verbatim — pasted unchanged into every cut prompt of the scene>" }
  ],
  "storyboard": {
    "keyframes": { "1": { "image_job": "<id>", "file": "storyboard/cut1.png" } },
    "board": "storyboard_board.html",
    "approved": false
  },
  "cuts": [
    { "n": 1, "matrix": { "characters": ["king"], "environment": "shore_joseon",
        "props": ["bottle"] },
      "video_job": "<seedance job id>", "file": "videos/cut1.mp4",
      "status": "pending | rendered | qc_failed | final",
      "qc": { "visual": null, "blocking": null, "language": null,
              "lines_spoken": null, "no_bgm": null, "stt": "qc/cut1_stt.json" } }
  ],
  "assembly": { "full": null, "full_bgm": null, "bgm_track": null },
  "optional": { "virality_report": null, "dubs": [] }
}
```

Rules: an entity with a non-null `element_id` is NEVER re-registered; **no video
job is ever submitted while `storyboard.approved` is not `true`** — on resume,
if it's false/missing, re-present the board and wait for the OK; a cut only
moves to `final` after all QC checks pass; on resume, work starts at the first
`pending`/`qc_failed` entry.

## QC checklist (run per cut at the §6b gate, record in project.json)

```
VISUAL (qc_frames.sh → Read frames vs. reference sheets)
[ ] each character: same face, hair, outfit colour, shirt text as their sheet
[ ] each prop/product: same shape, material, label as its reference shot
[ ] environment matches its plate; unified style holding; correct aspect ratio
[ ] blocking (same-location 2+ cut scenes): screen sides + facing match the
    previous cut and the scene's blocking lock — no left-right swap
AUDIO (speech_to_text on the cut's audio)
[ ] dialogue in the target language
[ ] every scripted line spoken (paraphrase ok, missing/extra lines not)
[ ] no music bed leaked in (no-BGM clause held)
→ any [ ] fails: fix prompt (usually a missing <<<id>>> / language / no-BGM
  clause), regenerate the cut, re-QC. Do not assemble around a failed cut.
```
