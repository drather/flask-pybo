# config/development.py
# 이 파일은, 개발 환경에서 사용하는 환경 변수를 정의한 파일.

from config.default import *

# from config.default import * 는 default 에 있는 모든 것을 import 하겠다는 뜻.

# SQLALCHEMY_DATABASE_URI: 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

# SQLALCHEMY_TRACK_MODIFICATIONS: SQLAlchemy 의 이벤트를 처리하는 옵션. 필요하지 않으므로 False 로 비활성화.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY: 플라스크가 어떤 값을 암호화할 때 사용하는 중요한 환경 변수.
# 개발 환경에서는 이런 간단한 값을 써도 되지만,
# 운영 환경에서는 이렇게 쓰면 안됨. b'Zb3\x81\xdb\xf1\xd9\xd7-Knb\x8eB\xa5\x18' 이러한 값을 써야 함.
SECRET_KEY = "dev"