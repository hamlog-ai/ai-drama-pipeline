#!/usr/bin/env python3
"""컷 편성 → concat 파일 자동 버전 관리 → ffmpeg 조립 → 조립 로그 기록.

사용법:
  python3 assemble.py --videos-dir videos --name FULL_3부 \
      --cuts cut1A,cut2B,cut3A,cut7R7 --reason "7컷 R7로 교체" [옵션]

동작:
  1. videos/concat_<name>_vN.txt 생성 (N = 기존 버전 자동 +1)
  2. ffmpeg concat (기본 -c copy, --reencode 시 재인코딩, --height 로 스케일)
  3. --bgm 을 주면 BGM을 낮은 볼륨(기본 0.10)으로 얹은 *_bgm.mp4 추가 생성
  4. videos/assembly_log.json 에 {버전, 일시, 컷 목록, 사유, 산출물} 기록

옵션:
  --dry-run     concat 텍스트와 로그만 쓰고 ffmpeg는 안 돌림
  --out-dir     산출물 폴더 (기본 --videos-dir)
"""
import argparse, datetime, json, re, subprocess, sys
from pathlib import Path

def next_version(vdir: Path, out_dir: Path, name: str) -> int:
    pat = re.compile(re.escape(name) + r".*_v(\d+)", re.IGNORECASE)
    vs = [0]
    for d in {vdir, out_dir}:
        for f in d.iterdir():
            m = pat.search(f.name)
            if m:
                vs.append(int(m.group(1)))
    return max(vs) + 1

def run(cmd):
    print("$", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos-dir", required=True)
    ap.add_argument("--name", required=True, help="예: FULL_3부")
    ap.add_argument("--cuts", required=True, help="쉼표 구분. 확장자 생략 가능 (기본 .mp4)")
    ap.add_argument("--reason", default="")
    ap.add_argument("--out-dir")
    ap.add_argument("--height", type=int, help="세로 해상도로 스케일 (재인코딩 포함), 예: 480")
    ap.add_argument("--reencode", action="store_true")
    ap.add_argument("--bgm"); ap.add_argument("--bgm-volume", type=float, default=0.10)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    vdir = Path(a.videos_dir).resolve()
    out_dir = Path(a.out_dir).resolve() if a.out_dir else vdir
    out_dir.mkdir(parents=True, exist_ok=True)

    cuts = []
    for c in a.cuts.split(","):
        c = c.strip()
        if not c:
            continue
        p = vdir / (c if c.lower().endswith(".mp4") else c + ".mp4")
        if not p.exists():
            sys.exit(f"컷 파일 없음: {p}")
        cuts.append(p)
    if not cuts:
        sys.exit("컷 목록이 비었음")

    v = next_version(vdir, out_dir, a.name)
    concat_txt = vdir / f"concat_{a.name}_v{v}.txt"
    concat_txt.write_text("".join(f"file '{p.name}'\n" for p in cuts), encoding="utf-8")
    print(f"편성표: {concat_txt} ({len(cuts)}컷)")

    output = out_dir / f"{a.name}_v{v}.mp4"
    if not a.dry_run:
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt)]
        if a.height or a.reencode:
            if a.height:
                cmd += ["-vf", f"scale=-2:{a.height}"]
            cmd += ["-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k"]
        else:
            cmd += ["-c", "copy"]
        cmd.append(str(output))
        try:
            run(cmd)
        except subprocess.CalledProcessError:
            sys.exit("concat 실패 — 컷들의 코덱/해상도가 다르면 --reencode 를 붙여서 다시 실행")
        print(f"완성본: {output}")

    bgm_out = None
    if a.bgm and not a.dry_run:
        bgm_out = out_dir / f"{a.name}_v{v}_bgm.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(output), "-i", str(Path(a.bgm)),
             "-filter_complex",
             f"[1:a]volume={a.bgm_volume},apad[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             str(bgm_out)])
        print(f"BGM 버전: {bgm_out}")

    log_path = vdir / "assembly_log.json"
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    log.append({
        "name": a.name, "version": v,
        "at": datetime.datetime.now().isoformat(timespec="seconds"),
        "cuts": [p.name for p in cuts], "reason": a.reason,
        "concat": concat_txt.name,
        "output": None if a.dry_run else output.name,
        "bgm": bgm_out.name if bgm_out else None,
    })
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"로그 기록: {log_path} (v{v})")

if __name__ == "__main__":
    main()
