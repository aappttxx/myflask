import os
from urllib.parse import urljoin, urlparse

from flask import (Flask, abort, g, json, jsonify,
                   make_response, redirect, request, session, url_for)
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)

# app.secret_key = 'secret string'
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/')
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    name = request.args.get('name', 'Human')  # 获取查询参数name的值
    response = '<h1>Hello, %s!</h1>' % name
    if name is None:
        name = request.cookies.get('name', 'Human')
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2019 - year)


# colors = ['blue', 'white', 'red']
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))  # 重定向到/hello


@app.route('/404')
def not_found():
    abort(404)


# @app.route('/foo')
# def foo():
#     # data = {
#     #     'name': 'Grey Li',
#     #     'gender': 'male'
#     # }
#     # response = make_response(json.dumps(data))
#     # response.mimetype = 'text/plain'

#     # jsonify(name='Grey Li', gender='male')
#     return jsonify(message='Error!'), 500


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'


@app.before_request
def get_name():
    g.name = request.args.get('name')


@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return'''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_more():
    return generate_lorem_ipsum(n=1)
