#!/usr/bin/env python3
"""캐스팅/의상/스토리보드 후보 비교 보드 HTML 생성기.

사용법:
  python3 build_board.py --title "엘라 볼가운 후보" --out board.html \
      --dir characters --pattern "ella_ballgown_v2_*" [옵션]
  python3 build_board.py --manifest board.json --out board.html

manifest JSON 구조:
{
  "title": "보드 제목",
  "subtitle": "번호로 골라주세요. 예: 2번",
  "ref": {"src": "characters/ella_rags_v2_1.png", "caption": "기준 얼굴"},
  "groups": [
    {"name": "그룹명", "items": [
      {"src": "characters/a.png", "label": "1", "note": "설명(선택)"}
    ]}
  ],
  "footer": "하단 비고(비용 표 등, HTML 허용)"
}
groups 없이 최상위 "items" 배열만 줘도 된다.

옵션:
  --no-embed     이미지를 base64로 심지 않고 상대경로로 참조 (HTML이 작아짐)
  --max N        임베드 전에 sips로 가로 N px 축소본을 만들어 씀 (기본 1024, 0=원본)
  --cols N       그리드 최소 카드 폭(px, 기본 280)
"""
import argparse, base64, fnmatch, html, json, mimetypes, os, subprocess, sys, tempfile
from pathlib import Path

CSS = """
body{background:#14151a;color:#eee;font-family:-apple-system,'Malgun Gothic',sans-serif;padding:24px;margin:0}
h1{font-size:20px;margin:0 0 6px} .sub{color:#aab;margin:0 0 18px}
h2{font-size:16px;color:#ffd54a;margin:26px 0 10px}
.ref{display:flex;gap:16px;align-items:center;margin-bottom:20px;background:#1d1f26;border-radius:14px;padding:14px;max-width:640px}
.ref img{width:130px;border-radius:10px;cursor:zoom-in}
.ref .cap{color:#aab;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(var(--minw),1fr));gap:18px}
.card{position:relative;background:#1d1f26;border-radius:14px;padding:10px}
.card img{width:100%;border-radius:10px;display:block;cursor:zoom-in}
.badge{position:absolute;top:18px;left:18px;background:#ffd54a;color:#222;font-size:22px;font-weight:800;min-width:44px;height:44px;padding:0 8px;border-radius:22px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.5)}
.fname{color:#778;font-size:11px;margin-top:8px;word-break:break-all}
.note{color:#cdd3e0;font-size:13px;margin-top:4px;white-space:pre-wrap}
.footer{margin-top:28px;color:#aab;font-size:13px}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}
#lb img{max-width:96vw;max-height:92vh;border-radius:8px}
#lb .lbl{position:fixed;top:14px;left:20px;color:#ffd54a;font-size:18px;font-weight:700}
"""
JS = """
const imgs=[...document.querySelectorAll('img[data-lb]')];const lb=document.getElementById('lb');
const lbi=lb.querySelector('img'),lbl=lb.querySelector('.lbl');let cur=0;
function show(i){cur=(i+imgs.length)%imgs.length;lbi.src=imgs[cur].src;lbl.textContent=imgs[cur].dataset.lb;lb.style.display='flex'}
imgs.forEach((im,i)=>im.addEventListener('click',()=>show(i)));
lb.addEventListener('click',()=>lb.style.display='none');
document.addEventListener('keydown',e=>{if(lb.style.display!=='flex')return;
 if(e.key==='Escape')lb.style.display='none';if(e.key==='ArrowRight')show(cur+1);if(e.key==='ArrowLeft')show(cur-1)});
"""

def img_src(path: Path, embed: bool, max_w: int, base: Path) -> str:
    if not embed:
        return html.escape(os.path.relpath(path, base))
    src_path, mime, tmp = path, mimetypes.guess_type(str(path))[0] or "image/png", None
    if max_w > 0:
        # 축소 + JPEG 변환 (PNG 원본을 그대로 임베드하면 보드가 수 MB로 커짐)
        try:
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tmp.close()
            subprocess.run(["sips", "--resampleWidth", str(max_w), "-s", "format", "jpeg",
                            "-s", "formatOptions", "80", str(path), "--out", tmp.name],
                           capture_output=True, check=True)
            src_path, mime = Path(tmp.name), "image/jpeg"
        except Exception:
            src_path = path  # sips 없거나 실패하면 원본 그대로
    data = base64.b64encode(src_path.read_bytes()).decode()
    if tmp:
        os.unlink(tmp.name)
    return f"data:{mime};base64,{data}"

