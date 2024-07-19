from db.db_actions import *

class Users:
    def __init__(self):
        self._user_my_uid = ""
        self._user_my_token = ""
        self._user_my_posts = ""
        self._user_my_posts_id = None
        self._user_my_friends = None
        self._user_my_del_friends = None

        self._user_map = {}
        self._user_uid = ""
        self._user_first_name = ""
        self._user_last_name = ""
        self._user_valid_token = False
        self._user_friend_posts_offset = 0
        self._user_friend_posts_limit = 5
        self._user_dialogs = []

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

    @property
    def user_my_uid(self):
        self._user_my_uid = db_get_my_user_id(self._user_my_token)
        if not self._user_my_uid:
            self._user_my_uid = "0"
        return self._user_my_uid

    # Token
    @property
    def user_token(self):
        return self._user_token

    @user_token.setter
    def user_token(self, user_password):
        self._user_token = db_token(self._user_uid, user_password)
        return self._user_token

    @property
    def user_my_token(self):
        return self._user_my_token

    @user_my_token.setter
    def user_my_token(self, user_my_token):
        self._user_my_token = user_my_token
        return self._user_my_token

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

    # Action for user dialogs
    @property
    def user_dialogs(self):
        return db_get_dialogs(self._user_uid)

    @user_dialogs.setter
    def user_dialogs(self, text):
        db_set_dialogs(self._user_uid, text)

    # Action for my posts
    @property
    def user_my_posts(self):
        if not self._user_my_posts_id:
            return self._user_my_posts

        return db_get_posts(self._user_my_posts_id)

    @user_my_posts.setter
    def user_my_posts(self, text):
        self._user_my_posts_id = db_set_posts(self.user_my_uid, text)
        db_set_posts_rmq(self.user_my_uid, text, self._user_my_posts_id)

    @property
    def user_my_posts_id(self):
        return self._user_my_posts_id

    @user_my_posts_id.setter
    def user_my_posts_id(self, post_id):
        self._user_my_posts_id = post_id

    @user_my_posts_id.deleter
    def user_my_posts_id(self):
        db_del_posts(self.user_my_uid, self.user_my_posts_id)

    # Get posts of friends
    @property
    def user_friend_posts(self):
        friend_posts = db_get_posts_redis(self._user_friend_posts_offset, self._user_friend_posts_limit, self.user_my_uid)
        return friend_posts

    @user_friend_posts.setter
    def user_friend_posts(self, page):
        self._user_friend_posts_offset = page[0]
        self._user_friend_posts_limit = page[1]

    @property
    def user_my_friends(self):
        my_friends = db_get_followers(self.user_my_uid)
        return my_friends

    @user_my_friends.setter
    def user_my_friends(self, user_my_friends):
        db_set_followers(self.user_my_uid, user_my_friends)

    @property
    def user_my_del_friends(self):
        return self._user_my_del_friends

    @user_my_del_friends.setter
    def user_my_del_friends(self, user_my_del_friends):
        self._user_my_del_friends = user_my_del_friends

    @user_my_del_friends.deleter
    def user_my_del_friends(self):
        db_del_followers(self.user_my_uid, self._user_my_del_friends)
