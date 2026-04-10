"""v1 config — flat dictionary format."""

DEFAULT_CONFIG = {
    "source_dir": "content/",
    "output_dir": "build/",
    "template": "<html><head><title>Site</title></head><body>{content}</body></html>",
    "base_url": "/",
}


def load_config(path: str = "site.json") -> dict:
    import json
    try:
        with open(path) as f:
            user = json.load(f)
        return {**DEFAULT_CONFIG, **user}
    except FileNotFoundError:
        return dict(DEFAULT_CONFIG)
