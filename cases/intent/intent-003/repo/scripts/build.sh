#!/bin/bash
# Build script — still uses v1 renderer despite v2 existing
echo "Building site with v1 renderer..."
python -c "
from src.v1.config import load_config
from src.v1.renderer import render_site
config = load_config()
render_site(config['source_dir'], config['output_dir'], config)
"
echo "Done."
