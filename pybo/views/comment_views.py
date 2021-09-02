# views/comment_views.py
# 질문과 답변 각각에 대한 댓글 등록, 수정, 삭재에 관한 view

from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Comment, Answer
from pybo.views.auth_views import login_required


# 이 bp는 /comment 요청을 처리함
bp = Blueprint('comment', __name__, url_prefix='/comment')


# GET, POST 방식의 요청을 나누어 처리
# 질문에 댓글을 생성하는 함수
@bp.route('/create/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def create_question(question_id):
    # 댓글 form 객체 생성
    form = CommentForm()

    # 인자로 받은 question_id 를 통해 question 데이터를 저장
    question = Question.query.get_or_404(question_id)

    # 요청 방식이 POST 방식이고, form 의 데이터가 조건을 만족하는 경우
    if request.method == 'POST' and form.validate_on_submit():
        # comment 생성. 이때, user 필드에는 g.user, 즉 컨텍스트 변수인 g 가 가지고 있는 user 의 값을 저장하면 된다.
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), question=question)

        # 저장
        db.session.add(comment)
        db.session.commit()

        # anchor 적용.
        # 이를 해석해보면, '/detail/질문번호#comment_코멘트번호' 의 url 을 리턴.
        return redirect('{}#comment_{}'.format(
            url_for('question.detail', question_id=question_id), comment.id))

    # GET 방식인 경우, 댓글 등록 화면으로 이동
    return render_template('comment/comment_form.html', form=form)


# 댓글 수정 함수
@bp.route('/modify/question/<int:comment_id>', methods=['POST'])
@login_required
def modify_question(comment_id):
    # comment_id 를 key 로써 comment 를 가져옴
    comment = Comment.query.get_or_404(comment_id)

    # 컨텍스트 변수 g가 가진 user 와 comment.user 가 다른 경우, 질문 상세 화면으로 redirect
    if g.user != comment.user:
        flash('수정 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.question.id))

    # 요청 방식이 POST 인 경우
    if request.method == 'POST':
        # commentForm 객체 생성
        form = CommentForm()

        # 입력 데이터가 조건에 맞는 경우
        if form.validate_on_submit():
            # comment 를 객체화?
            form.populate_obj(comment)

            # comment 의 수정 일자를 현재 시각으로 update
            comment.modify_date = datetime.now()

            # 저장
            db.session.commit()

            # 질문 상세 화면의 해당 댓글로 설정된 anchor 로 리턴
            return redirect(
                '{}#comment_{}'.format(url_for('question.detail', question_id=comment.question.id), comment_id)
            )
    # 요청 방식이 GET 방식인 경우
    else:
        # form 에 comment 객체를 저장
        form = CommentForm(obj=comment)

    # 댓글 입력 화면으로 이동
    return render_template('comment/comment_form.html', form=form)


# 댓글 삭제 함수
@bp.route('/delete/question/<int:comment_id>')
@login_required
def delete_question(comment_id):
    # comment_id 를 바탕으로, 해당 comment 를 불러옴
    comment = Comment.query.get_or_404(comment_id)

    # question_id 에 comment 데이터가 참조하는 question 데이터의 id 값을 저장
    question_id = comment.question.id

    # 컨텍스트 변수 g 의 user 데이터와 현재 작성 user 데이터가 다른 경우
    if g.user != comment.user:
        flash('삭제 권한이 없습니다')
        # 질문 상세 화면으로 이동
        return redirect(url_for('question.detail', question_id=question_id))

    # 저장
    db.session.delete(comment)
    db.session.commit()

    # 질문 상세 화면으로 이동
    return redirect(url_for('question.detail', question_id=question_id))


# 답변 댓글 등록 함수
@bp.route('/create/answer/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id):
    # 댓글 등록 form 객체 생성
    form = CommentForm()

    # answer_id 를 바탕으로 answer 객체를 불러옴
    answer = Answer.query.get_or_404(answer_id)

    # 요청 방식이 POST 이고 입력 데이터가 조건을 만족한다면
    if request.method == 'POST' and form.validate_on_submit():
        # comment 객체 생성
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), answer=answer)

        # 저장
        db.session.add(comment)
        db.session.commit()

        # anchor 기능 적용된 질문상세 화면 url 을 리턴
        return redirect('{}#comment_{}'.format(
            url_for('question.detail', question_id=answer.question.id), comment.id))

    # 댓글 등록 화면으로 이동
    return render_template('comment/comment_form.html', form=form)


# 답변 댓글 수정 함수
@bp.route('/modify/answer/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    # comment_id 를 바탕으로 comment 객체를 불러옴
    comment = Comment.query.get_or_404(comment_id)

    # 컨텍스트 변수의 user 데이터와 댓글 작성 user 데이터의 값이 다른 경우
    if g.user != comment.user:
        flash('수정 권한이 없습니다')

        # 질문 상세 화면으로 이동
        return redirect(url_for('question.detail', question_id=comment.answer.id))

    # 요청 메소드가 POST 인 경우
    if request.method == 'POST':
        # form 객체 생성
        form = CommentForm()

        # form 데이터가 조건을 만족하는 경우
        if form.validate_on_submit():
            # comment 를 객체화?
            form.populate_obj(comment)

            # comment 수정일자 update
            comment.modify_date = datetime.now()

            # 저장
            db.session.commit()

            # anchor 적용된 질문 상세 화면으로 이동
            return redirect('{}#comment_{}'.format(
                url_for('question.detail', question_id=comment.answer.question.id), comment.id))

    # 요청 방식이 GET 인 경우
    else:
        # form 변수에 comment 를 객체화
        form = CommentForm(obj=comment)

    # 댓글 등록 화면으로 이동
    return render_template('comment/comment_form.html', form=form)


# 답변 댓글 삭제 함수
@bp.route('/delete/answer/<int:comment_id>')
@login_required
def delete_answer(comment_id):
    # comment_id 를 바탕으로 댓글 데이터 가져옴
    comment = Comment.query.get_or_404(comment_id)

    # question_id 변수에 comment 데이터가 참조하는 answer 데이터가 참조하는 question 데이터의 id 를 가져옴
    question_id = comment.answer.question.id

    # 컨텍스트 변수 g 의 user 데이터와 comment 작성 user 의 데이터가 다른 경우
    if g.user != comment.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    # 해당 comment 삭제
    db.session.delete(comment)
    db.session.commit()

    # 질문 상세 화면으로 이동
    return redirect(url_for('question.detail', question_id=question_id))

