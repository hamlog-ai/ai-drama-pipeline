# HELL GRIND — Higgsfield Studio 프로젝트 브리프 (전문 스크랩)

- 출처: https://higgsfield.ai/@higgsfield.studio/projects/hell-grind
- 스크랩 일시: 2026-08-06
- 개요: 95분 장편 AI 영화. 15명 제작, 예산 $500K 미만, 생성 14일. 2026 칸 Marché du Film 상영.
  전 프레임 생성 — 카메라·배우·세트 없음.
- 사용 모델: 영상·음성 Seedance 2.0 / 얼굴·로케이션 Soul Cinema / 이미지 편집 Nano Banana Pro, Seedream 4.5 / 프레임 내 텍스트·소품·역앵글 GPT Image 2
- 첨부 파일(사이트에서 별도 다운로드 필요): CINEDANCE HIGGSFIELD SKILL.md, ACTING SKILL.md, LIRA SKILL.md

---

## About the project

On the night of a museum heist, crew leader Roco brushes off his girlfriend Lulu before she can tell him she's pregnant. The job goes sideways: Roco triggers an ancient artifact that splits into four shards, granting the crew powers they can barely control — and summoning a bone-clad demon that drags Lulu into the underworld.

A stranger from a demon-hunting organization offers a deal: find the two remaining artifacts of the earth realm before the demons do, and they'll help bring Lulu home. In Tibet, Roco crosses a line — he kills the artifact's elderly guardian. A stolen memory reveals Lulu's pregnancy and that his friends hid it from him. Feeling betrayed, he continues alone. The third artifact, in Japan, demands a price no one should ever pay. By the time Roco opens the portal to hell, only one question remains: how much of the man who set out to save her will be left?

The numbers: Hell Grind is a 95-minute feature film created by 15 people. A budget under $500K. 14 days of generation — after the assets were prepared, and before the post work. The film screened in Cannes at the 2026 Marché du Film. Every frame is generated. No cameras, no actors, no sets. Video and speech: Seedance 2.0. Faces and locations: Soul Cinema. Image edits: Nano Banana Pro and Seedream 4.5. Text in frame, props and reverse angles of locations: GPT Image 2. The team: a director group plus prompt engineers, each responsible for their own block of scenes.

HELL GRIND began as a short series and grew into a feature. The process improved from scene to scene; the working formula came together near the end. This brief is that formula — the version we would use from day one.

Making the film meant solving a few big problems: faces that change between shots, spaces that fall apart when the camera moves, voices that drift, scenes that lose their geography. The biggest one is consistency — keeping every character, place and object the same from shot to shot. A video model has no memory. Describe your hero incompletely in one prompt — and in the next shot he has a different face and a different jacket. Below is the system that solved it, problem by problem.

A small spoiler: at the end of this brief you will find the CINEDANCE skill — our tool that writes video prompts by all of these rules for you. But for it to work at full strength, you first need to understand the system it stands on.

## Pre-Production: Assets

An asset is a simple pair: text + image. The text is a full description of the character or place — we call it a descriptor. It goes into every prompt, word for word. The image is a reference — the model uses it as an anchor. Together they keep your hero the same person from shot to shot.

**A character sheet is three images:** A close-up of the face, a full body from the front, and a full body from the back. And the front full-body figure has no head. This sounds insane, but it fixed a whole class of broken shots. On wide shots the model kept taking the face from the small full-body figure on the sheet — where the face is tiny and blurry. Remove that head, and the model has only one place to take the face from: the close-up.

**Faces were born in Soul Cinema.** It gives the best skin texture, but it is a creative model: one prompt returns several different versions of the face. Pick the most believable one, not the most beautiful one. A "beautiful but fake" face will show its fakeness later, in video — when it is too late to fix. And always check the eyes: even dark eyes need a small light reflection in the pupil (a catch-light). Without it the face looks dead, and no video model can act with a dead face.

