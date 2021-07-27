# __init__.py
# create_app() 메소드를 통해서, application factory 방식으로 구현

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


# page not found 에러 (404) 발생 시, 404.html 을 보여주는 화면
def page_not_found(e):
    return render_template('404.html'), 404


# 만들어진 app 을 리턴하는 함수.
def create_app():
    # app: Flask app
    app = Flask(__name__)

    # APP_CONFIG_FILE 에서 환경일 가져옴.
    # APP_CONFIG_FILE 은 운영환경의 경우 production.py 를 불러옴
    # 개발 환경의 경우 development.py 를 불러옴
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM 설정.
    db.init_app(app)

    # sqlite 한정 설정
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트 설정
    # 핵심 기능들을 큰 단위로 쪼개놓은 것이 blueprint
    # blueprint 내에서, 서비스 단위로 처리한다.
    # url-prefix 를 통해 요청에 대한 blueprint 를 맵핑시킨다.

    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app