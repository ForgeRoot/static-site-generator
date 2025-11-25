import unittest
from src.generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_heading(self):
        markdown_text = "# Title"
        title = extract_title(markdown_text)
        self.assertEqual(title, "Title")

    def test_trailing_heading(self):
        markdown_text = "#     Title hoi      "
        title = extract_title(markdown_text)
        self.assertEqual(title, "Title hoi")

    def test_heading_with_multiple_blocks(self):
        markdown_text = """Some paragraph text

# Main Title

## Subheading

More content here"""
        title = extract_title(markdown_text)
        self.assertEqual(title, "Main Title")

    def test_heading_after_other_content(self):
        markdown_text = """Paragraph 1

Paragraph 2

# The Title

Content"""
        title = extract_title(markdown_text)
        self.assertEqual(title, "The Title")

    def test_only_h2_no_h1(self):
        markdown_text = """## Subheading Only

Some content"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown_text)
        self.assertEqual(str(context.exception), "There is no title found")

    def test_no_heading_at_all(self):
        markdown_text = """Just some regular text

And another paragraph"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown_text)
        self.assertEqual(str(context.exception), "There is no title found")

    def test_empty_markdown(self):
        markdown_text = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown_text)
        self.assertEqual(str(context.exception), "There is no title found")

    def test_h1_with_special_characters(self):
        markdown_text = "# Title with *emphasis* and **bold**"
        title = extract_title(markdown_text)
        self.assertEqual(title, "Title with *emphasis* and **bold**")

    def test_multiple_h1_headings(self):
        markdown_text = """# First Title

Some content

# Second Title"""
        title = extract_title(markdown_text)
        self.assertEqual(title, "First Title")

    def test_h1_with_numbers_and_symbols(self):
        markdown_text = "# 2024: A Year of Innovation!"
        title = extract_title(markdown_text)
        self.assertEqual(title, "2024: A Year of Innovation!")