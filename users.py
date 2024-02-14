from db.db_actions import *

class Users:
    def __init__(self):
        self._user_map = {}
        self._user_uid = ""
        self._user_first_name = ""
        self._user_last_name = ""
        self._user_token = ""
        self._user_valid_token = False
        self._user_friend_posts_offset = 0
        self._user_friend_posts_limit = 5

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
        self._user_first_name = new_user_map['first_name']
        self._user_last_name = new_user_map['last_name']

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

    # Token
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

    # Find user by name
    @property
    def user_first_name(self):
        return self._user_first_name

    @user_first_name.setter
    def user_first_name(self, user_first_name):
        self._user_first_name = user_first_name

    @property
    def user_last_name(self):
        return self._user_last_name

    @user_last_name.setter
    def user_last_name(self, user_last_name):
        self._user_last_name = user_last_name

    @property
    def user_find(self):
        get_user = db_finder(self._user_first_name, self._user_last_name)
        return get_user

    # Get posts of friends
    @property
    def user_friend_posts(self):
        friend_posts = db_get_posts_redis(self._user_friend_posts_offset, self._user_friend_posts_limit)
        return friend_posts

    @user_friend_posts.setter
    def user_friend_posts(self, page):
        self._user_friend_posts_offset = page[0]
        self._user_friend_posts_limit = page[1]
