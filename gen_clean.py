import json, urllib.request

with open("/root/.hermes/credentials.json") as f:
    key = json.load(f)["agnes_ai"]["api_key"]

headers = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

# ======= 加载页背景 - 绝对没有任何麻将牌 =======
payload1 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Chinese mahjong game loading screen background, landscape horizontal 16:9. Dark red background color #6F1A19 with traditional Chinese golden decorative borders. Chinese cloud patterns as subtle watermark at four corners. Golden gradient bar at bottom center for loading progress. No mahjong tiles at all. No text. Just the empty decorative background.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload1).encode(), headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    r1 = json.loads(r.read())
print("加载页URL:", r1["data"][0]["url"])

# ======= 桌布背景 - 绝对没有任何元素 =======
payload2 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Solid dark green felt fabric texture, top-down flat 2D view, filling the entire frame. Pure deep green color like a casino mahjong table felt. Subtle fabric weave texture. No patterns, no borders, no decorative elements, no text, no tiles, just the plain green felt surface.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload2).encode(), headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    r2 = json.loads(r.read())
print("桌布URL:", r2["data"][0]["url"])