# Higgsfield Cinema Studio 구조 프롬프트 — 분석과 이식 가이드

출처: Higgsfield Cinema Studio 3.5 공개 프로젝트 "Cat Story" (2026-07 관찰, 클립
프롬프트 ~15개 + 동일 씬 리비전 버전 다수). 고양이→청년 변신 판타지 단편으로,
전 클립 무대사(SFX only) 15초, 클립 간 연속성이 극도로 빡빡한 프로젝트다.
관찰 목적: **구도·연속성·물리 묘사가 뛰어난 프롬프트의 구조를 우리 파이프라인
(Seedance 2.0 + Element)에 이식**하기 위함.

## 0. 두 방언 — 언제 어느 쪽을 쓰나

코퍼스에는 두 가지 프롬프트 방언이 섞여 있다:

| | 숏 방언 | 풀 구조 방언 |
|---|---|---|
| 형태 | 캐릭터 한 줄 + `[00-06s] Shot 1: ...` 비트 + 스타일 꼬리 | 12개 대문자 섹션 헤더 |
| 분량 | 150~250단어 | 500~800단어 |
| 쓰인 곳 | 사람 주연, 액션 단순, 연속성 요구 낮은 컷 | 동물 주연, 무대사, 클립 간 연속성 크리티컬한 컷 |
| 작성자 추정 | 사용자 직접 | 플랫폼 AI Director 생성 |

**판단 기준**: 대사가 있으면 숏 방언(음절 예산이 지배 제약이라 콤팩트해야 함).
무대사이고 (a) 이전 컷과 프레임 단위 연속이거나 (b) 공간 트릭(변신, 옷 뒤 통과,
아이리스 아웃)이 있거나 (c) 비인간 주연이면 풀 구조가 압도적으로 유리하다.

## 1. 풀 구조 12섹션 해부도

섹션 순서는 항상 동일하다. 각 섹션의 역할:

```
SCENE CONTEXT        ← 내러티브 요약 + 시퀀스 내 위치("Continuing directly from
                       Clip 3") + 샷 수 선언("Five shots, handheld throughout")
                       + 주어 수 선언("Single subject")
ACTIVE REFERENCES    ← 참조 이미지마다 역할 + 통제 범위 선언 (§2)
LOCATION MAP         ← 공간 지리 — 뭐가 어디에, 무엇 기준으로. 프레임 밖 공간의
                       연속성까지 ("the room continues toward the dollhouse")
FIRST FRAME AND      ← 첫 프레임의 정확한 상태. "Frame opens with the cat already
SPATIAL BLOCKING       mid-stride" — 항상 이미 행동 중간(mid-action)으로 연다
FORMAT MODE          ← 비율/해상도/카메라 유형(fixed·non-fixed·handheld)/샷 수/
                       오디오 정책("SFX only, no dialogue, no subtitles")/시퀀스
                       위치("This is the final clip — nothing follows it")
OPTICS               ← 샷별 렌즈 스펙 (§3) — 이 스킬이 배울 최대 포인트
CAMERA               ← 샷별 카메라 무브먼트 + 타임코드 (피사체 액션과 분리)
ACTION TIMING        ← 비트 타임라인. 샷 경계마다 "3.0s HARD CUT." 한 줄
PHYSICS              ← 자연 운동 제약 (§4)
LIGHTING             ← 샷별 광원 + 동기(motivated) + 안티 아티팩트 가드 (§5)
AUDIO                ← 앰비언스 + 폴리 비트 + "No dialogue, no music, no captions"
POSITIVE LOCKS       ← 최종 제약 블록 (§6) — 마지막에 다시 못박기
```

핵심 설계 사상 둘:

1. **카메라와 피사체를 분리 서술한다.** CAMERA 섹션은 카메라만, ACTION TIMING은
   피사체만 말한다. 같은 타임코드 체계를 공유하므로 모델이 둘을 합성한다.
   우리의 "비트 안에 샷 지시 박기"보다 간섭이 적다.
2. **같은 제약을 3번 말한다.** 샷 수는 SCENE CONTEXT, FORMAT MODE, OPTICS에서
   반복된다. 연속성 락은 LOCATION MAP에서 서술되고 POSITIVE LOCKS에서 재선언된다.
   중복은 낭비가 아니라 가중치다.

## 2. 레퍼런스 역할 분류 — identity / location / continuity

참조 이미지를 그냥 나열하지 않고 **역할 + 통제 범위**를 선언한다:

