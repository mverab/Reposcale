"""v1 monolithic renderer — still used in production."""

import os


def render_site(source_dir: str, output_dir: str, config: dict):
    """Render all markdown files to HTML."""
    os.makedirs(output_dir, exist_ok=True)

    template = config.get("template", "<html><body>{content}</body></html>")

    for fname in os.listdir(source_dir):
        if fname.endswith(".md"):
            with open(os.path.join(source_dir, fname)) as f:
                content = f.read()

            html = template.replace("{content}", _md_to_html(content))
            out_name = fname.replace(".md", ".html")
            with open(os.path.join(output_dir, out_name), "w") as f:
                f.write(html)


def _md_to_html(text: str) -> str:
    """Naive markdown to HTML conversion."""
    lines = []
    for line in text.split("\n"):
        if line.startswith("# "):
            lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{line[3:]}</h2>")
        elif line.strip():
            lines.append(f"<p>{line}</p>")
    return "\n".join(lines)