**Keep the sheet boring on purpose.** Neutral grey background. Flat light. Real skin with visible pores, no retouch. The cinema look does not live in the character sheet — it lives in the locations and in the video prompts. Bake film grain and cinematic lenses into the sheet, and the character will carry that look into every scene and stop reacting to new light. One more thing we learned: the sheets the model understands best have a large portrait in 3/4 view (the face turned slightly, not straight-on).

**Clothes, scars and blood were added as point changes.** Our workflow: make the point change on the original character sheet in Nano Banana Pro or Seedream 4.5, then bring it onto the original by hand in any graphics editor that works with masks. The mask places only the changed part (the jacket, the scar, the blood) on top of the original; everything else stays untouched, so the original skin texture survives. The rule behind it: an image never runs through a model twice in full. Every extra pass destroys texture and drifts color — after two passes the face turns symmetrical, plastic and lifeless, and that dead texture later hurts the acting in video.

**Every asset passed a stress test before we locked it:** Ten generations in different poses and different light. The character must be recognizable in ten out of ten. And not alone — next to the other assets, and in the light of the real scenes ahead. A hero who looks stable alone often breaks when he shares the frame with someone. If the test fails, the problem is your description, not the model. Rewrite the words, test again.

**The voice is not an asset.** Seedance holds three or four voices per character inside one tonality — enough for a feature film, but only if you manage the voice. Lock every hero's voice in pre-production, before the dialogues: register, tempo, accent, manner. The voice prompt is pasted into the audio field as is, every time the hero speaks, and it never changes:

> Voice: deep, gravelly bass-baritone; slow, calculated pacing; London street accent; menacing calm — he never raises his voice.

Test how the voice holds between generations — the same way you stress-test the look; if it drifts, go back and lock the wording harder.

**The way a character acts is locked the same way as the look and the voice.** Every hero gets one paragraph — a behavior profile written before any shooting: how he moves, what his hands do, his nervous habits, how his eyes behave, how exactly he breaks under pressure. That paragraph is the source of truth: each scene adapts it to the moment's posture and action, but the core never changes. A behavior that is physically impossible in a scene is transferred, not deleted — a pacer sat down on a sofa keeps the same energy in swaying, finger-tapping and jagged gestures.

**Every state of a character is a separate asset.** Wet, wounded, changed clothes — that is @roco, @roco_wet, @roco_blood, each with its own description. Mix the states in one text, and the model starts mixing them between shots. Locations work the same way: day, night and rain are three different assets. Even props: our key artifact had three versions — a full one for close-ups, a small bloodied one for a brief reveal in a palm, and a "hidden" one for clenched-fist shots, where the prompt forbids showing the crystal and allows only blue light between the fingers. Splitting states is cheaper than fighting the model.

**Generate locations for your future camera angles.**
- Shoot the location sheet in 3/4, not frontal. A frontal "pretty picture" becomes flat wallpaper on wides, and past its edges the model invents new surroundings every time. A 3/4 view gives the model depth to read — it places the heroes correctly and covers almost a full circle of angles.
- Leave an anchor in every location — a column, a lamp, a sofa — and tie the staging to it. "The hero at the lamp, facing the door" works; "the hero in the room" is a lottery.
- Keep one light logic: one source, one direction of shadows, never two suns — otherwise every new angle re-invents the lighting.
- Reverse angles, way one: generate a corner of the same room in GPT Image 2 or Nano Banana, matching the soft focus of the original.
- Reverse angles, way two (found late in production): generate a video of the empty location where the camera slowly walks through the space — Seedance draws the other sides consistently with your sheet. Screenshot the angle you need, take it to Seedream or Nano Banana Pro, and prompt it to improve textures and lighting. A full location sheet out of a single image.

**When you feed assets to Seedance, name the role of every reference.** References are assets only: characters and locations. Name the role of each one right in the prompt — or the model decides by itself, and decides wrong: it copies the composition instead of the face, or the face instead of the color palette.

