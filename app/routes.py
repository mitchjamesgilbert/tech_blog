from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .utilities import load_articles, save_articles
from .auth import admin_required, USERS
from .models import BlogPost
from app import db
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/posts', methods=['GET'])
def posts():
    search_query = request.args.get('search', '').strip()
    if search_query:
        # Filter posts based on the search query
        articles = BlogPost.query.filter(
            (BlogPost.title.ilike(f"%{search_query}%")) |
            (BlogPost.content.ilike(f"%{search_query}%")) |
            (BlogPost.tags.ilike(f"%{search_query}%"))
        ).all()
    else:
        # Fetch all posts if no search query is provided
        articles = BlogPost.query.all()
    
    return render_template('posts.html', articles=articles)


@bp.route('/post/<int:article_id>')
def post(article_id):
    article = BlogPost.query.get_or_404(article_id)
    return render_template('post.html', article=article)

@bp.route('/admin')
@admin_required
def admin():
    articles = load_articles()
    return render_template('admin.html', articles=articles)

@bp.route('/edit-post/<int:article_id>', methods=['GET', 'POST'])
@admin_required
def edit_post(article_id):
    article = BlogPost.query.get_or_404(article_id)
    
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.tags = ",".join(request.form.getlist('tags'))
        db.session.commit()
        return redirect(url_for('routes.admin'))

    return render_template('edit_post.html', article=article)

@bp.route('/delete-post/<int:article_id>')
@admin_required
def delete_post(article_id):
    article = BlogPost.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('routes.admin'))

@bp.route('/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    if request.method == 'POST':

        new_article = BlogPost(
            title=request.form['title'],
            content=request.form['content'],
            date_posted = datetime.now(),
            tags=",".join(request.form.getlist('tags'))
        )
        db.session.add(new_article)
        db.session.commit()
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
