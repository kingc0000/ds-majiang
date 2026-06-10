from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math, shutil

random.seed(42)
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def add_shadow(draw, x, y, text, font, color=(0,0,0,180)):
    for ox, oy in [(3,3),(3,4),(4,3),(4,4),(5,5),(6,6)]:
        draw.text((x+ox, y+oy), text, font=font, fill=color)

def add_outline(draw, x, y, text, font, color, width=3):
    for ox in range(-width, width+1):
        for oy in range(-width, width+1):
            if ox==0 and oy==0: continue
            draw.text((x+ox, y+oy), text, font=font, fill=color)

def draw_tile(draw, x, y, w=40, h=55, color=(245,240,230)):
    """画一张麻将牌"""
    # 牌身
    draw.rounded_rectangle([x, y, x+w, y+h], radius=4, fill=color,
                           outline=(180,170,150), width=1)
    # 装饰线
    draw.rounded_rectangle([x+3, y+3, x+w-3, y+h-3], radius=3,
                           fill=None, outline=(200,190,170), width=1)

def draw_tile_with_symbol(draw, x, y, text, text_color=(0,120,0)):
    """画一张带文字的麻将牌"""
    w, h = 42, 58
    draw_tile(draw, x, y, w, h)
    # 文字
    font_s = ImageFont.truetype(WQY, 24)
    bbox = draw.textbbox((0,0), text, font=font_s)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    tx = x + (w - tw)//2
    ty = y + (h - th)//2 - 4
    draw.text((tx, ty), text, font=font_s, fill=text_color)

# ===================== 1. 加载页 =====================
print("处理加载页...")
img1 = Image.open("/tmp/loading_bg2.png").convert("RGBA")
overlay1 = Image.new("RGBA", img1.size, (0,0,0,0))
draw1 = ImageDraw.Draw(overlay1)

# 标题 - 卡通风格（多重彩色轮廓）
title = "砀山235麻将"
font_big = ImageFont.truetype(WQY, 110)
bbox = draw1.textbbox((0,0), title, font=font_big)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
cx, cy = img1.width//2, img1.height//2 - 60

# 多种彩色轮廓实现卡通效果
colors = [(255,100,100), (255,200,0), (100,255,100), (100,150,255), (255,150,255)]
for t in range(8, 0, -1):
    dx, dy = 0, 0
    draw1.text((cx - tw//2 + dx, cy + dy - t), title, font=font_big, fill=(255,100,80))
    draw1.text((cx - tw//2 + dx, cy + dy + t), title, font=font_big, fill=(255,100,80))
    draw1.text((cx - tw//2 + dx - t, cy + dy), title, font=font_big, fill=(255,100,80))
    draw1.text((cx - tw//2 + dx + t, cy + dy), title, font=font_big, fill=(255,100,80))

# 白色描边
for t in range(3, 0, -1):
    for dx, dy in [(0,-t), (0,t), (-t,0), (t,0), (-t,-t), (-t,t), (t,-t), (t,t)]:
        draw1.text((cx - tw//2 + dx, cy + dy), title, font=font_big, fill=(255,255,255,200))
draw1.text((cx - tw//2, cy), title, font=font_big, fill=(255,215,0))

# 散落的麻将牌 - 随机位置
tile_data = [
    ("一", (0,120,0)), ("二", (0,120,0)), ("三", (0,120,0)),
    ("四", (0,120,0)), ("五", (0,120,0)), ("六", (0,120,0)),
    ("壹", (200,0,0)), ("贰", (200,0,0)), ("叁", (200,0,0)),
    ("發", (0,120,0)), ("中", (200,0,0)), ("東", (0,80,160)),
]
positions = []
for _ in range(10):
    rx = random.randint(30, img1.width - 70)
    ry = random.randint(30, img1.height - 80)
    # 避免盖住标题
    if abs(rx - cx) < 250 and abs(ry - cy) < 100:
        continue
    # 避免重叠
    ok = True
    for px, py in positions:
        if abs(rx-px) < 60 and abs(ry-py) < 70:
            ok = False; break
    if not ok: continue
    positions.append((rx, ry))
    symbol, color = random.choice(tile_data)
    angle = random.uniform(-0.3, 0.3)
    # 旋转处理 - 使用临时图
    tile_img = Image.new("RGBA", (60, 76), (0,0,0,0))
    td = ImageDraw.Draw(tile_img)
    draw_tile_with_symbol(td, 9, 9, symbol, color)
    tile_img = tile_img.rotate(angle * 180 / math.pi, expand=True, resample=Image.BICUBIC)
    overlay1.paste(tile_img, (rx, ry), tile_img)

# 合成
result1 = Image.alpha_composite(img1, overlay1).convert("RGB")
result1.save("/www/wwwroot/mj-game/loading_bg_new.png", quality=95)
print("  加载页 OK")

# ===================== 2. 桌布 =====================
print("处理桌布...")
img2 = Image.open("/tmp/room_bg2.png").convert("RGBA")
overlay2 = Image.new("RGBA", img2.size, (0,0,0,0))
draw2 = ImageDraw.Draw(overlay2)

# 标题 - 放大、居中偏上、半透明
title2 = "砀山235麻将"
font_room = ImageFont.truetype(WQY, 130)
bbox2 = draw2.textbbox((0,0), title2, font=font_room)
tw2, th2 = bbox2[2]-bbox2[0], bbox2[3]-bbox2[1]
# 居中偏上: 1/3 高度位置
cx2, cy2 = img2.width//2, img2.height//3 - 20

# 半透明阴影
add_shadow(draw2, cx2 - tw2//2, cy2, title2, font_room, (0,60,0,100))

# 半透明金色文字 (alpha=120)
draw2.text((cx2 - tw2//2, cy2), title2, font=font_room, fill=(255,215,0,120))

# 半透明装饰 - 金色小圆圈和云纹
deco_font = ImageFont.truetype(WQY, 35)
deco_items = ["●", "○", "◇", "◆", "★", "☆", "✦", "✧"]
for i in range(15):
    dx = random.randint(20, img2.width - 20)
    dy = random.randint(20, img2.height - 20)
    # 避开标题
    if abs(dx - cx2) < 350 and abs(dy - cy2) < 120:
        continue
    deco = random.choice(deco_items)
    alpha = random.randint(30, 80)
    size = random.randint(25, 45)
    f = ImageFont.truetype(WQY, size)
    draw2.text((dx, dy), deco, font=f, fill=(255,215,0,alpha))

# 合成
result2 = Image.alpha_composite(img2, overlay2).convert("RGB")
result2.save("/www/wwwroot/mj-game/room_bg_new.png", quality=95)
print("  桌布 OK")

# 复制到下载目录
shutil.copy("/www/wwwroot/mj-game/loading_bg_new.png", "/www/wwwroot/mahjong-download/loading_bg_new.png")
shutil.copy("/www/wwwroot/mj-game/room_bg_new.png", "/www/wwwroot/mahjong-download/room_bg_new.png")
print("全部完成 ✅")