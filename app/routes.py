from flask import Blueprint, render_template, abort, request, redirect, url_for
from .utilities import load_articles, save_articles

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

@bp.route('/admin')
def admin():
    articles = load_articles()
    return render_template('admin.html', articles=articles)

@bp.route('/edit-post/<int:article_id>', methods=['GET', 'POST'])
def edit_post(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        abort(404)
    
    if request.method == 'POST':
        article['title'] = request.form['title']
        article['content'] = request.form['content']
        article['date'] = request.form['date']
        save_articles(articles)
        return redirect(url_for('routes.admin'))

    return render_template('edit_post.html', article=article)

@bp.route('/delete-post/<int:article_id>')
def delete_post(article_id):
    articles = load_articles()
    articles = [a for a in articles if a['id'] != article_id]
    save_articles(articles)
    return redirect(url_for('routes.admin'))

@bp.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        articles = load_articles()

        new_article = {
            "id": len(articles) + 1,
            "title": request.form['title'],
            "content": request.form['content'],
            "date": request.form['date']
        }

        articles.append(new_article)
        save_articles(articles)
        return redirect(url_for('routes.posts'))
    
    return render_template('new.html')