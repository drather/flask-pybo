# views/auth_views.py
# 회원가입, 로그인, 로그아웃, 로그인 되어있는 유저 확인, 로그인 여부 검사 함수를 포함.

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

# /auth 로 시작하는 요청은 아래 bp 가 처리한다.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 회원가입 함수
# /auth/signup 요청을 처리한다.
# GET 요청(회원 가입화면을 이동)과 POST 요청(입력 정보 DB INSERT)을 나눠서 처리한다.
@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    # 회원 정보 form 생성
    form = UserCreateForm()

    # 요청 방식이 POST 이고(= 회원 정보 저장), 입력 데이터가 모두 조건을 만족하는 경우
    if request.method == 'POST' and form.validate_on_submit():
        # 입력받은 form 의 username 을 가져와서, user 정보에 저장
        user = User.query.filter_by(username=form.username.data).first()

        # user 정보가 없다면, 즉 같은 이름의 데이터가 없다면
        if not user:
            # user 객체 생성. password 는 generate_password_hash 함수를 통해 암호화
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)

            # db 저장
            db.session.add(user)
            db.session.commit()

            # main 화면을 return
            return redirect(url_for('main.index'))

        # 같은 이름을 가진 사용자가 있다면
        else:
            flash('이미 존재하는 사용자입니다')

    # 요청 방식이 GET 이라면, 회원가입 화면으로 이동
    return render_template('auth/signup.html', form=form)


# auth/login 요청을 처리하는 함수
# 마찬가지로, GET 방식의 요청(login 화면으로 이동), POST(입력 데이터를 기반으로 로그인)
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    # 로그인 form 생성
    form = UserLoginForm()

    # 요청이 POST 방식이고, 입력 데이터가 모두 조건에 맞는 경우
    if request.method == 'POST' and form.validate_on_submit():
        error = None

        # 입력한 데이터를 갖는 회원 정보와 일치하는 데이터 불러옴
        user = User.query.filter_by(username=form.username.data).first()

        # 일치하는 데이터가 없다면, error 변수에 저장
        if not user:
            error = "존재하지 않는 사용자입니다"

        # 입력한 데이터를 암호화한 결과가 db에 저장된 내용과 다르다면
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."

        # error 변수에 아무런 값도 저장되어 있지 않다면
        if error is None:
            # session 클리어
            session.clear()

            # session 의 user_id 값을 id 값으로 저장
            session['user_id'] = user.id

            # main.index 가 가리키는 화면으로 이동
            return redirect(url_for('main.index'))

        # 에러 메시지를 화면에 출력
        flash(error)

    # 요청 방식이 GET 방식이라면, 로그인 화면으로 이동.
    return render_template('auth/login.html', form=form)


# before_app_request 어노테이션으로 인해, 라우팅 하는 함수보다 먼저 실행됨
# 즉, load_logged_in_user 함수는 모든 라우트 함수보다 먼저 실행된다.
@bp.before_app_request
def load_logged_in_user():
    # session 으로부터 user_id 를 받아온다.
    user_id = session.get('user_id')

    # session 객체가 가진 user_id 가 None 이라면
    if user_id is None:
        # g 객체의 user 를 None 으로 한다.
        g.user = None
    # session 객체가 가진 user_id 가 있다면
    else:
        # session 객체의 user_id 를 바탕으로 user 를 db 에서 로드한 뒤, g.user 에 저장한다.
        g.user = User.query.get(user_id)

# 로그아웃 관련 함수
@bp.route('/logout/')
def logout():
    # session 을 클리어한다.
    session.clear()

    # main bp 의 index 메소드가 리턴하는 url 을 리턴한다.
    return redirect(url_for('main.index'))


# 로그인이 필요한 기능들에 앞서 실행되는 메소드
# 이해 잘 안됨.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

