# views/answer_view.py
# create, modify, delete 메소드 포함


from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

# 'answer' 요청을 처리하는 blueprint 객체 bp
# 요청 뒤에 /answer 이 붙어있다면, 아래 블루프린트가 이를 받아 처리함.
bp = Blueprint('answer', __name__, url_prefix='/answer')


# 답변 생성 함수
# 사용자가 입력한 데이터를 담은 form 데이터를 받아서, DB INSERT 후 질문 상세 화면으로 이동

# 이 함수는, /create/question_id 형태의 요청을 POST 방식으로 처리
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    # AnswerForm 객체 생성
    form = AnswerForm()

    # 해당 질문에 대한 정보를 DB 에서 받아옴
    question = Question.query.get_or_404(question_id)

    # 입력받은 form 에 대해, 데이터 검증한 결과가 참(즉, 입력한 데이터가 모두 조건에 맞는 경우)
    if form.validate_on_submit():
        # request 객체의 form 속성(dictionary 로 추정) 에서, 'content' 의 value 를 content 변수에 저장
        content = request.form['content']

        # Answer 객체 생성. Answer 테이블에서 요구하는 데이터를 채움
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)

        # question 객체에 답변들에 answer 객체를 append, 이에 따라 question <-> answer_set 쌍방 참조 가능
        question.answer_set.append(answer)
        db.session.commit()

        # 질문 상세 화면의 url 을 리턴
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id)
        )

    # 입력받은 form 에 대해, 데이터 검증 결과가 참이 아닌 경우(즉, 입력한 데이터 중 조건에 맞지 않는 것이 하나 이상 있는 경우)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id)
            )
    else:
        form = AnswerForm(obj=answer)
    return render_template('question/answer_form.html', answer=answer, form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))