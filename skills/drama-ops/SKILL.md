---
name: drama-ops
description: AI 드라마/영상 제작의 반복 운영 작업 3종을 스크립트로 처리하는 스킬 — (1) 캐스팅·의상·스토리보드 후보 비교 보드 HTML 생성, (2) 렌더된 컷 영상의 QC 프레임 추출과 리테이크 비교 시트, (3) 컷 편성 → concat 버전 자동 관리 → ffmpeg 조립 → 조립 로그. 사용자가 "보드 만들어줘", "후보 보여줘", "비교해서 보여줘", "캐스팅 보드", "QC 뽑아줘", "프레임 확인", "리테이크 비교", "몇 번이 나아?", "합쳐줘", "조립해줘", "concat", "최종본/완성본 뽑아줘", "BGM 얹어줘"라고 하거나, 이미지 후보 여러 장을 고르는 상황, 영상 여러 테이크 중 선택하는 상황, 컷들을 이어붙이는 상황이면 반드시 이 스킬을 사용한다. 보드/시트 HTML을 손으로 직접 작성하지 말고 이 스킬의 스크립트를 쓸 것 (수 MB짜리 HTML을 매번 새로 쓰는 낭비 방지). ai-character-drama나 screenplay-pipeline 진행 중에도 보드·QC·조립 단계에서는 이 스킬의 스크립트를 사용한다.
---

# Drama Ops — 제작 운영 3종 세트

AI 드라마 제작에서 매번 반복되는 운영 작업(후보 보드, QC, 조립)을 스크립트로 처리한다.
모두 표준 라이브러리 + ffmpeg/sips만 쓴다. 산출물은 사용자의 프로젝트 폴더 규칙을 따른다:
보드 HTML은 프로젝트 루트, QC는 `qc/`, 편성표·완성본·로그는 `videos/`.

## 1. 후보 비교 보드 — `scripts/build_board.py`

캐스팅/의상/세트/스토리보드 후보를 번호 배지 달린 다크 테마 그리드로 보여주는 HTML을 만든다.
클릭하면 확대(라이트박스), 좌우 화살표로 넘기기. 사용자는 "2번" 식으로 고른다.

```bash
# 간단: 폴더 + 패턴으로 자동 수집
python3 scripts/build_board.py --title "엘라 볼가운 후보" \
  --dir characters --pattern "ella_ballgown_v2_*" \
  --ref "characters/ella_rags_v2_1.png:기준 얼굴(누더기 v2)" \
  --out 볼가운_보드.html

# 정교하게: 그룹/노트/푸터(비용 표)까지 manifest JSON으로
python3 scripts/build_board.py --manifest board.json --out 보드.html
```

- 기본으로 이미지를 base64 임베드하되 sips로 가로 1024px 축소본을 쓴다 → 기존처럼 3MB짜리
  HTML이 나오지 않는다. 원본 화질로 봐야 하면 `--max 0`, 파일을 아예 가볍게 하려면 `--no-embed`
  (단, 이미지 원본과 같은 디스크에서 열 때만).
- manifest 구조는 스크립트 상단 docstring 참고. 후보에 코멘트를 달아줄 때는 `note` 필드를 쓴다.
- 보드를 만든 뒤에는 `open <파일>` 로 열어주고, 사용자가 번호를 고르면 그 결과를
  project.json의 해당 element에 기록하는 것까지가 한 세트다 (pick 필드, 사용자 컨벤션).

## 2. QC 프레임 + 리테이크 비교 시트 — `scripts/qc_frames.py`

렌더된 컷마다 `qc/<컷이름>/f1~f5.jpg` (균등 간격, 마지막 프레임 포함)를 뽑고,
여러 테이크를 한 화면에서 줄줄이 비교하는 시트 HTML을 만든다.

```bash
# 리테이크 여러 개를 한 번에 QC + 비교 시트
python3 scripts/qc_frames.py --dir videos --glob "cut7R?.mp4" \
  --out qc --sheet qc/7R_비교시트.html --title "7컷 리테이크 비교"

# 특정 테이크 몇 개만: 파일을 위치 인자로 직접 지정
python3 scripts/qc_frames.py videos/cut7R4.mp4 videos/cut7R5.mp4 --out qc --sheet qc/시트.html
```

- glob 주의: 이 프로젝트들엔 `_v2`/`_v3` 변형 파일이 섞여 있어서 `cut7R*.mp4` 같은 넓은
  패턴은 원치 않는 파일까지 잡는다. 몇 개만 비교할 땐 위치 인자로 직접 지정하는 게 안전.
- 프레임 수는 기본 5장(`--frames N`으로 조절), 마지막 프레임은 항상 포함.
- `--out`/`--sheet`는 절대경로도 받는다. 기본 규칙은 프로젝트의 `qc/`지만 상황 따라 자유.
- 이미 추출된 폴더는 건너뛴다(재렌더 후 다시 뽑을 땐 `--force`).
- 렌더가 끝난 컷은 조립 전에 항상 이 QC를 먼저 돌리고, 시트를 열어 사용자가 고르게 한다.
- 시트에서 고른 결과("R7이 낫다")는 다음 단계인 조립의 `--cuts` 편성과 `--reason`에 반영한다.

## 3. 컷 편성 → 조립 → 로그 — `scripts/assemble.py`

concat 텍스트 버전 넘버링(v1, v2, ...)을 자동으로 관리하고, ffmpeg 조립과
`videos/assembly_log.json` 기록(어느 버전에 어떤 컷을 왜 넣었는지)까지 한 번에 한다.
`concat_v2.txt`, `concat_r.txt` 같은 파일이 난립하고 "어느 게 최신이지?"가 되는 문제를 막는다.

```bash
python3 scripts/assemble.py --videos-dir videos --name FULL_3부 \
  --cuts "cut1A,cut2B,cut3A,cut7R7,cut8A" \
  --reason "7컷을 R7로 교체 (표정 어색함 해결)" \
  --height 480 --bgm music/bgm.mp3
```

- 버전은 기존 `<name>*_vN` 파일들을 스캔해서 자동 +1. 수동으로 concat 파일을 만들지 말 것.
- 기본은 `-c copy`(빠름). 컷들의 코덱/해상도가 섞여 있으면 실패하는데, 그때는 `--reencode`.
  `--height`를 주면 자동으로 재인코딩 경로를 탄다.
- BGM은 사용자 컨벤션대로 볼륨 0.10, 컷별로 굽지 않고 완성본 위에 한 번만 얹는다
  (`--bgm-volume`으로 조정).
- 편성만 먼저 확정하고 싶으면 `--dry-run` (concat 텍스트 + 로그만 생성).
- 과거 조립 이력이 궁금하면 `videos/assembly_log.json`을 읽으면 된다. 사용자가
  "v4에 뭐 들어갔었지?"라고 물으면 이 로그를 본다.

## 흐름 요약

렌더 완료 → **2번 QC**로 프레임 뽑고 비교 시트 → 사용자가 테이크 선택 →
**3번 assemble**로 편성·조립·로그 → 최종 확인. 캐스팅/의상/스토리보드 확정 단계에서는
**1번 보드**로 후보를 보여주고 pick을 project.json에 기록.

주의: 이 스킬은 이미지를·영상을 "생성"하지 않는다. 생성은 ai-character-drama 스킬이나
스토리 스튜디오가 하고, 이 스킬은 그 산출물을 고르고·검수하고·묶는 운영 단계만 담당한다.
