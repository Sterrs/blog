import os
import re
import frontmatter
import markdown

from jinja2 import Environment, FileSystemLoader

def convert_math_expressions(text):
    # Convert block math: $$ ... $$ to a raw HTML div with backslashes for MathJax delimiters.
    text = re.sub(
        r'\$\$(.*?)\$\$', 
        lambda m: '<div class="math display">\\[' + m.group(1).strip() + '\\]</div>', 
        text, flags=re.DOTALL
    )
    # Convert inline math: $ ... $ to a raw HTML span with double backslashes.
    text = re.sub(
        r'(?<!\\)\$(.+?)(?<!\\)\$', 
        lambda m: '<span class="math inline">\\\\(' + m.group(1).strip() + '\\\\)</span>', 
        text
    )
    return text

# Create build directory if it doesn't exist
if not os.path.exists('build'):
    os.makedirs('build')

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
post_template = env.get_template('post.html.j2')
homepage_template = env.get_template('homepage.html.j2')

posts_metadata = []

# Process each markdown post in the posts directory
for filename in os.listdir('posts'):
    if filename.endswith('.md'):
        filepath = os.path.join('posts', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Preprocess math expressions in the markdown content
        post.content = convert_math_expressions(post.content)
        
        # Convert markdown content to HTML with extra and tables extensions
        content_html = markdown.markdown(
            post.content, 
            extensions=['fenced_code', 'codehilite', 'tables', 'extra']
        )
        
        # Prepare post metadata for the homepage list
        post_info = {
            'title': post.get('title', 'No Title'),
            'author': post.get('author', 'Unknown'),
            'date': post.get('date', ''),
            'filename': filename.replace('.md', '.html')
        }
        posts_metadata.append(post_info)

        # Render the individual post using the post template
        rendered_post = post_template.render(
            title=post.get('title'),
            author=post.get('author'),
            date=post.get('date'),
            content=content_html
        )
        output_path = os.path.join('build', filename.replace('.md', '.html'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_post)

# Sort posts by date (assuming YYYY-MM-DD format) in descending order
posts_metadata.sort(key=lambda x: x['date'], reverse=True)

# Render the homepage with the list of posts
rendered_homepage = homepage_template.render(posts=posts_metadata)
with open(os.path.join('build', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(rendered_homepage)

print("Blog built successfully!")
