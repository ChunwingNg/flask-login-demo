import secrets

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_admin import Admin
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()

def create_app():
    app = Flask(__name__)

    # update config
    app.config.from_object('config.Config')

    with app.app_context():
        Bootstrap(app)
        
        db.init_app(app)
        
        login_manager.init_app(app)
        login_manager.login_view = 'login_bp.login'
        

        app.secret_key = secrets.token_urlsafe(256)

        from modules.login import routes as login_routes
        from modules.users import routes as user_routes

        app.register_blueprint(login_routes.login_bp)
        app.register_blueprint(user_routes.user_bp, url_prefix="/user")
        
        
        from modules.login.user import User

        from modules.admins.model import CustomModelView, CustomAdminIndexView
        admin.init_app(app, index_view=CustomAdminIndexView())
        admin.add_view(CustomModelView(User, db.session))
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.isAdmin:
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('user_bp.dashboard'))
        else:
            return render_template('index.html')

    @event.listens_for(User.passW, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return generate_password_hash(value, method='sha256')
        return value
    
    return app