def render_items(items, embed, max_w, base):
    cards = []
    for i, it in enumerate(items, 1):
        p = Path(it["src"]).expanduser()
        if not p.is_absolute():
            p = base / p
        if not p.exists():
            print(f"경고: 없음 — {p}", file=sys.stderr)
            continue
        label = str(it.get("label", i))
        note = f'<div class="note">{html.escape(it["note"])}</div>' if it.get("note") else ""
        cards.append(
            f'<div class="card"><span class="badge">{html.escape(label)}</span>'
            f'<img src="{img_src(p, embed, max_w, base)}" data-lb="{html.escape(label)} — {html.escape(p.name)}">'
            f'<div class="fname">{html.escape(p.name)}</div>{note}</div>')
    return "\n".join(cards)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest")
    ap.add_argument("--title", default="후보 보드")
    ap.add_argument("--subtitle", default="번호로 골라주세요. 예: '2번'")
    ap.add_argument("--dir"); ap.add_argument("--pattern", default="*")
    ap.add_argument("--ref", help="기준 이미지 경로[:캡션]")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--max", type=int, default=1024)
    ap.add_argument("--cols", type=int, default=280)
    a = ap.parse_args()

    out = Path(a.out).expanduser().resolve()
    base = out.parent
    m = {"title": a.title, "subtitle": a.subtitle}
    if a.manifest:
        m = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
        mbase = Path(a.manifest).expanduser().resolve().parent
    else:
        mbase = base
        if not a.dir:
            sys.exit("--manifest 또는 --dir 중 하나는 필요")
        d = Path(a.dir).expanduser()
        files = sorted(f for f in d.iterdir()
                       if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
                       and fnmatch.fnmatch(f.name, a.pattern))
        if not files:
            sys.exit(f"매칭 이미지 없음: {d}/{a.pattern}")
        m["items"] = [{"src": str(f)} for f in files]
        if a.ref:
            src, _, cap = a.ref.partition(":")
            m["ref"] = {"src": src, "caption": cap or "기준"}

    embed = not a.no_embed
    body = [f"<h1>{html.escape(m['title'])}</h1>",
            f"<p class=\"sub\">{html.escape(m.get('subtitle',''))}</p>"]
    if m.get("ref"):
        rp = Path(m["ref"]["src"]).expanduser()
        if not rp.is_absolute():
            rp = mbase / rp
        body.append(f'<div class="ref"><img src="{img_src(rp, embed, a.max, base)}" data-lb="기준 — {html.escape(rp.name)}">'
                    f'<div class="cap">{html.escape(m["ref"].get("caption","기준"))}<br>'
                    f'<span class="fname">{html.escape(rp.name)}</span></div></div>')
    groups = m.get("groups") or [{"name": None, "items": m.get("items", [])}]
    for g in groups:
        if g.get("name"):
            body.append(f"<h2>{html.escape(g['name'])}</h2>")
        body.append(f'<div class="grid">{render_items(g["items"], embed, a.max, mbase)}</div>')
    if m.get("footer"):
        body.append(f'<div class="footer">{m["footer"]}</div>')
    body.append('<div id="lb"><span class="lbl"></span><img></div>')

    doc = (f"<!doctype html><meta charset=\"utf-8\"><title>{html.escape(m['title'])}</title>"
           f"<style>{CSS}:root{{--minw:{a.cols}px}}</style>" + "\n".join(body) + f"<script>{JS}</script>")
    out.write_text(doc, encoding="utf-8")
    n = sum(len(g["items"]) for g in groups)
    print(f"완료: {out} (후보 {n}개, {out.stat().st_size//1024}KB)")

if __name__ == "__main__":
    main()
