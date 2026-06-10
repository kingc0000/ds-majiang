import json, urllib.request

with open("/root/.hermes/credentials.json") as f:
    key = json.load(f)["agnes_ai"]["api_key"]

headers = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

# 1. 加载页 - 横屏 landscape
payload1 = {
    "model": "agnes-image-2.1-flash",
    "prompt": "A Chinese mahjong game loading screen, landscape horizontal layout 16:9. Dark red background with golden Chinese decorative borders and traditional patterns. The game title '砀山235麻将' in large bold golden Chinese calligraphy style font in the center. A traditional mahjong tile like 發 or 中 as decoration below the title. A loading progress bar at bottom in gold gradient. Elegant cloud and dragon shadow patterns in background. Professional mobile game UI style.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload1).encode(),
    headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    result1 = json.loads(r.read())
print("加载页 URL:", result1["data"][0]["url"])

# 2. 房间 - 纯2D桌面俯视图
payload2 = {
    "model": "agnes-image-2.1-flash",
    "prompt": "Pure top-down 2D view of a mahjong table surface, flat design. Dark green felt tablecloth texture with gold embroidered borders. The title '砀山235麻将' in gold Chinese calligraphy at top center area. Mahjong tile motifs like bamboo, characters and dots as subtle watermark patterns on the fabric. Clean flat 2D perspective, no 3D depth, no perspective angle, just the straight top-down table surface. High quality fabric texture, casino style mahjong table.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload2).encode(),
    headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    result2 = json.loads(r.read())
print("房间背景 URL:", result2["data"][0]["url"])
