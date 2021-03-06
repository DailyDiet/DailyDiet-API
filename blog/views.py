from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from extentions import db

from . import blog
from .forms import PostForm
from .models import Post
from users.models import User


@blog.route('/', methods=['GET'])
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    result = dict()
    for p in posts:
        tmp = dict()
        tmp['id'] = p.id
        slug = p.slug.replace(' ', '-')
        print(p.writer.FullName)
        tmp = {'slug': slug, 'title': p.title, 'summary': p.summary, 'content': p.content, 'category': p.category, 'author_fullname': p.writer.FullName, 'author_email': p.writer.Email}
        result.update({f'{p.id}': tmp})
    return jsonify(result), 200


@blog.route('/<string:slug>', methods=['GET'])
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if not post:
        return {'error': 'post not exist!'}, 404
    result = {'post_id':post.id, 'slug': post.slug, 'title': post.title, 'summary': post.summary, 'content': post.content, 'category': post.category, 'author_fullname': post.writer.FullName, 'author_email': post.writer.Email}
    return jsonify(result), 200


@blog.route('/posts/user', methods=['GET'])
@jwt_required
def get_user_posts():
    ID = User.query.filter_by(Email=get_jwt_identity()).first().id
    posts = Post.query.filter(Post.authorId == ID).all()
    result = dict()
    for p in posts:
        tmp = dict()
        tmp['id'] = p.id
        slug = p.slug.replace(' ', '-')
        print(p.writer.FullName)
        tmp = {'slug': slug, 'title': p.title, 'summary': p.summary, 'content': p.content, 'category': p.category, 'author_fullname': p.writer.FullName, 'author_email': p.writer.Email, 'current_user_mail': get_jwt_identity()}
        result.update({f'{p.id}': tmp})
    return jsonify(result), 200


@blog.route('/posts/new/', methods=['POST'])
@jwt_required
def create_post():
    ID = User.query.filter_by(Email=get_jwt_identity()).first().id
    form = PostForm()
    if not form.validate_on_submit():
        return {'error': form.errors}, 400
    new_post = Post()
    new_post.title = form.title.data
    new_post.content = form.content.data
    new_post.slug = form.slug.data
    new_post.summary = form.summary.data
    new_post.category = form.category.data
    new_post.authorId = ID
    db.session.add(new_post)
    db.session.commit()
    return {'msg': 'Post created successfully'}, 201


@blog.route('/posts/delete/<int:post_id>/', methods=['DELETE'])
@jwt_required
def delete_post(post_id):
    ID = User.query.filter_by(Email=get_jwt_identity()).first().id
    if not ID == Post.query.get(post_id).authorId:
        return {'error': 'access denied!'}, 403
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return {}, 204



# @blog.route('/posts/modify/<int:post_id>/', methods=['PATCH'])
# def modify_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = PostForm()
#     if not form.validate_on_submit():
#         return {'error': form.errors}, 400
#         new_post.title = form.title.data
#     post.content = form.content.data
#     post.slug = form.slug.data
#     post.summary = form.summary.data
#     post.category = form.category.data
#     db.session.commit()
#     return {'msg': 'Post Modified!'}, 201
