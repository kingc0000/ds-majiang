#!/usr/bin/env python3
"""Generate a beautiful mahjong app icon for 砀山235"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

OUTPUT_DIR = "/root/ds-majiang/client/cordova"

# Try calligraphy font first, fall back to WQY
FONT_PATHS = [
    "/usr/share/fonts/truetype/custom/MaShanZheng.ttf",
    "/usr/share/fonts/truetype/custom/ZCOOL-QingKe-HuangYou.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]

def get_font(size):
    for path in FONT_PATHS:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size, index=0)
                # Test if it can render 發
                test = Image.new('RGBA', (1,1))
                ImageDraw.Draw(test).text((0,0), "發", font=font)
                print(f"  Using font: {os.path.basename(path)} ({size}px)")
                return font
            except:
                continue
    return ImageFont.load_default()

def create_mahjong_tile(size=192):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # === 1. Background: Dark green felt ===
    for y in range(size):
        t = y / size
        r = int(14 + t * 12)
        g = int(50 + t * 35 + 25 * (1 - abs(y/size - 0.5) * 2))
        b = int(14 + t * 12)
        draw.line([(0, y), (size-1, y)], fill=(r, g, b))
    
    # Texture dots
    random.seed(42)
    for _ in range(size * 4):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        p = img.getpixel((x, y))
        v = random.randint(-5, 5)
        np = (max(0, min(255, p[0] + v)),
              max(0, min(255, p[1] + v)),
              max(0, min(255, p[2] + v)))
        img.putpixel((x, y), np)
    
    # === 2. Outer gold ornamental border ===
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
        radius=tr, fill=(0, 0, 0, 55)
    )
    
    # Tile gradient (ivory/cream)
    for y in range(tm, tm+ts):
        t = (y - tm) / ts
        r = int(250 - t * 10)
        g = int(243 - t * 10)
        b = int(228 - t * 10)
        draw.rectangle([tm, y, tm+ts-1, y], fill=(r, g, b))
    
    # Tile border
    draw.rounded_rectangle(
        [tm, tm, tm+ts-1, tm+ts-1], radius=tr,
        outline=(195, 180, 160), width=max(1, int(size*0.008))
    )
    
    # === 4. Inner decorative frame ===
    im = int(size * 0.085)
    draw.rounded_rectangle(
        [tm+im, tm+im, tm+ts-im-1, tm+ts-im-1],
        radius=int(size*0.04),
        outline=(180, 50, 50), width=max(1, int(size*0.005))
    )
    
    # === 5. Character 發 with gold gradient and calligraphy font ===
    fs = int(size * 0.52)
    font = get_font(fs)
    
    bbox = draw.textbbox((0, 0), "發", font=font)
    cw = bbox[2] - bbox[0]
    ch = bbox[3] - bbox[1]
    cx = int((size - cw) // 2 - bbox[0])
    cy = int((size - ch) // 2 - bbox[1]) - int(size * 0.02)
    
    # Create character mask for gradient
    char_mask = Image.new('L', (size, size), 0)
    char_draw = ImageDraw.Draw(char_mask)
    char_draw.text((cx, cy), "發", fill=255, font=font)
    
    # Gold outer outline (thicker for calligraphy font)
    ow = max(3, int(size * 0.018))
    outline_color = (200, 160, 40)  # gold
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx == 0 and dy == 0:
                continue
            if dx*dx + dy*dy <= ow*ow:
                draw.text((cx+dx, cy+dy), "發", fill=outline_color, font=font)
    
    # Inner gold outline (slightly different shade)
    ow2 = max(1, int(size * 0.008))
    for dx in range(-ow2, ow2+1):
        for dy in range(-ow2, ow2+1):
            if dx == 0 and dy == 0:
                continue
            draw.text((cx+dx, cy+dy), "發", fill=(230, 195, 60), font=font)
    
    # Main character with gradient red fill
    # Apply char_mask to create gradient effect
    char_size = int(size * 0.52)
    for y in range(size):
        for x in range(size):
            if char_mask.getpixel((x, y)) > 128:
                # Gradient from dark red (top) to bright red (bottom)
                gy = y / size
                r = int(160 + gy * 50)
                g = int(15 + gy * 20)
                b = int(15 + gy * 10)
                img.putpixel((x, y), (r, g, b, 255))
    
    # === 6. Subtle highlight/shine at top-left ===
    for y in range(int(size * 0.35)):
        for x in range(int(size * 0.35)):
            dist = (x*x + y*y) ** 0.5
            if dist < size * 0.18:
                alpha = int(35 * (1 - dist / (size * 0.18)))
                if alpha > 0:
                    p = img.getpixel((x, y))
                    img.putpixel((x, y), (
                        min(255, p[0] + alpha),
                        min(255, p[1] + alpha),
                        min(255, p[2] + alpha)
                    ))
    
    # Bottom-right subtle glow
    for y in range(int(size * 0.65), size):
        for x in range(int(size * 0.65), size):
            dx = x - size * 0.65
            dy = y - size * 0.65
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < size * 0.12:
                alpha = int(20 * (1 - dist / (size * 0.12)))
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
    print(f"  ✓ {os.path.basename(res_icon)}")
    
    # Density-named icons
    density_dir = os.path.join(OUTPUT_DIR, 'resources/android/icon')
    os.makedirs(density_dir, exist_ok=True)
    density_map = {'ldpi': 36, 'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    
    for name, sz in sizes:
        out_dir = os.path.join(base, name)
        os.makedirs(out_dir, exist_ok=True)
        icon_img = img_192 if sz == 192 else img_192.resize((sz, sz), Image.LANCZOS)
        icon_img.save(os.path.join(out_dir, 'icon.png'), 'PNG')
        print(f"  ✓ res/{name}/icon.png ({sz}x{sz})")
    
    for density, sz in density_map.items():
        icon_img = img_192 if sz == 192 else img_192.resize((sz, sz), Image.LANCZOS)
        out = os.path.join(density_dir, f'drawable-{density}-icon.png')
        icon_img.save(out, 'PNG')
        print(f"  ✓ resources/android/icon/drawable-{density}-icon.png ({sz}x{sz})")

if __name__ == '__main__':
    print("🎨 Generating mahjong app icon (calligraphy style)...")
    save_all_sizes(create_mahjong_tile(192))
    print("\n✅ Done!")