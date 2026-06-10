import json, urllib.request

with open("/root/.hermes/credentials.json") as f:
    key = json.load(f)["agnes_ai"]["api_key"]

headers = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

payload = {
    "model": "agnes-image-2.1-flash",
    "prompt": "A mahjong room tablecloth background, top-down view of a professional mahjong table. Dark green velvet texture with gold embroidered borders and Chinese traditional patterns. The title 砀山235麻将 embossed in gold Chinese calligraphy at top center area. Mahjong tile motifs including bamboo, characters and dots as subtle watermark patterns woven into fabric. Gold fringed edges. Luxury casino-style mahjong table aesthetic. Wide landscape ratio, high detail fabric texture, no UI elements, pure tablecloth background.",
    "size": "1344x768"
}

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/images/generations",
    json.dumps(payload).encode(),
    headers,
    method="POST"
)

with urllib.request.urlopen(req, timeout=60) as r:
    result = json.loads(r.read())

print("房间背景 URL:", result["data"][0]["url"])
