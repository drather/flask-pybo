from config.default import *
from logging.config import dictConfig

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='dbmasteruser',
    pw='Y2KqfJ{5m7r1uf%Ng7P*:O{s$-zab~2R',
    uri='ls-45f3d185c617157c0f19e01e0ad95a86a721ca12.cizc7qh0aggx.ap-northeast-2.rds.amazonaws.com',
    db='flask_pybo'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'z\xa7\x88Ij\xeef\xd0\xf4\xb73\xc2z?4\xa1'

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