# filter.py
# 필터, 즉 데이터를 원하는 형태로 출력해야 하는 일이 잦을 때, 함수로 만들어서 사용한다.

# datetime 을 fmt 의 형태로 바꿔서 출력할수 있게끔 하는 함수.
#     app.jinja_env.filters['datetime'] = format_datetime
# 위의 형태로, app.jinja_env.filters 에 datetime 이라고 정의한 뒤, 사용한다.
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)