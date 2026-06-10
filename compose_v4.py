#!/usr/bin/env python3
"""
Compose v4 - 砀山235麻将 加载页 & 桌布最终版
- 加载页：去掉游戏素彩票贴，手工绘制6张真实麻将牌散落
- 桌布：UKai楷体艺术字logo居中，金碧辉煌半透明效果
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, random, json

W, H = 1344, 768

# ---------- fonts ----------
FONT_WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_UKAI = "/usr/share/fonts/truetype/arphic/ukai.ttc"
FONT_UMING = "/usr/share/fonts/truetype/arphic/uming.ttc"

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_mahjong_tile(char, color, size=(80, 112), bg_color="#F5F0E0", rotated=0):
    """
    手绘精美麻将牌
    char: 主字符 (如 '一萬', '發', '中')
    color: 字符颜色
    size: 牌尺寸 (w, h)
    bg_color: 牌底色
    rotated: 旋转角度
    """
    tw, th = size
    # 创建带透明通道的牌 - 直接全部画在一个图层上，避免 alpha_composite 导致 dt 引用旧对象
    tile = Image.new('RGBA', (tw * 2, th * 2), (0, 0, 0, 0))
    
    cx, cy = tw, th
    r = 8  # 圆角半径
    
    # --- 阴影 (半透明画在 tile 主图层上) ---
    dt = ImageDraw.Draw(tile)
    draw_rounded_rect(dt, (cx - tw//2 + 3, cy - th//2 + 3, cx + tw//2 + 3, cy + th//2 + 3), r, fill=(0, 0, 0, 80))
    
    # --- 牌身 (主色) ---
    draw_rounded_rect(dt, (cx - tw//2, cy - th//2, cx + tw//2, cy + th//2), r, fill=bg_color)
    
    # --- 牌身边框 ---
    draw_rounded_rect(dt, (cx - tw//2, cy - th//2, cx + tw//2, cy + th//2), r, outline="#B8A88A", width=2)
    
    # --- 内框 (浅色装饰线) ---
    draw_rounded_rect(dt, (cx - tw//2 + 6, cy - th//2 + 6, cx + tw//2 - 6, cy + th//2 - 6), r-3, outline="#D4C8AA", width=1)
    
    # --- 顶部小数字 (万、条、饼用) ---
    small_num = None
    main_char = char
    if char in ['一萬','二萬','三萬','四萬','五萬','六萬','七萬','八萬','九萬']:
        small_num = char[0]
        main_char = '萬'
    elif char in ['一條','二條','三條','四條','五條','六條','七條','八條','九條']:
        small_num = char[0]
        main_char = '條'
    elif char in ['一筒','二筒','三筒','四筒','五筒','六筒','七筒','八筒','九筒']:
        small_num = char[0]
        main_char = '筒'
    
    try:
        # 尝试用 WQY 显示主字符（更清晰）
        main_font = ImageFont.truetype(FONT_WQY, 26)
        small_font = ImageFont.truetype(FONT_WQY, 12)
        
        # 上色：不同花色不同颜色
        if color:
            fill_color = color
        elif main_char in ['萬']:
            fill_color = "#CC2233"  # 红色
        elif main_char in ['條']:
            fill_color = "#228B22"  # 绿色
        elif main_char in ['筒']:
            fill_color = "#2266CC"  # 蓝色
        elif main_char in ['東','南','西','北']:
            fill_color = "#224488"  # 深蓝
        elif main_char == '發':
            fill_color = "#1B6B1B"  # 深绿
        elif main_char == '中':
            fill_color = "#CC1111"  # 大红
        else:
            fill_color = "#222222"
        
        # 绘制主字符
        mb = dt.textbbox((0,0), main_char, font=main_font)
        mw = mb[2] - mb[0]
        mh = mb[3] - mb[1]
        dt.text((cx - mw//2, cy - mh//2), main_char, fill=fill_color, font=main_font)
        
        # 绘制小数字 (左上角)
        if small_num:
            dt.text((cx - tw//2 + 8, cy - th//2 + 8), small_num, fill=fill_color, font=small_font)
        
        # 中字带红色圆框
        if main_char == '中':
            # 绘制红色圆框
            dt.ellipse([cx-16, cy-16, cx+16, cy+16], outline="#CC1111", width=3)
        
        # 發字周围绿色装饰
        if main_char == '發':
            dt.rectangle([cx-18, cy-22, cx+18, cy+22], outline="#1B6B1B", width=2)
        
    except Exception as e:
        print(f"  Font error: {e}")
    
    # 裁剪到实际内容区域
    tile = tile.crop(tile.getbbox()) if tile.getbbox() else tile
    
    # 旋转
    if rotated != 0:
        tile = tile.rotate(rotated, expand=True, resample=Image.BICUBIC)
    
    return tile

# ==================== 1. 加载页 ====================

def create_loading_page():
    """绘制加载页 - 暗红背景 + 金色边框 + 祥云 + 标题 + 手工麻将牌"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # --- 暗红色渐变背景 ---
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        # 径向渐变：中心到边缘变暗
        dx = W/2
        dy = H/2
        dist = min(1.0, math.sqrt((y-H/2)**2 + (W/2)**2) / math.sqrt((H/2)**2 + (W/2)**2))
        r = int(80 * (1 - dist * 0.5))
        g = int(20 * (1 - dist * 0.4))
        b = int(30 * (1 - dist * 0.3))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    
    # --- 金色回纹边框 (更精致) ---
    border_color = (212, 175, 55, 255)  # 金色
    light_gold = (240, 220, 150, 255)
    
    # 外边框
    draw.rectangle([10, 10, W-11, H-11], outline=border_color, width=3)
    # 内边框
    draw.rectangle([20, 20, W-21, H-21], outline=light_gold, width=1)
    # 中间装饰框
    draw.rectangle([25, 25, W-26, H-26], outline=border_color, width=1)
    
    # --- 四角祥云装饰 ---
    try:
        wqy = ImageFont.truetype(FONT_WQY, 36)
        cloud_chars = "☁✧☯✦❂"
        corners = [(60, 50), (W-80, 50), (60, H-60), (W-80, H-60)]
        for cx, cy in corners:
            for i, ch in enumerate(cloud_chars):
                alpha = 80 + random.randint(0, 60)
                c = (212, 175, 55, alpha)
                draw.text((cx + i*30 - 60, cy + (i%3)*25 - 30), ch, fill=c, font=wqy)
    except:
        pass
    
    # --- 下方金色半透明装饰线 ---
    for y_pos in [H-110, H-105, H-100]:
        draw.line([(60, y_pos), (W-60, y_pos)], fill=(212, 175, 55, 60), width=1)
    
    # --- 四角纯金装饰 ---
    corner_size = 40
    for ox, oy, dx_dir, dy_dir in [(30, 30, 1, 1), (W-30, 30, -1, 1), (30, H-30, 1, -1), (W-30, H-30, -1, -1)]:
        draw.line([(ox, oy), (ox + dx_dir * corner_size, oy)], fill=border_color, width=3)
        draw.line([(ox, oy), (ox, oy + dy_dir * corner_size)], fill=border_color, width=3)
    
    # --- 标题 "砀山235麻将" ---
    try:
        title_font = ImageFont.truetype(FONT_WQY, 72)
        title = "砀山235麻将"
        tb = draw.textbbox((0, 0), title, font=title_font)
        tw = tb[2] - tb[0]
        th = tb[3] - tb[1]
        tx = W//2 - tw//2
        ty = 120
        
        # 多层阴影效果
        for offset_x, offset_y, alpha in [(-4,4,120), (-2,3,80), (0,2,40)]:
            shadow_layer = Image.new('RGBA', (W, H), (0,0,0,0))
            sd = ImageDraw.Draw(shadow_layer)
            sd.text((tx+offset_x, ty+offset_y), title, fill=(0,0,0,alpha), font=title_font)
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
            img = Image.alpha_composite(img, shadow_layer)
        
        # 黑色轮廓
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx == 0 and dy == 0:
                    continue
                draw.text((tx+dx, ty+dy), title, fill=(30, 20, 10, 255), font=title_font)
        
        # 白色内发光
        draw.text((tx-1, ty-1), title, fill=(255, 250, 240, 200), font=title_font)
        draw.text((tx+1, ty+1), title, fill=(255, 250, 240, 150), font=title_font)
        
        # 主文字 - 金色渐变
        for y_off in range(th):
            progress = y_off / th
            r = int(255 - progress * 20)
            g = int(215 + progress * 15)
            b = int(50 - progress * 20)
            draw.text((tx, ty + y_off), title, fill=(r, g, b, 255), font=title_font)
        
        # --- 英文副标题 ---
        eng_font = ImageFont.truetype(FONT_WQY, 22)
        eng_text = "DangShan 235 Mahjong"
        eb = draw.textbbox((0, 0), eng_text, font=eng_font)
        ew = eb[2] - eb[0]
        eh = eb[3] - eb[1]
        ex = W//2 - ew//2
        ey = ty + th + 15
        
        # 英文阴影
        for ox, oy in [(1,1)]:
            draw.text((ex+ox, ey+oy), eng_text, fill=(0,0,0,150), font=eng_font)
        draw.text((ex, ey), eng_text, fill=(255, 230, 150, 255), font=eng_font)
        
    except Exception as e:
        print(f"Title error: {e}")
    
    # ==================== 手工麻将牌 ====================
    
    # --- 定义6张麻将牌 ---
    tile_defs = [
        ('一萬', '#CC2233', 40, 450, -15),
        ('九萬', '#CC2233', 220, 520, 8),
        ('發', '#1B6B1B', 520, 570, -10),
        ('中', '#CC1111', 720, 480, 12),
        ('東', '#224488', 950, 550, -8),
        ('八萬', '#CC2233', 1130, 460, 20),
    ]
    
    for ch, color, x, y, rot in tile_defs:
        tile = draw_mahjong_tile(ch, color, size=(80, 112), rotated=rot)
        # 计算旋转后的实际位置居中
        img.paste(tile, (x - tile.width//2, y - tile.height//2), tile)
        print(f"  Tile '{ch}' placed at ({x}, {y}) rotated {rot}°")
    
    # --- 加载进度条 (底部) ---
    bar_y = H - 60
    bar_w = 500
    bar_h = 18
    bar_x = W//2 - bar_w//2
    
    # 进度条背景
    draw_rounded_rect(draw, (bar_x, bar_y, bar_x+bar_w, bar_y+bar_h), 9, fill=(60, 30, 20, 200), outline=(180, 150, 50, 200), width=1)
    
    # 进度条填充 (一半)
    fill_w = int(bar_w * 0.6)
    draw_rounded_rect(draw, (bar_x+2, bar_y+2, bar_x+fill_w-2, bar_y+bar_h-2), 7, fill=(212, 175, 55, 220))
    
    # 加载文字
    try:
        load_font = ImageFont.truetype(FONT_WQY, 16)
        load_text = "LOADING..."
        lb = draw.textbbox((0, 0), load_text, font=load_font)
        lw = lb[2] - lb[0]
        draw.text((bar_x + fill_w + 15, bar_y + 2), load_text, fill=(212, 175, 55, 200), font=load_font)
    except:
        pass
    
    return img

# ==================== 2. 房间桌布 ====================

def create_room_bg():
    """绘制桌布 - 绿色绒面 + 楷体艺术字logo居中"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # --- 深绿色绒布纹理 ---
    base_green = (20, 80, 40)
    for y in range(H):
        # 细微纹理变化
        noise = random.randint(-15, 15)
        r = max(0, min(255, base_green[0] + noise))
        # 轻微的波浪纹理
        wave = int(math.sin(y * 0.05) * 5)
        g = max(0, min(255, base_green[1] + wave + noise//2))
        b = max(0, min(255, base_green[2] + wave//2 + noise//3))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    
    # --- 细微纹理点阵 ---
    for _ in range(8000):
        x = random.randint(0, W-1)
        y = random.randint(0, H-1)
        shade = random.randint(-20, 10)
        r = max(0, min(255, 20 + shade))
        g = max(0, min(255, 80 + shade))
        b = max(0, min(255, 40 + shade))
        img.putpixel((x, y), (r, g, b, 255))
    
    # --- 暗角效果 ---
    vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for y in range(H):
        for x in range(W):
            dist_x = abs(x - W/2) / (W/2)
            dist_y = abs(y - H/2) / (H/2)
            dist = max(dist_x, dist_y)
            if dist > 0.6:
                alpha = int((dist - 0.6) * 200)
                vd.point((x, y), fill=(0, 0, 0, min(alpha, 100)))
    img = Image.alpha_composite(img, vignette)
    
    # --- 桌布边框 (金色) ---
    border_color = (180, 150, 60, 150)
    draw.rectangle([15, 15, W-16, H-16], outline=border_color, width=2)
    draw.rectangle([25, 25, W-26, H-26], outline=(180, 150, 60, 80), width=1)
    
    # 四角金色装饰
    corner_len = 60
    for ox, oy, dx, dy in [(15, 15, 1, 1), (W-15, 15, -1, 1), (15, H-15, 1, -1), (W-15, H-15, -1, -1)]:
        points = [
            (ox + dx*corner_len, oy),
            (ox + dx*corner_len - dx*15, oy + dy*15),
            (ox, oy + dy*15),
            (ox, oy + dy*corner_len - dy*15),
            (ox + dx*15, oy + dy*corner_len - dy*15),
            (ox + dx*15, oy + dy*15),
            (ox + dx*15, oy),
        ]
        draw.line(points, fill=(200, 175, 80, 120), width=2)
    
    # ==================== 艺术字LOGO ====================
    # 使用UKai楷体 + 金属质感效果
    
    try:
        # --- Logo 主文字 "砀山235麻将" ---
        logo_text = "砀山235麻将"
        
        # 尝试较大尺寸（大约占宽度的60%）
        logo_size = 84
        logo_font = ImageFont.truetype(FONT_UKAI, logo_size)
        lb = draw.textbbox((0, 0), logo_text, font=logo_font)
        lw = lb[2] - lb[0]
        lh = lb[3] - lb[1]
        
        # 计算缩放以适配宽度
        target_w = int(W * 0.55)
        scale = min(1.0, target_w / lw)
        actual_size = int(logo_size * scale)
        logo_font = ImageFont.truetype(FONT_UKAI, actual_size)
        lb = draw.textbbox((0, 0), logo_text, font=logo_font)
        lw = lb[2] - lb[0]
        lh = lb[3] - lb[1]
        
        lx = W//2 - lw//2
        ly = H//2 - lh//2 - 40  # 居中偏上
        
        print(f"Logo '{logo_text}' font_size={actual_size}, pos=({lx}, {ly}), size=({lw}, {lh})")
        
        # --- 创建单独的logo图层用于处理 ---
        logo_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(logo_layer)
        
        # 描边（深色轮廓使文字更立体）
        stroke_width = 3
        for sx in range(-stroke_width, stroke_width+1):
            for sy in range(-stroke_width, stroke_width+1):
                if abs(sx) + abs(sy) > stroke_width:
                    continue
                ld.text((lx+sx, ly+sy), logo_text, fill=(0, 0, 0, 120), font=logo_font)
        
        # 主文字 - 金色金属质感（每个字符高度渐变）
        for y_off in range(lh + 10):
            # 顶部亮、底部暗的金色渐变
            progress = y_off / (lh + 10) if lh > 0 else 0
            r = int(255 - progress * 60)
            g = int(210 - progress * 80) 
            b = int(50 - progress * 40)
            ld.text((lx, ly + y_off), logo_text, fill=(r, g, b, 255), font=logo_font)
        
        # 高光（顶部加亮）
        highlight_size = max(1, int(lh * 0.2))
        for y_off in range(highlight_size):
            progress = 1.0 - y_off / highlight_size
            r_hl = int(255 * progress)
            g_hl = int(240 * progress)
            b_hl = int(180 * progress)
            ld.text((lx, ly + y_off), logo_text, fill=(r_hl, g_hl, b_hl, 200), font=logo_font)
        
        # 外发光
        glow = logo_layer.filter(ImageFilter.GaussianBlur(radius=8))
        glow.putalpha(80)  # 半透明
        
        # 二次外发光（更远）
        glow2 = logo_layer.filter(ImageFilter.GaussianBlur(radius=20))
        glow2.putalpha(40)
        
        # 合成到背景 - 先远光再近光再主文字
        img = Image.alpha_composite(img, glow2)
        img = Image.alpha_composite(img, glow)
        
        # 主文字 - 半透明（alpha ~100 左右）
        logo_rgba = logo_layer.copy()
        # 降低透明度到半透明效果
        r, g, b, a = logo_rgba.split()
        a = a.point(lambda x: int(x * 0.4) if x > 0 else 0)  # 40% 透明度
        logo_rgba = Image.merge('RGBA', (r, g, b, a))
        
        # 金色描边（加强轮廓可见度）
        stroke_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stroke_layer)
        for sx in range(-2, 3):
            for sy in range(-2, 3):
                sd.text((lx+sx, ly+sy), logo_text, fill=(200, 170, 60, 60), font=logo_font)
        img = Image.alpha_composite(img, stroke_layer)
        
        img = Image.alpha_composite(img, logo_rgba)
        
        # ==================== 装饰元素 ====================
        decor_font = ImageFont.truetype(FONT_UKAI, 30)
        
        # 半透明金色装饰：圆圈、小矩形、菱形
        decor_draw = ImageDraw.Draw(img)
        
        # 金色圆环
        for cx, cy, r_size, alpha_val in [
            (150, 150, 40, 40),
            (W-150, 180, 35, 35),
            (200, H-150, 30, 30),
            (W-200, H-180, 35, 40),
            (W//2, 100, 25, 30),
            (W//2, H-100, 25, 30),
        ]:
            # 圆环
            decor_draw.ellipse(
                [cx-r_size, cy-r_size, cx+r_size, cy+r_size],
                outline=(212, 180, 70, alpha_val), width=2
            )
            # 内部小圆
            decor_draw.ellipse(
                [cx-3, cy-3, cx+3, cy+3],
                fill=(200, 170, 60, alpha_val)
            )
        
        # 四角星形装饰
        for sx, sy, size, alpha_val in [
            (120, 220, 15, 35),
            (W-130, 250, 12, 30),
            (180, H-200, 14, 35),
            (W-180, H-220, 12, 30),
        ]:
            points = []
            for i in range(10):
                angle = i * math.pi / 5 - math.pi / 2
                r_star = size if i % 2 == 0 else size * 0.4
                x = sx + math.cos(angle) * r_star
                y = sy + math.sin(angle) * r_star
                points.append((x, y))
            decor_draw.polygon(points, fill=(212, 180, 70, alpha_val), outline=(180, 150, 50, alpha_val))
        
        # 矩形装饰
        for rx, ry, rw, rh, alpha_val in [
            (100, 300, 60, 4, 30),
            (W-150, 350, 50, 4, 30),
            (150, 500, 4, 50, 30),
            (W-120, 450, 4, 60, 30),
        ]:
            decor_draw.rectangle([rx, ry, rx+rw, ry+rh], fill=(200, 165, 50, alpha_val))
        
        # 小圆点装饰
        for _ in range(30):
            dx = random.randint(40, W-40)
            dy = random.randint(40, H-40)
            # 避开 logo 区域
            if abs(dx - W//2) < 300 and abs(dy - H//2) < 150:
                continue
            dot_size = random.randint(2, 5)
            dot_alpha = random.randint(15, 35)
            decor_draw.ellipse(
                [dx-dot_size, dy-dot_size, dx+dot_size, dy+dot_size],
                fill=(200, 170, 60, dot_alpha)
            )
        
    except Exception as e:
        print(f"Logo error: {e}")
        import traceback
        traceback.print_exc()
    
    return img

# ==================== MAIN ====================

if __name__ == "__main__":
    print("=== Creating Loading Page v4 ===")
    loading = create_loading_page()
    loading.save('/www/wwwroot/mahjong-download/loading_v4.png')
    print(f"  Saved: loading_v4.png ({loading.size})")
    
    print("\n=== Creating Room Tablecloth v4 ===")
    room = create_room_bg()
    room.save('/www/wwwroot/mahjong-download/room_v4.png')
    print(f"  Saved: room_v4.png ({room.size})")
    
    print("\nDone!")
