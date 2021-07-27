# config/default.py
# 프로젝트의 루트 디렉터리리를 가지고 있는 파일

import os

# 프로젝트의 루트 디렉터리인 BASE_DIR 은 기존 config.py 파일에 있던 환경 변수.
# os.path.dirname() 이 2번 사용된 이유는, myproject -> config 폴더로 depth 가 증가했기 때문.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))