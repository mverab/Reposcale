"""Markdown plugin — the only completed v2 plugin."""


def register():
    return MarkdownPlugin()


class MarkdownPlugin:
    name = "markdown"

    def transform(self, content: str) -> str:
        """Convert markdown to HTML (basic)."""
        lines = []
        for line in content.split("\n"):
            if line.startswith("# "):
                lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("- "):
                lines.append(f"<li>{line[2:]}</li>")
            elif line.strip():
                lines.append(f"<p>{line}</p>")
        return "\n".join(lines)
