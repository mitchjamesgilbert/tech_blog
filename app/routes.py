from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from .utilities import load_articles, save_articles
from .auth import admin_required, USERS

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
@admin_required
def admin():
    articles = load_articles()
    return render_template('admin.html', articles=articles)

@bp.route('/edit-post/<int:article_id>', methods=['GET', 'POST'])
@admin_required
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
@admin_required
def delete_post(article_id):
    articles = load_articles()
    article = next((a for a in articles if a['id'] == article_id), None)
    if not article:
        flash('Post not found.', 'danger')
        return redirect(url_for('routes.admin'))

    articles = [a for a in articles if a['id'] != article_id]
    save_articles(articles)
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('routes.admin'))

@bp.route('/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    if request.method == 'POST':
        articles = load_articles()

        next_id = max([article['id'] for article in articles], default=0) + 1
        new_article = {
            "id": next_id,
            "title": request.form['title'],
            "content": request.form['content'],
            "date": request.form['date']
        }

        articles.append(new_article)
        save_articles(articles)
        return redirect(url_for('routes.posts'))
    
    return render_template('new.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('routes.admin'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.login'))
