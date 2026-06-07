#!/usr/bin/env python3
"""Generate a beautiful mahjong app icon for 砀山麻游"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
OUTPUT_DIR = "/root/ds-majiang/client/cordova"

def create_mahjong_tile(size=192):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # === 1. Background: Dark green felt ===
    for y in range(size):
        t = y / size
        r = int(16 + t * 10)
        g = int(55 + t * 30 + 20 * (1 - abs(y/size - 0.5) * 2))
        b = int(16 + t * 10)
        draw.line([(0, y), (size-1, y)], fill=(r, g, b))
    
    # Texture dots
    random.seed(42)
    for _ in range(size * 3):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        p = img.getpixel((x, y))
        v = random.randint(-6, 6)
        np = (max(0, min(255, p[0] + v)),
              max(0, min(255, p[1] + v)),
              max(0, min(255, p[2] + v)))
        img.putpixel((x, y), np)
    
    # === 2. Gold ornamental border ===
    m = int(size * 0.07)
    bw = max(2, int(size * 0.015))
    for i in range(bw):
        aa = 200 + 55 * (bw - 1 - i) // bw
        draw.rounded_rectangle(
            [m-i, m-i, size-m+i-1, size-m+i-1],
            radius=int(size * 0.06),
            outline=(210, 175, 60, aa)
        )
    
    # === 3. White/ivory mahjong tile ===
    tm = int(size * 0.16)
    ts = size - tm * 2
    tr = int(size * 0.07)
    
    # Shadow
    so = int(size * 0.04)
    draw.rounded_rectangle(
        [tm+so, tm+so, tm+ts+so, tm+ts+so],
        radius=tr, fill=(0, 0, 0, 50)
    )
    
    # Tile gradient
    for y in range(tm, tm+ts):
        t = (y - tm) / ts
        r = int(248 - t * 12)
        g = int(240 - t * 12)
        b = int(225 - t * 12)
        draw.rectangle([tm, y, tm+ts-1, y], fill=(r, g, b))
    
    # Tile border
    draw.rounded_rectangle(
        [tm, tm, tm+ts-1, tm+ts-1], radius=tr,
        outline=(195, 180, 160), width=max(1, int(size*0.008))
    )
    
    # === 4. Inner red decorative border ===
    im = int(size * 0.085)
    draw.rounded_rectangle(
        [tm+im, tm+im, tm+ts-im-1, tm+ts-im-1],
        radius=int(size*0.04),
        outline=(180, 50, 50), width=max(1, int(size*0.005))
    )
    
    # === 5. Character 發 in red with gold outline ===
    fs = int(size * 0.48)
    font = ImageFont.truetype(FONT_PATH, fs, index=0)
    
    bbox = draw.textbbox((0, 0), "發", font=font)
    cw = bbox[2] - bbox[0]
    ch = bbox[3] - bbox[1]
    cx = (size - cw) // 2 - bbox[0]
    cy = (size - ch) // 2 - bbox[1] - int(size * 0.02)
    
    # Gold outline
    ow = max(2, int(size * 0.012))
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx == 0 and dy == 0:
                continue
            if dx*dx + dy*dy <= ow*ow:
                draw.text((cx+dx, cy+dy), "發", fill=(210, 175, 50), font=font)
    
    # Red character
    draw.text((cx, cy), "發", fill=(190, 25, 25), font=font)
    
    # === 6. Subtle shine ===
    for y in range(int(size * 0.35)):
        for x in range(int(size * 0.35)):
            dist = (x*x + y*y) ** 0.5
            if dist < size * 0.18:
                alpha = int(30 * (1 - dist / (size * 0.18)))
                if alpha > 0:
                    p = img.getpixel((x, y))
                    img.putpixel((x, y), (
                        min(255, p[0] + alpha),
                        min(255, p[1] + alpha),
                        min(255, p[2] + alpha)
                    ))
    
    return img

def save_all_sizes(img_192):
    sizes = [
        ('mipmap-xxxhdpi', 192),
        ('mipmap-xxhdpi', 144),
        ('mipmap-xhdpi', 96),
        ('mipmap-hdpi', 72),
        ('mipmap-mdpi', 48),
        ('mipmap-ldpi', 36),
    ]
    
    base = os.path.join(OUTPUT_DIR, 'res')
    
    # Source icon for config.xml
    res_icon = os.path.join(OUTPUT_DIR, 'resources/android/drawable-xxxhdpi-icon.png')
    os.makedirs(os.path.dirname(res_icon), exist_ok=True)
    img_192.save(res_icon, 'PNG')
    print(f"  ✓ {res_icon}")
    
    # Density-named icons
    density_dir = os.path.join(OUTPUT_DIR, 'resources/android/icon')
    os.makedirs(density_dir, exist_ok=True)
    density_map = {'ldpi': 36, 'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    
    for name, sz in sizes:
        # res/mipmap-*/
        out_dir = os.path.join(base, name)
        os.makedirs(out_dir, exist_ok=True)
        icon_img = img_192 if sz == 192 else img_192.resize((sz, sz), Image.LANCZOS)
        icon_img.save(os.path.join(out_dir, 'icon.png'), 'PNG')
        print(f"  ✓ res/{name}/icon.png ({sz}x{sz})")
    
    # Density icons
    for density, sz in density_map.items():
        icon_img = img_192 if sz == 192 else img_192.resize((sz, sz), Image.LANCZOS)
        out = os.path.join(density_dir, f'drawable-{density}-icon.png')
        icon_img.save(out, 'PNG')
        print(f"  ✓ resources/android/icon/drawable-{density}-icon.png ({sz}x{sz})")

if __name__ == '__main__':
    print("🎨 Generating mahjong app icon...")
    save_all_sizes(create_mahjong_tile(192))
    print("\n✅ Done! All icon sizes generated.")