```
@roco for character reference
@jaxx for character reference
@loc_cave_front for location reference
```

Location references get a direct ban on inheritance: "do not use as a starting frame, do not inherit the composition, the angle or the color — take only the space and the texture." All assets live under tags — @roco, @loc_cave_front — and the same tags are used everywhere: in documents, in prompts, in the interface. One dictionary of names for the whole project.

## Pre-Production: Preparing prompts for Video

We wrote prompts together with Claude. It held the whole project folder in its context: the script, the asset sheets, the registry, the shotlists with @-tagged assets. Our standards are packed into skills. A skill is a playbook of rules that Claude loads by itself and then works by. There are three systems:

- **CINEDANCE** — video prompts (writer / auditor / workbench)
- **Lira** — image prompts: the same as CINEDANCE, but for images; it knows the weak points of every image model.
- **The acting system** — the living performance: how to write behavior instead of emotions, the face-and-body prompt hacks, the character acting master format.

### 프롬프트 스켈레톤 (The prompt is a rigid skeleton)

- SCENE CONTEXT — with the header "EXACT N CHARACTERS — NO DUPLICATES": what happens, who is in the shot, how long the take is.
- ACTIVE REFERENCES — character and location tags with their roles named.
- LOCATION MAP — the geography of the place in words.
- FIRST FRAME AND SPATIAL BLOCKING — who stands where in frame one.
- FORMAT MODE — one take or hard cuts, duration, real time.
- OPTICS — the lens and the focus plan.
- CAMERA — how the camera behaves, and what it never does.
- ACTION TIMING — the action beat by beat, in seconds.
- PHYSICS — weight, contact, inertia of everything that moves.
- LIGHTING — one source logic, where it comes from.
- AUDIO — the voice descriptors and the exact lines; SFX only.
- CHARACTER ACTING — state, want, what is hidden, body rhythm, what changes.
- STYLE — the Style Prefix, pasted word for word.
- QUALITY — detail and stability requirements.
- POSITIVE CONSTRAINTS — every count and ban, written as what IS in the frame

The character-count header is not a formality. The model loves to add extra people and to clone furniture. Only those whose references are in the prompt exist in the frame — and furniture gets a direct ban: "exactly ONE mannequin, NEVER render a second one."

### 실제 샷 프롬프트 전체 예시 (크루가 혼자 훈련 중인 ROKO를 발견하는 샷)

