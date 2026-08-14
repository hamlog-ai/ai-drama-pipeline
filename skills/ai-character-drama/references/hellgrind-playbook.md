# Hell Grind Playbook — 힉스필드 장편 검증 기법 이식판

출처: Higgsfield Studio "Hell Grind" (95분 장편, 15명, 생성 14일, 칸 2026 마르셰
상영) 공개 프로덕션 브리프 + CINEDANCE V4 스킬. 원문: `source/HELLGRIND-BRIEF.md`,
`source/CINEDANCE-HIGGSFIELD-SKILL.md`, `source/LIRA-SKILL.md`.
연기 시스템은 `acting-system.md`로 분리. 이 문서는 **자산 제작 · 프롬프트 기법 ·
편집 레인 · 운영 규율**의 이식판이다. 기존 규격과의 충돌 판정은 §7.

---

## 1. 캐릭터 시트 제작 (asset 단계 업그레이드)

- **시트 = 한 장에 3패널: 전신 앞모습 + 전신 뒷모습 + 얼굴 클로즈업을 나란히
  배치하고, 전신 앞모습은 머리가 없다(headless).** LIRA 원판의 side-by-side
  합본 구성에 Hell Grind가 headless를 얹은 것 — 낱장 3장으로 쪼개는 게 아니라
  한 이미지(16:9) 안에 3패널이다. 미친 소리 같지만 와이드 샷 얼굴 붕괴를
  통째로 고친 핵이다: 와이드에서 모델이 시트의 작고 흐린 전신 얼굴을 참조해
  버리는 문제 → 그 머리를 지우면 얼굴을 가져올 곳이 클로즈업 하나뿐이 된다.
  (기존 규칙 "시트에 얼굴은 정확히 하나"의 구현법이 이것이다.)
- **클로즈업은 3/4 뷰 대형 초상** (정면 직시가 아니라 살짝 돌린 얼굴) — 모델이
  가장 잘 읽는 시트 구성.
- **시트는 일부러 심심하게**: 뉴트럴 그레이 배경, 플랫 라이트, 보정 없는 모공
  보이는 진짜 피부. 필름 그레인·시네 렌즈를 시트에 구우면 캐릭터가 그 룩을
  모든 씬에 끌고 다니며 새 조명에 반응을 멈춘다. **시네마 룩은 시트가 아니라
  로케이션과 비디오 프롬프트에 산다.**
- **캐치라이트 검사**: 어두운 눈이라도 동공에 작은 빛 반사가 있어야 한다.
  없으면 죽은 얼굴 — 죽은 얼굴로는 어떤 비디오 모델도 연기를 못 시킨다.
  "예쁜 얼굴"이 아니라 "믿기는 얼굴"을 골라라 — 예쁘지만 가짜인 얼굴은 영상
  단계에서 가짜티가 터진다(그때는 못 고친다).
- **포인트 변경은 마스킹으로**: 의상·흉터·피는 편집 모델(NBP/Seedream)로 변경분만
  만들고, 마스크 지원 그래픽 툴에서 원본 위에 그 부분만 얹는다. 원칙:
  **이미지를 모델에 통째로 두 번 돌리지 않는다** — 패스마다 텍스처가 죽고 색이
  드리프트하며, 두 번이면 얼굴이 대칭·플라스틱·무생물이 된다.
- **스트레스 테스트 후 락**: 자산마다 다른 포즈·다른 조명으로 10회 생성 —
  10/10 알아볼 수 있어야 통과. 혼자가 아니라 **다른 자산 옆에서, 실제 씬 조명
  아래서** 테스트하라 (혼자 안정적인 캐릭터가 프레임을 공유하면 깨진다).
  실패하면 문제는 모델이 아니라 묘사다 — 워딩을 고치고 재테스트.
  (단편 4컷 프로젝트는 3~5회로 축소 가능; 10회는 장편 기준.)
- **상태마다 별도 자산**: 젖음·부상·의상 교체 = `@roco`, `@roco_wet`,
  `@roco_blood` 각각 등록 (기존 변형 Element 규칙과 동일). 소품도: 키 아이템은
  클로즈업용 풀 버전 / 손바닥 리빌용 소형 버전 / **"숨김" 버전**(보이는 건
  손가락 사이 빛뿐, 아이템 노출 금지 명시) 3종까지 분리. 상태 분리가 모델과
  싸우는 것보다 싸다.

## 2. 로케이션 제작

- **3/4 앵글로 촬영** (기존 규칙). 프레임에 **앵커 오브젝트**(기둥·램프·소파)를
  남기고 스테이징을 거기 묶어라: "the hero at the lamp, facing the door"는
  작동, "the hero in the room"은 복권.
