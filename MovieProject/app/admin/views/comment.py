from flask import render_template, session, url_for

from app import app, db
from app.admin import admin, flash, redirect
from app.models import Comment


@admin.route('/comment/list/')
@admin.route('/comment/list/<int:page>/')
def comment_list(page=1):
    commentsPageObj=Comment.query.paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('admin/comment/comment_list.html',commentsPageObj=commentsPageObj,app=app)
@admin.route('/comment/del/<int:id>/')
def comment_del(id):
    comment=Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功")
    return redirect(url_for('admin.comment_list'))