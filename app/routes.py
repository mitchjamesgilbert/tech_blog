from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .utilities import load_articles, load_article, save_article, delete_article
from datetime import datetime
from .auth import admin_required

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/posts', methods=['GET'])
def posts():
    search_query = request.args.get('search', '').strip()
    articles = load_articles()
    if search_query:
        articles = [
            article for article in articles
            if search_query.lower() in article['title'].lower()
            or search_query.lower() in article['content'].lower()
            or any(search_query.lower() in tag.lower() for tag in article['tags'])
        ]
    return render_template('posts.html', articles=articles)

@bp.route('/post/<filename>')
def post(filename):
    article = load_article(filename)
    if not article:
        flash('Post not found.', 'danger')
        return redirect(url_for('routes.posts'))
    return render_template('post.html', article=article)

@bp.route('/admin')
@admin_required
def admin():
    articles = load_articles()
    return render_template('admin.html', articles=articles)

@bp.route('/edit-post/<filename>', methods=['GET', 'POST'])
@admin_required
def edit_post(filename):
    article = load_article(filename)
    if not article:
        flash('Post not found.', 'danger')
        return redirect(url_for('routes.admin'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.getlist('tags')
        save_article(title, content, tags, filename=filename)
        flash('Post updated successfully.', 'success')
        return redirect(url_for('routes.admin'))

    return render_template('edit_post.html', article=article)

@bp.route('/delete-post/<filename>')
@admin_required
def delete_post(filename):
    delete_article(filename)
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('routes.admin'))

@bp.route('/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form.getlist('tags')
        save_article(title, content, tags)
        flash('Post created successfully.', 'success')
        return redirect(url_for('routes.posts'))
    return render_template('new.html')

@bp.route('/about')
def about():
    return render_template('about.html')