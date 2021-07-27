# forms.py
# 사용자로부터 받은 입력 데이터를 처리할 때 사용한다.


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


# 질문 등록 form
class QuestionForm(FlaskForm):
    # 데이터 타입을 명시. '제목' 등으로 데이터 이름을 설정.
    # validators 를 통해 값 검증, 에러 발생 시 파라미터로 들어가있는 문자열을 리턴
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다. ')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다. ')])


# 답변 등록 form
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다')])


# 회원 가입 form
class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


# 회원 로그인 form
class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])