- **광원 논리 하나**: 광원 1개, 그림자 방향 1개, 태양 2개 금지 — 아니면 새
  앵글마다 조명이 재발명된다.
- **역앵글 두 가지 방법**: ① 같은 방의 코너를 편집 모델로 생성 (원본의 소프트
  포커스에 맞춰서). ② **빈 로케이션을 카메라가 천천히 걸어 통과하는 영상을
  생성** → 필요한 앵글을 스크린샷 → 편집 모델로 텍스처·조명 보강. 이미지
  한 장에서 풀 로케이션 시트가 나온다. (제작 후반 발견한 고효율 핵.)
- **두 공간 전환은 문턱에서**: 두 로케이션 자산을 한 프롬프트에, 이음새는
  빛 대비가 있는 출입구 — "a warm amber room, a cold blue corridor beyond the
  arch". 대비가 팔레트 변화를 설명하고 작은 지오메트리 실수를 용서한다.

## 3. 군중·거인·스케일

- **군중 = 키·옷 범위를 가진 "캐릭터" 자산 1개.** 클로즈업 나올 리드 엑스트라
  1~2명만 개별 자산. 미디엄 샷엔 숫자 직접 명시("20+") — 안 쓰면 테이크마다
  3명↔100명.
- **거인/스케일 = 스케일 앵커 필수**: 등장하는 **모든** 프롬프트에 ①크기 비교
  ("his open palm is as wide as a family car") + ②측정 기준 인간 형상 + ③프레임
  증거 조건 ("the frame cannot hold both his feet and his head at once",
  "silhouette at least FIVE TIMES the height of the human figure"). 둘 다 없으면
  모델이 거인을 조용히 인간 크기로 되돌린다.

## 4. 비디오 프롬프트 기법 (CINEDANCE V4 + 브리프 증분)

### 4.1 GEO SPATIAL LAYOUT — 씬당 1회 작성, 전 컷 무변경 복붙

블로킹 락(문장 1개)의 확장판 — **장소의 평면도 블록**. 인물·액션 없이 장소만:
랜드마크, 좌우 배치, 카메라가 서는 쪽, 절대 안 넘는 선.

**발동 조건: 같은 장소가 2컷 이상이면 무조건 쓴다.** 인물이 2명뿐인 단순한
씬도 예외가 아니다 — 컷을 따로 생성하면 모델은 이전 컷의 카메라 위치를 기억하지
못하므로, 블로킹 락(인물 좌우)만으로는 **랜드마크와 카메라가 매 컷 재발명된다**
(2026-08 실측: 우물 2인 3컷에서 좌우는 지켜졌으나 우물이 미드그라운드 →
전경으로 이동, 카메라가 우물 주위를 공전). 블로킹 락은 **단일 컷 안에서만**
충분하다.

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— [랜드마크] = [무엇, 어디, 크기].
— [인물/오브젝트]: [랜드마크 기준 방향 + 거리(미터) + 몸통이 향하는 쪽].
— [랜드마크] IN FRAME: [프레임 어디에 놓이는지] + [금지 위치].
    예: "the well sits in the MIDGROUND in every wide and two-shot, rim at
    waist height; never in the foreground bottom of frame, never behind
    both characters."
— 180° AXIS: camera ALWAYS stays on the [X] side — it NEVER crosses the line
    and never orbits around [랜드마크]; closer shots move IN along the same
    axis, never around it.
— CAMERA BASE: [와이드/투샷을 찍는 거리 + 높이]; tighter shots move in along
    that same line.
