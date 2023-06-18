from db import db
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

class UserRepository:
    def __init__(self, db) -> None:
        self._db = db

    def find_user(self, username):
        # try:
        sql = text('SELECT id, username, password, role_id FROM users WHERE username=:username')
        return self._db.session.execute(sql, {"username":username}).fetchone()
        #return result
        # except:
        #     if not result:
        #         return None
        #     return result

    def get_permission_level(self, role_id):
        sql = text('SELECT permission_level FROM roles WHERE id=:role_id')
        return self._db.session.execute(sql, {"role_id":role_id}).fetchone()[0]

    def get_user_roles(self):
        return self._db.session.execute(text('SELECT * FROM roles;')).fetchall()
    
    def create_credentials(self,username,password,role_id):
        if self.find_user(username) is not None:
            return False
        pw_hash = generate_password_hash(password)
        sql = text("""INSERT INTO users (username,password,role_id)
                    VALUES (:username, :password, :role_id)""")
        self._db.session.execute(sql, {"username":username,
                                       "password":pw_hash,
                                       "role_id":role_id})
        self._db.session.commit()
        return True
    
    def get_users(self, user_role_level):
        sql = text("""SELECT users.id as user_id, username
                    FROM users LEFT JOIN roles ON users.role_id = roles.id
                    WHERE permission_level <= :user_level GROUP BY users.id, roles.id;""")
        return  self._db.session.execute(sql,{"user_level":user_role_level}).fetchall()

    # session['user_id'] = result.id
    # session['permission_level'] =_get_permission_level(result.role_id)
    # for session_data in ['username','']
    #     session['username'] = username
    #     session['']

user_repository = UserRepository(db)
