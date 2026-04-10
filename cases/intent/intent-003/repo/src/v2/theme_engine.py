"""v2 theme engine — stub, never implemented."""


class ThemeEngine:
    def __init__(self, theme_dir: str = "themes"):
        self.theme_dir = theme_dir
        # TODO: implement theme loading
        # TODO: implement template compilation
        # TODO: implement asset pipeline
        raise NotImplementedError("Theme engine not yet implemented")

    def apply_theme(self, content: str, theme_name: str) -> str:
        pass

    def list_themes(self) -> list[str]:
        pass