— [광원 방향]: [어디서 오는지, 카메라 기준].
— [선택] ONE EXCEPTION: [축을 벗어나는 인서트가 있으면 여기에만 명시 —
    "it does not reposition the scene camera, every other shot returns to
    the [X] line"].
```

**IN FRAME과 CAMERA BASE가 이 블록의 핵심이다 (2026-08 추가).** 앞의 것이
"랜드마크가 전경으로 튀어나오는" 사고를, 뒤의 것이 "카메라가 랜드마크 주위를
도는" 사고를 막는다. 이 두 줄 없이 랜드마크·좌우·광원만 적으면 배치가 컷마다
흔들린다. 축을 벗어나는 인서트(톱다운 등)가 필요하면 **예외로 명시적으로 잘라라**
— 안 그러면 축 락 전체가 느슨해진다.

읽기 규칙: 좌우는 **카메라 기준만** ("frame-left/right" — 모델은 "주인공의
왼쪽"을 모른다). 위치는 랜드마크 기준 + 미터. 정적 대화엔 방 전체가
아니라 **방의 한 구석**을 줘라 — 공간이 좁을수록 모델의 선택지가 준다.
GEO는 지도일 뿐 — 장소의 룩은 여전히 로케이션 Element가 담당.

**STAGING THIS CUT — GEO 다음에 오는 별도 섹션 (필수).** GEO는 전 컷 무변경
복붙하는 **불변 지도**이고, 그 컷에서 누가 어디 서서 뭘 들고 어딜 보는지는
**컷마다 달라지는 상태**다. 둘을 한 블록에 섞으면 모델이 지도까지 컷마다
바꿔도 되는 것으로 읽는다. 분리해서 짧게 재명시하라 (모델은 이전 샷을 기억
못 한다):

```
STAGING THIS CUT
[인물 A] stands frame-LEFT at [랜드마크]'s left side, [그 컷의 손·자세].
[인물 B] stands frame-RIGHT at [랜드마크]'s right side, [그 컷의 소품 상태].
Same positions and distances as the map above.
```

### 4.2 첫 1초 와이드 규칙 (배치 고정 샷)

씬 첫 컷의 0~1초는 **대사·액션 없는 와이드**: 모델이 배치(누가 어디, 뭐가
어디, 빛이 어디서)를 "촬영"해 이후 샷에 유지한다. 이걸 빼면 캐릭터들이 자리를
바꾸기 시작한다. 핵 두 가지:
- 그 1초에 누군가 "hm" 같은 **짧은 한마디**를 시키면 Seedance가 와이드를 별도
  샷으로 다루기 쉬워진다.
- **직전 컷 대사의 꼬리를 첫 1초에 넣어라**: 배우가 맞는 톤으로 답하고 두
  클립이 이음새에서 붙는다. 새 컷은 직전 컷을 닫은 대사로 열어라 — 감정이
  텍스트와 함께 이음새를 건넌다. 비용 1초, 절약은 재촬영 몇 시간.

### 4.3 워딩 4규칙 (전 컷 공통)

1. **긍정형 액션만**: 모델은 "does NOT fall on his back"을 무시하거나 반대로
   한다 → "falls on his stomach". (비디오 락 블록의 "A, not B" 쌍은 예외적으로
   유효 — 기존 규칙 유지.)
2. **캐릭터는 첫 프레임부터 프레임 안에**, 요청 없인 카메라를 보지 않는다.
3. **나이를 쓰지 마라 (어떤 언어로도)** — 미성년 판독 순간 콘텐츠 필터가
   급격히 엄격해진다. 나이 대신 역할·의상·행동. (예외: 명백한 성인 —
   "in his 50s" — 은 정체성 앵커로 유효. 젊은/아동 캐릭터엔 절대 금지.)
4. **금칙어 사전 유지**: 모델이 벌주는 단어를 프로젝트 로그에 축적 —
   "dark"→"low key", "jolting"→"rapid motion". 거부당하면 사전에 추가.

### 4.4 캐릭터 수 헤더 + 가구 복제 금지

씬 컨텍스트 첫 줄에 **"EXACT N CHARACTERS — NO DUPLICATES: [이름들]"**.
모델은 사람을 추가하고 가구를 복제하길 좋아한다 — 참조가 프롬프트에 있는
사람만 존재하고, 소품 수는 직접 락: "exactly ONE mannequin, NEVER render a
second one." "FIVE smashed mannequins, never re-rendered as intact, never
multiplied."

### 4.5 시선·몸 방향 분리 락 (CINEDANCE)

몸 방향과 눈 방향은 별개다. 관계가 중요한 샷엔 둘 다 쓴다:
"torso faces X / eyes stay locked on X / head turns toward X / eyes reach the
door before the head turns". 약한 위치어 금지: near, around, beside, nearby →
**"within 1 meter", "touching", "hand on the handle", "back against the wall"**.

### 4.6 렌즈 결정 트리 (기존 3단 사다리의 상위 확장)

콘텐츠 유형이 렌즈를 고른다 (mm·조리개 대신 대각 화각° + 거리 + 가시적 결과):

| 콘텐츠 | 화각 |
|---|---|
| 친밀한 얼굴+환경 (Cuarón intimate-wide) | 84° / 카메라 1~1.5m |
| 미디엄 인물 | 29° / 4~6m |
| 타이트 감정 클로즈업 | 18~20° / 6~8m |
| 원거리 관찰 (파파라치/야생 다큐) | 8° / 20m+ — **전경 가림(foreground occlusion) 필수**: 하단 30~45%를 흐린 전경 보케가 차지 |
| 자연스러운 다큐 액션 | 47° / 3~5m |
| 와이드 환경 액션 | 84° |
| 대규모 지리 | 107° / 전경 0.5~0.8m |

- **망원 샷엔 가시적 결과 4개 이상** 명시: "background compressed flat",
  "razor focus on the subject", "creamy bokeh wash", "close framing achieved
  through lens reach, not physical proximity".
- **와이드 샷엔 3개 이상**: "foreground body presence looms larger",
  "deep edge-to-edge focus", "straight lines stay rectilinear".
- **콘텐츠-화각 정합**: 얼굴 인물 + 환경 지리 + 매크로 디테일을 한 비트에
  섞으면 렌즈 드리프트 — 콘텐츠 클래스가 다르면 컷을 나누고 샷마다 렌즈 배정.
- **멀티샷 렌즈 락**: 동일 렌즈 유지 시 "LENS IS X° ACROSS ALL SHOTS. NOT
  NEGOTIABLE." + 샷마다 열고 닫기(LENS LOCK / LENS CHECK).
- 금지: "extreme wide-angle lens" 같은 모호어, 렌즈 브랜드명·f값을 1차 제어로.

### 4.7 조명 우선 락 (장식이 아니라 제약)

콩트르주르(역광) 샷 표준 블록:
```
Subject stays between camera and the brighter background.
Camera stays on the shadow side of the subject.
Faces remain in deep shadow unless explicitly lit.
Only rim light, edge light, wet speculars, eye glints reveal detail.
No frontal key. No flat exposure. No beauty fill.
```
플랫하게 나오면 증축: "The entire shot is exposed for the backlight, not for
the face. The silhouette and rim contour carry the image." 광원마다 **동기**
명시 + 카메라가 광원의 어느 쪽인지.

### 4.8 컨텍스트 격리 (CINEDANCE 위생 규칙)

최종 프롬프트는 **밀봉된 현재-샷 문서**다. 금지: 씬 번호, 스크립트 헤더, 이전
씬 요약, 미사용 @태그, "previously / same as before / continues from / as
above", 이전 대사에만 등장한 인물. 모든 @태그는 이 샷에 보이거나 필요한
참조와 1:1 대응 — 스테일 태그는 최다 오염원이다.

### 4.9 복잡한 액션은 타이밍 중간에 안 둔다

문이 안 부서지던 문제의 해법: **액션이 프롬프트를 연다** — "he is ALREADY
mid-swing, the door ALREADY cracking". 문으로 다가가는 건 별도 컷.
(states-not-transitions의 샷 배치 버전.)

### 4.10 스타일 앵커 (콤팩트)

긴 시네필 체인 대신 압축 앵커: "Lubezki natural-light handheld", "Deakins
controlled silhouette", "Cuarón intimate wide", "Bergman profile face acting",
"Refn slow-walk minimalism". 스타일은 공간·광학·액션·조명 락 **뒤에** 온다 —
제어를 대체하지 않고 지원한다.

## 5. 이미지 편집 레인 (LIRA 이식)

우리 파이프라인은 생성을 `gpt_image_2`/`nano_banana_2`로 하지만, **완성된
프레임의 수정**은 편집 레인 규율을 따른다:

1. **모든 편집은 NBP(nano banana)급 편집 모델에서 시작** — 편집 = 원본의
   후처리 (원본이 베이스, 최소 변경).
2. **수술 편집 템플릿** (전 편집 공통):
```
Edit the image: [한 줄 목표].
CHANGE: [바뀌는 단 하나, 정밀하게].
PRESERVE EXACTLY:
- [동일해야 할 전부: 얼굴, 의상, 소품, 위치, 벽/바닥, 카메라 앵글, 기존 그림자]
- Color grade, palette, contrast, grain, falloff
ONLY CHANGE: [그 하나 재선언]. 100% identical otherwise.
```
   한 번에 한 변경. "너무 많이 바꿨다" = PRESERVE를 늘리고 CHANGE를 줄여라.
3. **텍스처 슬롭 → 텍스처 패스 전용** (Seedream류): 피부 모공·직물 짜임·표면
   질감 되살리기만. 포인트 편집은 절대 맡기지 않는다.
4. **프레임 재구축은 편집이 아니다** — 재생성으로.
5. **편집 프롬프트에서만 명시적 제거 허용** ("Remove the lamppost") — 항상
   채움과 짝으로 ("continuous brick wall behind"). 생성 프롬프트 부정문 금지는
   유지.
6. 로케이션 역앵글을 편집 모델로 시킬 땐 **새 오브젝트 배치를 명시적으로
   강제**: "In the main view the sofa is on the right; in this reverse view the
   sofa is on the LEFT" — 오브젝트마다. 안 쓰면 지오메트리가 뒤섞인다.
7. 프롬프트 길이: 이미지 생성은 80~150단어가 스위트스팟, ≤1500~2000자 상한 —
   과잉 절이 주의를 희석시켜 디테일이 떨어진다.

## 6. 운영 규율 (장편 검증)

- **자산 먼저.** 캐릭터·로케이션·소품 전부 락+스트레스 테스트 전엔 단 한 컷도
  생성하지 마라 — 이 규칙 하나가 나머지 전부보다 돈을 아낀다. (우리 파이프라인의
  스토리보드 OK 게이트와 동일 사상.)
- **매번 전부 묘사.** 모델은 기억이 없다 — descriptor는 모든 프롬프트에 word
  for word, 축약 금지. Style Prefix·GEO·블로킹 락은 상수로 관리: 한 번 수정하면
  전 샷 동시 업데이트.
- **한 번에 하나만 바꿔라.** 프롬프트는 작동하는 기계 — 전면 재작성하면 작동
  부분을 잃는다. 반복당 한 줄, 전부 로그로 (버전·변경·판정). 로그 없인 좋은
  샷을 재현 못 한다.
- **10~15회 룰**: 그 안에 샷이 안 나오면 문제는 워딩이 아니다 — **샷을
  단순화**하라: 둘로 쪼개고, 액션을 빼고, 앵글을 바꿔라.
- **모델에게 자유를 덜 줘라**: 방 대신 구석, 열린 공간 대신 앵커, 추측 대신
  지도, 샷당 액션 하나.
- **편집 페이스**: 생성물은 거의 항상 템포가 느리다 — 느낌보다 공격적으로
  자르고, 모든 클립의 **처음·끝 0.5초 트리밍을 계획**하라 (가장자리 드리프트).
- 클린업 우선순위: 얼굴·손 클로즈업 먼저, 전부 컬러 전에. 깨진 샷은 저장된
  최종 프롬프트에서 한 줄만 바꿔 재생성.

## 7. 기존 규격과의 충돌 판정

| Hell Grind 패턴 | 판정 |
|---|---|
| 기본 SINGLE CONTINUOUS TAKE + 명시적 컷 설계 (CINEDANCE) | **비채택 (대사 컷)** — 우리 대사 컷은 멀티샷 위임 유지 (숏폼 템포에 유리, 음절 예산과 공존). 구조 모드는 이미 HARD CUT 직접 설계 — 유지 |
| 프롬프트 3,000~4,000단어 | **비채택** — 장편 15초 R2V 멀티레퍼런스 전제. 우리 예산(대사 120~250 / 구조 400~600단어) 유지. 단 "길이가 아니라 과적된 비트가 적" 원리는 채택: 비트당 ≤3문장 |
| 캐릭터 수 헤더 (EXACT N) | **채택** — 콤팩트·구조 모드 양쪽 |
| GEO SPATIAL LAYOUT | **채택 — 같은 장소 2컷 이상이면 무조건** (2026-08 실측으로 상향). 최초 판정은 "단순 2인 씬은 블로킹 락 한 문장으로 충분"이었으나 반증됨: 2인 3컷에서 좌우는 지켜졌지만 랜드마크·카메라 위치가 컷마다 드리프트했다. 블로킹 락은 단일 컷 전용 |
| 첫 1초 와이드 + 대사 꼬리 | **채택** — 씬 첫 컷과 이음새 컷에 |
| 나이 금지 | **부분 채택** — 젊은/아동 캐릭터 절대 금지, 명백한 성인 나이대는 허용 |
| 시트 headless 전신 | **채택** — "얼굴 하나" 규칙의 구현법 |
| 시트에 스타일 굽기 금지 (boring sheet) | **채택** — 단 통일 스타일 문자열은 비디오 프롬프트에서 유지 (시트에서만 제외) |
| Voice 락 + 연기 프로필 | **채택** — acting-system.md, 바이블 단계로 |
| Style Prefix 상수 | **이미 있음** (통일 스타일 문자열) — Hell Grind 원문 프리픽스를 팔레트에 추가 |
| 렌즈 결정 트리 + 아웃컴 스택 | **채택** — 구조 모드 OPTICS 확장, 대사 컷은 축약 표기 유지 |
| 편집 레인 (NBP first, CHANGE/PRESERVE) | **채택** — §5 |
