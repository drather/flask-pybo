from flask import Blueprint, url_for
from pybo.models import Question
from werkzeug.utils import redirect


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'hello, pybo!'


@bp.route('/')
def index():
    3 / 0 # 강제로 오류 발생
    return redirect(url_for('question._list'))