```
SCENE CONTEXT
EXACT 3 CHARACTERS — NO DUPLICATES: ROCO, JAX, REIN. Underground base, training hall, day. ROCO has
been drilling alone for hours; JAX and REIN come in late with food and find the room wrecked. One
continuous 12-second shot, no cuts.

ACTIVE REFERENCES
@roco for character reference — bare-chested, the crystal sheathing his right arm from wrist to
shoulder, blood dried under his nose.
@jax for character reference — carrying two food trays.
@rein for character reference — tablet in her left hand, screen alive.
@loc_training_room for location reference — take only the space and the texture: raw concrete, black
rock walls, the round mat, the hard light above it. Do not use as a starting frame, do not inherit
the composition, the angle or the grade.

LOCATION MAP
The round training mat sits at the center of the hall under one hard overhead light. The door is in
the far wall at frame-LEFT, about eight metres from the mat. Five smashed mannequins lie scattered
at CENTER-RIGHT, one still rocking on its base. A bench with two trays stands at frame-RIGHT, two
metres off the mat. The camera lives on the door side of the room and never crosses that line.

FIRST FRAME AND SPATIAL BLOCKING
First frame is already the full room: ROCO planted at the center of the mat, torso angled to
frame-LEFT, gaze down on the broken mannequins; the open door at frame-LEFT with JAX and REIN just
inside it, trays in hand, two metres apart. No empty establishing beat, no camera move on frame one.

FORMAT MODE
Single continuous take, 12 seconds, real time, no cuts, no speed ramps.

OPTICS
≈40° wide, camera low at chest height, six metres from the mat, deep enough focus to hold the door
and the mannequins in one read; the crystal arm stays sharp.

CAMERA
Calm breathing handheld that holds its framing — a slow reframe of a few degrees when ROCO turns his
head, nothing more. No push, no zoom, no whip.

ACTION TIMING
0.0–1.0s — the room holds: positions fixed, one mannequin still rocking.
1.0–4.0s — the door swings; JAX and REIN step in and stop at the edge of the mat, trays held.
4.0–8.0s — ROCO's eyes find them before his head turns; chest pumping in short pulls, the blood
untouched, the jaw setting once.
8.0–12.0s — he speaks; the smile cracks on all three at once; nobody steps toward anybody.

PHYSICS
The crystal arm has real weight — it drags the right shoulder low and swings a beat behind the body.
The rocking mannequin loses momentum and settles. Trays carry liquid: the cups tilt and steady when
JAX stops. Breath is audible work, not decoration.

LIGHTING
One hard overhead source above the mat: ROCO lit from above, eye sockets in shadow, the crystal
catching a cold edge; the door area falls two stops darker; no fill from the camera side.

AUDIO
Diegetic only — the hum of the hall, one mannequin creaking to a stop, footsteps and trays. ROCO
voice (verbatim): "A worn-out voice in his twenties, dry and low, humour used as armour." His line,
and nothing else: "You're late." Nobody else speaks. No music.

CHARACTER ACTING
ROCO — burnt out and still going; wants one more clean hit before anyone sees him fail; hides that
the arm is winning; heavy planted rhythm, slow recovery; re-arms his face when the door opens.
JAX — carries the reaction: the grin holds a half-beat too long, then drops as he reads the room.
REIN — reads the damage before the person: eyes sweep the broken mannequins, then the arm, then his
face; the tablet lowers without her noticing.

STYLE
[Style Prefix, pasted word for word]

QUALITY
8K detail, pore-level skin, no jitter, no flicker; the three faces stay exactly their references at
every distance.

POSITIVE CONSTRAINTS
Exactly three people in the hall, and no one else. Exactly ONE crystal arm, on ROCO's right arm,
wrist to shoulder — never on the left, never spreading past the shoulder. FIVE smashed mannequins,
never re-rendered as intact, never multiplied. Two trays, never more. The camera stays on the door
side of the room for all twelve seconds. Photoreal. NON-IP. 16:9. 12s. SFX only. NO CGI. Cinematic.
```

### 작성 규칙

Write in present tense. Short sentences. The camera is written inside the action. Keep each beat light: up to three sentences per beat — overload a beat, and the model smears it. The prompt itself can be long: ours ran 3,000–4,000 words. Length is not the enemy; an overloaded beat is.

Four more wording rules:
1. Actions only in positive form — the model ignores "does NOT fall on his back," or does the opposite; write "falls on his stomach."
2. The character is in the frame from the first frame, and never looks into the camera unless you ask.
3. Never write age in any language — the content filter becomes much stricter the moment it reads a minor; instead of age, give the role, the clothes, the action.
4. Keep a ban dictionary of words the model punishes: "dark" becomes "low key," "jolting" becomes "rapid motion."

### Style Prefix (모든 프롬프트 끝에 word for word 복사)

```
Style: 8K IMAX. Photorealistic — no 3D render, no game engine, no game-cutscene aesthetic.
Cinematography: floating immersive camera that lives with the actors; natural motivated light; painterly composed frames, strong silhouettes against the light.
Lighting: Natural light only — contre-jour backlight, camera on shadow side, atmospheric haze throughout. Key light from sky and windows only.
Color: 60:30:10 — dominant / secondary / accent.
Camera: Physical cine lens. 180° shutter motion blur.
Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
Acting: Hollywood — micro-pauses before reactions, precise eye-line, wet living eyes with catch-lights, visible breath and chest rise.
Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
Composition: Rule of thirds + golden ratio. Every person moving from frame one.
Continuity: Characters, props, environment identical across every cut. No identity drift.
Technical: 24fps smooth motion. 8K detail. No jitter.
Audio: Environmental SFX only. No music. No subtitles.
```

