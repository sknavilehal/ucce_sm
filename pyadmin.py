from pymongo import MongoClient
from bson.objectid import ObjectId
from wtforms import form, fields, validators
from flask import redirect, url_for, request
from flask_admin.form import Select2Widget
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.contrib.pymongo import ModelView, filters
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin

client = MongoClient("mongodb://localhost:27017")
db = client["UCCE_Global"]

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User(db.users.find_one({"_id": ObjectId(user_id), "role":"admin"}))

class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json
    
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

# User admin
class UserForm(form.Form):
    login = fields.StringField('Login')
    password = fields.StringField('Password')
    role = fields.SelectField('Role', choices=[('admin', 'Admin'), ('user','User')])

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ('login', 'password', 'role')
    column_sortable_list = ('login', 'password', 'role')

    form = UserForm

class SignatureForm(form.Form):
    user = fields.SelectField('User', choices=[('UCCE_Admin', 'UCCE_Admin')])
    filter = fields.StringField('Filter')
    description = fields.StringField('Description')
    category = fields.SelectField('Category', choices=[('system', 'System'), ('feature', 'Feature')])
    #checkpoint = fields.SelectField('Checkpoint', choices=[('error', 'Error'), ('warning', 'Warning'), ('info', 'Info')])
    checkpoint = fields.StringField('Checkpoint')
    published = fields.BooleanField('Published', default=True)

class SignatureView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ('user','filter', 'description', 'category','checkpoint', 'published')
    column_sortable_list = ('user','filter', 'description', 'category','checkpoint', 'published')
    column_searchable_list = ('user','filter', 'description', 'category','checkpoint', 'published')

    form = SignatureForm

class EventForm(form.Form):
    datetime = fields.StringField('DateTime')
    username = fields.StringField('Username')
    category = fields.StringField('Category')
    action = fields.StringField('Action')

class EventView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ('datetime', 'username', 'category', 'action', 'param1', 'param2')
    column_sortable_list = ('datetime', 'username', 'category', 'action', 'param1', 'param2')

    form = EventForm

class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user.user_json is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if user.user_json["password"] != self.password.data:
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User(db.users.find_one({"login":self.login.data, "role": "admin"}))

class DashboardView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return True

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login_view'))
        return self.render('admin/index.html')
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)
            print(user.is_authenticated)

        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        self._template_args['form'] = form
        return self.render('admin/index.html')
    
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('admin.index'))

if not db.users.find_one({"login":"admin"},{"_id":1}):
    db.users.insert_one({"login":"admin", "password":"admin", "role":"admin"})

# Add administrative views here
admin = Admin(name='UCCE Admin Site', index_view=DashboardView(), base_template='my_master.html')
admin.add_view(UserView(db.users, 'User'))
admin.add_view(SignatureView(db.signatures, 'Signature'))
admin.add_view(EventView(db.event_log, 'Event Log'))