from sanic import Sanic
from sanic.response import json, file
from sanic.exceptions import NotFound
from sanic.log import logger
from pathlib import Path
import yaml

app = Sanic("cyoa")

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
ADVENTURES_DIR = STATIC_DIR / "adventures"


def load_scene(adventure_id: str, scene_id: str):
    scene_path = ADVENTURES_DIR / adventure_id / "scenes" / f"{scene_id}.yaml"
    if not scene_path.exists():
        raise NotFound(f"Scene '{scene_id}' not found")

    data = yaml.safe_load(scene_path.read_text())

    # Load text (textfile takes precedence)
    if "textfile" in data:
        text_path = scene_path.parent / data["textfile"]
        if not text_path.exists():
            raise NotFound(f"Text file '{data['textfile']}' not found")
        text = text_path.read_text()
    elif "text" in data:
        text = data["text"]
    else:
        text = ""

    choices = [
        {"label": label, "next": next_scene}
        for label, next_scene in data.get("choices", {}).items()
    ]

    image_url = None
    if "image" in data:
        #image_url = f"/static/adventures/{adventure_id}/images/{data['image']}"
        image_url = f"/assets/{adventure_id}/images/{data['image']}"
        logger.debug(f"Image URL: {image_url}")

    return {
        "id": data.get("id", scene_id),
        "text": text,
        "image": image_url,
        "choices": choices
    }

@app.get("/debug")
async def debug(request):
    url = ADVENTURES_DIR / "demo" / "images" / "trees.webp"
    return json({
        "url" : f"{url}",
        "exists": (
            url
        ).exists()
    })


@app.get("/")
async def landing_page(request):
    return await file(STATIC_DIR / "index.html")


@app.get("/play")
async def play_page(request):
    return await file(STATIC_DIR / "play.html")


@app.get("/api/adventures")
async def list_adventures(request):
    adventures = []
    for path in ADVENTURES_DIR.iterdir():
        if path.is_dir():
            adventures.append(path.name)
    return json(adventures)


@app.get("/adventure/<adventure_id>/scene/<scene_id>")
async def get_scene(request, adventure_id, scene_id):
    scene = load_scene(adventure_id, scene_id)
    return json(scene)


#app.static("/static", STATIC_DIR)
#app.static("/static/adventures", ADVENTURES_DIR)

app.static("/static", STATIC_DIR, name="static_root")
app.static("/assets", ADVENTURES_DIR, name="adventure_assets")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, dev=True)
