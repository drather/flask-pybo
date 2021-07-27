# views/main_views.py
# 사용자가 주소를 통해

from flask import Blueprint, url_for, current_app
from pybo.models import Question
from werkzeug.utils import redirect

# '/' 요청이 들어오면 아래 Blueprint 객체가 처리한다.
# '/' 요청이란, 3.36.9.91, 즉 pybo 홈페이지에 처음 접속하는 url 을 말한다.
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'hello, pybo!'


# question bp 의 _list 함수가 나타내는 url 로 이동한다.
@bp.route('/')
def index():
    current_app.logger.info("INFO 레벨로 출력")
    return redirect(url_for('question._list'))
