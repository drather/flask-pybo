# config/production.py
# 운영 환경에서 사용할 환경 변수를 정의한 파일

from config.default import *
from logging.config import dictConfig

# 운영 환경(AWS)에서 사용할 데이터 베이스 주소
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{uri}/{db}'.format(
#     user='dbmasteruser',
#     pw='Y2KqfJ{5m7r1uf%Ng7P*:O{s$-zab~2R',
#     uri='ls-45f3d185c617157c0f19e01e0ad95a86a721ca12.cizc7qh0aggx.ap-northeast-2.rds.amazonaws.com',
#     db='flask_pybo'
# )

# 운영 환경(daehyun)에서 사용할 데이터 베이스 주소
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///{user}:{pw}@{uri}/{db}'.format(
    user='dbmasteruser',
    pw='qwer!234',
    uri='localhost:5432',
    db='flask_pybo'
)

# SQLAlchemy 에서 이벤트 발생을 처리하는 기능. False 로 비활성화
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 운영 환경이므로, SECRET_KEY 를 복잡하게 설정.
SECRET_KEY = b'z\xa7\x88Ij\xeef\xd0\xf4\xb73\xc2z?4\xa1'

# 로그 config 설정
# formatter: 로그에 출력할 형식을 정의. asctime, levelname, module, message 를 출력하기로 결정
# handlers: 로그를 출력하는 방법을 결정. file 이라는 핸들러를 등록.
#   level: 심각도
#   class: 로그 핸들러 클래스. RoatatingFilerHandler 는 파일 개수를 일정하게 유지.
#   filename: 로그 파일 명
#   maxByte: 로그 파일 최대 크기
#   backUpCount: 로그파일 갯수. 로그 파일을 5개로 유지
#   formatter: 포맷터, default 설정

# root: 최상위 로거.
#   level: 로그 레벨 설정
#   handler: 로그 핸들러, 위에서 설정한 file로 설정

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/myproject.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
