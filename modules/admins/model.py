
from flask import url_for, redirect, flash
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

# Setup for db view
class CustomModelView(ModelView):
    action_disallowed_list = ['delete']
    
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.isAdmin
            
    def inaccessible_callback(self, name, **kwargs):
        flash('Please log in as an admin')
        return redirect(url_for('login_bp.login'))

# Setup for admin view
class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.isAdmin
            
    def inaccessible_callback(self, name, **kwargs):
        flash('Please log in as an admin')
        return redirect(url_for('login_bp.login'))