The line "SFX only. No music." is mandatory. Music belongs to post-production. Technical tags close the prompt: `Photoreal. NON-IP. [aspect ratio]. [duration]s. SFX only. NO CGI. Cinematic.`

### GEO SPATIAL LAYOUT (씬 지리 고정 블록)

가장 비쌌던 문제: 캐릭터 순간이동, 자리 바꿈, 카메라가 잘못된 쪽으로 점프. 원인: 모델은 이전 샷에서 누가 어디 섰는지 기억 못 함. 해결: 씬당 한 번 작성해 그 씬의 모든 샷에 무변경으로 붙여넣는 평면도.

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— PLATFORM = raised circular ritual stone disc at the edge of a cliff.
— ALTAR-MONOLITH: at the cliff edge, MID-RIGHT position relative to the platform.
— RITUAL CENTER: CENTER-LEFT, ~3 m from the altar.
— 180° AXIS: camera ALWAYS stays on the corpse-field side — it NEVER crosses the line.
— BACK-LIGHTING: crimson horizon glow comes from BEHIND the platform, rim-lighting silhouettes from camera's perspective.
```

- GEO는 지도일 뿐 — 장소의 룩은 여전히 로케이션 자산(descriptor+reference)에서 온다.
- 방향은 카메라 기준으로만: "frame-left"/"frame-right". 모델은 "주인공의 왼쪽"을 이해 못 함.
- 위치는 랜드마크 기준 + 미터 단위: "at the altar," "three meters away."
- 카메라가 어느 쪽에 서고 어떤 선을 절대 안 넘는지 직접 명시 — 모든 컷을 한 축에 유지.
- 컷마다 누가 어디 서서 어딜 보는지 다시 명시 (모델은 이전 샷을 기억 못 함).
- 정적 대화는 방 전체가 아니라 방의 한 구석을 줘라 — 공간이 좁을수록 모델의 선택지가 줄어든다.

### 첫 1초는 항상 와이드 샷

씬 시작 1초, 대사·액션 없이: 모델이 배치를 "촬영"해 이후 모든 샷에 유지. 이 1초를 빼면 캐릭터들이 자리를 바꾸기 시작함. 핵: 그 1초 동안 누군가 "hm" 같은 짧은 한마디를 하게 하면 Seedance가 와이드를 별도 샷으로 처리하기 쉬워짐.

와이드가 침묵일 필요는 없음 — 이전 클립 대사의 꼬리를 첫 1초에 넣으면 배우가 맞는 톤으로 답하고 두 클립이 이음새에서 붙는다:

```
FIRST FRAME AND SPATIAL BLOCKING
SHOT 1 (~1.0s) — a wide that FIXES THE POSITIONS and does nothing else: ROCO planted at the center
of the mat, five smashed mannequins at CENTER-RIGHT, the door open at frame-LEFT with JAX and REIN
one step inside it, trays in hand. No camera move, no action beat.

AUDIO
Over that first second, the tail of the previous clip's line arrives on REIN's lips as she walks in:
"...I've got the coordinates." ROCO's eyes find her before his head turns.

