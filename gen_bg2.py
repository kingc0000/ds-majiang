import json, urllib.request

with open("/root/.hermes/credentials.json") as f:
    key = json.load(f)["agnes_ai"]["api_key"]

headers = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

# ======= 1. 加载页背景 - 带散落的麻将牌 =======
payload1 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Chinese mahjong game loading screen background, landscape horizontal 16:9. Dark red background color #6F1A19 with traditional Chinese golden decorative borders and cloud patterns. Several mahjong tiles randomly scattered across the scene - tiles like bamboo suit, character suit and dragon tiles in ivory white with green/red engravings. Fun and festive atmosphere. Golden glowing area at bottom for loading bar. No text, no characters, just decorative background with scattered tiles.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload1).encode(), headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    r1 = json.loads(r.read())
print("加载页 URL:", r1["data"][0]["url"])

# ======= 2. 桌布背景 =======
payload2 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Flat green felt fabric texture for mahjong table surface, top-down straight view. Solid dark green color with thin gold border. Subtle gold Chinese cloud and coin motifs scattered as decorative elements. Clean minimal casino style felt texture, no text, just the green fabric with subtle gold decorative accents.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload2).encode(), headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    r2 = json.loads(r.read())
print("桌布 URL:", r2["data"][0]["url"])