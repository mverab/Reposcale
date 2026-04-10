"""Migration script from v1 to v2 — incomplete and untested."""

import json
import yaml


def migrate_config(v1_path: str = "site.json", v2_path: str = "site.yaml"):
    """Convert v1 JSON config to v2 YAML format."""
    with open(v1_path) as f:
        v1 = json.load(f)

    v2 = {
        "version": 2,
        "source_dir": v1.get("source_dir", "content/"),
        "output_dir": v1.get("output_dir", "build/").replace("build", "dist"),
        "plugins": ["markdown"],
        # TODO: migrate template to theme
        # TODO: migrate custom settings
    }

    with open(v2_path, "w") as f:
        yaml.dump(v2, f)

    print(f"Migrated {v1_path} → {v2_path}")


# TODO: migrate content files
# TODO: migrate assets
# TODO: validate migration
