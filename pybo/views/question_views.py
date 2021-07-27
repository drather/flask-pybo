# views/question_views.py
# _nullast, _list, detail, create, modify, delete 메소드 포함

from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash, current_app
from werkzeug.utils import redirect
from sqlalchemy import func, nullslast

from pybo import db

from pybo.forms import QuestionForm, AnswerForm

from pybo.models import Question, question_voter, Answer, User

from pybo.views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')


# sqlite DB 에 대한 처리.
def _nullslast(obj):
    if current_app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        return obj
    else:
        return nullslast(obj)


# /question/list 요청을 처리하는 함수
@bp.route('/list/')
def _list():
    # paging
    page = request.args.get('page', type=int, default=1)

    # request 객체에 담긴 검색 키워드
    kw = request.args.get('kw', type=str, default='')

    # request 객체에 담긴 정렬 기준
    so = request.args.get('so', type=str, default='recent')

    # 추천 순 정렬인 경우
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter'))\
            .group_by(question_voter.c.question_id).subquery()

        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(_nullslast(sub_query.c.num_voter.desc()), Question.create_date.desc())

    # 인기 순 정렬인 경우
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()

        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(_nullslast(sub_query.c.num_answer.desc()), Question.create_date.desc())

    # 그 이외 경우
    else:
        question_list = Question.query.order_by(Question.create_date.desc())

    # 검색 키워드가 있는 경우
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()

        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()

    question_list = question_list.paginate(page, per_page=10)

    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)


# 질문 상세 조회 화면
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


# 질문 생성 화면
# GET 요청(질문 등록 화면으로 이동)과 POST 요청(질문 데이터 db 저장)을 나눠서 처리
@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()

    # 요청방식 POST && form 데이터 조건 만족하는 경우
    if request.method == 'POST' and form.validate_on_submit():
        # DB 저장
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)


# 질문 수정 함수
# GET 요청(수정 화면으로 이동)과 POST 요청(수정 내역 저장)을 따로 처리
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    # 컨텍스트 변수 g 에 담긴 user 데이터와 질문 작성자 data 가 다른 경우
    if g.user != question.user:
        flash('수정 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    # 질문 수정하고 저장하기 버튼 누른 경우 -> post 방식 요청
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            # form 을 객체화
            form.populate_obj(question)

            # 수정일자 update
            question.modify_date = datetime.now()

            # commit
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))

    # 질문 수정 버튼을 누르는 경우 -> get 방식의 요청
    else:
        form = QuestionForm(obj=question)
        return render_template('question/question_form.html', form=form)


# 질문 삭제 함수
@bp.route('/delete/int:<question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('question._list'))


