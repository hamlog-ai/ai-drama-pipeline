---
name: seedance-cut-prompt
description: 각본/대본의 특정 씬(S#N)을 Seedance 2.0용 영상 컷 프롬프트로 변환한다 — 15초 3비트 구조, 대사 음절 예산, Element 태그 참조, 멀티샷 위임, no-BGM 클로즈, IP 세이프 네이밍까지 규격대로. 사용자가 "S#N 영상 프롬프트 줘", "이 씬 시댄스/Seedance용으로", "영상 프롬프트로 바꿔줘", "15초 컷으로 만들어줘"라고 하거나, 생성한 프롬프트가 "정책위반/policy violation/protected content"로 거부됐다고 할 때 반드시 사용한다. 프롬프트 텍스트만 원하는 경우에 쓰고, 실제 영상 생성·조립까지 원하면 ai-character-drama 스킬로 넘어간다.
---

# Seedance Cut Prompt (대본 씬 → 영상 프롬프트 변환)

각본의 씬 하나를 Seedance 2.0 컷 프롬프트로 변환한다. 산출물은 **프롬프트 텍스트 + 호출 파라미터 + 사전 준비물(Element별 완성 이미지 프롬프트 포함)** 3종 세트. 실제 렌더/전체 영상 제작은 `ai-character-drama` 스킬의 영역이다 — 그쪽으로 넘어갈 땐 이 스킬로 만든 프롬프트를 그대로 들고 간다.

**모드 선택이 첫 판단이다.** 대화가 중심인 컷(대사 2줄 이상 또는 화자 2명) → 아래 콤팩트 규격 (음절 예산이 지배 제약). 무대사(SFX only) **또는 대사 ≤1줄의 짧은 한마디뿐**이면서 ①이전 컷과 프레임 연속이거나 ②공간 트릭(변신·통과·아이리스)이 있거나 ③비인간 주연이거나 ④액션·VFX·연속성이 지배하는 컷 → **구조 모드** (아래 별도 섹션).

> **대사 컷의 예외 — 특정 샷이 지정된 컷은 대사가 있어도 구조 모드 (2026-08 실측).**
> 대본이 특정 샷을 요구하면(우물 수면 리플렉션, 손목 인서트, 톱다운, 그 밖의 특수
> 앵글) 콤팩트의 멀티샷 위임으로는 **그 샷이 안 나온다** — 모델이 평범한 투샷·
> 클로즈업으로 대체해버린다. 같은 대본·같은 Element로 A/B를 떠보니, 콤팩트는
> "우물에 비친 얼굴"을 두 사람 서 있는 그림으로 뭉갰고 구조 모드는
> `20° tight insert, 0.6m above the well mouth angled down`으로 정확히 뽑았다.
> 판정: **컷의 승부처가 "입"이어도, 대본에 그려진 특정 이미지가 그 컷의 핵심이면
> 구조 모드.** 대사는 구조 모드의 ACTION TIMING 안에 voice verbatim으로 격리한다. 짧은 한 줄 대사는 구조 모드의 AUDIO 섹션에 verbatim으로 격리한다 (보이스 descriptor + "His line, and nothing else" 하드 블록 — Hell Grind 방식). 1인칭(POV) 컷이나 격투/추격 컷이면 해당 모드 위에 **특수 컷 레시피**(아래 섹션)를 겹쳐 적용한다.

**납품 전 필수: 셀프리뷰 루브릭 통과.** 이 스킬의 예산·블로킹 수치는
`ai-character-drama/references/prompt-mastery.md`의 요약본이다 — 프롬프트를
사용자에게 주기 전에 그 문서의 셀프리뷰 루브릭(§6)을 실제로 순회하고, 걸리는
항목은 고친 뒤에 납품한다. 두 문서의 수치가 어긋나면 prompt-mastery.md가 원본이다.

## 프롬프트 해부도 — 콤팩트 규격 (대사 컷 기본)

```
CUT S#N (0-15s).                              ← 라벨
EXACT N CHARACTERS — NO DUPLICATES: [이름들].   ← 캐릭터 수 헤더 (2인 이상 컷 권장 — 모델은 사람을 추가하고 가구를 복제한다)
<통일 스타일 문자열>, <톤 키워드>               ← 스타일은 한 글자도 안 바뀌게; 톤은 genre 파라미터와 호응 (cinematic drama / fast comedy 등)
Location: <<<env_id>>> — 공간+조명+세트 묘사.   ← 환경 Element
<<<char_id>>> (한 줄 외형 요약) + 블로킹.        ← 캐릭터 Element + 누가 어디서 뭘 들고
<블로킹 락 문장 또는 GEO SPATIAL LAYOUT>         ← 같은 장소 2컷+ 씬이면 필수 (아래 참조)
0-5s: [비트 1 — 구체적 동사 액션 + 대사]         ← 씬 첫 컷이면 0-1s는 배치 고정 와이드 (아래 "첫 1초 규칙")
5-10s: [비트 2]
10-15s: [비트 3 — 리액션/표정으로 끝 (버튼)]
[선택] ROCO — state: X; wants: Y; hides: Z;     ← 압축 연기 블록 (감정 비중 큰 컷 —
rhythm: W; changes when: V.                       acting-system.md §10 축약형)
등장인물은 한국어로 말한다.                       ← 언어 클로즈 (필수)
Edited as a multi-shot scene with motivated hard cuts between varied angles
(establishing, two-shot, close-ups, reaction, insert) chosen naturally to fit
the beats; dynamic cinematic coverage.          ← 멀티샷 위임 (필수)
no background music, no BGM, no soundtrack — only spoken dialogue and natural
diegetic sound (<장면에 맞는 환경음 예시>).       ← no-BGM 클로즈 (필수, 마지막 줄)
```

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
- **대사: 컷당 ≤3줄, 줄당 ≤15음절, 화자 ≤2명, 구어체.** 한국어 발화 속도 초당 5~6음절 기준 — 초과하면 립싱크 붕괴.
- **전체 120~250단어.** 250 초과 시 가치 낮은 절부터 삭제.
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
- 특정 비트에 샷 스펙이 꼭 필요하면 그 비트에만 축약 표기를 붙인다 — `(29° FOV, ~1.5m, eye level)`. 전 비트에 샷을 지정하면 뚝뚝 끊긴다 (멀티샷 위임이 기본).

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
- `continuity reference` — 직전 컷의 마지막 프레임. 시작 포즈·카메라 높이·소품 상태를 잇는 접착제 (구조 모드 참조). 등록 방법: 로컬 프레임은 image_job이 없으므로 `media_upload`/`media_import_url`로 올린 뒤 반환된 media id/type으로 등록 — 절차는 `ai-character-drama/references/workflow.md` §4.

참조 사진과 씬의 현재 상태가 다르면 차이를 명시한다: "the room is tidier than the reference photo, no clutter."

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

예: *"<<<king>>> sits screen-LEFT facing right; <<<minister>>> stands screen-RIGHT facing left; all shots stay on the same side of the action axis (180-degree rule); they never swap screen sides."* 멀티샷 위임과 충돌하지 않는다 — 앵글은 모델이 고르되 축과 좌우는 이 문장이 못박는다. 여러 컷을 연속으로 뽑을 때 "사전 준비물"에 씬별 블로킹 락 문장도 함께 명시해 사용자가 컷마다 복붙하게 한다.

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
4. **노 텔레포트 연속성 락** — 멀티샷 위임 문장 뒤에 덧붙인다: "Across every
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

## 구조 모드 (무대사 시네마틱 컷 전용)

Higgsfield Cinema Studio 스타일의 섹션 구조 프롬프트. 무대사 + 연속성 크리티컬 컷에서 콤팩트 규격보다 구도·공간·물리가 확연히 좋게 나온다. 전체 분석과 예문은 `ai-character-drama/references/higgsfield-structure.md` 참조. 섹션 골격 (이 순서, 대문자 헤더 그대로):

```
SCENE CONTEXT      ← "EXACT N CHARACTERS — NO DUPLICATES" 헤더 + 요약 + 시퀀스
                     위치("Continuing from CUT N") + 샷 수 + 주어 수
ACTIVE REFERENCES  ← Element마다 역할+범위 선언 (위 Element 규칙)
LOCATION MAP       ← 공간 지리. 프레임 밖 연속성까지 ("the room continues toward...")
                     지리 복잡하면 GEO SPATIAL LAYOUT 블록으로 (위 참조)
FIRST FRAME AND SPATIAL BLOCKING ← 첫 프레임 상태. 항상 이미 행동 중간(mid-action)
FORMAT MODE        ← 비율/4K/카메라 유형/샷 수/"SFX only, no dialogue, no subtitles"
OPTICS             ← 샷별: 화각° + 거리m + 높이 + 실행 가능 근거 (아래)
CAMERA             ← 샷별 카메라 무브먼트 + 타임코드 (피사체 액션과 분리 서술)
ACTION TIMING      ← 비트 타임라인. 샷 경계마다 "N.Ns HARD CUT." 한 줄.
                     비트당 ≤3문장 — 과적된 비트는 뭉개진다
PHYSICS            ← 역학 계약 2~4문장 (아래)
LIGHTING           ← 광원마다 동기 명시 + 아티팩트 가드. 역광이면 콩트르주르
                     표준 블록 (hellgrind-playbook.md §4.7)
AUDIO              ← 앰비언스/폴리 + "No dialogue, no music, no captions"
CHARACTER ACTING   ← 캐릭터별 1~2줄: state / wants / hides / body rhythm /
                     what changes (감정 비중 있는 컷 — acting-system.md §10)
POSITIVE LOCKS     ← 최종 락 블록 (아래) — 통일 스타일 문자열은 여기 맨 끝
```

- **분량 400~600단어, 그리고 플랫폼 입력 한도 ~5,000자(한글 포함 문자 수) 필수 준수** — 납품 전 `wc -m`으로 실측하라 (어림 금지; 30초 컷은 쉽게 6,000자를 넘긴다). 초과 시 감량 순서: 수사적 문장 → OPTICS/CAMERA 섹션 통합 → 중복 선언 → PHYSICS/LIGHTING 부연. **절대 보존**: EXACT N 헤더, 소품·발사 카운트 락, 축·랜드마크 위치 락, HARD CUT 타임코드, AUDIO의 verbatim 대사 블록. (대사 컷의 120~250단어 예산은 이 모드에 적용 안 됨 — 대사가 없거나 한 줄뿐이라 희석될 립싱크 지시도 적다.) 대화 중심 컷(대사 2줄+ 또는 화자 2명)은 이 모드를 쓰지 마라 — 콤팩트 규격으로. **대사 ≤1줄은 허용**: AUDIO 섹션에만, 보이스 descriptor(verbatim) + "His line, and nothing else" 하드 블록과 함께. 액션 섹션에는 대사의 한 단어도 넣지 않는다.
- **OPTICS 3단 사다리**: `47°`(표준 50mm 상당 — 설정/트래킹) / `29°`(준망원 85mm — 인물/압축) / `20°`(타이트 135mm — 클로즈업). 특수 용도 확장: `8°`(초망원 스포츠 중계 압축, heat shimmer와 조합) / `12°`(매크로 소품 디테일) / `63°`(와이드) / `84°`(웜즈아이 울트라와이드, 지면 카메라) / `107°`(무릎 높이 달리 와이드). 각 샷에 `화각 + camera N meters + 높이 + "room-feasible framing"` 근거를 붙인다 — 근거가 있으면 물리적으로 불가능한 앵글·급작스런 광각 왜곡이 사라진다. 앵글엔 의도도 붙인다 ("oblique angle deliberately avoiding a frontal read"). **렌즈는 콘텐츠 유형으로 고른다** — 망원 샷엔 가시적 결과 4개+("background compressed flat", "creamy bokeh wash", "close framing achieved through lens reach, not physical proximity"), 와이드 샷엔 3개+("foreground looms larger", "deep edge-to-edge focus", "straight lines stay rectilinear"), 8° 초망원엔 전경 가림 필수; 한 비트에 콘텐츠 클래스(인물/환경/매크로)를 섞으면 렌즈 드리프트 — 결정 트리와 안티드리프트 락은 `ai-character-drama/references/hellgrind-playbook.md` §4.6.
- **HARD CUT 마커**: 샷 수를 선언하고 경계 초에 "6.0s HARD CUT."를 박는다. 이 모드에선 멀티샷 위임 문장을 쓰지 않는다 — 샷 설계를 직접 한다.
- **무브먼트 = 감정 지시**: 관찰·동행 = tracking(피사체 눈높이) / 긴장 홀드 = "static-leaning hold, natural breathing motion" / 관조·이별·데드팬 = static locked-off / 감정 고조·의심 = slow push-in / 규모 리빌 = slow pull-back / 올려다보기 = tilt-up. **줌 금지, 푸시인으로** (줌은 워블 생김). 카메라 유형(handheld/non-fixed)은 FORMAT MODE에 선언하고 클립 내내 유지. 전형 리듬: tracking → static hold → handheld 사건 → push-in 정점 → locked-off 여운. 상세 표는 `higgsfield-structure.md` §3.5.
  **핸드헬드는 촬영기사의 몸으로 서술한다** (CINEDANCE): "operator breath,
  micro-settling, weight shifts, shoulder-mounted mass, organic imperfect
  correction" — 기계적 표현(digital jitter, random shake)은 금지, gimbal
  smoothness·floating drone feel은 명시 요청 시에만.
- **PHYSICS**: "자연스럽게" 대신 역학을 계약: "crouch-launch-land arc with visible weight settling", "not a mechanical repeat", "residual drops falling under gravity". 반복 동작·점프·소품 조작·천·물이 있으면 필수.
- **POSITIVE LOCKS 구성**: ①주어 수 락 ("Exactly one subject throughout") ②연속성 락 (시작 상태·경로 제한·"the room's interior design does not change") ③트릭 실행 락 ④다음 컷 인계 소품 상태 ("the faucet is still running, carrying into CUT N+1") ⑤IP 가드 ⑥통일 스타일 문자열. 부정문은 **"A, not B" 쌍**으로만 ("a circular vignette, not a rectangular wipe") — 금지만 하지 말고 대안을 같이.
- **컷 체인 (Anchor-and-Extend)**: 직전 컷 마지막 프레임을 continuity reference Element로 등록하고 FIRST FRAME을 그 상태와 일치시킨다. 마지막 컷엔 "This is the final clip — nothing follows it" 선언.
- **변신/모핑은 화면 밖으로**: 중간 단계를 요구하지 말고 오프스크린 처리 ("he goes in, the cat comes out, in one unbroken shot — reads as an in-camera trick rather than an edit").

**리비전 원리**: 결과가 틀리면 프롬프트를 갈아엎지 말고, 모델이 발명한 것을 금지+대안 쌍으로 락 블록에 증축한다. 공간이 복잡해 동선이 붕괴하면 프롬프트를 늘리지 말고 **세계를 단순화**한다 ("a small studio apartment: just two rooms, nothing else"). 증상별 레시피 표는 `higgsfield-structure.md` §8.

## 특수 컷 레시피 (Higgsfield 공식 Seedance 가이드 반영)

기본 모드 위에 겹쳐 쓰는 컷 유형별 오버라이드. 출처: higgsfield.ai/blog/seedance-prompting-guide.

**POV (1인칭) 컷** — 카메라가 곧 인물의 눈. 이 컷에서는 **멀티샷 위임 문장을 빼고** 아래로 대체한다 (명시적 부정이 없으면 Seedance가 기본값으로 앵글을 커팅해 시점이 깨진다):

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
| model | `seedance_2_0` |
| duration | 4~15 (기본 15) |
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

## 연계

- 대본이 `screenplay-pipeline` 포맷(`## S#N.`, `**이름:** 대사`, 지문)이면 씬을 그대로 파싱해 비트로 재배열한다: 지문 → 액션 비트, 대사 → 음절 예산 검사 후 배치, 씬의 마지막 감정 비트 → 버튼.
- 원작 IP가 있는 작품이면 프로젝트의 IP 체크리스트(예: `디즈니요소_체크리스트.md`)를 먼저 읽고 그 기준을 프롬프트에 반영한다.
- 여러 컷을 연속으로 뽑을 땐 통일 스타일 문자열과 Element ID를 컷 간에 동일하게 유지하고, 같은 장소 씬에는 블로킹 락 문장도 동일하게 유지한다.
