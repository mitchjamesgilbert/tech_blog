from app.models import BlogPost
from app import db

def load_articles():
    return BlogPost.query.all()

def save_articles(title, content, tags):
    new_article = BlogPost(
        title=title,
        content=content,
        tags=",".join(tags)
    )
    db.session.add(new_article)
    db.session.commit()

def update_article(article_id, title=None, content=None, tags=None):
    article = BlogPost.query.get(article_id)
    if not article:
        return None
    
    if title:
        article.title = title
    if content:
        article.content = content
    if tags:
        article.tags = ",".join(tags)
    
    db.session.commit()
    return article

def delete_article(article_id):
    article = BlogPost.query.get(article_id)
    if not article:
        return None
    
    db.session.delete(article)
    db.session.commit()
    return True