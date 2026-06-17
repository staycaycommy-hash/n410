#!/usr/bin/env python3
"""
build_brochure.py — compose the No410 brand narrative into a luxury A4 PDF brochure.
Uses ReportLab for layout and Pillow for image cover-cropping + gradient overlays.
Output: dist/No410_Brochure.pdf
"""
import os, pathlib, tempfile
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG  = ROOT / "assets" / "images"
DIST = ROOT / "dist"; DIST.mkdir(exist_ok=True)
TMP  = pathlib.Path(tempfile.mkdtemp(prefix="no410_"))

PW, PH = A4  # 595.28 x 841.89

# ---- palette (from site CSS) ----
INK      = Color(*[c/255 for c in (0x15,0x16,0x1a)])
IVORY    = Color(*[c/255 for c in (0xf3,0xf1,0xec)])
PAPER    = Color(*[c/255 for c in (0xe9,0xe7,0xe1)])
BRONZE   = Color(*[c/255 for c in (0x9a,0x6a,0x3c)])
BRONZE_L = Color(*[c/255 for c in (0xb8,0x8a,0x5b)])
CONCRETE = Color(*[c/255 for c in (0x6f,0x71,0x77)])
WHITE    = Color(1,1,1)
INK_SOFT = Color(*[c/255 for c in (0x6f,0x71,0x77)])

# ---- fonts (macOS Didot + Avenir) ----
SF = "/System/Library/Fonts/Supplemental/"
def reg(name, path, idx):
    try:
        pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx)); return True
    except Exception:
        return False
# Display serif — Georgia has reliable metrics (Didot.ttc width metrics are broken in ReportLab)
DISP = "Didot"
reg("Didot", SF+"Georgia.ttf", 0)
reg("Didot-It", SF+"Georgia Italic.ttf", 0)
# Avenir (sans for labels)
SANS = "Avenir"
ok=False
for i in (0,1,2,3,4):
    if reg("Avenir", SF+"Avenir.ttc", i): ok=True; break
if not ok: reg("Avenir", "/System/Library/Fonts/Helvetica.ttc", 0)
SANS_B="Avenir-Heavy"
hb=False
for i in (5,6,7,8,3,2):
    if reg("Avenir-Heavy", SF+"Avenir.ttc", i): hb=True; break
if not hb: SANS_B = SANS