ACTION TIMING
1.0s onward — ROCO answers into the same rhythm, dry and worn: "You're late."
```

비용은 러닝타임 1초, 절약은 재촬영 몇 시간.

### 연기의 대원칙: 감정이 아니라 행동을 써라

살아있는 씬 = 주인공이 뭔가를 원하고, 방해물이 있고, 그것을 얻으려 행동한다. 감정은 그 싸움에서 저절로 태어난다. 목표와 장애물을 주고, 씬 내내 싸우는 방식을 바꿔라: 농담한다 → 실패 → 밀어붙인다 → 실패 → 애원한다. 각 변화는 눈에 보이는 사건: 멈춤, 자세 변화, 템포 변화.

**형용사가 아니라 물리를 써라.** "sad," "angry," "shocked" 같은 감정 단어에는 모델이 즉흥으로 얕은 결과를 냄. 깊은 감정은 근육과 몸의 일로 서술: 떨림, 분노로 악물리고 꿈틀대는 턱, 팽팽히 당겨진 광대, 코로 새는 가벼운 날숨. 근육 위에 의도를 얹기: 액션 구간마다 한 줄의 내적 독백 — INNER (unspoken) 표기. 단계적 눈 깜빡임 추가 — "one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink" — 살아있는 얼굴의 가장 값싼 신호. 명확한 시선 방향 또는 흔들리는 눈. 정적 샷의 얼어붙은 얼굴 방지 마이크로-라이프 규칙: 1~2초마다 하나의 가시적 미세사건 — 숨이 가슴을 들어올림, 콧구멍 움직임, 눈썹 긴장·이완. 정지는 동결이 아니라 유지된 긴장으로 서술 — "nobody moves" 같은 문구는 프레임 자체를 얼려버림.

실제 샷의 두 블록 예시 (몇 시간 훈련 후 혼자 있는 ROKO — "exhausted"와 "angry"라는 단어 없이 근육과 의도로 상태를 구축):

```
ACTION TIMING
0.0–2.0s — ROCO holds the center of the mat, feet planted wide, chest pumping in short shallow
pulls; the crystal arm hangs heavy at his side and drags his right shoulder a finger lower than the
left.
2.0–4.5s — the jaw sets and releases twice; a thread of blood runs from his nose to his upper lip
and he lets it run; one lazy blink, a quick DOUBLE-BLINK, one HARD reset-blink.
4.5–6.0s — the gaze drops to the smashed mannequins at CENTER-RIGHT, holds one beat, then lifts to
the door as it opens — the eyes reach the door before the head turns.

CHARACTER ACTING
ROCO — emotional state: burnt out and still going. What he wants in this moment: one more clean hit
before anyone walks in on him failing. What he is hiding: that the arm is winning, and that it
frightens him. Dominant body rhythm: heavy, planted, slow recovery between bursts. Visible habits in
this beat: the jaw set-and-release, the right shoulder pulled low by the crystal, the blood he does
not wipe, the gaze that finds the broken mannequins first and people second. What changes across the
shot: the second the door opens he re-arms his face — the exhaustion folds back behind a dry
half-smile before he says a word.
```

**살아있는 샷과 죽은 샷을 가르는 세 가지:**
1. 반응은 상대 대사가 끝나기 전에 시작 — 듣는 사람은 문장 중간에 요점을 알아채고 얼굴이 먼저 답한다. 중요한 사건 후에는 말하기 전 잠깐의 소화 시간을 줘라.
2. 감정은 즉시 꺼지지 않는다 — 무거운 순간 뒤 숨은 여전히 고르지 않고 손은 떨린다. 그 꼬리가 다음 클립으로 넘어가 컷들을 꿰맨다.
3. 주인공의 손을 바쁘게 — "대화를 나눈다"가 아니라 고치고, 세고, 따르며 그 위로 말한다. 씬의 가장 강한 악센트는 방금 들은 말 때문에 그 일을 멈추는 순간.

### 대사 라인 작성 공식

목소리와 감정 → 따옴표 속 대사 → 신체 동작 → 얼굴 반응. 대사는 프롬프트의 audio 섹션에만 — 액션에는 한 마디도 넣지 않는다. Seedance는 자기 마음대로 "uhm", 웃음, 문장을 추가하므로 하드 블록 필수: 모두가 따옴표 속 대사만 말한다; 대사 없는 사람은 완전히 침묵; 액션에 쓴 "half-laugh"는 소리 없는 표정. 믹스도 명시: 목소리는 깨끗하고 마이크에 가깝게, 앰비언스는 그 아래, 누가 말하면 앰비언스가 낮아진다. 희귀한 이름은 발음 표기를 주지 않으면 모델이 망가뜨린다. 이음새 트릭 2개: 대화 와이드 샷에는 직전 대사의 꼬리를 프롬프트에 넣기(입모양·리듬에 도움), 새 생성은 직전 생성을 닫은 대사로 열기(감정이 텍스트와 함께 이음새를 건넌다).

복도 씬의 2행 대화 예시 — 액션은 타이밍 블록에, 대사는 오디오 블록에, 둘은 절대 섞이지 않음:

```
ACTION TIMING
0.0–3.0s — JAX and REIN walk the corridor toward the lens, in step. JAX talks with his eyes up on
the ceiling lights, one hand patting his stomach; REIN's thumb keeps scrolling the tablet, her pace
unchanged, she never looks up at him.
3.0–4.0s — the distant THUD from the training room lands: REIN's thumb STOPS on the glass, and only
then her head turns to the door — the interrupted work is the accent of the beat. JAX's grin drops
half a second later.

