from flask import session, abort
from werkzeug.security import check_password_hash
from repositories.user_repository import user_repository
from secrets import token_hex

class UserService:
    def __init__(self) -> None:
        self.repository = user_repository
        self._roles = None

    def login(self, username, password):
        user = self.repository.find_user(username)
        if not user:
            return False
        if not check_password_hash(user.password,password):
            return False
        session['user_level'] = user_repository.get_permission_level(user.role_id)
        session['user_id'] = user.id
        session['username'] = user.username
        session["csrf_token"] = token_hex(16)

        return True
    
    def _get_user_roles(self):
        return self.repository.get_user_roles()
    
    def create_credentials(self,username,password,role_id):
        return self.repository.create_credentials(username,password,role_id)
    
    @property
    def roles(self):
        if not self._roles:
            self._roles = self._get_user_roles()
        return self._roles

    def check_user_role_level(self, level):
        if level < session.get("user_level", float('inf')):
            abort(403)

    def check_csrf(self, token):
        if session["csrf_token"] != token:
            abort(403)
user_service = UserService()
