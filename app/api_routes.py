from flask import Blueprint, jsonify, request
from app.models import BlogPost
from app import db
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    articles = BlogPost.query.all()
    return jsonify([
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "date_posted": article.date_posted.strftime('%Y-%M-%d'),
            "tags": article.tags.split(",") if article.tags else []
        }
        for article in articles
    ])

@api_bp.route('/posts/<int:article_id>', methods=['GET'])
def get_post(article_id):
    article = BlogPost.query.get_or_404(article_id)
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "date_posted": article.date_posted.strftime('%Y-%M-%d'),
        "tags": article.tags.split(",") if article.tags else []
    })

@api_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_article = BlogPost(
        title=data['title'],
        content=data['content'],
        date_posted=datetime.now(),
        tags=",".join(data.get('tags', []))
    )
    db.session.add(new_article)
    db.session.commit()
    return jsonify({"message": "Post created successfully!", "id": new_article.id}), 201

@api_bp.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'tags' in data:
        post.tags = ",".join(data['tags'])
    
    db.session.commit()
    return jsonify({
        "message": "Post updated successfully",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "date_posted": post.date_posted.strftime('%Y-%m-%d'),
            "tags": post.tags.split(",") if post.tags else []
        }
    })

@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({
        "message": f"Post with ID {post_id} deleted successfully"
    }), 200 