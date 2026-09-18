---
name: seedance-cut-prompt
description: 각본/대본의 특정 씬(S#N)을 Seedance 2.0/2.5용 영상 컷 프롬프트로 변환한다 — 대문자 헤더 구조 모드 단일 규격(SCENE CONTEXT~POSITIVE LOCKS), 15초 3비트·대사 음절 예산·DIALOGUE 블록, Element 태그 참조, no-BGM 클로즈, IP 세이프 네이밍, 2.5 확장 규격(월드 스타일 프리픽스·★LOCK★·EVENT TRACK)까지 규격대로. 사용자가 "S#N 영상 프롬프트 줘", "이 씬 시댄스/Seedance용으로", "영상 프롬프트로 바꿔줘", "15초 컷으로 만들어줘"라고 하거나, 생성한 프롬프트가 "정책위반/policy violation/protected content"로 거부됐다고 할 때 반드시 사용한다. 프롬프트 텍스트만 원하는 경우에 쓰고, 실제 영상 생성·조립까지 원하면 ai-character-drama 스킬로 넘어간다.
---

# Seedance Cut Prompt (대본 씬 → 영상 프롬프트 변환)

각본의 씬 하나를 Seedance 컷 프롬프트로 변환한다. 산출물은 **프롬프트 텍스트 + 호출 파라미터 + 사전 준비물(Element별 완성 이미지 프롬프트 포함)** 3종 세트. 실제 렌더/전체 영상 제작은 `ai-character-drama` 스킬의 영역이다 — 그쪽으로 넘어갈 땐 이 스킬로 만든 프롬프트를 그대로 들고 간다.

**규격은 구조 모드 하나다 (2026-08 개정 — 콤팩트 규격 폐지).** 대사 유무와 무관하게 모든 컷을 구조 모드(아래)로 쓴다. 폐지 근거 두 가지: ①힉스필드 스튜디오 실전(Cully Hill Boys 123컷)이 대사 컷 포함 전 컷을 이 구조로 감 — 멀티샷 위임 없이 샷을 직접 설계. ②자체 A/B 실측 — 대본이 특정 샷(우물 수면 리플렉션, 손목 인서트, 톱다운 등)을 요구할 때 콤팩트의 멀티샷 위임은 그 샷을 평범한 투샷·클로즈업으로 뭉갰고, 구조 모드는 `20° tight insert, 0.6m above the well mouth angled down`으로 정확히 뽑았다. 대사 컷은 구조 모드에 **DIALOGUE 블록**을 더하고(아래 대사 규칙), 1인칭(POV) 컷·격투/추격 컷은 **특수 컷 레시피**(아래 섹션)를 겹쳐 적용한다.

**납품 전 필수: 셀프리뷰 루브릭 통과.** 이 스킬의 예산·블로킹 수치는
`ai-character-drama/references/prompt-mastery.md`의 요약본이다 — 프롬프트를
사용자에게 주기 전에 그 문서의 셀프리뷰 루브릭(§6)을 실제로 순회하고, 걸리는
항목은 고친 뒤에 납품한다. 두 문서의 수치가 어긋나면 prompt-mastery.md가 원본이다.

## 대사 규칙 (전 컷 공통 — 구 콤팩트 규격에서 승계)

콤팩트 규격은 폐지됐지만, 그 안에서 실측 검증된 대사 도구는 전부 승계한다. 구조 모드 안에서의 배치: **대사 전문 → DIALOGUE 블록** (화자별 전달 톤 + 따옴표 원문), **발화 타이밍 → ACTION TIMING** (대사 원문은 넣지 않고 "he delivers line 1" 식 참조만), **보이스 descriptor·환경음·no-BGM → AUDIO**, **화자 락·입 다묾 → POSITIVE LOCKS**. 모든 대사 컷의 AUDIO에 언어 클로즈("등장인물은 한국어로 말한다")와 no-BGM 클로즈("no background music, no BGM, no music track, no soundtrack — only spoken dialogue and natural diegetic sound (<장면에 맞는 환경음 예시>)")와 캡션 클로즈("no captions, no subtitles, no on-screen text")를 반드시 넣는다. **이 두 클로즈는 대사 유무와 무관하게 모든 컷 공통 필수다 (2026-08-30 사용자 지시).**

**첫 1초 규칙 (씬의 첫 컷 + 이음새 컷).** 씬 첫 컷의 0~1초는 대사·액션 없는
**배치 고정 와이드**: 모델이 누가 어디 서고 빛이 어디서 오는지 "촬영"해 이후
샷에 유지한다 — 빼면 캐릭터들이 자리를 바꾼다. 그 1초에 "hm" 같은 짧은
한마디를 시키면 Seedance가 와이드를 별도 샷으로 다루기 쉽다. 직전 컷에 이어지는
컷이면 **직전 대사의 꼬리를 첫 1초에** 넣어라 ("Over that first second, the tail
of the previous clip's line arrives: '...'") — 배우가 맞는 톤으로 답하고 두 클립이
이음새에서 붙는다. 비용 1초, 절약은 재촬영 몇 시간. 단, 꼬리 대사의 화자가 이
컷에 안 나오면 **오디오 격리 가드**를 함께 쓴다: "Prior audio context only, not
visual content: '...'" — 안 쓰면 모델이 직전 화자를 프레임에 그려 넣는다
(CINEDANCE).

**대사 라인 공식.** 목소리 descriptor(verbatim) → 따옴표 대사 → 신체 동작 →
얼굴 반응 순. 캐릭터별 Voice 프롬프트는 바이블에서 락하고 매 컷 한 글자도 안
바꾸고 붙인다 (`ROCO voice (verbatim): "A worn-out voice in his twenties, dry
and low." His line, and nothing else: "..."`). 하드 블록 동반: 모두가 따옴표 속
대사만 말한다, 대사 없는 사람은 완전 침묵, 액션의 "half-laugh"는 소리 없는 표정.

**대사 타이밍 룰 (CINEDANCE).** 필요할 때만 골라 쓴다:

- **즉시 발화** — 이어지는 컷에서 대사가 바로 시작해야 하면: "The line begins
  within the first 0.3 seconds." (씬 첫 컷에는 쓰지 않는다 — 첫 1초 규칙이
  우선.)
- **침묵 버퍼** — 편집 여유가 필요하면: "At least 1 second of silence before
  and after each spoken line." 컷 경계에서 대사가 잘리는 사고를 막는다.
- **클린 믹스** — 환경음이 시끄러운 장면의 대사엔: "Ambient sound ducks under
  dialogue; the voice stays close, clean and emotionally controlled."

## 예산 (넘기면 품질이 무너진다)

- **15초 = 3비트, 비트당 물리적 액션 1개** + (선택) 대사 1줄. 밀도가 아쉬우면 액션 대신 리액션 샷.
- **대사: 컷당 ≤3줄, 줄당 ≤15음절, 화자 ≤2명, 구어체.** 한국어 발화 속도 초당 5~6음절 기준 — 초과하면 립싱크 붕괴. (DIALOGUE 블록에도 그대로 적용.)
- 감정은 컷당 하나. 대사엔 연기 부사("flat and deadpan", "whispers")를 붙인다.
- 추상어 금지: "감동적으로/멋지게" → 몸으로 번역 ("her smile switches off like a light").
  감정 단어("sad/angry") 대신 **근육으로**: 악물렸다 풀리는 턱, 단계적 깜빡임("one lazy
  blink → DOUBLE-BLINK → HARD reset-blink"), 코로 새는 날숨 (acting-system.md).
- **긍정형 액션만**: "does NOT fall on his back" → 무시되거나 반대로 나온다 →
  "falls on his stomach". (POSITIVE LOCKS의 "A, not B" 쌍만 예외.)
- **나이 금지**: 젊은/아동 캐릭터 나이는 어떤 언어로도 쓰지 않는다(필터 급강화) —
  역할·의상·행동으로. 명백한 성인 나이대만 허용.
- **금칙어 사전**: 거부당한 단어는 프로젝트 로그에 축적해 치환한다 — "dark"→"low
  key", "jolting"→"rapid motion".
- 초 타이밍은 리듬 가이드일 뿐 — Seedance는 정확한 초를 못 지킨다. 순서와 비중만 전달된다.
- 샷 스펙(화각·거리·높이)은 OPTICS/CAMERA 섹션이 담당한다 — ACTION TIMING 비트 안에 스펙을 중복 기재하지 않는다.

## Element 규칙

`<<<id>>>`는 장식이 아니라 **등록된 참조 Element의 자리**다. 2컷 이상 나오거나 플롯 중심인 캐릭터/환경/소품은 전부 Element로 등록돼야 하고, 말로만 묘사하면 컷마다 다르게 나온다. 프롬프트를 줄 때 반드시 "사전 준비물" 섹션에 필요한 Element 목록을 함께 명시한다.

**사전 준비물은 요약 가이드가 아니라 완성 이미지 프롬프트로 준다.** 생성해야 하는 Element(캐릭터 시트·로케이션 플레이트·소품 샷)마다 사용자가 **그대로 복붙해 돌릴 수 있는 영어 이미지 프롬프트 전문**을 첨부한다 — "나이/얼굴형/헤어 앵커를 넣어라" 같은 지시문만 주고 끝내지 않는다 (원본 규격: `ai-character-drama/references/prompt-mastery.md` §2). 작성 규칙:

- **절 순서**: `[샷 타입/구도] → [주제 + 구체적 시각 앵커] → [배경] → [디테일 꼬리]`. 가장 중요한 것이 맨 앞.
- **캐릭터 시트**: "character reference sheet, single character"로 시작. 단
  **포토리얼 프로젝트에서 일러스트/컨셉아트풍으로 드리프트하면** "character
  reference sheet"가 트리거일 수 있다 — "film character sheet" / "three studio
  photographs of the same person"으로 치환 (LIRA 규칙: "painterly"도 같은 트리거) + 나이대/얼굴형/헤어(스타일·길이·색)/**위치가 특정되는 구별 특징 2~3개**(점·안경·흉터·보조개) + 의상(색+소재+특이점 1개). "beautiful/handsome" 금지 — 목표는 distinctive. 한국인이면 "Korean" 명시. **뉴트럴 그레이 배경 + 플랫 라이트** — 필름 그레인·시네 렌즈 등 통일 스타일 문자열은 시트에 굽지 않는다(비디오 프롬프트 전용). 프레임에 얼굴 하나. 본격 멀티컷 프로젝트면 **한 장짜리 3패널 합본 시트**(16:9 — headless 전신 앞 | 전신 뒤 | 3/4 얼굴 클로즈업을 나란히, 얼굴은 클로즈업 하나만)로 확장 — 확장 규격은 prompt-mastery.md §2.
- **로케이션 플레이트**: wide + empty + 캐릭터가 들어갈 여백 + 시간대 조명 명시 + **3/4 앵글**(정면 플랫 금지). "no people"은 예외적으로 허용되는 표준 태그.
- **소품 샷**: 단일 오브젝트, 중앙, 뉴트럴 스튜디오 배경, **재질·라벨·마모 상태**까지 — 재질이 빠지면 컷마다 재질이 바뀐다.
- **부정문 금지** (플레이트 "no people" 예외). 이미지 모델은 언급된 것을 그린다.
- 프롬프트 옆에 생성 파라미터도 표기: `gpt_image_2, quality "high", resolution "2k"`, AR(3패널 합본 시트 16:9, 단독 클로즈업만 쓸 땐 1:1 또는 3:4, 플레이트는 프로젝트 AR).
- continuity reference처럼 **생성이 아니라 업로드**로 만드는 Element는 이미지 프롬프트 대신 추출·업로드 절차를 명시한다.

**역할 + 통제 범위를 선언하라.** Element를 나열만 하지 말고 셋 중 하나의 역할과 적용 범위를 한 절로 붙인다:

- `identity anchor` — 외형 고정. 범위 제한 가능: `<<<ella>>> — identity anchor, face/hair/dress only`. 발밑 로우앵글 샷이면 하반신만 계약하는 부분 앵커도 가능 ("legs and lower body only: striped socks, black loafers").
- `location reference` — 공간 기하 고정. **항상 "geometry only, not camera angle"을 붙인다** — 안 붙이면 참조 사진의 구도까지 복제한다.
- `continuity reference` — 직전 컷의 마지막 프레임. 시작 포즈·카메라 높이·소품 상태를 잇는 접착제 (구조 모드 참조). 추출은 `ai-character-drama/scripts/last_frame.sh`, 업로드는 `media_upload`(로컬 프레임은 image_job이 없다). **투입 방식은 이음새 종류로 고른다**: 같은 샷이 그대로 이어지면 Seedance 2.5 `start_image`(첫 프레임 픽셀 고정 — 이때 프롬프트 첫 비트는 그 프레임 그대로를 서술해야 하고 다른 오프닝 앵글을 요구하면 안 된다), 앵글이 바뀌는 하드컷이면 continuity Element로 등록하고 범위를 "location geometry, character positions and prop state only, not camera angle"로 제한. 전체 절차는 `ai-character-drama/references/workflow.md` §6a.

참조 사진과 씬의 현재 상태가 다르면 차이를 명시한다: "the room is tidier than the reference photo, no clutter."
스케일은 미터보다 **인물 대비**가 강할 때가 있다: "a longbow taller than she is" — 절대 치수 대신 상대 비교로 잠그면 드리프트가 준다.
**배경 인구도 앵커하라**: 엑스트라의 인종·민족을 명시하지 않으면 서구 얼굴이 디폴트로 나온다 — "지나가는 행인들의 얼굴은 한국인이다" 한 줄이면 잠긴다 (사란 파쿠르 런 실측).

**변형은 별도 Element로 잠근다.** 의상·상태가 바뀌는 캐릭터는 시트를 변형마다 따로 만들어 각각 등록한다 (`<<<ella>>>` 평상복 / `<<<ella_ballgown>>>` 드레스 / `<<<ella_soaked>>>` 비 맞은 상태). 한 시트로 "드레스 입혀줘"를 텍스트로 시키면 드리프트가 난다 — 컷 프롬프트에서는 그 컷의 상태에 맞는 변형 Element만 참조한다. 컷 안에서 의상/상태 변화가 불가능한 것과 같은 원리다.

**시트에는 얼굴이 정확히 하나.** 참조 시트 프레임 안에 얼굴이 2개 이상 보이면(분할 패널의 클로즈업+전신 등) 영상 모델이 어느 얼굴에 락할지 몰라 드리프트가 난다. 중복 얼굴은 시트 단계에서 지워라.

**location reference는 3/4 앵글로.** 정면 플랫 샷 참조는 카메라가 움직이는 순간 공간이 붕괴한다 — 깊이가 읽히는 3/4 앵글 참조가 무빙을 버틴다.

**블로킹이 텍스트로 안 잡히면 스키매틱 맵.** 소품·인물 배치가 복잡해 블로킹 락 문장으로도 위치가 흔들리면, 배치를 그린 약도 이미지를 만들어 참조로 첨부한다 — "Text can't hold a location down; a map can."

## 블로킹 락 (같은 장소가 2컷 이상 이어지면 필수)

> ⚠️ **블로킹 락은 단일 컷 안에서만 충분하다 (2026-08 실측).** 같은 장소를
> **컷을 나눠서 따로 생성**하면 블로킹 락은 인물의 좌우만 지키고 **랜드마크와
> 카메라 위치는 매 컷 재발명된다** — 우물이 컷1에선 미드그라운드, 컷3에선 화면
> 아래 전경으로 튀어나오는 식. 인물이 2명뿐인 단순한 씬도 예외가 아니다.
> **같은 장소가 2컷 이상이면 블로킹 락 대신 GEO SPATIAL LAYOUT을 쓴다**
> (`ai-character-drama/references/hellgrind-playbook.md` §4.1). 아래 블로킹 락은
> 한 컷 안의 좌우 고정용, 또는 GEO의 인물 항목을 채우는 재료로 읽어라.

Element는 얼굴을 고정하지 위치를 고정하지 않는다. 같은 장소의 연속 컷을 뽑으면서 블로킹을 컷마다 다르게(또는 느슨하게) 쓰면 Seedance가 매 컷 배치를 재발명해 **인물의 좌우가 컷마다 뒤바뀐다** — 얼굴이 완벽해도 이어 붙이면 장면이 붕괴한다. 해결은 씬 단위 **고정 블로킹 문장 하나**를 만들어 그 씬의 모든 컷 프롬프트에 한 글자도 안 바꾸고 넣는 것. 문장에 반드시 포함:

1. 화면 기준 좌우 — "screen-LEFT / screen-RIGHT" (인물 기준이 아니라 화면 기준)
2. 바라보는 방향 — "facing right / facing each other"
3. 축 유지 선언 — "all shots stay on the same side of the action axis (180-degree rule); they never swap screen sides between shots or cuts."

예: *"<<<king>>> sits screen-LEFT facing right; <<<minister>>> stands screen-RIGHT facing left; all shots stay on the same side of the action axis (180-degree rule); they never swap screen sides."* 샷 설계와 충돌하지 않는다 — 앵글은 OPTICS/CAMERA가 정하되 축과 좌우는 이 문장이 못박는다. 여러 컷을 연속으로 뽑을 때 "사전 준비물"에 씬별 블로킹 락 문장도 함께 명시해 사용자가 컷마다 복붙하게 한다.

**자리 고정 4중 락 (CINEDANCE 이식 — 블로킹 락만으로 자리가 흔들리면 겹친다).**
화면 좌우(screen-LEFT/RIGHT)는 카메라에 상대적이라, 모델이 앵글을 바꾸는 순간
재발명될 수 있다. 자리가 왔다갔다하는 씬에는 아래를 순서대로 증축한다:

1. **랜드마크 접촉 앵커 (가장 강력)** — 인물마다 고정 사물에 물리적으로 묶는다:
   "within 1 meter of the counter, one hand resting on it", "back against the
   wall", "boots planted at the south kerb edge". 접촉·미터가 좌표보다 강하다.
   약한 위치어 금지: near, beside, around, nearby → "within 1 meter",
   "touching", "hand on the door handle"로 치환.
2. **시선·몸통 분리 락** — 몸 방향과 눈 방향을 각각 쓴다: "torso faces the
   door; eyes stay locked on <<<minister>>>". 하나만 쓰면 모델이 나머지를
   발명하다 인물을 돌려세운다.
3. **첫 프레임 점유 락** — "The first visible frame already contains all
   required characters in their correct positions. No empty establishing
   frame, no delayed character reveal." 배치 고정 와이드(첫 1초 규칙)와 세트로
   쓰면 첫 샷에서 자리가 확정된다.
4. **노 텔레포트 연속성 락** — POSITIVE LOCKS에 덧붙인다: "Across every
   internal cut: same left/right relationship, same gaze targets, same
   distance to landmarks — characters never teleport or swap positions."

인물이 3명 이상이면 각자에게 전경/중경/후경 레이어도 지정한다 ("<<<king>>> in
the midground, <<<guard>>> in the background by the pillar") — 깊이 축까지
잠가야 좌우 축이 버틴다.

**지리가 복잡하면 블로킹 락 대신 GEO SPATIAL LAYOUT.** 같은 장소 컷이 3개
이상이거나 랜드마크·소품 배치가 많으면 문장 하나로는 부족하다 — 씬당 1회
**공간 평면도 블록**을 작성해 그 씬 모든 컷에 무변경 복붙한다 (Hell Grind 검증,
`ai-character-drama/references/hellgrind-playbook.md` §4.1):

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— [랜드마크] = [무엇, 어디].
— [오브젝트]: [랜드마크 기준 위치, ~N m].
— 180° AXIS: camera ALWAYS stays on the [X] side — it NEVER crosses the line.
— [광원]: comes from [방향, 카메라 기준].
```

인물·액션 없이 장소만. 좌우는 카메라 기준(frame-left/right)만, 위치는 랜드마크
기준+미터. 컷마다 누가 어디 서서 어딜 보는지는 **다시** 명시한다(모델은 이전
샷을 기억 못 한다). 정적 대화엔 방 전체가 아니라 **방의 한 구석**을 줘라 —
공간이 좁을수록 모델의 선택지가 준다. GEO는 지도일 뿐 — 룩은 로케이션 Element가
담당.

## 구조 모드 (기본 규격 — 모든 컷)

Higgsfield 스튜디오 실전 표준의 섹션 구조 프롬프트 — Cully Hill Boys 123컷 실측에서 대사 컷 포함 전 컷이 이 구조였다. 전체 분석과 예문은 `ai-character-drama/references/higgsfield-structure.md` 참조. 섹션 골격 (이 순서, 대문자 헤더 그대로):

```
SCENE CONTEXT      ← "EXACT N CHARACTERS — NO DUPLICATES" 헤더 + 요약 + 시퀀스
                     위치("Continuing from CUT N") + 샷 수 + 주어 수
ACTIVE REFERENCES  ← Element마다 역할+범위 선언 (위 Element 규칙)
LOCATION MAP       ← 공간 지리. 프레임 밖 연속성까지 ("the room continues toward...")
                     지리 복잡하면 GEO SPATIAL LAYOUT 블록으로 (위 참조)
FIRST FRAME AND SPATIAL BLOCKING ← 첫 프레임 상태. 항상 이미 행동 중간(mid-action)
FORMAT MODE        ← 비율/4K/카메라 유형/샷 수/무대사 컷은 "SFX only, no dialogue,
                     no captions" — 대사 컷은 "dialogue per DIALOGUE block, no
                     captions, no subtitles"
OPTICS             ← 샷별: 화각° + 거리m + 높이 + 실행 가능 근거 (아래)
CAMERA             ← 샷별 카메라 무브먼트 + 타임코드 (피사체 액션과 분리 서술)
ACTION TIMING      ← 비트 타임라인. 샷 경계마다 "N.Ns HARD CUT." 한 줄.
                     비트당 ≤3문장 — 과적된 비트는 뭉개진다
PHYSICS            ← 역학 계약 2~4문장 (아래)
LIGHTING           ← 광원마다 동기 명시 + 아티팩트 가드. 역광이면 콩트르주르
                     표준 블록 (hellgrind-playbook.md §4.7)
AUDIO              ← 앰비언스/폴리 + no-BGM 클로즈("... no music track ...") +
                     캡션 클로즈("no captions, no subtitles, no on-screen text" —
                     전 컷 필수). 무대사 컷은 "No dialogue, no music track, no
                     captions"; 대사 컷은 보이스 descriptor(verbatim) + 언어 클로즈
DIALOGUE           ← 대사 컷만: 화자별 (전달 톤 부사) + 따옴표 대사 전문.
                     음절 예산 적용 (컷당 ≤3줄, 줄당 ≤15음절, 화자 ≤2명)
CHARACTER ACTING   ← 캐릭터별 1~2줄: state / wants / hides / body rhythm /
                     what changes (감정 비중 있는 컷 — acting-system.md §10)
POSITIVE LOCKS     ← 최종 락 블록 (아래) — 통일 스타일 문자열은 여기 맨 끝
NEGATIVE           ← 맨 마지막: 금지 태그 나열 (아래 NEGATIVE 규칙)
```

**NEGATIVE 블록 (2026-08-30 추가 — 사란 컷 실측, 프롬프트 바이블 §15).** 프롬프트 맨
마지막에 순수 금지 태그를 나열하는 블록. "긍정형 액션만" 원칙과 충돌하지 않는다 — 그
원칙이 금지하는 것은 **액션 문장 속 부정**("does NOT fall"류, 오해석 위험)이고, 말미의
짧은 명사구 금지 태그("no tears, no BGM")는 별개 도구다. 작성 규칙:
- **주제별 클러스터로 묶는다** (줄바꿈으로 구분): 정체성 드리프트(머리·의상·소품) /
  액션 / 감정·신파 / 연기 톤 / 텍스트·자막 / 카메라 / 신체 결함·기타. 순서는 이 컷의
  사고 위험이 큰 클러스터부터.
- **사고 이력의 축적 문서다** — 드리프트를 겪을 때마다 한 줄씩 늘린다(금칙어 사전과
  같은 원리). 표준 상비 태그: no beauty filter, no extra fingers, no morphing faces,
  no identity drift in <머리/장비>, no slow motion, no optical zoom, no drone shot,
  no gimbal-smooth glide, no subtitles, no on-screen text, no BGM, no music track.
- **포지티브와 싸우게 하지 마라** — 전역 금지(no running 등)를 걸었으면 어떤 샷
  지시에도 그 동작이 없어야 한다. 충돌하면 화면이 어정쩡해진다.
- 승부처 금지는 NEGATIVE에만 두지 말고 3중 재진술(SCENE CONTEXT 선행 금지 →
  ★LOCK★ → NEGATIVE)로 조인다.

- **분량: 15초 표준 컷은 400~600단어, 플랫폼 입력 한도는 ~18,000자(한글 포함 문자 수)** — 힉스필드 입력창 1.8만자까지 수용 (사용자 실측 2026-08-30; 구 만자 한도(2026-08-22)와 5,000자 캡 주장은 폐기). 납품 전 `wc -m`으로 실측하라 (어림 금지). 1.8만자 예산에서는 2.5 확장 기법(3중 재진술·EVENT TRACK·CHARACTER ACTING·확장 락)을 온전히 적용할 수 있다 — 단 분량은 통제 수단이지 목표가 아니다: 컷의 통제에 기여하지 않는 수사는 한도가 허용돼도 넣지 않는다. 초과 시 감량 순서: 수사적 문장 → OPTICS/CAMERA 섹션 통합 → 중복 선언 → PHYSICS/LIGHTING 부연. **절대 보존**: EXACT N 헤더, 소품·발사 카운트 락, 축·랜드마크 위치 락, HARD CUT 타임코드, DIALOGUE 블록·AUDIO의 verbatim 대사. **대사 컷 처리**: 대사 2줄+ 또는 화자 2명이면 DIALOGUE 블록에 전문을 쓰고(음절 예산 적용) 화자 락·주소 락(★SPEAKER/ADDRESS LOCK★)을 POSITIVE LOCKS에 세운다. **대사 ≤1줄이면** DIALOGUE 블록 생략하고 AUDIO 섹션에 격리해도 된다: 보이스 descriptor(verbatim) + "His line, and nothing else" 하드 블록 (Hell Grind 방식). 어느 쪽이든 액션 섹션(ACTION TIMING)에는 대사의 한 단어도 넣지 않는다 — "he delivers line 1" 식 참조만.
- **OPTICS 3단 사다리**: `47°`(표준 50mm 상당 — 설정/트래킹) / `29°`(준망원 85mm — 인물/압축) / `20°`(타이트 135mm — 클로즈업). 특수 용도 확장: `8°`(초망원 스포츠 중계 압축, heat shimmer와 조합) / `12°`(매크로 소품 디테일) / `63°`(와이드) / `84°`(웜즈아이 울트라와이드, 지면 카메라) / `107°`(무릎 높이 달리 와이드). 각 샷에 `화각 + camera N meters + 높이 + "room-feasible framing"` 근거를 붙인다 — 근거가 있으면 물리적으로 불가능한 앵글·급작스런 광각 왜곡이 사라진다. 앵글엔 의도도 붙인다 ("oblique angle deliberately avoiding a frontal read"). **렌즈는 콘텐츠 유형으로 고른다** — 망원 샷엔 가시적 결과 4개+("background compressed flat", "creamy bokeh wash", "close framing achieved through lens reach, not physical proximity"), 와이드 샷엔 3개+("foreground looms larger", "deep edge-to-edge focus", "straight lines stay rectilinear"), 8° 초망원엔 전경 가림 필수; 한 비트에 콘텐츠 클래스(인물/환경/매크로)를 섞으면 렌즈 드리프트 — 결정 트리와 안티드리프트 락은 `ai-character-drama/references/hellgrind-playbook.md` §4.6.
- **HARD CUT 마커**: 샷 수를 선언하고 경계 초에 "6.0s HARD CUT."를 박는다. 이 모드에선 멀티샷 위임 문장을 쓰지 않는다 — 샷 설계를 직접 한다.
- **무브먼트 = 감정 지시**: 관찰·동행 = tracking(피사체 눈높이) / 긴장 홀드 = "static-leaning hold, natural breathing motion" / 관조·이별·데드팬 = static locked-off / 감정 고조·의심 = slow push-in / 규모 리빌 = slow pull-back / 올려다보기 = tilt-up. **줌 금지, 푸시인으로** (줌은 워블 생김). 카메라 유형(handheld/non-fixed)은 FORMAT MODE에 선언하고 클립 내내 유지. 전형 리듬: tracking → static hold → handheld 사건 → push-in 정점 → locked-off 여운. 상세 표는 `higgsfield-structure.md` §3.5.
- **감정 동기 카메라 4기법 (2026-08-30 — 사란 시장걷기 컷 실측 1회 통과, 프롬프트 바이블 §7 해부 근거)**: 멀티샷 감정 씬에 겹쳐 쓴다.
  ① **동기 명문화** — 무브를 고르는 데서 멈추지 말고 동기를 프롬프트 문장으로 박는다: "The move is motivated: her hope pulls the camera in." FORMAT MODE에는 씬의 동력원을 선언 ("the camera is alive and motivated by her energy / by the distance between them").
  ② **화각 곡선** — 샷별 화각을 개별 선택이 아니라 곡선으로 설계 (예: 40→47→29→33→26). 감정이 조여들수록 좁히고, 인물의 첫 정면 프레이밍은 마지막 샷까지 아껴서 보상으로 쓴다.
  ③ **카메라 편들기** — 인물이 갈라지는 비트에서 카메라가 누구와 함께 멈추는지 선언: "the CAMERA STOPS WITH HER — he keeps moving away INSIDE the frame, shrinking." 떠나는 쪽은 컷으로 지우지 말고 프레임 안에서 작아지게.
  ④ **도착 동기화** — 푸시인의 도착 순간을 대사의 도착 순간에 묶는다: "landing on her face exactly as the question lands" + 편집점 "Cut ON the question." 마지막 무브는 cm 단위로 절제 ("a final soft drift 20 cm closer") — 훅 들어가면 신파가 된다.
  **핸드헬드는 촬영기사의 몸으로 서술한다** (CINEDANCE): "operator breath,
  micro-settling, weight shifts, shoulder-mounted mass, organic imperfect
  correction" — 기계적 표현(digital jitter, random shake)은 금지, gimbal
  smoothness·floating drone feel은 명시 요청 시에만.
- **PHYSICS**: "자연스럽게" 대신 역학을 계약: "crouch-launch-land arc with visible weight settling", "not a mechanical repeat", "residual drops falling under gravity". 반복 동작·점프·소품 조작·천·물이 있으면 필수.
- **POSITIVE LOCKS 구성**: ①주어 수 락 ("Exactly one subject throughout") ②연속성 락 (시작 상태·경로 제한·"the room's interior design does not change") ③트릭 실행 락 ④다음 컷 인계 소품 상태 ("the faucet is still running, carrying into CUT N+1") ⑤IP 가드 ⑥통일 스타일 문자열. 부정문은 **"A, not B" 쌍**으로만 ("a circular vignette, not a rectangular wipe") — 금지만 하지 말고 대안을 같이.
- **컷 체인 (Anchor-and-Extend)**: 같은 장소에서 시간 점프 없이 이어지는 컷(30초·60초 씬을 15초로 쪼갠 경우는 항상)은 직전 컷 마지막 프레임을 continuity reference로 넣고, 프롬프트 첫 줄을 "Frame opens matching the final frame of CUT N: <누가 어느 쪽에, 어느 방향, 카메라 높이, 소품 상태>"로 시작한다. 직전 컷 POSITIVE LOCKS의 인계 소품 상태를 그대로 받고, 체인 마지막 컷엔 "This is the final clip of the scene — nothing follows it" 선언. 장소가 바뀌거나 시간이 건너뛰거나 일부러 새 설정샷으로 여는 컷은 체인하지 않는다.
- **변신/모핑은 화면 밖으로**: 중간 단계를 요구하지 말고 오프스크린 처리 ("he goes in, the cat comes out, in one unbroken shot — reads as an in-camera trick rather than an edit").

**리비전 원리**: 결과가 틀리면 프롬프트를 갈아엎지 말고, 모델이 발명한 것을 금지+대안 쌍으로 락 블록에 증축한다. 공간이 복잡해 동선이 붕괴하면 프롬프트를 늘리지 말고 **세계를 단순화**한다 ("a small studio apartment: just two rooms, nothing else"). 증상별 레시피 표는 `higgsfield-structure.md` §8.

## 특수 컷 레시피 (Higgsfield 공식 Seedance 가이드 반영)

기본 모드 위에 겹쳐 쓰는 컷 유형별 오버라이드. 출처: higgsfield.ai/blog/seedance-prompting-guide.

**POV (1인칭) 컷** — 카메라가 곧 인물의 눈. 이 컷에서는 샷을 나누지 말고 FORMAT MODE에 아래를 선언한다 (명시적 선언이 없으면 Seedance가 기본값으로 앵글을 커팅해 시점이 깨진다):

```
One continuous shot, first-person POV perspective. No cuts, no zoom,
natural head movement only.
```

- 몰입형 액션 POV면 추가: "hyper-chaotic handheld motion, constant micro-jitters, aggressive head swings" + 광각 왜곡("wide-angle lens with strong distortion, subtle chromatic aberration at frame edges").
- **손을 프레임에 상시 노출시켜라** ("her hands always visible in frame") — 시점 확정 + 그라운딩 앵커. 이게 빠지면 POV가 3인칭 스테디캠으로 미끄러진다.
- 블로킹 락·180도 축 문장도 이 컷에는 넣지 않는다 (단일 시점이라 무의미).

**격투/추격 컷** — 요구 3요소: ①명확한 장소 ②전력 차이(체급/능력 미스매치) ③격화 아크. 안무는 "싸운다"가 아니라 **비트 단위 동작으로 직접 기술**한다 — Seedance는 쓴 대로만 집행한다. 스피드 램프는 이 어휘 그대로:

```
...he ducks the swing — RAMPS INTO SLOW MOTION as the fist grazes past
his cheek, dust particles suspended — SNAPS BACK to full speed as he
counters with a shoulder throw.
```

정상 속도 확립 → 정밀 순간(회피 디테일, 임팩트)만 "RAMPS INTO SLOW MOTION" → "SNAPS BACK". 컷당 램프 1회가 안전선. 스타일 참조는 감독 이름 조합이 잘 먹는다 ("Guy Ritchie speed-ramping with Snyder impact slow-motion") — 단 IP 세이프 원칙상 캐릭터/작품명이 아닌 연출 스타일 참조만.

**원테이크 트래버설/추격 컷 (2026-08-30 — 사란 파쿠르 런 30초 실측 성공).** 컷 없는
30초 원테이크의 유일한 정규 용법 — 인물이 연결된 공간을 고속으로 통과하며 세계를
소개하는 컷. duration 규정의 "특수한 원테이크"가 바로 이것. 구성 요소:
- **연속성 3중 선언**: 헤더에 "a single uninterrupted long take" + CAMERA에 "one
  continuous move from first frame to last" + NEGATIVE에 "no cuts, no montage, no
  hidden transitions, no teleportation". 하나라도 빠지면 모델이 몰래 컷한다.
- **공간 연결 선언**: "Every space is physically connected through stairways,
  rooftops, awnings, ropes, bridges and doorways." — 원테이크의 생명. 이 선언이
  없으면 공간이 순간이동으로 이어진다.
- **화살표 루트 채보 (CONTINUOUS SPATIAL ROUTE)**: 통과 구간 전체를 "A → B → C"
  화살표 체인으로 명시하고, 구간마다 통과 동작(vault/slide/drop/rope descent)을
  하나씩 배정한다. 루트가 곧 액션 타임라인이 된다.
- **카메라 비미러링**: 카메라는 인물의 라인을 복사하지 않고 **자기 라인**을 탄다 —
  "when she vaults a stall counter, the camera swings through the gap beside it;
  when she slides under a beam, the camera ducks with a violent dip and rough
  recovery." 오퍼레이터가 같은 루트를 달리는 실체를 부여하고("like a real camera
  operator free-running the same route"), 착지엔 졸트("a real landing jolt")를 준다.
- **기계 카메라 3종 부정**: "must not feel like a gimbal, a drone, or a
  video-game camera." (A-not-B 허용 예외 — 대안은 오퍼레이터 실체 선언이 담당.)
- **군중 지연 반응**: "the street is crowded and nobody clears a path in advance —
  shoppers react with realistic, slightly delayed surprise." AI 군중이 미리 길을
  비켜주는 클리셰 차단 + 인물은 군중을 지형으로 읽는다("she reads the crowd like
  terrain").
- **경로 = 세계 쇼케이스**: 통과하는 배경에 세계 법칙 시연을 심는다 (연습장의
  원소 화살 3색 시연 등) — 이동 컷이 곧 세계관 소개가 된다.
- **얼굴 유예 리빌 (선택)**: "seen from behind throughout; her face is never
  clearly shown until the final beat" + NEGATIVE "no frontal shots before the
  final beat" — 뒷모습 추적으로 달리다 마지막 비트에서 정지+리빌. identity anchor는
  등 뒤 디테일(머리·장비)로 잠근다.
- **no-BGM은 이 컷 유형에도 예외 없이 유지 (2026-08-30 사용자 확정)**: 원테이크
  트래버설도 no-BGM 클로즈 + 캡션 클로즈를 그대로 넣는다. 스코어의 감정 곡선
  (달리기 가속 → 정지 순간 정적 → 엔딩 스웰)이 필요하면 프롬프트에 굽지 말고
  **후반에서 Suno BGM으로** 얹는다 — 그래야 음량·타이밍을 편집에서 통제할 수 있다.
  프롬프트 안에서는 디제틱 사운드(발소리·숨소리·장비 소리·군중)의 리듬 채보가
  스코어의 역할을 대신한다.

**인라인 VFX 브래킷** — 마법/에너지/입자 효과는 액션 비트 문장 안에 브래킷으로 박는다:

```
5-10s: she presses her palm to the door [VFX: branching electric circuits
pulsing with white-blue current] and the lock sparks open.
```

효과를 별도 문장으로 빼면 액션과 분리 렌더되거나 무시된다. 브래킷이 효과를 해당 동작·타이밍에 바인딩한다.

**리얼리즘 가드** — 포토리얼 컷에서 크리처/변신/특수분장이 3D 게임 그래픽처럼 나오면(피부가 매끈·플라스틱) 프롬프트에 `no 3D, no cartoon, no VFX look` 을 추가한다. 통일 스타일 문자열이 이미 "cinematic photorealistic live-action"이어도 크리처엔 이 가드가 별도로 필요하다.

**무음 비트** — 감정 정점 한 순간을 완전 무음으로 만들려면 해당 비트에 `NO MUSIC, NO SFX — total silence` 를 인라인으로 박는다. no-BGM 클로즈(음악 전역 차단)와는 별개 도구다.

**애니메이션 스타일 컷** — 프로젝트 통일 스타일이 애니메이션(2D/3D/스타일라이즈드)일 때의 오버라이드:

- **첫 줄에서 미학을 선언**한다. 하이브리드 공식이 잘 나온다: "Cinematic stylized 3D animation — photorealistic environments, stylized characters" (배경은 포토리얼, 캐릭터는 스타일라이즈드).
- **키프레임 이미지를 style reference Element로 등록**하고 역할을 선언한다 (`style reference — art style only, not composition`). 텍스트만으로 화풍을 유지하려 하지 마라.
- 타이밍을 대사 컷의 5초 3비트보다 잘게, **3~4초 세그먼트**로 쪼개 명시한다 (0-3s / 3-6s / 6-9s / 9-12s / 12-15s). 애니메이션은 동작 밀도가 높아 세그먼트가 잘수록 뭉개짐이 줄어든다.
- **물리를 명시적 키워드로**: "realistic particle physics", "volumetric dust storm", "realistic sand physics", "energy glow on character". 애니메이션 스타일에서 물리 언어를 빼면 입자·천·먼지가 종이처럼 나온다.
- 리얼리즘 가드("no 3D, no cartoon")는 당연히 **쓰지 않는다** — 포토리얼 컷 전용이다.

**뮤지컬/안무 컷 (음악 입력 Element)** — 춤·군무·뮤지컬 넘버는 예외적으로 **음악을 생성 입력 Element로 업로드**하고 Seedance가 박자에 안무를 싱크하게 한다 (가사 있으면 가사도 함께). 이 컷에서는 no-BGM 클로즈를 빼고 대신 "choreography synced to the uploaded music track"을 넣는다. 안무는 스텝을 마이크로매니징하지 말고 **장르 한 단어로 위임**한다 ("waltz", "K-pop choreography") — 스텝을 일일이 쓰면 오히려 동작이 붕괴한다. 후반 조립 시 이 컷 구간은 Suno BGM을 깔지 않는다(음악이 이미 베이크됨) — 사전 준비물에 이 사실을 명시할 것.

## 호출 파라미터 (항상 표로 같이 제공)

| 파라미터 | 값 |
|---|---|
| model | `seedance_2_0` — 플랫폼이 2.5를 제공하면 2.5 우선 (30초 + 동기화 오디오 + 레퍼런스 50개 + 영역 편집; 파라미터 표기는 플랫폼의 모델 목록에서 실측 확인) |
| duration | 4~15 (기본 15) — 2.5는 최대 30초. 15초는 3비트 예산 유지. **30초 멀티샷은 정규 패턴이다 (2026-08-30 갱신 — 사란 시장걷기 30초 5샷 대사극 실측 성공)**: 30초 = 5샷 안팎 + 5비트, 샷 경계마다 HARD CUT 타임코드, 비트당 액션 1개 원칙은 동일. 6비트 이상 욱여넣기는 금지. 컷 없는 30초 원테이크는 트래버설/추격 컷 한정 정규 용법 — 특수 컷 레시피 "원테이크 트래버설" 참조 |
| genre | 기본 `"drama"` — 코미디/액션 컷이어도 내러티브 컷이면 drama가 안전한 기본값이고, 톤은 프롬프트의 톤 키워드가 나른다. 플랫폼이 해당 톤의 genre 값을 별도 지원하면 그걸 쓰되, 한 프로젝트 안에서는 통일 |
| aspect_ratio | 쇼츠/릴스 → `"9:16"`, 그 외 `"16:9"` — 중간 변경 불가, 처음에 확정. 플랫폼은 `4:3, 1:1, 3:4, 21:9`도 지원 — 21:9는 시네마틱 트레일러 룩에 유효 |

## IP 세이프 네이밍 (정책위반의 90%가 여기)

영상 생성 플랫폼의 필터는 **보호 캐릭터명 + 연상 조합**을 선제 차단한다. 원작이 퍼블릭 도메인이어도 각색사(디즈니 등)의 캐릭터명·시그니처 스타일은 걸린다.

- 캐릭터명을 일반 명사로: "Cinderella-style gown" → "princess ball gown" → (더 걸리면) "elegant gown"
- 연상 조합 해체: "fairytale castle" → "palace facade at a theme park", "tiara" → "silver hair accessory"
- 시그니처 스타일링 복제 금지: 특정 각색판의 헤어+의상+액세서리 조합을 그대로 쓰지 않는다 (예: 금발 업두+헤드밴드+초커+퍼프 오프숄더 = 디즈니 신데렐라)

## 정책위반 트러블슈팅 (진단 사다리)

거부 메시지를 보고 **텍스트가 원인인지, 참조 이미지가 원인인지**부터 가른다:

1. **"reference elements may contain protected content"류** → 원인은 업로드한 참조 이미지. 텍스트 수정으로는 해결 안 됨. 이미지가 보호 캐릭터의 시그니처 스타일링을 닮은 것 — **오리지널 캐릭터 시트를 새로 생성해 교체**한다 (헤어 스타일 변경, 시그니처 액세서리 제거, 구별 특징 추가). 이미지를 살짝 고쳐 필터를 우회하는 건 금지 — 걸린 이유가 정당하고, 통과돼도 배급 단계에서 같은 문제가 터진다.
2. **텍스트 거부** → IP 세이프 네이밍 절차대로 캐릭터명→일반명사, 연상 조합 해체. 그래도 걸리면:
   - 참조 이미지 없이 텍스트만 돌려서 원인 분리
   - `natural skin texture` 삭제 (포토리얼+젊은 인물+피부 묘사 조합에 민감한 필터 존재)
   - 명칭을 한 단계 더 일반화
3. 어느 플랫폼인지 확인 — 필터 성향이 다르다. 수정본을 줄 때 "바꾼 것" 목록을 명시해 사용자가 원인을 학습하게 한다.

## Seedance 2.5 확장 규격 (2026-08 — Cully Hill Boys 123컷 실측 + 힉스필드 공식 가이드)

힉스필드 공식 스튜디오 장편 「Cully Hill Boys」(137씬 전편 Seedance 생성)의 실제 프롬프트
123건과 공식 2.5 프롬프팅 가이드(higgsfield.ai/blog/seedance-2-5-prompting-guide)에서 검증된
확장 도구들. 근거 통계·기법 전문: `~/.claude/skills/higgsfield-seedance-25/references/cully-hill-video-prompt-stats.md`
(같은 폴더의 production brief·golden sample도 참조). 기본 구조 모드를 대체하지
않는다 — **멀티컷 장편·시리즈급 통제가 필요할 때 구조 모드 위에 겹쳐 쓰는 증축분**이며,
어느 것을 쓰든 18,000자 입력 한도 안에서 적용한다 (2026-08-30 사용자 실측 갱신).

**① WORLD STYLE PREFIX — 세계관별 고정 스타일 헤더.** 프로젝트에 서사 축(인물 진영·정서
온도)이 2개 이상이면, 축마다 OPTICS(렌즈 사다리) + CAMERA(무브 성격) + LIGHTING +
STYLE + QUALITY + 60:30:10 컬러 배분을 통째로 잠근 프리픽스를 프로젝트 시작 시 설계하고,
그 세계에 속하는 모든 컷 프롬프트 맨 위에 **한 글자도 안 바꾸고** 복붙한다. 통일 스타일
문자열의 상위 호환 — 문자열 하나가 아니라 블록 세트를 잠근다. 효과: 룩만으로 "누구의
세계인지" 읽히고, 컷마다 스타일을 재기술하지 않아도 시리즈 룩이 유지된다.
(실측 예: 주인공 패거리=광각 몰입 핸드헬드 그라임 / 킬러=8°·18° 초망원 관찰 데드팬 /
갱단=가이 리치×레픈 / 잃어버린 가족 "Heaven"=따뜻한 화이트+오크.) 골든 샘플:
`higgsfield-seedance-25/references/golden-sample-style-prefix.md`.

**프리픽스 표준 4줄 공식 (2026-08-30 — 사란 시장걷기 컷 실측 통과, 프롬프트 바이블 §1 해부 근거).**
새 프리픽스를 설계할 때는 이 4줄 뼈대를 기본형으로 쓴다:
```
[① 룩 선언]  <질감어> <퀄리티 방어어> <시대/장르> <매체> look.
             예: "Gritty high-end medieval television production look."
[② 장비 줄]  Shot on <카메라> with <렌즈 성격>, <카메라 운용>.
             예: "Shot on ARRI Alexa 35 with classic spherical rectilinear lenses, operator-carried camera with restrained weight."
[③ 분위기 줄] <광원+확산 매개>, <muted+실명 색 2개 팔레트+그림자 색>, visible fine film grain, real <장면 재질> physics.
             예: "Harsh natural desert daylight softened by drifting dust haze, muted sun-bleached palette of ochre and bone with cold slate shadows, visible fine film grain, real fabric and dust physics."
[④ 인라인 금지] No <이 룩의 반대말> — 시대극 "No modern polish." / 현대물 "No commercial gloss."
```
규칙: ①의 질감어(gritty)는 퀄리티 방어어(high-end/prestige)와 반드시 쌍으로 — 단독이면 저예산 룩으로 빠진다.
③의 팔레트는 `muted` 단독 금지 — 실명 색(ochre and bone 등)과 함께 써야 desaturated化를 피한다.
카메라 운용은 handheld 단독 대신 "operator-carried … with restrained weight"(프로의 절제된 흔들림).
검증 변주: 현대 아파트판 "Gritty high-end contemporary television drama look / … / Late-night apartment stillness: one warm range-hood cone, cold city glow, muted palette of oat and charcoal with warm amber highlights, visible fine film grain, real fabric and water physics. / No commercial gloss." (테스트프롬프트_연인싸움)

**①-b WORLD 선언 블록 — 프리픽스의 짝 (2026-08-30, 사란 시리즈 실측).** 스타일
프리픽스가 "어떻게 찍나"를 잠근다면, WORLD 블록은 "무엇의 세계인가"를 잠근다.
프로젝트당 1회 설계해 시리즈의 모든 컷에서 프리픽스 바로 다음 자리에 무변경 복붙.
`WORLD:` 헤더로 시작하는 한 문단, 구성 5층:
1. **지리** — 장소의 형태와 랜드마크 ("a thriving archers' village carved into a
   natural sandstone amphitheater … terraces, rope bridges, carved stairways").
2. **팔레트의 소속** — 색을 나열하지 말고 장소의 속성으로 귀속 ("sun-warmed
   sandstone in golds, ambers and tans") — 색이 세계에 붙어 있으면 컷마다 안 흔들린다.
3. **공기** — 그 세계의 상시 대기 ("heat haze, fine golden dust hanging in sunbeams").
4. **세계 법칙 (범위 잠금)** — 초자연·기술 요소의 발현 범위를 잠그고 금지+대안 쌍으로
   닫는다 ("each has exactly one elemental gift, expressed only through their
   arrows … The elements live in arrows alone — no wands, no floating spells").
   이게 없으면 배경에 규칙 밖 마법·소품이 자란다.
5. **배경 인구 시그니처 + 톤 비유** — 엑스트라까지 시리즈 컬러 모티프에 편입
   ("ember-red / deep-blue / violet-white fletchings")하고, 세계의 일상 온도는
   비유 한 문장으로 ("Archery is everywhere and casual, the way a port town lives
   with sails").
LOCATION MAP과의 분업: WORLD는 시리즈 전역의 세계 헌법, LOCATION MAP은 이 컷이
벌어지는 구체 지점의 지도다 — WORLD를 컷마다 다시 쓰지 말고, LOCATION MAP이 WORLD의
지명·모티프를 좌표로 받아 쓴다.

**② 퍼센트 좌표 블로킹 (canon settle frame).** 승인된 스틸(키프레임)의 구도를 컷에서
재현해야 하면, 프레임 내 위치를 좌표로 박는다: "the plate spans x≈33–72%, top edge
~y≈50%, bottom cropped; the moth lands at the upper-left corner x≈43%, y≈47%, in profile".
GEO SPATIAL LAYOUT(랜드마크+미터)이 공간의 지도라면 이것은 **화면의 지도** — 정확한 착지
구도가 승부처인 컷(정물 인서트, 시그니처 구도, 이전 컷 마지막 프레임과의 1:1 매칭)에만
쓴다. 남용하면 카메라가 경직된다.

**③ ★LOCK★ 명명 조항.** POSITIVE LOCKS의 각 항목에 이름을 붙이고 별표로 감싼다:
`★SPEAKER LOCK — line 1 HORACE only; non-speakers' mouths CLOSED★`,
`★ADDRESS LOCK: the stare lands on OLI — never at the lens★`, `★SIZE IS LAW: the moth
stays 1 cm in every frame★`. 리비전 때 "어느 락이 깨졌는지"를 이름으로 추적·증축할 수
있게 된다. 실측 어휘: SPEAKER / ADDRESS / BLOCKING / BREAK / INSERT / CROWD / ALIVE
(자연스러운 깜빡임·호흡) / NOT-IMPRESSED(엔드 프레임 고정) LOCK 등 — 컷의 승부처마다
자유 명명.

**④ 3중 재진술 — 승부처 조항의 안전장치.** 스튜디오 원본(1만자급 — 웹 입력창이 아닌
경로로 추정)은 핵심 규칙을 SCENE CONTEXT 1회 + 해당 블록 1회 + 말미 POSITIVE
CONSTRAINTS 1회, 총 3회 반복한다. 1.8만자 한도(2026-08-30 갱신)에서는 승부처 조항 3~5개를 온전히 3회 반복할 수 있다 — 전 조항 재진술은 여전히 과잉이니, 컷의 생사를
가르는 것만 고른다.

**⑤ EVENT TRACK — 환경 요소 채보.** 파도·돌풍·군중 이동·배경 차량처럼 인물이 아닌 환경
요소가 연출에 개입하면, ACTION TIMING과 별도로 타임라인을 채보한다:
`EVENT TRACK: 2.0s a gust lifts the tarp edge; 5.5s the crowd surges left; 8.6s a distant
gull cry`. 안 하면 생성마다 랜덤 변동한다 (공식 가이드의 명시 실패 모드). 디제틱 사운드도
같은 방식으로 타임스탬프를 찍을 수 있다.
**대사 동기화 + 인지 지시 (2026-08-30, 사란 컷 실측):** 환경 이벤트를 특정 대사의 착지
순간에 묶고("11.0s one faint crackle between her fletchings AS her spark line lands")
누가 보고 누가 못 보는지까지 지시하면("unnoticed by both") 관객만 아는 극적 아이러니가
만들어진다. 복선 이벤트는 "unremarked"(아무도 언급 않음)로 눌러서 배경에 심는다.

**⑥ 시대 락 (시대물 필수).** 배경 연도가 현재가 아니면 "nothing in frame newer than
[연도] — no smartphones, no modern cars"를 **모든 컷 프롬프트와 모든 로케이션 플레이트에**
반복한다. 한 번만 쓰면 모델이 현대로 끌고 간다 — "엑스트라 한 명이 폰을 들면 그 샷은 끝"
(Cully Hill 브리프). QUALITY 블록에 넣는 것이 실측 표준.

**⑦ 매너 문단 — 캐릭터 거동 고정.** 주연마다 "어떻게 서고, 어떻게 말하고, 질 때 얼굴이
뭘 하는지" 한 문단을 첫 촬영 전에 확정하고 그 인물이 나오는 모든 프롬프트에 붙인다.
ROCO/CHARACTER ACTING이 컷 단위 연기라면 매너 문단은 **시리즈 단위 인격 고정** — 억양도
라벨("cockney")이 아니라 조건으로 쓴다 ("th→f/v, dropped h, glottal t, -ing→-in'").

**⑧ 운영 원칙 (2.5 물량 전략).** 스튜디오 실측: 720p Standard로 씬당 수십~수백 테이크를
돌려 선별하는 것이 1080p 소량보다 낫다 — 프롬프트는 통제를 높이는 도구지 1회 성공을
보장하는 도구가 아니다. 21:9는 시네마 룩 표준으로 실전 검증됨. 프롬프트 다국어 혼용(영어
기본 + 한국어/중국어 블록)도 소화되지만, 이 스킬의 기본은 영어 프롬프트 + "등장인물은
한국어로 말한다" 클로즈 유지.

## 감정 연출 마이크로 기법 (2026-08-30 — 프롬프트 바이블 47엔트리 해부 추출)

사란 "시장걷기 사냥조르기" 컷(실측 1회 통과)을 한 줄 단위로 해부해 추출한 기법.
감정 비중이 있는 컷에 골라 겹친다 (전부 의무는 아님 — 컷의 승부처에만).

1. **감정 출구 배선** — 감정 표현을 금지만 하지 말고 **허용 출구를 같이 배선**한다:
   "no tears — the desperation lives only in her cracking voice and white knuckles."
   금지(눈물) + 출구(목소리·손마디·한숨/헛웃음)를 한 문장에. 출구가 없으면 모델이
   금지를 뚫거나 감정 자체를 지운다. 결말 감정도 캐릭터 문법으로 번역해 지정
   ("the gruff kid's version of heartbreak, dry-eyed").
2. **횟수 연출 (count-as-drama)** — 아껴야 클라이맥스가 되는 동작(시선·돌아봄·미소·
   접촉)은 횟수+시각을 잠근다: "he looks back exactly ONCE — at 24.5s." 반대로
   "for the first time in the whole walk"로 **첫 허락**을 명시하면 그 순간에 무게가
   실린다. 양보·무너짐의 분량도 계량한다 ("for one line the gruffness cracks").
3. **금지+예외 열거 락** — 전면 금지가 필요하지만 예외가 있는 요소는 "전부 금지 +
   허용 예외를 시각까지 열거"로 쓴다: "no flames anywhere — the only elemental
   events are one faint crackle at 11.0s and one distant bloom at 22.5s." 모호한
   부분 허용보다 훨씬 안정적이다.
4. **연기 해석 표지판** — 오독 가능한 감정 순간마다 "A가 아니라 B" 표지판을 박는다:
   "a promise, not a brush-off", "not triumph but reassurance", "his dismissal is
   administrative, not hostile." 같은 대사도 이 한 절로 정반대 연기가 갈린다.
5. **조명 감정 곡선** — 캐치라이트를 샷 단위로 배정한다 ("visible catchlights in her
   eyes in shots 1, 2 and 5" — 거절당하는 3·4에는 없음). 조명 효과는 따로 만들지
   말고 **무브 × 광원 배치의 곱셈**으로 얻는다 ("the arcing camera crossing the
   sun shafts makes the light pulse naturally over their faces").
6. **사운드 캐릭터화** — 폴리에도 인물별 형용사를 배정한다: "two pairs of footsteps
   on stone — his slow and even, hers quick and eager." PHYSICS의 보폭 형용사를
   AUDIO에 그대로 이식하면 소리에도 성격이 실린다.
7. **배경 연기 상한 + 소품 의미** — 조연 리액션은 "~하되 ~는 아니다"로 상한을 긋는다
   ("mock-weary, zero real annoyance", "fond background rhythm, never
   scene-stealing"). 감정 소품은 의미까지 지정한다 ("the date is consolation") —
   던지는 손의 표정이 달라진다.
8. **대문자 = 볼륨** — 대문자는 프롬프트의 볼륨 노브다. 사고 다발 지점의 핵심 단어만
   선별적으로 올린다 (EXACT, BOTH, ONCE, INSIDE, DEAD, BACKWARDS, TALKED).
   문장 전체 대문자 남발은 볼륨을 도로 죽인다.

## 연계

- 대본이 `screenplay-pipeline` 포맷(`## S#N.`, `**이름:** 대사`, 지문)이면 씬을 그대로 파싱해 비트로 재배열한다: 지문 → 액션 비트, 대사 → 음절 예산 검사 후 배치, 씬의 마지막 감정 비트 → 버튼.
- 원작 IP가 있는 작품이면 프로젝트의 IP 체크리스트(예: `디즈니요소_체크리스트.md`)를 먼저 읽고 그 기준을 프롬프트에 반영한다.
- 여러 컷을 연속으로 뽑을 땐 통일 스타일 문자열과 Element ID를 컷 간에 동일하게 유지하고, 같은 장소 씬에는 블로킹 락 문장도 동일하게 유지한다.
