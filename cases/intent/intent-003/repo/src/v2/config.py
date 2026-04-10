"""v2 config — YAML-based, conflicts with v1 JSON format."""

DEFAULT_CONFIG = {
    "version": 2,
    "source_dir": "content/",
    "output_dir": "dist/",  # Different from v1's "build/"
    "plugins": ["markdown"],
    "theme": "default",
    "base_url": "/",
}


def load_config(path: str = "site.yaml") -> dict:
    import yaml
    try:
        with open(path) as f:
            user = yaml.safe_load(f)
        return {**DEFAULT_CONFIG, **(user or {})}
    except FileNotFoundError:
        return dict(DEFAULT_CONFIG)
