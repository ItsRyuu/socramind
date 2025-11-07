from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps
from app.models.models import db, User, UserProgress, ConversationLog, QuizAttempt
from ..learning.routes import curriculum 

admin = Blueprint('admin', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Anda tidak memiliki izin untuk mengakses halaman ini.", "error")
            return redirect(url_for('main.materi'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@admin.route('/user/<int:user_id>')
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)

    logs = ConversationLog.query.filter_by(user_id=user.id).order_by(ConversationLog.timestamp.desc()).all()
    quizzes = QuizAttempt.query.filter_by(user_id=user.id).order_by(QuizAttempt.timestamp.desc()).all()
    progress = UserProgress.query.filter_by(user_id=user.id).all()

    return render_template('admin_user_detail.html', 
                             user=user, 
                             logs=logs, 
                             quizzes=quizzes, 
                             progress=progress)