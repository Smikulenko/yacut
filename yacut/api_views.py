from re import match

from http import HTTPStatus
from flask import jsonify, request

from yacut import app, db

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short

USER_URL_LENGHT = 16
PATTERN = '^[a-zA-Z0-9_]*$'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short()

    if len(data.get('custom_id')) > USER_URL_LENGHT:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if not match(PATTERN, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
