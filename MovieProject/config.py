import os

SQLALCHEMY_DATABASE_URI = "mysql://root:redhat@localhost/MovieProject"
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY='REDHAThello123,,,'

BASEDIR=os.path.abspath(os.path.dirname(__file__))
#用户头像
USER_FACE_DIR=os.path.join(BASEDIR,'app/static','upload/userFaceImg')
#预告封面
PREVIEW_LOGO_DIR=os.path.join(BASEDIR,'app/static','upload/previewLogoImg')
#电影文件
MOVIE_DIR=os.path.join(BASEDIR,'app/static','upload/movieFile')
#电影封面
MOVIE_LOGO_DIR=os.path.join(BASEDIR,'app/static','upload/movieLogoImg')


PER_PAGE=5