- `identity anchor` — 캐릭터/소품의 외형 고정. 범위 제한 가능:
  "Reference controls face, hair, and shirt only."
- `location reference` — 공간 기하 고정. 항상 범위 제한 동반:
  "Reference controls this furniture and the screen's proportions only,
  **not camera angle**." ← 이 한 절이 "참조 사진 구도를 복제하지 마라"를 해결
- `continuity reference` — **이전 클립의 마지막 프레임**을 참조로 넣고 시작 포즈·
  카메라 높이·소품 위치를 확인시킨다. 클립 체인의 접착제.

부분 신체 identity anchor도 쓴다: "identity anchor for the woman's **legs and
lower body**: sage-striped knee socks, black loafers, plaid skirt hem" — 발만
나오는 로우앵글 샷에서 전신 참조 대신 하반신 디테일만 계약한다.

**이식**: Element `<<<id>>>` 도입부에 역할+범위를 한 절로 붙인다.
`Location: <<<kitchen>>> (geometry only, not camera angle)`,
`<<<ella>>> — identity anchor, face/hair/dress only`.

## 3. OPTICS — 구도가 좋은 진짜 이유

샷마다 4요소를 수치로 준다:

```
Shot 3 (close, shadow growth): 20° diagonal field of view, tight close-up
character, camera 1 to 1.2 meters, positioned low and to the side of the
screen's lower third, an oblique angle deliberately avoiding a clean frontal
silhouette read.
```

1. **화각(도)** — mm 대신 diagonal FOV. 코퍼스의 3단 사다리:
   - `47°` ≈ 표준 렌즈(FF 50mm), 설정/트래킹/와이드
   - `29°` ≈ 준망원(FF ~85mm), 인물/압축("compresses the curtain gap gently")
   - `20°` ≈ 타이트 클로즈업(FF ~135mm), 얼굴/디테일
2. **카메라 거리(m)** — "camera 1.5 meters", "2 to 2.5 meters"
3. **카메라 높이** — "low camera height near floor level", "at the cat's eye level"
4. **실행 가능성 근거** — "room-feasible framing", "without exceeding the room's
   depth". 화각×거리 조합이 그 방에서 물리적으로 가능함을 명시 → 모델이 벽을
   뚫는 불가능 앵글이나 갑작스러운 초광각 왜곡을 안 만든다.

앵글에 **연출 의도**를 붙이는 것도 패턴이다: "an oblique angle deliberately
avoiding a clean frontal silhouette read" — 왜 이 각도인지 말하면 모델이 그
의도를 지키는 방향으로 프레이밍을 보정한다.

**이식**: 대사 컷에서도 샷 지정이 필요한 비트에는
`(29° FOV, ~1.5m, eye level)` 식 축약 표기를 붙일 수 있다. 무대사 구조 모드에선
OPTICS 섹션을 통째로 쓴다.

## 3.5 카메라 무브먼트 선택 문법 — 어떤 감정에 어떤 카메라인가

코퍼스 전체에서 무브먼트 선택이 일관된 규칙을 따른다. **카메라는 장식이 아니라
그 비트의 감정을 지시하는 두 번째 연기자다**:

| 무브먼트 | 쓰는 순간 | 코퍼스 표현 (그대로 재사용) |
|---|---|---|
| handheld (일상 sway) | 자연주의 관찰 — 캐릭터의 일상을 목격자처럼 따라갈 때. 판타지 트릭 장면일수록 오히려 핸드헬드 (다큐 질감이 트릭을 진짜처럼 만든다) | "handheld non-fixed camera, natural everyday sway and micro-shake" |
| handheld static-leaning | 긴장 홀드 — 뭔가 벌어지기 직전, 숨죽이고 지켜보기. 완전 고정보다 사람 숨결이 남아야 할 때 | "static-leaning hold, gentle natural breathing motion in the frame" |
| static locked-off | 관조·이별·데드팬 — 개입하지 않고 바라보는 시점. 떠나는 사람을 지켜보는 샷, 마지막 정리 샷, 무표정 유머 | "static locked-off over-the-shoulder frame, subject centered" |
| slow push-in / dolly-in | 감정 고조·의심·집중 — 인물의 내면으로 파고들 때. 피날레 강조 | "slow continuous push-in toward the face", "slow dolly-in, subject centered" |
| slow pull-back | 리빌 — 인물이 보고 있는 것의 규모·맥락 공개 (어질러진 방 전체 등) | "slow pull-back revealing the cluttered rug, the vanity, the bed in one continuous move" |
| tracking (subject 높이) | 이동 동행 — 피사체와 같은 눈높이로 나란히. 동물이면 카메라를 바닥 근처까지 내린다 | "low tracking shot following at the cat's eye level, camera moving parallel to the floor" |
| slow tilt-up | 올려다보기 동조 — 피사체가 뭔가를 올려다볼 때 카메라도 함께 | "slow tilt-up ending on a static frame, matching the upward gaze" |
| glide (low sweep) | 인서트 나열 — 바닥/테이블 위 물건들을 차례로 훑으며 정보 전달 | "a slow low glide sweeps across the scattered items, each held briefly in sharp close focus" |

