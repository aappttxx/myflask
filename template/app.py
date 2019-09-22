from flask import Flask, render_template, Markup, flash, redirect, url_for
user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]

app = Flask(__name__)
app.secret_key = 'secret string'
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


# @app.context_processor
# def inject_foo():
#     foo = "baz"
#     return dict(foo=foo)


@app.template_global()
def bar():
    return "I'm bar."


@app.template_filter()
def musical(s):
    return s + Markup('&#9835')


@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


foo = 'foo'
app.jinja_env.globals['foo'] = foo


@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('watchlist'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
