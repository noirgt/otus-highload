from db.db_actions import db_setter, db_getter, db_deleter, db_token, db_check_token

class Users:
    def __init__(self):
        self._user_map = {}
        self._user_uid = ""
        self._user_token = ""
        self._user_valid_token = False

    @property
    def user_map(self):
        try:
            get_user = db_getter(self._user_uid)[0]
            self._user_map['first_name'] = get_user[1]
            self._user_map['last_name'] = get_user[2]
            self._user_map['city'] = get_user[3]
            self._user_map['sex'] = get_user[4]
            self._user_map['age'] = get_user[5]
            self._user_map['hobbie'] = get_user[6]
            self._user_map['uid'] = get_user[0]
        except IndexError:
            self._user_map = {}
        return self._user_map

    @user_map.setter
    def user_map(self, new_user_map):
        uid = db_setter(
                new_user_map['first_name'],
                new_user_map['last_name'],
                new_user_map['city'],
                new_user_map['sex'],
                new_user_map['age'],
                new_user_map['hobbie'],
                new_user_map['password'],
                new_user_map['token']
            )
        new_user_map['uid'] = uid
        self._user_map = new_user_map
        self._user_uid = uid

    @property
    def user_uid(self):
        return self._user_uid 

    @user_uid.setter
    def user_uid(self, user_uid):
        self._user_uid = user_uid

    @user_uid.deleter
    def user_uid(self):
        db_deleter(self._user_uid)
        self._user_uid = ""

    @property
    def user_token(self):
        return self._user_token

    @user_token.setter
    def user_token(self, user_password):
        self._user_token = db_token(self._user_uid, user_password)
        return self._user_token

    @property
    def user_valid_token(self):
        return self._user_valid_token

    @user_valid_token.setter
    def user_valid_token(self, user_token):
        self._user_valid_token = db_check_token(user_token)