운용 규칙 셋:

1. **줌 대신 푸시인.** 구조 방언은 광학 줌("zoom in")을 쓰지 않고 몸이 이동하는
   push-in/pull-back을 쓴다 — 줌은 AI 영상에서 워블·왜곡이 잘 생기고, 푸시인은
   공간감이 유지된다. 줌 어휘는 숏 방언(캐주얼 컷)에서만 관찰됨.
2. **한 클립 안에서 카메라 유형을 선언하고 유지한다.** FORMAT MODE에 "handheld
   throughout" 또는 "non-fixed camera"를 선언하면 전 샷이 그 질감을 공유한다.
   샷마다 tripod↔handheld를 오가면 클립이 조립품처럼 보인다.
3. **감정 곡선과 무브먼트 곡선을 맞춘다.** 코퍼스의 전형 시퀀스: 이동(tracking)
   → 도착·응시(static hold) → 사건(handheld) → 감정 정점(push-in) → 여운(locked-off).
   전 샷이 movement면 긴장이 안 쌓이고, 전 샷이 static이면 죽는다 — 교차가 리듬이다.

카메라 흔들림의 강도도 감정 지시다: 평온 = "subtle sway" → 다급/공포 =
"shaky handheld" (prompt-mastery §3 표 참조). 단 흔들림은 요청한 만큼보다 세게
나오는 경향이 있으니 기본은 "subtle/gentle"에서 시작하라.

## 4. PHYSICS 사전 — 자연스러움을 계약하는 문장들

동작마다 역학을 한 절로 명시한다. 코퍼스 빈출 표현 (그대로 재사용 가능):

- 보행: "natural weight transfer through hip and shoulder",
  "loose-limbed gait, weight shifting cleanly through the shoulders"
- 점프: "a clear crouch-launch-land arc with visible weight settling",
  "a brief balance correction on landing on the narrower ledge"
- 반복 동작 방지: "a small natural muscle motion, **not a mechanical repeat**"
- 소품: "the book is picked up with natural finger-and-palm grip, its weight
  visible in her wrist angle"
- 물: "water stream stopping instantly and residual drops falling under gravity"
- 천/부속물: "the backpack's straps shift slightly with each step, the pom-pom
  charm swaying and settling"
- 문: "swings on its hinge with natural resistance"
- 변형 통제: "a single sharp deformation completed within roughly two seconds,
  **no lingering intermediate creature stages, no slow morphing**"

**이식**: 컷에 신체 역학이 중요한 액션(점프, 소품 조작, 물, 천)이 있으면 비트
서술과 별도로 PHYSICS 2~3문장을 붙인다. "자연스럽게"라고 빌지 말고 역학을
계약하라 — prompt-mastery §0의 "몸으로 번역"의 물리 버전이다.

## 5. LIGHTING — 광원에 동기를 부여하고 아티팩트를 선제 차단

- 광원마다 **출처(동기)**를 명시: "motivated backlight — bright daylight flooding
  through the gap between the curtain panels", "warm tungsten practical glow"
- 역광 아티팩트 가드: "rim-lit at the edges **while fur texture remains visible
  on the camera-side — no full silhouette crush**"
- 감정 가독성 가드: "**visible catchlights**, readable expression"
- 조명이 연출 장치일 때 인과를 설명: "a shaft of sunlight grazes the screen at a
  low, raking angle, **which is what makes the shadow read as a soft bloom
  rather than a crisp silhouette**"
- 옵티컬 효과와 실제 조명의 분리: "the vignette is a black optical mask closing
  over the image, **not a change in the scene's actual lighting**"