AUDIO
Diegetic only — corridor air, two sets of footsteps on concrete, soft taps on the tablet, the
distant THUD and a hiss of crystal behind the door. JAX voice (verbatim): "A London street voice in
his twenties, loose and hungry, always half-joking, sentences thrown out mid-stride." His line, and
nothing else: "Man, some cereal and a milkshake would hit the spot right now." REIN voice (verbatim):
"A technical voice in her twenties — flat, fast, precise, no wasted air." Her line, and nothing else:
"I think I've got the coordinates." Nobody else speaks; JAX's amused breath is a facial expression,
with no sound. No music.
```

### 워크플로 운영

작업은 영화 순서대로 씬 블록 단위로 조직: 페인팅 프롤로그, 지옥 콜드오픈, 고아원 플래시백, 기지와 티베트 강탈, 일본 피날레. 블록마다 자체 샷리스트 파일. 모든 샷에 번호·타이밍·전체 프롬프트. Descriptor와 Style Prefix는 상수로 관리: 한 번 수정하면 모든 샷이 동시에 업데이트.

배치 생성, 씬 단위. 반복은 외과적으로: 한 줄만 바꾸고 나머지는 word for word 유지. 전부 로그에 기록: 프롬프트 버전, 변경 내용, 판정. 로그 없이는 좋은 샷을 재현할 수 없다. 10~15 규칙: 그 횟수 안에 샷이 안 나오면 문제는 워딩이 아니다. 샷을 단순화하라: 둘로 쪼개고, 액션을 빼고, 앵글을 바꿔라.

**데드라인 압박에서 태어난 해법들:**
- 복잡한 액션은 절대 타이밍 중간에 두지 않는다. 문이 안 부서지던 문제 → 액션이 프롬프트를 연다: "he is ALREADY mid-swing, the door ALREADY cracking" — 문으로 다가가는 건 별도 샷.
- 군중은 키·옷 범위를 가진 하나의 "캐릭터" 자산. 리드 엑스트라 1~2명만 클로즈업용 자체 자산. 미디엄 샷에는 숫자를 직접 명시 — "20+" — 안 그러면 어떤 테이크는 3명, 어떤 테이크는 100명.
- 두 공간 사이 전환은 문턱에서 유지: 두 로케이션 자산을 한 프롬프트에, 이음새는 빛 대비가 있는 출입구 — "a warm amber room, a cold blue corridor beyond the arch." 대비가 팔레트 변화를 설명하고 작은 지오메트리 실수를 용서한다.
- 거인은 스케일 앵커로 유지: 모든 프롬프트에 크기 비교 + 측정 기준이 될 인간 형상. 둘 다 없으면 모델이 거인을 조용히 인간 크기로 되돌린다:

```
POSITIVE CONSTRAINTS
THE SCALE LAW — VISIBLE PROOF IN THE PICTURE: the stone guardian stands THIRTY METRES tall — his head is lost in the darkness of the dome, his open palm is as wide as a family car, and ROCO at his foot reaches just above the ankle. In every frame the guardian's silhouette is at least FIVE TIMES the height of the human figure beside him, and the frame cannot hold both his feet and his head at once. A guardian that reads as a large man, or fits comfortably in frame next to a standing human = failed shot.
```

## Post-Production: Cleanup, Color, Sound

편집은 생성과 병행. 편집자가 도착하는 씬을 조립하며 부족분을 주문: "손 컷어웨이 필요," "더 와이드한 것 필요." 재촬영 비용이 몇 분이라 편집이 제작을 능동적으로 견인. 생성물은 거의 항상 템포가 느리게 느껴진다: 느낌보다 공격적으로 자르고, 모든 클립의 처음·끝 0.5초를 트리밍할 계획을 세워라 — 가장자리가 드리프트한다.

픽처 락 후 별도 클린업 패스. AI 소재는 작업 중엔 안 보이다 대형 스크린에서 보이는 결함을 거의 항상 가지고 있다: 여분의 손가락, "끓는" 텍스처, 간판의 가짜 텍스트. 작은 결함은 프레임 단위 리터치. 완전히 깨진 샷은 저장된 최종 프롬프트에서 한 줄만 바꿔 재생성. 1순위: 얼굴과 손 클로즈업. 전부 컬러 전에.

컬러는 통일부터: 모든 생성물이 자체 그레이드를 내장하고 도착하므로, 컬러리스트가 먼저 씬의 인접 샷들을 하나의 룩으로 맞춘다. 룩 자체는 프리프로덕션에서 로케이션 자산에 구워뒀다 — 컬러리스트는 발명이 아니라 정제.

목소리는 재녹음하지 않았다. Seedance의 립싱크 대사를 생성물에서 직접 클리닝: 노이즈 제거, 클립 간 음색 고르기, 공간에 목소리 배치. 사용 가능한 목소리가 없는 클립만 스튜디오 녹음. 사운드 디자인과 음악은 연속 앰비언스 위에 포스트에서 구축: 하나의 공유 대기가 생성된 샷들을 하나의 공간으로 붙인다.

## Conclusion — 5 rules

1. **Assets first.** 캐릭터·로케이션·소품 전부 락 + 스트레스 테스트 전엔 단 한 샷도 생성하지 마라. 이 규칙 하나가 나머지 전부보다 돈을 아낀다.
2. **Describe everything, every time.** 모델은 기억이 없다. Descriptor는 모든 프롬프트에 word for word, 절대 축약 금지.
3. **Change one thing at a time.** 프롬프트는 작동하는 기계다. 전면 재작성하면 작동하던 부분을 잃는다. 반복당 한 줄, 전부 로그로.
4. **Give the model less freedom.** 방 대신 구석, 열린 공간 대신 앵커, 추측 대신 지도, 샷당 액션 하나.
5. **샷이 안 나오면 워딩이 아니라 샷을 단순화하라.** 둘로 쪼개고, 액션을 빼고, 앵글을 바꿔라.

## What's attached (사이트 첨부물)

- The full production brief (전체 과정·결정·핵 상세)
- CINEDANCE skill bundle (writer / auditor / workbench) — 비디오 프롬프트 자동 작성 스킬
- Lira image-prompt skill
- Unified acting system (살아있는 연기 작성법: 씬의 5기둥, 프롬프트 핵, 캐릭터 연기 마스터 포맷)
- Team guide with learnings, 11-stage production pipeline, illustrated handbook with slop gallery, shotlists by block

> Note (원문): some assets and working files were lost during production — a few referenced materials may be unavailable or exist only in later versions.
