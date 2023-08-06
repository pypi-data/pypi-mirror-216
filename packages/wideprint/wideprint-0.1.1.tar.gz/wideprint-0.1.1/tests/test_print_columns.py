"""
Tests for wideprint.print_columns
"""

from wideprint import print_columns

def test_print_columns(capsys):
    """Test basic two columns"""
    print_columns(["a","b","c","d"], columns=2, sep=" ")
    out, _ = capsys.readouterr()
    assert out == '\n'.join([
        "a b",
        "c d",
    ])+"\n"


def test_print_columns_left(capsys):
    """Test basic two columns right-aligned"""
    print_columns(["aaa","b","cc","dd"], columns=2, sep=" ", alignment=">")
    out, _ = capsys.readouterr()
    assert out == '\n'.join([
        "aaa  b",
        " cc dd",
    ])+"\n"

def test_print_columns_incomplete_last_line(capsys):
    """Test basic two columns right-aligned"""
    print_columns(["abcd","e","f","g"], columns=3, sep=" ", alignment=">")
    out, _ = capsys.readouterr()
    assert out == '\n'.join([
        "abcd e f",
        "   g    ",
    ])+"\n"
