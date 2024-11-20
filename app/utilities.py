import os
import yaml
import markdown2
from datetime import datetime

POSTS_DIR = "./app/posts"

def load_articles():
    """Load all articles from the posts folder."""
    articles = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            article = load_article(filename)
            if article:
                articles.append(article)
    return sorted(articles, key=lambda x: x['date'], reverse=True)  # Sort by date

def load_article(filename):
    """Load a single article from a Markdown file."""
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as file:
        content = file.read()

    # Parse front matter (YAML metadata)
    if content.startswith("---"):
        _, front_matter, body = content.split("---", 2)
        metadata = yaml.safe_load(front_matter)
    else:
        metadata = {}

    # Convert Markdown to HTML
    html_body = markdown2.markdown(body)

    return {
        "filename": filename,
        "title": metadata.get("title", "Untitled"),
        "date": datetime.strptime(metadata.get("date", "1970-01-01"), "%Y-%m-%d"),
        "tags": metadata.get("tags", []),
        "content": html_body,
    }

def save_article(title, content, tags, filename=None):
    """Save a new or updated article to a Markdown file."""
    metadata = {
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": tags,
    }
    if not filename:
        filename = f"{title.lower().replace(' ', '-')}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    with open(filepath, "w") as file:
        file.write("---\n")
        file.write(yaml.dump(metadata))
        file.write("---\n")
        file.write(content)

def delete_article(filename):
    """Delete an article by its filename."""
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
