from secrets import token_hex
from datetime import datetime
from flask import session, abort, flash
from werkzeug.security import check_password_hash
from repositories.user_repository import user_repository


class UserService:
    """Service for handling interaction with the user repository."""

    def __init__(self) -> None:
        self.repository = user_repository
        self._roles = None

    def login(self, username: str, password: str) -> bool:
        """Check if user exists in repository and the given password matches.

        User's user_level, user_id, username, csrf_token and
        a chosen_date are stored in the flask session data.

        Args:
            username (str): username to find in repository.
            password (str): password to match if a result is found.

        Returns:
            bool: True if login was successful, else False.
        """
        user = self.repository.find_user(username)
        if not user:
            return False
        if not check_password_hash(user.password, password):
            return False
        session["user_level"] = user_repository.get_permission_level(user.role_id)
        session["user_id"] = user.id
        session["username"] = user.username
        session["csrf_token"] = token_hex(16)
        session["chosen_date"] = datetime.now()
        return True

    def logout(self):
        """User is logged out by removing the
        user details from the session object."""
        del session["user_id"]
        del session["username"]
        del session["user_level"]
        del session["chosen_date"]

    def _get_user_roles(self):
        """Get available roles from the user repository."""
        return self.repository.get_user_roles()

    def create_credentials(
        self,
        username: str,
        password: str,
        role_id: int,
        min_un_len: int,
        min_pw_len: int,
    ) -> bool:
        """Confirm validity of given username and password and attempt
        to create new user in repository. If the creation was successful, login is also performed.

        Args:
            username (str): new username.
            password (str): new user's password.
            role_id (int): role id of the user, affects permissions.
            min_un_len (int): min length of the username.
            min_pw_len (int): min length of the password.

        Returns:
            bool: True if the user creation was a success, else False.
        """
        if len(username) < min_un_len or len(password) < min_pw_len:
            flash(
                f"Username needs to be atleast {min_un_len} characters long"
                f"and password {min_pw_len} characters."
            )
            return False
        if self.repository.create_credentials(username, password, role_id):
            self.login(username, password)
            flash("New credentials created.")
            return True
        flash("Username is already in use.")
        return False

    @property
    def roles(self):
        """Property for the static user roles. If not yet assigned,
        they'll be fetched from the user repository."""
        if not self._roles:
            self._roles = self._get_user_roles()
        return self._roles

    def check_user_role_level(self, level: int):
        """Check if session's user_level exceeds the given
        level at which point 403 HTTPException is raised."""
        if level < session.get("user_level", float("inf")):
            abort(403)

    def check_csrf(self, token):
        """Compare the given token to session's csrf_token
        and if they don't match, 403 HTTPException is raised."""
        if session["csrf_token"] != token:
            abort(403)

    def get_users(self, level=float("inf")):
        """Get users of a specific level. If no level is provided, all users are fetched."""
        return self.repository.get_users(level)


user_service = UserService()
