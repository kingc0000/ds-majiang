import json, urllib.request

with open("/root/.hermes/credentials.json") as f:
    key = json.load(f)["agnes_ai"]["api_key"]

headers = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

# ======= 加载页背景 =======
payload1 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Chinese mahjong game loading screen background, landscape horizontal 16:9. Dark red background color #6F1A19 with traditional Chinese golden decorative borders and patterns. Elegant cloud and dragon motifs as subtle watermark. Golden gradient area at bottom for progress bar. Traditional Chinese aesthetic, no text, no characters, just decorative background pattern.",
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

# ======= 桌布背景 =======
payload2 = {
    "model": "agnes-image-2.0-flash",
    "prompt": "Flat green felt fabric texture for mahjong table surface, top-down view. Solid dark green color with thin gold border trim. Clean minimal casino style felt texture, no patterns, no decorative elements, no text, just the green felt fabric surface with subtle fabric weave texture.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload2).encode(),
    headers, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    result2 = json.loads(r.read())
print("桌布 URL:", result2["data"][0]["url"])