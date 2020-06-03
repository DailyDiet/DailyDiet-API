from flask import jsonify
from sqlalchemy.exc import IntegrityError

from extentions import db

from . import blog
from .forms import PostForm
from .models import Post


@blog.route('/posts/', methods=['GET'])
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    result = dict()
    for p in posts:
        tmp = dict()
        tmp['id'] = p.id
        tmp = {'slug': p.slug, 'title' : p.title, 'summary': p.summary, 'content': p.content, 'category': p.category}
        result.update({f'{p.id}': tmp})
    return jsonify(result), 200


@blog.route('/posts/<string:slug>', methods=['GET'])
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    result = {'slug': post.slug, 'title' : post.title, 'summary': post.summary, 'content': post.content, 'category': post.category}
    return jsonify(result), 200


@blog.route('/create_post', methods=['POST'])
def create_post():
    form = PostForm()
    if not form.validate_on_submit():
        return {'error': form.errors}, 400
    new_post = Post()
    new_post.title = form.title.data
    new_post.content = form.content.data
    new_post.slug = form.slug.data
    new_post.summary = form.summary.data
    new_post.category = form.category.data
    db.session.add(new_post)
    db.session.commit()
    return {'msg': 'Post created successfully'}, 201


@blog.route('/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return {}, 204