#!/usr/bin/env python3
"""렌더된 컷 영상에서 QC 프레임을 뽑고, 리테이크 비교 시트 HTML을 만든다.

사용법:
  python3 qc_frames.py videos/cut7R1.mp4 videos/cut7R2.mp4 --out qc
  python3 qc_frames.py --dir videos --glob "cut7R*.mp4" --out qc --sheet qc/7R_비교시트.html

동작:
  - 영상마다 qc/<파일명스템>/f1.jpg ~ fN.jpg 생성 (균등 간격, 마지막 프레임 포함)
  - 같은 스템 폴더가 이미 있으면 덮어쓰지 않고 건너뜀 (--force 로 재추출)
  - --sheet 를 주면 영상별 한 줄(가로 프레임 나열) 비교 HTML 생성 — 리테이크 고르기용
"""
import argparse, glob as globmod, html, json, os, subprocess, sys
from pathlib import Path

def probe(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", str(path)], capture_output=True, text=True)
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        sys.exit(f"ffprobe 실패: {path}")

def extract(video: Path, outdir: Path, n: int, force: bool) -> list[Path]:
    d = outdir / video.stem
    existing = sorted(d.glob("f*.jpg")) if d.exists() else []
    if existing and not force:
        print(f"건너뜀(이미 있음): {d}  (--force 로 재추출)")
        return existing
    d.mkdir(parents=True, exist_ok=True)
    dur = probe(video)
    frames = []
    for i in range(1, n + 1):
        # 마지막 프레임은 끝에서 0.15초 앞(디코더가 정확히 끝을 못 잡는 경우 대비)
        t = max(0.0, dur - 0.15) if i == n else dur * (i - 1) / max(1, n - 1)
        f = d / f"f{i}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                        "-frames:v", "1", "-q:v", "3", str(f)], check=True)
        frames.append(f)
    print(f"추출: {video.name} → {d} ({n}프레임, {dur:.1f}s)")
    return frames

CSS = """
body{background:#14151a;color:#eee;font-family:-apple-system,'Malgun Gothic',sans-serif;padding:20px;margin:0}
h1{font-size:18px;margin:0 0 14px}
.row{background:#1d1f26;border-radius:12px;padding:10px 12px;margin-bottom:12px}
.row .name{font-size:14px;font-weight:700;color:#ffd54a;margin-bottom:6px}
.row .meta{color:#889;font-size:11px;margin-left:8px;font-weight:400}
.strip{display:flex;gap:6px;overflow-x:auto}
.strip img{height:150px;border-radius:6px;cursor:zoom-in}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}
#lb img{max-width:96vw;max-height:92vh}
#lb .lbl{position:fixed;top:12px;left:18px;color:#ffd54a;font-weight:700}
"""
JS = """
const imgs=[...document.querySelectorAll('.strip img')];const lb=document.getElementById('lb');
const lbi=lb.querySelector('img'),lbl=lb.querySelector('.lbl');let cur=0;
function show(i){cur=(i+imgs.length)%imgs.length;lbi.src=imgs[cur].src;lbl.textContent=imgs[cur].dataset.lb;lb.style.display='flex'}
imgs.forEach((im,i)=>im.addEventListener('click',()=>show(i)));
lb.addEventListener('click',()=>lb.style.display='none');
document.addEventListener('keydown',e=>{if(lb.style.display!=='flex')return;
 if(e.key==='Escape')lb.style.display='none';if(e.key==='ArrowRight')show(cur+1);if(e.key==='ArrowLeft')show(cur-1)});
"""

def build_sheet(rows, sheet_path: Path, title: str):
    parts = [f"<h1>{html.escape(title)}</h1>"]
    for name, dur, frames in rows:
        imgs = "".join(
            f'<img src="{html.escape(os.path.relpath(f, sheet_path.parent))}" '
            f'data-lb="{html.escape(name)} — {f.name}">' for f in frames)
        parts.append(f'<div class="row"><div class="name">{html.escape(name)}'
                     f'<span class="meta">{dur:.1f}s · {len(frames)}프레임</span></div>'
                     f'<div class="strip">{imgs}</div></div>')
    parts.append('<div id="lb"><span class="lbl"></span><img></div>')
    doc = (f'<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title>'
           f"<style>{CSS}</style>" + "\n".join(parts) + f"<script>{JS}</script>")
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_path.write_text(doc, encoding="utf-8")
    print(f"비교 시트: {sheet_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="*")
    ap.add_argument("--dir"); ap.add_argument("--glob", default="*.mp4")
    ap.add_argument("--out", default="qc")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--sheet", help="비교 시트 HTML 경로")
    ap.add_argument("--title", default="QC 리테이크 비교")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    vids = [Path(v) for v in a.videos]
    if a.dir:
        vids += [Path(p) for p in sorted(globmod.glob(str(Path(a.dir) / a.glob)))]
    vids = [v for v in vids if v.exists()]
    if not vids:
        sys.exit("대상 영상이 없음")

    outdir = Path(a.out)
    rows = []
    for v in vids:
        frames = extract(v, outdir, a.frames, a.force)
        rows.append((v.stem, probe(v), frames))
    if a.sheet:
        build_sheet(rows, Path(a.sheet), a.title)

if __name__ == "__main__":
    main()