## 6. POSITIVE LOCKS — 마지막 제약 블록

프롬프트 맨 끝에 그 컷이 깨질 수 있는 모든 방식을 락으로 재선언한다. 구성:

1. **주어 수 락**: "Exactly one subject throughout" / "Exactly one living subject
   on screen at any moment" (교대 등장도 커버)
2. **연속성 락**: 시작 상태("matching exactly where Clip 2 ended"), 공간 동일성,
   경로 제한("dollhouse-top to sill-ledge only — no other perch is used")
3. **트릭 실행 락**: "The transformation is never shown — no shadow, no screen,
   no visual morph; he goes in and the cat comes out **in one unbroken shot**"
4. **다음 컷으로 넘기는 소품 상태**: "The faucet is **still running** when this
   clip ends, carrying that detail into Clip 7"
5. **IP 가드**: "not a copy of any specific existing cartoon character or logo,
   purely the generic classic-cinema iris technique"
6. **스타일 서명 (전 클립 한 글자도 안 바뀜)**: "Fine 35mm film grain, warm pastel
   palette, Shunji Iwai soft-light aesthetic, sharp clarity, stable exposure,
   consistent frame rate." ← 우리의 통일 스타일 문자열과 동일 사상. 감독 이름
   (Shunji Iwai)을 룩 앵커로 쓰는 것도 유효했다.

부정문("not X")이 이미지 프롬프트와 달리 **비디오 락 블록에서는 대량 사용되고
작동한다** — 단, 항상 "A, not B" 쌍 형태다. 금지만 하지 말고 대안을 같이 준다:
"a clean, perfectly circular vignette **, not a rectangular wipe**".

## 7. 클립 체인 — Anchor-and-Extend

- 모든 클립의 FIRST FRAME은 **직전 클립의 마지막 프레임과 일치**하도록 서술되고,
  그 마지막 프레임 스크린샷을 continuity reference로 첨부한다.
- 시작은 항상 mid-action: "Frame opens with the cat **already** mid-stride."
  정지 상태에서 시동 거는 프레임 낭비가 없다.
- 마지막 클립엔 명시적으로 체인 종료를 선언: "This is the final clip — nothing
  follows it. No Anchor-and-Extend hand-off is needed after it."
- 소품 상태(수도꼭지 틀어짐)를 락으로 다음 클립에 인계한다 (§6-4).

**이식**: 우리 파이프라인에서 컷 N 렌더 후 마지막 프레임을 추출(qc_frames.sh)해
컷 N+1의 참조 Element로 등록하고, 프롬프트 첫 줄에 "Frame opens matching the
final frame of CUT N: <상태 요약>"을 넣으면 동일 효과.

## 8. 리비전 레시피 — 같은 씬 v1→v3에서 관찰된 실패→수정

코퍼스에 동일 씬의 리비전이 여러 벌 있어 수정 패턴이 그대로 보인다:

| 실패 증상 | 수정 (버전 diff에서 관찰) |
|---|---|
| 컷 후반에 방 인테리어가 다른 방으로 바뀜 | LOCATION MAP에 "this is still the same pink bedroom, only the corner not visible in the establishing shot; the pink wall color continues unbroken" + LOCKS에 "the room's interior design does not change at any point" + 마지막 샷에 기존 가구 5개를 이름으로 재나열 |
| 공간 지리가 복잡해 동선 붕괴 (복도) | **세계를 단순화**: "This is a small studio apartment: just the kitchen and her bedroom, directly connected, **nothing else**" — 프롬프트를 늘리는 게 아니라 세트를 줄인다 |
| 변신/모핑이 괴상하게 나옴 | 변신을 화면 밖으로: 문 뒤로 들어가고 다른 존재가 나오는 **one unbroken take** ("no cut, so the transformation reads as an in-camera trick rather than an edit"). 중간 단계 자체를 요구하지 않는 게 최선 |
| 그림자 실루엣이 이상한 중간 형태를 거침 | 두 갈래: (a) 그림자를 의도적으로 뭉갬 — 사광(raking light) 동기 + "never resolves into a clean silhouette, an indistinct growing blob" (b) 스냅 컷 — "a single abrupt transformation, no intermediate stages held on screen" |
| 창밖/배경이 매번 다른 도시로 나옴 | 외부 뷰도 location reference로 계약: "the exact view established in <ref> — low houses with dark tile roofs, a green hillside — **no generic or invented cityscape**" |
| 참조 사진의 어수선함이 그대로 복제됨 (정리된 방이어야 하는데) | 참조와 현재 상태의 차이를 명시: "The rooms are tidier than the photos in the references input, no clutter or trash" |

