from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, random, math, shutil

random.seed(42)

# ====== 加载资源 ======
with open("/root/ds-majiang/client/cordova/www/res/atlas/ui/majiang.json") as f:
    atlas = json.load(f)
sprite = Image.open("/root/ds-majiang/client/cordova/www/res/atlas/ui/majiang.png").convert("RGBA")

# 艺术字体: Noto Serif CJK Bold（比WQY更艺术）
FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
# 备用
FONT_FALLBACK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

def get_tile(idx):
    """从图集提取第idx张牌（104x92）"""
    name = f"ce_{idx}.png"
    if name not in atlas["frames"]:
        name = f"ce_{idx}.png"
    info = atlas["frames"][name]
    f = info["frame"]
    tile = sprite.crop((f["x"], f["y"], f["x"]+f["w"], f["y"]+f["h"]))
    full = Image.new("RGBA", (info["sourceSize"]["w"], info["sourceSize"]["h"]), (0,0,0,0))
    sx, sy = info["spriteSourceSize"]["x"], info["spriteSourceSize"]["y"]
    full.paste(tile, (sx, sy), tile)
    return full

def add_text_artistic(draw, x, y, text, font_path, size, color=(255,215,0)):
    """添加艺术字体（金属渐变 + 发光效果）"""
    font = ImageFont.truetype(font_path, size)
    bbox = draw.textbbox((0,0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    
    # 大发光阴影（多层）
    for t in range(12, 3, -2):
        for dx, dy in [(0,-t), (0,t), (-t,0), (t,0), (-t,-t), (-t,t), (t,-t), (t,t)]:
            draw.text((x + dx, y + dy), text, font=font, fill=(200,100,0,int(40-t*2)))
    
    # 白色中层发光
    for t in range(4, 0, -1):
        for dx, dy in [(0,-t), (0,t), (-t,0), (t,0)]:
            draw.text((x+dx, y+dy), text, font=font, fill=(255,255,200,int(80/t)))
    
    # 黑色描边
    for ox in range(-3, 4):
        for oy in range(-3, 4):
            if ox==0 and oy==0: continue
            draw.text((x+ox, y+oy), text, font=font, fill=(0,0,0,200))
    
    # 主文字 - 金色渐变效果（两层叠加）
    draw.text((x-1, y-1), text, font=font, fill=(255,230,150))  # 亮金高光
    draw.text((x, y), text, font=font, fill=color)               # 主金色
    draw.text((x, y+1), text, font=font, fill=(200,160,50))      # 暗金底部


# ==================== 1. 加载页 ====================
print("=== 加载页 ===")
img1 = Image.open("/tmp/loading_bg2.png").convert("RGBA")
overlay1 = Image.new("RGBA", img1.size, (0,0,0,0))
draw1 = ImageDraw.Draw(overlay1)

# 标题 - 使用NotoSerifCJK Bold艺术字体
title = "砀山235麻将"
add_text_artistic(draw1, img1.width//2 - 280, img1.height//2 - 100, title, FONT, 120)

# 小字装饰
font_sub = ImageFont.truetype(FONT, 30)
sub = "DangShan 235 Mahjong"
bbox = draw1.textbbox((0,0), sub, font=font_sub)
sw = bbox[2]-bbox[0]
draw1.text((img1.width//2 - sw//2, img1.height//2 + 10), sub, font=font_sub, fill=(255,215,0,150))

# 5-6张真实麻将牌散落
tile_indices = [3, 10, 17, 20, 28, 33]  # 随机选不同花色
positions = []
for i, tidx in enumerate(tile_indices):
    tile_img = get_tile(tidx)
    
    # 随机位置 - 避开标题区域
    for attempt in range(20):
        rx = random.randint(10, img1.width - 114)
        ry = random.randint(10, img1.height - 102)
        # 避开标题中央区域
        cx, cy = img1.width//2, img1.height//2
        if abs(rx - cx + 52) < 350 and abs(ry - cy + 46) < 160:
            continue
        # 避免重叠
        ok = True
        for px, py in positions:
            if abs(rx-px) < 120 and abs(ry-py) < 110:
                ok = False; break
        if ok:
            positions.append((rx, ry))
            break
    
    if len(positions) < len(tile_indices):
        # 强制放置
        rx = random.randint(50, img1.width - 150)
        ry = random.randint(200, img1.height - 200)
        # 确保不在标题区
        if abs(rx - img1.width//2) < 300 and abs(ry - img1.height//2) < 150:
            ry = random.choice([30, img1.height - 150])
        positions.append((rx, ry))
    
    # 旋转
    angle = random.uniform(-25, 25)
    tile_img = tile_img.rotate(angle, expand=True, resample=Image.BICUBIC)
    
    # 轻微投影
    shadow = Image.new("RGBA", tile_img.size, (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle([5, 5, tile_img.width, tile_img.height], fill=(0,0,0,80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    
    rx, ry = positions[-1]
    overlay1.paste(shadow, (rx, ry), shadow)
    overlay1.paste(tile_img, (rx, ry), tile_img)

result1 = Image.alpha_composite(img1, overlay1).convert("RGB")
result1.save("/www/wwwroot/mj-game/loading_bg_new.png", quality=95)
print("  加载页完成 ✅")


# ==================== 2. 桌布 ====================
print("=== 桌布 ===")
img2 = Image.open("/tmp/room_bg2.png").convert("RGBA")
overlay2 = Image.new("RGBA", img2.size, (0,0,0,0))
draw2 = ImageDraw.Draw(overlay2)

# 标题 - 放大、居中偏上、半透明
title2 = "砀山235麻将"
font_room = ImageFont.truetype(FONT, 140)
bbox2 = draw2.textbbox((0,0), title2, font=font_room)
tw2, th2 = bbox2[2]-bbox2[0], bbox2[3]-bbox2[1]
cx2, cy2 = img2.width//2, img2.height//3 - 10

# 半透明阴影
for t in range(8, 2, -2):
    for dx, dy in [(0,-t), (0,t), (-t,0), (t,0)]:
        draw2.text((cx2 - tw2//2 + dx, cy2 + dy), title2, font=font_room, fill=(0,60,0,60-t*3))

# 半透明金色文字 (alpha=100)
draw2.text((cx2 - tw2//2, cy2), title2, font=font_room, fill=(255,215,0,100))

# 半透明装饰元素 - 金色云纹/圆圈
import math
for _ in range(25):
    dx = random.randint(20, img2.width - 20)
    dy = random.randint(20, img2.height - 20)
    if abs(dx - cx2) < 400 and abs(dy - cy2) < 140:
        continue
    alpha = random.randint(25, 70)
    radius = random.randint(8, 30)
    # 金色半透明圆环
    draw2.ellipse([dx-radius, dy-radius, dx+radius, dy+radius], 
                  outline=(255,215,0,alpha), width=2)

# 金色半透明四角装饰
for cx, cy, label in [(40,40,"★"), (1300,40,"★"), (40,720,"★"), (1300,720,"★")]:
    font_d = ImageFont.truetype(FONT, 40)
    draw2.text((cx, cy), label, font=font_d, fill=(255,215,0,80))

result2 = Image.alpha_composite(img2, overlay2).convert("RGB")
result2.save("/www/wwwroot/mj-game/room_bg_new.png", quality=95)
print("  桌布完成 ✅")

# 复制到下载目录
shutil.copy("/www/wwwroot/mj-game/loading_bg_new.png", "/www/wwwroot/mahjong-download/loading_bg_new.png")
shutil.copy("/www/wwwroot/mj-game/room_bg_new.png", "/www/wwwroot/mahjong-download/room_bg_new.png")
print("\n全部完成 ✅")