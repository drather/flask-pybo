# views/vote_views.py
# 추천 관련 함수인 question, answer 함수를 가짐

from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

# /vote url 을 처리하는 bp
bp = Blueprint('vote', __name__, url_prefix='/vote')


# /vote/question/q_id 를 처리하는 함수
@bp.route('/question/<int:question_id>/')
@login_required
def question(question_id):
    # question id 를 통해 해당 질문 데이터를 가져온다.
    _question = Question.query.get_or_404(question_id)

    # 컨텍스트 변수 g 의 user 데이터와 질문 작성자 데이터가 같은 경우, 추천 불가
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다')

    # 해당 질문 객체의 voter 에 현재 사용자 데이터를 추가
    else:
        _question.voter.append(g.user)
        db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))


# vote/answer/answer_id url 을 처리하는 함수
@bp.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    # answer_id 를 통해 답변 데이터를 가져옴
    _answer = Answer.query.get_or_404(answer_id)

    # 현재 사용자와 작성자가 같다면 추천 불가
    if g.user == _answer.user:
        flash('본인이 작성한 답변은 추천할 수 없습니다')

    # 아닌 경우
    else:
        # 해당 답변 데이터의 voter 에 현재 사용자 추가
        _answer.voter.append(g.user)

        # 저장
        db.session.commit()

    return redirect(url_for('question.detail', question_id=_answer.question.id))