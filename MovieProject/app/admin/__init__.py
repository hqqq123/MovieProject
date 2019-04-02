from flask import Blueprint
admin=Blueprint("admin",__name__)
from app.admin.views.main import *
from app.admin.views.admin import *
from app.admin.views.auth import *
from app.admin.views.role import *
from app.admin.views.tag import *
from app.admin.views.preview import *
from app.admin.views.user import *
from app.admin.views.movie import *
from app.admin.views.comment import *
from app.admin.views.log import *