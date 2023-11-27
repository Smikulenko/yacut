from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная сcылка ',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )

    custom_id = StringField(
        'Вариант короткой сcылки',
        validators=[Length(1, 16), Optional()]

    )
    submit = SubmitField('Создать')
