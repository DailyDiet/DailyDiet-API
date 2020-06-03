from flask import jsonify

from . import blog
from .models import Post


@blog.route('/', methods=['GET'])
def posts():
    posts = Post.query.all()
    result = dict()
    for p in posts:
        tmp = dict()
        tmp['id'] = p.id
        tmp = {'slug': p.slug, 'title' : p.title, 'summary': p.summary, 'content': p.content, 'category': p.category}
        result.update({f'{p.id}': tmp})
    return jsonify(result), 200


@blog.route('/<string:slug>')
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    result = {'slug': post.slug, 'title' : post.title, 'summary': post.summary, 'content': post.content, 'category': post.category}
    return jsonify(result), 200
