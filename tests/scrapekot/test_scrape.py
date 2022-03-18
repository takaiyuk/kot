from kot.scrapekot.scrape import Scraper

s = Scraper(html="")


def test_Scraper__str_to_int():
    string_value = "1"
    integer_value = s._str_to_int(string_value)
    expected = 1
    assert integer_value == expected


def test_Scraper__clean_test():
    string_value = "ab\ncd ef"
    cleaned_value = s._clean_text(string_value)
    expected = "abcdef"
    assert cleaned_value == expected
