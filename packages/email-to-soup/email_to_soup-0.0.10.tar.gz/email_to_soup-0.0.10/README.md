# email-to-soup
Convert Email to HTML-Soup &amp; Soup-Text

## Usage
```python
from email_to_soup import soupify_email

email = """ your email here
"""
soup_object = soupify_email(email)
print(soup_object.soup_text)
print(soup_object.html_body)
print(soup_object.html_soup)
```
