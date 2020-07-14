from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app import login_manager

user_bp = Blueprint('user_bp',__name__,static_folder='static', template_folder='templates')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.userN, isAdmin=current_user.isAdmin)