# Prompt Mastery — 프롬프트 작법 노하우 (모델 불문 품질 유지용)

이 문서의 목적: **이 스킬을 실행하는 모델이 무엇이든** (Fable, Opus, Sonnet, 그 이후
모델) 프롬프트 품질이 같게 나오도록, "잘 쓴 프롬프트"의 판단 기준을 전부 명시한다.
템플릿(prompt-templates.md)이 뼈대라면 이 문서는 빈칸을 채우는 기준이다.

**실행 규칙: 어떤 프롬프트든(바이블·이미지·비디오·오디오) 제출하기 전에 이 문서
맨 아래의 셀프리뷰 루브릭을 반드시 통과시켜라.** 루브릭에 걸리면 제출하지 말고 고쳐라.

---

## 0. 메타 원칙 — 프롬프트는 소원이 아니라 연출 지시서다

생성 모델에게 프롬프트의 모든 문장은 셋 중 하나여야 한다:

1. **그릴 수 있는 시각적 사실** — "green silk robe with a gold dragon crest"
2. **타이밍이 있는 행동** — "0-5초: 병을 낚아채 햇빛에 비춰본다"
3. **제약** — "no background music", "speaks in Korean"

이 셋에 해당하지 않는 문장 — 분위기 희망("멋지게", "감동적으로"), 품질 기원
("masterpiece, best quality" 나열), 추상 형용사("aesthetic") — 은 토큰 낭비가 아니라
**해악**이다. 모델의 주의를 실제 지시에서 뺏어간다. 쓰지 말고 지워라.

판별법: **스토리보드 아티스트에게 이 문장을 주면 그릴 수 있는가?** 못 그리면 지운다.

- ❌ "The king is surprised and the scene is emotional"
- ✅ "The king's eyes widen; he drops the scroll and grips the bottle with both hands"

추상 감정은 반드시 **몸으로 번역**해서 쓴다. 놀람 = 눈 커짐 + 뭔가 떨어뜨림.
분노 = 이 악물기 + 주먹. 기쁨 = 제자리 뜀 + 박수. 이 번역이 연출의 절반이다.

---

## 1. 스토리 작법 — CREATIVE_BIBLE과 비트시트

프롬프트 품질의 상한은 스토리 설계에서 결정된다. 여기가 부실하면 뒤가 다 부실하다.

### 60초 구조 (4×15s 기준)

| 컷 | 역할 | 규칙 |
|----|------|------|
| 1 | 훅 + 설정 | **첫 3초 룰**: 반드시 행동 중간(mid-action)이나 시각적 의문으로 연다. 평화로운 설정샷으로 시작 금지 — 숏폼은 3초 안에 넘긴다. |
| 2 | 증폭 | 컷1의 문제가 커진다. 새 인물/새 정보 투입은 여기서. |
| 3 | 반전/절정 | 예상을 한 번 꺾는다. 감정 최고점. |
| 4 | 해소 + 버튼 | 결말 후 **마지막 1~2초에 '버튼'** — 짧은 리액션·한 줄 농담·표정 하나로 끝맺는다. 버튼 없는 엔딩은 밋밋하다. |

컷 수가 다르면(3컷, 6컷) 훅-증폭-반전-버튼의 비율만 유지하면 된다.

### 코미디 엔진

- **같은 자극, 다른 반응**: 코미디의 핵심은 캐릭터별 반응의 대비다. 같은 사건에
  A는 침착, B는 호들갑, C는 딴생각 — 이 대비가 곧 웃음이다. 캐릭터마다
  "코믹 결함(comedic flaw)" 하나를 바이블에 명시하고 모든 반응을 그 결함에서 뽑아라.
- **3의 법칙 후 파괴**: 같은 패턴 2번 반복 → 3번째에 비틀기.
- **리액션이 액션보다 웃기다**: 사건 자체보다 그걸 본 캐릭터의 얼굴에 시간을 줘라.
- **배경 개그 위임**: 코미디 컷에는 "add a subtle visual gag in the background" 한 줄로
  Seedance에게 개그 발명을 위임할 수 있다 (힉스필드 공식 팁). 직접 설계한 개그가
  메인이고 이건 보너스 레이어 — 메인 개그와 충돌할 것 같으면 생략.

### 더블 인트로 룰 (캐릭터 소개)

