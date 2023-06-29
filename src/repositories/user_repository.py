from sqlalchemy import text
from werkzeug.security import generate_password_hash
from db import db


class UserRepository:
    def __init__(self, db_) -> None:
        self._db = db_

    def find_user(self, username: str):
        """Search for a speciic based on their username.

        Args:
            username (str): user's username.

        Returns:
            sqlalchemy result object: contains the user's details.
        """
        sql = text(
            "SELECT id, username, password, role_id FROM users WHERE username=:username"
        )
        return self._db.session.execute(sql, {"username": username}).fetchone()

    def get_permission_level(self, role_id: int):
        """Get permission_level from the roles table based on a role_id."""
        sql = text("SELECT permission_level FROM roles WHERE id=:role_id")
        return self._db.session.execute(sql, {"role_id": role_id}).fetchone()[0]

    def get_user_roles(self):
        """Get available role details."""
        return self._db.session.execute(
            text(
                """
        SELECT id, name, permission_level,
        work_cost_modifier FROM roles;"""
            )
        ).fetchall()

    def create_credentials(self, username, password, role_id):
        """Add new credentials to the user repository."""
        if self.find_user(username) is not None:
            return False
        pw_hash = generate_password_hash(password)
        sql = text(
            """INSERT INTO users (username,password,role_id)
                    VALUES (:username, :password, :role_id)"""
        )
        self._db.session.execute(
            sql, {"username": username, "password": pw_hash, "role_id": role_id}
        )
        self._db.session.commit()
        return True

    def get_users(self, user_role_level):
        """Get users below a specific permission level."""
        sql = text(
            """SELECT users.id as user_id, username
                    FROM users LEFT JOIN roles ON users.role_id = roles.id
                    WHERE permission_level <= :user_level GROUP BY users.id, roles.id;"""
        )
        return self._db.session.execute(sql, {"user_level": user_role_level}).fetchall()


user_repository = UserRepository(db)
