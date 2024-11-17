from flask import Blueprint, render_template
from .utilities import load_articles

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/posts')
def posts():
    articles = load_articles()
    return render_template('posts.html', articles=articles)

@bp.route('/post/<int:article_id>')
def post(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        return "Article not found", 404
    return render_template('post.html', article=article)
