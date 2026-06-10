from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, random, math, shutil

random.seed(42)

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# ====== 加载游戏麻将图集 ======
with open("/root/ds-majiang/client/cordova/www/res/atlas/ui/majiang.json") as f:
    atlas = json.load(f)
sprite = Image.open("/root/ds-majiang/client/cordova/www/res/atlas/ui/majiang.png").convert("RGBA")

def get_tile(idx):
    name = f"ce_{idx}.png"
    info = atlas["frames"][name]
    f = info["frame"]
    tile = sprite.crop((f["x"], f["y"], f["x"]+f["w"], f["y"]+f["h"]))
    full = Image.new("RGBA", (info["sourceSize"]["w"], info["sourceSize"]["h"]), (0,0,0,0))
    full.paste(tile, (info["spriteSourceSize"]["x"], info["spriteSourceSize"]["y"]), tile)
    # 缩放到70%大小
    full = full.resize((int(full.width*0.7), int(full.height*0.7)), Image.LANCZOS)
    return full

def gold_text(draw, x, y, text, font, color=(255,215,0)):
    """金色文字，白色内发光 + 黑边"""
    # 外层发光
    for r in range(10, 2, -2):
        for dx, dy in [(0,-r),(0,r),(-r,0),(r,0)]:
            draw.text((x+dx, y+dy), text, font=font, fill=(200,100,0,max(1,40-r*3)))
    # 黑边
    for ox in range(-3, 4):
        for oy in range(-3, 4):
            if ox==0 and oy==0: continue
            draw.text((x+ox, y+oy), text, font=font, fill=(0,0,0))
    # 白色高光内层
    for t in range(3, 0, -1):
        draw.text((x, y-t), text, font=font, fill=(255,255,220,80//t if t>0 else 255))
    # 主色
    draw.text((x, y), text, font=font, fill=color)
    draw.text((x, y+1), text, font=font, fill=(200,160,50))


# ===================== 1. 加载页 =====================
print("=== 加载页 ===")
img1 = Image.open("/tmp/loading_clean.png").convert("RGBA")
W, H = img1.width, img1.height

# 标题
title_font = ImageFont.truetype(FONT, 110)
bbox = ImageDraw.Draw(Image.new("RGBA",(1,1))).textbbox((0,0),"砀山235麻将",font=title_font)
tw = bbox[2]-bbox[0]
tx, ty = (W - tw)//2, H//2 - 90

overlay1 = Image.new("RGBA", (W, H), (0,0,0,0))
d1 = ImageDraw.Draw(overlay1)

gold_text(d1, tx, ty, "砀山235麻将", title_font)

# 英文小字 - 不透明，不会被挡住
sub_font = ImageFont.truetype(FONT, 32)
bbox2 = d1.textbbox((0,0), "DangShan 235 Mahjong", font=sub_font)
sw = bbox2[2]-bbox2[0]
d1.text(((W-sw)//2, ty + 125), "DangShan 235 Mahjong", font=sub_font, fill=(255,215,0,200))

# 5张真实麻将牌散落 - 避开标题区
tile_ids = [5, 15, 22, 28, 33]  # 不同花色
positions = []
for tid in tile_ids:
    tile = get_tile(tid)
    for attempt in range(30):
        rx = random.randint(20, W - tile.width - 20)
        ry = random.randint(20, H - tile.height - 20)
        # 避开标题和英文区域
        if abs(rx + tile.width//2 - W//2) < 320 and abs(ry + tile.height//2 - H//2) < 160:
            continue
        ok = True
        for px, py in positions:
            if abs(rx-px) < 100 and abs(ry-py) < 90:
                ok = False; break
        if ok:
            positions.append((rx, ry)); break
    
    angle = random.uniform(-20, 20)
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    
    # 投影
    sh = Image.new("RGBA", tile.size, (0,0,0,0))
    ImageDraw.Draw(sh).rectangle([4,4,tile.width,tile.height], fill=(0,0,0,100))
    sh = sh.filter(ImageFilter.GaussianBlur(3))
    overlay1.paste(sh, (rx+3, ry+5), sh)
    overlay1.paste(tile, (rx, ry), tile)

result1 = Image.alpha_composite(img1, overlay1).convert("RGB")
result1.save("/tmp/loading_final.png", quality=95)
print("  加载页 OK ✅")


# ===================== 2. 桌布 =====================
print("=== 桌布 ===")
img2 = Image.open("/tmp/room_clean.png").convert("RGBA")
W2, H2 = img2.width, img2.height

overlay2 = Image.new("RGBA", (W2, H2), (0,0,0,0))
d2 = ImageDraw.Draw(overlay2)

# 放大半透明标题 - 居中偏上
title2 = "砀山235麻将"
font_room = ImageFont.truetype(FONT, 150)
bbox_r = d2.textbbox((0,0), title2, font=font_room)
tw2 = bbox_r[2]-bbox_r[0]
tx2, ty2 = (W2-tw2)//2, H2//3 - 20

# 阴影
for t in range(6, 0, -2):
    d2.text((tx2, ty2+t), title2, font=font_room, fill=(0,60,0,60-t*8))
# 半透明主文字 (alpha=130)
d2.text((tx2, ty2), title2, font=font_room, fill=(255,215,0,130))

# 半透明装饰 - 清晰可见的金色小元素
for _ in range(20):
    dx = random.randint(20, W2-20)
    dy = random.randint(20, H2-20)
    if abs(dx-W2//2) < 400 and abs(dy-ty2) < 130:
        continue
    r = random.randint(6, 20)
    alpha = random.randint(40, 80)
    d2.ellipse([dx-r, dy-r, dx+r, dy+r], outline=(255,215,0,alpha), width=2)

# 四角装饰
for cx, cy in [(30,30), (W2-30,30), (30,H2-30), (W2-30,H2-30)]:
    fd = ImageFont.truetype(FONT, 35)
    d2.text((cx, cy), "✦", font=fd, fill=(255,215,0,80))

result2 = Image.alpha_composite(img2, overlay2).convert("RGB")
result2.save("/tmp/room_final.png", quality=95)
print("  桌布 OK ✅")

# 复制到服务器
shutil.copy("/tmp/loading_final.png", "/www/wwwroot/mj-game/loading_bg_new.png")
shutil.copy("/tmp/room_final.png", "/www/wwwroot/mj-game/room_bg_new.png")
shutil.copy("/tmp/loading_final.png", "/www/wwwroot/mahjong-download/loading_bg_new.png")
shutil.copy("/tmp/room_final.png", "/www/wwwroot/mahjong-download/room_bg_new.png")
print("\n全部完成 ✅")