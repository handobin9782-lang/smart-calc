"""Generate og.png (1200x630) for the universal public version of the calculator."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 16, 32)
FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"

def f(size):
    return ImageFont.truetype(FONT, size)

img = Image.new("RGB", (W, H), BG)

# soft radial glow (top-left) like the CSS gradient
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
cx, cy = 380, 60
for i in range(240, 0, -8):
    val = int(26 * (1 - i / 240) ** 1.6)
    gd.ellipse([cx - i * 2.2, cy - i * 1.5, cx + i * 2.2, cy + i * 1.5], fill=val)
layer = Image.new("RGB", (W, H), (23, 42, 74))
img = Image.composite(layer, img, glow)

d = ImageDraw.Draw(img)

# pill "무료 계산기"
pill_font = f(26)
pw = d.textlength("무료 계산기", font=pill_font)
pad_x, pad_y = 26, 14
x0, y0 = 74, 48
d.rounded_rectangle([x0, y0, x0 + pw + pad_x * 2, y0 + 26 + pad_y * 2 - 6],
                    radius=26, outline=(56, 211, 153), width=2)
d.text((x0 + pad_x, y0 + pad_y - 3), "무료 계산기", font=pill_font, fill=(56, 211, 153))

# title
title_font = f(80)
d.text((74, 122), "생활·금융 계산기", font=title_font,
       fill=(243, 246, 255), stroke_width=2, stroke_fill=(243, 246, 255))

# subtitle
sub_font = f(38)
d.text((78, 240), "월 50만 원 × 15년이면 얼마가 될까?", font=sub_font, fill=(147, 161, 198))

# third line (blue)
line3_font = f(29)
d.text((78, 300), "복리 · 대출 · 연봉 · 연차 · 실업급여 5가지 계산기", font=line3_font,
       fill=(96, 165, 250))

# growth bars
base_y = 516
bar_w, gap = 40, 66
heights = [20, 30, 44, 60, 82, 106, 136, 168]
start_x = 74
for i, h in enumerate(heights):
    x = start_x + i * (bar_w + gap)
    top = base_y - h
    split = top + int(h * 0.42)
    d.rounded_rectangle([x, top, x + bar_w, base_y], radius=6, fill=(96, 165, 250))
    d.rounded_rectangle([x, split, x + bar_w, base_y], radius=6, fill=(56, 211, 153))
    d.rectangle([x, split, x + bar_w, split + 6], fill=(56, 211, 153))

# axis line
d.line([(74, base_y), (1126, base_y)], fill=(45, 58, 92), width=1)

# footer
foot_font = f(25)
d.text((78, 552), "설치 없이 모바일에서 바로 · 회원가입 없음", font=foot_font, fill=(147, 161, 198))

img.save("og.png", optimize=True)
print("saved", img.size)