# ---- image helpers ----
def cover(src, w, h, darken_bottom=0.0, darken_all=0.0, name=None):
    """Cover-crop src to w:h aspect (pixels scaled x2 for print), optional gradient/darken."""
    im = Image.open(src).convert("RGB")
    tw, th = int(w*2), int(h*2)
    sr, tr = im.width/im.height, tw/th
    if sr > tr:
        nw = int(im.height*tr); im = im.crop(((im.width-nw)//2,0,(im.width-nw)//2+nw,im.height))
    else:
        nh = int(im.width/tr); im = im.crop((0,(im.height-nh)//2,im.width,(im.height-nh)//2+nh))
    im = im.resize((tw,th), Image.LANCZOS)
    if darken_all>0:
        ov = Image.new("RGB",(tw,th),(0,0,0)); im = Image.blend(im,ov,darken_all)
    if darken_bottom>0:
        grad = Image.new("L",(1,th),0);
        for y in range(th):
            t=y/th; a=max(0,(t-(1-darken_bottom))/darken_bottom) if darken_bottom else 0
            grad.putpixel((0,y),int(255*min(1,a)*0.82))
        grad = grad.resize((tw,th))
        black = Image.new("RGB",(tw,th),(0,0,0))
        im = Image.composite(black, im, grad)
    out = TMP / (name or (pathlib.Path(src).stem+f"_{w}x{h}.jpg"))
    im.save(out,"JPEG",quality=90); return str(out)

def fit(src, w, h, name=None):
    """Contain src within w:h, return (path, draw_w, draw_h) preserving aspect."""
    im = Image.open(src).convert("RGB")
    r = min(w/im.width, h/im.height)
    dw, dh = im.width*r, im.height*r
    out = TMP / (name or (pathlib.Path(src).stem+"_fit.jpg"))
    im.save(out,"JPEG",quality=90); return str(out), dw, dh

# ---- text helpers ----
def tracked(c, x, y, s, font, size, color, track, align='left'):
    w = c.stringWidth(s,font,size)+track*max(0,len(s)-1)
    if align=='center': x -= w/2
    elif align=='right': x -= w
    to = c.beginText(x,y); to.setFont(font,size); to.setFillColor(color)
    to.setCharSpace(track); to.textOut(s); to.setCharSpace(0)  # reset; Tc persists in PDF state
    c.drawText(to); return w

def wrap(c, s, font, size, maxw):
    words=s.split(); lines=[]; cur=""
    for wd in words:
        t=(cur+" "+wd).strip()
        if c.stringWidth(t,font,size)<=maxw: cur=t
        else: lines.append(cur); cur=wd
    if cur: lines.append(cur)
    return lines

def paragraph(c, x, y, s, font, size, color, maxw, leading, align='left'):
    c.setFillColor(color)
    for ln in wrap(c,s,font,size,maxw):
        c.setFont(font,size)
        if align=='center': c.drawCentredString(x,y,ln)
        else: c.drawString(x,y,ln)
        y-=leading
    return y

def rule(c, x, y, w, color=BRONZE, lw=1):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(x,y,x+w,y)

# =====================================================================
c = canvas.Canvas(str(DIST/"No410_Brochure.pdf"), pagesize=A4)
MX = 54  # text margin

# ---------- 1. COVER ----------
c.drawImage(cover(IMG/"light1.jpg", PW, PH, darken_bottom=0.6, darken_all=0.12, name="cover.jpg"),
            0,0,PW,PH)
tracked(c, PW/2, PH-70, "TVX GROUP  ·  REAL ESTATE", SANS, 8.5, Color(1,1,1,0.85), 3.2, 'center')
# big mark
c.setFont(DISP, 132); c.setFillColor(WHITE)
c.drawCentredString(PW/2, 250, "N°410")
rule(c, PW/2-26, 232, 52, BRONZE_L, 1.2)
tracked(c, PW/2, 196, "WHERE YOU TRULY BELONG", SANS, 11, WHITE, 5.0, 'center')
tracked(c, PW/2, 120, "HILLTOP  ·  MIRI, SARAWAK", SANS, 8.5, Color(1,1,1,0.7), 3.5, 'center')
c.showPage()

# ---------- 2. THE PURSUIT (opening prose) ----------
c.setFillColor(IVORY); c.rect(0,0,PW,PH,fill=1,stroke=0)
tracked(c, MX, PH-120, "A DESTINATION AFTER SUCCESS", SANS, 9, BRONZE, 3.5)
rule(c, MX, PH-138, 40, BRONZE, 1)
tease=("For most of our lives we are chasing — the next milestone, the next version "
       "of ourselves. The city is the stage where those dreams are built. Yet in time, "
       "success changes what it means: measured no longer by what we acquire, but by "
       "what we choose to protect.")
paragraph(c, MX, PH-200, tease, DISP, 23, INK, PW-2*MX, 33)
tracked(c, MX, 110, "OUR FAMILY · OUR TIME · OUR PEACE · OUR FUTURE", SANS, 8, CONCRETE, 2.6)
c.showPage()

# ---------- 3. THE ARRIVAL (image + lead) ----------
imgH = PH*0.62
c.drawImage(cover(IMG/"drone.jpg", PW, imgH, darken_bottom=0.5, name="arrival.jpg"),
            0, PH-imgH, PW, imgH)
tracked(c, MX, PH-imgH+30, "THE ARRIVAL", SANS, 9, WHITE, 4.0)
c.setFillColor(IVORY); c.rect(0,0,PW,PH-imgH,fill=1,stroke=0)
ly=PH-imgH-58
tracked(c, MX, ly, "WHERE EVERY RETURN FEELS MEANINGFUL", SANS, 8.5, BRONZE, 3.0)
lead=("Arriving here is not about reaching a destination. It is about finding the one "
      "place where you can finally exhale — where every return feels meaningful, and "
      "the noise of the day is left at the gate.")
paragraph(c, MX, ly-34, lead, DISP, 17.5, INK, PW-2*MX, 26)
c.showPage()

# ---------- 4–6. THE BELONGING (three spreads) ----------
belong=[("sun.jpg","Mornings that belong to you.",
         "Here mornings begin with stillness, not urgency. The first hour belongs to the "
         "kitchen, the long table, the children, and the lawn beyond the glass — and already, "
         "the day feels enough."),
        ("light2.jpg","Evenings that belong to family.",
         "At dusk the evenings belong to family, not to work. Soft light, quiet conversation, "
         "laughter around the table — the everyday moments that quietly become a lifetime of memory."),
        ("side.jpg","A place to grow up in.",
         "Water, shade, and open green to run through — a childhood surrounded by nature. "
         "The home holds its garden the way a family holds its years — generously, and without hurry.")]
for i,(img,title,body) in enumerate(belong):
    ih = PH*0.55
    c.drawImage(cover(IMG/img, PW, ih, name=f"bel{i}.jpg"), 0, PH-ih, PW, ih)
    c.setFillColor(IVORY); c.rect(0,0,PW,PH-ih,fill=1,stroke=0)
    y=PH-ih-60
    if i==0:
        tracked(c, MX, y, "THE BELONGING", SANS, 9, BRONZE, 4.0); y-=30
    tracked(c, MX, y, f"0{i+1}", SANS, 9, BRONZE_L, 2)
    c.setFont(DISP,27); c.setFillColor(INK); c.drawString(MX+26,y,title)
    paragraph(c, MX, y-40, body, DISP, 15.5, INK_SOFT, PW-2*MX, 24)
    c.showPage()

# ---------- 7. THE STUDIES (gallery) ----------
c.setFillColor(INK); c.rect(0,0,PW,PH,fill=1,stroke=0)
tracked(c, MX, PH-70, "A LIFE, IN GLIMPSES", SANS, 9, BRONZE_L, 3.5)
paragraph(c, MX, PH-100, "Not drawings of a house, but glimpses of a life — the garden at "
          "golden hour, the walled calm, and the unhurried approach home.", DISP, 14, WHITE, PW-2*MX, 21)
gx=MX; gy=PH-150; gw=PW-2*MX
# big image
bigh=190
c.drawImage(cover(IMG/"d_big.jpg", gw, bigh, name="g_big.jpg"), gx, gy-bigh, gw, bigh)
# 2x2 of smaller
small=["d_aerial.jpg","d_t1.jpg","d_t2.jpg","d_t3.jpg"]
cw=(gw-12)/2; ch=128; sy=gy-bigh-14
for k,s in enumerate(small):
    r,cc=divmod(k,2)
    x=gx+cc*(cw+12); yy=sy-r*(ch+12)
    c.drawImage(cover(IMG/s, cw, ch, name=f"g{k}.jpg"), x, yy-ch, cw, ch)
c.showPage()

# ---------- 8. FLOOR PLANS ----------
c.setFillColor(IVORY); c.rect(0,0,PW,PH,fill=1,stroke=0)
tracked(c, MX, PH-70, "THE PLANS", SANS, 9, BRONZE, 3.5)
c.setFont(DISP,22); c.setFillColor(INK); c.drawString(MX, PH-100, "Drawn for the way it lives.")
half=(PH-150)/2
for j,(plan,lab) in enumerate([("plan_ground.png","GROUND FLOOR"),("plan_first.png","FIRST FLOOR")]):
    band_top = PH-130 - j*half
    p,dw,dh = fit(IMG/plan, PW-2*MX, half-34, name=f"plan{j}.jpg")
    c.drawImage(p, (PW-dw)/2, band_top-dh-20, dw, dh)
    tracked(c, MX, band_top-4, lab+"  ·  SCALE 1:150", SANS, 8, CONCRETE, 2.6)
c.showPage()

# ---------- 9. THE DOSSIER ----------
c.setFillColor(INK); c.rect(0,0,PW,PH,fill=1,stroke=0)
tracked(c, MX, PH-90, "THE DOSSIER", SANS, 9, BRONZE_L, 3.5)
rows=[("Expected Completion","End 2026"),("Offered At","RM 3,580,000"),
      ("Tenure","Detached · Individual Title")]
y=PH-150
for l,v in rows:
    tracked(c, MX, y, l.upper(), SANS, 8, CONCRETE, 2.6)
    c.setFont(DISP,22); c.setFillColor(WHITE); c.drawString(MX, y-30, v)
    rule(c, MX, y-50, PW-2*MX, Color(1,1,1,0.12), 0.6); y-=84
# ledger
y-=10
tracked(c, MX, y, "THE RESIDENCE", SANS, 8.5, BRONZE_L, 3.0); y-=34
ledger=[("Bedrooms","4"),("Bathrooms","5"),("Walk-in Wardrobe","1"),
        ("Covered Porch","3 Cars"),("Built-up Area","3,406.77 ft²"),
        ("Garden","Wrap-around"),("Frontage","22.2 m")]
for l,v in ledger:
    c.setFont(SANS,9.5); c.setFillColor(Color(1,1,1,0.55)); c.drawString(MX,y,l)
    c.setFont(DISP,13); c.setFillColor(WHITE); c.drawRightString(PW-MX,y,v)
    y-=27
c.showPage()

# ---------- 10. THE LEGACY / CONTACT ----------
c.drawImage(cover(IMG/"front.jpg", PW, PH, darken_all=0.55, name="legacy.jpg"),0,0,PW,PH)
tracked(c, PW/2, PH-110, "THE LEGACY", SANS, 9, BRONZE_L, 4.0, 'center')
c.setFont(DISP,26); c.setFillColor(WHITE)
c.drawCentredString(PW/2, PH-260, "Some houses are built for today.")
c.drawCentredString(PW/2, PH-296, "Some homes are built for generations.")
rule(c, PW/2-26, PH-330, 52, BRONZE_L, 1.2)
c.setFont(DISP, 40); c.setFillColor(WHITE); c.drawCentredString(PW/2, 300, "N°410")
tracked(c, PW/2, 268, "WHERE YOU TRULY BELONG", SANS, 10, BRONZE_L, 4.5, 'center')
# contact block
tracked(c, PW/2, 188, "ARRANGE A PRIVATE VIEWING", SANS, 8.5, WHITE, 3.0, 'center')
c.setFont(SANS,10); c.setFillColor(Color(1,1,1,0.85))
c.drawCentredString(PW/2, 166, "hello@no410.my")
tracked(c, PW/2, 96, "AUTHORISED MARKETING AGENCY · PRESENTED BY", SANS, 7.5, Color(1,1,1,0.6), 2.6,'center')
c.setFont(SANS_B,13); c.setFillColor(WHITE); c.drawCentredString(PW/2, 74, "TVX GROUP")
tracked(c, PW/2, 44, "© 2026 SUNHOURI PROPERTY HOLDINGS · TVX GROUP REAL ESTATE", SANS, 6.5, Color(1,1,1,0.45),1.8,'center')
c.showPage()

c.setTitle("No410 — Where You Truly Belong")
c.setAuthor("TVX Group | Real Estate")
c.setSubject("A Detached Hilltop Residence · Miri, Sarawak")
c.save()
print("wrote", (DIST/"No410_Brochure.pdf").relative_to(ROOT),
      f"({(DIST/'No410_Brochure.pdf').stat().st_size//1024} KB)")
