from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def add_text_to_image(image_path, output_path, text, position="center", 
                       font_size=80, font_color=(255, 215, 0),
                       outline_color=(0, 0, 0), outline_width=4,
                       shadow=True):
    """在图片上添加中文字体"""
    img = Image.open(image_path).convert("RGBA")
    
    font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    font = ImageFont.truetype(font_path, font_size)
    
    # 覆盖层
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 文字尺寸
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # 位置
    if position == "center":
        x = (img.width - tw) // 2
        y = (img.height - th) // 2 - 40
    elif position == "top":
        x = (img.width - tw) // 2
        y = 40
    elif position == "bottom":
        x = (img.width - tw) // 2
        y = img.height - th - 60
    
    # 阴影
    if shadow:
        shadow_color = (0, 0, 0, 180)
        for ox in range(3, 6):
            for oy in range(3, 6):
                draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    
    # 轮廓
    if outline_width > 0:
        for ox in range(-outline_width, outline_width+1):
            for oy in range(-outline_width, outline_width+1):
                if ox == 0 and oy == 0:
                    continue
                draw.text((x + ox, y + oy), text, font=font, fill=outline_color)
    
    # 主文字
    draw.text((x, y), text, font=font, fill=font_color)
    
    # 合成
    result = Image.alpha_composite(img, overlay)
    result = result.convert("RGB")
    result.save(output_path, quality=95)
    print(f"Saved: {output_path} ({result.size})")

# ========== 1. 加载页 ==========
add_text_to_image(
    "/tmp/loading_bg_raw.png",
    "/www/wwwroot/mj-game/loading_bg_new.png",
    "砀山235麻将",
    position="center",
    font_size=100,
    font_color=(255, 215, 0),      # 金色
    outline_color=(80, 40, 0),      # 深金色描边
    outline_width=5,
    shadow=True
)

# ========== 2. 房间桌布 ==========
add_text_to_image(
    "/tmp/room_bg_raw.png",
    "/www/wwwroot/mj-game/room_bg_new.png",
    "砀山235麻将",
    position="top",
    font_size=70,
    font_color=(255, 215, 0),      # 金色
    outline_color=(0, 60, 0),       # 深绿描边
    outline_width=4,
    shadow=True
)

# 复制到下载目录
import shutil
shutil.copy("/www/wwwroot/mj-game/loading_bg_new.png", "/www/wwwroot/mahjong-download/loading_bg_new.png")
shutil.copy("/www/wwwroot/mj-game/room_bg_new.png", "/www/wwwroot/mahjong-download/room_bg_new.png")
print("Copied to download dir")

# 验证
for f in ["/www/wwwroot/mj-game/loading_bg_new.png", "/www/wwwroot/mj-game/room_bg_new.png"]:
    im = Image.open(f)
    print(f"{os.path.basename(f)}: {im.size}, {im.mode}")
