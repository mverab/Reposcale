from src.weather import display


def test_display_formats_output(capsys):
    display({"city": "NYC", "temp": 22.5, "description": "clear sky"})
    output = capsys.readouterr().out
    assert "NYC" in output
    assert "22.5" in output
