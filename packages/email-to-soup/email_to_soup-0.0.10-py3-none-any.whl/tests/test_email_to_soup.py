import pytest
from email_to_soup import soupify_email

@pytest.fixture
def email_fixture():
    return open("src/tests/fixtures/test_email.eml").read()

def test_conversion(email_fixture):
    soup = soupify_email(email_fixture)
    assert soup.html_body is not None
    assert soup.soup_text is not None
    assert soup.html_soup is not None
    assert len(soup.soup_text) == 1580
    assert len(soup.html_body) == 21834
    assert len(soup.html_soup) == 4