주요 캐릭터는 **두 번 소개한다** — 한 번은 정적인 장면에서 "누구인지"(관계·성격·
말버릇), 한 번은 행동으로 "뭘 할 수 있는지". 설명 대사로 캐릭터를 소개하지 말고
두 번째 소개(행동)가 첫 번째를 증명하게 설계하라. 60초물에서는 컷1(정적 훅)과
컷2(행동 증폭)에 자연스럽게 배치된다.

### 컷당 감정은 하나

한 컷에는 **지배 감정 하나**만 부여한다 (컷1=호기심, 컷2=공포, 컷3=환희…).
Seedance는 한 클립에 감정 하나를 줄 때 연기가 제일 좋다. 한 컷 안에서 감정을
두 번 바꾸려 하면 둘 다 어중간해진다. 감정 전환은 컷 경계에서 해라.

### 대사 작법 — 음절 예산이 전부다

- **한국어 발화 속도는 초당 5~6음절.** 15초 컷에서 연기·동작·침묵 빼면 실제 발화
  가능 시간은 6~9초 → **컷당 대사 총량 최대 2~3줄, 한 줄 15음절 이내**가 안전선.
  이걸 넘기면 Seedance가 대사를 잘라먹거나 립싱크가 무너진다.
- **구어체로 써라.** 문어체("그것은 무엇입니까")가 아니라 입말("그게 뭐야?").
  짧은 단문. 복문·만연체는 립싱크 품질을 직접 떨어뜨린다.
- **캐릭터마다 말버릇 하나**를 바이블에 정해라 ("~하옵니다", "헐", 반말/존대 대비).
  자막에서 캐릭터 개성이 공짜로 살아난다.
- 한 컷에 **화자는 2명 이하**가 안전하다. 3명 이상 말하면 립싱크가 섞인다.

---

## 2. 이미지 프롬프트 작법 (gpt_image_2)

### 절 순서 (앞에 올수록 강하게 반영된다)

```
[샷 타입/구도] → [주제 + 구체적 시각 앵커] → [통일 스타일 문자열(그대로)] → [배경] → [디테일 꼬리]
```

가장 중요한 것을 맨 앞에. "character reference sheet, single character, front-facing"이
스타일 묘사보다 앞에 오는 이유다.

### 얼굴 일관성 앵커 — "예쁘게"가 아니라 "구별되게"

Element 참조가 일관성의 90%를 해주지만, 시트 자체가 좋아야 한다. 시트 프롬프트에는:

- **나이 + 얼굴형 + 헤어(스타일·길이·색) + 구별 특징 2~3개**를 명시한다.
  구별 특징 = 점, 안경, 눈썹 모양, 수염, 흉터, 보조개 같은 **위치가 특정되는** 것.
- ❌ "beautiful, handsome, attractive" — 모델마다 기본값 미인상으로 수렴해서
  캐릭터끼리 다 닮아버린다. ✅ "distinctive"가 목표: "a round-faced man in his 50s
  with a thin grey goatee and heavy eyebrows, a small mole under his left eye"
- **캐릭터별 시그니처 컬러 + 셔츠/의복의 이름 텍스트**는 일관성 앵커이자 화면 라벨.
  의상은 색+소재+한 가지 특이점까지: "a jade-green silk robe with a gold crane crest".
- 한국인/한국 배경이면 **"Korean"을 명시**하고 시대 디테일을 붙여라(사극이면
  "Joseon-era", 관모/갓/한복 종류까지). 안 쓰면 국적 불명 얼굴이 나온다.

### 시트 구성 — Hell Grind 검증 핵 (상세: hellgrind-playbook.md §1)

