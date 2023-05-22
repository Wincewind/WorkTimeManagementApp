from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from repositories.user_repository import user_repository

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

user_service = UserService()
