#!/usr/bin/env python3
"""
build_bundle.py — bundle No410 into a single self-contained HTML file.

Reads index.html + assets/, inlines CSS, JS, all images (base64), and the
hero video sources. Output is written to dist/no410_bundle.html.

Usage:
  python3 scripts/build_bundle.py
"""
import base64, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()

def mime_for(p: pathlib.Path) -> str:
    return {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png",
            "mp4":"video/mp4","webm":"video/webm"}.get(p.suffix.lstrip("."),"application/octet-stream")

def main():
    html = (ROOT/"index.html").read_text(encoding="utf-8")
    css  = (ROOT/"assets/style.css").read_text(encoding="utf-8")
    js   = (ROOT/"assets/main.js").read_text(encoding="utf-8")

    # 1) Inline CSS in place of <link rel="stylesheet" ...>
    html = re.sub(r'<link rel="stylesheet" href="assets/style\.css">',
                  lambda m: f'<style>{css}</style>', html, count=1)

    # 2) Rewrite main.js: replace external image/video loading with embedded data URIs.
    #    Build a dict mapping each image filename -> data URI.
    img_dir = ROOT/"assets/images"
    img_data = {p.name: f"data:{mime_for(p)};base64,{b64(p)}" for p in img_dir.iterdir() if p.is_file()}

    # Replace the assets/images/<file> path resolution with a lookup table
    inject = "\nconst IMG_DATA = " + repr(img_data) + ";\n"
    js = inject + js.replace("'assets/images/'+IMG_FILES[k]",
                             "IMG_DATA[IMG_FILES[k]]") \
                    .replace("'assets/images/'+IMG_FILES.eeg_logo",
                             "IMG_DATA[IMG_FILES.eeg_logo]")

    # Replace video source paths with data URIs
    v_dir = ROOT/"assets/video"
    v_mp4   = f"data:video/mp4;base64,{b64(v_dir/'hero.mp4')}"
    v_webm  = f"data:video/webm;base64,{b64(v_dir/'hero.webm')}"
    v_poster= f"data:image/jpeg;base64,{b64(v_dir/'hero_poster.jpg')}"
    js = js.replace("'assets/video/hero_poster.jpg'", repr(v_poster))
    js = js.replace("'assets/video/hero.webm'", repr(v_webm))
    js = js.replace("'assets/video/hero.mp4'",  repr(v_mp4))

    # 3) Inline JS in place of <script src="assets/main.js"></script>
    html = re.sub(r'<script src="assets/main\.js"></script>',
                  lambda m: f'<script>{js}</script>', html, count=1)

    out = DIST/"no410_bundle.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ wrote {out.relative_to(ROOT)}  ({out.stat().st_size//1024} KB)")

if __name__ == "__main__":
    main()