공통 원리: **재생성 전에 모델이 뭘 발명했는지 보고, 그 발명을 금지+대안 쌍으로
락에 추가한다.** 프롬프트 전면 재작성이 아니라 락 블록 증축이다
(prompt-mastery §7 진단→최소 수정과 동일 사상).

## 9. 우리 규격과의 충돌 — 뭘 가져오고 뭘 안 가져오나

| 힉스필드 패턴 | 이식 판정 |
|---|---|
| 12섹션 풀 구조 | **조건부** — 무대사 시네마틱 컷 전용 (구조 모드). 대사 컷은 기존 콤팩트 규격 유지 — 500단어 프롬프트에 대사 음절 예산까지 넣으면 립싱크 지시가 희석된다 |
| 레퍼런스 역할+범위 선언 | **전면 채택** — 몇 단어로 끝나는 고효율 패턴 |
| OPTICS 수치 (FOV°+거리+높이+근거) | **채택** — 구조 모드는 섹션으로, 대사 컷은 비트 내 축약 표기로 |
| HARD CUT 마커 + 샷 수 선언 | **채택** — 멀티샷 위임과 택일. 연속성 크리티컬 컷은 샷을 직접 설계(HARD CUT), 일반 컷은 위임 유지 |
| PHYSICS 섹션 | **채택** — 역학 중요 컷에 2~3문장 |
| POSITIVE LOCKS 블록 | **채택** — 기존 클로즈 3종(언어/멀티샷/no-BGM)을 락 블록의 일부로 흡수 |
| 카메라/액션 분리 서술 | **구조 모드에서만** — 콤팩트 규격에선 비트에 통합이 낫다 |
| "A, not B" 부정문 쌍 | **채택** (비디오 한정 — 이미지 프롬프트 부정문 금지는 유지) |
| 500~800단어 분량 | **비채택** — 무대사 구조 모드에서만 400~600단어까지 허용, 대사 컷 120~250단어 유지 |

구조 모드의 실전 규격은 seedance-cut-prompt 스킬의 "구조 모드" 섹션을 따른다.

## 10. 공식 확인 — CINEDANCE V4 (Hell Grind, 2026-08)

힉스필드가 장편 "Hell Grind"와 함께 공개한 공식 프롬프트 시스템 CINEDANCE V4
(`source/CINEDANCE-HIGGSFIELD-SKILL.md`)가 이 문서의 관찰을 공식 확인했다 —
12섹션 골격, OPTICS 화각° 체계, 역할 선언 레퍼런스, POSITIVE LOCKS 전부 동일
사상. 관찰판(이 문서)에 없던 **공식 증분**은 `hellgrind-playbook.md` §4에 이식:

- 렌즈 결정 트리 (콘텐츠 유형→화각) + 망원/와이드 가시적 결과 스택 + 안티드리프트 락 (§4.6)
- 시선·몸 방향 분리 락 + 약한 위치어("near/beside") 금지 어휘 (§4.5)
- GEO SPATIAL LAYOUT — 씬당 1회 작성해 전 컷 복붙하는 공간 평면도 블록 (§4.1)
- 첫 1초 와이드 배치 고정 + 직전 대사 꼬리 이음새 (§4.2)
- EXACT N CHARACTERS 헤더 + 가구 복제 금지 락 (§4.4)
- 컨텍스트 격리 규칙 — 스테일 @태그·씬 번호·"previously"류 금지 (§4.8)
- 조명 우선 락 (콩트르주르 표준 블록) (§4.7)
- 컷 타입 어휘 확장: HARD/SMASH/MATCH/INSERT/REVERSE/WHIP CUT (fade/dissolve는
  요청 없인 금지 유지)
- 캐릭터 묘사 공식: `@TAG: 나이대(성인만)+역할/체형+현재 상태+가시 앵커+액션
  크리티컬 소품. 100% matches the reference.` — 참조가 진실의 원천, 과잉 산문으로
  덮어쓰지 않는다
- 밀도 제어 원칙: 정체성 앵커·블로킹·첫 프레임·광학·조명·물리엔 고밀도,
  장식 형용사·참조에 이미 명백한 디테일엔 저밀도 — "개선은 신호 강화지 增量이 아니다"