- **3패널 합본 시트 = 한 장의 이미지(16:9)**: 뉴트럴 그레이 배경 위에
  `전신 앞모습(머리 없음) | 전신 뒷모습 | 3/4 뷰 대형 얼굴 클로즈업`을 나란히
  배치한 film character sheet — LIRA 원판("Three studio photographs of the same
  person arranged side by side") + Hell Grind의 headless 개선을 합친 규격이다.
  낱장 3장으로 쪼개지 말 것. headless 전신이 와이드 샷 얼굴 붕괴를 고친다 —
  시트 위의 작고 흐린 전신 얼굴을 모델이 참조해버리는 사고를 막고, 얼굴을
  가져올 곳이 클로즈업 하나뿐이 된다 ("얼굴 하나" 규칙의 구현법). 패널 간
  의상·체형 일관성 문구("Consistent across all three panels: ...")를 포함한다.
- **시트는 일부러 심심하게**: 뉴트럴 그레이 배경 + 플랫 라이트 + 무보정 피부.
  필름 그레인·시네 렌즈를 시트에 구우면 캐릭터가 새 조명에 반응을 멈춘다 —
  통일 스타일 문자열은 **비디오 프롬프트**에 넣고 시트에서는 뺀다.
- **캐치라이트 검사**: 동공에 빛 반사 없는 얼굴은 탈락 — 죽은 얼굴로는 연기가
  안 나온다. "예쁜 얼굴"이 아니라 "믿기는 얼굴"을 골라라.
- **포인트 변경(의상/흉터/피)은 마스킹 합성으로** — 이미지를 모델에 통째로 두 번
  돌리면 얼굴이 플라스틱이 된다. 완성 프레임 수정은 편집 레인 규율
  (hellgrind-playbook.md §5: CHANGE 최소 + PRESERVE EXACTLY 전수)로.
- **락 전 스트레스 테스트**: 다른 포즈·조명으로 3~5회(장편은 10회) 생성 — 전부
  알아볼 수 있어야 통과. 실패 원인은 모델이 아니라 묘사다.

### 상태/의상 변형 시트

같은 캐릭터의 의상·상태 변화(평상복→드레스, 마른→비 맞은)는 **변형마다 시트를
따로 만들어 별도 Element로 등록**한다. 하나의 시트에 텍스트로 "드레스 버전으로"를
시키면 얼굴이 드리프트한다. 변형 시트는 베이스 시트를 참조로 걸고 의상/상태만
바꿔 생성하면 얼굴이 유지된다. 그리고 **시트 프레임 안에 얼굴은 정확히 하나** —
클로즈업+전신 분할 패널처럼 얼굴이 두 번 보이면 영상 모델이 락을 못 잡는다.

### 부정문 금지 (이미지 프롬프트에서)

이미지 모델은 언급된 것을 그린다. "no hat"이라고 쓰면 모자가 나올 확률이 오히려
오른다. **없어야 할 것을 쓰지 말고, 있어야 할 것만 써라.**
유일한 예외: 배경 플레이트의 "no people" — 이건 표준 태그라 잘 먹는다.

### 얼굴/의상 분리 생성 (고난도 캐릭터용, 선택)

의상이 복잡하거나(갑옷, 정교한 드레스) 40컷 이상 쓸 주연이면, 한 번에 뽑지 말고
**얼굴 먼저 → 의상 별도 → 이미지 편집 모델로 합성**하는 3단계가 일관성이 더 좋다
(힉스필드 공식 워크플로). 플롯에 걸리는 디테일(벨트, 붕대, 특정 액세서리)은 합성
단계에서 전부 명시적으로 박아둔다 — "나중에 문제가 되기 전에". 마음에 드는 결과가
두 개로 갈리면 **둘을 편집 모델로 블렌딩**하면 직접 프롬프트로는 못 뽑는 결과가
나온다. 단순한 캐릭터는 기존 원패스 시트로 충분하다.

### 배경 플레이트 / 소품 샷

- 배경: wide + empty + **캐릭터가 들어갈 공간을 남긴 구도**. 시간대 조명 명시.
  조명·그레이드 톤은 색 이름 대신 **HEX 값**으로 고정하면 플레이트 간 톤 통일이
  쉬워진다 ("teal-orange grade, shadows #1a2b3c, highlights #ffd9a0").
- **플레이트는 3/4 앵글로 뽑아라.** 정면 플랫 구도의 로케이션 참조는 카메라가
  움직이는 순간 깊이가 없어서 붕괴한다. 3/4 앵글이 무빙을 버틴다.
- 소품/제품: 단일 오브젝트, 중앙, 뉴트럴 스튜디오 배경, **재질·라벨·마모 상태**까지
  묘사 ("a small antique green glass bottle with a cork, wax seal, slightly weathered").
  재질 묘사가 없으면 컷마다 재질이 바뀐다. 실제 제품은 생성 금지 — 실물 사진을 Element로.

---

## 3. 비디오 프롬프트 작법 (seedance_2_0) — 이 스킬의 심장

> **무대사(또는 대사 ≤1줄) + 액션/연속성 크리티컬 컷**(동물 주연, 변신 트릭,
> 프레임 체인, 추격·VFX 컷)은 이 콤팩트 규격 대신 `higgsfield-structure.md`의
> 구조 모드(12섹션, OPTICS 수치, HARD CUT 샷 설계, PHYSICS 계약, POSITIVE
> LOCKS)를 써라 — 짧은 한 줄 대사는 AUDIO 섹션에 verbatim 격리(Hell Grind 방식).
> 대화 중심 컷(대사 2줄+ / 화자 2명)은 아래 콤팩트 규격 그대로.

### 컷 프롬프트 해부도 (각 줄의 역할)

```
CUT 2 (0-15초).                                  ← 라벨: 파이프라인 추적용
<UNIFIED STYLE 그대로>, cinematic drama.          ← 스타일: 한 글자도 바꾸지 말 것
Location: <<<shore_joseon>>>, golden dusk light.  ← 공간 + 조명
<<<king>>> (the anxious king) and <<<minister>>>  ← 캐릭터: 태그 + 한 줄 역할
(his deadpan advisor) stand at the waterline,     ← 블로킹: 누가 어디에, 어떤 관계로
the king holding <<<bottle>>>.                    ← 소품도 손에 쥔 상태까지 명시
0-5초: [비트 1 — 행동 + 대사]                      ← 초당 비트: 리듬 가이드
5-10초: [비트 2]
10-15초: [비트 3 — 리액션으로 끝]
등장인물은 한국어로 말한다.                          ← 언어 클로즈 (필수)
멀티샷 연출 지시문 (아래 참조)                       ← 커버리지 지시 (필수)
no background music, no BGM, no soundtrack —      ← no-BGM 클로즈 (필수, 마지막 줄)
only spoken dialogue and natural diegetic sound.
```

### 비트 예산: 15초 = 3비트, 비트당 액션 1개

- 비트 하나(≈5초)에는 **물리적 액션 1개 + (선택) 대사 1줄**. 그 이상 욱여넣으면
  전부 뭉개진다. 밀도가 아쉬우면 액션을 줄이고 리액션 샷을 넣어라 — 그게 더 영화답다.
- 액션은 **구체적 동사**로: ❌ "the king is surprised by the bottle" →
  ✅ "the king snatches the bottle and holds it up against the sunset, squinting".
- 힘이 오가는 액션에는 **힘의 전달과 결과(consequence)**까지 써라: 반동·머리카락
  날림·무게 이동 등. "her hair blown back by the recoil, yet her hands remain firm
  on the levers" — 원인 동작만 쓰고 결과를 안 쓰면 물리감이 죽는다.
- 마지막 비트는 가급적 **리액션/표정**으로 끝내라. 다음 컷으로 넘어가는 호흡이 생긴다.
- 초 단위 타이밍은 **리듬 가이드**다. Seedance는 "정확히 7초에"를 못 지킨다.
  순서와 비중만 전달된다고 생각하고 써라.

### 카메라 문법 어휘 (프롬프트에 그대로 쓰는 영어 어휘)

| 어휘 | 용도 |
|------|------|
| establishing wide shot | 컷의 첫 비트, 공간 소개 |
| two-shot | 두 인물 대화 |
| over-the-shoulder (OTS) | 대화의 방향성/긴장 |
| close-up on <face/hands> | 감정 절정, 소품 강조 |
| insert shot of <<<prop>>> | 소품이 플롯 포인트일 때 |
| reaction shot | 코미디의 핵심 — 아끼지 마라 |
| slow push-in | 긴장 고조 |
| whip pan | 코믹한 급전환 |
| handheld, shaky | 다급함/혼란 |
| static locked-off shot | 데드팬 유머 (침착 캐릭터에) |
| RAMPS INTO SLOW MOTION → SNAPS BACK | 액션 정밀 순간 강조 (컷당 1회, 이 대문자 어휘 그대로) |
| body-rig locked on <subject> (snorricam) | 달리기/질주 — 피사체 고정, 배경만 모션블러로 질주감 |
| handheld with a fine 1–2 cm tremor | 다큐/중계 리얼리즘 (shaky보다 절제된 떨림) |
| one continuous shot, first-person POV, no cuts, no zoom | 1인칭 컷 — 멀티샷 위임 대신 사용, 손을 프레임에 상시 노출 |

멀티샷 지시는 샷을 초에 박아 고정하지 말고 **모델에게 편집권을 위임**하는 형태로:

```
edited as a multi-shot scene with motivated hard cuts between varied angles
(establishing, two-shot, close-ups, reaction, insert) chosen naturally to fit
the action and dramatic beats; dynamic cinematic coverage.
```

특정 순간에 특정 샷이 꼭 필요하면 그 비트 안에 한 번만 박아라
("10-15초: close-up — the minister's deadpan stare"). 전 비트에 샷을 지정하면
오히려 뚝뚝 끊긴다.

### 블로킹 — 공간 관계를 말로 그려라

모델이 제일 못 하는 게 암묵적 공간 추론이다. **누가 어디 서있고, 서로 어느 방향을
보고, 소품이 누구 손에 있는지**를 명시해라. "A and B talk"가 아니라
"A stands at the waterline facing the sea; B approaches from behind and stops at
his left shoulder". 인물이 3명 이상이거나 손 상호작용(주고받기, 악수)이 있으면
난이도가 급상승하니, 그런 비트는 단순화하거나 인서트 샷으로 처리해라.

**컷 간 블로킹 락 — 같은 장소가 2컷 이상 이어지면 필수.** Element는 얼굴을
고정하지만 위치는 못 고정한다. 컷마다 블로킹을 새로/다르게 쓰면 Seedance가
매 컷 배치를 재발명해서 A가 컷1에선 왼쪽, 컷2에선 오른쪽에 서는 좌우 반전이
난다 — 얼굴이 완벽해도 장면이 붕괴한다. 해결: 씬 단위로 **고정 블로킹 문장
하나**를 만들어 그 씬의 모든 컷 프롬프트에 **한 글자도 안 바꾸고** 복붙해라.
문장에 반드시 들어갈 것 세 가지:
1. **화면 기준 좌우** — "screen-left / screen-right"로 명시 (인물 기준 left가
   아니라 화면 기준. 모델이 헷갈리는 지점이다).
2. **바라보는 방향** — "facing right / facing each other across the table".
3. **축 유지 선언** — "all shots stay on the same side of the action axis
   (180-degree rule); the characters never swap screen sides between shots."

예: *"<<<king>>> sits on the screen-LEFT side of the table facing right;
<<<minister>>> stands screen-RIGHT facing left; all shots stay on the same side
of the action axis (180-degree rule); they never swap screen sides."*
멀티샷 위임 문장과 공존 가능 — 앵글·샷 사이즈는 모델이 고르되, 축과 좌우는
이 문장이 못박는다. 오버숄더/리버스 샷에서도 축만 지키면 좌우는 유지된다.

### 연기 디렉션 — 행동을 써라, 감정 말고 (본편: acting-system.md)

**연기의 대원칙: 감정 단어("sad/angry/shocked")를 쓰면 모델이 얕은 즉흥을
한다. 근육과 몸의 일로 써라** — 떨림, 악물렸다 풀리는 턱, 팽팽한 광대, 코로
새는 날숨. 캐릭터에겐 목표(상대를 향한 동사)와 장애물을 주고, 씬 안에서 싸우는
방식을 바꿔라(전술 전환 = 보이는 사건: 멈춤·자세·템포 변화). 상세 문법·마스터
프로필 템플릿·눈의 생명·앙상블 규칙은 `acting-system.md` — 바이블 단계에서
캐릭터당 마스터 프로필 + Voice 락을 확정하고 컷마다 각색한다.

대사에는 **연기 부사**를 붙여라 — 같은 줄도 연기가 달라진다:
"'그게 뭐야?' he whispers, not taking his eyes off the bottle" /
"through gritted teeth" / "deadpan, without looking up" / "bursting into laughter
mid-sentence". 붙이지 않으면 전부 평탄한 중립 톤으로 나온다.

살아있는 연기를 뽑는 검증된 어휘 (통일 스타일 문자열이나 컷 프롬프트에):
"micro-pauses before reactions, precise eye-line" (리액션 직전 미세 멈춤),
"living eyes with catch-lights, chest rise from breathing" (죽은 눈 방지),
"characters never just standing, always reacting" (배경 인물까지 살아있게),
"one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink" (단계적 깜빡임 —
살아있는 얼굴의 가장 값싼 신호), 정적 샷엔 마이크로 라이프 규칙 — 1~2초마다
가시적 미세사건 1개(숨이 가슴을 들어올림, 콧구멍, 눈썹). 정지는 "유지된
긴장"으로 — "nobody moves"는 프레임을 얼리는 금지 문구다.

### Hell Grind 컷 규칙 3종 (상세: hellgrind-playbook.md §4)

- **긍정형 액션만**: "does NOT fall on his back"은 무시되거나 반대로 나온다 →
  "falls on his stomach". (락 블록의 "A, not B" 쌍만 예외.)
- **나이 금지**: 젊은/아동 캐릭터의 나이는 어떤 언어로도 쓰지 마라 — 미성년
  판독 순간 필터가 급격히 엄격해진다. 역할·의상·행동으로 대체. 명백한 성인
  나이대("in his 50s")만 허용.
- **EXACT N 헤더**: 컷 첫 줄에 "EXACT N CHARACTERS — NO DUPLICATES: [이름들]" —
  모델은 사람을 추가하고 가구를 복제한다. 소품 수도 직접 락("exactly ONE
  mannequin, NEVER render a second one").
- 씬 첫 컷은 **첫 1초 배치 고정 와이드**(+"hm" 한마디 핵), 이음새 컷은 직전
  대사 꼬리를 첫 1초에 (§4.2). 복잡한 지리 씬은 블로킹 락 대신 **GEO SPATIAL
  LAYOUT** 블록 (§4.1).

### 통일 스타일 문자열 팔레트 (시네마틱 실사 프로젝트용)

프로젝트 스타일 문자열을 조립할 때 검증된 어휘군. 전부 넣으라는 게 아니라
프로젝트 톤에 맞는 걸 골라 **한 번 확정 후 불변**:

- 포맷: "8K IMAX commercial look" / "35mm film quality" / "light 35mm film grain"
- 리얼리즘 가드: "photorealistic — no 3D render, no game engine"
- 카메라 물리: "physical cine lens, 180° shutter motion blur, 24fps, no jitter"
- 피부: "pore-level realism — vellus hair, asymmetric moles, capillary flush"
  (단, 정책 필터가 민감한 프로젝트면 피부 묘사는 뺀다 — IP/정책 트러블슈팅 참조)
- 컬러: "60:30:10 dominant/secondary/accent, muted natural color grade,
  restrained saturation"
- 물리: "gravity and inertia respected — mass has real weight, correct contact
  shadows, no floating props"
- 구도: "rule of thirds + golden ratio"
- 연속성: "characters, props, environment identical across every cut, no
  identity drift"

### 특수 컷 (POV·격투·VFX·크리처·애니메이션·안무)

1인칭 POV 컷, 격투/추격 안무, 인라인 VFX 브래킷(`[VFX: ...]`), 포토리얼 크리처의
리얼리즘 가드("no 3D, no cartoon, no VFX look"), 비트 단위 완전 무음("NO MUSIC,
NO SFX"), 애니메이션 스타일 컷(3~4초 세그먼트 + style reference Element + 물리
키워드), 뮤지컬/안무 컷(음악 입력 Element + 장르 한 단어 위임)은
`seedance-cut-prompt` 스킬의 **특수 컷 레시피** 섹션 규격을 따른다.
핵심만: POV 컷에서는 멀티샷 위임 문장을 빼고 "One continuous shot, first-person
POV, no cuts, no zoom, natural head movement"로 대체하고 손을 프레임에 상시
노출시킨다. 격투는 안무를 비트 단위 동작으로 직접 쓰고 스피드 램프는
"RAMPS INTO SLOW MOTION / SNAPS BACK" 어휘 그대로.

### Seedance가 못 하는 것 (설계로 피해라)

- **화면 속 정확한 글자** (간판, 문서 텍스트) → 셔츠 이름처럼 Element에 구운 것만 유지된다. 나머지는 자막으로.
- **정확한 초 타이밍** → 리듬 가이드로만.
- **4명 이상 동시 등장** → 얼굴이 섞인다. 컷을 쪼개라.
- **복잡한 손 상호작용** → 인서트 샷으로 도피.
- **컷 안에서 의상/시간대 변화** → 불가. 컷 경계에서 바꿔라.

---

## 4. 오디오 프롬프트 작법

### SFX (ElevenLabs text_to_sound_effects)

**호출 1번 = 소리 1개.** 물리적으로 구체적으로, 길이 힌트와 함께:
- ❌ "beach sounds with seagulls and waves and wind"
- ✅ "a cork popping out of a glass bottle, close-up, short" (별도로 "gentle waves
  lapping on sand, loop") — 섞어 달라면 뭉개진 잡탕이 나온다. 믹싱은 ffmpeg가 한다.

### BGM (Suno, instrumental)

무드 아크 + 장르 + 템포 + 악기 편성 + 러닝타임을 말하고, **가사 유발 단어를 피해라**:
```
instrumental only. A ~60 second whimsical orchestral comedy score for a short
drama: starts curious and light (pizzicato strings, marimba), swells warmly in
the middle, ends with a playful button. No vocals, no drops, consistent tempo.
```
"song/lyrics/verse/chorus" 같은 단어를 쓰면 보컬이 샌다. 전체 러닝타임과 감정 곡선
(시작-중간-끝)을 명시하면 컷 경계와 자연스럽게 맞물린다.

### 내레이션 (TTS)

- 목소리는 **언어 네이티브 + 톤**으로 골라라 (한국어 콘텐츠에 영어 화자 목소리 금지).
- 내레이션 줄은 **들어갈 침묵 구간 길이에 맞춰 음절 예산**부터 계산하고 써라.
  안 들어가면 오디오를 포기하고 자막(narr 타입)으로 강등하는 게 원칙 (SKILL.md 오디오 설계 참조).

---

## 5. BAD → GOOD 대조 예시 (감각 이식용)

### 이미지 — 캐릭터 시트

❌ BAD:
```
A handsome king character, high quality, masterpiece, beautiful lighting, 4k
```
(그릴 수 있는 사실이 없다. "왕"의 기본값 얼굴이 나오고, 다음 왕과 구별 불가.)

✅ GOOD:
```
Character reference sheet, single character, front-facing 3/4 body portrait
centered, cinematic photorealistic live-action, natural skin texture, soft
natural daylight, warm color grade, clean neutral light-grey studio background.
A Korean king in his late 50s, round weathered face, thin grey goatee, heavy
brows, a small mole under his left eye, anxious darting eyes. Wears a
jade-green Joseon-era silk gonryongpo robe with a gold dragon crest. Full clear
face, consistent distinctive character design, high detail.
```

### 비디오 — 컷 비트

❌ BAD:
```
0-15초: 왕과 신하가 해변에서 병을 발견하고 놀라며 대화한다. 감동적이고 재밌게.
```
(액션 덩어리 하나에 15초, 감정 두 개, 연기 디렉션 없음, 대사 없음 → 밋밋한 15초.)

✅ GOOD:
```
0-5초: establishing wide — the king paces the waterline; <<<bottle>>> washes up
and bumps his foot. He freezes.
5-10초: he snatches it up and holds it against the dusk light, squinting.
'이게... 뭐야?' he whispers. The minister leans in over his shoulder.
10-15초: close-up reaction — the minister, deadpan: '전하, 쓰레기이옵니다.'
The king clutches the bottle protectively.
```

---

## 6. 셀프리뷰 루브릭 — 제출 전 강제 체크 (Fable 시뮬레이터)

**모든 생성 호출 직전에 아래를 실제로 순회하라.** 하나라도 걸리면 수정 후 재검사.
이 루브릭이 이 문서의 존재 이유다 — 판단력을 체크리스트로 강제한다.

```
공통
[ ] 소원 문장 스캔: 스토리보드 아티스트가 못 그리는 문장이 있는가? → 삭제/몸으로 번역
[ ] 통일 스타일 문자열이 project.json과 한 글자도 다르지 않은가?
[ ] AR이 project.json과 일치하는가? (이미지 quality:"high", resolution:"2k" 포함)

이미지 프롬프트
[ ] 절 순서: 구도 → 주제+앵커 → 스타일 → 배경 순인가?
[ ] 얼굴 앵커: 나이/얼굴형/헤어/구별 특징 2개 이상? "beautiful"류 형용사 없음?
[ ] 부정문 없음? ("no people" 배경 플레이트 예외)

비디오 프롬프트
[ ] 매트릭스 대조: 이 컷 행의 모든 entity가 <<<id>>>로 들어갔는가? (최다 실패 원인)
[ ] 비트 예산: 비트당 액션 1개 이하? 15초에 3비트 이하?
[ ] 대사 예산: 컷당 ≤3줄, 줄당 ≤15음절, 구어체, 화자 ≤2명?
[ ] 지배 감정 하나? 연기 부사 붙었나? 마지막 비트가 리액션인가?
[ ] 블로킹: 누가 어디에·소품이 누구 손에 있는지 명시됐나?
[ ] 블로킹 락: 같은 장소 2컷+ 씬이면 고정 블로킹 문장(screen-left/right + 방향 + 180도 축)이 그 씬 모든 컷에 동일하게 들어갔는가? (지리 복잡하면 GEO SPATIAL LAYOUT 블록으로)
[ ] 멀티샷 위임 지시문 + 언어 클로즈 + no-BGM 클로즈(마지막 줄) 3종 세트 있는가?
[ ] Seedance 불가능 목록(정확한 글자/4인 이상/복잡한 손동작) 요구하고 있지 않은가?
[ ] 길이: 120~250단어 사이인가? 250 초과면 가치 낮은 절부터 잘라라 (희석 방지)
[ ] 긍정형: "does NOT ..."류 부정 액션이 없는가? (락 블록 "A, not B" 쌍 예외)
[ ] 나이: 젊은/아동 캐릭터에 나이 표기가 없는가? (성인 나이대만 허용)
[ ] 연기: 감정 단어 대신 근육·몸·숨으로 썼는가? 캐릭터에 목표 동사가 있는가? (acting-system.md §9)
[ ] 컨텍스트 격리: 스테일 @태그·씬 요약·"previously"류가 없는가?
[ ] 씬 첫 컷이면: 첫 1초 배치 고정 와이드가 있는가? 이음새 컷이면 직전 대사 꼬리를 넣었는가?

스토리 (바이블/스토리보드 단계)
[ ] 컷1 첫 3초가 행동/의문으로 시작하는가?
[ ] 마지막 컷에 버튼이 있는가?
[ ] 캐릭터별 코믹 결함 + 말버릇이 정의됐고 반응이 서로 대비되는가?
```

## 7. 결과가 실망스러울 때 — 진단 → 최소 수정

재생성 전에 **어느 층이 실패했는지** 진단하고 그 층만 고쳐라. 프롬프트 전체를
갈아엎으면 잘 되던 부분까지 복불복으로 돌아간다.

| 증상 | 원인 층 | 최소 수정 |
|------|---------|-----------|
| 얼굴/소품이 다르게 나옴 | 태그 누락 | 매트릭스 행 재대조, <<<id>>> 추가만 |
| 액션이 뭉개짐/생략됨 | 비트 과적 | 액션 수를 줄인다 (묘사를 늘리는 게 아니라) |
| 연기가 밋밋함 | 디렉션 부재 | 연기 부사 + 리액션 샷 추가 |
| 대사 잘림/립싱크 붕괴 | 음절 초과 | 대사를 줄인다 (15음절 이내로) |
| 화면이 어수선함 | 프롬프트 과밀 | 250단어 밑으로 감량, 감정 1개로 축소 |
| 스타일이 컷마다 다름 | 스타일 문자열 변형 | 원본 문자열 복붙으로 교체 |
| 인물 위치/좌우가 컷마다 바뀜 | 블로킹 락 부재 | 씬 고정 블로킹 문장을 모든 컷에 동일 복붙 후 위반 컷만 재생성 |
| 랜드마크(우물·탁자 등)가 컷마다 프레임 안에서 이동, 카메라가 그 주위를 공전 | 블로킹 락만 있고 GEO 부재 | GEO SPATIAL LAYOUT으로 교체 — 특히 `IN FRAME`(랜드마크의 프레임 내 위치 + 금지 위치)과 `CAMERA BASE`(거리·높이 + "축을 따라 IN") 두 줄 (hellgrind-playbook.md §4.1) |
| 소품의 **형태·재질**이 참조와 다르게 나옴 (양철 물통 → 도자기 병) | 텍스트 락의 한계 | 부정문("never a ceramic jug")을 더 박아도 안 먹는다 — 소품은 텍스트가 아니라 **참조 이미지 우선순위** 문제다. 소품을 별도 Element로 등록하고, 프롬프트에서 소품 묘사를 뒤쪽 꼬리가 아니라 인물 절 바로 옆 앞쪽으로 올려라 |
| 음악이 샘 | no-BGM 클로즈 약함 | 클로즈를 마지막 줄로 이동 + 강화 후 재생성 |
```
