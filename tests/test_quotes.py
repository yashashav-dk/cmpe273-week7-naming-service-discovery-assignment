from quote_service.quotes import QUOTES, get_random_quote


def test_quotes_not_empty():
    assert len(QUOTES) >= 20


def test_quote_has_required_fields():
    for q in QUOTES:
        assert "text" in q
        assert "book" in q
        assert isinstance(q["text"], str)
        assert isinstance(q["book"], str)


def test_get_random_quote_returns_valid_quote():
    quote = get_random_quote()
    assert "text" in quote
    assert "book" in quote
    assert quote in QUOTES
