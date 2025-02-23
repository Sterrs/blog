import markdown

def convert_markdown_to_html(md_text):
    """
    Converts Markdown text to HTML using Python-Markdown.
    """
    html_output = markdown.markdown(md_text)
    return html_output

# Example usage
if __name__ == "__main__":
    with open('posts/20250223_first_post.md') as f:
        md_text = f.read()
    html_result = convert_markdown_to_html(md_text)
    print(html_result)
