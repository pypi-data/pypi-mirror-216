import re
from bs4 import BeautifulSoup
from bs4 import Tag
from typing import Optional, Tuple
from email.parser import Parser
from email.policy import default as default_policy
from dataclasses import dataclass
from lxml import html
import html2text


MULTIPLE_SPACES_REGEX = re.compile(r"[\s\u200c]+")

@dataclass
class EmailSoup:
    html_body: Optional[Tag]
    soup_text: str
    html_soup: BeautifulSoup
    xml_tree: html.HtmlElement
    markdown_text: str = None
    url_soup: Tuple[str, dict] = None

def soupify_email(email: str) -> EmailSoup:
    """Convert an email string to a BeautifulSoup object.

    Args:
        email: The email string to convert.

    Returns:
        An EmailSoup object representing the email html-soup, html-body, soup-text.
    """
    email = Parser(policy=default_policy).parsestr(email)
    html_body = email.get_body(preferencelist=('html', 'plain')).get_content()

    # Oh, the wonders of HTML emails. Some emails have multiple <html> tags. Let's use the one with more content.
    if html_body:
        try:
            html_body = max(re.findall(r"<html.*?</html>", html_body, re.M|re.S|re.I), key=len)
        except ValueError:
            html_body = html_body
            
    html_soup = BeautifulSoup(html_body, features="lxml")
    xml_tree = html.fromstring(html_body)
    email_soup = EmailSoup(
        html_soup = html_soup,
        soup_text = _extract_soup_text(html_soup),
        html_body = html_body,
        xml_tree = xml_tree,
        markdown_text = _markdownify_email(html_body),
        url_soup = _extract_url_soup(html_soup)
    )
    return email_soup


def _markdownify_email(html_body: str) -> Optional[str]:
    try:
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_tables = False
        markdown_text = h.handle(html_body)
        return markdown_text
    except Exception:
        return ""

def _extract_soup_text(html_soup: BeautifulSoup) -> str:
    try:
        soup_text = re.sub(
            MULTIPLE_SPACES_REGEX, " ", html_soup.get_text(strip=True, separator=" ")
        ).strip()
    except Exception:  # pylint: disable=broad-except
        return ""

    return soup_text

def _extract_url_soup(html_soup: BeautifulSoup) -> Tuple[str, dict]:
    url_soup = ""
    link_counter = 1
    url_dict = {}
    for link in html_soup.find_all("a"):
        full_link = link.get("href")
        enumerated_link = f"https://{link_counter}.com"

        # add the link to the url dict
        url_dict[enumerated_link] = full_link
        # get the link text and url
        url_soup += f"{link.text.strip()} url: {enumerated_link}.\n"

        link_counter += 1

    return (url_soup, url_dict)
