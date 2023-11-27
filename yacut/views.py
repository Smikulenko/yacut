from random import choices
from string import ascii_letters, digits

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short():
    while True:
        short_id = ''.join(choices(ascii_letters + digits, k=6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_name = form.custom_id.data
        if not short_name:
            short_name = get_unique_short()
        if URLMap.query.filter_by(short=short_name).first():
            flash('Предложенный вариант короткой ссылки уже существует.', "error")
            return render_template('yacut.html', form=form)
        unique_short_id = URLMap(original=form.original_link.data, short=short_name)
        db.session.add(unique_short_id)
        db.session.commit()
        full_link = url_for('index_view', _external=True) + short_name
        return render_template('yacut.html', form=form, short=full_link)
    return render_template('yacut.html', form=form,)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original)